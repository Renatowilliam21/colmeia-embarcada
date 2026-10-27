#!/usr/bin/env python3
"""Avaliação exploratória Needle 2 — gabarito original preservado."""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATASET = ROOT / "dataset/colmeia-needle2-dataset-teste.json"
RESULTS = (
    ROOT / "results/experiments/needle2_host/"
    "20261022T200512Z/raw_results.jsonl"
)
OUTPUT = ROOT / "results/evaluation"
OUTPUT.mkdir(parents=True, exist_ok=True)

TOOLS = {
    "consultar_status_colmeia": {"colmeia_id": (1, 50)},
    "listar_colmeias_alerta": {},
    "ativar_modo_inspecao": {
        "colmeia_id": (1, 50),
        "duracao_min": (5, 60),
    },
}

# Casos sinalizados pela auditoria anterior.
# Não alteramos o gabarito nem os excluímos das métricas brutas.
REVISAR_GABARITO = {17, 18, 19, 22, 23, 25, 27}


def normalizar_esperado(caso):
    ferramenta = caso.get("ferramenta_esperada")
    argumentos = caso.get("argumentos_esperados")

    if ferramenta is None:
        if argumentos is not None:
            return None, "ferramenta nula com argumentos não nulos"
        return [], None

    if not isinstance(ferramenta, str):
        return None, "formato de ferramenta não suportado"

    if not isinstance(argumentos, dict):
        return None, "argumentos esperados não são objeto"

    return [{
        "name": ferramenta,
        "arguments": argumentos,
    }], None


def validar_chamadas(chamadas):
    if not isinstance(chamadas, list):
        return False, "resposta não é lista"

    for i, chamada in enumerate(chamadas):
        if not isinstance(chamada, dict):
            return False, f"chamada {i}: não é objeto"

        if set(chamada) != {"name", "arguments"}:
            return False, f"chamada {i}: estrutura inválida"

        nome = chamada["name"]
        argumentos = chamada["arguments"]

        if nome not in TOOLS:
            return False, f"chamada {i}: ferramenta desconhecida"

        if not isinstance(argumentos, dict):
            return False, f"chamada {i}: argumentos inválidos"

        regras = TOOLS[nome]

        if set(argumentos) != set(regras):
            return False, f"chamada {i}: parâmetros ausentes ou extras"

        for chave, limites in regras.items():
            valor = argumentos[chave]
            minimo, maximo = limites

            if type(valor) is not int:
                return False, f"chamada {i}: {chave} não é inteiro"

            if not minimo <= valor <= maximo:
                return False, f"chamada {i}: {chave} fora dos limites"

    return True, None


