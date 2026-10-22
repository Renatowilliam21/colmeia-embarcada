#!/usr/bin/env python3
"""Avaliação do gabarito original e do revisado, separadamente."""

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ORIGINAL = ROOT / "dataset/colmeia-needle2-dataset-teste.json"
REVISADO = ROOT / "dataset/colmeia-needle2-gabarito-revisado.json"
RESULTADOS = (
    ROOT / "results/experiments/needle2_host/"
    "20261022T200512Z/raw_results.jsonl"
)
SAIDA = ROOT / "results/evaluation"


def original_esperado(caso):
    ferramenta = caso.get("ferramenta_esperada")
    argumentos = caso.get("argumentos_esperados")

    if ferramenta is None:
        return [] if argumentos is None else None

    if not isinstance(ferramenta, str):
        return None

    if not isinstance(argumentos, dict):
        return None

    return [{"name": ferramenta, "arguments": argumentos}]


def normalizar_chamadas(chamadas):
    if not isinstance(chamadas, list):
        return None

    if not all(isinstance(x, dict) for x in chamadas):
        return None

    return sorted(
        [json.dumps(x, sort_keys=True, ensure_ascii=False) for x in chamadas]
    )


def comparar(predito, esperado):
    a = normalizar_chamadas(predito)
    b = normalizar_chamadas(esperado)

    if a is None or b is None:
        return None

    return a == b


def main():
    original = json.loads(ORIGINAL.read_text(encoding="utf-8"))["casos"]
    revisado = json.loads(REVISADO.read_text(encoding="utf-8"))["casos"]

    registros = [
        json.loads(linha)
        for linha in RESULTADOS.read_text(encoding="utf-8").splitlines()
        if linha.strip()
    ]

    if len(original) != 36 or len(revisado) != 36 or len(registros) != 36:
        raise SystemExit("[ERRO] Quantidade inesperada de casos.")

    def indexar(itens, campo):
        ids = [str(x[campo]) for x in itens]
        if len(set(ids)) != len(ids):
            raise SystemExit("[ERRO] IDs duplicados.")
        return {str(x[campo]): x for x in itens}

    orig = indexar(original, "id")
    rev = indexar(revisado, "id")
    pred = indexar(registros, "case_id")

    if not (set(orig) == set(rev) == set(pred)):
        raise SystemExit("[ERRO] IDs incompatíveis.")

    linhas = []
    categorias = defaultdict(list)

    for id_caso in sorted(orig, key=int):
        caso = orig[id_caso]
        novo = rev[id_caso]
        resposta = pred[id_caso].get("parsed_calls")

        exato_original = comparar(
            resposta, original_esperado(caso)
        )
        exato_revisado = comparar(
            resposta, novo["chamadas_esperadas_revisadas"]
        )

        linha = {
            "id": int(id_caso),
            "categoria": caso["categoria"],
            "exact_match_original": exato_original,
            "exact_match_revisado": exato_revisado,
            "gabarito_revisado": novo[
                "revisao_metodologica"
            ]["revisado"],
        }

        linhas.append(linha)
        categorias[caso["categoria"]].append(linha)

    print("=" * 72)
    print("PT-07 — AVALIAÇÃO ORIGINAL × REVISADA")
    print("=" * 72)

    for chave, titulo in [
        ("exact_match_original", "Original"),
        ("exact_match_revisado", "Revisado"),
    ]:
        avaliaveis = [x for x in linhas if x[chave] is not None]
        acertos = sum(x[chave] is True for x in avaliaveis)

        print(
            f"{titulo}: {acertos}/{len(avaliaveis)} "
            f"({100 * acertos / len(avaliaveis):.2f}%)"
        )

    print("\nPOR CATEGORIA")
    print("-" * 72)

    for categoria, grupo in sorted(categorias.items()):
        total = len(grupo)
        acertos = sum(
            x["exact_match_revisado"] is True for x in grupo
        )
        print(f"{categoria:22s}: {acertos}/{total}")

    print("\nALTERAÇÕES DE CLASSIFICAÇÃO")
    print("-" * 72)

    for x in linhas:
        if x["gabarito_revisado"]:
            print(
                f"Caso {x['id']:02d}: "
                f"original={x['exact_match_original']} "
                f"revisado={x['exact_match_revisado']}"
            )

    SAIDA.mkdir(parents=True, exist_ok=True)

    destino_json = SAIDA / "pt07_comparacao_original_revisado.json"
    destino_csv = SAIDA / "pt07_comparacao_original_revisado.csv"

    destino_json.write_text(
        json.dumps(linhas, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with destino_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(linhas[0]))
        writer.writeheader()
        writer.writerows(linhas)

    print("\nARQUIVOS GERADOS")
    print(destino_json.relative_to(ROOT))
    print(destino_csv.relative_to(ROOT))
    print("\n[OK] Avaliação PT-07 concluída.")


if __name__ == "__main__":
    main()
