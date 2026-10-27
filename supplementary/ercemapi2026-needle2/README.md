# Pacote interno de reprodutibilidade — ERCEMAPI 2026

Artigo: Avaliação Exploratória de um Modelo Compacto de Tool-Calling
para Interfaces de Comando em Português no Contexto de IoT Apícola.

## Estado

Pacote de trabalho interno, preparado a partir dos artefatos históricos
verificados nas auditorias PT-13 e PT-14.

Este pacote não representa autorização de publicação ou distribuição.
Licenciamento e disponibilização pública permanecem pendentes.

## Organização

- artefatos/dataset: conjunto original e gabarito revisado posteriormente.
- artefatos/schema: schema exato identificado no manifesto original.
- artefatos/execucao: metadados e saídas brutas.
- artefatos/avaliacao: resultados processados e resumo.
- artefatos/scripts: scripts históricos de inferência e avaliação.

## Cuidados metodológicos

O gabarito original está incorporado ao dataset original.

O arquivo `gabarito_revisado_posteriormente.json` não deve ser tratado
como o gabarito empregado na avaliação inicial.

Os resultados foram obtidos em Linux host, com uma execução por frase.
Não representam medições de latência, memória ou energia no ESP32.

A avaliação original possui três casos não comparáveis ao gabarito.
Consultar `resultados_e_metricas.md` e `limitacoes.md`.

## Integridade

O arquivo `MANIFEST_SHA256.txt` permite verificar os arquivos copiados.

Os arquivos históricos são preservados sem alterações.
