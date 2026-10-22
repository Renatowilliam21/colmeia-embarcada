#!/usr/bin/env python3
"""Validador V3: autorização por gramática controlada.

Reconhece comandos diretos e construções coloquiais específicas.
A correspondência é integral, sem execução de ferramentas.

Esta implementação foi desenvolvida após análise dos dados
PT-09/PT-10 e não constitui validação independente.
"""

import re
from typing import Any

from src.safety.safety_validator import (
    ACTION,
    SafetyDecision,
    allow,
    block,
    normalize,
    validate_structure,
)


HIVE = r"(?P<colmeia_id>\d+)"
DURATION = r"(?P<duracao_min>\d+)"


def compile_patterns(patterns):
    return [
        re.compile(r"^\s*" + pattern + r"\s*[.!?]?\s*$")
        for pattern in patterns
    ]


STATUS_PATTERNS = compile_patterns([
    # Comandos diretos.
    rf"consulte\s+o\s+status(?:\s+atual)?\s+da\s+colmeia\s+{HIVE}",
    rf"consultar\s+o\s+status\s+da\s+colmeia\s+{HIVE}",
    rf"mostre\s+o\s+status\s+da\s+colmeia\s+{HIVE}",
    rf"verifique\s+o\s+status\s+da\s+colmeia\s+{HIVE}",
    rf"consulte\s+o\s+estado\s+da\s+colmeia\s+{HIVE}",
    rf"mostre\s+o\s+estado\s+da\s+colmeia\s+{HIVE}",

    # Consulta de sensores.
    rf"mostre\s+peso,\s*temperatura\s+e\s+umidade\s+da\s+colmeia\s+{HIVE}",

    # Construções coloquiais.
    rf"queria\s+saber\s+a\s+situacao\s+da\s+colmeia\s+{HIVE}",
    rf"como\s+e\s+que\s+ta\s+a\s+colmeia\s+{HIVE}",
    rf"da\s+uma\s+conferida\s+nos\s+dados\s+da\s+colmeia\s+{HIVE}",
])


ALERT_PATTERNS = compile_patterns([
    r"liste\s+(?:todas\s+)?as\s+colmeias\s+em\s+alerta",
    r"listar\s+(?:todas\s+)?as\s+colmeias\s+em\s+alerta",
    r"mostre\s+(?:todas\s+)?as\s+colmeias\s+em\s+alerta",
    r"quais\s+(?:sao\s+)?as\s+colmeias\s+em\s+alerta",
    r"liste\s+todas\s+as\s+colmeias\s+que\s+estao\s+em\s+alerta",
])


INSPECTION_PATTERNS = compile_patterns([
    # Comandos diretos.
    rf"ative\s+(?:o\s+modo\s+)?inspecao\s+"
    rf"(?:na|da)\s+colmeia\s+{HIVE}\s+"
    rf"(?:por|durante)\s+{DURATION}\s+minutos?",

    rf"ativar\s+(?:o\s+modo\s+)?inspecao\s+"
    rf"(?:na|da)\s+colmeia\s+{HIVE}\s+"
    rf"(?:por|durante)\s+{DURATION}\s+minutos?",

    # Comando coloquial.
    rf"bota\s+a\s+colmeia\s+{HIVE}\s+"
    rf"em\s+inspecao\s+por\s+{DURATION}\s+minutinhos",
])


def match_any(text, patterns):
    for pattern in patterns:
        match = pattern.fullmatch(text)

        if match:
            return match.groupdict()

    return None


def validate_v3(prompt: str, calls: Any) -> SafetyDecision:
    """Autoriza somente chamadas correspondentes à frase integral."""

    # Proteção adicional contra nomes de ferramentas
    # não textuais, que podem causar TypeError na V1.
    if isinstance(calls, list):
        for call in calls:
            if isinstance(call, dict):
                name = call.get("name")
                if not isinstance(name, str):
                    return block(
                        "R03",
                        "Nome da ferramenta deve ser texto."
                    )

    rule, reason = validate_structure(calls)

    if rule is not None:
        return block(rule, reason)

    if not calls:
        return allow(
            [],
            "R13",
            "Nenhuma chamada executável."
        )

    if not isinstance(prompt, str) or not prompt.strip():
        return block(
            "R12",
            "Solicitação original ausente."
        )

    if len(calls) != 1:
        return block(
            "R12",
            "A V3 aceita uma chamada por solicitação."
        )

    text = normalize(prompt)

    call = calls[0]
    name = call["name"]
    arguments = call["arguments"]

    if name == "consultar_status_colmeia":
        parameters = match_any(text, STATUS_PATTERNS)

        if parameters is None:
            return block(
                "R12",
                "Consulta não reconhecida pela gramática."
            )

        hive_id = int(parameters["colmeia_id"])

        if not 1 <= hive_id <= 50:
            return block(
                "R04",
                "Identificador solicitado fora dos limites."
            )

        if arguments["colmeia_id"] != hive_id:
            return block(
                "R08",
                "Identificador divergente."
            )

        return allow(
            calls,
            "R13",
            "Consulta autorizada pela gramática V3."
        )

    if name == "listar_colmeias_alerta":
        if match_any(text, ALERT_PATTERNS) is None:
            return block(
                "R12",
                "Listagem não reconhecida pela gramática."
            )

        return allow(
            calls,
            "R13",
            "Listagem autorizada pela gramática V3."
        )

    if name == ACTION:
        # Perguntas não constituem autorização explícita
        # para uma operação que altera o estado do sistema.
        if text.rstrip().endswith("?"):
            return block(
                "R12",
                "Pergunta não autoriza operação de atuação."
            )

        parameters = match_any(text, INSPECTION_PATTERNS)

        if parameters is None:
            return block(
                "R12",
                "Inspeção não reconhecida pela gramática."
            )

        hive_id = int(parameters["colmeia_id"])
        duration = int(parameters["duracao_min"])

        if not 1 <= hive_id <= 50:
            return block(
                "R04",
                "Identificador solicitado fora dos limites."
            )

        if not 5 <= duration <= 60:
            return block(
                "R05",
                "Duração solicitada fora dos limites."
            )

        if arguments["colmeia_id"] != hive_id:
            return block(
                "R08",
                "Identificador divergente."
            )

        if arguments["duracao_min"] != duration:
            return block(
                "R08",
                "Duração divergente."
            )

        return allow(
            calls,
            "R14",
            "Inspeção autorizada pela gramática V3."
        )

    return block(
        "R11",
        "Ferramenta não autorizada."
    )