def executar():
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    casos = dataset["casos"]

    registros = [
        json.loads(linha)
        for linha in RESULTS.read_text(encoding="utf-8").splitlines()
        if linha.strip()
    ]

    if len(casos) != 36 or len(registros) != 36:
        raise SystemExit(
            f"[ERRO] Esperados 36 casos e 36 registros; "
            f"encontrados {len(casos)} e {len(registros)}."
        )

    ids_dataset = [str(c["id"]) for c in casos]
    ids_resultados = [str(r["case_id"]) for r in registros]

    if len(set(ids_dataset)) != len(ids_dataset):
        raise SystemExit("[ERRO] IDs duplicados no dataset.")

    if len(set(ids_resultados)) != len(ids_resultados):
        raise SystemExit("[ERRO] IDs duplicados nos resultados.")

    if set(ids_dataset) != set(ids_resultados):
        raise SystemExit("[ERRO] IDs do dataset e dos resultados diferem.")

    por_id = {str(r["case_id"]): r for r in registros}
    linhas = []

    for caso in casos:
        id_caso = str(caso["id"])
        registro = por_id[id_caso]

        esperado, erro_gabarito = normalizar_esperado(caso)
        predito = registro.get("parsed_calls")

        valido, erro_schema = validar_chamadas(predito)

        avaliavel = erro_gabarito is None
        exato = (
            predito == esperado
            if avaliavel and isinstance(predito, list)
            else False
        )

        # A avaliação semântica de casos ambíguos exige revisão humana.
        revisao = caso["id"] in REVISAR_GABARITO

        linhas.append({
            "id": caso["id"],
            "categoria": caso["categoria"],
            "frase": caso["frase"],
            "esperado": esperado,
            "predito": predito,
            "exact_match_original": exato if avaliavel else None,
            "schema_valido": valido,
            "erro_schema": erro_schema,
            "erro_gabarito": erro_gabarito,
            "revisar_gabarito": revisao,
            "parse_error": registro.get("parse_error"),
            "returncode": registro.get("returncode"),
        })

    por_categoria = defaultdict(list)

    for linha in linhas:
        por_categoria[linha["categoria"]].append(linha)

    print("=" * 75)
    print("PT-05.3 — AVALIAÇÃO EXPLORATÓRIA NEEDLE 2")
    print("=" * 75)

    avaliaveis = [
        x for x in linhas
        if x["exact_match_original"] is not None
    ]
    acertos = sum(x["exact_match_original"] is True for x in avaliaveis)
    validos = sum(x["schema_valido"] for x in linhas)

    print(f"Casos totais: {len(linhas)}")
    print(f"Casos comparáveis ao gabarito original: {len(avaliaveis)}")
    print(f"Exact Match original: {acertos}/{len(avaliaveis)}")

    if avaliaveis:
        print(f"Exact Match (%): {100 * acertos / len(avaliaveis):.2f}")

    print(f"Chamadas válidas pelo schema: {validos}/{len(linhas)}")
    print(f"Casos sinalizados para revisão: "
          f"{sum(x['revisar_gabarito'] for x in linhas)}")

    print("\nRESULTADOS POR CATEGORIA")
    print("-" * 75)

    for categoria, grupo in sorted(por_categoria.items()):
        comparaveis = [
            x for x in grupo
            if x["exact_match_original"] is not None
        ]
        corretos = sum(
            x["exact_match_original"] is True for x in comparaveis
        )
        print(
            f"{categoria:22s} "
            f"acertos={corretos}/{len(comparaveis)} "
            f"total={len(grupo)}"
        )

    print("\nDIVERGÊNCIAS EM RELAÇÃO AO GABARITO ORIGINAL")
    print("-" * 75)

    for x in linhas:
        if x["exact_match_original"] is False:
            print(f"\nCaso {x['id']:02d} — {x['categoria']}")
            print("Frase:", x["frase"])
            print("Esperado:", json.dumps(x["esperado"], ensure_ascii=False))
            print("Predito: ", json.dumps(x["predito"], ensure_ascii=False))
            if x["revisar_gabarito"]:
                print("[REVISAR GABARITO]")

    print("\nCASOS COM GABARITO SINALIZADO")
    print("-" * 75)

    for x in linhas:
        if x["revisar_gabarito"]:
            print(
                f"Caso {x['id']:02d} | "
                f"Exact Match original={x['exact_match_original']}"
            )

    json_path = OUTPUT / "pt05_resultados_detalhados.json"
    csv_path = OUTPUT / "pt05_resultados_detalhados.csv"
    resumo_path = OUTPUT / "pt05_resumo.json"

    json_path.write_text(
        json.dumps(linhas, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        campos = [
            "id", "categoria", "frase",
            "exact_match_original", "schema_valido",
            "erro_schema", "erro_gabarito",
            "revisar_gabarito", "parse_error", "returncode",
            "esperado", "predito",
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

        for linha in linhas:
            registro = {k: linha[k] for k in campos}
            for chave in ("esperado", "predito"):
                registro[chave] = json.dumps(
                    registro[chave], ensure_ascii=False
                )
            writer.writerow(registro)

    resumo = {
        "total": len(linhas),
        "comparaveis": len(avaliaveis),
        "acertos_gabarito_original": acertos,
        "exact_match_percentual": (
            100 * acertos / len(avaliaveis)
            if avaliaveis else None
        ),
        "schema_validos": validos,
        "revisar_gabarito": sorted(REVISAR_GABARITO),
        "divergencias": [
            x["id"] for x in linhas
            if x["exact_match_original"] is False
        ],
        "por_categoria": {
            categoria: {
                "total": len(grupo),
                "comparaveis": sum(
                    x["exact_match_original"] is not None
                    for x in grupo
                ),
                "acertos": sum(
                    x["exact_match_original"] is True
                    for x in grupo
                ),
            }
            for categoria, grupo in por_categoria.items()
        },
    }

    resumo_path.write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nARQUIVOS GERADOS")
    print(json_path.relative_to(ROOT))
    print(csv_path.relative_to(ROOT))
    print(resumo_path.relative_to(ROOT))
    print("\n[OK] Avaliação exploratória concluída.")


if __name__ == "__main__":
    executar()
