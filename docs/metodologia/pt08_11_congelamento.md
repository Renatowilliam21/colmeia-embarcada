# PT-08.11 — Homologação e congelamento experimental

## Decisão

Os 180 gabaritos sintéticos foram homologados pelo
responsável pelo experimento, após a revisão semântica
dos seis lotes e a consolidação PT-08.10.

**Estado:** HOMOLOGADO_CONGELADO

**Versão:** 1.0.0

## Integridade

- Dataset original: `dataset/synthetic/colmeia-needle2-sintetico-v1.json`
- SHA-256 original: `c0927a014dec323e83db8ef68641b99c777818cdff8fab3445c4a418e79ed555`
- Dataset congelado: `dataset/frozen/colmeia-needle2-sintetico-v1-homologado.json`
- SHA-256 congelado: `becf137d69b5eb39ad727f10be70b48672d2909d75a1c1563617e53f5a5fda18`
- Schema SHA-256: `aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2`

## Composição

- Total: 180 casos
- Com chamadas esperadas: 80
- Sem chamadas esperadas: 100

## Política operacional

- Consultas múltiplas de leitura são permitidas.
- Ativações múltiplas são proibidas pelo protocolo.
- Parâmetros obrigatórios ausentes não são inferidos.
- Parâmetros inválidos não são corrigidos automaticamente.
- Pedidos fora do escopo não produzem chamadas.

## Limitações

Os casos foram gerados sinteticamente a partir de
famílias de templates e não constituem observações
linguísticas independentes.

Os 36 casos originais já utilizados na exploração
devem ser analisados separadamente.

A avaliação de seleção de ferramentas não equivale
à avaliação da qualidade de respostas em linguagem
natural.

## Regra de preservação

Qualquer alteração futura dos casos ou gabaritos
deverá produzir uma nova versão, sem sobrescrever
o conjunto congelado.

## Próxima etapa

Executar o protocolo experimental com os modelos
selecionados e registrar predições, latência,
validade estrutural, correção semântica e violações
da política operacional.
