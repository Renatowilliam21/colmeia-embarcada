import json, csv, re, math, glob, statistics as st
from collections import Counter, defaultdict
from pathlib import Path

ESP = Path("resultados_esp32/20261025T164514Z_ESP32S3/raw_results.jsonl")
PT05 = Path("artefatos/avaliacao/pt05_resultados_detalhados.csv")
REV = Path("artefatos/dataset/gabarito_revisado_posteriormente.json")
REPRO = sorted(glob.glob("resultados_novos/*/raw_results.jsonl"))[0]

def norm(calls):
    out = []
    for c in calls or []:
        a = c.get("arguments") or {}
        out.append((c.get("name"), tuple(sorted(a.items()))))
    return out

def pj(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return json.loads(s)
    except Exception:
        return None

def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)

def mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)

def outcome(exp, got):
    if exp == got:
        return "acerto (abstencao correta)" if not exp else "acerto exato"
    if not exp:
        return "chamada indevida"
    if not got:
        return "omissao (nao chamou)"
    if [n for n, _ in exp] == [n for n, _ in got]:
        return "erro de argumento"
    return "erro de ferramenta/sequencia"

esp = {}
for l in ESP.read_text(encoding="utf-8").splitlines():
    r = json.loads(l)
    m = re.search(r"CONF ([\d.]+)", "\n".join(r["serial_lines"]))
    esp[r["case_id"]] = dict(cat=r["category"], calls=norm(r["parsed_calls"]),
                             conf=float(m.group(1)) if m else None,
                             ac=r.get("answer_correct"), ce=r.get("correctness_evaluated"))
ids = sorted(esp)

host = {}
for row in csv.DictReader(open(PT05, encoding="utf-8")):
    i = int(row["id"])
    host[i] = dict(exp=pj(row["esperado"]), pred=norm(pj(row["predito"])), em=row["exact_match_original"])

rev = {c["id"]: norm(c["chamadas_esperadas_revisadas"])
       for c in json.load(open(REV, encoding="utf-8"))["casos"]}

repro = {}
rows_repro = [json.loads(l) for l in open(REPRO, encoding="utf-8")]
print("chaves repro:", list(rows_repro[0].keys()))
for r in rows_repro:
    repro[r.get("case_id", r.get("id"))] = norm(r.get("parsed_calls"))

print("\n=== campos de correcao no JSONL do ESP32 ===")
print("answer_correct:", Counter(str(esp[i]["ac"]) for i in ids), "| correctness_evaluated:", Counter(str(esp[i]["ce"]) for i in ids))

# historico
nonev = [i for i in ids if host[i]["exp"] is None]
ev = [i for i in ids if host[i]["exp"] is not None]
hh = {i: (host[i]["pred"] == norm(host[i]["exp"])) for i in ev}
he = {i: (esp[i]["calls"] == norm(host[i]["exp"])) for i in ev}
print("\n=== GABARITO HISTORICO ===")
print("nao avaliaveis:", nonev, "| avaliaveis:", len(ev))
print("host pt05 (coluna exact_match_original=True):", sum(host[i]["em"] == "True" for i in ids), "| recalculado:", sum(hh.values()))
for nome, d in (("host", hh), ("esp32", he)):
    k = sum(d.values()); lo, hi = wilson(k, len(ev))
    print(f"{nome}: {k}/{len(ev)} = {100*k/len(ev):.2f}%  IC95% {lo:.1f}-{hi:.1f}")
b = sum(hh[i] and not he[i] for i in ev); c = sum(he[i] and not hh[i] for i in ev)
print(f"McNemar exato (so host certo={b}, so esp certo={c}): p={mcnemar(b, c):.3f}")

# revisado
rh = {i: (host[i]["pred"] == rev[i]) for i in ids}
re_ = {i: (esp[i]["calls"] == rev[i]) for i in ids}
print("\n=== GABARITO REVISADO (36 casos) ===")
for nome, d in (("host", rh), ("esp32", re_)):
    k = sum(d.values()); lo, hi = wilson(k, len(ids))
    print(f"{nome}: {k}/36 = {100*k/36:.2f}%  IC95% {lo:.1f}-{hi:.1f}")
b = sum(rh[i] and not re_[i] for i in ids); c = sum(re_[i] and not rh[i] for i in ids)
print(f"McNemar exato (so host certo={b}, so esp certo={c}): p={mcnemar(b, c):.3f}")
print("\npor categoria (revisado):  host | esp32")
cats = defaultdict(list)
for i in ids:
    cats[esp[i]["cat"]].append(i)
for cat, lst in cats.items():
    kh = sum(rh[i] for i in lst); ke = sum(re_[i] for i in lst)
    print(f"  {cat:<22} n={len(lst)}  {kh}/{len(lst)} | {ke}/{len(lst)}")
need = [i for i in ids if not rev[i]]
print(f"\nabstencao exigida: {len(need)} casos | chamadas indevidas host={sum(bool(host[i]['pred']) for i in need)} esp32={sum(bool(esp[i]['calls']) for i in need)}")

# host x esp32 e reproducao
dif = [i for i in ids if host[i]["pred"] != esp[i]["calls"]]
print(f"\nhost(pt05) x esp32: sequencias identicas {36-len(dif)}/36; divergem em {dif}")
dr = [i for i in ids if repro.get(i) != host[i]["pred"]]
print(f"host(pt05) x reproducao 25/10: identicas {36-len(dr)}/36; divergem em {dr}")
rr = sum(repro.get(i) == rev[i] for i in ids)
print(f"reproducao 25/10 contra gabarito revisado: {rr}/36")

# confianca
print("\n=== CONFIANCA ESP32 por desfecho (gabarito revisado) ===")
g = defaultdict(list)
out = {i: outcome(rev[i], esp[i]["calls"]) for i in ids}
for i in ids:
    g[out[i]].append(esp[i]["conf"])
for k, v in g.items():
    v = [x for x in v if x is not None]
    print(f"  {k:<30} n={len(v):>2} media={st.mean(v):.3f} min={min(v):.3f} max={max(v):.3f}")
wr = [i for i in ids if not re_[i] and esp[i]["conf"] is not None and esp[i]["conf"] >= 0.90]
rl = [i for i in ids if re_[i] and esp[i]["conf"] is not None and esp[i]["conf"] < 0.90]
print(f"limiar 0.90: erros aceitos automaticamente {len(wr)}/{sum(not re_[i] for i in ids)} {wr} | acertos barrados {len(rl)}/{sum(re_[i] for i in ids)} {rl}")

print("\n=== POR CASO ===")
ok = lambda x: "ok" if x else "x "
for i in ids:
    h = (ok(hh[i]) + "/" + ok(he[i])) if i in hh else "n/a"
    print(f"{i:>2} {esp[i]['cat'][:10]:<10} conf={esp[i]['conf']:.3f} hist[h/e]={h:<6} rev[h/e]={ok(rh[i])}/{ok(re_[i])} {out[i]}")

with open("avaliacao_esp32.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "categoria", "conf", "rev_host", "rev_esp32", "desfecho_esp32", "chamadas_esp32"])
    for i in ids:
        w.writerow([i, esp[i]["cat"], esp[i]["conf"], rh[i], re_[i], out[i], json.dumps(esp[i]["calls"], ensure_ascii=False)])
