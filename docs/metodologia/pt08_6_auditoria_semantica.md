# PT-08.6 — Auditoria do dataset sintético

## Estado

**PENDENTE DE REVISÃO HUMANA.**

## Distribuição

| Categoria | Casos | Abstenções esperadas |
|---|---:|---:|
| diretos | 28 | 0 |
| variacoes_fala | 36 | 0 |
| parametro_implicito | 40 | 40 |
| ambiguos | 40 | 24 |
| fora_escopo | 36 | 36 |

## Diversidade de templates

- Total de comandos: **180**
- Famílias declaradas: **20**
- Assinaturas com números substituídos: **55**

A assinatura é uma aproximação da diversidade superficial, não uma medida de independência semântica.

| Família | Casos |
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

## Revisão individual

As predições do Needle 2 não são exibidas.

### Caso 37

**Categoria:** diretos

**Família:** alertas_direto

**Frase:** Liste todas as colmeias que estão em alerta.

**Gabarito candidato:**

```json
[
  {
    "name": "listar_colmeias_alerta",
    "arguments": {}
  }
]
```

**Justificativa:** Consulta de alertas atuais.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 38

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 42 por 15 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 42,
      "duracao_min": 15
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 39

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 50 por 60 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 50,
      "duracao_min": 60
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 40

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 5 por 25 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 5,
      "duracao_min": 25
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 41

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 22 por 5 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 22,
      "duracao_min": 5
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 42

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 49 por 40 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 49,
      "duracao_min": 40
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 43

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 36 por 25 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 36,
      "duracao_min": 25
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 44

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 49 por 60 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 49,
      "duracao_min": 60
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 45

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 16 por 60 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 16,
      "duracao_min": 60
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 46

**Categoria:** diretos

**Família:** sensores_direto

**Frase:** Mostre peso, temperatura e umidade da colmeia 40.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 40
    }
  }
]
```

**Justificativa:** Consulta de variáveis fornecidas pela ferramenta de status.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 47

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 20 por 5 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 20,
      "duracao_min": 5
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 48

**Categoria:** diretos

**Família:** status_direto

**Frase:** Consulte o status atual da colmeia 4.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 4
    }
  }
]
```

**Justificativa:** Consulta individual com identificador explícito.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 49

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 40 por 5 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 40,
      "duracao_min": 5
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 50

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 24 por 60 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 24,
      "duracao_min": 60
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 51

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 15 por 60 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 15,
      "duracao_min": 60
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 52

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 26 por 60 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 26,
      "duracao_min": 60
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 53

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 34 por 60 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 34,
      "duracao_min": 60
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 54

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 17 por 15 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 17,
      "duracao_min": 15
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 55

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 3 por 40 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 3,
      "duracao_min": 40
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 56

**Categoria:** diretos

**Família:** status_direto

**Frase:** Consulte o status atual da colmeia 6.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 6
    }
  }
]
```

**Justificativa:** Consulta individual com identificador explícito.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 57

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 31 por 15 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 31,
      "duracao_min": 15
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 58

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 42 por 40 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 42,
      "duracao_min": 40
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 59

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 29 por 60 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 29,
      "duracao_min": 60
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 60

**Categoria:** diretos

**Família:** status_direto

**Frase:** Consulte o status atual da colmeia 1.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 1
    }
  }
]
```

**Justificativa:** Consulta individual com identificador explícito.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 61

**Categoria:** diretos

**Família:** status_direto

**Frase:** Consulte o status atual da colmeia 14.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 14
    }
  }
]
```

**Justificativa:** Consulta individual com identificador explícito.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 62

**Categoria:** diretos

**Família:** status_direto

**Frase:** Consulte o status atual da colmeia 22.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 22
    }
  }
]
```

**Justificativa:** Consulta individual com identificador explícito.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 63

**Categoria:** diretos

**Família:** inspecao_direta

**Frase:** Ative o modo inspeção da colmeia 38 por 60 minutos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 38,
      "duracao_min": 60
    }
  }
]
```

**Justificativa:** Identificador e duração válidos explicitamente informados.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 64

**Categoria:** diretos

**Família:** sensores_direto

**Frase:** Mostre peso, temperatura e umidade da colmeia 27.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 27
    }
  }
]
```

