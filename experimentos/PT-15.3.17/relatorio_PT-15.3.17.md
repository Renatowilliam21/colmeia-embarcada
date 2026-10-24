# PT-15.3.17 — Correção e validação do snapshot KV

## Contexto

O projeto Colmeia Embarcada executa o modelo Needle 2
localmente em um ESP32-S3.

O firmware disponibiliza três ferramentas simuladas para
operações relacionadas ao monitoramento de colmeias.

A configuração C2 utiliza um prefixo de 205 tokens e uma
região fixa (sink) de 192 tokens.

Os 13 tokens restantes ocupam posições da região circular
do cache KV.

## Problema investigado

Durante inferências suficientemente longas, o mecanismo
circular pode sobrescrever as posições do tail do prefixo.

Sem a restauração desses dados, solicitações posteriores
podem reutilizar um estado de cache diferente daquele
produzido ao final do priming.

## Correção implementada

O mecanismo de snapshot foi ampliado para preservar:

- Chaves quantizadas
- Valores quantizados
- Escalas das chaves
- Escalas dos valores

O rewind restaura os buffers antes de cada solicitação.

## PT-15.3.17-D — Integridade

Resultado observado:

- Antes do rewind: diferenças em 27 camadas nos quatro buffers.
- Depois do rewind: zero camadas com diferenças.
- Posição restaurada: 205.
- Tail preservado: 13 tokens.

Conclusão: restauração dos buffers confirmada no cenário
experimental observado.

## PT-15.3.17-E — Regressão funcional

Foram identificadas seis solicitações corretas:

| Teste | Ferramenta | Resultado |
|---|---|---|
| E01 | ativar_modo_inspecao(3,10) | Correto |
| E02 | ativar_modo_inspecao(7,20) | Correto |
| E03 | ativar_modo_inspecao(12,15) | Correto |
| E04 | ativar_modo_inspecao(5,30) | Correto |
| E05 | consultar_status_colmeia(5) | Correto |
| E06 | listar_colmeias_alerta() | Correto |

Taxa de acerto observada: 6/6 (100%).

Latência média de prefill + geração: 37.348 segundos.

A latência não inclui o priming inicial.

## Comparação descritiva

| Configuração | Acertos |
|---|---|
| C2 original | 1/4 |
| C3 sem descrições | 2/4 |
| C2 corrigido — quatro frases de inspeção | 4/4 |
| C2 corrigido — seis solicitações | 6/6 |

As execuções não constituem um estudo estatístico
controlado e não permitem atribuir causalidade
exclusivamente à correção do cache KV.

## Limitações

1. Amostra funcional reduzida.
2. Execuções sem repetições independentes suficientes.
3. Confiança do modelo não calibrada.
4. Ferramentas executadas em modo simulado.
5. Integridade validada especificamente para o cenário C2.
6. Logs apresentados incluem repetições e não identificam
   explicitamente cada solicitação com um marcador E01–E06.

## Próximas atividades

1. Preservar os logs integrais dos experimentos.
2. Executar repetições controladas com identificação de testes.
3. Comparar versões anterior e corrigida sob condições equivalentes.
4. Avaliar o comportamento com gerações mais longas.
5. Consolidar os resultados para publicação científica.
