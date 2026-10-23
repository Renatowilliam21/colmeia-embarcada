#!/usr/bin/env python3
"""PT-12.8 — V4.1 experimental.

Ampliação controlada de comandos de leitura.
A política de atuação permanece delegada integralmente à V4.
"""

import re

from src.safety.safety_validator import (
    allow,
    normalize,
    validate_structure,
)
from src.safety.safety_validator_v4 import validate_v4


HIVE = r"(?:colmeia|caixa)\s+(?:numero\s+)?(?P<colmeia_id>\d+)"

STATUS_PATTERNS = [
    rf"cheque o monitoramento da {HIVE}",
    rf"e os dados da {HIVE},?\s*como estao",
    rf"abra a consulta da {HIVE}",
    rf"o que os sensores indicam para a {HIVE}",
    rf"pode verificar a condicao da {HIVE}",
    rf"me atualize sobre a {HIVE}",
    rf"ha alguma informacao recente da {HIVE}",
    rf"traga o estado da {HIVE}",
    rf"preciso do resumo de monitoramento da {HIVE}",
    rf"como estao peso e temperatura na {HIVE}",
    rf"veja os registros atuais da {HIVE}",
    rf"quero saber o estado da {HIVE} neste instante",
]

ALERT_PATTERNS = [
    r"quero a relacao de colmeias sinalizadas pelo monitoramento",
    r"preciso conferir todos os alertas de colmeias",
    r"liste as colmeias que o sistema marcou com alerta",
    r"tem colmeia com alerta pendente\?\s*relacione todas",
    r"traga as colmeias identificadas como em alerta",
    r"mostre a listagem atual de colmeias alertadas",
    r"quero saber quais colmeias estao com aviso no sistema",
]


def compile_patterns(patterns):
    return [
        re.compile(r"^\s*(?:" + pattern + r")\s*[.!?]?\s*$")
        for pattern in patterns
    ]


STATUS = compile_patterns(STATUS_PATTERNS)
ALERTS = compile_patterns(ALERT_PATTERNS)


def match_patterns(text, patterns):
    for pattern in patterns:
        match = pattern.fullmatch(text)
        if match:
            return match.groupdict()
    return None


def validate_v4_1(prompt, calls):
    """Retorna SafetyDecision, sem executar ferramentas."""

    original = validate_v4(prompt, calls)

    # Nunca alterar uma autorização já concedida pela V4.
    if original.authorized:
        return original

    # A V4.1 não amplia permissões de atuação.
    if not isinstance(calls, list) or len(calls) != 1:
        return original

    call = calls[0]

    if not isinstance(call, dict):
        return original

    name = call.get("name")

    if name not in (
        "consultar_status_colmeia",
        "listar_colmeias_alerta",
    ):
        return original

    # Reaplicar a validação estrutural.
    try:
        error_rule, _ = validate_structure(calls)
    except (TypeError, ValueError):
        return original

    if error_rule is not None:
        return original

    if not isinstance(prompt, str) or not prompt.strip():
        return original

    text = normalize(prompt)

    if name == "consultar_status_colmeia":
        match = match_patterns(text, STATUS)

        if match is None:
            return original

        requested_id = int(match["colmeia_id"])
        produced_id = call["arguments"]["colmeia_id"]

        if requested_id != produced_id:
            return original

        return allow(
            calls,
            "V4.1-R11",
            "Consulta de leitura reconhecida pela gramática ampliada.",
        )

    if name == "listar_colmeias_alerta":
        if match_patterns(text, ALERTS) is None:
            return original

        return allow(
            calls,
            "V4.1-R12",
            "Listagem de alertas reconhecida pela gramática ampliada.",
        )

    return original