**Justificativa:** Consulta de variáveis fornecidas pela ferramenta de status.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 65

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Queria saber a situação da colmeia 14.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 14
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 66

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Me diz aí como anda a colmeia 46.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 46
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 67

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Me diz aí como anda a colmeia 7.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 7
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 68

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Como é que tá a colmeia 29?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 29
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 69

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Me diz aí como anda a colmeia 42.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 42
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 70

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 8 em inspeção por 10 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 8,
      "duracao_min": 10
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 71

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Queria saber a situação da colmeia 33.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 33
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 72

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Como é que tá a colmeia 13?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 13
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 73

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Dá uma conferida nos dados da colmeia 32.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 32
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 74

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 15 em inspeção por 20 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 15,
      "duracao_min": 20
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 75

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 10 em inspeção por 30 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 10,
      "duracao_min": 30
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 76

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 31 em inspeção por 20 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 31,
      "duracao_min": 20
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 77

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Como é que tá a colmeia 2?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 2
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 78

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 7 em inspeção por 10 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 7,
      "duracao_min": 10
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 79

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 16 em inspeção por 20 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 16,
      "duracao_min": 20
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 80

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Me diz aí como anda a colmeia 48.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 48
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 81

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Como é que tá a colmeia 11?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 11
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 82

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Dá uma conferida nos dados da colmeia 10.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 10
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 83

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Como é que tá a colmeia 14?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 14
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 84

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 13 em inspeção por 30 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 13,
      "duracao_min": 30
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 85

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Dá uma conferida nos dados da colmeia 12.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 12
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 86

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 24 em inspeção por 30 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 24,
      "duracao_min": 30
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 87

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 46 em inspeção por 30 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 46,
      "duracao_min": 30
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 88

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 35 em inspeção por 10 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 35,
      "duracao_min": 10
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 89

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 48 em inspeção por 20 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 48,
      "duracao_min": 20
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 90

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Dá uma conferida nos dados da colmeia 18.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 18
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 91

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Queria saber a situação da colmeia 4.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 4
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 92

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 38 em inspeção por 20 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 38,
      "duracao_min": 20
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 93

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Queria saber a situação da colmeia 43.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 43
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 94

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Queria saber a situação da colmeia 50.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 50
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 95

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 16 em inspeção por 30 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 16,
      "duracao_min": 30
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 96

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Como é que tá a colmeia 34?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 34
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 97

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 6 em inspeção por 30 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 6,
      "duracao_min": 30
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 98

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Queria saber a situação da colmeia 2.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 2
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 99

**Categoria:** variacoes_fala

**Família:** status_coloquial

**Frase:** Queria saber a situação da colmeia 36.

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 36
    }
  }
]
```

**Justificativa:** Paráfrase coloquial de consulta individual.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 100

**Categoria:** variacoes_fala

**Família:** inspecao_coloquial

**Frase:** Bota a colmeia 45 em inspeção por 20 minutinhos.

**Gabarito candidato:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 45,
      "duracao_min": 20
    }
  }
]
```

**Justificativa:** Pedido coloquial com duração determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 101

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Coloque a colmeia 26 em modo inspeção.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração obrigatória não informada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 102

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Coloque a colmeia 19 em modo inspeção.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração obrigatória não informada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 103

**Categoria:** parametro_implicito

**Família:** intencao_insuficiente

**Frase:** Preciso verificar a colmeia 11 rapidinho.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Não há ação executável suficientemente determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 104

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 9; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 105

**Categoria:** parametro_implicito

**Família:** identificador_ausente

**Frase:** Como estão os sensores?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Não é possível identificar a colmeia solicitada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 106

**Categoria:** parametro_implicito

**Família:** intencao_insuficiente

**Frase:** Preciso verificar a colmeia 45 rapidinho.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Não há ação executável suficientemente determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 107

**Categoria:** parametro_implicito

**Família:** identificador_ausente

**Frase:** Ative a inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Identificador obrigatório ausente.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 108

**Categoria:** parametro_implicito

**Família:** duracao_indeterminada

**Frase:** Ative inspeção na colmeia 35 por alguns minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração não quantificada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 109

**Categoria:** parametro_implicito

**Família:** duracao_indeterminada

**Frase:** Ative inspeção na colmeia 23 por alguns minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração não quantificada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 110

**Categoria:** parametro_implicito

**Família:** intencao_insuficiente

**Frase:** Preciso verificar a colmeia 22 rapidinho.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Não há ação executável suficientemente determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 111

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 38; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 112

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 49; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 113

**Categoria:** parametro_implicito

**Família:** intencao_insuficiente

**Frase:** Preciso verificar a colmeia 10 rapidinho.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Não há ação executável suficientemente determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 114

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 47; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 115

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 39; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 116

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 11; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 117

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Coloque a colmeia 11 em modo inspeção.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração obrigatória não informada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 118

**Categoria:** parametro_implicito

**Família:** duracao_indeterminada

**Frase:** Ative inspeção na colmeia 8 por alguns minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração não quantificada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 119

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 46; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 120

**Categoria:** parametro_implicito

**Família:** intencao_insuficiente

**Frase:** Preciso verificar a colmeia 35 rapidinho.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Não há ação executável suficientemente determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 121

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Coloque a colmeia 12 em modo inspeção.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração obrigatória não informada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 122

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Coloque a colmeia 34 em modo inspeção.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração obrigatória não informada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 123

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 34; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 124

