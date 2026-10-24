# PT-15.3.18 — Protocolo experimental

## Objetivo

Comparar a confiabilidade funcional do Needle 2 original e do Needle 2 com correção do cache KV.

## Condições

- BASE: motor Needle 2 no commit 61cafad7014a5664bb3ffd5f0c457ce5aa6598ae.
- PATCH: mesmo commit com o patch PT-15.3.17 aplicado.
- Hardware: ESP32-S3 N16R8.
- Configuração: C2, prefixo 205, sink 192, tail 13.
- Ferramentas: execução simulada.

## Planejamento

- 6 solicitações.
- 2 condições.
- 5 repetições por solicitação e condição.
- Total: 60 inferências planejadas.

## Métricas

1. Ferramenta selecionada corretamente.
2. Argumentos produzidos corretamente.
3. Validade sintática da chamada.
4. Latência de prefill.
5. Latência de geração.
6. Latência total.
7. Integridade do cache KV.
8. Falhas e reinicializações.

## Controles necessários

Antes da coleta, definir e verificar:

- Procedimento de inicialização do estado do modelo.
- Alternância entre as condições BASE e PATCH.
- Ordem de execução para reduzir efeitos de sequência.
- Parâmetros de geração idênticos.
- Identificação do firmware utilizado em cada execução.
- Procedimento para preservar o modelo na partição flash.

## Critério de avaliação

Uma chamada será funcionalmente correta quando a ferramenta e todos os argumentos corresponderem ao resultado esperado.

A confiança informada pelo modelo será registrada apenas como métrica exploratória.

## Estado

Planejamento preparado. Nenhuma inferência da PT-15.3.18 foi executada.
