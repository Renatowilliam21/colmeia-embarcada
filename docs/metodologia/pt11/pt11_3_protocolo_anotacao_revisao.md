# PT-11.3 — Protocolo de anotação e revisão

## 1. Objetivo

Estabelecer procedimentos para elaboração, anotação e revisão
de 120 solicitações inéditas.

O conjunto será utilizado na avaliação independente da
arquitetura Needle 2 + validadores determinísticos.

## 2. Responsabilidades

Colaborador A:
- Elaborar 60 solicitações.
- Revisar as 60 solicitações do colaborador B.

Colaborador B:
- Elaborar 60 solicitações.
- Revisar as 60 solicitações do colaborador A.

Os colaboradores não deverão consultar:
- Código dos validadores V1, V2 e V3.
- Dataset utilizado na PT-09.
- Resultados experimentais da PT-10.
- Frases elaboradas pelo outro colaborador antes da revisão.

## 3. Regras de elaboração

As solicitações deverão utilizar português brasileiro.

Os participantes devem variar:
- Vocabulário.
- Construções gramaticais.
- Formalidade.
- Ordem dos elementos da frase.
- Formas naturais de solicitação.

Não devem produzir apenas variações numéricas
da mesma frase.

## 4. Ferramentas disponíveis

### consultar_status_colmeia

Argumentos:
{"colmeia_id": inteiro entre 1 e 50}

### listar_colmeias_alerta

Argumentos:
{}

### ativar_modo_inspecao

Argumentos:
{
  "colmeia_id": inteiro entre 1 e 50,
  "duracao_min": inteiro entre 5 e 60
}

A ativação de inspeção exige intenção explícita.

## 5. Representação do gabarito

O campo chamadas_esperadas deverá conter JSON válido.

Uma chamada esperada:

[
  {
    "name": "consultar_status_colmeia",
    "arguments": {
      "colmeia_id": 15
    }
  }
]

Nenhuma chamada esperada:

[]

Esses exemplos ilustram somente a estrutura do JSON.

## 6. Critérios de anotação

A anotação deve refletir a intenção expressa na frase.

Não se deve consultar a resposta do Needle 2
para determinar o gabarito.

Parâmetros precisam corresponder ao texto.

Uma solicitação sem autorização suficiente
deve receber lista vazia.

Solicitações de atuação condicionais, negadas,
hipotéticas ou ambíguas não autorizam execução.

Perguntas informativas podem autorizar operações
somente de leitura, quando a intenção for inequívoca.

## 7. Revisão cruzada

O revisor deverá verificar:

1. Adequação da frase à categoria.
2. Clareza da intenção.
3. Correção dos parâmetros.
4. Validade do JSON.
5. Correspondência entre frase e gabarito.
6. Originalidade e diversidade linguística.

## 8. Estados de revisão

pendente:
Caso ainda não revisado.

aprovado:
Frase e gabarito conferidos.

revisar:
Há divergência ou problema identificado.

excluido:
Caso considerado inadequado.

Casos excluídos deverão ser substituídos
antes do congelamento, preservando a distribuição
de categorias e o registro da substituição.

## 9. Resolução de divergências

Toda divergência deverá ser documentada.

A decisão final deve ocorrer antes das inferências.

Se não houver consenso, um terceiro avaliador
deverá realizar a adjudicação, quando disponível.

O gabarito não poderá ser ajustado com base
nas respostas produzidas pelo modelo.

## 10. Congelamento

Após a aprovação dos 120 casos:

1. Consolidar os formulários.
2. Validar os identificadores.
3. Validar a estrutura JSON.
4. Verificar duplicatas.
5. Registrar o procedimento de coleta.
6. Calcular os hashes SHA-256.
7. Registrar a versão do dataset no Git.

Apenas depois dessas etapas será permitida
a execução do Needle 2.

## 11. Integridade experimental

Validador V3 congelado no commit:

c5ecff3

SHA-256 da V3:

a70f8cec58fcf548415f1a2c5572e68b95e534f84b0ccebd38f8f2bc70da3c8a

Os resultados do conjunto PT-11 não deverão
ser utilizados para modificar a V3 e depois
reavaliá-la como validação independente.
