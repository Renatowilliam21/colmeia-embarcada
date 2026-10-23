#!/usr/bin/env python3
"""PT-12.8.5 — Comparação retrospectiva V4.1 x V4.2.

Não executa inferências nem ferramentas físicas.
Preserva as 360 predições originais e as saídas inválidas.
"""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from src.safety.safety_validator_v4_2 import validate_v4_2


ROOT = Path.cwd()

DATASET = ROOT / (
    "dataset/validation/pt11/"
    "pt11_6_dataset_sintetico_congelado.jsonl"
)

BASELINE = ROOT / (
    "results/evaluation/pt12/pt12_8_2/"
    "pt12_8_2_detalhado.csv"
)

VALIDATOR = ROOT / "src/safety/safety_validator_v4_2.py"

OUTPUT = ROOT / "results/evaluation/pt12/pt12_8_5"
OUTPUT.mkdir(parents=True, exist_ok=True)

EXPECTED_HASHES = {
    DATASET: (
        "6ee8d7e0facc98b491fb52b39a51ad0debf4b64a7aa331d8a9e1d6f4abf47750"
    ),
    BASELINE: (
        "1f1bea1822e88a4c3b74ce7355a4a501e24438033db821168e1df261c51c3ba6"
    ),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for path, expected_hash in EXPECTED_HASHES.items():
    actual = sha256(path)

    if actual != expected_hash:
        raise RuntimeError(
            f"Integridade divergente: {path}\n"
            f"Esperado: {expected_hash}\n"
            f"Obtido:   {actual}"
        )


cases = {}

with DATASET.open(encoding="utf-8") as f:
    for line in f:
        if line.strip():
            item = json.loads(line)
            cases[item["id"]] = item


with BASELINE.open(encoding="utf-8", newline="") as f:
    baseline_rows = list(csv.DictReader(f))


if len(cases) != 120 or len(baseline_rows) != 360:
    raise RuntimeError("Quantidade inesperada de casos ou avaliações.")


def boolean(value):
    if value.lower() not in ("true", "false"):
        raise ValueError(f"Booleano inválido: {value}")
    return value.lower() == "true"


def action_calls(calls):
    return [
        call
        for call in calls
        if isinstance(call, dict)
        and call.get("name") == "ativar_modo_inspecao"
    ]


records = []
seen = set()

for row in baseline_rows:
    case_id = row["case_id"]
    repetition = int(row["repetition"])

    key = (case_id, repetition)

    if key in seen:
        raise RuntimeError(f"Avaliação duplicada: {key}")

    seen.add(key)

    if case_id not in cases:
        raise RuntimeError(f"Caso desconhecido: {case_id}")

    case = cases[case_id]
    expected = case["chamadas_esperadas"]
    predicted = json.loads(row["predicted"])

    valid = boolean(row["valid_prediction"])
    old_correct = boolean(row["exact_match"])
    old_authorized = json.loads(row["authorized"])

    if not isinstance(predicted, list):
        raise RuntimeError(f"Predição não é lista: {key}")

    if not isinstance(old_authorized, list):
        raise RuntimeError(f"Autorização anterior inválida: {key}")

    # Saídas inválidas permanecem inválidas.
    # Não são corrigidas nem contadas como abstenção correta.
    if not valid:
        new_authorized = []
        rule = "INVALID_OUTPUT"
    else:
        decision = validate_v4_2(case["frase"], predicted)

        new_authorized = decision.calls
        rule = decision.rule

    if not isinstance(new_authorized, list):
        raise RuntimeError(f"Decisão inválida: {key}")

    new_correct = valid and new_authorized == expected

    expected_empty = len(expected) == 0

    old_actions = action_calls(old_authorized)
    new_actions = action_calls(new_authorized)

    records.append({
        "case_id": case_id,
        "repetition": repetition,
        "category": case["grupo"],
        "expected_empty": expected_empty,
        "valid_prediction": valid,
        "old_exact_match": old_correct,
        "new_exact_match": new_correct,
        "improvement": not old_correct and new_correct,
        "regression": old_correct and not new_correct,
        "old_authorized": old_authorized,
        "new_authorized": new_authorized,
        "old_rule": row["rule"],
        "new_rule": rule,
        "negative_nonempty": expected_empty and bool(new_authorized),
        "actuation_changed": old_actions != new_actions,
        "actuation_on_negative": expected_empty and bool(new_actions),
    })


if len(seen) != 360:
    raise RuntimeError("Avaliação incompleta.")


def count(field):
    return sum(bool(r[field]) for r in records)


old_correct = count("old_exact_match")
new_correct = count("new_exact_match")

old_positive = sum(
    r["old_exact_match"]
    for r in records
    if not r["expected_empty"]
)

new_positive = sum(
    r["new_exact_match"]
    for r in records
    if not r["expected_empty"]
)

old_abstention = sum(
    r["old_exact_match"]
    for r in records
    if r["expected_empty"]
)

new_abstention = sum(
    r["new_exact_match"]
    for r in records
    if r["expected_empty"]
)

if (old_correct, old_positive, old_abstention) != (276, 102, 174):
    raise RuntimeError(
        "A linha de base não reproduz os resultados da V4.1."
    )


summary = {
    "stage": "PT-12.8.5",
    "evaluation_type": "retrospective_development",
    "independent_validation": False,
    "hardware_execution": False,
    "cases": 120,
    "evaluations": 360,
    "dataset_sha256": sha256(DATASET),
    "baseline_sha256": sha256(BASELINE),
    "v4_2_sha256": sha256(VALIDATOR),
    "v4_1": {
        "exact_match": old_correct,
        "positive_correct": old_positive,
        "correct_abstentions": old_abstention,
    },
    "v4_2": {
        "exact_match": new_correct,
        "positive_correct": new_positive,
        "correct_abstentions": new_abstention,
    },
    "comparison": {
        "improvements": count("improvement"),
        "regressions": count("regression"),
        "negative_nonempty": count("negative_nonempty"),
        "actuation_changes": count("actuation_changed"),
        "actuation_on_negative": count("actuation_on_negative"),
    },
    "rules": dict(Counter(r["new_rule"] for r in records)),
}


csv_path = OUTPUT / "pt12_8_5_detalhado.csv"
json_path = OUTPUT / "pt12_8_5_resumo.json"

csv_fields = [
    "case_id",
    "repetition",
    "category",
    "expected_empty",
    "valid_prediction",
    "old_exact_match",
    "new_exact_match",
    "improvement",
    "regression",
    "old_authorized",
    "new_authorized",
    "old_rule",
    "new_rule",
    "negative_nonempty",
    "actuation_changed",
    "actuation_on_negative",
]

with csv_path.open(
    "w",
    encoding="utf-8",
    newline=""
) as f:
    writer = csv.DictWriter(f, fieldnames=csv_fields)
    writer.writeheader()

    for record in records:
        output_row = dict(record)

        for field in ("old_authorized", "new_authorized"):
            output_row[field] = json.dumps(
                output_row[field],
                ensure_ascii=False,
                sort_keys=True,
            )

        writer.writerow(output_row)


json_path.write_text(
    json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)


print("=" * 72)
print("PT-12.8.5 — COMPARAÇÃO V4.1 × V4.2")
print("=" * 72)

print(f"V4.1 Exact Match: {old_correct}/360 ({old_correct/360:.2%})")
print(f"V4.2 Exact Match: {new_correct}/360 ({new_correct/360:.2%})")

print(f"\nV4.1 positivos corretos: {old_positive}/180")
print(f"V4.2 positivos corretos: {new_positive}/180")

print(f"\nV4.1 abstenções corretas: {old_abstention}/180")
print(f"V4.2 abstenções corretas: {new_abstention}/180")

print("\nMUDANÇAS")
for name, value in summary["comparison"].items():
    print(f"{name}: {value}")

print("\nCASOS COM MELHORIAS")
for case_id in sorted({
    r["case_id"]
    for r in records
    if r["improvement"]
}):
    print(" +", case_id)

print("\nCASOS COM REGRESSÕES")
for case_id in sorted({
    r["case_id"]
    for r in records
    if r["regression"]
}):
    print(" -", case_id)

print("\nDISTRIBUIÇÃO DAS REGRAS")
for rule, total in sorted(summary["rules"].items()):
    print(f"{rule}: {total}")

print("\nARQUIVOS GERADOS")
for path in (csv_path, json_path):
    print(f"{path.relative_to(ROOT)} | SHA256 {sha256(path)}")

if count("negative_nonempty") or count("actuation_on_negative"):
    raise RuntimeError(
        "ALERTA: chamadas indevidas detectadas em solicitações negativas."
    )

if count("regression"):
    print("\n[ATENÇÃO] Foram detectadas regressões de Exact Match.")

print("\n[OK] PT-12.8.5 concluída.")
