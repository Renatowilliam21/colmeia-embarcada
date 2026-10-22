#!/usr/bin/env python3
"""PT-11.9 — Análise estatística pareada por caso experimental."""

import csv
import hashlib
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / (
    "results/evaluation/pt11/pt11_8/"
    "pt11_8_detalhado.csv"
)

OUTPUT = ROOT / "results/evaluation/pt11/pt11_9"

CONFIGS = [
    "C0_Needle2",
    "C1_Needle2_V1",
    "C2_Needle2_V2",
    "C3_Needle2_V3",
]

COMPARISONS = [
    ("C0_Needle2", "C1_Needle2_V1"),
    ("C0_Needle2", "C2_Needle2_V2"),
    ("C0_Needle2", "C3_Needle2_V3"),
    ("C1_Needle2_V1", "C3_Needle2_V3"),
    ("C2_Needle2_V2", "C3_Needle2_V3"),
]

EXPECTED_SHA256 = (
    "2cea16f42868f223f85c2626cf4884ce6"
    "d6160152fff301df6b5274282478b98"
)

N_BOOT = 10000
SEED = 20261109


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mean(values):
    return sum(values) / len(values) if values else 0.0


def percentile(sorted_values, q):
    if not sorted_values:
        return None

    pos = (len(sorted_values) - 1) * q
    low = math.floor(pos)
    high = math.ceil(pos)

    if low == high:
        return sorted_values[low]

    weight = pos - low

    return (
        sorted_values[low] * (1 - weight)
        + sorted_values[high] * weight
    )


def bootstrap_ci(values, rng):
    """IC percentil por reamostragem de casos completos."""

    n = len(values)

    if n == 0:
        return None, None

    samples = []

    for _ in range(N_BOOT):
        sample = [
            values[rng.randrange(n)]
            for _ in range(n)
        ]
        samples.append(mean(sample))

    samples.sort()

    return (
        percentile(samples, 0.025),
        percentile(samples, 0.975),
    )


def write_csv(path, rows, columns):
    with path.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as stream:

        writer = csv.DictWriter(
            stream,
            fieldnames=columns,
        )

        writer.writeheader()
        writer.writerows(rows)


def friedman_test(matrix):
    """Friedman com postos médios e correção para empates."""

    n = len(matrix)

    if n == 0:
        return None

    k = len(matrix[0])

    rank_sums = [0.0] * k
    tie_sum = 0.0

    for values in matrix:
        if len(values) != k:
            raise RuntimeError("Matriz de Friedman irregular.")

        indexed = sorted(
            enumerate(values),
            key=lambda item: item[1]
        )

        ranks = [0.0] * k
        pos = 0

        while pos < k:
            end = pos + 1

            while (
                end < k
                and indexed[end][1] == indexed[pos][1]
            ):
                end += 1

            average_rank = ((pos + 1) + end) / 2.0

            for j in range(pos, end):
                ranks[indexed[j][0]] = average_rank

            size = end - pos

            if size > 1:
                tie_sum += size ** 3 - size

            pos = end

        for j, rank in enumerate(ranks):
            rank_sums[j] += rank

    q = (
        12.0 / (n * k * (k + 1))
        * sum(value ** 2 for value in rank_sums)
        - 3.0 * n * (k + 1)
    )

    denominator = n * (k ** 3 - k)

    correction = (
        1.0 - tie_sum / denominator
        if denominator
        else 0.0
    )

    if correction <= 0:
        return {
            "statistic": 0.0,
            "degrees_of_freedom": k - 1,
            "p_value": 1.0,
            "method": "all_tied",
        }

    q /= correction

    try:
        from scipy.stats import chi2

        p_value = float(chi2.sf(q, k - 1))
    except ImportError:
        p_value = None

    return {
        "statistic": round(q, 6),
        "degrees_of_freedom": k - 1,
        "p_value": p_value,
        "method": "friedman_tie_corrected",
        "note": (
            "p-valor assintótico; interpretar com cautela "
            "devido aos empates e à origem sintética."
        ),
    }


