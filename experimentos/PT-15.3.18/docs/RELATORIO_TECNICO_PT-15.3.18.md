# PT-15.3.18 — Relatório técnico experimental

**Data de consolidação:** 24/10/2026  
**Plataforma:** ESP32-S3 N16R8  
**Modelo:** Needle 2  
**Objeto:** comparação entre reutilização de cache KV do prefixo (PATCH)
e reprocessamento integral do prefixo a cada solicitação (BASE).

## 1. Objetivo

Avaliar o impacto da reutilização do estado KV de um prefixo fixo
sobre a latência de execução de comandos em linguagem natural,
mantendo a avaliação da correção das chamadas de ferramentas.

## 2. Desenho experimental

Foram definidos seis casos (E01–E06), com cinco repetições em cada
uma das duas condições, totalizando 60 execuções oficiais:
30 PATCH e 30 BASE.

As condições foram avaliadas no ESP32-S3. Na PATCH, o estado KV do
prefixo é reutilizado. Na BASE, o prefixo de 205 tokens é
reprocessado a cada solicitação.

As chamadas de ferramentas foram simuladas, conforme indicado pelo
campo `simulated=1` nos logs. Portanto, a correção observada diz
respeito à seleção da ferramenta e dos argumentos esperados, não
à atuação física sobre dispositivos.

As durações foram registradas pelos coletores com
`time.monotonic()`, desde antes do envio da solicitação até a
conclusão normal do protocolo de resposta.

## 3. Integridade e rastreabilidade

Foram preservados 60 arquivos JSON e 60 arquivos LOG oficiais.
Seus hashes SHA-256 constam em
`resultados/manifesto_sha256.csv`.

Os arquivos `PT15318-DIAG-E01.json` e
`PT15318-DIAG-E01.log` foram preservados, mas excluídos
da análise oficial. Execuções piloto também não integram
as estatísticas apresentadas.

## 4. Correção funcional

As 60 execuções oficiais foram classificadas como corretas:
30/30 PATCH e 30/30 BASE, segundo os critérios dos coletores.

## 5. Comparação de latência

| Indicador | Principal (29 pares) | Sensibilidade (30 pares) |
|---|---:|---:|
| PATCH, média (s) | 39.963 | 40.144 |
| BASE, média (s) | 153.465 | 153.647 |
| Economia absoluta (s) | 113.502 | 113.502 |
| Redução percentual | 73.96% | 73.87% |
| Razão BASE/PATCH | 3.840× | 3.827× |

A análise principal utiliza 29 pares com registro explícito
de `RESULT` nas duas condições. A análise de sensibilidade
inclui os 30 pares originalmente coletados.

## 6. Resultados por caso

| Caso | PATCH (s) | BASE (s) | Diferença (s) | Redução |
|---|---:|---:|---:|---:|
| E01 | 45.395 | 158.900 | 113.505 | 71.43% |
| E02 | 46.103 | 159.616 | 113.513 | 71.12% |
| E03 | 44.677 | 158.185 | 113.508 | 71.76% |
| E04 | 48.244 | 161.754 | 113.510 | 70.17% |
| E05 | 31.063 | 144.556 | 113.492 | 78.51% |
| E06 | 25.383 | 138.869 | 113.486 | 81.72% |

Todas as seis médias por caso favoreceram a PATCH.

## 7. Inferência estatística exploratória

Considerando as seis solicitações distintas como unidades
de comparação, a diferença média BASE − PATCH foi
113.502400 s, com desvio-padrão entre casos de 0.010696 s.

O intervalo t de 95% para a diferença média entre os seis
casos foi [113.491175; 113.513625] s.

O teste exato bilateral de sinais apresentou p = 0,03125,
com seis diferenças positivas e nenhuma negativa.

Esses resultados dependem das hipóteses dos testes e não
devem ser extrapolados automaticamente para outras tarefas,
modelos, dispositivos ou tamanhos de prefixo.

## 8. Decomposição temporal

Médias observadas nas 30 execuções de cada condição:

| Etapa | PATCH | BASE |
|---|---:|---:|
| Reprocessamento do prefixo | Não registrado | 113,480 s |
| Prefill da solicitação | 17,122 s | 17,137 s |
| Geração | 20,226 s | 20,247 s |

A diferença entre os tempos de prefill foi de aproximadamente
0,0151 s e entre os tempos de geração, 0,0207 s.

A economia total média de 113,5024 s é compatível com
a eliminação do reprocessamento do prefixo, que consumiu
em média 113,480 s na condição BASE.

## 9. Limitações

1. Apenas seis solicitações distintas foram avaliadas,
   com cinco repetições por condição.
2. A execução PATCH R01-E01 possui `ACT` correto e
   `EVT done`, mas não apresenta `RESULT` no log.
   Seu tempo foi preservado na análise de sensibilidade,
   não na análise principal.
3. O campo `firmware_verificado=False` na PATCH indica
   ausência de verificação explícita pelo coletor utilizado.
   A BASE registrou verificação explícita.
4. O prefixo possui tamanho fixo de 205 tokens.
   A economia observada não caracteriza outros tamanhos.
5. A avaliação de ferramentas utilizou execução simulada.
6. Os seis casos foram selecionados para o experimento;
   não constituem amostra aleatória de comandos gerais.
7. Os intervalos inferenciais refletem a variabilidade
   observada neste desenho experimental restrito.

## 10. Conclusão

Nas condições avaliadas, a reutilização do cache KV do
prefixo reduziu substancialmente a latência sem alterar
a taxa de correção observada das chamadas de ferramentas.

Na análise principal, a redução média foi de 73.96%,
correspondente a 113.502 s por solicitação e aceleração
de 3.840×.

A decomposição temporal sustenta a interpretação de que
a maior parte da economia resulta da eliminação do
reprocessamento do prefixo fixo.

## 11. Artefatos de reprodução

- `PROTOCOLO.md`
- `config/casos.json`
- `config/matriz_execucoes.csv`
- `scripts/coletor_lote.py`
- `scripts/coletor_lote_base.py`
- `logs/patch/`
- `logs/base/`
- `resultados/manifesto_sha256.csv`

**Nota:** este relatório foi gerado a partir dos arquivos
experimentais preservados. Não foram executados novos testes.
