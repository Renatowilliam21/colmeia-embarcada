#!/usr/bin/env python3
"""PT-15.3.18 — Coleta automatizada da condição PATCH."""

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import serial

BASE = Path(__file__).resolve().parents[1]
MATRIZ = BASE / "config" / "matriz_execucoes.csv"
DESTINO = BASE / "logs" / "patch"

CASOS = ("E01", "E02", "E03", "E04", "E05", "E06")


def carregar_casos():
    with MATRIZ.open(encoding="utf-8", newline="") as arquivo:
        registros = list(csv.DictReader(arquivo))

    selecionados = []

    for caso_id in CASOS:
        correspondencias = [
            r for r in registros
            if r["caso_id"] == caso_id
            and r["condicao"] == "patch"
        ]

        if not correspondencias:
            raise ValueError(f"Caso PATCH não encontrado: {caso_id}")

        selecionados.extend(correspondencias)

    selecionados.sort(key=lambda r: (
        int(r["repeticao"]),
        r["caso_id"]
    ))
    return selecionados


def interpretar_act(linha):
    partes = linha.strip().split()

    if len(partes) < 2 or partes[0] != "ACT":
        return None

    if partes[1] == "none":
        return None

    argumentos = {}

    for campo in partes[2:]:
        if "=" not in campo:
            return None

        chave, valor = campo.split("=", 1)

        if chave == "simulated":
            if valor != "1":
                return None
            continue

        if chave not in ("colmeia_id", "duracao_min"):
            return None

        try:
            argumentos[chave] = int(valor)
        except ValueError:
            return None

    return partes[1], argumentos


def receber_linha(conexao):
    return conexao.readline().decode("utf-8", errors="replace")


def aguardar(conexao, marcador, timeout):
    inicio = time.monotonic()

    while time.monotonic() - inicio < timeout:
        linha = receber_linha(conexao)

        if linha:
            print(linha.rstrip(), flush=True)

        if marcador in linha:
            return True

    return False