**Categoria:** parametro_implicito

**Família:** intencao_insuficiente

**Frase:** Preciso verificar a colmeia 26 rapidinho.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Não há ação executável suficientemente determinada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 125

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 25; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 126

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Coloque a colmeia 17 em modo inspeção.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração obrigatória não informada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 127

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 42; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 128

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 20; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 129

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 14; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 130

**Categoria:** parametro_implicito

**Família:** duracao_indeterminada

**Frase:** Ative inspeção na colmeia 10 por alguns minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração não quantificada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 131

**Categoria:** parametro_implicito

**Família:** duracao_indeterminada

**Frase:** Ative inspeção na colmeia 1 por alguns minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração não quantificada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 132

**Categoria:** parametro_implicito

**Família:** duracao_indeterminada

**Frase:** Ative inspeção na colmeia 9 por alguns minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração não quantificada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 133

**Categoria:** parametro_implicito

**Família:** duracao_indeterminada

**Frase:** Ative inspeção na colmeia 40 por alguns minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração não quantificada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 134

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 4; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 135

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 40; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 136

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 27; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 137

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Vou abrir a colmeia 1; pause os alertas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Pedido de ação sem duração.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 138

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Coloque a colmeia 37 em modo inspeção.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração obrigatória não informada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 139

**Categoria:** parametro_implicito

**Família:** duracao_ausente

**Frase:** Coloque a colmeia 24 em modo inspeção.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração obrigatória não informada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 140

**Categoria:** parametro_implicito

**Família:** duracao_indeterminada

**Frase:** Ative inspeção na colmeia 18 por alguns minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração não quantificada.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 141

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 20 e 23 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 142

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 39 e 41 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 143

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 15 e 18?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 15
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 18
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 144

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 39 e 42?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 39
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 42
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 145

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 25 e 28?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 25
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 28
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 146

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 6 e 9?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 6
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 9
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 147

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 11 e 15 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 148

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 27 e 29 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 149

**Categoria:** ambiguos

**Família:** duracao_invalida

**Frase:** Ative inspeção na colmeia 33 por 3 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração abaixo do mínimo de 5 minutos.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 150

**Categoria:** ambiguos

**Família:** duracao_invalida

**Frase:** Ative inspeção na colmeia 2 por 3 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração abaixo do mínimo de 5 minutos.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 151

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 3 e 7 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 152

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 35 e 38?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 35
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 38
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 153

**Categoria:** ambiguos

**Família:** duracao_invalida

**Frase:** Ative inspeção na colmeia 36 por 3 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração abaixo do mínimo de 5 minutos.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 154

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 24 e 27 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 155

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 7 e 10 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 156

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 1 e 4?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 1
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 4
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 157

**Categoria:** ambiguos

**Família:** duracao_invalida

**Frase:** Ative inspeção na colmeia 19 por 90 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração acima do máximo de 60 minutos.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 158

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 14 e 17?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 14
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 17
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 159

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 21 e 24 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 160

**Categoria:** ambiguos

**Família:** identificador_invalido

**Frase:** Mostre o status da colmeia 0.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Identificador fora do intervalo permitido.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 161

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 27 e 30?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 27
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 30
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 162

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 17 e 21?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 17
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 21
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 163

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 17 e 21 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 164

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 39 e 40 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 165

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 34 e 35 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 166

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 17 e 20 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 167

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 5 e 7 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 168

**Categoria:** ambiguos

**Família:** identificador_invalido

**Frase:** Mostre o status da colmeia 52.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Identificador fora do intervalo permitido.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 169

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 44 e 46?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 44
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 46
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 170

**Categoria:** ambiguos

**Família:** duracao_invalida

**Frase:** Ative inspeção na colmeia 3 por 90 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Duração acima do máximo de 60 minutos.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 171

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 26 e 29?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 26
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 29
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 172

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 33 e 35 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 173

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 8 e 11?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 8
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 11
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 174

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 8 e 10?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 8
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 10
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 175

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 17 e 19 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 176

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 1 e 2 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 177

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 39 e 40?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 39
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 40
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 178

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 18 e 20?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 18
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 20
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 179

**Categoria:** ambiguos

**Família:** consulta_multipla

**Frase:** Como estão as colmeias 37 e 40?

