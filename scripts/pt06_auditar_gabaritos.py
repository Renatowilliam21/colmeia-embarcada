#!/usr/bin/env python3
"""PT-06: auditoria metodológica dos gabaritos e predições."""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset/colmeia-needle2-dataset-teste.json"
RESULTS = (
    ROOT / "results/experiments/needle2_host/"
    "20261022T200512Z/raw_results.jsonl"
)
OUTPUT = ROOT / "results/auditoria"
OUTPUT.mkdir(parents=True, exist_ok=True)

SINALIZADOS = {17, 18, 19, 22, 23, 25, 27}

REQUIRED = {
    "consultar_status_colmeia": {"colmeia_id"},
    "listar_colmeias_alerta": set(),
    "ativar_modo_inspecao": {"colmeia_id", "duracao_min"},
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analisar_gabarito(caso):
    ferramenta = caso.get("ferramenta_esperada")
    argumentos = caso.get("argumentos_esperados")
    problemas = []

    if ferramenta is None:
        if argumentos is not None:
            problemas.append("Ferramenta nula com argumentos não nulos")
        return problemas

    if isinstance(ferramenta, str):
        if ferramenta not in REQUIRED:
            problemas.append("Ferramenta desconhecida")
        elif not isinstance(argumentos, dict):
            problemas.append("Argumentos não representados como objeto")
        else:
            faltantes = REQUIRED[ferramenta] - set(argumentos)
            if faltantes:
                problemas.append(
                    "Parâmetros obrigatórios ausentes: "
                    + ", ".join(sorted(faltantes))
                )
        return problemas

    problemas.append(
        "Gabarito não escalar: requer interpretação específica"
    )
    return problemas


def main():
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    casos = dataset["casos"]

    registros = [
        json.loads(linha)
        for linha in RESULTS.read_text(encoding="utf-8").splitlines()
        if linha.strip()
    ]

    por_id = {str(r["case_id"]): r for r in registros}

    if len(por_id) != len(registros):
        raise SystemExit("[ERRO] IDs duplicados nos resultados.")

    if len(casos) != len(registros):
        raise SystemExit("[ERRO] Quantidade de casos diferente.")

    if {str(c["id"]) for c in casos} != set(por_id):
        raise SystemExit("[ERRO] IDs incompatíveis.")

    linhas = []
    frequencia_duracoes = Counter()
    frequencia_ids = Counter()

    for caso in casos:
        registro = por_id[str(caso["id"])]
        chamadas = registro.get("parsed_calls")

        problemas = analisar_gabarito(caso)

        if caso["id"] in SINALIZADOS:
            problemas.append("Revisão metodológica previamente sinalizada")

        if isinstance(chamadas, list):
            for chamada in chamadas:
                if not isinstance(chamada, dict):
                    continue

                args = chamada.get("arguments", {})

                if not isinstance(args, dict):
                    continue

                if "duracao_min" in args:
                    frequencia_duracoes[str(args["duracao_min"])] += 1

                if "colmeia_id" in args:
                    frequencia_ids[str(args["colmeia_id"])] += 1

        linhas.append({
            "id": caso["id"],
            "categoria": caso["categoria"],
            "frase": caso["frase"],
            "ferramenta_esperada": caso.get("ferramenta_esperada"),
            "argumentos_esperados": caso.get("argumentos_esperados"),
            "predicao": chamadas,
            "problemas": problemas,
            "necessita_revisao": bool(problemas),
        })

    auditoria = {
        "dataset_sha256": sha256(DATASET),
        "resultados_sha256": sha256(RESULTS),
        "total_casos": len(casos),
        "casos_sinalizados": [
            x["id"] for x in linhas if x["necessita_revisao"]
        ],
        "frequencia_duracoes": dict(frequencia_duracoes),
        "frequencia_ids": dict(frequencia_ids),
        "casos": linhas,
    }

    destino = OUTPUT / "pt06_auditoria_gabaritos.json"
    destino.write_text(
        json.dumps(auditoria, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    csv_path = OUTPUT / "pt06_auditoria_gabaritos.csv"

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        campos = [
            "id", "categoria", "frase",
            "necessita_revisao", "problemas",
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()

        for item in linhas:
            writer.writerow({
                "id": item["id"],
                "categoria": item["categoria"],
                "frase": item["frase"],
                "necessita_revisao": item["necessita_revisao"],
                "problemas": "; ".join(item["problemas"]),
            })

    print("=" * 72)
    print("PT-06 — AUDITORIA METODOLÓGICA")
    print("=" * 72)

    print(f"Casos analisados: {len(casos)}")
    print(
        "Casos sinalizados:",
        auditoria["casos_sinalizados"]
    )

    print("\nFREQUÊNCIA DE DURAÇÕES GERADAS")
    for valor, quantidade in frequencia_duracoes.most_common():
        print(f"  {valor} minutos: {quantidade} ocorrência(s)")

    print("\nFREQUÊNCIA DE IDENTIFICADORES GERADOS")
    for valor, quantidade in frequencia_ids.most_common():
        print(f"  Colmeia {valor}: {quantidade} ocorrência(s)")

    print("\nCASOS QUE EXIGEM REVISÃO")
    for item in linhas:
        if item["necessita_revisao"]:
            print(f"\nCaso {item['id']:02d}: {item['frase']}")
            print("Gabarito:", json.dumps({
                "ferramenta": item["ferramenta_esperada"],
                "argumentos": item["argumentos_esperados"],
            }, ensure_ascii=False))
            print("Predição:", json.dumps(
                item["predicao"], ensure_ascii=False
            ))
            print("Problemas:", "; ".join(item["problemas"]))

    print("\nARQUIVOS GERADOS")
    print(destino.relative_to(ROOT))
    print(csv_path.relative_to(ROOT))
    print("\n[OK] Auditoria concluída.")


if __name__ == "__main__":
    main()
