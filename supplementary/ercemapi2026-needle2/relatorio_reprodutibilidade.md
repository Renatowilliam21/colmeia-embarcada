# Relatório Técnico de Reprodutibilidade Experimental

## PT-14 — ERCEMAPI 2026

**Trabalho:** Avaliação Exploratória de um Modelo Compacto de Tool-Calling para Interfaces de Comando em Português no Contexto de IoT Apícola

**Natureza do documento:** relatório técnico de reprodução experimental independente.

**Ambiente:** Linux host.

**Data de execução registrada (UTC):** 2026-10-25T14:02:45.649301+00:00

**Data de encerramento registrada (UTC):** 2026-10-25T14:04:37.872617+00:00

**Situação:** reprodução concluída, com 36 casos processados e nenhuma falha técnica registrada.

---

## 1. Objetivo

Documentar a reprodução independente da execução histórica de 36 comandos em português submetidos ao modelo Needle 2, preservando o dataset, o esquema de ferramentas, o modelo, o motor de inferência de referência e os parâmetros experimentais.

O objetivo específico foi verificar se uma nova execução no ambiente Linux host produziria as mesmas saídas textuais e chamadas estruturadas registradas no experimento original.

Esta reprodução não constitui avaliação de desempenho embarcado no ESP32-S3, estudo com usuários ou validação em apiários.

## 2. Delineamento experimental

A reprodução utilizou os 36 casos do dataset original, com uma execução por caso.

A inferência foi realizada sequencialmente no Linux host, sem acionamento físico de ferramentas, sensores ou atuadores.

A execução utilizou o esquema histórico de três ferramentas:

1. `consultar_status_colmeia`;
2. `listar_colmeias_alerta`;
3. `ativar_modo_inspecao`.

O processamento das saídas utilizou o parser histórico, que identifica o primeiro bloco `<tool_call>` e interpreta seu conteúdo JSON como uma lista de chamadas.

A geração utiliza amostragem greedy com restrições gramaticais, conforme a implementação do motor inspecionada durante a auditoria técnica. O modo `nothink` foi utilizado para suprimir a geração do conteúdo de raciocínio.

Não foram configurados parâmetros de amostragem por temperatura, top-k ou top-p.

## 3. Configuração e rastreabilidade

| Elemento | Valor |
|---|---|
| Ambiente de execução | `Linux host` |
| Plataforma registrada | `Linux-7.0.0-38-generic-x86_64-desconhecido-with-glibc2.43` |
| Python | `3.14.4` |
| Commit de referência do motor | `61cafad7014a5664bb3ffd5f0c457ce5aa6598ae` |
| Repetições por caso | `1` |
| Limite de geração (`max_new`) | `96` |
| Modo `think` | `false` |
| Timeout por caso | `300 s` |
| Casos selecionados | `36` |
| Execução física de ferramentas | `false` |

### 3.1 Identificadores SHA-256

| Artefato | SHA-256 |
|---|---|
| Dataset original | `44848860ea06a7b8cdd297316d497d641d43d69185962bb3913b9e16d7b5be8e` |
| Esquema histórico | `aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2` |
| Modelo Needle 2 | `b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba` |
| Binário host | `7318a5784e0bb91487a2016ebfae7bd6aec2a6692ecb1a308a8bb3c2996577a4` |
| Parser histórico | `3e711ab09274c0d9a5dccdbbec1040fc7f09f56d0beabb255170c25f31ff12f6` |
| Executor independente | `fdebccc4fd1748854d18de485683e33bb1410fdde918288761651a648ec14691` |
| Resultados brutos históricos | `b035651f8d5d9705e58d9f64b2e5a737d56c207f410f7015bd07171c0cfa7e77` |
| Resultados brutos reproduzidos | `1d8e23b3313ccbf8eafa6995be5c959a87e145945b80b795e609d9440271b4f0` |
| Metadados da reprodução | `84bca5e00afab6529a9f1aca48ce9df8aefb8428d91953bf7c62f19b64d3056c` |

O commit do motor está armazenado em `engine_commit_referencia` nos novos metadados e em `engine_commit` nos metadados históricos.

A igualdade dos hashes do modelo, esquema e dataset foi verificada diretamente. O commit é registrado como referência de proveniência; a presente auditoria documental não substitui uma verificação independente de identidade do código-fonte em cada ambiente futuro.

## 4. Procedimento de reprodução

O executor independente realizou:

1. Verificação da integridade dos artefatos históricos;
2. Verificação do ambiente e dos componentes de inferência;
3. Criação de diretório exclusivo para os resultados novos;
4. Execução sequencial dos 36 comandos com o esquema histórico;
5. Captura das saídas brutas, códigos de retorno, eventos e tempos;
6. Reconstrução dos tokens e interpretação das chamadas;
7. Gravação incremental de resultados JSONL;
8. Atualização dos metadados de execução;
9. Classificação do estado final do experimento.

