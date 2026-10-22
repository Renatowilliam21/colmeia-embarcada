#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PT-08.11 — Homologação e congelamento experimental.

Preserva os arquivos originais.
Não executa inferências.
Não altera .gitignore.
Não modifica o dataset sintético de origem.
"""

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "dataset/synthetic/colmeia-needle2-sintetico-v1.json"
PARECERES = ROOT / "docs/metodologia/pt08_10_pareceres.csv"
MANIFEST_10 = ROOT / "docs/metodologia/pt08_10_manifest.json"
SCHEMA = ROOT / "firmware/tools/colmeia.json"

OUT = ROOT / "dataset/frozen"
DOCS = ROOT / "docs/metodologia"

FROZEN = OUT / "colmeia-needle2-sintetico-v1-homologado.json"
MANIFEST = OUT / "pt08_11_manifest.json"
REPORT = DOCS / "pt08_11_congelamento.md"

EXPECTED_SOURCE_SHA = (
    "c0927a014dec323e83db8ef68641b99c777818cdff8fab3445c4a418e79ed555"
)

EXPECTED_SCHEMA_SHA = (
    "aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2"
)

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def sha256(path):
    return sha256_bytes(path.read_bytes())

def require(condition, message):
    if not condition:
        raise ValueError(message)

def relative(path):
    return path.relative_to(ROOT).as_posix()

def write_once(path, content):
    """
    Nunca sobrescreve um artefato congelado divergente.
    """
    if path.exists():
        require(
            path.read_bytes() == content,
            f"Arquivo existente divergente: {path}"
        )
        print(f"[OK] Artefato existente preservado: {relative(path)}")
        return

    with path.open("xb") as stream:
        stream.write(content)

    print(f"[OK] Artefato criado: {relative(path)}")

def main():
    print("=" * 70)
    print("PT-08.11 — HOMOLOGAÇÃO E CONGELAMENTO")
    print("=" * 70)

    for path in (SOURCE, PARECERES, MANIFEST_10, SCHEMA):
        require(path.is_file(), f"Arquivo não encontrado: {path}")

    source_sha = sha256(SOURCE)
    schema_sha = sha256(SCHEMA)

    require(
        source_sha == EXPECTED_SOURCE_SHA,
        "Hash do dataset sintético de origem divergente."
    )

    require(
        schema_sha == EXPECTED_SCHEMA_SHA,
        "Hash do schema das ferramentas divergente."
    )

    manifest_10 = json.loads(
        MANIFEST_10.read_text(encoding="utf-8")
    )

    require(
        manifest_10["dataset"]["sha256"] == source_sha,
        "Manifesto PT-08.10 não corresponde ao dataset."
    )

    require(
        manifest_10.get("homologacao") == "PENDENTE",
        "Estado inesperado no manifesto PT-08.10."
    )

    artefatos_10 = manifest_10.get("artefatos", {})

    require(
        artefatos_10.get(relative(PARECERES)) == sha256(PARECERES),
        "CSV de pareceres difere do manifesto PT-08.10."
    )

    for filename, expected_hash in artefatos_10.items():
        path = ROOT / filename

        require(
            path.is_file() and sha256(path) == expected_hash,
            f"Artefato PT-08.10 divergente: {filename}"
        )

    data = json.loads(SOURCE.read_text(encoding="utf-8"))

    if isinstance(data, list):
        cases = data
    elif isinstance(data, dict):
        cases = data.get("casos")
        require(
            isinstance(cases, list),
            "Estrutura do dataset não reconhecida."
        )
    else:
        raise ValueError("Estrutura JSON inválida.")

    require(len(cases) == 180, "Quantidade de casos inválida.")

    by_id = {}

    for case in cases:
        cid = case["id"]

        require(
            type(cid) is int and cid not in by_id,
            f"ID inválido ou duplicado: {cid}"
        )

        by_id[cid] = case

    require(
        set(by_id) == set(range(37, 217)),
        "Intervalo de IDs divergente."
    )

    with PARECERES.open(
        encoding="utf-8",
        newline=""
    ) as stream:
        pareceres = list(csv.DictReader(stream))

    require(
        len(pareceres) == 180,
        "Quantidade de pareceres inválida."
    )

    pareceres_por_id = {}

    for row in pareceres:
        cid = int(row["id"])

        require(
            cid not in pareceres_por_id,
            f"Parecer duplicado: {cid}"
        )

        pareceres_por_id[cid] = row

    require(
        set(pareceres_por_id) == set(by_id),
        "IDs dos pareceres não correspondem ao dataset."
    )

    frozen_cases = []

    for cid in sorted(by_id):
        original = by_id[cid]
        parecer = pareceres_por_id[cid]

        require(
            parecer["parecer_tecnico"] == "FAVORAVEL",
            f"Caso {cid} sem parecer favorável."
        )

        require(
            parecer["homologacao"] == "PENDENTE",
            f"Caso {cid} com estado inesperado."
        )

        require(
            original["frase"] == parecer["frase"],
            f"Frase divergente no caso {cid}."
        )

        require(
            original["categoria"] == parecer["categoria"],
            f"Categoria divergente no caso {cid}."
        )

        require(
            original["familia"] == parecer["familia"],
            f"Família divergente no caso {cid}."
        )

        calls = original["chamadas_esperadas_revisadas"]

        require(
            calls == json.loads(parecer["gabarito_json"]),
            f"Gabarito divergente no caso {cid}."
        )

        frozen_case = dict(original)
        frozen_case["status_validacao"] = "homologado"
        frozen_cases.append(frozen_case)

    positive = sum(
        bool(c["chamadas_esperadas_revisadas"])
        for c in frozen_cases
    )

    negative = len(frozen_cases) - positive

    require(
        (positive, negative) == (80, 100),
        "Distribuição de chamadas divergente."
    )

    categories = Counter(
        c["categoria"] for c in frozen_cases
    )

    families = Counter(
        c["familia"] for c in frozen_cases
    )

    frozen_data = {
        "identificacao": "colmeia-needle2-sintetico-v1",
        "versao": "1.0.0",
        "estado": "homologado_congelado",
        "total_casos": 180,
        "politica": {
            "modo": "conservador",
            "consultas_multiplas": "permitidas",
            "ativacoes_multiplas": "proibidas",
            "parametros_ausentes": "nao_inferir",
            "parametros_invalidos": "nao_corrigir",
            "fora_escopo": "nenhuma_chamada"
        },
        "casos": frozen_cases
    }

    frozen_bytes = (
        json.dumps(
            frozen_data,
            ensure_ascii=False,
            indent=2
        ) + "\n"
    ).encode("utf-8")

    frozen_sha = sha256_bytes(frozen_bytes)

    manifest = {
        "etapa": "PT-08.11",
        "estado": "HOMOLOGADO_CONGELADO",
        "versao": "1.0.0",
        "homologacao": {
            "decisao": "APROVADA",
            "responsavel": "coordenador_do_experimento",
            "fundamento": (
                "Confirmação expressa após revisão semântica "
                "dos seis lotes e auditoria PT-08.10."
            )
        },
        "origem": {
            "arquivo": relative(SOURCE),
            "sha256": source_sha
        },
        "schema": {
            "arquivo": relative(SCHEMA),
            "sha256": schema_sha
        },
        "revisao": {
            "arquivo": relative(PARECERES),
            "sha256": sha256(PARECERES),
            "manifesto_pt08_10_sha256": sha256(MANIFEST_10)
        },
        "dataset_congelado": {
            "arquivo": relative(FROZEN),
            "sha256": frozen_sha,
            "casos": 180,
            "com_chamadas": positive,
            "sem_chamadas": negative
        },
        "categorias": dict(sorted(categories.items())),
        "familias": dict(sorted(families.items())),
        "restricoes_metodologicas": [
            "Dataset sintético gerado por templates.",
            "Frases de uma mesma família não são independentes.",
            "Os 36 casos originais pertencem ao conjunto exploratório.",
            "A política conservadora integra o gabarito.",
            "Abstenção significa ausência de chamada de ferramenta.",
            "Resultados devem ser apresentados por categoria e família."
        ]
    }

    manifest_bytes = (
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2
        ) + "\n"
    ).encode("utf-8")

    report = f"""# PT-08.11 — Homologação e congelamento experimental

