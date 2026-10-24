/* Colmeia Embarcada: Needle 2 on ESP32-S3, simulated apiculture tools.
 *
 * The 13.1 MB model lives in its own flash partition and is memory-mapped, so
 * the engine reads weights in place and never copies them into RAM (there is
 * nowhere near enough). Activations and the KV cache go to octal PSRAM via
 * ND_ALLOC.
 *
 * Line protocol on the console UART, matching tools/needle_tui.py:
 *   in : one request per line
 *   out: EVT / TOK / CONF / ACT / ERR lines
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <limits.h>

#include "esp_heap_caps.h"
#include "esp_partition.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "nd_cact.h"
#include "nd_grammar.h"
#include "nd_model.h"
#include "nd_sample.h"
#include "nd_tokenizer.h"
#include "nd_quant.h"
#include "freertos/semphr.h"

#define MAX_NEW        96
#define ND_LINE_MAX    256   /* not LINE_MAX: that is taken by limits.h */

#include "tools_schema.h"
#include "colmeia_tools.h"

/* The schema is generated from firmware/tools/colmeia.json at build time; see
 * main/CMakeLists.txt. Edit that JSON, not this file. */
static const char TOOLS_RAW[] = ND_TOOLS_JSON;

/* Compacted at boot: the model was trained on whitespace-free schemas, and an
 * indented one degrades it silently (it starts naming tools that were never
 * declared). Doing this here means the JSON file's formatting is free. */
static char TOOLS_JSON[sizeof(TOOLS_RAW)];

static nd_model             s_model;
static nd_grammar           s_grammar;

/* ------------------------------------------------- second-core GEMV worker
 *
 * Every matvec is independent across output rows, so the row range is split
 * in half and core 1 runs one half while core 0 runs the other. Both halves
 * read disjoint weight slices and write disjoint outputs, so no locking is
 * needed beyond the start/done handshake. */

static SemaphoreHandle_t s_go, s_done;
static nd_row_fn         s_fn;
static void             *s_ctx;
static uint32_t          s_r0, s_r1;

static void worker_task(void *arg)
{
    for (;;) {
        xSemaphoreTake(s_go, portMAX_DELAY);
        s_fn(s_ctx, s_r0, s_r1);
        xSemaphoreGive(s_done);
    }
}

static void rows_dual_core(nd_row_fn fn, void *ctx, uint32_t nrows)
{
    uint32_t half = nrows / 2;

    /* Below this the handshake costs more than the work it saves. Attention
     * splits only 8 heads at a time, but each head is ~10K MACs, far above the
     * ~15 us handshake. */
    if (half < 2 || !s_go) {
        fn(ctx, 0, nrows);
        return;
    }
    s_fn  = fn;
    s_ctx = ctx;
    s_r0  = half;
    s_r1  = nrows;
    xSemaphoreGive(s_go);
    fn(ctx, 0, half);
    xSemaphoreTake(s_done, portMAX_DELAY);
}

static void worker_start(void)
{
    s_go   = xSemaphoreCreateBinary();
    s_done = xSemaphoreCreateBinary();
    xTaskCreatePinnedToCore(worker_task, "nd_worker", 4096, NULL,
                            configMAX_PRIORITIES - 2, NULL, 1);
    nd_parallel_rows = rows_dual_core;
}

/* ------------------------------------------------------------ argument access
 *
 * The call is grammar-constrained, so it is already well-formed and contains
 * only declared keys - a full JSON parser would be dead weight. These read a
 * field out of the arguments object by name.
 *
 * Tool handlers below use these; they are the only JSON you need to touch when
 * adding a tool. */

static int arg_str(const char *json, const char *key, char *out, size_t cap)
{
    char        quoted[ND_GR_STRLEN + 4];
    const char *p;
    size_t      w = 0;

    snprintf(quoted, sizeof(quoted), "\"%s\"", key);
    p = strstr(json, quoted);
    if (!p)
        return 0;
    p = strchr(p + strlen(quoted), ':');
    if (!p)
        return 0;
    p = strchr(p, '"');
    if (!p)
        return 0;
    p++;
    while (*p && *p != '"' && w + 1 < cap)
        out[w++] = *p++;
    out[w] = '\0';
    return w > 0;
}

