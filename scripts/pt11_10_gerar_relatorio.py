#!/usr/bin/env python3
"""PT-11.10 — Relatório técnico consolidado."""

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVAL_DIR = ROOT / "results/evaluation/pt11"
OUTPUT_DIR = ROOT / "docs/metodologia/pt11"

SUMMARY_PATH = EVAL_DIR / "pt11_8/pt11_8_resumo.json"
DETAIL_PATH = EVAL_DIR / "pt11_8/pt11_8_detalhado.csv"
STATS_PATH = EVAL_DIR / "pt11_9/pt11_9_resumo_estatistico.json"

REPORT_PATH = OUTPUT_DIR / "pt11_10_relatorio_tecnico.md"
MANIFEST_PATH = OUTPUT_DIR / "pt11_10_manifesto.json"

CONFIGS = [
    "C0_Needle2",
    "C1_Needle2_V1",
    "C2_Needle2_V2",
    "C3_Needle2_V3",
]

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pct(value):
    return f"{value:.2f}".replace(".", ",")

def main():
    summary = json.loads(
        SUMMARY_PATH.read_text(encoding="utf-8")
    )

    stats = json.loads(
        STATS_PATH.read_text(encoding="utf-8")
    )

    with DETAIL_PATH.open(
        encoding="utf-8",
        newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))

    if len(rows) != 1440:
        raise RuntimeError("Quantidade inesperada de avaliações.")

    if summary["cases"] != 120 or summary["inferences"] != 360:
        raise RuntimeError("Metadados experimentais divergentes.")

    if stats["cases"] != 120:
        raise RuntimeError("Quantidade de casos estatísticos divergente.")

    lines = []

    def add(text=""):
        lines.append(text)

    add("# PT-11.10 — Relatório técnico consolidado")
    add()
    add("## 1. Identificação")
    add()
    add("**Projeto:** Colmeia Embarcada")
    add()
    add("**Modelo:** Needle 2")
    add()
    add("**Etapa:** PT-11 — Avaliação em conjunto sintético novo")
    add()
    add("**Natureza:** avaliação retrospectiva de segurança e funcionalidade")
    add()
    add("**Ambiente de inferência:** Linux x86-64; não ESP32")
    add()
    add("**Execução física de ferramentas:** não realizada")
    add()

    add("## 2. Conjunto experimental")
    add()
    add(
        "O experimento utilizou 120 solicitações sintéticas "
        "geradas com assistência de IA, distribuídas em "
        "60 casos positivos e 60 negativos."
    )
    add()
    add(
        "Cada solicitação foi submetida ao modelo em três "
        "repetições, totalizando 360 inferências."
    )
    add()
    add(
        "As mesmas predições foram avaliadas retrospectivamente "
        "nas quatro configurações, produzindo 1.440 avaliações."
    )
    add()
    add(
        "**Atenção:** os gabaritos ainda não foram homologados "
        "por avaliadores humanos independentes."
    )
    add()

    add("## 3. Configurações")
    add()
    add("- **C0:** Needle 2 sem validador.")
    add("- **C1:** Needle 2 com validador V1.")
    add("- **C2:** Needle 2 com validador V2.")
    add("- **C3:** Needle 2 com validador V3.")
    add()
    add(
        "Os validadores foram preservados sem modificações "
        "durante a avaliação PT-11."
    )
    add()

    add("## 4. Resultados experimentais")
    add()
    add(
        "| Configuração | Exact Match | Positivos corretos | "
        "Abstenções corretas | Chamadas indevidas | "
        "Atuações indevidas previstas |"
    )
    add("|---|---:|---:|---:|---:|---:|")

    for config in CONFIGS:
        result = summary["configurations"][config]

        add(
            f"| {config} | "
            f"{pct(result['exact_match_percent'])}% | "
            f"{result['correct_positive_cases']}/"
            f"{result['positive_cases']} | "
            f"{result['correct_abstentions']}/"
            f"{result['negative_cases']} | "
            f"{result['unauthorized_calls_negative']} | "
            f"{result['unauthorized_actuations']} |"
        )

    add()
    add(
        "A C1 apresentou a maior correspondência exata global "
        "(51,67%). Entretanto, a C0 preservou mais comandos "
        "positivos corretos (147/180)."
    )
    add()
    add(
        "As configurações C2 e C3 rejeitaram todas as "
        "solicitações positivas avaliadas."
    )
    add()

    add("## 5. Erros de parsing")
    add()
    add(
        "Foram identificadas seis inferências com erro de parsing, "
        "correspondentes a dois casos distintos, cada um "
        "repetido três vezes."
    )
    add()
    add(
        "Essas saídas permaneceram no denominador das métricas "
        "e não foram classificadas como acertos ou abstenções corretas."
    )
    add()
    add(
        "As falhas ocorreram nos casos PT11-N4-001 e PT11-N4-006."
    )
    add()

    add("## 6. Análise estatística")
    add()
    add(
        "A unidade de reamostragem foi o caso experimental, "
        "preservando conjuntamente suas três repetições."
    )
    add()
    add(
        "Foram realizadas 10.000 reamostragens bootstrap "
        "para estimar intervalos de confiança percentis de 95%."
    )
    add()

    add("| Configuração | Acurácia | IC 95% bootstrap |")
    add("|---|---:|---|")

    for config in CONFIGS:
        result = stats["metrics"][config]
        low, high = result["bootstrap_ci95_percent"]

        add(
            f"| {config} | "
            f"{pct(result['accuracy_percent'])}% | "
            f"[{pct(low)}%; {pct(high)}%] |"
        )

    add()
    add("### 6.1. Comparações pareadas")
    add()
    add("| Comparação | Diferença (p.p.) | IC 95% (p.p.) |")
    add("|---|---:|---|")

    for comparison in stats["comparisons"]:
        a = comparison["configuration_a"]
        b = comparison["configuration_b"]

        diff = comparison["difference_b_minus_a_pp"]
        low = comparison["ci95_lower_pp"]
        high = comparison["ci95_upper_pp"]

        add(
            f"| {a} → {b} | "
            f"{pct(diff)} | "
            f"[{pct(low)}; {pct(high)}] |"
        )

    add()
    add(
        "As comparações pareadas com C0 apresentaram "
        "intervalos de confiança que incluem zero."
    )
    add()
    add(
        "Portanto, não foi identificada evidência conclusiva "
        "de melhoria na correspondência exata global "
        "com base nesses intervalos."
    )
    add()

    friedman = stats["friedman"]

    add("### 6.2. Teste de Friedman")
    add()
    add(
        f"Estatística calculada: "
        f"{friedman['statistic']}."
    )
    add()
    add(
        "O p-valor não foi obtido na execução registrada. "
        "Consequentemente, não se apresenta conclusão "
        "de significância baseada nesse teste."
    )
    add()

    add("## 7. Diagnóstico dos bloqueios")
    add()
    add(
        "A auditoria identificou predominância da regra R12 "
        "nos bloqueios de solicitações positivas."
    )
    add()
    add(
        "| Configuração | Bloqueios positivos pela R12 |"
    )
    add("|---|---:|")

    for config in CONFIGS[1:]:
        selected = [
            row for row in rows
            if row["configuration"] == config
            and row["expected_empty"] == "False"
            and row["authorized"] == "[]"
            and row["rule"] == "R12"
        ]

        add(f"| {config} | {len(selected)} |")

    add()
    add(
        "Na V3, a R12 é utilizada, entre outras condições, "
        "quando a solicitação não corresponde à gramática "
        "associada à ferramenta."
    )
    add()
    add(
        "O resultado é compatível com cobertura linguística "
        "insuficiente, embora o código da regra deva ser "
        "considerado para atribuir causas específicas "
        "a cada bloqueio."
    )
    add()

    add("## 8. Discussão")
    add()
    add(
        "Os resultados evidenciam um compromisso entre "
        "rejeição de chamadas indevidas e preservação "
        "de funcionalidades legítimas."
    )
    add()
    add(
        "Embora C2 e C3 tenham eliminado as atuações "
        "indevidas previstas nos registros avaliados, "
        "também rejeitaram todos os comandos positivos."
    )
    add()
    add(
        "Esse comportamento impede considerar a redução "
        "isolada de chamadas indevidas como evidência "
        "de superioridade operacional."
    )
    add()
    add(
        "A avaliação em um novo conjunto sintético revelou "
        "uma limitação que não era evidente na avaliação "
        "retrospectiva de desenvolvimento PT-10."
    )
    add()

    add("## 9. Limitações")
    add()
    add(
        "- O conjunto foi gerado com assistência de IA."
    )
    add(
        "- Os gabaritos não possuem homologação humana independente."
    )
    add(
        "- As três repetições não são observações independentes."
    )
    add(
        "- A inferência ocorreu em Linux x86-64, não em ESP32."
    )
    add(
        "- Não foram realizadas atuações físicas."
    )
    add(
        "- Os resultados não demonstram segurança em campo."
    )
    add(
        "- Os intervalos bootstrap são condicionados "
        "ao conjunto sintético utilizado."
    )
    add()

    add("## 10. Encaminhamentos")
    add()
    add(
        "Recomenda-se preservar os resultados da PT-11 "
        "e desenvolver posteriormente uma nova versão "
        "do validador com maior cobertura linguística."
    )
    add()
    add(
        "Essa versão deverá ser avaliada em conjunto "
        "não utilizado durante seu desenvolvimento."
    )
    add()
    add(
        "Também são recomendadas avaliação humana "
        "dos gabaritos, testes de robustez linguística "
        "e validação em hardware."
    )
    add()

    add("## 11. Rastreabilidade")
    add()

    inputs = {
        "PT-11.8 — resumo": SUMMARY_PATH,
        "PT-11.8 — detalhado": DETAIL_PATH,
        "PT-11.9 — estatística": STATS_PATH,
    }

    for label, path in inputs.items():
        add(
            f"- **{label}:** `{path.relative_to(ROOT)}` "
            f"— SHA-256 `{sha256(path)}`"
        )

    add()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    REPORT_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    manifest = {
        "stage": "PT-11.10",
        "created_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "report": str(REPORT_PATH.relative_to(ROOT)),
        "report_sha256": sha256(REPORT_PATH),
        "inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in inputs.values()
        },
        "status": "relatorio_tecnico_consolidado",
        "human_validation": False,
        "physical_actuation": False,
    }

    MANIFEST_PATH.write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("PT-11.10 — RELATÓRIO TÉCNICO")
    print("=" * 72)
    print()
    print("Relatório:", REPORT_PATH.relative_to(ROOT))
    print("SHA-256:", sha256(REPORT_PATH))
    print()
    print("Manifesto:", MANIFEST_PATH.relative_to(ROOT))
    print("SHA-256:", sha256(MANIFEST_PATH))
    print()
    print("[OK] Relatório técnico gerado.")


if __name__ == "__main__":
    main()
