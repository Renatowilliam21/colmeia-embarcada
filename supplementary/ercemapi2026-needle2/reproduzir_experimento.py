#!/usr/bin/env python3
"""Verificacao e preparacao de reproducao do experimento Needle 2.

Modos verify e dry-run nao executam inferencias.
O modo run realiza uma nova rodada somente quando solicitado explicitamente.
"""

import argparse
import hashlib
from datetime import datetime, timezone
import json
import sys
from pathlib import Path


PACOTE = Path(__file__).resolve().parent
REPOSITORIO = PACOTE.parents[1]

DATASET = PACOTE / "artefatos/dataset/dataset_original_36_casos.json"
SCHEMA = PACOTE / "artefatos/schema/schema_historico_original.json"
METADATA = PACOTE / "artefatos/execucao/metadata_original.json"
RAW = PACOTE / "artefatos/execucao/raw_results_original.jsonl"
AVALIACAO = PACOTE / "artefatos/avaliacao/pt05_resultados_detalhados.json"
MANIFESTO = PACOTE / "MANIFEST_SHA256.txt"

ENGINE = REPOSITORIO / "external/needle-2-esp32"
BINARIO = ENGINE / "build-host/nd_dump"
MODELO = ENGINE / "model/needle2.cact"

HASH_MODELO = (
    "b43aabfcaf1a6db6acf488076eab71d823c08697c7af4521fc1d174b60ede5ba"
)
HASH_BINARIO = (
    "7318a5784e0bb91487a2016ebfae7bd6aec2a6692ecb1a308a8bb3c2996577a4"
)
HASH_SCHEMA = (
    "aea810e7afdfde235393b2b9765d8290622f25790efc3d9951a0dd562c6440f2"
)
HASH_DATASET = (
    "44848860ea06a7b8cdd297316d497d641d43d69185962bb3913b9e16d7b5be8e"
)
COMMIT_ENGINE = "61cafad7014a5664bb3ffd5f0c457ce5aa6598ae"


def sha256(caminho):
    h = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def verificar_manifesto():
    erros = []
    registrados = set()

    if not MANIFESTO.is_file():
        return ["Manifesto ausente"]

    for numero, linha in enumerate(
        MANIFESTO.read_text(encoding="utf-8").splitlines(), 1
    ):
        partes = linha.split("  ", 1)

        if len(partes) != 2:
            erros.append(f"Linha {numero}: formato invalido")
            continue

        esperado, relativo = partes

        caminho_relativo = Path(relativo)

        if (
            not relativo
            or caminho_relativo.is_absolute()
            or ".." in caminho_relativo.parts
        ):
            erros.append(f"Linha {numero}: caminho invalido")
            continue

        if relativo in registrados:
            erros.append(f"Registro duplicado: {relativo}")
            continue

        registrados.add(relativo)
        caminho = PACOTE / caminho_relativo

        if not caminho.is_file():
            erros.append(f"Arquivo ausente: {relativo}")
        elif sha256(caminho) != esperado:
            erros.append(f"Hash divergente: {relativo}")

    if len(registrados) != 16:
        erros.append(
            f"Manifesto historico: esperados 16 registros, encontrados {len(registrados)}"
        )

    return erros


def verificar_ambiente():
    erros = []

    for nome, caminho, esperado in (
        ("binario", BINARIO, HASH_BINARIO),
        ("modelo", MODELO, HASH_MODELO),
        ("schema", SCHEMA, HASH_SCHEMA),
        ("dataset", DATASET, HASH_DATASET),
    ):
        if not caminho.is_file():
            erros.append(f"{nome}: arquivo ausente")
        elif sha256(caminho) != esperado:
            erros.append(f"{nome}: SHA-256 divergente")

    return erros


def carregar_dados():
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    avaliacao = json.loads(AVALIACAO.read_text(encoding="utf-8"))

    with RAW.open(encoding="utf-8") as arquivo:
        brutos = [
            json.loads(linha)
            for linha in arquivo
            if linha.strip()
        ]

    return dataset, metadata, avaliacao, brutos


