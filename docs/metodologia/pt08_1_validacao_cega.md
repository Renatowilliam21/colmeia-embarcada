# PT-08.1 — Validação semântica dos gabaritos

## Procedimento

Revisar cada comando utilizando apenas a frase,
a categoria e o gabarito proposto.

As predições do Needle 2 não são apresentadas.

**Estado:** PENDENTE DE VALIDAÇÃO HUMANA.

## Critérios

- Comandos completos devem gerar chamadas exatas.
- Parâmetros obrigatórios ausentes exigem abstenção.
- Solicitações ambíguas devem ser rejeitadas quando
  não for possível identificar a ação ou a colmeia.
- Comandos fora do escopo exigem abstenção.
- Consultas múltiplas podem gerar múltiplas chamadas.
- Ações coletivas não suportadas exigem abstenção.

## Caso 01

**Categoria:** diretos

**Frase:** Qual o status da colmeia 3?

**Gabarito proposto:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 3
    }
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 02

**Categoria:** diretos

**Frase:** Colmeia 7: peso e temperatura atual.

**Gabarito proposto:**

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

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 03

**Categoria:** diretos

**Frase:** Tem alguma colmeia em alerta agora?

**Gabarito proposto:**

```json
[
  {
    "name": "listar_colmeias_alerta",
    "arguments": {}
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 04

**Categoria:** diretos

**Frase:** Liste as colmeias com problema.

**Gabarito proposto:**

```json
[
  {
    "name": "listar_colmeias_alerta",
    "arguments": {}
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 05

**Categoria:** diretos

**Frase:** Ativa o modo inspecao na colmeia 5 por 20 minutos.

**Gabarito proposto:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 5,
      "duracao_min": 20
    }
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 06

**Categoria:** diretos

**Frase:** Preciso inspecionar a colmeia 12, pausa os alertas por 30 minutos.

**Gabarito proposto:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 12,
      "duracao_min": 30
    }
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 07

**Categoria:** diretos

**Frase:** Como esta a colmeia 1?

**Gabarito proposto:**

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

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 08

**Categoria:** diretos

**Frase:** Mostra os dados da colmeia 9.

**Gabarito proposto:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 9
    }
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 09

**Categoria:** variacoes_fala

**Frase:** E ai, a colmeia dois ta como?

**Gabarito proposto:**

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

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 10

**Categoria:** variacoes_fala

**Frase:** Da uma olhada na colmeia quatro pra mim.

**Gabarito proposto:**

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

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 11

**Categoria:** variacoes_fala

**Frase:** Alguma colmeia pedindo atencao?

**Gabarito proposto:**

```json
[
  {
    "name": "listar_colmeias_alerta",
    "arguments": {}
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 12

**Categoria:** variacoes_fala

**Frase:** Quais colmeias estao fora do normal?

**Gabarito proposto:**

```json
[
  {
    "name": "listar_colmeias_alerta",
    "arguments": {}
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 13

**Categoria:** variacoes_fala

**Frase:** Vou abrir a colmeia 6, desliga o alerta por meia hora.

**Gabarito proposto:**

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

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 14

**Categoria:** variacoes_fala

**Frase:** Bota a colmeia 15 em modo inspecao, uns 10 minutinhos.

**Gabarito proposto:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 15,
      "duracao_min": 10
    }
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 15

**Categoria:** variacoes_fala

**Frase:** Peso da colmeia numero oito?

**Gabarito proposto:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 8
    }
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 16

**Categoria:** variacoes_fala

**Frase:** Umidade e temperatura da colmeia 20, por favor.

**Gabarito proposto:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 20
    }
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 17

**Categoria:** parametro_implicito

**Frase:** Ativa modo inspecao na colmeia 3.

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Duração obrigatória ausente.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 18

**Categoria:** parametro_implicito

**Frase:** Preciso mexer na colmeia 11 rapidinho.

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Intenção e duração insuficientemente definidas.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 19

**Categoria:** parametro_implicito

**Frase:** Status.

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Identificador da colmeia ausente.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 20

**Categoria:** parametro_implicito

**Frase:** Colmeias com alerta nos ultimos dias?

**Gabarito proposto:**

```json
[
  {
    "name": "listar_colmeias_alerta",
    "arguments": {}
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 21

**Categoria:** parametro_implicito

**Frase:** Inspecao na colmeia 9 por um quarto de hora.

**Gabarito proposto:**

```json
[
  {
    "name": "ativar_modo_inspecao",
    "arguments": {
      "colmeia_id": 9,
      "duracao_min": 15
    }
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 22

**Categoria:** parametro_implicito

**Frase:** Coloca a colmeia 2 em inspecao ate eu terminar.

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Duração indeterminada.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 23

**Categoria:** ambiguos

**Frase:** Colmeia 3 e colmeia 4, como estao?

**Gabarito proposto:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 3
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

**Justificativa anterior:** Consulta explícita às colmeias 3 e 4.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 24

**Categoria:** ambiguos

**Frase:** As colmeias da fileira de tras estao bem?

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 25

**Categoria:** ambiguos

**Frase:** Coloca todas as colmeias em modo inspecao.

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Ativação coletiva não suportada pelo schema.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 26

**Categoria:** ambiguos

**Frase:** A colmeia la do fundo, perto da mangueira, ta como?

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 27

**Categoria:** ambiguos

**Frase:** Inspecao na colmeia 5, tipo, agora.

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Duração obrigatória ausente.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 28

**Categoria:** ambiguos

**Frase:** Quero saber da colmeia 3, mas so a temperatura.

**Gabarito proposto:**

```json
[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 3
    }
  }
]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 29

**Categoria:** fora_escopo

**Frase:** Vai chover hoje?

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 30

**Categoria:** fora_escopo

**Frase:** Qual a previsao do tempo pra semana?

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 31

**Categoria:** fora_escopo

**Frase:** Quanto custa um quilo de mel?

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 32

**Categoria:** fora_escopo

**Frase:** Explica como funciona a colmeia.

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 33

**Categoria:** fora_escopo

**Frase:** Oi, tudo bem?

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 34

**Categoria:** fora_escopo

**Frase:** Reinicia o sistema.

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 35

**Categoria:** fora_escopo

**Frase:** Qual o preco do dolar hoje?

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---

## Caso 36

**Categoria:** fora_escopo

**Frase:** Manda um relatorio completo do mes passado.

**Gabarito proposto:**

```json
[]
```

**Justificativa anterior:** Gabarito preservado.

**Decisão humana:** PENDENTE

**Justificativa da decisão:**

---
