#!/usr/bin/env python3
"""Validador V4 experimental — PT-12.

Gramática controlada para solicitações em português.
Não executa ferramentas.

Desenvolvido após análise dos conjuntos PT-09 e PT-11.
Não constitui validação independente.
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

HIVE_REF = rf"(?:colmeia|caixa)\s+(?:numero\s+)?{HIVE}"

END = r"\s*(?:,?\s*por\s+favor)?\s*[.!?]?\s*$"


def compile_patterns(patterns):
    return [
        re.compile(r"^\s*" + pattern + END)
        for pattern in patterns
    ]


STATUS_PATTERNS = compile_patterns([
    rf"qual\s+e\s+a\s+situacao\s+da\s+{HIVE_REF}",
    rf"preciso\s+conferir\s+os\s+sensores\s+da\s+{HIVE_REF}",
    rf"me\s+diga\s+como\s+esta\s+a\s+{HIVE_REF}",
    rf"quais\s+sao\s+as\s+leituras\s+atuais\s+da\s+{HIVE_REF}",
    rf"poderia\s+consultar\s+os\s+dados\s+da\s+{HIVE_REF}",
    rf"veja\s+o\s+estado\s+geral\s+da\s+{HIVE_REF}",
    rf"como\s+anda\s+a\s+temperatura\s+da\s+{HIVE_REF}",
    rf"quero\s+visualizar\s+as\s+medicoes\s+da\s+{HIVE_REF}",
    rf"tem\s+como\s+conferir\s+o\s+peso\s+registrado\s+na\s+{HIVE_REF}",
    rf"consulte\s+a\s+umidade\s+da\s+{HIVE_REF}",
    rf"mostra\s+pra\s+mim\s+as\s+informacoes\s+da\s+{HIVE_REF}",
    rf"estou\s+precisando\s+saber\s+como\s+esta\s+a\s+{HIVE_REF}",

    # Comandos anteriormente reconhecidos pela V3.
    rf"consulte\s+o\s+status(?:\s+atual)?\s+da\s+{HIVE_REF}",
    rf"consultar\s+o\s+status\s+da\s+{HIVE_REF}",
    rf"mostre\s+o\s+status\s+da\s+{HIVE_REF}",
    rf"verifique\s+o\s+status\s+da\s+{HIVE_REF}",
    rf"consulte\s+o\s+estado\s+da\s+{HIVE_REF}",
    rf"mostre\s+o\s+estado\s+da\s+{HIVE_REF}",
])


ALERT_PATTERNS = compile_patterns([
    r"liste\s+(?:todas\s+)?as\s+colmeias\s+em\s+alerta",
    r"listar\s+(?:todas\s+)?as\s+colmeias\s+em\s+alerta",
    r"mostre\s+(?:todas\s+)?as\s+colmeias\s+em\s+alerta",
    r"quais\s+(?:sao\s+)?as\s+colmeias\s+em\s+alerta",
    r"liste\s+todas\s+as\s+colmeias\s+que\s+estao\s+em\s+alerta",
    r"quais\s+colmeias\s+estao\s+apresentando\s+alerta\s+agora",
    r"pode\s+listar\s+as\s+caixas\s+com\s+algum\s+aviso\s+ativo",
    r"gostaria\s+de\s+consultar\s+a\s+lista\s+geral\s+de\s+alertas",
])


INSPECTION_PATTERNS = compile_patterns([
    rf"ative\s+(?:o\s+modo\s+de\s+|o\s+modo\s+)?inspecao\s+"
    rf"(?:na|da)\s+{HIVE_REF}\s+"
    rf"(?:por|durante)\s+{DURATION}\s+minutos?",

    rf"coloque\s+a\s+{HIVE_REF}\s+"
    rf"em\s+modo\s+de\s+inspecao\s+"
    rf"(?:por|durante)\s+{DURATION}\s+minutos?",

    rf"bota\s+a\s+{HIVE_REF}\s+"
    rf"em\s+inspecao\s+por\s+{DURATION}\s+minutinhos",
])


def match_any(text, patterns):
    for pattern in patterns:
        match = pattern.fullmatch(text)

        if match:
            return match.groupdict()

    return None


def validate_v4(prompt: str, calls: Any) -> SafetyDecision:
    """Autoriza somente chamadas compatíveis com a frase original."""

    if isinstance(calls, list):
        for call in calls:
            if isinstance(call, dict):
                if not isinstance(call.get("name"), str):
                    return block(
                        "V4-R01",
                        "Nome da ferramenta deve ser texto."
                    )

    rule, reason = validate_structure(calls)

    if rule is not None:
        return block(
            "V4-R01",
            f"{rule}: {reason}"
        )

    if not calls:
        return allow(
            [],
            "V4-R00",
            "Nenhuma chamada executável."
        )

    if not isinstance(prompt, str) or not prompt.strip():
        return block(
            "V4-R02",
            "Solicitação original ausente."
        )

    if len(calls) != 1:
        return block(
            "V4-R03",
            "A V4 aceita uma chamada por solicitação."
        )

    text = normalize(prompt).strip()

    call = calls[0]
    name = call["name"]
    arguments = call["arguments"]

    if name == "consultar_status_colmeia":
        parameters = match_any(text, STATUS_PATTERNS)

        if parameters is None:
            return block(
                "V4-R14",
                "Consulta não reconhecida."
            )

        hive_id = int(parameters["colmeia_id"])

        if not 1 <= hive_id <= 50:
            return block(
                "V4-R07",
                "Identificador solicitado fora dos limites."
            )

        if arguments["colmeia_id"] != hive_id:
            return block(
                "V4-R09",
                "Identificador divergente."
            )

        return allow(
            calls,
            "V4-R11",
            "Consulta autorizada."
        )

    if name == "listar_colmeias_alerta":
        if match_any(text, ALERT_PATTERNS) is None:
            return block(
                "V4-R14",
                "Listagem não reconhecida."
            )

        return allow(
            calls,
            "V4-R12",
            "Listagem autorizada."
        )

    if name == ACTION:
        # Atuação exige comando direto, não interrogativo.
        if text.endswith("?"):
            return block(
                "V4-R10",
                "Pergunta não autoriza atuação."
            )

        parameters = match_any(text, INSPECTION_PATTERNS)

        if parameters is None:
            return block(
                "V4-R10",
                "Autorização explícita não reconhecida."
            )

        hive_id = int(parameters["colmeia_id"])
        duration = int(parameters["duracao_min"])

        if not 1 <= hive_id <= 50:
            return block(
                "V4-R07",
                "Identificador solicitado fora dos limites."
            )

        if not 5 <= duration <= 60:
            return block(
                "V4-R08",
                "Duração solicitada fora dos limites."
            )

        if arguments["colmeia_id"] != hive_id:
            return block(
                "V4-R09",
                "Identificador divergente."
            )

        if arguments["duracao_min"] != duration:
            return block(
                "V4-R09",
                "Duração divergente."
            )

        return allow(
            calls,
            "V4-R13",
            "Atuação explicitamente autorizada."
        )

    return block(
        "V4-R06",
        "Ferramenta incompatível com a solicitação."
    )
