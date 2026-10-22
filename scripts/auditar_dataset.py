
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATASET = ROOT / "dataset/colmeia-needle2-dataset-teste.json"
SCHEMA = ROOT / "firmware/tools/colmeia.json"
OUTPUT = ROOT / "results/auditoria/pt01_dataset.json"


def main():
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    ferramentas = json.loads(SCHEMA.read_text(encoding="utf-8"))

    casos = dataset["casos"]
    schemas = {f["name"]: f for f in ferramentas}

    ids = [caso["id"] for caso in casos]
    problemas = []
    categorias = Counter(caso["categoria"] for caso in casos)

    if len(ids) != len(set(ids)):
        problemas.append({
            "tipo": "ids_duplicados",
            "descricao": "Existem IDs repetidos no dataset."
        })

    for caso in casos:
        identificador = caso["id"]
        ferramenta = caso["ferramenta_esperada"]
        argumentos = caso["argumentos_esperados"]

        if ferramenta is None:
            if argumentos is not None:
                problemas.append({
                    "id": identificador,
                    "tipo": "rejeicao_inconsistente"
                })
            continue

        if ferramenta not in schemas:
            problemas.append({
                "id": identificador,
                "tipo": "ferramenta_inexistente"
            })
            continue

        if argumentos is None:
            problemas.append({
                "id": identificador,
                "tipo": "gabarito_indefinido",
                "descricao": "Não há argumentos para avaliação exata."
            })
            continue

        parametros = schemas[ferramenta]["parameters"]
        obrigatorios = set(parametros.get("required", []))
        presentes = set(argumentos)

        ausentes = sorted(obrigatorios - presentes)

        if ausentes:
            problemas.append({
                "id": identificador,
                "tipo": "parametros_obrigatorios_ausentes",
                "campos": ausentes
            })

        desconhecidos = sorted(
            presentes - set(parametros.get("properties", {}))
        )

        if desconhecidos:
            problemas.append({
                "id": identificador,
                "tipo": "parametros_desconhecidos",
                "campos": desconhecidos
            })

    relatorio = {
        "total_casos": len(casos),
        "ids_unicos": len(set(ids)),
        "categorias": dict(sorted(categorias.items())),
        "ferramentas": list(schemas),
        "total_problemas": len(problemas),
        "problemas": problemas,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    print(f"\nRelatório salvo em: {OUTPUT}")


if __name__ == "__main__":
    main()
