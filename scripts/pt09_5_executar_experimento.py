#!/usr/bin/env python3
"""PT-09.5 — Controlador experimental Needle 2 (Linux host)."""

import argparse
import hashlib
import json
import random
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "src/inference"))
from batch_runner import run_case

DATASET = ROOT / "dataset/frozen/colmeia-needle2-sintetico-v1-homologado.json"
MANIFEST = ROOT / "dataset/frozen/pt08_11_manifest.json"
SCHEMA = ROOT / "firmware/tools/colmeia.json"
MODEL = ROOT / "external/needle-2-esp32/model/needle2.cact"
BINARY = ROOT / "external/needle-2-esp32/build-host/nd_dump"
ENGINE = ROOT / "external/needle-2-esp32"

EXPECTED = {
    DATASET: "becf137d69b5eb39ad727f10be70b48672d2909d75a1c1563617e53f5a5fda18",
    SCHEMA: "aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2",
    MODEL: "b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba",
}

EXPECTED_ENGINE = "61cafad7014a5664bb3ffd5f0c457ce5aa6598ae"
EXPECTED_PROTOCOL_COMMIT = "2331634"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args, cwd=ROOT):
    return subprocess.check_output(
        ["git", "-C", str(cwd), *args],
        text=True
    ).strip()


def verify():
    print("=== VERIFICAÇÃO DE INTEGRIDADE ===")

    for path, expected in EXPECTED.items():
        require(path.is_file(), f"Arquivo ausente: {path}")
        actual = sha256(path)
        require(actual == expected, f"SHA-256 divergente: {path}")
        print(f"[OK] {path.relative_to(ROOT)}")

    require(BINARY.is_file(), "Executável ausente.")
    require(BINARY.stat().st_mode & 0o111, "Executável sem permissão.")

    engine_commit = git("rev-parse", "HEAD", cwd=ENGINE)
    require(engine_commit == EXPECTED_ENGINE, "Commit do motor divergente.")

    require(
        subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor",
             EXPECTED_PROTOCOL_COMMIT, "HEAD"],
            check=False
        ).returncode == 0,
        "Commit de homologação não encontrado no histórico atual."
    )

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    frozen = manifest["dataset_congelado"]
    require(frozen["sha256"] == sha256(DATASET), "Manifesto divergente.")
    require(manifest["estado"] == "HOMOLOGADO_CONGELADO",
            "Estado de homologação inválido.")

    data = json.loads(DATASET.read_text(encoding="utf-8"))
    cases = data["casos"]

    require(len(cases) == 180, "Quantidade de casos incorreta.")
    require(
        {c["id"] for c in cases} == set(range(37, 217)),
        "IDs incorretos ou duplicados."
    )
    require(
        all(c["status_validacao"] == "homologado" for c in cases),
        "Existe caso não homologado."
    )

    positives = sum(bool(c["chamadas_esperadas_revisadas"]) for c in cases)
    require(positives == 80, "Distribuição de gabaritos divergente.")

    print("[OK] 180 casos, 80 positivos, 100 negativos")
    print("[OK] Motor e commit de homologação verificados")
    return cases, engine_commit


def build_plan(cases, repetitions, seed):
    plan = [
        (case["id"], rep)
        for rep in range(1, repetitions + 1)
        for case in cases
    ]
    random.Random(seed).shuffle(plan)
    return plan


