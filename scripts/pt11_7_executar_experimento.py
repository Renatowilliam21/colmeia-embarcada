#!/usr/bin/env python3
"""PT-11.7: inferência sintética congelada com retomada segura."""

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src/inference"))

from batch_runner import run_case, BINARY, MODEL, SCHEMA  # noqa: E402

DATASET = ROOT / "dataset/validation/pt11/pt11_6_dataset_sintetico_congelado.jsonl"
OUTPUT = ROOT / "results/experiments/needle2_validation/pt11_7_experimento_principal"
RAW = OUTPUT / "raw_results.jsonl"
METADATA = OUTPUT / "metadata.json"

EXPECTED = {
    "dataset": "6ee8d7e0facc98b491fb52b39a51ad0debf4b64a7aa331d8a9e1d6f4abf47750",
    "model": "b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba",
    "schema": "aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2",
}
ENGINE_COMMIT = "61cafad7014a5664bb3ffd5f0c457ce5aa6598ae"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify():
    for name, path in (
        ("dataset", DATASET),
        ("model", MODEL),
        ("schema", SCHEMA),
    ):
        if not path.is_file():
            raise RuntimeError(f"Arquivo ausente: {path}")
        if sha256(path) != EXPECTED[name]:
            raise RuntimeError(f"SHA-256 divergente: {name}")

    if not BINARY.is_file() or not os.access(BINARY, os.X_OK):
        raise RuntimeError(f"Executável indisponível: {BINARY}")

    cases = []
    with DATASET.open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                cases.append(json.loads(line))

    if len(cases) != 120:
        raise RuntimeError("Dataset não possui 120 casos.")

    expected_groups = {
        "P1": 25, "P2": 15, "P3": 20,
        "N1": 10, "N2": 10, "N3": 10,
        "N4": 10, "N5": 10, "N6": 10,
    }
    if Counter(c.get("grupo") for c in cases) != expected_groups:
        raise RuntimeError("Distribuição dos grupos divergente.")

    ids = [c["id"] for c in cases]
    if len(set(ids)) != 120:
        raise RuntimeError("IDs duplicados no dataset.")

    return cases

def load_existing(cases, repetitions):
    completed = set()
    valid_ids = {case["id"] for case in cases}

    if not RAW.exists():
        return completed

    with RAW.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                raise RuntimeError(
                    f"Linha vazia no resultado: {line_number}"
                )
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"JSON inválido na linha {line_number}: {exc}"
                ) from exc

            key = (record.get("case_id"), record.get("repetition"))

            if key[0] not in valid_ids:
                raise RuntimeError(f"Caso desconhecido: {key}")
            if not isinstance(key[1], int) or not 1 <= key[1] <= repetitions:
                raise RuntimeError(f"Repetição inválida: {key}")
            if key in completed:
                raise RuntimeError(f"Registro duplicado: {key}")

            case = next(c for c in cases if c["id"] == key[0])
            if record.get("prompt") != case["frase"]:
                raise RuntimeError(f"Frase divergente: {key}")
            if record.get("category") != case["grupo"]:
                raise RuntimeError(f"Grupo divergente: {key}")
            if record.get("experimental_protocol") != "PT-11.7":
                raise RuntimeError(f"Protocolo divergente: {key}")

            completed.add(key)

    return completed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--max-new", type=int, default=96)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    if args.repetitions != 3 or args.max_new != 96 or args.timeout != 300:
        parser.error("Parâmetros congelados: repetitions=3, max-new=96, timeout=300.")

    if args.limit < 0 or args.limit > 120:
        parser.error("--limit deve estar entre 0 e 120.")

    cases = verify()
    OUTPUT.mkdir(parents=True, exist_ok=True)

    metadata = {
        "experimental_protocol": "PT-11.7",
        "dataset_sha256": EXPECTED["dataset"],
        "model_sha256": EXPECTED["model"],
        "schema_sha256": EXPECTED["schema"],
        "binary_sha256": sha256(BINARY),
        "engine_commit_reference": ENGINE_COMMIT,
        "repetitions": 3,
        "max_new": 96,
        "think": False,
        "timeout_seconds": 300,
        "selected_cases": 120,
        "execution_environment": "Linux host x86-64",
        "physical_actuation": False,
        "dataset_origin": "synthetic_ai_assisted",
        "human_independent_validation": False,
    }

    if METADATA.exists():
        existing = json.loads(METADATA.read_text(encoding="utf-8"))
        for key, value in metadata.items():
            if existing.get(key) != value:
                raise RuntimeError(f"Metadados incompatíveis: {key}")
    else:
        if RAW.exists():
            raise RuntimeError("Resultados existentes sem metadados.")
        metadata["created_at_utc"] = datetime.now(timezone.utc).isoformat()
        METADATA.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    completed = load_existing(cases, 3)
    total = 360

    print("=" * 60)
    print("PT-11.7 — EXPERIMENTO PRINCIPAL")
    print("=" * 60)
    print("Dataset:", len(cases), "casos")
    print("Inferências previstas:", total)
    print("Registros existentes:", len(completed))
    print("Pendentes:", total - len(completed))
    print("Arquivo:", RAW)

    if args.check_only:
        print("[OK] Verificação concluída; nenhuma inferência executada.")
        return

    executed_now = 0

    with RAW.open("a", encoding="utf-8") as out:
        for repetition in range(1, 4):
            for case in cases:
                key = (case["id"], repetition)
                if key in completed:
                    continue

                if args.limit and executed_now >= args.limit:
                    print("[PAUSA] Limite de novas inferências atingido.")
                    return

                print(
                    f"[{len(completed) + 1}/{total}] "
                    f"{case['id']} | repetição {repetition}",
                    flush=True,
                )

                adapted_case = {
                    "id": case["id"],
                    "categoria": case["grupo"],
                    "frase": case["frase"],
                }

                result = run_case(
                    adapted_case,
                    repetition,
                    max_new=96,
                    think=False,
                    timeout=300,
                )

                result["family"] = case["grupo"]
                result["experimental_protocol"] = "PT-11.7"

                out.write(json.dumps(result, ensure_ascii=False) + "\n")
                out.flush()
                os.fsync(out.fileno())

                completed.add(key)
                executed_now += 1

                print(
                    f"  tempo={result['elapsed_wall_ms']} ms | "
                    f"retorno={result['returncode']} | "
                    f"erro={result['error']}",
                    flush=True,
                )

    print()
    print("[OK] Execução finalizada.")
    print("Registros:", len(completed), "/", total)
    print("SHA-256 resultados:", sha256(RAW))

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        sys.exit(1)