def verificar_resultados():
    erros = []

    try:
        dataset, metadata, avaliacao, brutos = carregar_dados()
    except (OSError, ValueError, TypeError) as erro:
        return [f"Falha ao carregar resultados: {erro}"]

    casos = dataset.get("casos")

    if not isinstance(casos, list) or len(casos) != 36:
        erros.append("Dataset nao contem exatamente 36 casos")
        return erros

    if len(brutos) != 36 or len(avaliacao) != 36:
        erros.append("Quantidade de resultados diferente de 36")
        return erros

    ids_dataset = [caso.get("id") for caso in casos]
    ids_brutos = [caso.get("case_id") for caso in brutos]
    ids_avaliacao = [caso.get("id") for caso in avaliacao]

    if (
        len(set(ids_dataset)) != 36
        or ids_dataset != ids_brutos
        or ids_dataset != ids_avaliacao
    ):
        erros.append("IDs ou ordenacao inconsistentes")

    valores = [caso.get("exact_match_original") for caso in avaliacao]

    acertos = sum(valor is True for valor in valores)
    falhas = sum(valor is False for valor in valores)
    indeterminados = sum(valor is None for valor in valores)

    if (acertos, falhas, indeterminados) != (13, 20, 3):
        erros.append("Metricas divergentes do registro historico")

    esperados = {
        "engine_commit": COMMIT_ENGINE,
        "model_sha256": HASH_MODELO,
        "schema_sha256": HASH_SCHEMA,
        "dataset_sha256": HASH_DATASET,
        "repetitions": 1,
        "max_new": 96,
        "think": False,
        "timeout_seconds": 300,
        "selected_cases": 36,
        "execution_environment": "Linux host",
    }

    for chave, esperado in esperados.items():
        if metadata.get(chave) != esperado:
            erros.append(f"Metadata divergente: {chave}")

    print(
        f"RESULTADOS: {acertos} acertos, {falhas} erros, "
        f"{indeterminados} indeterminados"
    )
    print(f"TAXA TOTAL: {acertos}/36 = {acertos / 36 * 100:.2f}%")
    print(f"EXACT MATCH COMPARAVEL: {acertos}/33 = {acertos / 33 * 100:.2f}%")

    return erros


def verificar():
    print("PT-14 — VERIFICACAO DOCUMENTAL")

    verificacoes = (
        ("MANIFESTO", verificar_manifesto),
        ("AMBIENTE", verificar_ambiente),
        ("RESULTADOS", verificar_resultados),
    )

    total_erros = []

    for nome, funcao in verificacoes:
        try:
            erros = funcao()
        except (OSError, ValueError, TypeError) as erro:
            erros = [str(erro)]

        if erros:
            print(f"[ERRO] {nome}")
            for erro in erros:
                print(" -", erro)
            total_erros.extend(erros)
        else:
            print(f"[OK] {nome}")

    return not total_erros


def dry_run():
    if not verificar():
        print("[ERRO] Dry-run bloqueado: verificacao falhou")
        return False

    dataset, _, _, _ = carregar_dados()

    print("\nPT-14 — DRY-RUN")
    print("Nenhuma inferencia sera executada.")

    for caso in dataset["casos"]:
        frase = caso["frase"]

        comando = [
            str(BINARIO),
            str(MODELO),
            "genp",
            str(SCHEMA),
            frase,
            "96",
            "nothink",
        ]

        print(
            f"CASO {caso['id']:02d}:",
            json.dumps(comando, ensure_ascii=False)
        )

    print("\nTOTAL: 36 comandos planejados")
    print("SCHEMA: copia historica do pacote")
    print("SAIDA: nenhuma; modo exclusivamente demonstrativo")

    return True



