#!/usr/bin/env python3
"""PT-13.2 — Auditoria da coleta e preparação da revisão cruzada."""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()

COLETA = ROOT / "dataset/validation/pt13/coleta"
REVISAO = ROOT / "dataset/validation/pt13/revisao"

REVISAO.mkdir(parents=True, exist_ok=True)

REVISOR = {
    "A": "B",
    "B": "C",
    "C": "D",
    "D": "A",
}

CAMPOS_REVISAO = [
    "id",
    "grupo",
    "frase",
    "autor_codigo",
    "revisor_codigo",
    "avaliacao_semantica",
    "grupo_confirmado",
    "chamadas_esperadas_json",
    "justificativa",
    "observacoes_revisor",
]

todos = []
erros = []

for autor in REVISOR:
    origem = COLETA / f"pt13_1_coleta_colaborador_{autor}.csv"

    if not origem.exists():
        erros.append(f"Arquivo ausente: {origem}")
        continue

    with origem.open(
        encoding="utf-8-sig",
        newline=""
    ) as f:
        registros = list(csv.DictReader(f, delimiter=";"))

    if len(registros) != 30:
        erros.append(
            f"Colaborador {autor}: "
            f"esperados 30 registros, encontrados {len(registros)}"
        )

    for registro in registros:
        identificador = registro.get("id", "").strip()
        frase = registro.get("frase", "").strip()
        codigo = registro.get("autor_codigo", "").strip()
        data = registro.get("data_coleta", "").strip()

        if not identificador:
            erros.append(f"ID vazio no formulário {autor}")

        if not frase:
            erros.append(f"Frase vazia: {identificador}")

        if codigo != autor:
            erros.append(
                f"Autor divergente: {identificador}"
            )

        if not data:
            erros.append(
                f"Data não preenchida: {identificador}"
            )

        todos.append(registro)

ids = Counter(r.get("id", "") for r in todos)

for identificador, quantidade in ids.items():
    if quantidade != 1:
        erros.append(
            f"ID duplicado: {identificador}"
        )

print("=" * 70)
print("PT-13.2 — AUDITORIA DA COLETA")
print("=" * 70)

print("Registros encontrados:", len(todos))
print("Problemas identificados:", len(erros))

if erros:
    for erro in erros:
        print("[PENDENTE]", erro)

    raise SystemExit(
        "\n[AGUARDANDO] Finalizar a coleta antes da revisão."
    )

for autor, revisor in REVISOR.items():
    registros = [
        r for r in todos
        if r["autor_codigo"] == autor
    ]

    destino = REVISAO / (
        f"pt13_2_revisao_{revisor}_sobre_{autor}.csv"
    )

    if destino.exists():
        raise FileExistsError(
            f"Formulário de revisão já existe: {destino}"
        )

    with destino.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=CAMPOS_REVISAO,
            delimiter=";",
        )

        writer.writeheader()

        for registro in registros:
            writer.writerow({
                "id": registro["id"],
                "grupo": registro["grupo"],
                "frase": registro["frase"],
                "autor_codigo": autor,
                "revisor_codigo": revisor,
                "avaliacao_semantica": "pendente",
                "grupo_confirmado": "",
                "chamadas_esperadas_json": "",
                "justificativa": "",
                "observacoes_revisor": "",
            })

    print(
        f"[OK] Revisor {revisor}: "
        f"{len(registros)} frases do autor {autor}"
    )

print("\n[OK] Formulários de revisão criados.")
