#!/usr/bin/env python3
"""PT-12.8.4 — Validador V4.2 experimental.

Ampliação controlada da gramática de atuação.
Não executa ferramentas nem controla hardware.
"""

import re

from src.safety.safety_validator import (
    allow,
    normalize,
    validate_structure,
)

from src.safety.safety_validator_v4_1 import validate_v4_1


HIVE = r"(?:colmeia|caixa)\s+(?:numero\s+)?(?P<colmeia_id>\d+)"
DURATION = r"(?P<duracao_min>\d+)"

# Apenas construções de atuação previamente delimitadas.
INSPECTION_PATTERNS = [
    rf"ative a inspecao na {HIVE} durante {DURATION} minutos",
    rf"ligue o modo de inspecao da {HIVE} por {DURATION} minutos",
    rf"habilite o modo de inspecao da {HIVE} durante {DURATION} minutos",
    rf"acione a inspecao da {HIVE} e mantenha por {DURATION} minutos",
    rf"inicie o modo de inspecao por {DURATION} minutos na {HIVE}",
    rf"ativar modo de inspecao:\s*{HIVE},\s*duracao {DURATION} minutos",
    rf"acione o modo de inspecao por {DURATION} minutos na {HIVE}",
    rf"faca a ativacao da inspecao da {HIVE} por {DURATION} minutos",
    rf"ligue a inspecao temporaria da {HIVE} por {DURATION} minutos",
    rf"habilitar inspecao da {HIVE} por {DURATION} minutos",
    rf"inicie imediatamente o modo de inspecao na {HIVE} por {DURATION} minutos",
]

PATTERNS = [
    re.compile(r"^\s*(?:" + pattern + r")\s*[.!]?\s*$")
    for pattern in INSPECTION_PATTERNS
]


def validate_v4_2(prompt, calls):
    """Avalia chamadas, sem executá-las."""

    original = validate_v4_1(prompt, calls)

    if original.authorized:
        return original

    if not isinstance(calls, list) or len(calls) != 1:
        return original

    call = calls[0]

    if not isinstance(call, dict):
        return original

    if call.get("name") != "ativar_modo_inspecao":
        return original

    try:
        rule, _ = validate_structure(calls)
    except (TypeError, ValueError):
        return original

    if rule is not None:
        return original

    if not isinstance(prompt, str) or not prompt.strip():
        return original

    text = normalize(prompt)

    # Uma pergunta não constitui autorização de atuação.
    if text.rstrip().endswith("?"):
        return original

    for pattern in PATTERNS:
        match = pattern.fullmatch(text)

        if match is None:
            continue

        requested_id = int(match.group("colmeia_id"))
        requested_duration = int(match.group("duracao_min"))

        arguments = call["arguments"]

        if arguments["colmeia_id"] != requested_id:
            return original

        if arguments["duracao_min"] != requested_duration:
            return original

        return allow(
            calls,
            "V4.2-R13",
            "Comando explícito de inspeção reconhecido.",
        )

    return original
