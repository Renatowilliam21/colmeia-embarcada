#!/usr/bin/env python3
"""PT-09.8 — Avaliação independente do dataset congelado Needle 2."""

import csv
import hashlib
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATASET = ROOT / "dataset/frozen/colmeia-needle2-sintetico-v1-homologado.json"
RUN = ROOT / "results/experiments/needle2_frozen/pt09_7_experimento_principal"
RESULTS = RUN / "raw_results.jsonl"
METADATA = RUN / "metadata.json"
OUTPUT = ROOT / "results/evaluation/pt09_8"

EXPECTED_HASH = (
    "becf137d69b5eb39ad727f10be70b48672d2909d75a1c1563617e53f5a5fda18"
)

TOOLS = {
    "consultar_status_colmeia": {"colmeia_id": (1, 50)},
    "listar_colmeias_alerta": {},
    "ativar_modo_inspecao": {
        "colmeia_id": (1, 50),
        "duracao_min": (5, 60),
    },
}

ACTION = "ativar_modo_inspecao"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def percentile(values, p):
    ordered = sorted(values)
    if not ordered:
        return None
    position = (len(ordered) - 1) * p / 100
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def validate_calls(calls):
    if not isinstance(calls, list):
        return False, "resposta_nao_e_lista"

    actions = 0

    for index, call in enumerate(calls):
        if not isinstance(call, dict):
            return False, f"chamada_{index}_nao_e_objeto"

        if set(call) != {"name", "arguments"}:
            return False, f"estrutura_invalida_{index}"

        name = call["name"]
        arguments = call["arguments"]

        if name not in TOOLS:
            return False, f"ferramenta_desconhecida_{index}"

        if not isinstance(arguments, dict):
            return False, f"argumentos_invalidos_{index}"

        rules = TOOLS[name]

        if set(arguments) != set(rules):
            return False, f"parametros_incorretos_{index}"

        for key, (minimum, maximum) in rules.items():
            value = arguments[key]

            if type(value) is not int:
                return False, f"tipo_invalido_{key}"

            if not minimum <= value <= maximum:
                return False, f"fora_dos_limites_{key}"

        if name == ACTION:
            actions += 1

    if actions > 1:
        return False, "multiplas_acoes_nao_permitidas"

    return True, None


def action_calls(calls):
    if not isinstance(calls, list):
        return []

    return [
        call for call in calls
        if isinstance(call, dict)
        and call.get("name") == ACTION
    ]


def aggregate(rows):
    total = len(rows)
    require(total > 0, "Grupo vazio.")

    correct = sum(row["exact_match"] for row in rows)
    valid = sum(row["schema_valido"] for row in rows)
    abstention_cases = [
        row for row in rows if row["esperado_vazio"]
    ]
    authorized_cases = [
        row for row in rows if not row["esperado_vazio"]
    ]

    correct_abstentions = sum(
        row["abstencao_correta"] for row in abstention_cases
    )

    unwarranted_calls = sum(
        row["chamada_indevida"] for row in abstention_cases
    )

    times = [row["elapsed_wall_ms"] for row in rows]

    return {
        "total": total,
        "exact_match": correct,
        "exact_match_percent": round(100 * correct / total, 4),
        "schema_validos": valid,
        "schema_validos_percent": round(100 * valid / total, 4),
        "casos_abstencao_esperada": len(abstention_cases),
        "abstencoes_corretas": correct_abstentions,
        "taxa_abstencao_correta_percent": (
            round(100 * correct_abstentions / len(abstention_cases), 4)
            if abstention_cases else None
        ),
        "chamadas_indevidas": unwarranted_calls,
        "taxa_chamadas_indevidas_percent": (
            round(100 * unwarranted_calls / len(abstention_cases), 4)
            if abstention_cases else None
        ),
        "casos_chamada_esperada": len(authorized_cases),
        "falhas_em_casos_com_chamada_esperada": sum(
            not row["exact_match"] for row in authorized_cases
        ),
        "acionamentos_indevidos": sum(
            row["acionamento_indevido"] for row in rows
        ),
        "erros_parsing": sum(row["erro_parsing"] for row in rows),
        "erros_execucao": sum(row["erro_execucao"] for row in rows),
        "latencia_media_ms": round(statistics.mean(times), 3),
        "latencia_mediana_ms": round(statistics.median(times), 3),
        "latencia_p90_ms": round(percentile(times, 90), 3),
        "latencia_p95_ms": round(percentile(times, 95), 3),
    }


def write_csv(path, rows):
    if not rows:
        return

    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()

        for row in rows:
            writer.writerow({
                key: canonical(value)
                if isinstance(value, (list, dict)) else value
                for key, value in row.items()
            })


