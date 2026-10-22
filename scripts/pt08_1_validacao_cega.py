#!/usr/bin/env python3
"""Gera documento de revisão semântica sem exibir predições."""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONTE = ROOT / "dataset/colmeia-needle2-gabarito-revisado.json"
DESTINO = ROOT / "docs/metodologia/pt08_1_validacao_cega.md"

dados = json.loads(FONTE.read_text(encoding="utf-8"))
casos = dados["casos"]

if len(casos) != 36:
    raise SystemExit("[ERRO] Esperados 36 casos.")

ids = [c["id"] for c in casos]
if len(set(ids)) != 36:
    raise SystemExit("[ERRO] IDs duplicados.")

linhas = [
    "# PT-08.1 — Validação semântica dos gabaritos",
    "",
    "## Procedimento",
    "",
    "Revisar cada comando utilizando apenas a frase,",
    "a categoria e o gabarito proposto.",
    "",
    "As predições do Needle 2 não são apresentadas.",
    "",
    "**Estado:** PENDENTE DE VALIDAÇÃO HUMANA.",
    "",
    "## Critérios",
    "",
    "- Comandos completos devem gerar chamadas exatas.",
    "- Parâmetros obrigatórios ausentes exigem abstenção.",
    "- Solicitações ambíguas devem ser rejeitadas quando",
    "  não for possível identificar a ação ou a colmeia.",
    "- Comandos fora do escopo exigem abstenção.",
    "- Consultas múltiplas podem gerar múltiplas chamadas.",
    "- Ações coletivas não suportadas exigem abstenção.",
    "",
]

for caso in sorted(casos, key=lambda c: c["id"]):
    chamadas = caso["chamadas_esperadas_revisadas"]
    revisao = caso["revisao_metodologica"]

    linhas.extend([
        f"## Caso {caso['id']:02d}",
        "",
        f"**Categoria:** {caso['categoria']}",
        "",
        f"**Frase:** {caso['frase']}",
        "",
        "**Gabarito proposto:**",
        "",
        "```json",
        json.dumps(
            chamadas,
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "**Justificativa anterior:** "
        + str(revisao.get("justificativa") or "Gabarito preservado."),
        "",
        "**Decisão humana:** PENDENTE",
        "",
        "**Justificativa da decisão:**",
        "",
        "---",
        "",
    ])

DESTINO.write_text(
    "\n".join(linhas),
    encoding="utf-8",
)

sha = hashlib.sha256(FONTE.read_bytes()).hexdigest()

print("=" * 70)
print("PT-08.1 — DOCUMENTO DE VALIDAÇÃO SEMÂNTICA")
print("=" * 70)
print(f"Casos: {len(casos)}")
print(f"SHA-256 do dataset: {sha}")
print(f"Documento: {DESTINO.relative_to(ROOT)}")
print("[OK] Documento gerado.")
print("[PENDENTE] Aprovação semântica dos 36 gabaritos.")