static float arg_num(const char *json, const char *key, float dflt)
{
    char        quoted[ND_GR_STRLEN + 4];
    const char *p;

    snprintf(quoted, sizeof(quoted), "\"%s\"", key);
    p = strstr(json, quoted);
    if (!p)
        return dflt;
    p = strchr(p + strlen(quoted), ':');
    if (!p)
        return dflt;
    return (float)atof(p + 1);
}

__attribute__((unused))    /* provided for handlers with boolean fields */
static int arg_bool(const char *json, const char *key, int dflt)
{
    char        quoted[ND_GR_STRLEN + 4];
    const char *p;

    snprintf(quoted, sizeof(quoted), "\"%s\"", key);
    p = strstr(json, quoted);
    if (!p)
        return dflt;
    p = strchr(p + strlen(quoted), ':');
    if (!p)
        return dflt;
    return strncmp(p + 1, "true", 4) == 0 || strncmp(p + 2, "true", 4) == 0;
}

/* ===========================================================================
 *                 COLMEIA EMBARCADA — FERRAMENTAS SIMULADAS
 * ======================================================================== */
typedef void (*tool_fn)(const char *args);

static const struct {
    const char *name;
    tool_fn fn;
} TOOL_TABLE[] = {
    { "consultar_status_colmeia", colmeia_consultar_status },
    { "listar_colmeias_alerta", colmeia_listar_alertas },
    { "ativar_modo_inspecao", colmeia_ativar_inspecao },
};



/* PT-15.3.10: strict, single-call parser. Reject partial/multiple tool calls.
 * The handlers are SIMULATED. This parser deliberately accepts only the
 * integer-only schema currently used by Colmeia Embarcada. */
static const char *skip_ws(const char *p)
{
    while (*p && isspace((unsigned char)*p)) p++;
    return p;
}

static int parse_literal(const char **pp, char expected)
{
    const char *p = skip_ws(*pp);
    if (*p != expected) return 0;
    *pp = p + 1;
    return 1;
}

static int parse_text(const char **pp, char *out, size_t cap)
{
    const char *p = skip_ws(*pp);
    size_t n = 0;
    if (*p++ != '"') return 0;
    while (*p && *p != '"') {
        /* No escaped characters are needed in our tool names/keys. */
        if (*p == '\\' || (unsigned char)*p < 0x20 || n + 1 >= cap) return 0;
        out[n++] = *p++;
    }
    if (*p != '"') return 0;
    out[n] = 0;
    *pp = p + 1;
    return 1;
}

static int parse_int(const char **pp, int *value)
{
    const char *p = skip_ws(*pp);
    char *end;
    long v;
    if (*p == '+' || (!isdigit((unsigned char)*p) && *p != '-')) return 0;
    v = strtol(p, &end, 10);
    if (end == p || v < INT_MIN || v > INT_MAX) return 0;
    if (*end && *end != ',' && *end != '}' && !isspace((unsigned char)*end)) return 0;
    *value = (int)v;
    *pp = end;
    return 1;
}

static int parse_args(const char **pp, int *id, int *duration,
                      unsigned *seen)
{
    const char *p = *pp;
    if (!parse_literal(&p, '{')) return 0;
    if (parse_literal(&p, '}')) { *pp = p; return 1; }
    for (;;) {
        char key[40];
        int value;
        unsigned bit;
        if (!parse_text(&p, key, sizeof(key)) || !parse_literal(&p, ':') ||
            !parse_int(&p, &value)) return 0;
        if (!strcmp(key, "colmeia_id")) {
            bit = 1;
            *id = value;
        } else if (!strcmp(key, "duracao_min")) {
            bit = 2;
            *duration = value;
        } else return 0;
        if (*seen & bit) return 0;
        *seen |= bit;
        if (parse_literal(&p, '}')) break;
        if (!parse_literal(&p, ',')) return 0;
    }
    *pp = p;
    return 1;
}