def main():
    print("=== PT-09.8 — AVALIAÇÃO EXPERIMENTAL ===")

    dataset_hash = hashlib.sha256(DATASET.read_bytes()).hexdigest()
    require(dataset_hash == EXPECTED_HASH, "Hash do dataset divergente.")

    metadata = json.loads(METADATA.read_text(encoding="utf-8"))

    require(
        metadata["dataset_sha256"] == dataset_hash,
        "Dataset diferente daquele utilizado na inferência."
    )
    require(
        metadata["planned_inferences"] == 540,
        "Plano experimental inesperado."
    )
    require(
        metadata["repetitions"] == 3,
        "Quantidade de repetições inesperada."
    )

    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    cases = dataset["casos"]

    require(len(cases) == 180, "Dataset não contém 180 casos.")

    by_id = {case["id"]: case for case in cases}
    require(len(by_id) == 180, "IDs duplicados no dataset.")

    records = [
        json.loads(line)
        for line in RESULTS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    require(len(records) == 540, "Quantidade de resultados incorreta.")

    expected_keys = {
        (item["case_id"], item["repetition"])
        for item in metadata["plan"]
    }

    actual_keys = [
        (record["case_id"], record["repetition"])
        for record in records
    ]

    require(
        len(set(actual_keys)) == 540,
        "Existem registros duplicados."
    )
    require(
        set(actual_keys) == expected_keys,
        "Resultados diferentes do plano experimental."
    )

    detailed = []

    for record in records:
        case = by_id[record["case_id"]]

        require(
            record["prompt"] == case["frase"],
            f"Frase divergente no caso {case['id']}."
        )

        expected = case["chamadas_esperadas_revisadas"]
        predicted = record["parsed_calls"]

        require(
            isinstance(expected, list),
            f"Gabarito inválido no caso {case['id']}."
        )

        expected_valid, expected_error = validate_calls(expected)
        require(
            expected_valid,
            f"Gabarito inválido no caso {case['id']}: {expected_error}"
        )

        valid, schema_error = validate_calls(predicted)

        execution_error = (
            record["returncode"] != 0
            or record["error"] is not None
        )

        parsing_error = (
            record["parse_error"] is not None
            or not isinstance(predicted, list)
        )

        exact = (
            not execution_error
            and not parsing_error
            and canonical(predicted) == canonical(expected)
        )

        expected_empty = len(expected) == 0
        predicted_empty = (
            isinstance(predicted, list)
            and len(predicted) == 0
        )

        correct_abstention = (
            expected_empty
            and predicted_empty
            and not execution_error
            and not parsing_error
        )

        unwarranted = (
            expected_empty
            and isinstance(predicted, list)
            and len(predicted) > 0
        )

        predicted_actions = action_calls(predicted)
        expected_actions = action_calls(expected)

        unauthorized_action = (
            bool(predicted_actions)
            and canonical(predicted_actions)
            != canonical(expected_actions)
        )

        detailed.append({
            "case_id": case["id"],
            "repetition": record["repetition"],
            "categoria": case["categoria"],
            "familia": case["familia"],
            "frase": case["frase"],
            "esperado": expected,
            "predito": predicted,
            "exact_match": exact,
            "schema_valido": valid and not parsing_error,
            "erro_schema": schema_error,
            "esperado_vazio": expected_empty,
            "abstencao_correta": correct_abstention,
            "chamada_indevida": unwarranted,
            "acionamento_indevido": unauthorized_action,
            "erro_parsing": parsing_error,
            "erro_execucao": execution_error,
            "elapsed_wall_ms": record["elapsed_wall_ms"],
        })

    by_category = defaultdict(list)
    by_family = defaultdict(list)
    by_case = defaultdict(list)

    for row in detailed:
        by_category[row["categoria"]].append(row)
        by_family[row["familia"]].append(row)
        by_case[row["case_id"]].append(row)

    category_rows = [
        {"categoria": name, **aggregate(group)}
        for name, group in sorted(by_category.items())
    ]

    family_rows = [
        {"familia": name, **aggregate(group)}
        for name, group in sorted(by_family.items())
    ]

    stability_rows = []

    for case_id, group in sorted(by_case.items()):
        require(len(group) == 3, f"Caso {case_id} sem três repetições.")

        predictions = [
            canonical(row["predito"])
            for row in group
        ]

        all_equal = len(set(predictions)) == 1

        stability_rows.append({
            "case_id": case_id,
            "categoria": group[0]["categoria"],
            "familia": group[0]["familia"],
            "predicoes_identicas": all_equal,
            "acertos_nas_tres_repeticoes": sum(
                row["exact_match"] for row in group
            ),
            "todas_corretas": all(
                row["exact_match"] for row in group
            ),
        })

    summary = aggregate(detailed)

    summary["casos_distintos"] = 180
    summary["repeticoes"] = 3
    summary["dataset_sha256"] = dataset_hash
    summary["resultados_sha256"] = hashlib.sha256(
        RESULTS.read_bytes()
    ).hexdigest()

    summary["casos_com_predicoes_identicas"] = sum(
        row["predicoes_identicas"] for row in stability_rows
    )

    summary["casos_com_tres_acertos"] = sum(
        row["todas_corretas"] for row in stability_rows
    )

    summary["casos_com_zero_acertos"] = sum(
        row["acertos_nas_tres_repeticoes"] == 0
        for row in stability_rows
    )

    summary["erros_schema"] = dict(Counter(
        row["erro_schema"] or "sem_erro"
        for row in detailed
    ))

    OUTPUT.mkdir(parents=True, exist_ok=True)

    write_csv(
        OUTPUT / "pt09_8_resultados_detalhados.csv",
        detailed
    )

    write_csv(
        OUTPUT / "pt09_8_por_categoria.csv",
        category_rows
    )

    write_csv(
        OUTPUT / "pt09_8_por_familia.csv",
        family_rows
    )

    write_csv(
        OUTPUT / "pt09_8_estabilidade.csv",
        stability_rows
    )

    (OUTPUT / "pt09_8_resumo.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    report = [
        "# PT-09.8 — Avaliação experimental Needle 2",
        "",
        "## Resultados gerais",
        "",
        f"- Inferências: {summary['total']}",
        f"- Exact Match: {summary['exact_match']}/{summary['total']} "
        f"({summary['exact_match_percent']:.2f}%)",
        f"- Schema válido: {summary['schema_validos']}/{summary['total']} "
        f"({summary['schema_validos_percent']:.2f}%)",
        f"- Abstenções corretas: {summary['abstencoes_corretas']}/"
        f"{summary['casos_abstencao_esperada']}",
        f"- Chamadas indevidas: {summary['chamadas_indevidas']}",
        f"- Acionamentos indevidos: {summary['acionamentos_indevidos']}",
        f"- Erros de parsing: {summary['erros_parsing']}",
        f"- Latência média: {summary['latencia_media_ms']:.2f} ms",
        f"- Latência mediana: {summary['latencia_mediana_ms']:.2f} ms",
        f"- Latência P95: {summary['latencia_p95_ms']:.2f} ms",
        "",
        "## Estabilidade",
        "",
        f"- Casos com três predições idênticas: "
        f"{summary['casos_com_predicoes_identicas']}/180",
        f"- Casos corretos nas três repetições: "
        f"{summary['casos_com_tres_acertos']}/180",
        f"- Casos incorretos nas três repetições: "
        f"{summary['casos_com_zero_acertos']}/180",
        "",
        "## Limitações metodológicas",
        "",
        "- O dataset é sintético e derivado de modelos de frases.",
        "- As três repetições não são observações independentes.",
        "- Os resultados foram obtidos em Linux host, não em ESP32.",
        "- O indicador CONF não foi interpretado como probabilidade calibrada.",
        "- Nenhuma ação física foi executada.",
        "- Uma chamada estruturalmente válida não garante segurança.",
        "- A ordem das chamadas é considerada no Exact Match.",
        "- Acionamento indevido é definido como chamada de inspeção "
        "diferente das chamadas de inspeção esperadas.",
        "",
    ]

    (OUTPUT / "pt09_8_relatorio.md").write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\n=== RESULTADOS GERAIS ===")
    print(f"Exact Match: {summary['exact_match']}/540 "
          f"({summary['exact_match_percent']:.2f}%)")
    print(f"Schema válido: {summary['schema_validos']}/540 "
          f"({summary['schema_validos_percent']:.2f}%)")
    print(f"Abstenções corretas: "
          f"{summary['abstencoes_corretas']}/"
          f"{summary['casos_abstencao_esperada']}")
    print(f"Chamadas indevidas: {summary['chamadas_indevidas']}")
    print(f"Acionamentos indevidos: {summary['acionamentos_indevidos']}")
    print(f"Erros de parsing: {summary['erros_parsing']}")
    print(f"Latência média: {summary['latencia_media_ms']:.2f} ms")
    print(f"Latência P95: {summary['latencia_p95_ms']:.2f} ms")

    print("\n=== ESTABILIDADE ===")
    print(
        "Casos com predições idênticas:",
        summary["casos_com_predicoes_identicas"],
        "/180"
    )
    print(
        "Casos corretos nas três repetições:",
        summary["casos_com_tres_acertos"],
        "/180"
    )
    print(
        "Casos incorretos nas três repetições:",
        summary["casos_com_zero_acertos"],
        "/180"
    )

    print("\n=== RESULTADOS POR CATEGORIA ===")

    for row in category_rows:
        print(
            f"{row['categoria']}: "
            f"{row['exact_match']}/{row['total']} "
            f"({row['exact_match_percent']:.2f}%)"
        )

    print("\n=== ARQUIVOS GERADOS ===")

    for path in sorted(OUTPUT.iterdir()):
        if path.is_file() and path.name.startswith("pt09_8_"):
            print(path.relative_to(ROOT))

    print("\n[OK] PT-09.8 concluída.")


if __name__ == "__main__":
    main()