def write_new(path, obj):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def read_results(path, valid_keys):
    completed = set()
    if not path.exists():
        return completed

    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"JSONL inválido na linha {line_no}; "
                    "não altere o arquivo automaticamente."
                ) from exc

            key = (record["case_id"], record["repetition"])
            require(key in valid_keys, f"Registro inesperado: {key}")
            require(key not in completed, f"Registro duplicado: {key}")
            completed.add(key)

    return completed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20261022)
    parser.add_argument("--max-new", type=int, default=96)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--limit", type=int, default=0,
                        help="Somente para ensaio técnico, não para análise final.")
    args = parser.parse_args()

    require(args.repetitions > 0, "Repetições inválidas.")
    require(args.max_new > 0, "max-new inválido.")
    require(args.timeout > 0, "Timeout inválido.")
    require(0 <= args.limit <= 180, "Limite inválido.")

    cases, engine_commit = verify()
    case_map = {c["id"]: c for c in cases}

    plan = build_plan(cases, args.repetitions, args.seed)
    if args.limit:
        plan = plan[:args.limit]

    metadata = {
        "protocol": "PT-09.5",
        "dataset_sha256": sha256(DATASET),
        "manifest_sha256": sha256(MANIFEST),
        "schema_sha256": sha256(SCHEMA),
        "model_sha256": sha256(MODEL),
        "binary_sha256": sha256(BINARY),
        "engine_commit": engine_commit,
        "project_commit": git("rev-parse", "HEAD"),
        "repetitions": args.repetitions,
        "seed": args.seed,
        "max_new": args.max_new,
        "think": False,
        "timeout_seconds": args.timeout,
        "limit": args.limit,
        "planned_inferences": len(plan),
        "execution_environment": "Linux host x86-64",
        "physical_actions_enabled": False,
        "plan": [{"case_id": cid, "repetition": rep}
                 for cid, rep in plan]
    }

    print("\n=== PLANO EXPERIMENTAL ===")
    print(f"Casos: {len(cases)}")
    print(f"Repetições: {args.repetitions}")
    print(f"Inferências planejadas: {len(plan)}")
    print(f"Semente de ordenação: {args.seed}")
    print(f"max_new: {args.max_new}")
    print("think: false")
    print(f"timeout: {args.timeout} segundos")
    print("Ações físicas: desativadas")

    print("\nPrimeiras cinco posições:")
    for cid, rep in plan[:5]:
        print(f"  Caso {cid} | repetição {rep}")

    if args.dry_run:
        print("\n[OK] DRY-RUN CONCLUÍDO — nenhuma inferência realizada.")
        return

    require(args.run_dir is not None,
            "Informe --run-dir para executar ou retomar.")
    run_dir = args.run_dir.resolve()
    output_root = (ROOT / "results/experiments/needle2_frozen").resolve()
    require(
        run_dir.is_relative_to(output_root) and run_dir != output_root,
        "Diretório deve estar dentro de results/experiments/needle2_frozen/."
    )

    output_root.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)

    meta_file = run_dir / "metadata.json"
    results_file = run_dir / "raw_results.jsonl"

    if meta_file.exists():
        existing = json.loads(meta_file.read_text(encoding="utf-8"))
        require(existing == metadata,
                "Metadados divergentes. Não é seguro retomar.")
    else:
        require(not results_file.exists(),
                "Resultados existentes sem metadados.")
        write_new(meta_file, metadata)

    completed = read_results(results_file, set(plan))
    print(f"\nRegistros já concluídos: {len(completed)}")

    with results_file.open("a", encoding="utf-8") as stream:
        for index, (cid, rep) in enumerate(plan, 1):
            if (cid, rep) in completed:
                continue

            print(f"[{index}/{len(plan)}] Caso {cid} | repetição {rep}",
                  flush=True)

            result = run_case(
                case_map[cid],
                rep,
                args.max_new,
                False,
                args.timeout
            )

            result["family"] = case_map[cid]["familia"]
            result["experimental_protocol"] = "PT-09.5"

            stream.write(json.dumps(result, ensure_ascii=False) + "\n")
            stream.flush()

            print(
                f"  tempo={result['elapsed_wall_ms']} ms "
                f"retorno={result['returncode']} "
                f"erro={result['error']}",
                flush=True
            )

    final_count = len(read_results(results_file, set(plan)))
    print(f"\n[OK] Registros gravados: {final_count}/{len(plan)}")
    print(f"[OK] Resultados: {results_file}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, KeyError, ValueError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        sys.exit(1)
