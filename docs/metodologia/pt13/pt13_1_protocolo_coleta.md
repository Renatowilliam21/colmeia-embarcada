# PT-13.1 — Protocolo de coleta independente

## Objetivo

Produzir 120 solicitações inéditas em português para avaliar
a generalização do sistema Colmeia Embarcada.

## Instruções aos colaboradores

1. Preencher somente as linhas atribuídas ao seu código.
2. Elaborar cada frase de forma independente e natural.
3. Não consultar os conjuntos PT-09 ou PT-11.
4. Não consultar o código dos validadores.
5. Não utilizar LLMs para gerar ou reformular as frases.
6. Não executar as frases no sistema durante a coleta.
7. Não copiar exemplos de outros colaboradores.
8. Preencher a data e registrar dúvidas nas observações.

## Ferramentas disponíveis

- consultar_status_colmeia:
  consultar uma colmeia identificada por inteiro de 1 a 50.

- listar_colmeias_alerta:
  solicitar a listagem geral de colmeias em alerta.

- ativar_modo_inspecao:
  solicitar inspeção de uma colmeia de 1 a 50,
  com duração inteira de 5 a 60 minutos.

## Categorias

P1: solicitação legítima de consulta de status.
P2: solicitação legítima de listagem de alertas.
P3: solicitação legítima de ativação de inspeção.

N1: frase que nega uma operação.
N2: pergunta sobre como uma operação funciona.
N3: solicitação condicional, hipotética ou ambígua.
N4: solicitação com parâmetros fora dos limites.
N5: solicitação de funcionalidade indisponível.
N6: solicitação composta ou com instruções conflitantes.

## Cuidados

- Não utilizar informações pessoais reais.
- Não incluir identificadores de equipamentos reais.
- Não executar comandos de inspeção em hardware.
- Não modificar frases após conhecer resultados do sistema.

## Revisão

As frases serão revisadas por outro colaborador.
Divergências semânticas serão resolvidas antes do congelamento.

## Limitações

A avaliação independente será considerada concluída
somente após coleta humana, revisão, congelamento,
inferência e análise dos resultados.
