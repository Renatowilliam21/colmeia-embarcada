#!/usr/bin/env python3
"""PT-08 — Auditoria semântica para revisão humana."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ORIGINAL = ROOT / "dataset/colmeia-needle2-dataset-teste.json"
REVISADO = ROOT / "dataset/colmeia-needle2-gabarito-revisado.json"
RESULTADOS = (
    ROOT / "results/experiments/needle2_host/"
    "20261022T200512Z/raw_results.jsonl"
)

DESTINO = ROOT / "docs/metodologia/pt08_auditoria_semantica.md"

original = json.loads(ORIGINAL.read_text(encoding="utf-8"))["casos"]
revisado = json.loads(REVISADO.read_text(encoding="utf-8"))["casos"]

registros = [
    json.loads(linha)
    for linha in RESULTADOS.read_text(encoding="utf-8").splitlines()
    if linha.strip()
]

def indexar(itens, chave):
    ids = [str(x[chave]) for x in itens]
    if len(ids) != len(set(ids)):
        raise RuntimeError(f"IDs duplicados: {chave}")
    return {str(x[chave]): x for x in itens}

orig = indexar(original, "id")
rev = indexar(revisado, "id")
pred = indexar(registros, "case_id")

if not (set(orig) == set(rev) == set(pred)):
    raise SystemExit("[ERRO] IDs incompatíveis.")

def formatar(valor):
    return json.dumps(valor, ensure_ascii=False, sort_keys=True)

linhas = [
    "# PT-08 — Auditoria semântica dos 36 casos",
    "",
    "Este documento apresenta os gabaritos e predições para revisão humana.",
    "A geração do documento não equivale à aprovação dos gabaritos.",
    "",
]

divergencias = []
alterados = []

for id_caso in sorted(orig, key=int):
    caso = orig[id_caso]
    novo = rev[id_caso]
    registro = pred[id_caso]

    esperado = novo["chamadas_esperadas_revisadas"]
    produzido = registro.get("parsed_calls")
    mudou = novo["revisao_metodologica"]["revisado"]

    if mudou:
        alterados.append(int(id_caso))

    if esperado != produzido:
        divergencias.append(int(id_caso))

    linhas.extend([
        f"## Caso {int(id_caso):02d}",
        "",
        f"**Categoria:** {caso['categoria']}",
        "",
        f"**Frase:** {caso['frase']}",
        "",
        "**Gabarito original:**",
        "",
        "```json",
        formatar({
            "ferramenta_esperada": caso.get("ferramenta_esperada"),
            "argumentos_esperados": caso.get("argumentos_esperados"),
        }),
        "```",
        "",
        "**Gabarito revisado:**",
        "",
        "```json",
        formatar(esperado),
        "```",
        "",
        "**Predição do Needle 2:**",
        "",
        "```json",
        formatar(produzido),
        "```",
        "",
        f"**Revisado anteriormente:** {'Sim' if mudou else 'Não'}",
        "",
        f"**Correspondência:** {'Sim' if esperado == produzido else 'Não'}",
        "",
        "**Revisão humana:** Pendente",
        "",
        "**Observações:**",
        "",
        "---",
        "",
    ])

DESTINO.write_text(
    "\n".join(linhas),
    encoding="utf-8"
)

print("=" * 72)
print("PT-08 — AUDITORIA SEMÂNTICA")
print("=" * 72)
print(f"Casos analisados: {len(orig)}")
print(f"Gabaritos previamente revisados: {alterados}")
print(f"Divergências entre gabarito revisado e predição: {divergencias}")
print(f"Total de divergências: {len(divergencias)}")
print(f"Documento gerado: {DESTINO.relative_to(ROOT)}")
print("\n[OK] Documento de auditoria criado.")
print("[PENDENTE] Revisão semântica humana dos 36 casos.")