static void dispatch_call(const char *generated)
{
    const char *p = generated;
    char name[64] = "", key[40];
    int id = 0, duration = 0;
    unsigned seen = 0, fields = 0;
    char args[96];
    size_t i;

    /* Reasoning is allowed but must close before the tool call. */
    p = skip_ws(p);
    if (!strncmp(p, "<think>", 7)) {
        const char *end = strstr(p + 7, "</think>");
        if (!end) goto reject;
        p = skip_ws(end + strlen("</think>"));
    }
    if (strncmp(p, "<tool_call>", 11)) goto reject;
    p += 11;
    if (!parse_literal(&p, '[') || !parse_literal(&p, '{')) goto reject;
    for (;;) {
        if (!parse_text(&p, key, sizeof(key)) || !parse_literal(&p, ':')) goto reject;
        if (!strcmp(key, "name")) {
            if (fields & 1 || !parse_text(&p, name, sizeof(name))) goto reject;
            fields |= 1;
        } else if (!strcmp(key, "arguments")) {
            if (fields & 2 || !parse_args(&p, &id, &duration, &seen)) goto reject;
            fields |= 2;
        } else goto reject;
        if (parse_literal(&p, '}')) break;
        if (!parse_literal(&p, ',')) goto reject;
    }
    if (!parse_literal(&p, ']')) goto reject; /* rejects multiple calls */
    p = skip_ws(p);
    if (strncmp(p, "</tool_call>", 12)) goto reject;
    p = skip_ws(p + 12);
    if (*p != 0 || fields != 3) goto reject;

    if (!strcmp(name, "consultar_status_colmeia")) {
        if (seen != 1 || id < 1 || id > 50) goto reject;
        snprintf(args, sizeof(args), "{\"colmeia_id\":%d}", id);
    } else if (!strcmp(name, "listar_colmeias_alerta")) {
        if (seen != 0) goto reject;
        strcpy(args, "{}");
    } else if (!strcmp(name, "ativar_modo_inspecao")) {
        if (seen != 3 || id < 1 || id > 50 || duration < 5 || duration > 60)
            goto reject;
        snprintf(args, sizeof(args), "{\"colmeia_id\":%d,\"duracao_min\":%d}",
                 id, duration);
    } else goto reject;

    for (i = 0; i < sizeof(TOOL_TABLE) / sizeof(TOOL_TABLE[0]); i++) {
        if (!strcmp(TOOL_TABLE[i].name, name)) {
            TOOL_TABLE[i].fn(args);
            return;
        }
    }
reject:
    printf("ERR invalid_or_incomplete_tool_call\n");
    printf("ACT none\n");
    fflush(stdout);
}

/* -------------------------------------------------------------- inference */

static int s_show_think = 0;   /* toggled from the host with "!think" */

/* Prefill the constant part of the prompt once and snapshot it. Every request
 * then resumes from here, so only the query and the assistant header are
 * prefilled per turn - ~13 tokens instead of ~171. */
static void kv_verify(const nd_model *m, const char *phase);

static void prime_prefix(void)
{
    static uint32_t ids[512];
    static char     pre[1024];
    int64_t         t0 = esp_timer_get_time();
    int             n;
    int             i;

    snprintf(pre, sizeof(pre), "<|im_start|>user\n<tools>%s</tools>", TOOLS_JSON);

    nd_model_reset(&s_model);
    ids[0] = ND_BOS_ID;
    n = nd_tok_encode(&s_model.tok, pre, strlen(pre), ids + 1,
                      (uint32_t)(sizeof(ids) / sizeof(ids[0]) - 1));
    if (n < 0) {
        printf("ERR prefix_too_long\n");
        return;
    }
    n += 1;
    printf("EVT priming tokens=%d (one-time; every later request reuses this)\n", n);
    fflush(stdout);
    for (i = 0; i < n; i++) {
        nd_model_step_hidden(&s_model, (uint32_t)ids[i]);
        if ((i + 1) % 8 == 0 || i + 1 == n) {
            double el = (esp_timer_get_time() - t0) / 1000000.0;
            double eta = el / (i + 1) * (n - i - 1);
            printf("EVT priming %d/%d  %.0f%%  elapsed=%.0fs  eta=%.0fs\n",
                   i + 1, n, 100.0 * (i + 1) / n, el, eta);
            fflush(stdout);
        }
    }
    if (nd_model_snapshot(&s_model) != 0) {
        printf("ERR kv_snapshot_failed\n");
        fflush(stdout);
        abort();
    }
    kv_verify(&s_model, "after_snapshot");
    printf("EVT prefix tokens=%d ms=%.0f sink=%u (cached for all requests)\n",
           n, (esp_timer_get_time() - t0) / 1000.0, (unsigned)s_model.n_sink);
    fflush(stdout);
}


