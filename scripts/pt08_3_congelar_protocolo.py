#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ORIGINAL = ROOT / "dataset/colmeia-needle2-dataset-teste.json"
REVISADO = ROOT / "dataset/colmeia-needle2-gabarito-revisado.json"
FINAL = ROOT / "dataset/colmeia-needle2-gabarito-final.json"
SCHEMA = ROOT / "firmware/tools/colmeia.json"
DOCUMENTO = ROOT / "docs/metodologia/pt08_3_protocolo_congelado.md"

def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def salvar_json(path, obj):
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

def main():
    dados = json.loads(REVISADO.read_text(encoding="utf-8"))
    ferramentas = json.loads(SCHEMA.read_text(encoding="utf-8"))

    mapa = {f["name"]: f for f in ferramentas}

    casos = dados["casos"]

    if len(casos) != 36:
        raise RuntimeError("Quantidade de casos diferente de 36.")

    ids = [c["id"] for c in casos]

    if len(set(ids)) != 36:
        raise RuntimeError("IDs duplicados.")

    for caso in casos:
        if caso["id"] == 20:
            caso["chamadas_esperadas_revisadas"] = []
            caso["revisao_metodologica"] = {
                "revisado": True,
                "justificativa": (
                    "Consulta histórica não suportada pelo contrato "
                    "atual da ferramenta listar_colmeias_alerta."
                ),
                "ferramenta_original": caso.get("ferramenta_esperada"),
                "argumentos_originais": caso.get("argumentos_esperados"),
            }

        if caso["id"] == 28:
            caso["observacao_validacao"] = (
                "A chamada consulta o status completo. "
                "A avaliação considera a seleção da ferramenta, "
                "não a apresentação exclusiva da temperatura."
            )

        chamadas = caso["chamadas_esperadas_revisadas"]

        if not isinstance(chamadas, list):
            raise RuntimeError(
                f"Caso {caso['id']}: chamadas não são uma lista."
            )

        for chamada in chamadas:
            if not isinstance(chamada, dict):
                raise RuntimeError("Chamada inválida.")

            nome = chamada.get("name")
            argumentos = chamada.get("arguments")

            if nome not in mapa:
                raise RuntimeError(f"Ferramenta desconhecida: {nome}")

            if not isinstance(argumentos, dict):
                raise RuntimeError("Argumentos inválidos.")

            parametros = mapa[nome]["parameters"]
            propriedades = parametros.get("properties", {})
            obrigatorios = set(parametros.get("required", []))

            if not obrigatorios.issubset(argumentos):
                raise RuntimeError(
                    f"Caso {caso['id']}: argumentos obrigatórios ausentes."
                )

            if set(argumentos) - set(propriedades):
                raise RuntimeError(
                    f"Caso {caso['id']}: argumentos desconhecidos."
                )

            for chave, valor in argumentos.items():
                regra = propriedades[chave]

                if regra.get("type") == "integer":
                    if type(valor) is not int:
                        raise RuntimeError("Tipo de argumento inválido.")

                    minimo = regra.get("minimum")
                    maximo = regra.get("maximum")

                    if minimo is not None and valor < minimo:
                        raise RuntimeError("Valor abaixo do mínimo.")

                    if maximo is not None and valor > maximo:
                        raise RuntimeError("Valor acima do máximo.")

    dados["_protocolo"] = {
        "versao": "PT-08.3-final-1",
        "status": "congelado_para_validacao_experimental",
        "dataset_original_sha256": hash_file(ORIGINAL),
        "dataset_revisado_sha256": hash_file(REVISADO),
        "schema_sha256": hash_file(SCHEMA),
        "criterio": (
            "Correspondência exata de chamadas e argumentos; "
            "abstenção quando a execução não for suficientemente "
            "determinada ou suportada pelo contrato."
        ),
        "observacao": (
            "Protocolo definido após estudo exploratório. "
            "Resultados futuros devem ser relatados separadamente."
        )
    }

    if FINAL.exists():
        atual = json.loads(FINAL.read_text(encoding="utf-8"))
        if atual != dados:
            raise RuntimeError(
                "Arquivo final já existe com conteúdo diferente. "
                "Nenhuma sobrescrita realizada."
            )
    else:
        salvar_json(FINAL, dados)

    linhas = [
        "# PT-08.3 — Protocolo experimental congelado",
        "",
        "## Integridade",
        "",
        f"- Dataset original: `{hash_file(ORIGINAL)}`",
        f"- Dataset revisado: `{hash_file(REVISADO)}`",
        f"- Dataset final: `{hash_file(FINAL)}`",
        f"- Schema: `{hash_file(SCHEMA)}`",
        "",
        "## Decisões metodológicas",
        "",
        "- Os 36 casos foram revisados semanticamente.",
        "- Os casos 17, 18, 19, 22, 25 e 27 exigem abstenção.",
        "- O caso 23 exige duas consultas independentes.",
        "- O caso 20 exige abstenção por ausência de consulta histórica.",
        "- O caso 28 mantém consulta de status, com ressalva "
        "sobre seleção de atributos.",
        "- Comandos fora do escopo exigem abstenção.",
        "",
        "## Limitações",
        "",
        "O protocolo foi estabelecido após uma rodada exploratória.",
        "As inferências posteriores não constituem um conjunto de teste "
        "independente, pois reutilizam os mesmos 36 comandos.",
        "",
        "A lista vazia representa ausência de chamada executável, "
        "não uma solicitação de esclarecimento ao usuário.",
        "",
        "A validade estrutural de uma chamada não comprova "
        "segurança operacional.",
        "",
    ]

    DOCUMENTO.write_text("\n".join(linhas), encoding="utf-8")

    print("=" * 70)
    print("PT-08.3 — CONGELAMENTO DO PROTOCOLO")
    print("=" * 70)
    print("Casos:", len(casos))
    print("Dataset final:", FINAL.relative_to(ROOT))
    print("SHA-256 final:", hash_file(FINAL))
    print("Schema SHA-256:", hash_file(SCHEMA))
    print("Documento:", DOCUMENTO.relative_to(ROOT))
    print("[OK] Validação estrutural concluída.")
    print("[OK] Protocolo final registrado.")

if __name__ == "__main__":
    main()
