#!/usr/bin/env python3

import json
import re
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATASET = ROOT / "dataset/synthetic/colmeia-needle2-sintetico-v1.json"
SCHEMA = ROOT / "firmware/tools/colmeia.json"
REPORT = ROOT / "docs/metodologia/pt08_6_auditoria_semantica.md"

dados = json.loads(DATASET.read_text(encoding="utf-8"))
casos = dados["casos"]

if len(casos) != 180:
    raise RuntimeError("Esperados 180 casos sintéticos.")

if hashlib.sha256(DATASET.read_bytes()).hexdigest() != (
    "c0927a014dec323e83db8ef68641b99c777818cdff8fab3445c4a418e79ed555"
):
    raise RuntimeError("Hash do dataset sintético diferente do esperado.")

def assinatura(frase):
    frase = frase.lower()
    frase = re.sub(r"\b\d+\b", "<NUM>", frase)
    frase = re.sub(r"\s+", " ", frase)
    return frase.strip()

familias = defaultdict(list)
assinaturas = defaultdict(list)
categorias = Counter()
abstencoes = Counter()

for caso in casos:
    categorias[caso["categoria"]] += 1
    familias[caso["familia"]].append(caso)
    assinaturas[assinatura(caso["frase"])].append(caso)

    if not caso["chamadas_esperadas_revisadas"]:
        abstencoes[caso["categoria"]] += 1

linhas = [
    "# PT-08.6 — Auditoria do dataset sintético",
    "",
    "## Estado",
    "",
    "**PENDENTE DE REVISÃO HUMANA.**",
    "",
    "## Distribuição",
    "",
    "| Categoria | Casos | Abstenções esperadas |",
    "|---|---:|---:|",
]

for categoria, total in categorias.items():
    linhas.append(
        f"| {categoria} | {total} | {abstencoes[categoria]} |"
    )

linhas += [
    "",
    "## Diversidade de templates",
    "",
    f"- Total de comandos: **{len(casos)}**",
    f"- Famílias declaradas: **{len(familias)}**",
    f"- Assinaturas com números substituídos: **{len(assinaturas)}**",
    "",
    "A assinatura é uma aproximação da diversidade superficial, "
    "não uma medida de independência semântica.",
    "",
    "| Família | Casos |",
    "|---|---:|",
]

for familia, itens in sorted(familias.items()):
    linhas.append(f"| {familia} | {len(itens)} |")

linhas += [
    "",
    "## Revisão individual",
    "",
    "As predições do Needle 2 não são exibidas.",
    "",
]

for caso in sorted(casos, key=lambda x: x["id"]):
    linhas += [
        f"### Caso {caso['id']}",
        "",
        f"**Categoria:** {caso['categoria']}",
        "",
        f"**Família:** {caso['familia']}",
        "",
        f"**Frase:** {caso['frase']}",
        "",
        "**Gabarito candidato:**",
        "",
        "```json",
        json.dumps(
            caso["chamadas_esperadas_revisadas"],
            ensure_ascii=False,
            indent=2
        ),
        "```",
        "",
        f"**Justificativa:** {caso['justificativa']}",
        "",
        "**Decisão humana:** PENDENTE",
        "",
        "**Observações:**",
        "",
        "---",
        "",
    ]

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(linhas), encoding="utf-8")

print("=" * 68)
print("PT-08.6 — AUDITORIA DO DATASET SINTÉTICO")
print("=" * 68)
print("Comandos:", len(casos))
print("Famílias:", len(familias))
print("Assinaturas linguísticas:", len(assinaturas))
print("Abstenções esperadas:", sum(abstencoes.values()))
print()
print("Distribuição:")
for categoria, total in categorias.items():
    print(
        f"  {categoria}: {total} "
        f"(abstenções: {abstencoes[categoria]})"
    )
print()
print("Relatório:", REPORT.relative_to(ROOT))
print("[OK] Relatório gerado.")
print("[PENDENTE] Revisão humana e congelamento.")
