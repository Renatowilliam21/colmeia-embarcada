#!/usr/bin/env python3
"""Prepara seis lotes para revisão semântica dos 180 casos."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset/synthetic/colmeia-needle2-sintetico-v1.json"
OUTDIR = ROOT / "docs/metodologia/revisao_sintetica"

EXPECTED_SHA = (
    "c0927a014dec323e83db8ef68641b99c777818cdff8fab3445c4a418e79ed555"
)

actual_sha = hashlib.sha256(DATASET.read_bytes()).hexdigest()

if actual_sha != EXPECTED_SHA:
    raise RuntimeError("Dataset alterado após a auditoria.")

dados = json.loads(DATASET.read_text(encoding="utf-8"))
casos = sorted(dados["casos"], key=lambda c: c["id"])

if len(casos) != 180:
    raise RuntimeError("Quantidade de casos inesperada.")

if [c["id"] for c in casos] != list(range(37, 217)):
    raise RuntimeError("IDs não correspondem ao intervalo esperado.")

OUTDIR.mkdir(parents=True, exist_ok=True)

for indice in range(6):
    inicio = 37 + indice * 30
    fim = inicio + 29

    lote = [
        c for c in casos
        if inicio <= c["id"] <= fim
    ]

    linhas = [
        f"# PT-08.9 — Lote {indice + 1}",
        "",
        f"**Casos:** {inicio}–{fim}",
        "",
        f"**Dataset SHA-256:** `{actual_sha}`",
        "",
        "**Estado:** PENDENTE DE REVISÃO SEMÂNTICA",
        "",
        "As predições do modelo não são exibidas.",
        "",
    ]

    for caso in lote:
        linhas.extend([
            f"## Caso {caso['id']}",
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
            "**Decisão do revisor:** PENDENTE",
            "",
            "**Justificativa da revisão:**",
            "",
            "---",
            "",
        ])

    destino = OUTDIR / f"lote_{indice + 1:02d}_{inicio}_{fim}.md"

    destino.write_text(
        "\n".join(linhas),
        encoding="utf-8"
    )

    print(
        f"[OK] Lote {indice + 1}: "
        f"{len(lote)} casos -> {destino.relative_to(ROOT)}"
    )

print()
print("Total de casos preparados:", len(casos))
print("[PENDENTE] Revisão semântica individual.")
