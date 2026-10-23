#!/usr/bin/env python3
"""PT-12.10 — Congelamento da V4.2 para validação futura."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()

OUTPUT = ROOT / (
    "docs/metodologia/pt12/"
    "pt12_10_manifesto_congelamento.json"
)

FILES = {
    "dataset_pt11": (
        "dataset/validation/pt11/"
        "pt11_6_dataset_sintetico_congelado.jsonl"
    ),
    "inference_pt11": (
        "results/experiments/needle2_validation/"
        "pt11_7_experimento_principal/raw_results.jsonl"
    ),
    "validator_v4": "src/safety/safety_validator_v4.py",
    "validator_v4_1": "src/safety/safety_validator_v4_1.py",
    "validator_v4_2": "src/safety/safety_validator_v4_2.py",
    "tests_v4_2": "tests/test_safety_validator_v4_2.py",
    "evaluation_pt12_8_5": (
        "results/evaluation/pt12/pt12_8_5/"
        "pt12_8_5_resumo.json"
    ),
    "adversarial_pt12_9": (
        "results/evaluation/pt12/pt12_9/"
        "pt12_9_resumo.json"
    ),
}

EXPECTED = {
    "dataset_pt11":
        "6ee8d7e0facc98b491fb52b39a51ad0debf4b64a7aa331d8a9e1d6f4abf47750",
    "inference_pt11":
        "fba9ce9e24a2c7019a49b0edecee873ae4bb1e1e412c3410267c5efdce53253f",
    "validator_v4":
        "65ed06c144ca571929869336d8f74b859de2613f4b3330057702e8f3c0d2a190",
    "validator_v4_1":
        "1e7df9d4d839221f469ef81fa05098fa7781f944848fd766b600a8ab00905565",
    "evaluation_pt12_8_5":
        "80f7d86e325c4560ced030c16c617f6092aeee1485ac6676b0a509370ca1abb6",
    "adversarial_pt12_9":
        "a5ee5fc852fc95f0bfe46afdce577e6c6a9c238c0ac380992e3e10e350810bdf",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


hashes = {}

for name, relative_path in FILES.items():
    path = ROOT / relative_path

    if not path.is_file():
        raise FileNotFoundError(relative_path)

    digest = sha256(path)

    if name in EXPECTED and digest != EXPECTED[name]:
        raise RuntimeError(
            f"Integridade divergente: {relative_path}"
        )

    hashes[name] = {
        "path": relative_path,
        "sha256": digest,
    }

evaluation = json.loads(
    (ROOT / FILES["evaluation_pt12_8_5"]).read_text(
        encoding="utf-8"
    )
)

adversarial = json.loads(
    (ROOT / FILES["adversarial_pt12_9"]).read_text(
        encoding="utf-8"
    )
)

assert evaluation["evaluations"] == 360
assert evaluation["v4_2"]["exact_match"] == 309
assert evaluation["v4_2"]["positive_correct"] == 135
assert evaluation["v4_2"]["correct_abstentions"] == 174

assert evaluation["comparison"]["regressions"] == 0
assert evaluation["comparison"]["negative_nonempty"] == 0
assert evaluation["comparison"]["actuation_on_negative"] == 0

assert adversarial["total"] == 24
assert adversarial["passed"] == 24
assert adversarial["failed"] == 0

manifest = {
    "stage": "PT-12.10",
    "created_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "status": "frozen_experimental_candidate",
    "validator": "V4.2",
    "development_dataset": "PT-11",
    "independent_validation": False,
    "human_homologation_pt11": False,
    "hardware_execution": False,
    "physical_actuation_authorized": False,
    "results": {
        "exact_match": 309,
        "total_evaluations": 360,
        "positive_correct": 135,
        "correct_abstentions": 174,
        "negative_unauthorized_calls": 0,
        "adversarial_passed": 24,
        "adversarial_total": 24,
    },
    "artifacts": hashes,
    "next_stage": "PT-13 independent validation",
}

if OUTPUT.exists():
    raise FileExistsError(
        "Manifesto já existente. Não sobrescrever."
    )

OUTPUT.write_text(
    json.dumps(
        manifest,
        ensure_ascii=False,
        indent=2,
    ) + "\n",
    encoding="utf-8",
)

print("=" * 70)
print("PT-12.10 — CONGELAMENTO EXPERIMENTAL")
print("=" * 70)

for name, item in hashes.items():
    print(f"[OK] {name}: {item['sha256']}")

print()
print(f"[OK] Manifesto: {OUTPUT.relative_to(ROOT)}")
print(f"[OK] SHA256: {sha256(OUTPUT)}")
print("[OK] V4.2 registrada como candidata experimental.")
print("[PENDENTE] Validação independente PT-13.")