/* PT-15.3.17-D: diagnostico experimental do cache KV. */
static void kv_verify(const nd_model *m, const char *phase)
{
    uint32_t li;
    size_t kb, sb;
    unsigned dk = 0, dv = 0, dks = 0, dvs = 0;

    if (!m->has_snap) {
        printf("KV_DIAG phase=%s result=NO_SNAPSHOT\n", phase);
        return;
    }

    if (m->snap_kv_tail == 0) {
        printf("KV_DIAG phase=%s tail=0 result=NOT_APPLICABLE\n", phase);
        return;
    }

    if (!m->snap_k_cache || !m->snap_v_cache ||
        !m->snap_k_scale || !m->snap_v_scale) {
        printf("KV_DIAG phase=%s result=INVALID_SNAPSHOT\n", phase);
        return;
    }

    kb = (size_t)m->snap_kv_tail * m->kv_dim;
    sb = (size_t)m->snap_kv_tail * m->n_kv_heads;

    for (li = 0; li < m->n_layers; li++) {
        size_t off_k =
            ((size_t)li * m->window + m->n_sink) * m->kv_dim;
        size_t off_s =
            ((size_t)li * m->window + m->n_sink) * m->n_kv_heads;

        if (memcmp(m->k_cache + off_k,
                   m->snap_k_cache + (size_t)li * kb, kb))
            dk++;

        if (memcmp(m->v_cache + off_k,
                   m->snap_v_cache + (size_t)li * kb, kb))
            dv++;

        if (memcmp(m->k_scale + off_s,
                   m->snap_k_scale + (size_t)li * sb,
                   sb * sizeof(float)))
            dks++;

        if (memcmp(m->v_scale + off_s,
                   m->snap_v_scale + (size_t)li * sb,
                   sb * sizeof(float)))
            dvs++;
    }

    printf(
        "KV_DIAG phase=%s pos=%u tail=%u layers=%u "
        "diff_k=%u diff_v=%u diff_ks=%u diff_vs=%u result=%s\n",
        phase, (unsigned)m->pos,
        (unsigned)m->snap_kv_tail,
        (unsigned)m->n_layers,
        dk, dv, dks, dvs,
        (dk || dv || dks || dvs) ? "DIFF" : "PASS"
    );
    fflush(stdout);
}

