# PT-15.3.17-D — Integridade do cache KV

## Objetivo

Verificar experimentalmente se o mecanismo de snapshot e rewind
restaura os buffers do tail do prefixo após sua sobrescrita pelo
cache circular durante a inferência.

## Ambiente experimental

- Plataforma: ESP32-S3 N16R8
- Modelo: Needle 2
- Janela de contexto: 256 tokens
- Prefixo C2: 205 tokens
- Sink: 192 tokens
- Tail preservado: 13 tokens
- Camadas: 27
- Ferramentas simuladas: 3

## Mapeamento do cache

A função `kv_slot()` utiliza a seguinte expressão para posições
fora da região fixa:

    slot = n_sink + (pos - n_sink) % (window - n_sink)

Para a configuração C2:

- Posições 0–191: região fixa
- Posições 192–204: tail do prefixo
- Posição 256: sobrescreve a posição física 192
- Posição 268: sobrescreve a posição física 204

O snapshot armazena os quatro buffers do tail:

- k_cache
- v_cache
- k_scale
- v_scale

## Instrumentação

Foi adicionada a função `kv_verify()` ao firmware.

A função compara o conteúdo atual dos buffers com o snapshot
por meio de `memcmp()`.

O diagnóstico contabiliza o número de camadas com diferenças
em cada buffer.

A verificação é realizada antes e depois de `nd_model_rewind()`.

## Resultado observado

Antes da restauração:

    KV_DIAG phase=before_rewind pos=270 tail=13 layers=27 diff_k=27 diff_v=27 diff_ks=27 diff_vs=27 result=DIFF

Depois da restauração:

    KV_DIAG phase=after_rewind pos=205 tail=13 layers=27 diff_k=0 diff_v=0 diff_ks=0 diff_vs=0 result=PASS

Outras restaurações observadas apresentaram diferenças nas
27 camadas antes do rewind e nenhuma diferença depois.

## Interpretação

O resultado demonstra que:

1. O processamento ultrapassou o início da região circular.
2. Os quatro buffers do tail foram modificados.
3. O rewind restaurou o conteúdo dos buffers preservados.
4. O modelo continuou executando chamadas de ferramenta válidas.

## Limitações

A instrumentação contabiliza diferenças por camada, não por
posição individual ou byte.

A comparação confirma a correspondência entre os buffers
restaurados e o snapshot, mas não demonstra que todos os
tokens do prefixo permaneceram acessíveis à atenção durante
uma geração longa.

O resultado corresponde à configuração C2 testada.

## Conclusão

A PT-15.3.17-D confirmou experimentalmente a restauração
dos quatro buffers do tail do cache KV após sua modificação
durante a inferência.
