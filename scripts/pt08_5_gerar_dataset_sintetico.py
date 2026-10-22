#!/usr/bin/env python3
"""PT-08.5: geração determinística de 180 casos sintéticos candidatos."""

import csv
import hashlib
import json
import random
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261022
rng = random.Random(SEED)

ORIGINAL = ROOT / "dataset/colmeia-needle2-dataset-teste.json"
FINAL = ROOT / "dataset/colmeia-needle2-gabarito-final.json"
SCHEMA = ROOT / "firmware/tools/colmeia.json"

OUT = ROOT / "dataset/synthetic/colmeia-needle2-sintetico-v1.json"
CSV = ROOT / "dataset/synthetic/pt08_5_auditoria.csv"
REPORT = ROOT / "docs/metodologia/pt08_5_relatorio.md"

TARGET = {
    "diretos": 28,
    "variacoes_fala": 36,
    "parametro_implicito": 40,
    "ambiguos": 40,
    "fora_escopo": 36,
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def normalize(s):
    s = unicodedata.normalize("NFKD", s.casefold())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()

def call(name, **kwargs):
    return [{"name": name, "arguments": kwargs}]

def status(i):
    return call("consultar_status_colmeia", colmeia_id=i)

def alertas():
    return call("listar_colmeias_alerta")

def inspecao(i, minutos):
    return call(
        "ativar_modo_inspecao",
        colmeia_id=i,
        duracao_min=minutos
    )

def add(pool, category, phrase, expected, family, rationale):
    pool.append({
        "categoria": category,
        "frase": phrase,
        "chamadas_esperadas_revisadas": expected,
        "familia": family,
        "justificativa": rationale,
        "origem": "sintetico_template",
        "status_validacao": "pendente_revisao_humana",
    })

pool = []

# 1. Comandos diretos: 28
for i in range(1, 51):
    add(pool, "diretos",
        f"Consulte o status atual da colmeia {i}.",
        status(i), "status_direto",
        "Consulta individual com identificador explícito.")

    add(pool, "diretos",
        f"Mostre peso, temperatura e umidade da colmeia {i}.",
        status(i), "sensores_direto",
        "Consulta de variáveis fornecidas pela ferramenta de status.")

for i in range(1, 51):
    for minutos in (5, 15, 25, 40, 60):
        add(pool, "diretos",
            f"Ative o modo inspeção da colmeia {i} por {minutos} minutos.",
            inspecao(i, minutos), "inspecao_direta",
            "Identificador e duração válidos explicitamente informados.")

for frase in (
    "Liste todas as colmeias que estão em alerta.",
    "Quais colmeias apresentam valores fora da faixa normal?",
    "Mostre a relação atual de colmeias em alerta.",
    "Informe quais colmeias estão com alertas ativos.",
):
    add(pool, "diretos", frase, alertas(), "alertas_direto",
        "Consulta de alertas atuais.")

# 2. Variações de fala: 36
for i in range(1, 51):
    for modelo in (
        "Como é que tá a colmeia {i}?",
        "Me diz aí como anda a colmeia {i}.",
        "Dá uma conferida nos dados da colmeia {i}.",
        "Queria saber a situação da colmeia {i}.",
    ):
        add(pool, "variacoes_fala", modelo.format(i=i),
            status(i), "status_coloquial",
            "Paráfrase coloquial de consulta individual.")

    for minutos in (10, 20, 30):
        add(pool, "variacoes_fala",
            f"Bota a colmeia {i} em inspeção por {minutos} minutinhos.",
            inspecao(i, minutos), "inspecao_coloquial",
            "Pedido coloquial com duração determinada.")

for frase in (
    "Tem alguma colmeia dando problema?",
    "Quais colmeias tão pedindo atenção?",
    "Me mostra as colmeias fora do normal.",
    "Tem colmeia com alerta ligado?",
):
    add(pool, "variacoes_fala", frase, alertas(),
        "alertas_coloquial",
        "Paráfrase coloquial de consulta de alertas.")

# 3. Parâmetros implícitos: 40
for i in range(1, 51):
    add(pool, "parametro_implicito",
        f"Coloque a colmeia {i} em modo inspeção.",
        [], "duracao_ausente",
        "Duração obrigatória não informada.")

    add(pool, "parametro_implicito",
        f"Vou abrir a colmeia {i}; pause os alertas.",
        [], "duracao_ausente",
        "Pedido de ação sem duração.")

    add(pool, "parametro_implicito",
        f"Preciso verificar a colmeia {i} rapidinho.",
        [], "intencao_insuficiente",
        "Não há ação executável suficientemente determinada.")

    add(pool, "parametro_implicito",
        f"Ative inspeção na colmeia {i} por alguns minutos.",
        [], "duracao_indeterminada",
        "Duração não quantificada.")

for minutos in (5, 10, 15, 20, 30, 45, 60):
    add(pool, "parametro_implicito",
        f"Ative a inspeção por {minutos} minutos.",
        [], "identificador_ausente",
        "Identificador obrigatório ausente.")

for frase in (
    "Mostre o status da colmeia.",
    "Como estão os sensores?",
    "Quero consultar o peso.",
    "Qual é a temperatura agora?",
):
    add(pool, "parametro_implicito", frase, [],
        "identificador_ausente",
        "Não é possível identificar a colmeia solicitada.")

# 4. Ambíguos: 40
for i in range(1, 51):
    for j in range(i + 1, min(i + 5, 51)):
        add(pool, "ambiguos",
            f"Como estão as colmeias {i} e {j}?",
            status(i) + status(j), "consulta_multipla",
            "Duas consultas individuais identificadas.")

for i in range(1, 51):
    for j in range(i + 1, min(i + 5, 51)):
        add(pool, "ambiguos",
            f"Coloque as colmeias {i} e {j} em inspeção por 20 minutos.",
            [], "acao_multipla_nao_suportada",
            "Política conservadora: não executar ação coletiva.")

for i in range(1, 51):
    add(pool, "ambiguos",
        f"Ative inspeção na colmeia {i} por 3 minutos.",
        [], "duracao_invalida",
        "Duração abaixo do mínimo de 5 minutos.")

    add(pool, "ambiguos",
        f"Ative inspeção na colmeia {i} por 90 minutos.",
        [], "duracao_invalida",
        "Duração acima do máximo de 60 minutos.")

for i in (0, 51, 52, 99):
    add(pool, "ambiguos",
        f"Mostre o status da colmeia {i}.",
        [], "identificador_invalido",
        "Identificador fora do intervalo permitido.")

for referencia in (
    "a que fica atrás do galpão",
    "a colmeia perto da cerca",
    "a caixa do lado da árvore",
    "a colmeia mais distante",
    "aquela colmeia do canto",
    "a colmeia perto do bebedouro",
):
    add(pool, "ambiguos",
        f"Como está {referencia}?",
        [], "referencia_espacial",
        "Referência espacial não mapeada para identificador.")

# 5. Fora do escopo: 36
assuntos = [
    ("previsao_tempo", [
        "Vai chover amanhã?",
        "Qual a previsão de chuva para sábado?",
        "Vai fazer muito vento esta noite?",
        "Qual será a temperatura da cidade amanhã?",
        "Vai ter tempestade no fim de semana?",
        "Como fica a previsão do tempo para o próximo mês?",
    ]),
    ("mercado", [
        "Qual é o preço do mel hoje?",
        "Quanto custa um quilo de cera de abelha?",
        "Qual a cotação do dólar?",
        "Quanto custa uma caixa de madeira?",
        "Qual é o valor do própolis no mercado?",
        "Onde encontro o mel mais barato?",
    ]),
    ("administracao", [
        "Envie uma mensagem para o apicultor.",
        "Cadastre um novo funcionário.",
        "Gere uma nota fiscal.",
        "Exporte todos os dados em PDF.",
        "Envie o relatório por e-mail.",
        "Apague todos os registros antigos.",
    ]),
    ("controle_nao_suportado", [
        "Reinicie o ESP32.",
        "Desligue todos os sensores.",
        "Ligue o ventilador do laboratório.",
        "Atualize o firmware pela internet.",
        "Formate a memória do dispositivo.",
        "Desative permanentemente os alarmes.",
    ]),
    ("conversa_geral", [
        "Bom dia, tudo bem?",
        "Conte uma piada sobre abelhas.",
        "Quem inventou o computador?",
        "Explique a história da apicultura.",
        "Qual é a capital do Brasil?",
        "Obrigado pela ajuda.",
    ]),
    ("analise_nao_suportada", [
        "Calcule a produção anual de mel.",
        "Compare os dados de todas as colmeias no último ano.",
        "Preveja a próxima enxameação.",
        "Diagnostique a doença das abelhas.",
        "Faça um gráfico mensal da produtividade.",
        "Estime o lucro da próxima safra.",
    ]),
]

for familia, frases in assuntos:
    for frase in frases:
        add(pool, "fora_escopo", frase, [], familia,
            "Nenhuma ferramenta disponível atende à solicitação.")

# Deduplicação, inclusive contra os 36 casos originais.
original_data = json.loads(ORIGINAL.read_text(encoding="utf-8"))
original_cases = (
    original_data["casos"] if isinstance(original_data, dict)
    else original_data
)

seen = {normalize(c["frase"]) for c in original_cases}
selected = []

for category, target in TARGET.items():
    candidates = [c for c in pool if c["categoria"] == category]
    rng.shuffle(candidates)
    count = 0

    for candidate in candidates:
        key = normalize(candidate["frase"])
        if key in seen:
            continue
        seen.add(key)
        selected.append(candidate)
        count += 1
        if count == target:
            break

    if count != target:
        raise RuntimeError(
            f"Categoria {category}: gerados {count}, esperados {target}"
        )

for idx, case in enumerate(selected, start=37):
    case["id"] = idx

# Validação do contrato.
tools = {
    tool["name"]: tool
    for tool in json.loads(SCHEMA.read_text(encoding="utf-8"))
}

for case in selected:
    for invocation in case["chamadas_esperadas_revisadas"]:
        name = invocation["name"]
        args = invocation["arguments"]
        spec = tools[name]["parameters"]
        properties = spec.get("properties", {})

        assert set(spec.get("required", [])) <= set(args)
        assert set(args) <= set(properties)

        for key, value in args.items():
            rule = properties[key]
            if rule.get("type") == "integer":
                assert type(value) is int
                assert rule.get("minimum", value) <= value
                assert value <= rule.get("maximum", value)

assert len(selected) == 180
assert len({normalize(c["frase"]) for c in selected}) == 180
assert Counter(c["categoria"] for c in selected) == TARGET

final_data = json.loads(FINAL.read_text(encoding="utf-8"))
assert len(final_data["casos"]) == 36

payload = {
    "protocolo": "PT-08.5",
    "versao": "sintetico-v1-candidato",
    "semente": SEED,
    "status": "pendente_revisao_humana",
    "dataset_original_sha256": sha(ORIGINAL),
    "dataset_final_36_sha256": sha(FINAL),
    "schema_sha256": sha(SCHEMA),
    "quantidade": len(selected),
    "casos": selected,
}

content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

if OUT.exists() and OUT.read_text(encoding="utf-8") != content:
    raise RuntimeError("Dataset sintético existente difere do gerado.")

OUT.write_text(content, encoding="utf-8")

with CSV.open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "id", "categoria", "familia", "frase",
        "gabarito_proposto", "status_validacao"
    ])
    for c in selected:
        writer.writerow([
            c["id"], c["categoria"], c["familia"], c["frase"],
            json.dumps(c["chamadas_esperadas_revisadas"],
                       ensure_ascii=False),
            c["status_validacao"],
        ])

