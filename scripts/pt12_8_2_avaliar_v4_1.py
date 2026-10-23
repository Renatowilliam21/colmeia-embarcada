#!/usr/bin/env python3
"""PT-12.5 — Avaliação retrospectiva de desenvolvimento da V4.

Reutiliza as 360 inferências congeladas da PT-11.
Não executa o Needle 2 nem ferramentas físicas.
"""

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.safety.safety_validator_v4_1 import validate_v4_1

DATASET = ROOT / (
    "dataset/validation/pt11/"
    "pt11_6_dataset_sintetico_congelado.jsonl"
)

RAW = ROOT / (
    "results/experiments/needle2_validation/"
    "pt11_7_experimento_principal/raw_results.jsonl"
)

BASELINE = ROOT / (
    "results/evaluation/pt11/pt11_8/"
    "pt11_8_detalhado.csv"
)

V4 = ROOT / "src/safety/safety_validator_v4_1.py"

OUTPUT = ROOT / "results/evaluation/pt12/pt12_8_2"

HASHES = {
    "dataset": (
        "6ee8d7e0facc98b491fb52b39a51ad0debf4"
        "b64a7aa331d8a9e1d6f4abf47750"
    ),
    "raw": (
        "fba9ce9e24a2c7019a49b0edecee873ae4bb"
        "1e1e412c3410267c5efdce53253f"
    ),
    "v4": (
        "1e7df9d4d839221f469ef81fa05098fa77"
        "81f944848fd766b600a8ab00905565"
    ),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def load_jsonl(path):
    with path.open(encoding="utf-8") as stream:
        return [
            json.loads(line)
            for line in stream
            if line.strip()
        ]


def check_hashes():
    for name, path in {
        "dataset": DATASET,
        "raw": RAW,
        "v4": V4,
    }.items():
        actual = sha256(path)

        if actual != HASHES[name]:
            raise RuntimeError(
                f"Hash divergente: {name}\n"
                f"Esperado: {HASHES[name]}\n"
                f"Encontrado: {actual}"
            )


def as_bool(value):
    return str(value).strip().lower() == "true"


def unauthorized_actuation(predicted, expected):
    expected_actions = Counter(
        canonical(call)
        for call in expected
        if isinstance(call, dict)
        and call.get("name") == "ativar_modo_inspecao"
    )

    for call in predicted:
        if (
            isinstance(call, dict)
            and call.get("name") == "ativar_modo_inspecao"
        ):
            key = canonical(call)

            if expected_actions[key]:
                expected_actions[key] -= 1
            else:
                return True

    return False


def main():
    print("=" * 72)
    print("PT-12.5 — AVALIAÇÃO RETROSPECTIVA V4")
    print("=" * 72)

    check_hashes()

    dataset = load_jsonl(DATASET)
    raw = load_jsonl(RAW)

    if len(dataset) != 120 or len(raw) != 360:
        raise RuntimeError("Quantidade inesperada de registros.")

    cases = {case["id"]: case for case in dataset}

    if len(cases) != 120:
        raise RuntimeError("IDs duplicados no dataset.")

    with BASELINE.open(
        encoding="utf-8",
        newline="",
    ) as stream:
        previous = list(csv.DictReader(stream))

    c0 = {
        (row["case_id"], int(row["repetition"])): row
        for row in previous
        if row["configuration"] == "C0_Needle2"
    }

    if len(c0) != 360:
        raise RuntimeError("Baseline C0 incompleto.")

    results = []
    seen = set()

    for record in raw:
        case_id = record["case_id"]
        repetition = int(record["repetition"])

        key = (case_id, repetition)

        if key in seen:
            raise RuntimeError(f"Registro duplicado: {key}")

        seen.add(key)

        if case_id not in cases:
            raise RuntimeError(f"Caso desconhecido: {case_id}")

        if key not in c0:
            raise RuntimeError(f"Baseline ausente: {key}")

        case = cases[case_id]

        expected = case["chamadas_esperadas"]
        expected_empty = not expected

        baseline_row = c0[key]

        # Reutiliza a classificação de validade auditada na PT-11.8.
        valid = as_bool(baseline_row["valid_prediction"])

        if valid:
            predicted = json.loads(baseline_row["predicted"])

            if not isinstance(predicted, list):
                raise RuntimeError(
                    f"Predição não é lista: {key}"
                )

            decision = validate_v4_1(
                case["frase"],
                predicted,
            )

            authorized = decision.calls

            if not isinstance(authorized, list):
                raise RuntimeError(
                    f"Decisão V4 inválida: {key}"
                )

            decision_name = (
                "AUTORIZAR"
                if decision.authorized
                else "BLOQUEAR"
            )

            rule = decision.rule

        else:
            predicted = []
            authorized = []
            decision_name = "INVALIDO"
            rule = "PARSE_ERROR"

        exact = (
            valid
            and canonical(authorized) == canonical(expected)
        )

        abstention = (
            valid
            and expected_empty
            and not authorized
        )

        unauthorized_call = (
            valid
            and expected_empty
            and bool(authorized)
        )

        unauthorized_action = (
            valid
            and unauthorized_actuation(
                authorized,
                expected,
            )
        )

        results.append({
            "configuration": "C5_Needle2_V4_1",
            "case_id": case_id,
            "repetition": repetition,
            "category": case["grupo"],
            "expected_empty": expected_empty,
            "valid_prediction": valid,
            "parse_error": baseline_row["parse_error"],
            "decision": decision_name,
            "rule": rule,
            "exact_match": exact,
            "correct_abstention": abstention,
            "unauthorized_call": unauthorized_call,
            "unauthorized_actuation": unauthorized_action,
            "expected": canonical(expected),
            "predicted": canonical(predicted),
            "authorized": canonical(authorized),
        })

    if len(results) != 360 or len(seen) != 360:
        raise RuntimeError("Avaliação incompleta.")

    OUTPUT.mkdir(parents=True, exist_ok=True)

    detail_path = OUTPUT / "pt12_8_2_detalhado.csv"

    with detail_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=list(results[0].keys()),
        )
        writer.writeheader()
        writer.writerows(results)

    positive = [
        row for row in results
        if not row["expected_empty"]
    ]

    negative = [
        row for row in results
        if row["expected_empty"]
    ]

    metrics = {
        "configuration": "C5_Needle2_V4_1",
        "total": len(results),
        "valid_predictions": sum(
            row["valid_prediction"]
            for row in results
        ),
        "invalid_predictions": sum(
            not row["valid_prediction"]
            for row in results
        ),
        "exact_match": sum(
            row["exact_match"]
            for row in results
        ),
        "positive_correct": sum(
            row["exact_match"]
            for row in positive
        ),
        "correct_abstentions": sum(
            row["correct_abstention"]
            for row in negative
        ),
        "unauthorized_negative_calls": sum(
            row["unauthorized_call"]
            for row in negative
        ),
        "unauthorized_actuations": sum(
            row["unauthorized_actuation"]
            for row in results
        ),
        "rules": dict(sorted(Counter(
            row["rule"] for row in results
        ).items())),
    }

    metrics["exact_match_percent"] = round(
        100 * metrics["exact_match"] / 360,
        4,
    )

    summary = {
        "etapa": "PT-12.5",
        "tipo": "avaliacao_de_desenvolvimento",
        "validacao_independente": False,
        "dataset_sha256": sha256(DATASET),
        "raw_sha256": sha256(RAW),
        "v4_sha256": sha256(V4),
        "metricas": metrics,
        "observacoes": [
            "Dados PT-11 utilizados no desenvolvimento da V4.",
            "Tres repeticoes por caso, nao independentes.",
            "Saidas invalidas permanecem no denominador.",
            "Nenhuma ferramenta fisica foi executada.",
        ],
    }

    summary_path = OUTPUT / "pt12_8_2_resumo.json"

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )

    print()
    print("RESULTADOS V4")
    print(
        f"Exact Match: {metrics['exact_match']}/360 "
        f"({metrics['exact_match_percent']:.2f}%)"
    )
    print(
        f"Positivos corretos: "
        f"{metrics['positive_correct']}/180"
    )
    print(
        f"Abstenções corretas: "
        f"{metrics['correct_abstentions']}/180"
    )
    print(
        f"Chamadas indevidas em negativos: "
        f"{metrics['unauthorized_negative_calls']}"
    )
    print(
        f"Atuações indevidas: "
        f"{metrics['unauthorized_actuations']}"
    )
    print(
        f"Saídas inválidas: "
        f"{metrics['invalid_predictions']}"
    )

    print()
    print("DISTRIBUIÇÃO DAS REGRAS")

    for rule, count in metrics["rules"].items():
        print(f"{rule}: {count}")

    print()
    print("ARQUIVOS GERADOS")

    for path in (detail_path, summary_path):
        print(
            f"{path.relative_to(ROOT)} "
            f"| SHA256 {sha256(path)}"
        )

    print()
    print("[OK] PT-12.5 concluída.")


if __name__ == "__main__":
    main()
