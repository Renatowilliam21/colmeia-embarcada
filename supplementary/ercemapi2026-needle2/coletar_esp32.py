#!/usr/bin/env python3
"""Coletor experimental Needle 2 / ESP32-S3 — PT-16.

Modos:
    --verificar  Valida entradas e dependencias, sem acessar a placa.
    --simular    Testa o fluxo com dados sinteticos identificados.
    --executar   Executa 36 inferencias reais no ESP32-S3.

Nao modifica firmware, Flash ou arquivos historicos.
"""

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[2]

ENTRADA = (
    RAIZ
    / "results/experiments/needle2_host"
    / "20261022T200512Z/raw_results.jsonl"
)

SAIDA = Path(__file__).resolve().parent / "resultados_esp32"

SHA_ESPERADO = (
    "b035651f8d5d9705e58d9f64b2e5a737d56c207f410f7015bd07171c0cfa7e77"
)

MAX_NEW = 96
TIMEOUT_PADRAO = 240


def agora():
    return datetime.now(timezone.utc).isoformat()


def gravar_json(caminho, dados):
    temporario = caminho.with_suffix(caminho.suffix + ".tmp")
    with temporario.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
        arquivo.flush()
    temporario.replace(caminho)


def carregar_casos():
    conteudo = ENTRADA.read_bytes()
    sha = hashlib.sha256(conteudo).hexdigest()

    if sha != SHA_ESPERADO:
        raise ValueError(
            "SHA-256 do conjunto historico divergente: " + sha
        )

    casos = [
        json.loads(linha)
        for linha in conteudo.decode("utf-8").splitlines()
        if linha.strip()
    ]

    if len(casos) != 36:
        raise ValueError("Esperados exatamente 36 registros")

    ids = [caso.get("case_id") for caso in casos]
    frases = [caso.get("prompt") for caso in casos]

    if ids != list(range(1, 37)):
        raise ValueError("IDs historicos invalidos ou fora de ordem")

    if not all(isinstance(f, str) and f.strip() for f in frases):
        raise ValueError("Frase vazia ou invalida")

    if len(set(frases)) != 36:
        raise ValueError("Frases duplicadas")

    if any(c.get("max_new") != MAX_NEW for c in casos):
        raise ValueError("max_new historico diferente de 96")

    if any(c.get("think") is not False for c in casos):
        raise ValueError("Configuracao think historica divergente")

    if any(c.get("repetition") != 1 for c in casos):
        raise ValueError("Repeticao historica divergente")

    return casos, sha


def extrair_campos_evento(linha):
    """Converte pares chave=valor de eventos EVT em campos tipados."""
    campos = {}
    if not linha:
        return campos
    for chave, valor in re.findall(
        r"([a-zA-Z_][a-zA-Z0-9_]*)=([^\s]+)", linha
    ):
        if re.fullmatch(r"-?\d+", valor):
            campos[chave] = int(valor)
        elif re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", valor):
            campos[chave] = float(valor)
        else:
            campos[chave] = valor
    return campos

