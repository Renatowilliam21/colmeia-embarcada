# PT-08 — Auditoria semântica dos 36 casos

Este documento apresenta os gabaritos e predições para revisão humana.
A geração do documento não equivale à aprovação dos gabaritos.

## Caso 01

**Categoria:** diretos

**Frase:** Qual o status da colmeia 3?

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 3}, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 3}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 3}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 02

**Categoria:** diretos

**Frase:** Colmeia 7: peso e temperatura atual.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 7}, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 7}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 7}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 03

**Categoria:** diretos

**Frase:** Tem alguma colmeia em alerta agora?

**Gabarito original:**

```json
{"argumentos_esperados": {}, "ferramenta_esperada": "listar_colmeias_alerta"}
```

**Gabarito revisado:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 04

**Categoria:** diretos

**Frase:** Liste as colmeias com problema.

**Gabarito original:**

```json
{"argumentos_esperados": {}, "ferramenta_esperada": "listar_colmeias_alerta"}
```

**Gabarito revisado:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 05

**Categoria:** diretos

**Frase:** Ativa o modo inspecao na colmeia 5 por 20 minutos.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 5, "duracao_min": 20}, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 5, "duracao_min": 20}, "name": "ativar_modo_inspecao"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 5, "duracao_min": 20}, "name": "ativar_modo_inspecao"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 06

**Categoria:** diretos

**Frase:** Preciso inspecionar a colmeia 12, pausa os alertas por 30 minutos.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 12, "duracao_min": 30}, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 12, "duracao_min": 30}, "name": "ativar_modo_inspecao"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 12, "duracao_min": 13}, "name": "ativar_modo_inspecao"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 07

**Categoria:** diretos

**Frase:** Como esta a colmeia 1?

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 1}, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 08

**Categoria:** diretos

**Frase:** Mostra os dados da colmeia 9.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 9}, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 9}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 9}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 09

**Categoria:** variacoes_fala

**Frase:** E ai, a colmeia dois ta como?

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 2}, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 2}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 10

**Categoria:** variacoes_fala

**Frase:** Da uma olhada na colmeia quatro pra mim.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 4}, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 4}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 4, "duracao_min": 13}, "name": "ativar_modo_inspecao"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 11

**Categoria:** variacoes_fala

**Frase:** Alguma colmeia pedindo atencao?

**Gabarito original:**

```json
{"argumentos_esperados": {}, "ferramenta_esperada": "listar_colmeias_alerta"}
```

**Gabarito revisado:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 12

**Categoria:** variacoes_fala

**Frase:** Quais colmeias estao fora do normal?

**Gabarito original:**

```json
{"argumentos_esperados": {}, "ferramenta_esperada": "listar_colmeias_alerta"}
```

**Gabarito revisado:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 13

**Categoria:** variacoes_fala

**Frase:** Vou abrir a colmeia 6, desliga o alerta por meia hora.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 6, "duracao_min": 30}, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 6, "duracao_min": 30}, "name": "ativar_modo_inspecao"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 6, "duracao_min": 13}, "name": "ativar_modo_inspecao"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 14

**Categoria:** variacoes_fala

**Frase:** Bota a colmeia 15 em modo inspecao, uns 10 minutinhos.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 15, "duracao_min": 10}, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 15, "duracao_min": 10}, "name": "ativar_modo_inspecao"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 15, "duracao_min": 10}, "name": "ativar_modo_inspecao"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 15

**Categoria:** variacoes_fala

**Frase:** Peso da colmeia numero oito?

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 8}, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 8}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 16

**Categoria:** variacoes_fala

**Frase:** Umidade e temperatura da colmeia 20, por favor.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 20}, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 20}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 20}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 17

**Categoria:** parametro_implicito