def executar_experimento():
    """Executa nova rodada em Linux host, sem acionar ferramentas fisicas."""
    import importlib.util
    import os
    import platform
    import subprocess
    import time
    import uuid

    if not verificar():
        print("[ERRO] Verificacao previa falhou; execucao bloqueada")
        return False

    parser_historico = PACOTE / "artefatos/scripts/parse_output.py"

    spec = importlib.util.spec_from_file_location(
        "pt14_parser_historico", parser_historico
    )

    if spec is None or spec.loader is None:
        print("[ERRO] Parser historico indisponivel")
        return False

    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)

    if not hasattr(modulo, "extract_tool_calls"):
        print("[ERRO] Funcao extract_tool_calls ausente")
        return False

    dataset, metadata_original, _, _ = carregar_dados()
    casos = dataset["casos"]

    identificador = (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "_"
        + uuid.uuid4().hex[:8]
    )

    destino_base = PACOTE / "resultados_novos"
    destino_base.mkdir(exist_ok=True)

    destino = destino_base / identificador
    destino.mkdir(exist_ok=False)

    arquivo_raw = destino / "raw_results.jsonl"
    arquivo_metadata = destino / "metadata.json"

    configuracao = {
        "tipo": "reproducao_independente",
        "historico_original": False,
        "executado_em_utc": datetime.now(timezone.utc).isoformat(),
        "execution_environment": "Linux host",
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "engine_commit_referencia": COMMIT_ENGINE,
        "binary_sha256": sha256(BINARIO),
        "model_sha256": sha256(MODELO),
        "schema_sha256": sha256(SCHEMA),
        "dataset_sha256": sha256(DATASET),
        "parser_sha256": sha256(parser_historico),
        "executor_sha256": sha256(Path(__file__)),
        "max_new": 96,
        "think": False,
        "timeout_seconds": 300,
        "repetitions": 1,
        "selected_cases": len(casos),
        "status": "em_execucao",
        "completed_cases": 0,
        "results_file": "raw_results.jsonl",
        "original_metadata_reference": metadata_original,
        "physical_tool_execution": False,
    }

    def salvar_metadata():
        temporario = arquivo_metadata.with_suffix(".json.tmp")
        temporario.write_text(
            json.dumps(configuracao, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporario, arquivo_metadata)

    salvar_metadata()

    print("=" * 78)
    print("PT-14 — REPRODUCAO EXPERIMENTAL INDEPENDENTE")
    print("Diretorio:", destino)
    print("Casos:", len(casos))
    print("Nenhuma ferramenta fisica sera acionada")
    print("=" * 78, flush=True)

    interrompido = False
    casos_com_falha = 0
    falha_interna = None

    try:
        with arquivo_raw.open("x", encoding="utf-8") as saida:
            for indice, caso in enumerate(casos, 1):
                comando = [
                    str(BINARIO),
                    str(MODELO),
                    "genp",
                    str(SCHEMA),
                    caso["frase"],
                    "96",
                    "nothink",
                ]

                inicio = time.perf_counter()
                iniciado_em = datetime.now(timezone.utc).isoformat()

                stdout = ""
                stderr = ""
                returncode = None
                erro = None

                try:
                    processo = subprocess.run(
                        comando,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=300,
                        check=False,
                    )
                    stdout = processo.stdout
                    stderr = processo.stderr
                    returncode = processo.returncode
                except subprocess.TimeoutExpired as exc:
                    erro = "timeout"
                    stdout = (
                        exc.stdout.decode("utf-8", errors="replace")
                        if isinstance(exc.stdout, bytes)
                        else (exc.stdout or "")
                    )
                    stderr = (
                        exc.stderr.decode("utf-8", errors="replace")
                        if isinstance(exc.stderr, bytes)
                        else (exc.stderr or "")
                    )
                except OSError as exc:
                    erro = f"{type(exc).__name__}: {exc}"

                tempo_ms = (time.perf_counter() - inicio) * 1000.0

                tokens = []

                for linha in stdout.splitlines():
                    if linha.startswith("TOK "):
                        tokens.append(linha[4:].replace("\\n", "\n"))

                resposta = "".join(tokens)

                chamadas = []
                erro_parse = None

                try:
                    resultado_parse = modulo.extract_tool_calls(resposta)
                    chamadas = resultado_parse["parsed_calls"]
                    erro_parse = resultado_parse["parse_error"]
                except Exception as exc:
                    chamadas = None
                    erro_parse = f"{type(exc).__name__}: {exc}"

                registro = {
                    "case_id": caso["id"],
                    "category": caso.get("categoria"),
                    "prompt": caso["frase"],
                    "repetition": 1,
                    "started_at_utc": iniciado_em,
                    "max_new": 96,
                    "think": False,
                    "timeout_seconds": 300,
                    "model_output": resposta,
                    "parsed_calls": chamadas,
                    "parse_error": erro_parse,
                    "elapsed_wall_ms": round(tempo_ms, 3),
                    "stdout_raw": stdout,
                    "stderr_raw": stderr,
                    "returncode": returncode,
                    "error": erro,
                    "confidence_events": [
                        linha for linha in stdout.splitlines()
                        if linha.startswith("CONF ")
                    ],
                    "timing_events": [
                        linha for linha in stdout.splitlines()
                        if linha.startswith("EVT ")
                    ],
                    "action_events": [
                        linha for linha in stdout.splitlines()
                        if linha.startswith("ACT ")
                    ],
                    "error_events": [
                        linha for linha in stdout.splitlines()
                        if linha.startswith("ERR ")
                    ],
                }

                if (
                    erro is not None
                    or returncode != 0
                    or erro_parse is not None
                ):
                    casos_com_falha += 1

                saida.write(
                    json.dumps(registro, ensure_ascii=False) + "\n"
                )
                saida.flush()
                os.fsync(saida.fileno())

                configuracao["completed_cases"] = indice
                salvar_metadata()

                print(
                    f"[{indice:02d}/{len(casos):02d}] "
                    f"ID={caso['id']} "
                    f"returncode={returncode} "
                    f"erro={erro} "
                    f"tempo_ms={tempo_ms:.1f}",
                    flush=True,
                )

    except KeyboardInterrupt:
        interrompido = True
        print("\n[ATENCAO] Execucao interrompida pelo usuario")

    except Exception as exc:
        falha_interna = f"{type(exc).__name__}: {exc}"
        raise

    finally:
        configuracao["cases_with_failure"] = casos_com_falha

        if falha_interna is not None:
            configuracao["status"] = "falha_interna"
            configuracao["internal_error"] = falha_interna
        elif interrompido:
            configuracao["status"] = "interrompido"
        elif configuracao["completed_cases"] != len(casos):
            configuracao["status"] = "falha_interna"
            configuracao["internal_error"] = "Processamento incompleto"
        elif casos_com_falha:
            configuracao["status"] = "concluido_com_falhas"
        else:
            configuracao["status"] = "concluido"

        configuracao["finalizado_em_utc"] = (
            datetime.now(timezone.utc).isoformat()
        )
        salvar_metadata()

    print("Resultados:", arquivo_raw)
    print("Metadados:", arquivo_metadata)

    return (
        not interrompido
        and falha_interna is None
        and configuracao["completed_cases"] == len(casos)
        and casos_com_falha == 0
    )


def main():
    parser = argparse.ArgumentParser(
        description="Reprodutibilidade do experimento Needle 2"
    )

    parser.add_argument(
        "modo",
        choices=("verify", "dry-run", "run")
    )

    args = parser.parse_args()

    if args.modo == "run":
        return 0 if executar_experimento() else 1

    if args.modo == "verify":
        return 0 if verificar() else 1

    if args.modo == "dry-run":
        return 0 if dry_run() else 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