def interpretar_linhas(linhas):
    tokens = []
    prefill = geracao = confianca = None
    memoria_antes = memoria_depois = None
    erros = []
    iniciou = terminou = False
    acao = None

    for linha in linhas:
        if linha.startswith("TOK "):
            tokens.append(linha[4:])
        if re.search(r"\bEVT\s+memory phase=before\b", linha):
            iniciou = True
            memoria_antes = linha
        if re.search(r"\bEVT\s+memory phase=after\b", linha):
            memoria_depois = linha
        if re.search(r"\bEVT\s+prefill\b", linha):
            prefill = linha
        if re.search(r"\bEVT\s+done\b", linha):
            terminou = True
            geracao = linha
        if linha.startswith("CONF "):
            confianca = linha
        if linha.startswith("ERR "):
            erros.append(linha)
        if linha.startswith("ACT "):
            acao = linha

    saida_modelo = "".join(tokens)
    chamadas = None
    erro_parse = None

    if saida_modelo:
        texto = saida_modelo.strip()
        texto = re.sub(r"^<tool_call>\s*", "", texto).strip()
        texto = re.sub(r"</tool_call>\s*$", "", texto).strip()
        try:
            chamadas = json.loads(texto)
        except json.JSONDecodeError as erro:
            erro_parse = str(erro)

    p = extrair_campos_evento(prefill)
    g = extrair_campos_evento(geracao)
    ma = extrair_campos_evento(memoria_antes)
    md = extrair_campos_evento(memoria_depois)

    concluido = (
        iniciou and terminou and memoria_depois is not None
        and acao == "ACT none benchmark_no_physical_execution"
        and not erros
    )

    return {
        "model_output": saida_modelo,
        "parsed_calls": chamadas,
        "parse_error": erro_parse,
        "json_valid": chamadas is not None,
        "answer_correct": None,
        "correctness_evaluated": False,
        "token_count_observed": len(tokens),
        "prefill_event": prefill,
        "prefill_tokens": p.get("tokens"),
        "prefill_ms": p.get("ms"),
        "prefill_tps": p.get("tps"),
        "generation_event": geracao,
        "generation_tokens": g.get("tokens"),
        "generation_ms": g.get("ms"),
        "generation_tps": g.get("tps"),
        "confidence_event": confianca,
        "memory_before_event": memoria_antes,
        "memory_after_event": memoria_depois,
        "psram_free_before": ma.get("psram_free"),
        "psram_free_after": md.get("psram_free"),
        "internal_free_before": ma.get("internal_free"),
        "internal_free_after": md.get("internal_free"),
        "psram_min_free_before": ma.get("psram_min_free"),
        "psram_min_free_after": md.get("psram_min_free"),
        "internal_min_free_before": ma.get("internal_min_free"),
        "internal_min_free_after": md.get("internal_min_free"),
        "action_event": acao,
        "error_events": erros,
        "inference_started": iniciou,
        "inference_finished": terminou,
        "completed": concluido,
    }



def ler_inferencia(dispositivo, limite):
    inicio = time.monotonic()
    buffer = bytearray()
    linhas = []
    terminou = acao = erro = False
    falha = None

    while time.monotonic() - inicio < limite:
        try:
            dados = dispositivo.read(512)
        except Exception as excecao:
            falha = f"{type(excecao).__name__}: {excecao}"
            break

        if not dados:
            continue

        buffer.extend(dados)
        while b"\n" in buffer:
            linha, _, restante = buffer.partition(b"\n")
            buffer = bytearray(restante)
            texto = linha.decode("utf-8", errors="replace").rstrip("\r")
            if not texto:
                continue

            linhas.append(texto)
            print(texto, flush=True)

            if re.search(r"\bEVT\s+done\b", texto):
                terminou = True
            if texto.startswith("ACT "):
                acao = True
            if texto.startswith("ERR "):
                erro = True

        if (terminou and acao) or erro:
            break

    if buffer:
        linhas.append(
            "[HOST_PARTIAL_SERIAL] "
            + buffer.decode("utf-8", errors="replace")
        )

    duracao = time.monotonic() - inicio

    if falha:
        linhas.append("[HOST_SERIAL_ERROR] " + falha)
    elif not ((terminou and acao) or erro):
        linhas.append(f"[HOST_TIMEOUT] limit_seconds={limite}")

    return linhas, duracao



def resultado_caso(
    caso, linhas, duracao, simulado,
    inicio_utc=None, fim_utc=None
):
    interpretacao = interpretar_linhas(linhas)
    falhas_host = [
        linha for linha in linhas if linha.startswith("[HOST_")
    ]
    if falhas_host:
        interpretacao["completed"] = False

    return {
        "case_id": caso["case_id"],
        "category": caso.get("category"),
        "prompt": caso["prompt"],
        "repetition": 1,
        "max_new": MAX_NEW,
        "think": False,
        "platform": "simulation" if simulado else "esp32s3",
        "simulated": simulado,
        "started_at_utc": inicio_utc or agora(),
        "finished_at_utc": fim_utc or agora(),
        "elapsed_wall_ms": round(duracao * 1000, 3),
        "serial_lines": linhas,
        "host_errors": falhas_host,
        **interpretacao,
    }



