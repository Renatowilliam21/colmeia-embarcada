# Guia de Desenvolvimento — Needle 2 + Colmeia v2.0 (ERCEMAPI 2026)

Placa de referência confirmada: **Sparkle IoT XH-S3E N16R8** (ESP32-S3-WROOM-1,
16 MB flash, 8 MB PSRAM octal). A ESP32-S3-DevKitC-1 entra como placa secundária
para comparação de latência, **assim que confirmar a variante de memória** com
`esptool.py --port /dev/ttyACM0 flash_id` (ou `idf.py monitor` para ver o log de
PSRAM no boot). Até lá, todo o desenvolvimento segue só na Sparkle.

---

## Etapa 1 — Ambiente (hoje)

```bash
# ESP-IDF v5.5+
git clone -b v5.5 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf && ./install.sh esp32s3
. ./export.sh

# host tools + repo de referencia
python3 -m venv .venv
.venv/bin/pip install numpy rich pyserial huggingface_hub sentencepiece
git clone https://github.com/andrisgauracs/needle-2-esp32.git
cd needle-2-esp32

# modelo (13.7 MB)
.venv/bin/python -c "
from huggingface_hub import hf_hub_download; import shutil, os
os.makedirs('model', exist_ok=True)
shutil.copy(hf_hub_download('Cactus-Compute/needle2','needle2.cact'),
            'model/needle2.cact')"
```

## Etapa 2 — Validar a placa com o exemplo padrão (antes de tocar no schema próprio)

```bash
cd esp32/needle_demo
idf.py set-target esp32s3
idf.py menuconfig
```

Dentro do `menuconfig`, checar/ajustar (são os três pontos que o próprio
repositório aponta como causa da maioria dos problemas silenciosos):

- `Component config → ESP PSRAM`: `Octal Mode PSRAM` habilitado (`CONFIG_SPIRAM_MODE_OCT=y`), velocidade 80 MHz (`CONFIG_SPIRAM_SPEED_80M=y`).
- `Component config → ESP System Settings → CPU frequency`: 240 MHz (`CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ_240=y`).
- `Component config → ESP System Settings → Channel for console output`: deixar no padrão (**não** marcar `CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG`). Se a Sparkle usa USB nativo em vez de ponte UART própria, esse é o ponto a testar primeiro caso não saia nada na serial — inverter essa opção é o primeiro diagnóstico, não assumir que a placa está com defeito.

```bash
idf.py build
idf.py -p /dev/ttyACM0 flash
cd ../..
esptool.py --chip esp32s3 -p /dev/ttyACM0 -b 921600 \
    write_flash 0x210000 model/needle2.cact
```

Depois, validar com a TUI de referência antes de qualquer mudança:

```bash
.venv/bin/python tools/needle_tui.py --serial /dev/ttyACM0
```

Critério de saída desta etapa: LED pisca 3x no boot (prime do prompt) e um
comando de teste do exemplo padrão (`led.json`) retorna uma chamada `ACT`
coerente. Só depois disso faz sentido trocar o schema.

## Etapa 3 — Trocar `tools/led.json` pelo schema Colmeia

Usar a versão compactada (sem espaços) do schema já desenhado — o repositório
avisa que um schema indentado degrada a precisão silenciosamente:

```json
[{"name":"consultar_status_colmeia","description":"Consulta peso, temperatura e umidade atuais de uma colmeia","parameters":{"type":"object","properties":{"colmeia_id":{"type":"integer","minimum":1,"maximum":50}},"required":["colmeia_id"]}},{"name":"listar_colmeias_alerta","description":"Lista colmeias com peso, temperatura ou umidade fora da faixa normal","parameters":{"type":"object","properties":{}}},{"name":"ativar_modo_inspecao","description":"Pausa alertas e aumenta frequencia de leitura durante inspecao manual","parameters":{"type":"object","properties":{"colmeia_id":{"type":"integer","minimum":1,"maximum":50},"duracao_min":{"type":"integer","minimum":5,"maximum":60}},"required":["colmeia_id","duracao_min"]}}]
```

Handlers em `esp32/needle_demo/main/main.c`, entre os marcadores
`YOUR TOOLS START HERE` / `END HERE`. Para este experimento, **dados mockados**
são aceitáveis e devem ser declarados como tal no artigo — o objetivo é medir
a interpretação do comando, não a leitura real do sensor:

