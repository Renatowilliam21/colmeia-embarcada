# Colmeia v2.0 + Needle 2 — Experimento exploratório (ERCEMAPI 2026)

Repositório de apoio ao artigo submetido ao ERCEMAPI 2026: avaliação
exploratória do Needle 2 (motor de tool-calling compacto, offline) como
interface de comando em português para IoT apícola.

## Status

Em desenvolvimento. Prazo de submissão: 06/09/2026.

## ⚠️ Aviso sobre revisão double-blind

Este repositório **não deve ser referenciado no artigo nem tornado público**
enquanto a revisão double-blind estiver em andamento. Manter como **privado**
no GitHub até a decisão do ERCEMAPI 2026. Não commitar nomes de autores,
instituição ou laboratório em nenhum arquivo texto (README incluso).

## Estrutura

```
.
├── docs/                         guia de desenvolvimento, notas, figuras
├── dataset/                      dataset de teste (36 casos em PT-BR)
├── firmware/                     schema de tools + scripts de execução
│   └── tools/
│       ├── colmeia.json          schema compactado das 3 ferramentas
│       └── run_dataset.py        script de execução em lote (a implementar)
├── paper/                        esqueleto LaTeX do artigo + bibliografia
└── results/                      CSVs brutos e classificados do experimento
```

O motor de inferência (Needle 2) **não está vendorizado aqui** — ver
`firmware/README.md` para como obtê-lo via fork do repositório original.

## Como reproduzir

1. Seguir `firmware/README.md` para obter e configurar o motor Needle 2.
2. Copiar `firmware/tools/colmeia.json` para o lugar do `tools/led.json`
   de referência.
3. Implementar os handlers conforme `docs/guia-desenvolvimento.md`.
4. Rodar `firmware/tools/run_dataset.py` contra `dataset/colmeia-needle2-dataset-teste.json`.
5. Resultados brutos em `results/resultados_brutos.csv`; classificação e
   métricas agregadas em arquivos subsequentes na mesma pasta.
6. Artigo em `paper/artigo-needle2-colmeia-esqueleto.tex`.

## Créditos e licença

Este projeto usa como base o motor de inferência do repositório
[`andrisgauracs/needle-2-esp32`](https://github.com/andrisgauracs/needle-2-esp32).
**Confirmar a licença exata no repositório original antes de publicar** e
manter o aviso de copyright deles no fork. O material próprio deste
repositório (schema `colmeia.json`, handlers, dataset, scripts, artigo) —
definir licença antes de tornar público (ex.: MIT para código, CC-BY para
dataset/artigo).
