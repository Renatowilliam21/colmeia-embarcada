# PT-08.10 — Consolidação da revisão semântica

**Data UTC:** 2026-10-22T20:51:35+00:00

## Estado

- Revisão técnica dos 180 casos: concluída.
- Pareceres favoráveis: 180.
- Correções de gabarito: 0.
- Homologação definitiva: PENDENTE.
- Novas inferências: não executadas.

## Integridade

- Dataset SHA-256: `c0927a014dec323e83db8ef68641b99c777818cdff8fab3445c4a418e79ed555`
- IDs: 37 a 216, sem duplicações.
- Seis lotes conferidos com o dataset.

## Distribuição por categoria

| Categoria | Quantidade |
|---|---:|
| ambiguos | 40 |
| diretos | 28 |
| fora_escopo | 36 |
| parametro_implicito | 40 |
| variacoes_fala | 36 |

## Chamadas esperadas

- Casos com chamadas: 80.
- Casos sem chamadas (`[]`): 100.

## Ressalvas metodológicas

1. `intencao_insuficiente`: abstenção conservadora diante de intenção ambígua.
2. `acao_multipla_nao_suportada`: restrição operacional de segurança, não limitação estrutural do schema.
3. `consulta_multipla`: duas consultas de leitura são permitidas.
4. Os exemplos sintéticos compartilham famílias e modelos de frases; não são observações independentes.
5. O conjunto original de 36 frases deve ser analisado separadamente.
6. `[]` representa ausência de chamada de ferramenta, não necessariamente solicitação de esclarecimento.
7. A revisão técnica não constitui homologação final pelo responsável.

## Frequência por família

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

## Próxima etapa

Homologação formal, congelamento e planejamento das inferências controladas.
