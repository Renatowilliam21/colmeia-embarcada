#!/usr/bin/env python3
"""PT-12.6 — Diagnóstico dos erros da V4.

Utiliza exclusivamente os resultados já produzidos.
Não executa inferências nem ferramentas físicas.
"""

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / (
    "results/evaluation/pt12/pt12_5/"
    "pt12_5_detalhado.csv"
)

OUTPUT = ROOT / "results/evaluation/pt12/pt12_6"

EXPECTED_SHA256 = (
    "3e060d09d42b5717b5dadebb26102e7cf115"
    "3e1d032e5a7dbd79d5f77f9f9b1b"
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def as_bool(value):
    return str(value).strip().lower() == "true"


def classify(row):
    if not as_bool(row["valid_prediction"]):
        return "saida_invalida"

    predicted = json.loads(row["predicted"])
    expected = json.loads(row["expected"])

    if not predicted:
        return "modelo_sem_chamada"

    predicted_names = [
        call.get("name")
        for call in predicted
        if isinstance(call, dict)
    ]

    expected_names = [
        call.get("name")
        for call in expected
        if isinstance(call, dict)
    ]

    if predicted_names != expected_names:
        return "ferramenta_divergente"

    if predicted != expected:
        return "argumentos_divergentes"

    return "chamada_correta_bloqueada"


def main():
    print("=" * 72)
    print("PT-12.6 — DIAGNÓSTICO DOS ERROS DA V4")
    print("=" * 72)

    if sha256(INPUT) != EXPECTED_SHA256:
        raise RuntimeError(
            "Hash do resultado PT-12.5 divergente."
        )

    with INPUT.open(
        encoding="utf-8",
        newline="",
    ) as stream:
        rows = list(csv.DictReader(stream))

    if len(rows) != 360:
        raise RuntimeError(
            f"Esperadas 360 avaliações; encontradas {len(rows)}."
        )

    positives = [
        row for row in rows
        if not as_bool(row["expected_empty"])
    ]

    negatives = [
        row for row in rows
        if as_bool(row["expected_empty"])
    ]

    if len(positives) != 180 or len(negatives) != 180:
        raise RuntimeError(
            "Distribuição positiva/negativa inesperada."
        )

    failures = [
        row for row in positives
        if not as_bool(row["exact_match"])
    ]

    if len(failures) != 135:
        raise RuntimeError(
            f"Esperadas 135 falhas positivas; encontradas {len(failures)}."
        )

    reasons = Counter()
    rules = Counter()
    categories = Counter()
    by_case = defaultdict(list)

    for row in failures:
        reason = classify(row)

        reasons[reason] += 1
        rules[row["rule"]] += 1
        categories[row["category"]] += 1

        by_case[row["case_id"]].append({
            "repetition": int(row["repetition"]),
            "reason": reason,
            "rule": row["rule"],
            "predicted": row["predicted"],
            "authorized": row["authorized"],
        })

    OUTPUT.mkdir(parents=True, exist_ok=True)

    case_path = OUTPUT / "pt12_6_erros_por_caso.json"

    case_path.write_text(
        json.dumps(
            dict(sorted(by_case.items())),
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    summary = {
        "etapa": "PT-12.6",
        "tipo": "diagnostico_de_desenvolvimento",
        "total_avaliacoes": len(rows),
        "avaliacoes_positivas": len(positives),
        "avaliacoes_negativas": len(negatives),
        "falhas_positivas": len(failures),
        "causas": dict(sorted(reasons.items())),
        "regras": dict(sorted(rules.items())),
        "categorias": dict(sorted(categories.items())),
        "casos_distintos_com_falhas": len(by_case),
        "observacao": (
            "Classificação automática preliminar. "
            "A causa linguística específica exige "
            "inspeção humana dos casos."
        ),
    }

    summary_path = OUTPUT / "pt12_6_resumo.json"

    summary_path.write_text(
        json.dumps(
            summary,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print()
    print("FALHAS POSITIVAS:", len(failures), "/180")
    print("CASOS DISTINTOS COM FALHAS:", len(by_case))

    print()
    print("CLASSIFICAÇÃO DAS FALHAS")

    for reason, count in sorted(reasons.items()):
        print(f"{reason}: {count}")

    print()
    print("REGRAS ASSOCIADAS")

    for rule, count in sorted(rules.items()):
        print(f"{rule}: {count}")

    print()
    print("DISTRIBUIÇÃO POR CATEGORIA")

    for category, count in sorted(categories.items()):
        print(f"{category}: {count}")

    print()
    print("ARQUIVOS GERADOS")

    for path in (case_path, summary_path):
        print(
            f"{path.relative_to(ROOT)} "
            f"| SHA256 {sha256(path)}"
        )

    print()
    print("[OK] PT-12.6 concluída.")


if __name__ == "__main__":
    main()
