# PT-16 — Protocolo experimental da execução física no ESP32-S3

**Artigo:** Avaliação Exploratória de um Modelo Compacto de Tool-Calling para Interfaces de Comando em Português no Contexto de IoT Apícola  
**Evento:** ERCEMAPI 2026  
**Identificador interno:** PT-16  
**Data da coleta:** 25 de outubro de 2026

## 1. Objetivo e escopo

Documentar o procedimento registrado para submeter 36 comandos em português a um modelo compacto Needle 2 executado em uma placa ESP32-S3 física, coletar chamadas estruturadas de ferramentas e indicadores de desempenho e comparar as saídas com os registros históricos obtidos no Linux host.

A execução física diz respeito **à inferência do modelo no dispositivo**. Não houve despacho das chamadas geradas a handlers, leitura operacional de sensores, acionamento de atuadores nem validação em apiário. O campo `physical_tool_execution` dos metadados é `false`.

## 2. Plataforma e componentes

| Elemento | Registro ou condição |
|---|---|
| Dispositivo | ESP32-S3 N16R8 |
| Modelo | Needle 2, arquivo de referência `needle2.cact` |
| Representação do modelo | Aproximadamente 14 MB, quantização CQ2-bit, conforme caracterização do estudo |
| Comunicação com o host | Porta serial `/dev/ttyACM0` na coleta registrada |
| Script de coleta | `coletar_esp32.py` |
| Dependência externa do coletor | Python `pyserial` |
| Firmware | Compatível com o protocolo serial registrado; imagem e versão exatas não estabelecidas neste documento |
| Motor host de referência | `nd_dump`, do projeto Needle 2 para ESP32 |

O motor e os pesos do modelo não integram o pacote histórico. Para reexecutar o experimento é necessário obtê-los por meios autorizados e preparar o firmware compatível. Não se afirma que os hashes do binário host identifiquem o firmware embarcado.

### 2.1. Proveniência do motor e do modelo

- Commit de referência do motor: `61cafad7014a5664bb3ffd5f0c457ce5aa6598ae`.
- SHA-256 do arquivo `needle2.cact`: `b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba`.
- SHA-256 do executável host `nd_dump`: `7318a5784e0bb91487a2016ebfae7bd6aec2a6692ecb1a308a8bb3c2996577a4`.

O commit é uma referência de proveniência; sua existência não garante, isoladamente, uma compilação reproduzível byte a byte.

## 3. Entradas experimentais

O conjunto contém **36 comandos em português**, relacionados ao contexto de IoT apícola. O esquema de chamadas estruturadas contempla:

1. `consultar_status_colmeia`;
2. `listar_colmeias_alerta`;
3. `ativar_modo_inspecao`.

Arquivos de referência:

- `artefatos/dataset/dataset_original_36_casos.json` — conjunto original;
- `artefatos/schema/schema_historico_original.json` — esquema histórico;
- `artefatos/execucao/raw_results_original.jsonl` — registros originais do Linux host;
- `artefatos/dataset/gabarito_revisado_posteriormente.json` — gabarito revisado **após** as execuções.

O gabarito retrospectivo não deve ser tratado como uma nova rodada experimental.

### 3.1. Origem exata utilizada pelo coletor

O script histórico aponta para:

`results/experiments/needle2_host/20261022T200512Z/raw_results.jsonl`

SHA-256 registrado nos metadados físicos:

`b035651f8d5d9705e58d9f64b2e5a737d56c207f410f7015bd07171c0cfa7e77`

A auditoria verificou identidade integral, inclusive byte a byte, entre esse arquivo e `artefatos/execucao/raw_results_original.jsonl`. Assim, os dados de origem estão presentes no pacote suplementar, embora o **caminho fixo do coletor original** exija a estrutura histórica de diretórios. O script não foi modificado.

## 4. Configuração registrada da coleta física

Os parâmetros a seguir foram extraídos de `resultados_esp32/20261025T164514Z_ESP32S3/metadata.json`.

| Parâmetro | Valor |
|---|---|
| `experiment` | `PT-16` |
| `platform` | `esp32s3` |
| `simulated` | `false` |
| `case_count_expected` | 36 |
| `repetitions` | 1 |
| `max_new` | 96 |
| `think` | `false` |
| `serial_port` | `/dev/ttyACM0` |
| `timeout_per_case_seconds` | 240 |
| `physical_tool_execution` | `false` |
| `status` | `completed` |
| `started_at_utc` | `2026-10-25T16:45:14.495806+00:00` |
| `finished_at_utc` | `2026-10-25T17:06:47.615828+00:00` |

O comando serial `!think 0` foi confirmado pelo firmware: resposta registrada `EVT think=0`, com duração de sincronização de 0,501 s.

## 5. Procedimento documentado

O fluxo abaixo descreve a coleta registrada e os modos previstos no script, sem alegar que um terceiro possa reproduzir a execução sem as dependências externas.

1. Preparar um ESP32-S3 compatível com o firmware e o modelo Needle 2 empregados no estudo.
2. Disponibilizar os 36 comandos e os arquivos de referência na estrutura esperada pelo coletor, conferindo o SHA-256 da entrada.
3. Disponibilizar Python e `pyserial` no computador de coleta e estabelecer a comunicação serial com o dispositivo.
4. Utilizar a verificação prévia do coletor (`--verificar`) para inspecionar entradas e dependências; esse modo não acessa a placa.
5. Na execução física registrada, confirmar o modo sem raciocínio por meio do comando `!think 0`.
6. Submeter sequencialmente os 36 comandos, com uma execução por caso, limite de 96 tokens de saída e timeout de 240 s por caso.
7. Registrar as saídas textuais, as chamadas interpretadas, os eventos seriais, os tempos e os indicadores disponíveis de memória.
8. Encerrar a coleta e registrar metadados, resultados brutos e resumo em arquivos separados.

