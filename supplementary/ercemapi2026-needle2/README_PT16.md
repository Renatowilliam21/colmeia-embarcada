# PT-16 — Experimento Needle 2 no ESP32-S3

## Identificação

**Artigo:** Avaliação Exploratória de um Modelo Compacto de Tool-Calling para Interfaces de Comando em Português no Contexto de IoT Apícola.

**Evento:** ERCEMAPI 2026.  
**Identificação:** PT-16.  
**Modelo:** Needle 2.  
**Ambientes:** Linux host e ESP32-S3 N16R8 físico.

Este documento descreve os artefatos suplementares da avaliação exploratória da geração de chamadas estruturadas de ferramentas a partir de 36 comandos em português no contexto de IoT apícola. O experimento não executou handlers de ferramentas, não consultou sensores e não acionou atuadores.

## Escopo e histórico

O experimento original no Linux host avaliou 36 comandos, uma execução por comando, utilizando as ferramentas `consultar_status_colmeia`, `listar_colmeias_alerta` e `ativar_modo_inspecao`.

O relatório `relatorio_reprodutibilidade.md` documenta uma reprodução independente no Linux host (PT-14) que obteve correspondência integral das saídas textuais e chamadas estruturadas nos 36 casos. **Essa reprodução não é a execução física PT-16.**

O PT-16 registrou 36 inferências concluídas no ESP32-S3 físico, com uma execução por caso, `max_new=96`, modo de raciocínio desativado (`!think 0`) e timeout de 240 segundos por caso. Os metadados indicam `simulated=false` e `physical_tool_execution=false`.

## Modelo e proveniência

- Motor host: `nd_dump`, projeto Needle 2 para ESP32.
- Modelo: `needle2.cact`.
- Commit de referência do motor: `61cafad7014a5664bb3ffd5f0c457ce5aa6598ae`.
- SHA-256 do modelo: `b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba`.
- SHA-256 do binário host: `7318a5784e0bb91487a2016ebfae7bd6aec2a6692ecb1a308a8bb3c2996577a4`.

O commit é uma referência de proveniência, não uma garantia de reconstrução binária idêntica. O motor e os pesos do modelo não foram incorporados ao pacote histórico.

## Resultados de correção

| Critério | Linux host | ESP32-S3 |
|---|---:|---:|
| Gabarito histórico, 33 casos avaliáveis | 13/33 (39,39%) | 14/33 (42,42%) |
| Gabarito revisado retrospectivamente, 36 casos | 13/36 (36,11%) | 14/36 (38,89%) |

No gabarito histórico, os casos 19, 23 e 25 foram excluídos por problemas de tipagem dos argumentos esperados. O gabarito revisado foi aplicado retrospectivamente, sem novas inferências, e contempla 17 abstenções esperadas.

As chamadas estruturadas do host e do ESP32-S3 coincidiram em **34/36 casos (94,44%)**; as divergências ocorreram nos casos 6 e 34. Essa concordância **não é acurácia**. O teste exato de McNemar resultou em `p=1,000`; a ausência de diferença significativa **não demonstra equivalência**.

## Desempenho físico observado

| Métrica | Valor |
|---|---:|
| Latência média | 35,85 s |
| Latência mediana | 34,04 s |
| Desvio-padrão da latência | 10,48 s |
| Prefill médio | 14,60 s |
| Geração média | 18,15 s |
| Vazão média de geração | 1,378 token/s |
| Tokens gerados, média | 25,06 |

São estatísticas descritivas de uma execução por caso. Não foram medidas potência nem energia.

## Arquivos principais