distribution = Counter(c["categoria"] for c in selected)
families = Counter(c["familia"] for c in selected)

lines = [
    "# PT-08.5 — Relatório de geração sintética",
    "",
    "## Proveniência",
    "",
    "- Método: templates controlados e seleção pseudoaleatória.",
    f"- Semente: `{SEED}`",
    f"- SHA-256 original: `{sha(ORIGINAL)}`",
    f"- SHA-256 protocolo de 36 casos: `{sha(FINAL)}`",
    f"- SHA-256 schema: `{sha(SCHEMA)}`",
    f"- SHA-256 dataset sintético: `{sha(OUT)}`",
    "- Estado: candidato, pendente de revisão humana.",
    "",
    "## Distribuição",
    "",
    "| Categoria | Quantidade |",
    "|---|---:|",
]

for category, count in distribution.items():
    lines.append(f"| {category} | {count} |")

lines += [
    "",
    "## Famílias de templates",
    "",
    "| Família | Quantidade |",
    "|---|---:|",
]

for family, count in sorted(families.items()):
    lines.append(f"| {family} | {count} |")

lines += [
    "",
    "## Limitações e decisões pendentes",
    "",
    "- Os comandos são sintéticos, não coletados de apicultores.",
    "- Templates semelhantes não representam observações independentes.",
    "- A política conservadora de abstenção em ações múltiplas "
    "deve ser confirmada antes do congelamento.",
    "- `[]` significa nenhuma chamada executável; não comprova "
    "que o modelo solicitou esclarecimento.",
    "- A auditoria automática verifica estrutura, limites, "
    "distribuição e duplicatas, não correção semântica completa.",
    "- Os 36 comandos anteriores já foram usados em estudo "
    "exploratório; não constituem teste independente.",
    "- Não executar inferências definitivas antes da revisão "
    "e do congelamento do conjunto sintético.",
    "",
]

REPORT.write_text("\n".join(lines), encoding="utf-8")

print("=" * 68)
print("PT-08.5 — GERAÇÃO DO DATASET SINTÉTICO")
print("=" * 68)
print("Casos originais:", len(final_data["casos"]))
print("Casos sintéticos:", len(selected))
print("Total planejado:", len(final_data["casos"]) + len(selected))
print()
for category, count in distribution.items():
    print(f"{category}: {count}")
print()
print("Dataset:", OUT.relative_to(ROOT))
print("SHA-256:", sha(OUT))
print("Auditoria:", CSV.relative_to(ROOT))
print("Relatório:", REPORT.relative_to(ROOT))
print()
print("[OK] Integridade estrutural verificada.")
print("[OK] Nenhuma duplicata textual normalizada.")
print("[PENDENTE] Revisão semântica e congelamento.")
