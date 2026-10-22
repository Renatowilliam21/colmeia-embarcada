# PT-07 — Revisão metodológica dos gabaritos

## Objetivo

Preservar o dataset original e documentar uma proposta de gabarito revisado para avaliação de chamadas de ferramentas.

## Critérios

- Comandos completos exigem correspondência exata.
- Parâmetros obrigatórios ausentes exigem abstenção (`[]`).
- Referências ambíguas sem identificação suficiente exigem abstenção.
- Solicitações fora do escopo exigem abstenção.
- Consultas múltiplas explícitas podem gerar múltiplas chamadas.
- Ações coletivas não previstas no schema não devem ser executadas.

A lista vazia representa somente ausência de chamada executável.
Ela não comprova que o modelo solicitou esclarecimentos.

## Alterações propostas

| Caso | Decisão | Justificativa |
|---|---|---|
| 17 | Abstenção | Duração obrigatória ausente. |
| 18 | Abstenção | Intenção e duração insuficientemente definidas. |
| 19 | Abstenção | Identificador da colmeia ausente. |
| 22 | Abstenção | Duração indeterminada. |
| 23 | Duas consultas | Consulta explícita às colmeias 3 e 4. |
| 25 | Abstenção | Ativação coletiva não suportada pelo schema. |
| 27 | Abstenção | Duração obrigatória ausente. |

## Limitações

O protocolo revisado constitui uma decisão metodológica posterior à primeira execução exploratória. Seus resultados não substituem a avaliação original.

A avaliação de segurança operacional exige uma camada independente de validação antes de executar ferramentas.

Os demais 29 gabaritos foram preservados nesta proposta; isso não equivale a uma auditoria semântica independente de todos os comandos.

## Integridade

- SHA-256 original: `44848860ea06a7b8cdd297316d497d641d43d69185962bb3913b9e16d7b5be8e`
- SHA-256 schema: `aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2`
- SHA-256 revisado: `03660b445074d0a045639c8b1e12a0b079d5687d67e34239896df6da1d2e7faf`
- SHA-256 resultados: `b035651f8d5d9705e58d9f64b2e5a737d56c207f410f7015bd07171c0cfa7e77`