O script possui ainda `--simular`, destinado a testes com dados sintéticos, e `--executar`, destinado à inferência física. **Resultados simulados não devem ser combinados com os dados do ESP32-S3.** Nenhum modo experimental é executado pela simples leitura deste protocolo.

## 6. Saídas e rastreabilidade

Diretório da coleta física:

`resultados_esp32/20261025T164514Z_ESP32S3/`

| Arquivo | Função | SHA-256 |
|---|---|---|
| `metadata.json` | Configuração e proveniência | `9b41f4f47bf350851fe6530866f04f34c2c2990b6c10dcbf0c717ff00c515288` |
| `raw_results.jsonl` | 36 registros individuais | `07ef15c260c7ace3e57a36a765e3bc0f26d6d6fb4d393836f9527991e44b9905` |
| `resumo.json` | Totalização da coleta | `49c50907f93efdcc9ed9572f57e8ea268e812700e652d1a5a2f5b257dd266bda` |

O resumo registra **36 casos esperados, 36 registrados, 36 concluídos e zero incompletos**. Os identificadores verificados cobrem os casos de 1 a 36. `completed=true` indica conclusão técnica da inferência, não correção semântica.

O JSONL registra, entre outros, `case_id`, `prompt`, `model_output`, `parsed_calls`, `json_valid`, `parse_error`, `elapsed_wall_ms`, `prefill_ms`, `generation_ms`, `generation_tokens`, `generation_tps`, `serial_lines` e campos de memória interna e PSRAM.

A presença de campos de memória não equivale à validação de uma medida consolidada de ocupação de memória. **Não há medição de energia** nesse experimento.

## 7. Avaliação e comparação

As chamadas estruturadas foram comparadas com dois referenciais distintos:

- **Gabarito histórico:** 33 casos avaliáveis; três casos excluídos por problemas de tipagem dos argumentos esperados (19, 23 e 25). Host: 13/33 (39,39%); ESP32-S3: 14/33 (42,42%).
- **Gabarito revisado retrospectivamente:** 36 casos avaliáveis, incluindo 17 casos de abstenção esperada. Host: 13/36 (36,11%); ESP32-S3: 14/36 (38,89%). Não houve nova inferência para essa revisão.

As chamadas estruturadas coincidiram em 34/36 casos (94,44%); as divergências ocorreram nos casos 6 e 34. Essa concordância **não é acurácia**. O teste exato de McNemar resultou em `p = 1,000`; a ausência de diferença estatisticamente significativa **não demonstra equivalência** entre as plataformas.

### 7.1. Desempenho descritivo do ESP32-S3

| Indicador | Valor aproximado |
|---|---:|
| Latência média | 35,85 s |
| Latência mediana | 34,04 s |
| Desvio-padrão da latência | 10,48 s |
| Prefill médio | 14,60 s |
| Geração média | 18,15 s |
| Vazão média de geração | 1,378 token/s |
| Tokens gerados, média | 25,06 |

Os indicadores representam uma única execução por comando, sem estimativa robusta de variabilidade entre rodadas independentes.

## 8. Reprodução analítica versus reexecução física

**Reprodução analítica:** é possível examinar os registros publicados, conferir os hashes e recalcular os indicadores e comparações documentados, sem acesso ao ESP32-S3.

**Reexecução no host:** depende do executável `nd_dump`, do modelo, dos caminhos esperados pelo script `reproduzir_experimento.py` e de ambiente compatível. O relatório `relatorio_reprodutibilidade.md` descreve uma reprodução independente no **Linux host (PT-14)**, não uma segunda execução física.

**Reexecução no ESP32-S3:** requer hardware, firmware compatível, modelo, comunicação serial, `pyserial` e preparação dos caminhos de entrada do coletor. Este pacote não garante reconstrução independente do firmware ou dos binários exatos. Não executar o modo `--executar` sem planejar uma nova rodada e seu registro separado.

## 9. Limitações e precauções de interpretação

- Amostra exploratória de 36 comandos em português, sem generalização estatística ampla.
- Uma execução por caso; não houve replicações independentes por plataforma.
- Ausência de acionamento de ferramentas, sensores ou atuadores.
- Ausência de validação em apiário e com usuários.
- Ausência de medições energéticas.
- Resultados de memória registrados sem uma análise consolidada validada neste protocolo.
- Dependências externas não incluídas no pacote histórico.
- Caminhos locais fixos nos scripts originais.
- Revisão retrospectiva do gabarito, distinta da avaliação histórica.
- Concordância entre plataformas não implica correção semântica nem equivalência estatística.

## 10. Documentos relacionados

- `README_PT16.md`: visão geral e orientação de navegação do PT-16.
- `README.md`, `protocolo_experimental.md`, `resultados_e_metricas.md`, `limitacoes.md`: documentação histórica, a preservar.
- `relatorio_reprodutibilidade.md`: reprodução PT-14 no Linux host.
- `MANIFEST_SHA256.txt`: manifesto dos artefatos históricos; não alterar.
- `resultados_pt16.md`: documento de resultados específico do PT-16, previsto para a etapa seguinte.
- `MANIFEST_PT16_SHA256.txt`: manifesto complementar, a criar após a seleção final dos arquivos.

**Estado:** protocolo documental da coleta física PT-16, preparado a partir dos registros auditados. Não substitui o código, os metadados ou os dados brutos originais.
