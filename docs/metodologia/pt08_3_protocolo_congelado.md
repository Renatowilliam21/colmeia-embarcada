# PT-08.3 — Protocolo experimental congelado

## Integridade

- Dataset original: `44848860ea06a7b8cdd297316d497d641d43d69185962bb3913b9e16d7b5be8e`
- Dataset revisado: `03660b445074d0a045639c8b1e12a0b079d5687d67e34239896df6da1d2e7faf`
- Dataset final: `59b267f878efaa80e414f02065e33f018661a961baeaacf033ec893f30b291c5`
- Schema: `aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2`

## Decisões metodológicas

- Os 36 casos foram revisados semanticamente.
- Os casos 17, 18, 19, 22, 25 e 27 exigem abstenção.
- O caso 23 exige duas consultas independentes.
- O caso 20 exige abstenção por ausência de consulta histórica.
- O caso 28 mantém consulta de status, com ressalva sobre seleção de atributos.
- Comandos fora do escopo exigem abstenção.

## Limitações

O protocolo foi estabelecido após uma rodada exploratória.
As inferências posteriores não constituem um conjunto de teste independente, pois reutilizam os mesmos 36 comandos.

A lista vazia representa ausência de chamada executável, não uma solicitação de esclarecimento ao usuário.

A validade estrutural de uma chamada não comprova segurança operacional.
