#!/usr/bin/env python3
"""PT-13.5 — Executor experimental com homologação obrigatória.

Não executa ferramentas de atuação física.
Não altera datasets, validadores, parser ou modelo.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src/inference"))

from batch_runner import run_case, BINARY, MODEL, SCHEMA  # noqa: E402


PROTOCOL = "PT-13.5"

DATASET = ROOT / (
    "dataset/validation/pt13/frozen/"
    "pt13_dataset_homologado.jsonl"
)

MANIFEST = ROOT / (
    "docs/metodologia/pt13/"
    "pt13_manifesto_homologacao.json"
)

OUTPUT = ROOT / (
    "results/experiments/needle2_validation/"
    "pt13/pt13_5_experimento_principal"
)

RAW = OUTPUT / "raw_results.jsonl"
METADATA = OUTPUT / "metadata.json"

VALIDATOR = ROOT / "src/safety/safety_validator_v4_2.py"

EXPECTED = {
    "model": (
        "b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba"
    ),
    "schema": (
        "aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2"
    ),
    "binary": (
        "7318a5784e0bb91487a2016ebfae7bd6aec2a6692ecb1a308a8bb3c2996577a4"
    ),
    "validator": (
        "77d69cecdb763ad2ad5e7ef5ab46803170be9db359430ff49053c5b4f3107b71"
    ),
}

ENGINE_COMMIT = "61cafad7014a5664bb3ffd5f0c457ce5aa6598ae"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_hash(path, expected, name):
    if not path.is_file():
        raise RuntimeError(f"Arquivo ausente: {name}: {path}")

    actual = sha256(path)

    if actual != expected:
        raise RuntimeError(
            f"SHA-256 divergente: {name}\n"
            f"Esperado: {expected}\n"
            f"Obtido:   {actual}"
        )


def verify():
    if not MANIFEST.is_file():
        raise RuntimeError(
            "Manifesto de homologação PT-13 inexistente. "
            "A coleta e a revisão humana precisam ser concluídas."
        )

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    required = {
        "status": "homologado",
        "dataset_origin": "human_authored",
        "human_review_completed": True,
        "independent_validation": True,
        "cases": 120,
    }

    for key, value in required.items():
        if manifest.get(key) != value:
            raise RuntimeError(
                f"Homologação inválida: {key}. "
                f"Esperado: {value!r}"
            )

    dataset_hash = manifest.get("dataset_sha256")
    if not isinstance(dataset_hash, str) or len(dataset_hash) != 64:
        raise RuntimeError("Hash do dataset ausente no manifesto.")

    verify_hash(DATASET, dataset_hash, "dataset PT-13")

    verify_hash(MODEL, EXPECTED["model"], "modelo")
    verify_hash(SCHEMA, EXPECTED["schema"], "schema")
    verify_hash(BINARY, EXPECTED["binary"], "binário")
    verify_hash(VALIDATOR, EXPECTED["validator"], "V4.2")

    if not os.access(BINARY, os.X_OK):
        raise RuntimeError("Binário de inferência não executável.")

    # O validador estrutural existente verifica os 120 registros,
    # a distribuição dos grupos, os tipos e as chamadas esperadas.
    check = subprocess.run(
        [
            sys.executable,
            "-m",
            "scripts.pt13_5_validar_entrada",
            "--dataset",
            str(DATASET),
            "--expected-sha256",
            dataset_hash,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if check.returncode != 0:
        raise RuntimeError(
            "Validação estrutural reprovada:\n"
            + check.stdout
            + check.stderr
        )

    cases = [
        json.loads(line)
        for line in DATASET.read_text(
            encoding="utf-8"
        ).splitlines()
    ]

    return cases, manifest


def load_existing(cases):
    completed = set()
    case_map = {case["id"]: case for case in cases}

    if not RAW.exists():
        return completed

    with RAW.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                raise RuntimeError(
                    f"Linha vazia nos resultados: {line_number}"
                )

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Resultado inválido na linha {line_number}: {exc}"
                ) from exc

            key = (
                record.get("case_id"),
                record.get("repetition"),
            )

            if key[0] not in case_map:
                raise RuntimeError(f"Caso desconhecido: {key}")

            if type(key[1]) is not int or not 1 <= key[1] <= 3:
                raise RuntimeError(f"Repetição inválida: {key}")

            if key in completed:
                raise RuntimeError(f"Registro duplicado: {key}")

            case = case_map[key[0]]

            if record.get("prompt") != case["frase"]:
                raise RuntimeError(f"Frase divergente: {key}")

            if record.get("category") != case["grupo"]:
                raise RuntimeError(f"Grupo divergente: {key}")

            if record.get("experimental_protocol") != PROTOCOL:
                raise RuntimeError(f"Protocolo divergente: {key}")

            completed.add(key)

    return completed


def main():
    parser = argparse.ArgumentParser()

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-only", action="store_true")
    mode.add_argument("--run", action="store_true")

    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Número máximo de novas inferências; 0 = todas.",
    )

    args = parser.parse_args()

    if args.limit < 0 or args.limit > 360:
        parser.error("--limit deve estar entre 0 e 360.")

    if args.check_only and args.limit:
        parser.error("--limit só pode ser usado com --run.")

    cases, manifest = verify()

    # Não criar diretórios ou metadados durante --check-only.
    if RAW.exists() and not METADATA.exists():
        raise RuntimeError(
            "Resultados existentes sem metadados. "
            "Retomada bloqueada."
        )

    metadata = {
        "experimental_protocol": PROTOCOL,
        "dataset_sha256": manifest["dataset_sha256"],
        "manifest_sha256": sha256(MANIFEST),
        "model_sha256": EXPECTED["model"],
        "schema_sha256": EXPECTED["schema"],
        "binary_sha256": EXPECTED["binary"],
        "validator_v4_2_sha256": EXPECTED["validator"],
        "engine_commit_reference": ENGINE_COMMIT,
        "repetitions": 3,
        "max_new": 96,
        "think": False,
        "timeout_seconds": 300,
        "selected_cases": 120,
        "execution_environment": "Linux host x86-64",
        "physical_actuation": False,
        "dataset_origin": "human_authored",
        "human_independent_validation": True,
    }

    if METADATA.exists():
        existing = json.loads(
            METADATA.read_text(encoding="utf-8")
        )

        for key, value in metadata.items():
            if existing.get(key) != value:
                raise RuntimeError(
                    f"Metadados incompatíveis: {key}"
                )

    completed = load_existing(cases)

    print("=" * 70)
    print("PT-13.5 — EXECUTOR EXPERIMENTAL")
    print("=" * 70)
    print("Dataset homologado:", len(cases), "casos")
    print("Inferências previstas:", 360)
    print("Registros existentes:", len(completed))
    print("Pendentes:", 360 - len(completed))
    print("Execução física: NÃO")

    if args.check_only:
        print(
            "\n[OK] Pré-requisitos verificados. "
            "Nenhuma inferência executada."
        )
        return

    OUTPUT.mkdir(parents=True, exist_ok=True)

    if not METADATA.exists():
        metadata["created_at_utc"] = datetime.now(
            timezone.utc
        ).isoformat()

        # Criação exclusiva: nunca sobrescrever metadados.
        with METADATA.open("x", encoding="utf-8") as stream:
            json.dump(
                metadata,
                stream,
                ensure_ascii=False,
                indent=2,
            )
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())

    executed_now = 0

    with RAW.open("a", encoding="utf-8") as out:
        for repetition in range(1, 4):
            for case in cases:
                key = (case["id"], repetition)

                if key in completed:
                    continue

                if args.limit and executed_now >= args.limit:
                    print(
                        "\n[PAUSA] Limite de inferências atingido."
                    )
                    return

                print(
                    f"[{len(completed) + 1}/360] "
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
                result["experimental_protocol"] = PROTOCOL

                out.write(
                    json.dumps(result, ensure_ascii=False) + "\n"
                )
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

    print("\n[OK] Execução concluída.")
    print("Registros:", len(completed), "/360")
    print("SHA-256:", sha256(RAW))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        sys.exit(1)
