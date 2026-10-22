# PT-11.10 — Relatório técnico consolidado

## 1. Identificação

**Projeto:** Colmeia Embarcada

**Modelo:** Needle 2

**Etapa:** PT-11 — Avaliação em conjunto sintético novo

**Natureza:** avaliação retrospectiva de segurança e funcionalidade

**Ambiente de inferência:** Linux x86-64; não ESP32

**Execução física de ferramentas:** não realizada

## 2. Conjunto experimental

O experimento utilizou 120 solicitações sintéticas geradas com assistência de IA, distribuídas em 60 casos positivos e 60 negativos.

Cada solicitação foi submetida ao modelo em três repetições, totalizando 360 inferências.

As mesmas predições foram avaliadas retrospectivamente nas quatro configurações, produzindo 1.440 avaliações.

**Atenção:** os gabaritos ainda não foram homologados por avaliadores humanos independentes.

## 3. Configurações

- **C0:** Needle 2 sem validador.
- **C1:** Needle 2 com validador V1.
- **C2:** Needle 2 com validador V2.
- **C3:** Needle 2 com validador V3.

Os validadores foram preservados sem modificações durante a avaliação PT-11.

## 4. Resultados experimentais

| Configuração | Exact Match | Positivos corretos | Abstenções corretas | Chamadas indevidas | Atuações indevidas previstas |
|---|---:|---:|---:|---:|---:|
| C0_Needle2 | 42,50% | 147/180 | 6/180 | 168 | 72 |
| C1_Needle2_V1 | 51,67% | 15/180 | 171/180 | 3 | 3 |
| C2_Needle2_V2 | 48,33% | 0/180 | 174/180 | 0 | 0 |
| C3_Needle2_V3 | 48,33% | 0/180 | 174/180 | 0 | 0 |

A C1 apresentou a maior correspondência exata global (51,67%). Entretanto, a C0 preservou mais comandos positivos corretos (147/180).

As configurações C2 e C3 rejeitaram todas as solicitações positivas avaliadas.

## 5. Erros de parsing

Foram identificadas seis inferências com erro de parsing, correspondentes a dois casos distintos, cada um repetido três vezes.

Essas saídas permaneceram no denominador das métricas e não foram classificadas como acertos ou abstenções corretas.

As falhas ocorreram nos casos PT11-N4-001 e PT11-N4-006.

## 6. Análise estatística

A unidade de reamostragem foi o caso experimental, preservando conjuntamente suas três repetições.

Foram realizadas 10.000 reamostragens bootstrap para estimar intervalos de confiança percentis de 95%.

| Configuração | Acurácia | IC 95% bootstrap |
|---|---:|---|
| C0_Needle2 | 42,50% | [33,33%; 50,83%] |
| C1_Needle2_V1 | 51,67% | [42,50%; 60,83%] |
| C2_Needle2_V2 | 48,33% | [39,17%; 57,50%] |
| C3_Needle2_V3 | 48,33% | [39,17%; 56,67%] |

### 6.1. Comparações pareadas

| Comparação | Diferença (p.p.) | IC 95% (p.p.) |
|---|---:|---|
| C0_Needle2 → C1_Needle2_V1 | 9,17 | [-6,67; 25,83] |
| C0_Needle2 → C2_Needle2_V2 | 5,83 | [-10,83; 22,50] |
| C0_Needle2 → C3_Needle2_V3 | 5,83 | [-10,83; 21,67] |
| C1_Needle2_V1 → C3_Needle2_V3 | -3,33 | [-7,50; 0,00] |
| C2_Needle2_V2 → C3_Needle2_V3 | 0,00 | [0,00; 0,00] |

As comparações pareadas com C0 apresentaram intervalos de confiança que incluem zero.

Portanto, não foi identificada evidência conclusiva de melhoria na correspondência exata global com base nesses intervalos.

### 6.2. Teste de Friedman

Estatística calculada: 2.345794.

O p-valor não foi obtido na execução registrada. Consequentemente, não se apresenta conclusão de significância baseada nesse teste.

## 7. Diagnóstico dos bloqueios

A auditoria identificou predominância da regra R12 nos bloqueios de solicitações positivas.

| Configuração | Bloqueios positivos pela R12 |
|---|---:|
| C1_Needle2_V1 | 147 |
| C2_Needle2_V2 | 180 |
| C3_Needle2_V3 | 180 |

Na V3, a R12 é utilizada, entre outras condições, quando a solicitação não corresponde à gramática associada à ferramenta.

O resultado é compatível com cobertura linguística insuficiente, embora o código da regra deva ser considerado para atribuir causas específicas a cada bloqueio.

## 8. Discussão

Os resultados evidenciam um compromisso entre rejeição de chamadas indevidas e preservação de funcionalidades legítimas.

Embora C2 e C3 tenham eliminado as atuações indevidas previstas nos registros avaliados, também rejeitaram todos os comandos positivos.

Esse comportamento impede considerar a redução isolada de chamadas indevidas como evidência de superioridade operacional.

A avaliação em um novo conjunto sintético revelou uma limitação que não era evidente na avaliação retrospectiva de desenvolvimento PT-10.

## 9. Limitações

- O conjunto foi gerado com assistência de IA.
- Os gabaritos não possuem homologação humana independente.
- As três repetições não são observações independentes.
- A inferência ocorreu em Linux x86-64, não em ESP32.
- Não foram realizadas atuações físicas.
- Os resultados não demonstram segurança em campo.
- Os intervalos bootstrap são condicionados ao conjunto sintético utilizado.

## 10. Encaminhamentos

Recomenda-se preservar os resultados da PT-11 e desenvolver posteriormente uma nova versão do validador com maior cobertura linguística.

Essa versão deverá ser avaliada em conjunto não utilizado durante seu desenvolvimento.

Também são recomendadas avaliação humana dos gabaritos, testes de robustez linguística e validação em hardware.

## 11. Rastreabilidade

- **PT-11.8 — resumo:** `results/evaluation/pt11/pt11_8/pt11_8_resumo.json` — SHA-256 `2cea16f42868f223f85c2626cf4884ce6d6160152fff301df6b5274282478b98`
- **PT-11.8 — detalhado:** `results/evaluation/pt11/pt11_8/pt11_8_detalhado.csv` — SHA-256 `131ca75eb11cb88deacac470cd86298abb562d79dfe197ec45cbc0e0de79b1bd`
- **PT-11.9 — estatística:** `results/evaluation/pt11/pt11_9/pt11_9_resumo_estatistico.json` — SHA-256 `a2f33688de77b2a6722dc457b12ba44680f6f9fc33b1675caa85a0f9a2181816`