## Decisão

Os 180 gabaritos sintéticos foram homologados pelo
responsável pelo experimento, após a revisão semântica
dos seis lotes e a consolidação PT-08.10.

**Estado:** HOMOLOGADO_CONGELADO

**Versão:** 1.0.0

## Integridade

- Dataset original: `{relative(SOURCE)}`
- SHA-256 original: `{source_sha}`
- Dataset congelado: `{relative(FROZEN)}`
- SHA-256 congelado: `{frozen_sha}`
- Schema SHA-256: `{schema_sha}`

## Composição

- Total: 180 casos
- Com chamadas esperadas: {positive}
- Sem chamadas esperadas: {negative}

## Política operacional

- Consultas múltiplas de leitura são permitidas.
- Ativações múltiplas são proibidas pelo protocolo.
- Parâmetros obrigatórios ausentes não são inferidos.
- Parâmetros inválidos não são corrigidos automaticamente.
- Pedidos fora do escopo não produzem chamadas.

## Limitações

Os casos foram gerados sinteticamente a partir de
famílias de templates e não constituem observações
linguísticas independentes.

Os 36 casos originais já utilizados na exploração
devem ser analisados separadamente.

A avaliação de seleção de ferramentas não equivale
à avaliação da qualidade de respostas em linguagem
natural.

## Regra de preservação

Qualquer alteração futura dos casos ou gabaritos
deverá produzir uma nova versão, sem sobrescrever
o conjunto congelado.

## Próxima etapa

Executar o protocolo experimental com os modelos
selecionados e registrar predições, latência,
validade estrutural, correção semântica e violações
da política operacional.
"""

    report_bytes = report.encode("utf-8")

    OUT.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    write_once(FROZEN, frozen_bytes)
    write_once(MANIFEST, manifest_bytes)
    write_once(REPORT, report_bytes)

    require(
        sha256(FROZEN) == frozen_sha,
        "Falha na verificação do dataset congelado."
    )

    require(
        sha256(SOURCE) == source_sha,
        "Dataset original foi alterado."
    )

    print()
    print("[OK] Homologação registrada.")
    print("[OK] Dataset congelado: 180 casos.")
    print(f"[OK] Com chamadas: {positive}")
    print(f"[OK] Sem chamadas: {negative}")
    print(f"[OK] SHA-256 congelado: {frozen_sha}")
    print("[OK] Dataset original preservado.")
    print("[OK] Manifesto e relatório gerados.")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        json.JSONDecodeError
    ) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        sys.exit(1)