- `README.md`: documentação histórica do pacote.
- `protocolo_experimental.md`, `resultados_e_metricas.md`, `limitacoes.md`: documentação histórica do Linux host.
- `relatorio_reprodutibilidade.md`: reprodução independente PT-14 no host.
- `artefatos/dataset/dataset_original_36_casos.json`: conjunto original de comandos.
- `artefatos/dataset/gabarito_revisado_posteriormente.json`: referência retrospectiva.
- `artefatos/schema/schema_historico_original.json`: esquema de ferramentas.
- `artefatos/execucao/raw_results_original.jsonl`: resultados históricos do host.
- `artefatos/avaliacao/`: resultados históricos de avaliação.
- `artefatos/scripts/`: scripts históricos de processamento e avaliação.
- `reproduzir_experimento.py`: utilitário de verificação e reexecução no host.
- `coletar_esp32.py`: coletor de inferências no ESP32-S3.
- `resultados_esp32/20261025T164514Z_ESP32S3/`: `metadata.json`, `raw_results.jsonl` e `resumo.json` da coleta física.
- `MANIFEST_SHA256.txt`: manifesto dos 16 arquivos históricos; não deve ser alterado.

## Rastreabilidade e integridade

O arquivo histórico `artefatos/execucao/raw_results_original.jsonl` é idêntico, inclusive em bytes, ao arquivo de origem indicado nos metadados físicos (`results/experiments/needle2_host/20261022T200512Z/raw_results.jsonl`). Seu SHA-256 é:

`b035651f8d5d9705e58d9f64b2e5a737d56c207f410f7015bd07171c0cfa7e77`

Hashes dos arquivos físicos em `resultados_esp32/20261025T164514Z_ESP32S3/`:

| Arquivo | SHA-256 |
|---|---|
| `metadata.json` | `9b41f4f47bf350851fe6530866f04f34c2c2990b6c10dcbf0c717ff00c515288` |
| `raw_results.jsonl` | `07ef15c260c7ace3e57a36a765e3bc0f26d6d6fb4d393836f9527991e44b9905` |
| `resumo.json` | `49c50907f93efdcc9ed9572f57e8ea268e812700e652d1a5a2f5b257dd266bda` |

Os arquivos históricos e seus hashes devem permanecer intactos. Um manifesto adicional específico do PT-16 será preparado após a seleção final dos artefatos para publicação.

## Reprodução e dependências

A **reprodução analítica** utiliza os datasets, os gabaritos e os resultados publicados para verificar hashes, recalcular métricas e comparar chamadas, sem executar o modelo novamente.

A **reexecução no Linux host** exige o motor e o modelo externos nos caminhos previstos em `reproduzir_experimento.py`. Esse script oferece os modos `verify` (verificação), `dry-run` (preparação sem inferência) e `run` (nova inferência no host). O modo `run` não reproduz a coleta física.

A **reexecução no ESP32-S3** exige hardware, firmware compatível, comunicação serial e `pyserial`. O script `coletar_esp32.py` possui os modos `--verificar`, `--simular` e `--executar`. Somente `--executar` realiza inferências físicas. O script original espera os dados de entrada no caminho histórico `results/experiments/needle2_host/20261022T200512Z/raw_results.jsonl`, fora da pasta suplementar; uma nova instalação pode precisar recriar essa estrutura. A cópia de mesmo hash está disponível no pacote.

Os scripts originais não foram modificados na preparação deste README. Não se deve interpretar a presença de scripts como garantia de portabilidade irrestrita ou reprodução binária idêntica.

## Limitações

- Amostra de 36 comandos e uma execução por caso.
- Ausência de testes com usuários e de validação em apiários.
- Nenhuma execução real de ferramentas, leitura de sensores ou atuação física.
- Ausência de medições energéticas e de repetição experimental para estimar variabilidade entre rodadas.
- Dependência de motor, modelo e firmware externos para reexecução.
- Revisão retrospectiva do gabarito, distinta da avaliação histórica.
- Ausência de demonstração de equivalência estatística entre ambientes.

## Reutilização

Ao reutilizar os artefatos, identifique o gabarito aplicado e diferencie os resultados históricos, a reprodução PT-14 e a coleta física PT-16. A publicação dos dados não concede automaticamente direitos de redistribuição sobre o motor, o modelo ou componentes de terceiros; suas licenças devem ser verificadas separadamente.

**Estado:** documentação suplementar em preparação para publicação.