static void run_inference(const char *query)
{
    static uint32_t ids[512];
    static char     out[1024];
    static char     suf[512];
    nd_sampler      smp;
    const float    *lg = NULL;
    int             n;
    uint32_t        i, produced = 0, w = 0;
    int             truncated = 0, finished = 0, generation_error = 0;
    int64_t         t0;
    double          pre_ms;

    snprintf(suf, sizeof(suf),
             "\n%s<|im_end|>\n<|im_start|>assistant\n", query);

    /* Resume from the cached prefix rather than re-running it. */
    kv_verify(&s_model, "before_rewind");
    nd_model_rewind(&s_model);
    kv_verify(&s_model, "after_rewind");
    nd_sampler_init(&smp, &s_model.tok, &s_grammar);

    n = nd_tok_encode_ex(&s_model.tok, suf, strlen(suf), ids,
                         (uint32_t)(sizeof(ids) / sizeof(ids[0])), 0);
    if (n < 0) {
        printf("ERR prompt_too_long\n");
        return;
    }

    t0 = esp_timer_get_time();
    for (i = 0; i < (uint32_t)n; i++) {
        lg = nd_model_step_hidden(&s_model, ids[i]);
        printf("EVT reading %u/%d\n", (unsigned)(i + 1), n);
        fflush(stdout);
    }
    pre_ms = (esp_timer_get_time() - t0) / 1000.0;

    printf("EVT prefill tokens=%d ms=%.0f tps=%.2f sink=%u\n",
           n, pre_ms, n / (pre_ms / 1000.0), (unsigned)s_model.n_sink);
    fflush(stdout);

    /* Optionally skip the reasoning block: force an empty <think></think> and
     * open the call directly. Verified to produce identical calls at roughly
     * half the generated tokens. */
    if (!s_show_think) {
        uint32_t forced[8], nf = 0, fi, tmp[4];
        int tn;
        forced[nf++] = ND_THINK_START_ID;
        forced[nf++] = ND_THINK_END_ID;
        tn = nd_tok_encode_ex(&s_model.tok, "\n", 1, tmp, 4, 0);
        for (fi = 0; fi < (uint32_t)tn; fi++)
            forced[nf++] = tmp[fi];
        forced[nf++] = ND_TOOL_CALL_START_ID;
        for (fi = 0; fi < nf; fi++) {
            char pc[128];
            nd_sample_accept(&smp, forced[fi]);
            nd_tok_decode_ex(&s_model.tok, &forced[fi], 1, pc, sizeof(pc), 0);
            if (w + strlen(pc) < sizeof(out) - 1) { strcpy(out + w, pc); w += strlen(pc); }
            lg = nd_model_step_hidden(&s_model, forced[fi]);
        }
    }

    t0 = esp_timer_get_time();
    for (i = 0; i < MAX_NEW; i++) {
        uint32_t id = nd_sample_hidden(&s_model, &smp, lg);
        char     piece[256];
        uint32_t k;

        if (id == (uint32_t)-1) {
            printf("ERR no_legal_token\n");
            generation_error = 1;
            break;
        }
        if (id == ND_EOS_ID || id == ND_IM_END_ID) {
            finished = 1;
            break;
        }
        nd_sample_accept(&smp, id);

        nd_tok_decode_ex(&s_model.tok, &id, 1, piece, sizeof(piece), 0);
        printf("TOK ");
        for (k = 0; piece[k]; k++) {
            if (piece[k] == '\n')      printf("\\n");
            else if (piece[k] != '\r') putchar(piece[k]);
        }
        printf("\n");
        fflush(stdout);

        if (w + strlen(piece) < sizeof(out) - 1) {
            strcpy(out + w, piece);
            w += strlen(piece);
        } else {
            truncated = 1;
            break;
        }
        produced++;
        lg = nd_model_step_hidden(&s_model, id);
        if (strstr(out, "</tool_call>")) {
            finished = 1;
            break;
        }
    }
    out[w] = '\0';

    {
        double dec_ms = (esp_timer_get_time() - t0) / 1000.0;
        float  conf   = nd_model_confidence(&s_model);
        if (conf >= 0.0f)
            printf("CONF %.4f\n", conf);
        printf("EVT done tokens=%u ms=%.0f tps=%.2f\n", (unsigned)produced,
               dec_ms, produced ? produced / (dec_ms / 1000.0) : 0.0);
        fflush(stdout);
    }

    if (!finished || truncated || generation_error) {
        printf("ERR generation_incomplete tokens=%u limit=%d overflow=%d\n",
               (unsigned)produced, MAX_NEW, truncated);
        printf("ACT none\n");
        fflush(stdout);
        return;
    }
    dispatch_call(out);
}

/* ------------------------------------------------------------------- main */