def linhas_simuladas(caso):
    """Dados artificiais apenas para teste do coletor."""
    return [
        (
            "EVT memory phase=before "
            "psram_free=0 internal_free=0 "
            "psram_min_free=0 internal_min_free=0"
        ),
        "EVT reading 1/1",
        "EVT prefill tokens=1 ms=1 tps=1 sink=0",
        'TOK [{"name":"SIMULACAO_NAO_E_RESULTADO","arguments":{}}]',
        "CONF 0.0000",
        "EVT done tokens=1 ms=1 tps=1",
        (
            "EVT memory phase=after "
            "psram_free=0 internal_free=0 "
            "psram_min_free=0 internal_min_free=0"
        ),
        "ACT none benchmark_no_physical_execution",
    ]


def executar(args):
    casos, sha = carregar_casos()

    if args.modo == "verificar":
        print("[OK] 36 casos historicos validados")
        print("[OK] SHA-256:", sha)
        print("[OK] max_new=96, think=False, repetition=1")
        print("[OK] Nenhuma comunicacao serial realizada")
        print("[OK] Nenhum arquivo criado")
        return 0

    simulado = args.modo == "simular"

    if not simulado:
        try:
            import serial
        except ImportError:
            print("[ERRO] Dependencia pyserial indisponivel")
            return 2

    SAIDA.mkdir(parents=True, exist_ok=True)

    identificador = (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + ("_SIMULACAO" if simulado else "_ESP32S3")
    )

    diretorio = SAIDA / identificador
    diretorio.mkdir(exist_ok=False)

    metadata = {
        "experiment": "PT-16",
        "platform": "simulation" if simulado else "esp32s3",
        "simulated": simulado,
        "started_at_utc": agora(),
        "source_file": str(ENTRADA.relative_to(RAIZ)),
        "source_sha256": sha,
        "case_count_expected": 36,
        "repetitions": 1,
        "max_new": MAX_NEW,
        "think": False,
        "serial_port": None if simulado else args.porta,
        "timeout_per_case_seconds": args.timeout,
        "physical_tool_execution": False,
        "status": "running",
    }

    gravar_json(diretorio / "metadata.json", metadata)

    resultados = []
    dispositivo = None

    try:
        if not simulado:
            dispositivo = serial.Serial(
                port=args.porta,
                baudrate=115200,
                timeout=0.5,
                write_timeout=10,
            )

            print("[OK] Porta serial:", args.porta, flush=True)
            time.sleep(2)

            comando = b"!think 0\n"
            escritos = dispositivo.write(comando)
            dispositivo.flush()

            if escritos != len(comando):
                raise RuntimeError(
                    "Falha ao configurar !think 0"
                )

            confirmacao = bytearray()
            confirmado = False
            inicio_sincronizacao = time.monotonic()
            limite_sincronizacao = 180.0

            print(
                "[INFO] Aguardando confirmacao de !think 0 "
                f"(limite={limite_sincronizacao:.0f}s)",
                flush=True,
            )

            while (
                time.monotonic() - inicio_sincronizacao
                < limite_sincronizacao
            ):
                dados = dispositivo.read(512)

                if not dados:
                    continue

                confirmacao.extend(dados)

                if len(confirmacao) > 65536:
                    confirmacao = confirmacao[-65536:]

                if re.search(
                    rb"\bEVT\s+think=0\b",
                    bytes(confirmacao),
                ):
                    confirmado = True
                    break

            duracao_sincronizacao = (
                time.monotonic() - inicio_sincronizacao
            )

            metadata["serial_sync"] = {
                "command": "!think 0",
                "confirmed": confirmado,
                "duration_seconds": round(
                    duracao_sincronizacao, 3
                ),
                "timeout_seconds": limite_sincronizacao,
                "received_bytes": len(confirmacao),
                "received_text_tail": confirmacao.decode(
                    "utf-8", errors="replace"
                )[-4096:],
            }

            if not confirmado:
                raise RuntimeError(
                    "Comando !think 0 nao confirmado pelo firmware "
                    f"apos {duracao_sincronizacao:.1f}s"
                )

            print(
                "[OK] think=0 confirmado "
                f"em {duracao_sincronizacao:.2f}s",
                flush=True,
            )

        with (diretorio / "raw_results.jsonl").open(
            "w", encoding="utf-8"
        ) as arquivo:
            for caso in casos:
                identificador_caso = caso["case_id"]

                print(
                    f"\n[CASO {identificador_caso:02d}/36] "
                    f"{caso['prompt']}",
                    flush=True,
                )

                inicio_caso_utc = agora()
                linhas = []
                duracao = 0.0

                if simulado:
                    linhas = linhas_simuladas(caso)
                else:
                    inicio_monotonico = time.monotonic()
                    try:
                        dados = (caso["prompt"] + "\n").encode("utf-8")
                        escritos = dispositivo.write(dados)
                        dispositivo.flush()

                        if escritos != len(dados):
                            raise RuntimeError(
                                "Transmissao incompleta no caso "
                                f"{identificador_caso}"
                            )

                        linhas, duracao = ler_inferencia(
                            dispositivo, args.timeout
                        )

                    except Exception as excecao:
                        duracao = time.monotonic() - inicio_monotonico
                        linhas.append(
                            "[HOST_TRANSPORT_ERROR] "
                            f"{type(excecao).__name__}: {excecao}"
                        )

                fim_caso_utc = agora()

                resultado = resultado_caso(
                    caso, linhas, duracao, simulado,
                    inicio_utc=inicio_caso_utc,
                    fim_utc=fim_caso_utc,
                )

                arquivo.write(
                    json.dumps(
                        resultado, ensure_ascii=False
                    ) + "\n"
                )
                arquivo.flush()

                resultados.append(resultado)

                print(
                    "[RESULTADO] "
                    f"concluido={resultado['completed']} "
                    f"tokens={resultado['token_count_observed']} "
                    f"tempo={duracao:.2f}s",
                    flush=True,
                )

                if not resultado["completed"]:
                    print(
                        "[ATENCAO] Coleta interrompida: "
                        "caso incompleto",
                        flush=True,
                    )
                    break

    except (Exception, KeyboardInterrupt) as erro:
        metadata["status"] = "interrupted"
        metadata["interruption_reason"] = (
            f"{type(erro).__name__}: {erro}"
        )
        print("[ERRO]", metadata["interruption_reason"], flush=True)

    finally:
        if dispositivo is not None:
            dispositivo.close()

        concluidos = sum(
            1 for resultado in resultados
            if resultado["completed"]
        )

        total = len(resultados)

        resumo = {
            "experiment": "PT-16",
            "simulated": simulado,
            "cases_expected": 36,
            "cases_recorded": total,
            "cases_completed": concluidos,
            "cases_incomplete": total - concluidos,
            "source_sha256": sha,
            "finished_at_utc": agora(),
        }

        if metadata["status"] == "running":
            metadata["status"] = (
                "completed"
                if total == 36 and concluidos == 36
                else "incomplete"
            )

        metadata["finished_at_utc"] = agora()

        gravar_json(diretorio / "resumo.json", resumo)
        gravar_json(diretorio / "metadata.json", metadata)

        print("\n" + "=" * 78, flush=True)
        print("RESUMO FINAL", flush=True)
        print("Diretorio:", diretorio, flush=True)
        print("Status:", metadata["status"], flush=True)
        print("Casos registrados:", total, flush=True)
        print("Casos concluidos:", concluidos, flush=True)
        print("Simulacao:", simulado, flush=True)
        print("=" * 78, flush=True)

    return 0 if metadata["status"] == "completed" else 1


def main():
    parser = argparse.ArgumentParser(
        description="Coletor experimental Needle 2 no ESP32-S3"
    )

    grupo = parser.add_mutually_exclusive_group(required=True)

    grupo.add_argument(
        "--verificar",
        dest="modo",
        action="store_const",
        const="verificar",
    )

    grupo.add_argument(
        "--simular",
        dest="modo",
        action="store_const",
        const="simular",
    )

    grupo.add_argument(
        "--executar",
        dest="modo",
        action="store_const",
        const="executar",
    )

    parser.add_argument(
        "--porta",
        default="/dev/ttyACM0",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=TIMEOUT_PADRAO,
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout deve ser positivo")

    return executar(args)


if __name__ == "__main__":
    sys.exit(main())
