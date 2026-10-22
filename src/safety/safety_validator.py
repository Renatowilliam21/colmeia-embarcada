#!/usr/bin/env python3
"""Validador determinístico de chamadas de ferramentas do Needle 2.

Implementação conservadora, sem execução de ferramentas.
"""

import re
import unicodedata
from dataclasses import dataclass
from typing import Any


TOOLS = {
    "consultar_status_colmeia": {
        "colmeia_id": (1, 50),
    },
    "listar_colmeias_alerta": {},
    "ativar_modo_inspecao": {
        "colmeia_id": (1, 50),
        "duracao_min": (5, 60),
    },
}

ACTION = "ativar_modo_inspecao"


@dataclass(frozen=True)
class SafetyDecision:
    authorized: bool
    rule: str
    reason: str
    calls: list

    def as_dict(self):
        return {
            "authorized": self.authorized,
            "decision": "AUTORIZAR" if self.authorized else "BLOQUEAR",
            "rule": self.rule,
            "reason": self.reason,
            "calls": self.calls,
        }


def allow(calls, rule, reason):
    return SafetyDecision(True, rule, reason, calls)


def block(rule, reason):
    return SafetyDecision(False, rule, reason, [])


def normalize(text):
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(
        char for char in text
        if not unicodedata.combining(char)
    )


def has_blocking_language(text):
    """Detecta construções sem autorização inequívoca.

    Política conservadora baseada nas auditorias PT-10.4.1
    e PT-10.4.2.

    Esta função não constitui um analisador semântico completo.
    """

    patterns = [
        # Negações e proibições.
        r"\bnao\b",
        r"\bnunca\b",
        r"\bjamais\b",
        r"\bevite\b",
        r"\bevitar\b",
        r"\bimpeca\b",
        r"\bproibido\b",
        r"\bsem\b",

        # Condições, hipóteses e dependências.
        r"\bse\b",
        r"\bcaso\b",
        r"\btalvez\b",
        r"\bseria\b",
        r"\bpoderia\b",
        r"\bdeveria\b",
        r"\bquando\b",
        r"\bantes\s+de\b",
        r"\bdepois\s+de\b",
        r"\bsomente\s+depois\b",
        r"\bapos\b",
        r"\bconfirmacao\b",
        r"\bconfirmar\b",
        r"\bautorizar\s+depois\b",

        # Perguntas sobre capacidade.
        r"\b(?:voce|vc)\s+(?:pode|consegue|sabe)\b",
        r"\b(?:e|seria)\s+possivel\b",
        r"\btem\s+como\b",

        # Pedidos de explicação, não de execução.
        r"\bexplique\b",
        r"\bexplicar\b",
        r"\bensine\b",
        r"\bensinar\b",
        r"\bcomo\s+(?:ativar|consultar|listar)\b",
        r"\bquero\s+saber\b",

        # Operações adicionais não suportadas.
        r"\be\s+(?:registre|registrar|cadastre|cadastrar|"
        r"exclua|excluir|apague|apagar|envie|enviar|"
        r"altere|alterar|configure|configurar|"
        r"desligue|desligar|ligue|ligar|"
        r"ignore|ignorar|reinicie|reiniciar|"
        r"remova|remover|bloqueie|bloquear)\b",
    ]

    return any(re.search(pattern, text) for pattern in patterns)

def validate_structure(calls):
    if not isinstance(calls, list):
        return "R01", "Resposta não interpretável."

    actions = 0

    for index, call in enumerate(calls):
        if not isinstance(call, dict):
            return "R03", f"Chamada {index} não é um objeto."

        if set(call) != {"name", "arguments"}:
            return "R03", f"Estrutura inválida na chamada {index}."

        name = call["name"]
        arguments = call["arguments"]

        if name not in TOOLS:
            return "R02", f"Ferramenta desconhecida: {name}."

        if not isinstance(arguments, dict):
            return "R03", "Argumentos não são um objeto."

        rules = TOOLS[name]

        if set(arguments) != set(rules):
            return "R03", "Parâmetros ausentes ou adicionais."

        for parameter, (minimum, maximum) in rules.items():
            value = arguments[parameter]

            if type(value) is not int:
                return "R03", f"Tipo inválido: {parameter}."

            if not minimum <= value <= maximum:
                rule = (
                    "R05" if parameter == "duracao_min"
                    else "R04"
                )
                return rule, f"Valor fora dos limites: {parameter}."

        if name == ACTION:
            actions += 1

    if actions > 1:
        return "R10", "Múltiplas ações de controle."

    return None, None


