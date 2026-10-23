#!/usr/bin/env python3
"""PT-13.1 — Preparação da coleta humana independente."""

import csv
from pathlib import Path

ROOT = Path.cwd()

COLETA = ROOT / "dataset/validation/pt13/coleta"
DOCS = ROOT / "docs/metodologia/pt13"

COLETA.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

DISTRIBUICAO = {
    "P1": 25,
    "P2": 15,
    "P3": 20,
    "N1": 10,
    "N2": 10,
    "N3": 10,
    "N4": 10,
    "N5": 10,
    "N6": 10,
}

DESCRICOES = {
    "P1": "Consultar status de uma colmeia",
    "P2": "Listar colmeias em alerta",
    "P3": "Ativar modo de inspeção",
    "N1": "Negação de operação",
    "N2": "Pergunta explicativa",
    "N3": "Solicitação condicional ou ambígua",
    "N4": "Parâmetros inválidos",
    "N5": "Fora do escopo",
    "N6": "Comandos compostos ou conflitantes",
}

FIELDS = [
    "id",
    "grupo",
    "descricao_grupo",
    "frase",
    "autor_codigo",
    "data_coleta",
    "observacoes_autor",
]

COLABORADORES = ["A", "B", "C", "D"]

# Distribuição balanceada por categoria.
linhas = {codigo: [] for codigo in COLABORADORES}

contador_global = 0

for grupo, quantidade in DISTRIBUICAO.items():
    for indice in range(1, quantidade + 1):
        colaborador = COLABORADORES[
            contador_global % len(COLABORADORES)
        ]

        linhas[colaborador].append({
            "id": f"PT13-{grupo}-{indice:03d}",
            "grupo": grupo,
            "descricao_grupo": DESCRICOES[grupo],
            "frase": "",
            "autor_codigo": colaborador,
            "data_coleta": "",
            "observacoes_autor": "",
        })

        contador_global += 1

for colaborador, registros in linhas.items():
    destino = COLETA / (
        f"pt13_1_coleta_colaborador_{colaborador}.csv"
    )

    if destino.exists():
        raise FileExistsError(
            f"Arquivo já existe: {destino}"
        )

    with destino.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        writer = csv.DictWriter(
            arquivo,
            fieldnames=FIELDS,
            delimiter=";",
        )

        writer.writeheader()
        writer.writerows(registros)

    print(
        f"[OK] Colaborador {colaborador}: "
        f"{len(registros)} solicitações"
    )

protocolo = """# PT-13.1 — Protocolo de coleta independente

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
"""

destino = DOCS / "pt13_1_protocolo_coleta.md"

if destino.exists():
    raise FileExistsError(
        f"Protocolo já existe: {destino}"
    )

destino.write_text(protocolo, encoding="utf-8")

print("\n[OK] Protocolo criado:", destino.relative_to(ROOT))
print("[OK] Total previsto:", contador_global)
