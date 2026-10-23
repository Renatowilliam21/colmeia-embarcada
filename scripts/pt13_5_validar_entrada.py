#!/usr/bin/env python3
"""PT-13.5 — Validação estrutural do dataset PT-13."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

EXPECTED_GROUPS = {
    "P1": 25,
    "P2": 15,
    "P3": 20,
    "N1": 10,
    "N2": 10,
    "N3": 10,
    "N4": 10,
    "N5": 10,
    "N6": 10,
}

ALLOWED_TOOLS = {
    "consultar_status_colmeia",
    "listar_colmeias_alerta",
    "ativar_modo_inspecao",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_integer(value):
    return type(value) is int


def validate_calls(calls, case_id):
    errors = []

    if not isinstance(calls, list):
        return [f"{case_id}: chamadas_esperadas não é lista"]

    if len(calls) > 1:
        errors.append(
            f"{case_id}: mais de uma chamada esperada"
        )

    for call in calls:
        if not isinstance(call, dict):
            errors.append(
                f"{case_id}: chamada não é objeto"
            )
            continue

        if set(call) != {"name", "arguments"}:
            errors.append(
                f"{case_id}: estrutura de chamada inválida"
            )
            continue

        name = call["name"]
        args = call["arguments"]

        if name not in ALLOWED_TOOLS:
            errors.append(
                f"{case_id}: ferramenta desconhecida: {name}"
            )
            continue

        if not isinstance(args, dict):
            errors.append(
                f"{case_id}: argumentos inválidos"
            )
            continue

        if name == "consultar_status_colmeia":
            if (
                set(args) != {"colmeia_id"}
                or not is_integer(args.get("colmeia_id"))
                or not 1 <= args["colmeia_id"] <= 50
            ):
                errors.append(
                    f"{case_id}: argumentos de status inválidos"
                )

        elif name == "listar_colmeias_alerta":
            if args != {}:
                errors.append(
                    f"{case_id}: alertas exige argumentos vazios"
                )

        elif name == "ativar_modo_inspecao":
            if (
                set(args) != {"colmeia_id", "duracao_min"}
                or not is_integer(args.get("colmeia_id"))
                or not is_integer(args.get("duracao_min"))
                or not 1 <= args["colmeia_id"] <= 50
                or not 5 <= args["duracao_min"] <= 60
            ):
                errors.append(
                    f"{case_id}: argumentos de inspeção inválidos"
                )

    return errors


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--expected-sha256",
        required=True,
    )

    args = parser.parse_args()

    path = args.dataset

    if not path.is_file():
        raise SystemExit(
            f"[ERRO] Dataset inexistente: {path}"
        )

    actual_hash = sha256(path)

    if actual_hash != args.expected_sha256.lower():
        raise SystemExit(
            "[ERRO] SHA-256 divergente.\n"
            f"Esperado: {args.expected_sha256}\n"
            f"Encontrado: {actual_hash}"
        )

    records = []
    errors = []
    ids = set()

    with path.open(encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            if not line.strip():
                errors.append(
                    f"Linha {line_number}: linha vazia"
                )
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(
                    f"Linha {line_number}: JSON inválido: {exc}"
                )
                continue

            if not isinstance(record, dict):
                errors.append(
                    f"Linha {line_number}: registro não é objeto"
                )
                continue

            records.append(record)

            case_id = record.get("id")
            group = record.get("grupo")
            phrase = record.get("frase")
            calls = record.get("chamadas_esperadas")

            if not isinstance(case_id, str):
                errors.append(
                    f"Linha {line_number}: ID inválido"
                )
                continue

            if case_id in ids:
                errors.append(
                    f"ID duplicado: {case_id}"
                )

            ids.add(case_id)

            if group not in EXPECTED_GROUPS:
                errors.append(
                    f"{case_id}: grupo desconhecido"
                )
            elif not case_id.startswith(f"PT13-{group}-"):
                errors.append(
                    f"{case_id}: ID incompatível com o grupo"
                )

            if not isinstance(phrase, str) or not phrase.strip():
                errors.append(
                    f"{case_id}: frase vazia ou inválida"
                )

            errors.extend(
                validate_calls(calls, case_id)
            )

            if isinstance(calls, list):
                if group in {"P1", "P2", "P3"}:
                    expected_tool = {
                        "P1": "consultar_status_colmeia",
                        "P2": "listar_colmeias_alerta",
                        "P3": "ativar_modo_inspecao",
                    }[group]

                    if (
                        len(calls) != 1
                        or not isinstance(calls[0], dict)
                        or calls[0].get("name") != expected_tool
                    ):
                        errors.append(
                            f"{case_id}: chamada incompatível "
                            f"com grupo positivo"
                        )
                elif group in EXPECTED_GROUPS and calls != []:
                    errors.append(
                        f"{case_id}: grupo negativo deve abster"
                    )

    counts = Counter(
        record.get("grupo")
        for record in records
        if isinstance(record.get("grupo"), str)
    )

    if len(records) != 120:
        errors.append(
            f"Esperados 120 registros; encontrados {len(records)}"
        )

    for group, expected in EXPECTED_GROUPS.items():
        if counts[group] != expected:
            errors.append(
                f"{group}: esperado {expected}, "
                f"encontrado {counts[group]}"
            )

    print("=" * 70)
    print("PT-13.5 — VALIDAÇÃO ESTRUTURAL")
    print("=" * 70)

    print("Dataset:", path)
    print("SHA-256:", actual_hash)
    print("Registros:", len(records))
    print("Erros:", len(errors))

    for error in errors:
        print("[ERRO]", error)

    if errors:
        raise SystemExit(
            "\n[REPROVADO] Dataset não autorizado para inferência."
        )

    print("\n[OK] Estrutura do dataset validada.")
    print(
        "[ATENÇÃO] A validação estrutural não substitui "
        "a revisão semântica humana."
    )


if __name__ == "__main__":
    main()