def extract_hive_ids(text):
    return [
        int(value)
        for value in re.findall(
            r"\bcolmeia\s*(?:n(?:umero|o)?\.?\s*)?(\d+)\b",
            text
        )
    ]


def extract_duration(text):
    values = re.findall(
        r"\b(?:por|durante)\s+(\d+)\s*minutos?\b",
        text
    )

    return [int(value) for value in values]


def detect_intent(text):
    """Reconhece apenas intenções suficientemente explícitas."""

    inspection = bool(re.search(
        r"\b(?:ative|ativar|ativa|coloque|colocar)\b",
        text
    )) and bool(re.search(
        r"\b(?:inspecao|modo\s+inspecao)\b",
        text
    ))

    status = bool(re.search(
        r"\b(?:status|estado|situacao)\b",
        text
    )) and bool(re.search(
        r"\b(?:consulte|consultar|mostre|mostrar|"
        r"verifique|verificar|informe|informar)\b",
        text
    ))

    alerts = bool(re.search(
        r"\b(?:liste|listar|mostre|mostrar|"
        r"quais|exiba|exibir)\b",
        text
    )) and bool(re.search(
        r"\b(?:alerta|alertas)\b",
        text
    ))

    detected = []

    if inspection:
        detected.append(ACTION)

    if status:
        detected.append("consultar_status_colmeia")

    if alerts:
        detected.append("listar_colmeias_alerta")

    return detected


def validate(prompt: str, calls: Any) -> SafetyDecision:
    """Autoriza apenas chamadas reconhecidas e coerentes.

    Não executa nenhuma ferramenta.
    """

    error_rule, error_reason = validate_structure(calls)

    if error_rule:
        return block(error_rule, error_reason)

    if not calls:
        return allow([], "R13", "Nenhuma chamada executável.")

    if not isinstance(prompt, str) or not prompt.strip():
        return block("R12", "Frase original ausente.")

    text = normalize(prompt)

    if has_blocking_language(text):
        return block(
            "R12",
            "Negação, condição ou intenção não inequívoca."
        )

    intents = detect_intent(text)

    if len(intents) != 1:
        return block(
            "R12",
            "Intenção ausente, múltipla ou ambígua."
        )

    intent = intents[0]

    if any(call["name"] != intent for call in calls):
        return block(
            "R09",
            "Ferramenta produzida não corresponde à intenção."
        )

    ids = extract_hive_ids(text)

    if intent == "listar_colmeias_alerta":
        if len(calls) != 1:
            return block(
                "R12",
                "Quantidade de chamadas não autorizada."
            )

        if ids:
            return block(
                "R12",
                "Identificador incompatível com listagem geral."
            )

        return allow(
            calls,
            "R13",
            "Listagem de alertas explicitamente solicitada."
        )

    if len(ids) != 1:
        return block(
            "R06",
            "Identificador da colmeia ausente ou ambíguo."
        )

    hive_id = ids[0]

    if not 1 <= hive_id <= 50:
        return block(
            "R04",
            "Identificador solicitado fora dos limites."
        )

    if len(calls) != 1:
        return block(
            "R12",
            "Quantidade de chamadas não autorizada."
        )

    if calls[0]["arguments"]["colmeia_id"] != hive_id:
        return block(
            "R08",
            "Identificador produzido difere do solicitado."
        )

    if intent == "consultar_status_colmeia":
        return allow(
            calls,
            "R13",
            "Consulta de status explicitamente autorizada."
        )

    if intent == ACTION:
        durations = extract_duration(text)

        if len(durations) != 1:
            return block(
                "R07",
                "Duração ausente ou ambígua."
            )

        duration = durations[0]

        if not 5 <= duration <= 60:
            return block(
                "R05",
                "Duração solicitada fora dos limites."
            )

        if calls[0]["arguments"]["duracao_min"] != duration:
            return block(
                "R08",
                "Duração produzida difere da solicitada."
            )

        return allow(
            calls,
            "R14",
            "Inspeção explícita com parâmetros válidos."
        )

    return block(
        "R11",
        "Operação não autorizada."
    )
