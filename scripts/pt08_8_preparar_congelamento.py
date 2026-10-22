#!/usr/bin/env python3

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATASET = ROOT / "dataset/synthetic/colmeia-needle2-sintetico-v1.json"
SCHEMA = ROOT / "firmware/tools/colmeia.json"

POLICY = ROOT / "docs/metodologia/pt08_8_politica_seguranca.md"
CHECKLIST = ROOT / "dataset/synthetic/pt08_8_checklist_validacao.csv"

EXPECTED_HASH = (
    "c0927a014dec323e83db8ef68641b99c777818cdff8fab3445c4a418e79ed555"
)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if sha(DATASET) != EXPECTED_HASH:
    raise RuntimeError("Hash do dataset diferente do esperado.")

dados = json.loads(DATASET.read_text(encoding="utf-8"))
casos = dados["casos"]

if len(casos) != 180:
    raise RuntimeError("Quantidade de casos inválida.")

ids = [c["id"] for c in casos]

if len(set(ids)) != 180 or set(ids) != set(range(37, 217)):
    raise RuntimeError("IDs ausentes ou duplicados.")

ferramentas = {
    f["name"]: f
    for f in json.loads(SCHEMA.read_text(encoding="utf-8"))
}

for caso in casos:
    chamadas = caso["chamadas_esperadas_revisadas"]

    for chamada in chamadas:
        nome = chamada["name"]
        args = chamada["arguments"]

        if nome not in ferramentas:
            raise RuntimeError(f"Ferramenta desconhecida: {nome}")

        spec = ferramentas[nome]["parameters"]
        props = spec.get("properties", {})
        required = set(spec.get("required", []))

        if not required.issubset(args):
            raise RuntimeError(f"Argumento ausente no caso {caso['id']}")

        if set(args) - set(props):
            raise RuntimeError(f"Argumento desconhecido no caso {caso['id']}")

        for chave, valor in args.items():
            regra = props[chave]

            if regra.get("type") == "integer":
                if type(valor) is not int:
                    raise RuntimeError("Tipo inválido.")

                if not (
                    regra.get("minimum", valor)
                    <= valor
                    <= regra.get("maximum", valor)
                ):
                    raise RuntimeError("Valor fora do intervalo.")

    if caso["familia"] == "acao_multipla_nao_suportada":
        if chamadas != []:
            raise RuntimeError(
                "Ação múltipla incompatível com a política conservadora."
            )

    if caso["familia"] == "consulta_multipla":
        if len(chamadas) != 2:
            raise RuntimeError(
                "Consulta múltipla deve conter duas chamadas."
            )

with CHECKLIST.open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "id",
        "categoria",
        "familia",
        "frase",
        "gabarito_proposto",
        "decisao_humana",
        "justificativa_revisor"
    ])

    for caso in sorted(casos, key=lambda c: c["id"]):
        writer.writerow([
            caso["id"],
            caso["categoria"],
            caso["familia"],
            caso["frase"],
            json.dumps(
                caso["chamadas_esperadas_revisadas"],
                ensure_ascii=False,
                separators=(",", ":")
            ),
            "PENDENTE",
            ""
        ])

contagem = Counter(c["familia"] for c in casos)

texto = [
    "# PT-08.8 — Política de segurança e validação",
    "",
    "## Identificação",
    "",
    f"- Dataset sintético SHA-256: `{sha(DATASET)}`",
    f"- Schema SHA-256: `{sha(SCHEMA)}`",
    "- Quantidade de casos: 180",
    "- Estado: PENDENTE DE REVISÃO HUMANA",
    "",
    "## Política experimental",
    "",
    "1. Consultas de duas colmeias identificadas podem gerar "
    "duas chamadas de leitura.",
    "2. Inspeções individuais exigem identificador e duração válidos.",
    "3. Solicitações de múltiplas ativações de inspeção devem "
    "resultar em nenhuma chamada executável.",
    "4. Parâmetros obrigatórios ausentes exigem abstenção.",
    "5. Identificadores e durações fora dos limites exigem abstenção.",
    "6. Solicitações fora do escopo exigem abstenção.",
    "",
    "## Fundamentação",
    "",
    "A restrição sobre múltiplas ativações é uma política "
    "conservadora de segurança operacional, não uma limitação "
    "estrutural do schema.",
    "",
    "O sistema deverá implementar uma camada de validação "
    "independente do modelo antes de executar ações.",
    "",
    "A lista vazia `[]` representa ausência de chamadas executáveis; "
    "não demonstra que o modelo pediu esclarecimentos.",
    "",
    "## Validação",
    "",
    "A auditoria automática confirma apenas propriedades "
    "estruturais e consistência com regras codificadas.",
    "",
    "A aprovação semântica individual permanece pendente.",
    "",
    "## Distribuição por família",
    "",
    "| Família | Quantidade |",
    "|---|---:|",
]

for familia, total in sorted(contagem.items()):
    texto.append(f"| {familia} | {total} |")

POLICY.write_text("\n".join(texto) + "\n", encoding="utf-8")

print("=" * 68)
print("PT-08.8 — PREPARAÇÃO DO CONGELAMENTO")
print("=" * 68)
print("Casos verificados:", len(casos))
print("Famílias:", len(contagem))
print("Dataset SHA-256:", sha(DATASET))
print("Política:", POLICY.relative_to(ROOT))
print("Checklist:", CHECKLIST.relative_to(ROOT))
print("[OK] Consistência estrutural verificada.")
print("[PENDENTE] Revisão semântica individual.")
