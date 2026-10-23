#!/usr/bin/env python3
"""PT-12.1 — Diagnóstico linguístico das rejeições da V3."""

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATASET = ROOT / (
    "dataset/validation/pt11/"
    "pt11_6_dataset_sintetico_congelado.jsonl"
)

DETAIL = ROOT / (
    "results/evaluation/pt11/pt11_8/"
    "pt11_8_detalhado.csv"
)

OUTPUT = ROOT / "results/evaluation/pt12/pt12_1"

EXPECTED_DATASET_SHA256 = (
    "6ee8d7e0facc98b491fb52b39a51ad0debf4"
    "b64a7aa331d8a9e1d6f4abf47750"
)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def is_true(value):
    return str(value).strip().lower() == "true"

def load_jsonl(path):
    with path.open(encoding="utf-8") as stream:
        return [
            json.loads(line)
            for line in stream
            if line.strip()
        ]

def main():
    print("=" * 72)
    print("PT-12.1 — DIAGNÓSTICO LINGUÍSTICO")
    print("=" * 72)

    if sha256(DATASET) != EXPECTED_DATASET_SHA256:
        raise RuntimeError("Dataset congelado com hash divergente.")

    cases = load_jsonl(DATASET)

    if len(cases) != 120:
        raise RuntimeError("Quantidade inesperada de casos.")

    case_map = {case["id"]: case for case in cases}

    if len(case_map) != 120:
        raise RuntimeError("IDs duplicados no dataset.")

    with DETAIL.open(encoding="utf-8", newline="") as stream:
        evaluations = list(csv.DictReader(stream))

    if len(evaluations) != 1440:
        raise RuntimeError("Quantidade inesperada de avaliações.")

    v3_rows = [
        row for row in evaluations
        if row["configuration"] == "C3_Needle2_V3"
    ]

    if len(v3_rows) != 360:
        raise RuntimeError("Quantidade inesperada de avaliações V3.")

    positive_rows = [
        row for row in v3_rows
        if not is_true(row["expected_empty"])
    ]

    if len(positive_rows) != 180:
        raise RuntimeError("Quantidade inesperada de avaliações positivas.")

    rejected = [
        row for row in positive_rows
        if row["rule"] == "R12"
        and row["authorized"].strip() == "[]"
    ]

    if len(rejected) != 180:
        raise RuntimeError(
            f"Esperadas 180 rejeições R12; encontradas {len(rejected)}."
        )

    grouped = defaultdict(list)

    for row in rejected:
        case_id = row["case_id"]

        if case_id not in case_map:
            raise RuntimeError(f"Caso desconhecido: {case_id}")

        grouped[case_id].append(row)

    if len(grouped) != 60:
        raise RuntimeError(
            f"Esperados 60 casos positivos; encontrados {len(grouped)}."
        )

    output_rows = []
    categories = Counter()

    for case_id in sorted(grouped):
        case = case_map[case_id]
        rows = grouped[case_id]

        if len(rows) != 3:
            raise RuntimeError(
                f"Caso {case_id} possui {len(rows)} repetições."
            )

        category = case["grupo"]
        categories[category] += 1

        output_rows.append({
            "case_id": case_id,
            "categoria": category,
            "frase": case["frase"],
            "chamadas_esperadas": json.dumps(
                case["chamadas_esperadas"],
                ensure_ascii=False,
                sort_keys=True,
            ),
            "repeticoes_rejeitadas_r12": len(rows),
            "diagnostico_linguistico": "pendente",
            "proposta_cobertura_v4": "",
            "observacoes": "",
        })

    OUTPUT.mkdir(parents=True, exist_ok=True)

    csv_path = OUTPUT / "pt12_1_frases_rejeitadas.csv"

    with csv_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=list(output_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(output_rows)

    summary = {
        "etapa": "PT-12.1",
        "dataset_origem": str(DATASET.relative_to(ROOT)),
        "dataset_sha256": sha256(DATASET),
        "avaliacao_origem": str(DETAIL.relative_to(ROOT)),
        "avaliacao_sha256": sha256(DETAIL),
        "configuracao": "C3_Needle2_V3",
        "avaliacoes_positivas": len(positive_rows),
        "avaliacoes_positivas_rejeitadas_r12": len(rejected),
        "casos_positivos_distintos_rejeitados_r12": len(grouped),
        "categorias_por_caso": dict(sorted(categories.items())),
        "revisao_linguistica_humana": "pendente",
        "observacao": (
            "As 180 avaliações correspondem a 60 casos "
            "com três repetições, não a 180 frases independentes."
        ),
    }

    json_path = OUTPUT / "pt12_1_resumo.json"

    json_path.write_text(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )

    md_path = OUTPUT / "pt12_1_diagnostico.md"

    lines = [
        "# PT-12.1 — Diagnóstico linguístico",
        "",
        "## Objetivo",
        "",
        "Examinar as solicitações positivas rejeitadas pela "
        "regra R12 do validador V3.",
        "",
        "## Resultados",
        "",
        f"- Avaliações positivas: {len(positive_rows)}",
        f"- Avaliações rejeitadas pela R12: {len(rejected)}",
        f"- Casos distintos rejeitados: {len(grouped)}",
        "",
        "## Distribuição por categoria",
        "",
        "| Categoria | Casos distintos |",
        "|---|---:|",
    ]

    for category, count in sorted(categories.items()):
        lines.append(f"| {category} | {count} |")

    lines.extend([
        "",
        "## Interpretação",
        "",
        "A V3 rejeitou as 60 solicitações positivas distintas "
        "do conjunto PT-11, em suas três repetições.",
        "",
        "A regra R12 indica ausência de autorização pela "
        "gramática ou por outras condições de validação. "
        "A classificação da causa linguística específica "
        "ainda requer análise das frases e do código.",
        "",
        "## Limitações",
        "",
        "- Dataset sintético gerado com assistência de IA.",
        "- Gabaritos sem homologação humana independente.",
        "- Repetições não independentes.",
        "- Nenhuma atuação física realizada.",
        "",
        "## Próxima atividade",
        "",
        "Classificar os padrões linguísticos rejeitados e "
        "definir requisitos para a V4, mantendo uma "
        "avaliação posterior em dados não utilizados "
        "durante o desenvolvimento.",
        "",
    ])

    md_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print()
    print("RESULTADOS")
    print(f"Casos positivos distintos: {len(grouped)}")
    print(f"Rejeições R12: {len(rejected)}/180")

    print()
    print("DISTRIBUIÇÃO POR CATEGORIA")

    for category, count in sorted(categories.items()):
        print(f"{category}: {count} casos")

    print()
    print("AMOSTRA DAS FRASES REJEITADAS")

    for row in output_rows[:12]:
        print(f"[{row['case_id']}] {row['frase']}")

    print()
    print("ARQUIVOS GERADOS")

    for path in (csv_path, json_path, md_path):
        print(
            f"{path.relative_to(ROOT)} "
            f"| SHA256 {sha256(path)}"
        )

    print()
    print("[OK] PT-12.1 — Extração concluída.")


if __name__ == "__main__":
    main()