def executar_caso(conexao, registro):
    caso_id = registro["caso_id"]
    identificador = registro["execucao_id"]

    log = DESTINO / f"{identificador}.log"
    resumo = DESTINO / f"{identificador}.json"

    if log.exists() or resumo.exists():
        raise FileExistsError(
            f"Já existe resultado para {identificador}"
        )

    esperado_nome = registro["ferramenta_esperada"]
    esperado_args = json.loads(registro["argumentos_esperados"])

    print(f"\n=== EXECUTANDO {identificador} ===")
    print("Solicitação:", registro["solicitacao"])

    inicio = time.monotonic()
    act = None
    result = None
    erro_ferramenta = False
    eventos = []

    with log.open("x", encoding="utf-8") as arquivo:
        arquivo.write(f"# execucao={identificador}\n")
        arquivo.write(f"# data={datetime.now().isoformat()}\n")
        arquivo.write(
            f"# solicitacao={registro['solicitacao']}\n"
        )

        conexao.write(
            (registro["solicitacao"] + "\n").encode("utf-8")
        )
        conexao.flush()

        while time.monotonic() - inicio < 180:
            linha = receber_linha(conexao)

            if not linha:
                continue

            arquivo.write(linha)
            arquivo.flush()
            print(linha.rstrip(), flush=True)

            eventos.append(linha.strip())

            if linha.startswith("ERR "):
                erro_ferramenta = True

            if linha.startswith("ACT "):
                act = linha.strip()
                if act == "ACT none":
                    break

            if linha.startswith("RESULT ") and act is not None:
                result = linha.strip()
                break

        if act is None or (act != "ACT none" and result is None):
            arquivo.write("# ERRO resposta_incompleta\n")
            raise TimeoutError(
                f"Resposta incompleta: {identificador}"
            )

    obtido = interpretar_act(act)

    correto = (
        obtido is not None
        and obtido[0] == esperado_nome
        and obtido[1] == esperado_args
    )

    resultado = {
        "execucao_id": identificador,
        "caso_id": caso_id,
        "condicao": "patch",
        "data": datetime.now().isoformat(),
        "solicitacao": registro["solicitacao"],
        "ferramenta_esperada": esperado_nome,
        "argumentos_esperados": esperado_args,
        "act": act,
        "result": result,
        "erro_ferramenta": erro_ferramenta,
        "ferramenta_obtida": obtido[0] if obtido else None,
        "argumentos_obtidos": obtido[1] if obtido else None,
        "correto": correto,
        "duracao_s": round(time.monotonic() - inicio, 3),
        "kv_diag": [
            linha for linha in eventos
            if linha.startswith("KV_DIAG")
        ],
        "evts": [
            linha for linha in eventos
            if linha.startswith("EVT prefill")
            or linha.startswith("EVT done")
        ],
        "conf": [
            linha for linha in eventos
            if linha.startswith("CONF ")
        ],
        "firmware_verificado": False,
    }

    with resumo.open("x", encoding="utf-8") as arquivo:
        json.dump(resultado, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")

    print(f"[RESULTADO] {identificador}: correto={correto}")

    return resultado


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--porta", default="/dev/ttyACM0")
    parser.add_argument("--baudrate", type=int, default=115200)
    parser.add_argument("--timeout-inicio", type=int, default=300)
    parser.add_argument("--verificar", action="store_true")
    parser.add_argument("--limite", type=int, default=3)

    args = parser.parse_args()
    casos = carregar_casos()

    if args.limite < 1 or args.limite > 30:
        parser.error("--limite deve estar entre 1 e 30")

    if args.verificar:
        print("=== COLETA PATCH PT-15.3.18 ===")

        for registro in casos:
            print(
                registro["caso_id"],
                registro["solicitacao"]
            )

        print("[OK] Execuções disponíveis:", len(casos))
        print("[OK] Limite configurado:", args.limite)
        print("[OK] Nenhuma conexão serial aberta")
        return 0

    DESTINO.mkdir(parents=True, exist_ok=True)

    pendentes = []
    concluidos = 0

    for registro in casos:
        identificador = registro["execucao_id"]
        log = DESTINO / (identificador + ".log")
        resumo = DESTINO / (identificador + ".json")

        if log.exists() and resumo.exists():
            dados = json.loads(resumo.read_text(encoding="utf-8"))

            if dados.get("execucao_id") != identificador:
                raise ValueError(
                    f"Identificador incompatível: {identificador}"
                )

            concluidos += 1
            continue

        if log.exists() or resumo.exists():
            raise ValueError(
                f"Execução parcial requer revisão: {identificador}"
            )

        pendentes.append(registro)

    casos = pendentes[:args.limite]

    print("[INFO] Execuções concluídas:", concluidos)
    print("[INFO] Execuções pendentes:", len(pendentes))
    print("[INFO] Selecionadas para este lote:", len(casos))

    for registro in casos:
        print(
            "[PENDENTE]",
            registro["execucao_id"],
            registro["solicitacao"]
        )

    if not casos:
        print("[OK] Todas as execuções PATCH estão registradas")
        return 0

    print("[INFO] Abrindo sessão serial única")

    with serial.Serial(
        port=args.porta,
        baudrate=args.baudrate,
        timeout=0.5,
        write_timeout=5,
        exclusive=True,
        dsrdtr=False,
        rtscts=False,
    ) as conexao:

        conexao.dtr = False
        conexao.rts = False

        print("[INFO] Aguardando READY")

        if not aguardar(
            conexao,
            "READY - type a request",
            args.timeout_inicio
        ):
            raise TimeoutError("Firmware não apresentou READY")

        conexao.write(b"!think 0\n")
        conexao.flush()

        if not aguardar(conexao, "EVT think=0", 10):
            raise TimeoutError("Firmware não confirmou !think 0")

        resultados = []

        for registro in casos:
            resultado = executar_caso(conexao, registro)
            resultados.append(resultado)

            # Uma chamada incorreta é registrada, mas não impede
            # os próximos casos. Falhas de comunicação interrompem.
            time.sleep(1)

    print("\n=== RESUMO DO LOTE PATCH ===")

    for resultado in resultados:
        print(
            resultado["execucao_id"],
            "CORRETO" if resultado["correto"] else "INCORRETO",
            f"tempo={resultado['duracao_s']}s"
        )

    print("[OK] Lote finalizado")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (
        OSError,
        ValueError,
        TimeoutError,
        serial.SerialException,
    ) as erro:
        print("[ERRO]", erro, file=sys.stderr)
        sys.exit(1)
