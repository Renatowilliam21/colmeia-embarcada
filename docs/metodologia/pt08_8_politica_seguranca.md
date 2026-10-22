# PT-08.8 — Política de segurança e validação

## Identificação

- Dataset sintético SHA-256: `c0927a014dec323e83db8ef68641b99c777818cdff8fab3445c4a418e79ed555`
- Schema SHA-256: `aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2`
- Quantidade de casos: 180
- Estado: PENDENTE DE REVISÃO HUMANA

## Política experimental

1. Consultas de duas colmeias identificadas podem gerar duas chamadas de leitura.
2. Inspeções individuais exigem identificador e duração válidos.
3. Solicitações de múltiplas ativações de inspeção devem resultar em nenhuma chamada executável.
4. Parâmetros obrigatórios ausentes exigem abstenção.
5. Identificadores e durações fora dos limites exigem abstenção.
6. Solicitações fora do escopo exigem abstenção.

## Fundamentação

A restrição sobre múltiplas ativações é uma política conservadora de segurança operacional, não uma limitação estrutural do schema.

O sistema deverá implementar uma camada de validação independente do modelo antes de executar ações.

A lista vazia `[]` representa ausência de chamadas executáveis; não demonstra que o modelo pediu esclarecimentos.

## Validação

A auditoria automática confirma apenas propriedades estruturais e consistência com regras codificadas.

A aprovação semântica individual permanece pendente.

## Distribuição por família

| Família | Quantidade |
|---|---:|
| acao_multipla_nao_suportada | 17 |
| administracao | 6 |
| alertas_direto | 1 |
| analise_nao_suportada | 6 |
| consulta_multipla | 16 |
| controle_nao_suportado | 6 |
| conversa_geral | 6 |
| duracao_ausente | 24 |
| duracao_indeterminada | 8 |
| duracao_invalida | 5 |
| identificador_ausente | 2 |
| identificador_invalido | 2 |
| inspecao_coloquial | 15 |
| inspecao_direta | 20 |
| intencao_insuficiente | 6 |
| mercado | 6 |
| previsao_tempo | 6 |
| sensores_direto | 2 |
| status_coloquial | 21 |
| status_direto | 5 |
