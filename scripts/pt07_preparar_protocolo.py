#!/usr/bin/env python3
"""PT-07: revisão rastreável do gabarito e avaliação exploratória."""

import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ORIGINAL = ROOT / "dataset/colmeia-needle2-dataset-teste.json"
REVISADO = ROOT / "dataset/colmeia-needle2-gabarito-revisado.json"
SCHEMA = ROOT / "firmware/tools/colmeia.json"
RESULTADOS = (
    ROOT / "results/experiments/needle2_host/"
    "20261022T200512Z/raw_results.jsonl"
)
AVALIADOR = ROOT / "src/evaluation/evaluate_revised.py"
DOCUMENTO = ROOT / "docs/metodologia/revisao_gabaritos.md"
SAIDA = ROOT / "results/evaluation"

SAIDA.mkdir(parents=True, exist_ok=True)

# Decisões metodológicas propostas.
# Cada alteração permanece explicitamente identificada.
REVISOES = {
    17: ("abstencao", "Duração obrigatória ausente."),
    18: ("abstencao", "Intenção e duração insuficientemente definidas."),
    19: ("abstencao", "Identificador da colmeia ausente."),
    22: ("abstencao", "Duração indeterminada."),
    23: ("duas_consultas", "Consulta explícita às colmeias 3 e 4."),
    25: ("abstencao", "Ativação coletiva não suportada pelo schema."),
    27: ("abstencao", "Duração obrigatória ausente."),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chamadas_esperadas(caso):
    ferramenta = caso.get("ferramenta_esperada")
    argumentos = caso.get("argumentos_esperados")

    if ferramenta is None:
        return []

    if not isinstance(ferramenta, str):
        return None

    if not isinstance(argumentos, dict):
        return None

    return [{
        "name": ferramenta,
        "arguments": argumentos,
    }]


def gerar_revisado():
    original = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    casos = original["casos"]

    if len(casos) != 36:
        raise RuntimeError("Dataset não contém 36 casos.")

    ids = [c["id"] for c in casos]

    if len(set(ids)) != 36:
        raise RuntimeError("IDs duplicados.")

    if not set(REVISOES).issubset(set(ids)):
        raise RuntimeError("ID de revisão inexistente.")

    revisados = []

    for caso in casos:
        novo = dict(caso)
        id_caso = caso["id"]

        if id_caso in REVISOES:
            tipo, justificativa = REVISOES[id_caso]

            if tipo == "abstencao":
                esperado = []
            else:
                esperado = [
                    {
                        "name": "consultar_status_colmeia",
                        "arguments": {"colmeia_id": 3},
                    },
                    {
                        "name": "consultar_status_colmeia",
                        "arguments": {"colmeia_id": 4},
                    },
                ]

            novo["revisao_metodologica"] = {
                "revisado": True,
                "justificativa": justificativa,
                "ferramenta_original": caso.get("ferramenta_esperada"),
                "argumentos_originais": caso.get("argumentos_esperados"),
            }
        else:
            esperado = chamadas_esperadas(caso)
            novo["revisao_metodologica"] = {
                "revisado": False,
                "justificativa": None,
            }

        if esperado is None:
            raise RuntimeError(
                f"Caso {id_caso}: gabarito ainda não interpretável."
            )

        novo["chamadas_esperadas_revisadas"] = esperado
        revisados.append(novo)

    novo_dataset = {
        "_protocolo": {
            "versao": "PT-07-proposta-1",
            "status": "proposta_exploratoria",
            "dataset_original_sha256": sha256(ORIGINAL),
            "schema_sha256": sha256(SCHEMA),
            "criterio_abstencao": (
                "Lista vazia significa ausência de chamadas executáveis; "
                "não demonstra capacidade de esclarecimento conversacional."
            ),
            "observacao": (
                "Revisão metodológica documentada; "
                "dataset original não modificado."
            ),
        },
        "casos": revisados,
    }

    REVISADO.write_text(
        json.dumps(novo_dataset, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return revisados


def gerar_documento():
    linhas = [
        "# PT-07 — Revisão metodológica dos gabaritos",
        "",
        "## Objetivo",
        "",
        "Preservar o dataset original e documentar uma proposta "
        "de gabarito revisado para avaliação de chamadas de ferramentas.",
        "",
        "## Critérios",
        "",
        "- Comandos completos exigem correspondência exata.",
        "- Parâmetros obrigatórios ausentes exigem abstenção (`[]`).",
        "- Referências ambíguas sem identificação suficiente exigem abstenção.",
        "- Solicitações fora do escopo exigem abstenção.",
        "- Consultas múltiplas explícitas podem gerar múltiplas chamadas.",
        "- Ações coletivas não previstas no schema não devem ser executadas.",
        "",
        "A lista vazia representa somente ausência de chamada executável.",
        "Ela não comprova que o modelo solicitou esclarecimentos.",
        "",
        "## Alterações propostas",
        "",
        "| Caso | Decisão | Justificativa |",
        "|---|---|---|",
    ]

    for id_caso, (tipo, justificativa) in REVISOES.items():
        decisao = "Duas consultas" if tipo == "duas_consultas" else "Abstenção"
        linhas.append(
            f"| {id_caso} | {decisao} | {justificativa} |"
        )

    linhas.extend([
        "",
        "## Limitações",
        "",
        "O protocolo revisado constitui uma decisão metodológica "
        "posterior à primeira execução exploratória. "
        "Seus resultados não substituem a avaliação original.",
        "",
        "A avaliação de segurança operacional exige uma camada "
        "independente de validação antes de executar ferramentas.",
        "",
        "Os demais 29 gabaritos foram preservados nesta proposta; "
        "isso não equivale a uma auditoria semântica independente "
        "de todos os comandos.",
        "",
        "## Integridade",
        "",
        f"- SHA-256 original: `{sha256(ORIGINAL)}`",
        f"- SHA-256 schema: `{sha256(SCHEMA)}`",
        f"- SHA-256 revisado: `{sha256(REVISADO)}`",
        f"- SHA-256 resultados: `{sha256(RESULTADOS)}`",
        "",
    ])

    DOCUMENTO.write_text(
        "\n".join(linhas),
        encoding="utf-8",
    )


def gerar_avaliador():
    codigo = r'''#!/usr/bin/env python3
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
'''
    AVALIADOR.write_text(codigo, encoding="utf-8")


def main():
    for arquivo in [ORIGINAL, SCHEMA, RESULTADOS]:
        if not arquivo.is_file():
            raise SystemExit(f"[ERRO] Arquivo ausente: {arquivo}")

    gerar_revisado()
    gerar_documento()
    gerar_avaliador()

    print("=" * 72)
    print("PT-07 — PREPARAÇÃO DO PROTOCOLO REVISADO")
    print("=" * 72)
    print("[OK] Dataset original preservado.")
    print("[OK] Dataset revisado criado.")
    print("[OK] Justificativas metodológicas documentadas.")
    print("[OK] Avaliador independente criado.")
    print(f"[OK] SHA-256 original: {sha256(ORIGINAL)}")
    print(f"[OK] SHA-256 revisado: {sha256(REVISADO)}")
    print("\nArquivos:")
    print(REVISADO.relative_to(ROOT))
    print(DOCUMENTO.relative_to(ROOT))
    print(AVALIADOR.relative_to(ROOT))


if __name__ == "__main__":
    main()