def main():

    previous_summary = ROOT / (
        "results/evaluation/pt11/pt11_8/"
        "pt11_8_resumo.json"
    )

    if sha256(previous_summary) != EXPECTED_SHA256:
        raise RuntimeError(
            "Resumo PT-11.8 divergente do SHA-256 registrado."
        )

    with INPUT.open(
        encoding="utf-8",
        newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))

    if len(rows) != 1440:
        raise RuntimeError(
            f"Esperadas 1440 avaliações; encontradas {len(rows)}."
        )

    data = defaultdict(dict)
    categories = {}
    repetitions = defaultdict(set)

    for row in rows:

        case_id = row["case_id"]
        config = row["configuration"]
        repetition = int(row["repetition"])

        if config not in CONFIGS:
            raise RuntimeError(f"Configuração inesperada: {config}")

        if repetition not in (1, 2, 3):
            raise RuntimeError("Repetição fora de 1, 2 ou 3.")

        key = (case_id, config, repetition)

        if repetition in repetitions[(case_id, config)]:
            raise RuntimeError(f"Duplicata: {key}")

        repetitions[(case_id, config)].add(repetition)

        category = row["category"]

        if (
            case_id in categories
            and categories[case_id] != category
        ):
            raise RuntimeError("Categoria inconsistente.")

        categories[case_id] = category

        data[(case_id, config)][repetition] = (
            1 if row["exact_match"] == "True" else 0
        )

    case_ids = sorted(categories)

    if len(case_ids) != 120:
        raise RuntimeError("Quantidade de casos divergente.")

    case_results = []
    values = {}

    for case_id in case_ids:
        for config in CONFIGS:

            repetitions_data = data[(case_id, config)]

            if set(repetitions_data) != {1, 2, 3}:
                raise RuntimeError(
                    f"Repetições incompletas: {case_id}, {config}"
                )

            scores = [
                repetitions_data[i]
                for i in (1, 2, 3)
            ]

            score = mean(scores)

            values[(case_id, config)] = score

            case_results.append({
                "case_id": case_id,
                "category": categories[case_id],
                "configuration": config,
                "correct_repetitions": sum(scores),
                "total_repetitions": 3,
                "case_accuracy": score,
            })

    rng = random.Random(SEED)

    metrics = {}

    for config in CONFIGS:

        scores = [
            values[(case_id, config)]
            for case_id in case_ids
        ]

        low, high = bootstrap_ci(scores, rng)

        metrics[config] = {
            "cases": len(scores),
            "mean_case_accuracy": round(mean(scores), 6),
            "accuracy_percent": round(
                100 * mean(scores), 4
            ),
            "bootstrap_ci95_percent": [
                round(100 * low, 4),
                round(100 * high, 4),
            ],
        }

    comparisons = []

    for config_a, config_b in COMPARISONS:

        differences = [
            values[(case_id, config_b)]
            - values[(case_id, config_a)]
            for case_id in case_ids
        ]

        low, high = bootstrap_ci(differences, rng)

        comparisons.append({
            "configuration_a": config_a,
            "configuration_b": config_b,
            "difference_b_minus_a_pp": round(
                100 * mean(differences), 4
            ),
            "ci95_lower_pp": round(100 * low, 4),
            "ci95_upper_pp": round(100 * high, 4),
            "cases_b_better": sum(
                d > 0 for d in differences
            ),
            "cases_a_better": sum(
                d < 0 for d in differences
            ),
            "cases_tied": sum(
                d == 0 for d in differences
            ),
        })

    category_rows = []

    for config in CONFIGS:
        for category in sorted(set(categories.values())):

            selected = [
                case_id
                for case_id in case_ids
                if categories[case_id] == category
            ]

            scores = [
                values[(case_id, config)]
                for case_id in selected
            ]

            category_rows.append({
                "configuration": config,
                "category": category,
                "cases": len(selected),
                "mean_accuracy_percent": round(
                    100 * mean(scores), 4
                ),
            })

    matrix = [
        [
            values[(case_id, config)]
            for config in CONFIGS
        ]
        for case_id in case_ids
    ]

    friedman = friedman_test(matrix)

    summary = {
        "stage": "PT-11.9",
        "analysis_type": "paired_case_level",
        "independent_human_validation": False,
        "cases": 120,
        "repetitions_per_case": 3,
        "configurations": CONFIGS,
        "bootstrap": {
            "iterations": N_BOOT,
            "seed": SEED,
            "resampling_unit": "case_id",
            "confidence_level": 0.95,
            "method": "percentile",
        },
        "metrics": metrics,
        "comparisons": comparisons,
        "friedman": friedman,
        "limitations": [
            "Dataset sintético gerado com assistência de IA.",
            "Sem validação humana independente.",
            "As três repetições não são independentes.",
            "Bootstrap condicionado aos 120 casos sintéticos.",
            "Teste de Friedman complementar e assintótico.",
            "Não foram realizadas atuações físicas.",
        ],
    }

    OUTPUT.mkdir(parents=True, exist_ok=True)

    write_csv(
        OUTPUT / "pt11_9_resultados_por_caso.csv",
        case_results,
        [
            "case_id",
            "category",
            "configuration",
            "correct_repetitions",
            "total_repetitions",
            "case_accuracy",
        ],
    )

    write_csv(
        OUTPUT / "pt11_9_comparacoes_pareadas.csv",
        comparisons,
        [
            "configuration_a",
            "configuration_b",
            "difference_b_minus_a_pp",
            "ci95_lower_pp",
            "ci95_upper_pp",
            "cases_b_better",
            "cases_a_better",
            "cases_tied",
        ],
    )

    write_csv(
        OUTPUT / "pt11_9_metricas_por_categoria.csv",
        category_rows,
        [
            "configuration",
            "category",
            "cases",
            "mean_accuracy_percent",
        ],
    )

    summary_path = OUTPUT / "pt11_9_resumo_estatistico.json"

    summary_path.write_text(
        json.dumps(
            summary,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("=" * 75)
    print("PT-11.9 — ANÁLISE ESTATÍSTICA")
    print("=" * 75)

    print("\nDESEMPENHO POR CONFIGURAÇÃO")

    for config, result in metrics.items():
        ci = result["bootstrap_ci95_percent"]

        print(
            f"{config}: "
            f"{result['accuracy_percent']:.2f}% "
            f"[IC95% {ci[0]:.2f}%, {ci[1]:.2f}%]"
        )

    print("\nCOMPARAÇÕES PAREADAS")

    for result in comparisons:
        print(
            f"{result['configuration_a']} -> "
            f"{result['configuration_b']}: "
            f"{result['difference_b_minus_a_pp']:+.2f} p.p. "
            f"[{result['ci95_lower_pp']:+.2f}, "
            f"{result['ci95_upper_pp']:+.2f}]"
        )

    print("\nFRIEDMAN")
    print(
        f"Estatística: {friedman['statistic']}"
    )
    print(
        f"p-valor: {friedman['p_value']}"
    )

    print("\nArquivos gerados:")

    for path in sorted(OUTPUT.iterdir()):
        if path.is_file():
            print(
                f"  {path.relative_to(ROOT)} "
                f"| SHA256 {sha256(path)}"
            )

    print("\n[OK] PT-11.9 concluída.")


if __name__ == "__main__":
    try:
        main()
    except (
        RuntimeError,
        OSError,
        ValueError,
        KeyError,
        ImportError,
    ) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        sys.exit(1)