**Frase:** Ativa modo inspecao na colmeia 3.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 3}, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 3, "duracao_min": 13}, "name": "ativar_modo_inspecao"}]
```

**Revisado anteriormente:** Sim

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 18

**Categoria:** parametro_implicito

**Frase:** Preciso mexer na colmeia 11 rapidinho.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 11}, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 11}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Sim

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 19

**Categoria:** parametro_implicito

**Frase:** Status.

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Sim

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 20

**Categoria:** parametro_implicito

**Frase:** Colmeias com alerta nos ultimos dias?

**Gabarito original:**

```json
{"argumentos_esperados": {}, "ferramenta_esperada": "listar_colmeias_alerta"}
```

**Gabarito revisado:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 21

**Categoria:** parametro_implicito

**Frase:** Inspecao na colmeia 9 por um quarto de hora.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 9, "duracao_min": 15}, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 9, "duracao_min": 15}, "name": "ativar_modo_inspecao"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 9, "duracao_min": 13}, "name": "ativar_modo_inspecao"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 22

**Categoria:** parametro_implicito

**Frase:** Coloca a colmeia 2 em inspecao ate eu terminar.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 2}, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Revisado anteriormente:** Sim

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 23

**Categoria:** ambiguos

**Frase:** Colmeia 3 e colmeia 4, como estao?

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 3}, "name": "consultar_status_colmeia"}, {"arguments": {"colmeia_id": 4}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 3}, "name": "consultar_status_colmeia"}, {"arguments": {"colmeia_id": 4}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Sim

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 24

**Categoria:** ambiguos

**Frase:** As colmeias da fileira de tras estao bem?

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 25

**Categoria:** ambiguos

**Frase:** Coloca todas as colmeias em modo inspecao.

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {}, "name": "listar_colmeias_alerta"}]
```

**Revisado anteriormente:** Sim

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 26

**Categoria:** ambiguos

**Frase:** A colmeia la do fundo, perto da mangueira, ta como?

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 27

**Categoria:** ambiguos

**Frase:** Inspecao na colmeia 5, tipo, agora.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 5}, "ferramenta_esperada": "ativar_modo_inspecao"}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 5, "duracao_min": 13}, "name": "ativar_modo_inspecao"}]
```

**Revisado anteriormente:** Sim

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 28

**Categoria:** ambiguos

**Frase:** Quero saber da colmeia 3, mas so a temperatura.

**Gabarito original:**

```json
{"argumentos_esperados": {"colmeia_id": 3}, "ferramenta_esperada": "consultar_status_colmeia"}
```

**Gabarito revisado:**

```json
[{"arguments": {"colmeia_id": 3}, "name": "consultar_status_colmeia"}]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 3}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 29

**Categoria:** fora_escopo

**Frase:** Vai chover hoje?

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 30

**Categoria:** fora_escopo

**Frase:** Qual a previsao do tempo pra semana?

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 31

**Categoria:** fora_escopo

**Frase:** Quanto custa um quilo de mel?

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 32

**Categoria:** fora_escopo

**Frase:** Explica como funciona a colmeia.

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1, "duracao_min": 13}, "name": "ativar_modo_inspecao"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 33

**Categoria:** fora_escopo

**Frase:** Oi, tudo bem?

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 34

**Categoria:** fora_escopo

**Frase:** Reinicia o sistema.

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[{"arguments": {"colmeia_id": 1}, "name": "consultar_status_colmeia"}]
```

**Revisado anteriormente:** Não

**Correspondência:** Não

**Revisão humana:** Pendente

**Observações:**

---

## Caso 35

**Categoria:** fora_escopo

**Frase:** Qual o preco do dolar hoje?

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---

## Caso 36

**Categoria:** fora_escopo

**Frase:** Manda um relatorio completo do mes passado.

**Gabarito original:**

```json
{"argumentos_esperados": null, "ferramenta_esperada": null}
```

**Gabarito revisado:**

```json
[]
```

**Predição do Needle 2:**

```json
[]
```

**Revisado anteriormente:** Não

**Correspondência:** Sim

**Revisão humana:** Pendente

**Observações:**

---