O executor foi previamente testado quanto à reconstrução das 36 saídas históricas e à classificação simulada de estados de encerramento.

## 5. Resultados da reprodução

| Indicador | Resultado |
|---|---:|
| Casos históricos | 36 |
| Casos reproduzidos | 36 |
| Prompts idênticos | 36/36 |
| Respostas textuais idênticas | 36/36 |
| Chamadas estruturadas idênticas | 36/36 |
| Divergências observadas | 0 |
| Retornos de subprocesso iguais a zero | 36/36 |
| Erros de execução | 0 |
| Erros de parsing | 0 |

A reprodução apresentou correspondência exata entre os campos `prompt`, `model_output`, `parsed_calls` e `parse_error` para todos os 36 identificadores.

A identidade das saídas não significa que as respostas sejam semanticamente corretas, apenas que os resultados registrados foram reproduzidos.

## 6. Avaliação histórica preservada

A avaliação original apresentou:

| Indicador | Resultado |
|---|---:|
| Total de casos | 36 |
| Acertos | 13 |
| Erros | 20 |
| Não avaliáveis | 3 |
| Acertos sobre o conjunto completo | **13/36 = 36,11%** |
| Exact match entre casos avaliáveis | **13/33 = 39,39%** |

Os casos **19, 23 e 25** foram considerados não avaliáveis na avaliação histórica devido a problemas na estrutura do gabarito original. Essa classificação não deve ser interpretada como falha de inferência.

O percentual de 36,11% utiliza todos os 36 casos como denominador; o percentual de 39,39% considera exclusivamente os 33 casos comparáveis. As duas medidas respondem a critérios de contabilização diferentes e não devem ser apresentadas como resultados intercambiáveis.

### 6.1 Distribuição por categoria

| Categoria | Total | Corretos | Incorretos | Indeterminados |
|---|---:|---:|---:|---:|
| `ambiguos` | 6 | 1 | 3 | 2 |
| `diretos` | 8 | 6 | 2 | 0 |
| `fora_escopo` | 8 | 2 | 6 | 0 |
| `parametro_implicito` | 6 | 1 | 4 | 1 |
| `variacoes_fala` | 8 | 3 | 5 | 0 |

A distribuição por categoria deriva da avaliação histórica. Como as chamadas estruturadas foram reproduzidas integralmente, essa avaliação permanece aplicável à nova execução sob o mesmo gabarito e procedimento de comparação.

## 7. Limitações metodológicas

- O experimento compreende apenas 36 frases, com uma execução por caso.
- A identidade das saídas foi observada no ambiente Linux host inspecionado; não se demonstra portabilidade da reprodução para qualquer hardware ou sistema operacional.
- Não houve avaliação experimental de latência, memória ou consumo energético no ESP32-S3 nesta reprodução.
- Não foram utilizados sensores reais nem realizados acionamentos físicos.
- Não houve estudo com usuários finais ou apicultores nesta etapa.
- Não foi realizado experimento comparativo controlado com modelos alternativos ou baseline determinístico independente.
- Os três casos historicamente não avaliáveis permanecem identificados e não foram corrigidos retrospectivamente.
- Os tempos capturados são tempos de execução no host e não podem ser apresentados como latências embarcadas.
- A reprodução exata de uma execução não equivale a demonstração de robustez estatística entre diferentes sementes, configurações, dispositivos ou distribuições de comandos.

## 8. Integridade e preservação

O pacote contém 16 artefatos históricos registrados no arquivo `MANIFEST_SHA256.txt`, todos verificados sem divergências na auditoria final.

Os resultados reproduzidos foram armazenados separadamente, no diretório:

`resultados_novos/20261025T140245Z_c00d27c4/`

Os arquivos históricos não foram sobrescritos. Não houve `git commit` nem `git push` durante a reprodução e as auditorias documentadas.

O pacote permanece interno, sem decisão registrada de publicação ou licenciamento.

## 9. Conclusão

A reprodução independente executada no Linux host produziu saídas textuais e chamadas estruturadas idênticas às do experimento histórico nos 36 casos, sem falhas técnicas registradas.

Os resultados reforçam a rastreabilidade e a reprodutibilidade operacional da execução original sob as condições verificadas.

A avaliação histórica permanece em 13 acertos, 20 erros e 3 casos não avaliáveis, correspondendo a 36,11% sobre o conjunto completo ou 39,39% entre os casos comparáveis.

Esses achados devem ser interpretados como evidência de reprodução exata das saídas no host, sem extrapolação para desempenho embarcado, segurança operacional de atuadores ou generalização a comandos não avaliados.

---

**Documento gerado a partir dos artefatos históricos e dos registros da reprodução independente.**
