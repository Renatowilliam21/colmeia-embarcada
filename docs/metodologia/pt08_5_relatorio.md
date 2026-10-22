# PT-08.5 — Relatório de geração sintética

## Proveniência

- Método: templates controlados e seleção pseudoaleatória.
- Semente: `20261022`
- SHA-256 original: `44848860ea06a7b8cdd297316d497d641d43d69185962bb3913b9e16d7b5be8e`
- SHA-256 protocolo de 36 casos: `59b267f878efaa80e414f02065e33f018661a961baeaacf033ec893f30b291c5`
- SHA-256 schema: `aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2`
- SHA-256 dataset sintético: `c0927a014dec323e83db8ef68641b99c777818cdff8fab3445c4a418e79ed555`
- Estado: candidato, pendente de revisão humana.

## Distribuição

| Categoria | Quantidade |
|---|---:|
| diretos | 28 |
| variacoes_fala | 36 |
| parametro_implicito | 40 |
| ambiguos | 40 |
| fora_escopo | 36 |

## Famílias de templates

| Família | Quantidade |
|---|---:|
| acao_multipla_nao_suportada | 17 |
| administracao | 6 |
| alertas_direto | 1 |
| analise_nao_suportada | 6 |
| consulta_multipla | 16 |
| controle_nao_suportado | 6 |
| conversa_geral | 6 |
| duracao_ausente | 24 |
| duracao_indeterminada | 8 |
| duracao_invalida | 5 |
| identificador_ausente | 2 |
| identificador_invalido | 2 |
| inspecao_coloquial | 15 |
| inspecao_direta | 20 |
| intencao_insuficiente | 6 |
| mercado | 6 |
| previsao_tempo | 6 |
| sensores_direto | 2 |
| status_coloquial | 21 |
| status_direto | 5 |

## Limitações e decisões pendentes

- Os comandos são sintéticos, não coletados de apicultores.
- Templates semelhantes não representam observações independentes.
- A política conservadora de abstenção em ações múltiplas deve ser confirmada antes do congelamento.
- `[]` significa nenhuma chamada executável; não comprova que o modelo solicitou esclarecimento.
- A auditoria automática verifica estrutura, limites, distribuição e duplicatas, não correção semântica completa.
- Os 36 comandos anteriores já foram usados em estudo exploratório; não constituem teste independente.
- Não executar inferências definitivas antes da revisão e do congelamento do conjunto sintético.