**Gabarito candidato:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 37
    }
  },
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 40
    }
  }
]
```

**Justificativa:** Duas consultas individuais identificadas.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 180

**Categoria:** ambiguos

**Família:** acao_multipla_nao_suportada

**Frase:** Coloque as colmeias 1 e 3 em inspeção por 20 minutos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Política conservadora: não executar ação coletiva.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 181

**Categoria:** fora_escopo

**Família:** controle_nao_suportado

**Frase:** Formate a memória do dispositivo.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 182

**Categoria:** fora_escopo

**Família:** administracao

**Frase:** Gere uma nota fiscal.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 183

**Categoria:** fora_escopo

**Família:** controle_nao_suportado

**Frase:** Desligue todos os sensores.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 184

**Categoria:** fora_escopo

**Família:** mercado

**Frase:** Quanto custa uma caixa de madeira?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 185

**Categoria:** fora_escopo

**Família:** administracao

**Frase:** Apague todos os registros antigos.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 186

**Categoria:** fora_escopo

**Família:** administracao

**Frase:** Envie uma mensagem para o apicultor.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 187

**Categoria:** fora_escopo

**Família:** analise_nao_suportada

**Frase:** Diagnostique a doença das abelhas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 188

**Categoria:** fora_escopo

**Família:** previsao_tempo

**Frase:** Vai fazer muito vento esta noite?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 189

**Categoria:** fora_escopo

**Família:** conversa_geral

**Frase:** Bom dia, tudo bem?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 190

**Categoria:** fora_escopo

**Família:** analise_nao_suportada

**Frase:** Preveja a próxima enxameação.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 191

**Categoria:** fora_escopo

**Família:** mercado

**Frase:** Qual a cotação do dólar?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 192

**Categoria:** fora_escopo

**Família:** administracao

**Frase:** Exporte todos os dados em PDF.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 193

**Categoria:** fora_escopo

**Família:** conversa_geral

**Frase:** Explique a história da apicultura.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 194

**Categoria:** fora_escopo

**Família:** mercado

**Frase:** Quanto custa um quilo de cera de abelha?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 195

**Categoria:** fora_escopo

**Família:** mercado

**Frase:** Qual é o valor do própolis no mercado?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 196

**Categoria:** fora_escopo

**Família:** mercado

**Frase:** Onde encontro o mel mais barato?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 197

**Categoria:** fora_escopo

**Família:** controle_nao_suportado

**Frase:** Reinicie o ESP32.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 198

**Categoria:** fora_escopo

**Família:** conversa_geral

**Frase:** Conte uma piada sobre abelhas.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 199

**Categoria:** fora_escopo

**Família:** conversa_geral

**Frase:** Qual é a capital do Brasil?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 200

**Categoria:** fora_escopo

**Família:** administracao

**Frase:** Envie o relatório por e-mail.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 201

**Categoria:** fora_escopo

**Família:** analise_nao_suportada

**Frase:** Compare os dados de todas as colmeias no último ano.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 202

**Categoria:** fora_escopo

**Família:** controle_nao_suportado

**Frase:** Desative permanentemente os alarmes.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 203

**Categoria:** fora_escopo

**Família:** administracao

**Frase:** Cadastre um novo funcionário.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 204

**Categoria:** fora_escopo

**Família:** controle_nao_suportado

**Frase:** Ligue o ventilador do laboratório.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 205

**Categoria:** fora_escopo

**Família:** conversa_geral

**Frase:** Obrigado pela ajuda.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 206

**Categoria:** fora_escopo

**Família:** previsao_tempo

**Frase:** Como fica a previsão do tempo para o próximo mês?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 207

**Categoria:** fora_escopo

**Família:** analise_nao_suportada

**Frase:** Faça um gráfico mensal da produtividade.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 208

**Categoria:** fora_escopo

**Família:** previsao_tempo

**Frase:** Vai chover amanhã?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 209

**Categoria:** fora_escopo

**Família:** analise_nao_suportada

**Frase:** Estime o lucro da próxima safra.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 210

**Categoria:** fora_escopo

**Família:** mercado

**Frase:** Qual é o preço do mel hoje?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 211

**Categoria:** fora_escopo

**Família:** previsao_tempo

**Frase:** Vai ter tempestade no fim de semana?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 212

**Categoria:** fora_escopo

**Família:** controle_nao_suportado

**Frase:** Atualize o firmware pela internet.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 213

**Categoria:** fora_escopo

**Família:** previsao_tempo

**Frase:** Qual será a temperatura da cidade amanhã?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 214

**Categoria:** fora_escopo

**Família:** conversa_geral

**Frase:** Quem inventou o computador?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 215

**Categoria:** fora_escopo

**Família:** previsao_tempo

**Frase:** Qual a previsão de chuva para sábado?

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---

### Caso 216

**Categoria:** fora_escopo

**Família:** analise_nao_suportada

**Frase:** Calcule a produção anual de mel.

**Gabarito candidato:**

```json
[]
```

**Justificativa:** Nenhuma ferramenta disponível atende à solicitação.

**Decisão humana:** PENDENTE

**Observações:**

---
