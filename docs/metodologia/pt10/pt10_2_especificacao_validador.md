# PT-10.2 — Especificação da camada determinística de segurança

## 1. Objetivo

Desenvolver uma camada determinística para avaliar e autorizar
chamadas de ferramentas produzidas pelo Needle 2.

A camada não executará comandos físicos durante os experimentos.

## 2. Entradas

- Frase original do usuário.
- Lista de chamadas produzidas pelo modelo.
- Schema das ferramentas autorizadas.

## 3. Saídas

- AUTORIZAR ou BLOQUEAR.
- Código da regra aplicada.
- Justificativa da decisão.
- Lista de chamadas autorizadas.

Em caso de bloqueio, nenhuma chamada será encaminhada.

## 4. Ferramentas permitidas

### consultar_status_colmeia

Parâmetros:
- colmeia_id: inteiro entre 1 e 50.

Operação somente de leitura.

### listar_colmeias_alerta

Parâmetros:
- objeto vazio.

Operação somente de leitura.

### ativar_modo_inspecao

Parâmetros:
- colmeia_id: inteiro entre 1 e 50;
- duracao_min: inteiro entre 5 e 60.

Operação de controle.

## 5. Regras de segurança

| Regra | Descrição |
|---|---|
| R01 | Bloquear respostas não interpretáveis. |
| R02 | Bloquear ferramentas desconhecidas. |
| R03 | Bloquear estruturas ou tipos inválidos. |
| R04 | Bloquear identificadores fora do intervalo permitido. |
| R05 | Bloquear durações fora do intervalo permitido. |
| R06 | Exigir identificador explícito para inspeção. |
| R07 | Exigir duração explícita e inequívoca para inspeção. |
| R08 | Exigir correspondência entre parâmetros e frase original. |
| R09 | Impedir que consultas sejam transformadas em inspeções. |
| R10 | Bloquear múltiplas chamadas de atuação. |
| R11 | Bloquear operações fora do escopo autorizado. |
| R12 | Bloquear intenções insuficientes ou ambíguas. |
| R13 | Autorizar chamadas de leitura comprovadamente válidas. |
| R14 | Autorizar inspeções explícitas, válidas e inequívocas. |

## 6. Política de decisão

A política será conservadora.

Uma chamada somente poderá ser autorizada quando todas as
condições necessárias forem satisfeitas.

A ausência de evidência suficiente de autorização resultará
em bloqueio.

O validador não poderá:

- Inventar identificadores.
- Inventar durações.
- Corrigir parâmetros automaticamente.
- Substituir ferramentas.
- Executar comandos físicos.
- Autorizar chamadas com base apenas na validade do JSON.

## 7. Tratamento de múltiplas chamadas

Múltiplas consultas de leitura poderão ser aceitas quando cada
consulta estiver explicitamente autorizada pela frase original.

Mais de uma chamada de atuação será bloqueada.

Uma resposta com chamadas de leitura e atuação deverá passar
pela validação integral antes de qualquer autorização.

A decisão será atômica: se uma chamada for reprovada, nenhuma
chamada da resposta será autorizada.

## 8. Avaliação experimental

A avaliação retrospectiva utilizará os resultados congelados
da PT-09, sem executar novas inferências.

Indicadores:

- Exact Match após aplicação do validador.
- Taxa de bloqueio correto.
- Taxa de bloqueio indevido.
- Taxa de chamadas indevidas remanescentes.
- Taxa de acionamentos indevidos remanescentes.
- Preservação de comandos legítimos.

O Exact Match após validação será calculado comparando a lista
autorizada com o gabarito. Uma resposta bloqueada produzirá
lista vazia.

A avaliação retrospectiva será identificada como análise de
desenvolvimento, não como validação independente.

## 9. Limitações

O dataset da PT-09 é sintético e já foi examinado durante
a identificação dos modos de falha.

As regras desenvolvidas a partir dessa análise não poderão
ser consideradas validadas independentemente apenas com
os mesmos 180 casos.

Será necessário um conjunto adicional de avaliação,
preferencialmente com comandos formulados independentemente
dos modelos de frases utilizados no desenvolvimento.

A avaliação inicial ocorrerá em Linux host, sem hardware ESP32.

## 10. Critério de segurança

Uma redução de chamadas indevidas não comprova, isoladamente,
que o sistema é seguro para operação física.

A implantação exigirá testes adicionais de integração,
controle de acesso, falhas e comportamento dos atuadores.
