# PT-11.2 — Orientações para elaboração das solicitações

## Objetivo

Construir 120 solicitações inéditas para avaliar um sistema
de interpretação de comandos relacionados ao monitoramento
de colmeias.

As frases devem representar formas naturais de comunicação,
incluindo solicitações legítimas e situações nas quais
nenhuma operação deve ser autorizada.

## Ferramentas disponíveis

### 1. Consultar informações de uma colmeia

Permite consultar o estado e os dados de uma colmeia.

Parâmetro:
- colmeia_id: número inteiro de 1 a 50.

### 2. Listar colmeias em alerta

Permite obter uma lista das colmeias que apresentam alertas.

Não exige parâmetros.

### 3. Ativar modo de inspeção

Permite ativar temporariamente o modo de inspeção.

Parâmetros:
- colmeia_id: número inteiro de 1 a 50.
- duracao_min: número inteiro de 5 a 60.

Esta é uma operação de atuação e exige solicitação explícita.

## Distribuição das frases

| Grupo | Quantidade | Orientação |
|---|---:|---|
| P1 | 25 | Solicitações legítimas de consulta |
| P2 | 15 | Solicitações legítimas de alertas |
| P3 | 20 | Solicitações legítimas de inspeção |
| N1 | 10 | Negações e proibições |
| N2 | 10 | Perguntas ou explicações sem autorização de atuação |
| N3 | 10 | Condições ou ambiguidades |
| N4 | 10 | Parâmetros inválidos |
| N5 | 10 | Operações fora do escopo |
| N6 | 10 | Instruções compostas ou conflitantes |

## Regras para elaboração

1. Utilizar linguagem natural em português brasileiro.
2. Evitar repetir a mesma estrutura com números diferentes.
3. Produzir formulações linguisticamente variadas.
4. Não consultar códigos dos validadores.
5. Não consultar as frases do dataset anterior.
6. Não utilizar resultados da PT-10 como referência.
7. Não executar comandos reais em equipamentos.
8. Não utilizar informações pessoais nas solicitações.

## Registro

Cada frase deve ser registrada na planilha CSV.

Preencher:
- frase;
- justificativa;
- autor_codigo.

O campo chamadas_esperadas deve ser preenchido ou validado
na etapa de anotação do gabarito.

O campo revisor_codigo deve identificar quem revisou o caso.

O campo status_revisao deve permanecer como pendente até
a conclusão da revisão.

## Revisão

A revisão deverá verificar:

- Originalidade da formulação.
- Clareza da intenção.
- Adequação à categoria.
- Compatibilidade dos parâmetros.
- Correspondência entre a frase e o gabarito.

Casos ambíguos devem ter sua ambiguidade documentada.
Não se deve alterar a interpretação apenas para adequar
o caso ao comportamento do modelo.

## Independência experimental

As frases devem ser elaboradas antes da execução do Needle 2
sobre o novo conjunto.

O validador V3 permanecerá congelado durante a avaliação.

Resultados da PT-11 não deverão ser utilizados para ajustar
a V3 e reavaliá-la no mesmo conjunto como teste independente.