void app_main(void)
{
    const esp_partition_t     *part;
    esp_partition_mmap_handle_t handle;
    const void                *blob = NULL;
    const char                *gerr = NULL;

    vTaskDelay(pdMS_TO_TICKS(500));
    worker_start();

    if (nd_json_compact(TOOLS_RAW, strlen(TOOLS_RAW),
                        TOOLS_JSON, sizeof(TOOLS_JSON)) < 0) {
        printf("ERR schema_too_large\n");
        return;
    }

    part = esp_partition_find_first(ESP_PARTITION_TYPE_DATA, 0x40, "model");
    if (!part) {
        printf("ERR no_model_partition\n");
        return;
    }
    if (esp_partition_mmap(part, 0, part->size, ESP_PARTITION_MMAP_DATA,
                           &blob, &handle) != ESP_OK) {
        printf("ERR mmap_failed size=%u\n", (unsigned)part->size);
        return;
    }
    printf("EVT mapped partition=%u bytes at %p\n", (unsigned)part->size, blob);

    if (nd_model_open(&s_model, blob, part->size) != 0) {
        printf("ERR model_open\n");
        return;
    }
    if (nd_grammar_compile(&s_grammar, TOOLS_JSON, strlen(TOOLS_JSON), &gerr) != 0) {
        printf("ERR grammar %s\n", gerr ? gerr : "?");
        return;
    }

    printf("EVT ready model=needle2 layers=%u d_model=%u vocab=%u window=%u "
           "tools=%u psram_free=%u internal_free=%u\n",
           (unsigned)s_model.n_layers, (unsigned)s_model.d_model,
           (unsigned)s_model.vocab, (unsigned)s_model.window,
           (unsigned)s_grammar.n_tools,
           (unsigned)heap_caps_get_free_size(MALLOC_CAP_SPIRAM),
           (unsigned)heap_caps_get_free_size(MALLOC_CAP_INTERNAL));
    fflush(stdout);
    prime_prefix();

    /* Startup benchmark: a fixed number of steps with the KV cache cold, so
     * kernel changes can be measured in seconds instead of running a whole
     * 9-minute request. */
    {
        const int N = 6;
        int64_t   t;
        int       i;
        nd_model_rewind(&s_model);
        t = esp_timer_get_time();
        for (i = 0; i < N; i++)
            nd_model_step_hidden(&s_model, (uint32_t)(100 + i));
        {
            double ms = (esp_timer_get_time() - t) / 1000.0;
            printf("EVT bench tokens=%d ms=%.0f ms_per_tok=%.0f tps=%.3f\n",
                   N, ms, ms / N, N / (ms / 1000.0));
#ifdef ND_PROFILE
            {   /* Per-phase breakdown; enable ND_PROFILE in the component's
                 * CMakeLists to get it. Off by default: the timers add work
                 * to every layer and the output is noise during a demo. */
                static const char *PN[ND_P_COUNT] = {
                    "proj2bit", "attention", "hadamard", "mhc_phi4",
                    "engram", "logits4", "prep+lut", "confpool" };
                int p;
                for (p = 0; p < ND_P_COUNT; p++)
                    printf("EVT prof %-10s %8.1f ms  %5.1f%%\n", PN[p],
                           nd_prof[p] / 1000.0 / N,
                           100.0 * nd_prof[p] / 1000.0 / ms);
            }
#endif
            fflush(stdout);
        }
        nd_model_rewind(&s_model);
    }

    printf("\n");
    printf("EVT ==================================================\n");
    printf("EVT  READY - type a request and press enter\n");
    printf("EVT  e.g. \"Qual e o status da colmeia 5?\"\n");
    printf("EVT  commands: !think (toggle reasoning; default=0)\n");
    printf("EVT ==================================================\n\n");
    fflush(stdout);

    for (;;) {
        char line[ND_LINE_MAX];
        int  len = 0;

        /* Read one request line from the console. */
        for (;;) {
            int c = getchar();
            if (c == EOF) {
                vTaskDelay(pdMS_TO_TICKS(20));
                continue;
            }
            if (c == '\r')
                continue;
            if (c == '\n')
                break;
            if (len < ND_LINE_MAX - 1)
                line[len++] = (char)c;
        }
        line[len] = '\0';
        if (len == 0)
            continue;

        /* Reasoning control. "!think 0" / "!think 1" set it explicitly so a
         * reconnecting client is never at the mercy of the current state;
         * bare "!think" still toggles for interactive use. */
        if (!strncmp(line, "!think", 6)) {
            if (line[6] == ' ')
                s_show_think = (line[7] != '0');
            else
                s_show_think = !s_show_think;
            printf("EVT think=%d\n", s_show_think);
            fflush(stdout);
            continue;
        }

        run_inference(line);
    }
}
