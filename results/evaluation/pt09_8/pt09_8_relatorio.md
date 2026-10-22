# PT-09.8 — Avaliação experimental Needle 2

## Resultados gerais

- Inferências: 540
- Exact Match: 195/540 (36.11%)
- Schema válido: 537/540 (99.44%)
- Abstenções corretas: 15/300
- Chamadas indevidas: 282
- Acionamentos indevidos: 135
- Erros de parsing: 3
- Latência média: 3241.19 ms
- Latência mediana: 3238.76 ms
- Latência P95: 3552.20 ms

## Estabilidade

- Casos com três predições idênticas: 180/180
- Casos corretos nas três repetições: 65/180
- Casos incorretos nas três repetições: 115/180

## Limitações metodológicas

- O dataset é sintético e derivado de modelos de frases.
- As três repetições não são observações independentes.
- Os resultados foram obtidos em Linux host, não em ESP32.
- O indicador CONF não foi interpretado como probabilidade calibrada.
- Nenhuma ação física foi executada.
- Uma chamada estruturalmente válida não garante segurança.
- A ordem das chamadas é considerada no Exact Match.
- Acionamento indevido é definido como chamada de inspeção diferente das chamadas de inspeção esperadas.