```c
static void tool_consultar_status_colmeia(const char *args)
{
    int id = (int)arg_num(args, "colmeia_id", -1);
    if (id < 1) { printf("ACT none\n"); fflush(stdout); return; }
    /* dados mockados para este experimento */
    printf("ACT status colmeia_id=%d peso=18.4 temp=34.2 umid=61.0\n", id);
    fflush(stdout);
}

static void tool_listar_colmeias_alerta(const char *args)
{
    (void)args;
    printf("ACT alerta colmeias=3,7\n");
    fflush(stdout);
}

static void tool_ativar_modo_inspecao(const char *args)
{
    int id  = (int)arg_num(args, "colmeia_id", -1);
    int dur = (int)arg_num(args, "duracao_min", -1);
    if (id < 1) { printf("ACT none\n"); fflush(stdout); return; }
    printf("ACT inspecao colmeia_id=%d duracao_min=%d\n", id, dur);
    fflush(stdout);
}
```

E registrar na `TOOL_TABLE`:

```c
static const struct { const char *name; tool_fn fn; } TOOL_TABLE[] = {
    { "consultar_status_colmeia", tool_consultar_status_colmeia },
    { "listar_colmeias_alerta",   tool_listar_colmeias_alerta },
    { "ativar_modo_inspecao",     tool_ativar_modo_inspecao },
};
```

Rebuild e flash (não precisa regravar o modelo, só o firmware):

```bash
idf.py build && idf.py -p /dev/ttyACM0 flash
```

## Etapa 4 — Rodar os 36 casos de forma automatizada (não manual)

Rodar 36 frases uma a uma pela TUI interativa é lento e sujeito a erro de
transcrição do resultado. Melhor **estender o `tools/needle_tui.py` existente**
em vez de reescrever o protocolo serial do zero — ele já sabe conversar com a
placa; falta só um modo batch. Abrir o arquivo, identificar a função que envia
uma requisição e lê a resposta (é a peça que a TUI interativa já usa a cada
prompt), e reaproveitá-la num laço:

```python
# tools/run_dataset.py — esqueleto, adaptar aos nomes reais das funções
# encontradas em needle_tui.py (enviar_prompt / ler_resposta ou equivalente)
import json, time, csv
from needle_tui import conectar_serial, enviar_e_receber  # nomes de exemplo

with open("colmeia-needle2-dataset-teste.json") as f:
    dataset = json.load(f)["casos"]

porta = conectar_serial("/dev/ttyACM0")
resultados = []

for caso in dataset:
    inicio = time.time()
    saida = enviar_e_receber(porta, caso["frase"])
    duracao = time.time() - inicio
    resultados.append({
        "id": caso["id"],
        "categoria": caso["categoria"],
        "frase": caso["frase"],
        "saida_bruta": saida,
        "duracao_s": round(duracao, 1),
    })
    print(f"[{caso['id']:02d}] {duracao:5.1f}s  {caso['frase'][:40]:40}  -> {saida}")

with open("resultados_brutos.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=resultados[0].keys())
    w.writeheader()
    w.writerows(resultados)
```

Isso gera um `resultados_brutos.csv` com a saída literal de cada uma das 36
frases e o tempo de resposta — a base direta das tabelas do artigo. A
classificação (acerto exato / parcial / erro / vazio correto / vazio incorreto)
comparando com `argumentos_esperados` do dataset é feita depois, manualmente ou
com um segundo script pequeno, já que são poucos casos (36) e a checagem manual
reduz risco de erro de parsing às vésperas do prazo.

## Etapa 5 — Checklist antes de começar a escrever

- [ ] `resultados_brutos.csv` com as 36 linhas preenchidas.
- [ ] Classificação de cada caso feita (coluna extra: `veredito`).
- [ ] Métricas agregadas calculadas: acurácia exata, taxa de bem-formado, taxa
      de rejeição correta (categoria `fora_escopo`), taxa de omissão correta
      (categoria `parametro_implicito`), latência média/mín/máx.
- [ ] Se sobrar tempo: repetir a rodada 2-3x para os casos que falharam, para
      distinguir erro sistemático de variação de amostragem (o modelo não é
      determinístico).
- [ ] Anotar qualquer comportamento inesperado nos casos `ambiguos` — são
      material de discussão, não ruído a descartar.

Com o CSV pronto, o próximo passo natural é o esqueleto LaTeX no template SBC
para encaixar os resultados direto nas tabelas.
