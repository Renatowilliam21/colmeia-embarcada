#!/usr/bin/env python3
"""Política conservadora de autorização por correspondência integral.

Não executa ferramentas e não modifica chamadas do modelo.
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
        re.compile(r"^\s*" + pattern + r"\s*[.!]?\s*$")
        for pattern in patterns
    ]


STATUS_PATTERNS = compile_patterns([
    rf"consulte\s+o\s+status\s+da\s+colmeia\s+{HIVE}",
    rf"consultar\s+o\s+status\s+da\s+colmeia\s+{HIVE}",
    rf"mostre\s+o\s+status\s+da\s+colmeia\s+{HIVE}",
    rf"verifique\s+o\s+status\s+da\s+colmeia\s+{HIVE}",
    rf"consulte\s+o\s+estado\s+da\s+colmeia\s+{HIVE}",
    rf"mostre\s+o\s+estado\s+da\s+colmeia\s+{HIVE}",
])

ALERT_PATTERNS = compile_patterns([
    r"liste\s+(?:todas\s+)?as\s+colmeias\s+em\s+alerta",
    r"listar\s+(?:todas\s+)?as\s+colmeias\s+em\s+alerta",
    r"mostre\s+(?:todas\s+)?as\s+colmeias\s+em\s+alerta",
    r"quais\s+(?:sao\s+)?as\s+colmeias\s+em\s+alerta",
])

INSPECTION_PATTERNS = compile_patterns([
    rf"ative\s+(?:o\s+modo\s+)?inspecao\s+"
    rf"(?:na|da)\s+colmeia\s+{HIVE}\s+"
    rf"por\s+{DURATION}\s+minutos?",

    rf"ative\s+o\s+modo\s+inspecao\s+"
    rf"(?:na|da)\s+colmeia\s+{HIVE}\s+"
    rf"durante\s+{DURATION}\s+minutos?",

    rf"ativar\s+(?:o\s+modo\s+)?inspecao\s+"
    rf"(?:na|da)\s+colmeia\s+{HIVE}\s+"
    rf"por\s+{DURATION}\s+minutos?",
])


def match_any(text, patterns):
    for pattern in patterns:
        match = pattern.fullmatch(text)

        if match:
            return match.groupdict()

    return None


def validate_strict(prompt: str, calls: Any) -> SafetyDecision:
    """Valida chamadas com base em padrões integrais explícitos."""

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
        return block("R12", "Frase original ausente.")

    text = normalize(prompt)

    # Não aceita comandos compostos nesta versão.
    if len(calls) != 1:
        return block(
            "R12",
            "A política estrita aceita uma chamada por solicitação."
        )

    call = calls[0]
    name = call["name"]
    arguments = call["arguments"]

    if name == "consultar_status_colmeia":
        parameters = match_any(text, STATUS_PATTERNS)

        if parameters is None:
            return block(
                "R12",
                "Frase não corresponde a um comando de consulta permitido."
            )

        hive_id = int(parameters["colmeia_id"])

        if not 1 <= hive_id <= 50:
            return block("R04", "Identificador solicitado inválido.")

        if arguments["colmeia_id"] != hive_id:
            return block("R08", "Identificador divergente.")

        return allow(
            calls,
            "R13",
            "Consulta autorizada por correspondência integral."
        )

    if name == "listar_colmeias_alerta":
        if match_any(text, ALERT_PATTERNS) is None:
            return block(
                "R12",
                "Frase não corresponde a uma listagem permitida."
            )

        return allow(
            calls,
            "R13",
            "Listagem autorizada por correspondência integral."
        )

    if name == ACTION:
        parameters = match_any(text, INSPECTION_PATTERNS)

        if parameters is None:
            return block(
                "R12",
                "Frase não corresponde a uma inspeção permitida."
            )

        hive_id = int(parameters["colmeia_id"])
        duration = int(parameters["duracao_min"])

        if not 1 <= hive_id <= 50:
            return block("R04", "Identificador solicitado inválido.")

        if not 5 <= duration <= 60:
            return block("R05", "Duração solicitada inválida.")

        if arguments["colmeia_id"] != hive_id:
            return block("R08", "Identificador divergente.")

        if arguments["duracao_min"] != duration:
            return block("R08", "Duração divergente.")

        return allow(
            calls,
            "R14",
            "Inspeção autorizada por correspondência integral."
        )

    return block("R11", "Operação não autorizada.")
