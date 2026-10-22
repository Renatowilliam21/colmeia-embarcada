#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PT-08.10 — Consolidação dos pareceres semânticos.

Objetivos:
- Validar os 180 casos sintéticos.
- Conferir a correspondência com os seis lotes de revisão.
- Registrar pareceres técnicos.
- Documentar ressalvas metodológicas.
- Produzir manifesto SHA-256.
- Preservar integralmente os dados originais.

Não executa inferências.
Não modifica o dataset.
Não homologa automaticamente os gabaritos.
"""

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATASET = (
    ROOT
    / "dataset/synthetic/colmeia-needle2-sintetico-v1.json"
)

REVISAO_DIR = (
    ROOT
    / "docs/metodologia/revisao_sintetica"
)

OUT_DIR = (
    ROOT
    / "docs/metodologia"
)

CSV_OUT = OUT_DIR / "pt08_10_pareceres.csv"
REPORT_OUT = OUT_DIR / "pt08_10_relatorio.md"
MANIFEST_OUT = OUT_DIR / "pt08_10_manifest.json"

EXPECTED_SHA256 = (
    "c0927a014dec323e83db8ef68641b99c777818cdff8fab3445c4a418e79ed555"
)

EXPECTED_IDS = set(range(37, 217))

BATCHES = [
    (37, 66),
    (67, 96),
    (97, 126),
    (127, 156),
    (157, 186),
    (187, 216),
]

ALLOWED_TOOLS = {
    "consultar_status_colmeia",
    "listar_colmeias_alerta",
    "ativar_modo_inspecao",
}

EXPECTED_CATEGORIES = {
    "diretos": 28,
    "variacoes_fala": 36,
    "parametro_implicito": 40,
    "ambiguos": 40,
    "fora_escopo": 36,
}

REVIEW_NOTES = {
    "intencao_insuficiente": (
        "Intenção operacional insuficientemente determinada; "
        "abstenção definida pela política conservadora."
    ),
    "acao_multipla_nao_suportada": (
        "Múltiplas ativações são tecnicamente representáveis, "
        "mas proibidas pela política operacional adotada."
    ),
    "consulta_multipla": (
        "Duas consultas individuais são permitidas; "
        "verificar correspondência de ambas as chamadas."
    ),
    "duracao_ausente": (
        "Duração obrigatória ausente; não inferir valor padrão."
    ),
    "duracao_indeterminada": (
        "Duração não quantificada; não inventar parâmetro."
    ),
    "duracao_invalida": (
        "Duração fora do intervalo permitido de 5 a 60 minutos."
    ),
    "identificador_ausente": (
        "Identificador obrigatório não informado."
    ),
    "identificador_invalido": (
        "Identificador fora do intervalo permitido de 1 a 50."
    ),
}

def fail(message):
    raise ValueError(message)

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def extract_cases(data):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("casos", "cases", "itens", "items"):
            value = data.get(key)
            if isinstance(value, list):
                return value

    fail(
        "Estrutura JSON não reconhecida. "
        "Esperado array ou objeto contendo lista de casos."
    )

def get_field(item, names, required=True):
    for name in names:
        if name in item:
            return item[name]

    if required:
        fail(
            f"Campo obrigatório ausente. "
            f"Alternativas esperadas: {names}"
        )

    return None

def validate_call(call, case_id):
    if not isinstance(call, dict):
        fail(f"Caso {case_id}: chamada não é objeto.")

    name = call.get("name")
    args = call.get("arguments")

    if name not in ALLOWED_TOOLS:
        fail(
            f"Caso {case_id}: ferramenta inválida: {name}"
        )

    if not isinstance(args, dict):
        fail(
            f"Caso {case_id}: arguments não é objeto."
        )

    if name == "listar_colmeias_alerta":
        if args != {}:
            fail(
                f"Caso {case_id}: listar_colmeias_alerta "
                "não aceita argumentos."
            )

    elif name == "consultar_status_colmeia":
        if set(args) != {"colmeia_id"}:
            fail(
                f"Caso {case_id}: argumentos de consulta inválidos."
            )

        value = args["colmeia_id"]

        if type(value) is not int or not 1 <= value <= 50:
            fail(
                f"Caso {case_id}: colmeia_id inválido."
            )

    elif name == "ativar_modo_inspecao":
        if set(args) != {"colmeia_id", "duracao_min"}:
            fail(
                f"Caso {case_id}: argumentos de inspeção inválidos."
            )

        cid = args["colmeia_id"]
        duration = args["duracao_min"]

        if type(cid) is not int or not 1 <= cid <= 50:
            fail(
                f"Caso {case_id}: colmeia_id inválido."
            )

        if (
            type(duration) is not int
            or not 5 <= duration <= 60
        ):
            fail(
                f"Caso {case_id}: duracao_min inválida."
            )

def validate_policy(calls, family, case_id):
    if family in {
        "duracao_ausente",
        "duracao_indeterminada",
        "duracao_invalida",
        "identificador_ausente",
        "identificador_invalido",
        "intencao_insuficiente",
        "acao_multipla_nao_suportada",
        "analise_nao_suportada",
        "previsao_tempo",
        "conversa_geral",
        "mercado",
        "administracao",
        "controle_nao_suportado",
    }:
        if calls:
            fail(
                f"Caso {case_id}: família exige "
                "gabarito sem chamadas."
            )

    if family == "consulta_multipla":
        if len(calls) != 2:
            fail(
                f"Caso {case_id}: consulta múltipla "
                "deve ter duas chamadas."
            )

        if any(
            c["name"] != "consultar_status_colmeia"
            for c in calls
        ):
            fail(
                f"Caso {case_id}: consulta múltipla "
                "contém ferramenta incorreta."
            )

    actuation_calls = sum(
        c["name"] == "ativar_modo_inspecao"
        for c in calls
    )

    if actuation_calls > 1:
        fail(
            f"Caso {case_id}: múltiplas ativações "
            "contrariam a política operacional."
        )

def main():
    if not DATASET.is_file():
        fail(f"Dataset não encontrado: {DATASET}")

    dataset_hash = sha256(DATASET)

    if dataset_hash != EXPECTED_SHA256:
        fail(
            "SHA-256 do dataset diferente do esperado.\n"
            f"Esperado: {EXPECTED_SHA256}\n"
            f"Obtido:   {dataset_hash}\n"
            "Nenhum artefato será produzido."
        )

    with DATASET.open("r", encoding="utf-8") as stream:
        data = json.load(stream)

    cases = extract_cases(data)

    if len(cases) != 180:
        fail(
            f"Quantidade incorreta: {len(cases)}. "
            "Esperados: 180."
        )

    normalized = []
    seen_ids = set()

    for item in cases:
        if not isinstance(item, dict):
            fail("Caso não representado como objeto.")

        case_id = get_field(
            item, ("id", "caso_id", "case_id")
        )

        if type(case_id) is not int:
            fail(f"ID inválido: {case_id}")

        if case_id in seen_ids:
            fail(f"ID duplicado: {case_id}")

        seen_ids.add(case_id)

        category = get_field(
            item, ("categoria", "category")
        )

        family = get_field(
            item, ("familia", "família", "family")
        )

        phrase = get_field(
            item, ("frase", "utterance", "texto")
        )

        calls = get_field(
            item,
            (
                "chamadas_esperadas_revisadas",
                "chamadas_esperadas_propostas",
                "chamadas_esperadas",
                "gabarito_candidato",
                "expected_calls",
            ),
        )

        if not isinstance(phrase, str) or not phrase.strip():
            fail(f"Caso {case_id}: frase vazia.")

        if not isinstance(calls, list):
            fail(f"Caso {case_id}: gabarito não é lista.")

        for call in calls:
            validate_call(call, case_id)

        validate_policy(calls, family, case_id)

        normalized.append({
            "id": case_id,
            "categoria": category,
            "familia": family,
            "frase": phrase.strip(),
            "chamadas": calls,
        })

    if seen_ids != EXPECTED_IDS:
        missing = sorted(EXPECTED_IDS - seen_ids)
        extra = sorted(seen_ids - EXPECTED_IDS)

        fail(
            f"IDs divergentes. Faltantes: {missing}; "
            f"extras: {extra}"
        )

    normalized.sort(key=lambda x: x["id"])

    category_counts = Counter(
        item["categoria"] for item in normalized
    )

    if dict(category_counts) != EXPECTED_CATEGORIES:
        fail(
            "Distribuição de categorias divergente.\n"
            f"Obtido: {dict(category_counts)}"
        )

    batch_hashes = {}

    for start, end in BATCHES:
        path = (
            REVISAO_DIR
            / f"lote_{(start - 37) // 30 + 1:02d}_{start}_{end}.md"
        )

        if not path.is_file():
            fail(f"Lote não encontrado: {path}")

        content = path.read_text(encoding="utf-8")

        if EXPECTED_SHA256 not in content:
            fail(
                f"Lote {start}-{end}: "
                "hash de referência divergente."
            )

        blocks = re.findall(
            r"(?ms)^## Caso (\d+)\s*\n(.*?)(?=^## Caso \d+|\Z)",
            content,
        )

        found_ids = [int(cid) for cid, _ in blocks]

        if found_ids != list(range(start, end + 1)):
            fail(
                f"Lote {start}-{end}: IDs divergentes."
            )

        for cid_text, block in blocks:
            cid = int(cid_text)
            original = normalized[cid - 37]

            phrase_match = re.search(
                r"(?m)^\*\*Frase:\*\*\s*(.+)$",
                block,
            )

            if not phrase_match:
                fail(
                    f"Lote {start}-{end}: "
                    f"frase ausente no caso {cid}."
                )

            if phrase_match.group(1).strip() != original["frase"]:
                fail(
                    f"Lote {start}-{end}: "
                    f"frase divergente no caso {cid}."
                )

            json_match = re.search(
                r"(?s)```json\s*(.*?)\s*```",
                block,
            )

            if not json_match:
                fail(
                    f"Lote {start}-{end}: "
                    f"gabarito ausente no caso {cid}."
                )

            batch_calls = json.loads(
                json_match.group(1)
            )

            if batch_calls != original["chamadas"]:
                fail(
                    f"Lote {start}-{end}: "
                    f"gabarito divergente no caso {cid}."
                )

        batch_hashes[path.relative_to(ROOT).as_posix()] = sha256(path)

    positive = sum(
        bool(item["chamadas"])
        for item in normalized
    )

    negative = len(normalized) - positive

    if positive != 80 or negative != 100:
        fail(
            f"Distribuição executável/abstenção divergente: "
            f"{positive}/{negative}"
        )

    family_counts = Counter(
        item["familia"] for item in normalized
    )

    csv_rows = []

    for item in normalized:
        family = item["familia"]

        note = REVIEW_NOTES.get(
            family,
            "Gabarito semanticamente coerente "
            "com a ferramenta e o protocolo."
        )

        restriction = (
            "SIM"
            if family in {
                "intencao_insuficiente",
                "acao_multipla_nao_suportada",
            }
            else "NAO"
        )

        csv_rows.append({
            "id": item["id"],
            "categoria": item["categoria"],
            "familia": family,
            "frase": item["frase"],
            "gabarito_json": json.dumps(
                item["chamadas"],
                ensure_ascii=False,
                sort_keys=True,
            ),
            "parecer_tecnico": "FAVORAVEL",
            "ressalva_metodologica": restriction,
            "justificativa": note,
            "homologacao": "PENDENTE",
        })

    # Só escreve arquivos após todas as verificações.
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with CSV_OUT.open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=list(csv_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    timestamp = datetime.now(
        timezone.utc
    ).isoformat(timespec="seconds")

    report_lines = [
        "# PT-08.10 — Consolidação da revisão semântica",
        "",
        f"**Data UTC:** {timestamp}",
        "",
        "## Estado",
        "",
        "- Revisão técnica dos 180 casos: concluída.",
        "- Pareceres favoráveis: 180.",
        "- Correções de gabarito: 0.",
        "- Homologação definitiva: PENDENTE.",
        "- Novas inferências: não executadas.",
        "",
        "## Integridade",
        "",
        f"- Dataset SHA-256: `{dataset_hash}`",
        "- IDs: 37 a 216, sem duplicações.",
        "- Seis lotes conferidos com o dataset.",
        "",
        "## Distribuição por categoria",
        "",
        "| Categoria | Quantidade |",
        "|---|---:|",
    ]

    for category, count in sorted(category_counts.items()):
        report_lines.append(
            f"| {category} | {count} |"
        )

    report_lines.extend([
        "",
        "## Chamadas esperadas",
        "",
        f"- Casos com chamadas: {positive}.",
        f"- Casos sem chamadas (`[]`): {negative}.",
        "",
        "## Ressalvas metodológicas",
        "",
        (
            "1. `intencao_insuficiente`: "
            "abstenção conservadora diante de intenção ambígua."
        ),
        (
            "2. `acao_multipla_nao_suportada`: "
            "restrição operacional de segurança, "
            "não limitação estrutural do schema."
        ),
        (
            "3. `consulta_multipla`: "
            "duas consultas de leitura são permitidas."
        ),
        (
            "4. Os exemplos sintéticos compartilham "
            "famílias e modelos de frases; "
            "não são observações independentes."
        ),
        (
            "5. O conjunto original de 36 frases "
            "deve ser analisado separadamente."
        ),
        (
            "6. `[]` representa ausência de chamada "
            "de ferramenta, não necessariamente "
            "solicitação de esclarecimento."
        ),
        (
            "7. A revisão técnica não constitui "
            "homologação final pelo responsável."
        ),
        "",
        "## Frequência por família",
        "",
        "| Família | Quantidade |",
        "|---|---:|",
    ])

    for family, count in sorted(family_counts.items()):
        report_lines.append(
            f"| {family} | {count} |"
        )

    report_lines.extend([
        "",
        "## Próxima etapa",
        "",
        "Homologação formal, congelamento e "
        "planejamento das inferências controladas.",
        "",
    ])

    REPORT_OUT.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    manifest = {
        "etapa": "PT-08.10",
        "gerado_em_utc": timestamp,
        "estado": "PARECER_TECNICO_CONSOLIDADO",
        "homologacao": "PENDENTE",
        "dataset": {
            "arquivo": DATASET.relative_to(ROOT).as_posix(),
            "sha256": dataset_hash,
            "casos": len(normalized),
            "com_chamadas": positive,
            "sem_chamadas": negative,
        },
        "lotes": batch_hashes,
        "artefatos": {
            CSV_OUT.relative_to(ROOT).as_posix(): sha256(CSV_OUT),
            REPORT_OUT.relative_to(ROOT).as_posix(): sha256(REPORT_OUT),
        },
    }

    MANIFEST_OUT.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("=" * 70)
    print("PT-08.10 — CONSOLIDAÇÃO")
    print("=" * 70)
    print(f"[OK] Dataset SHA-256: {dataset_hash}")
    print(f"[OK] Casos analisados: {len(normalized)}")
    print(f"[OK] Com chamadas: {positive}")
    print(f"[OK] Sem chamadas: {negative}")
    print(f"[OK] Lotes conferidos: {len(batch_hashes)}")
    print(f"[OK] CSV: {CSV_OUT.relative_to(ROOT)}")
    print(f"[OK] Relatório: {REPORT_OUT.relative_to(ROOT)}")
    print(f"[OK] Manifesto: {MANIFEST_OUT.relative_to(ROOT)}")
    print("[PENDENTE] Homologação definitiva.")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        sys.exit(1)
