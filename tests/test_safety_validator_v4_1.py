#!/usr/bin/env python3
"""Testes iniciais da V4.1."""

import unittest

from src.safety.safety_validator_v4 import validate_v4
from src.safety.safety_validator_v4_1 import validate_v4_1


class TestSafetyValidatorV41(unittest.TestCase):

    def test_nova_consulta(self):
        result = validate_v4_1(
            "Cheque o monitoramento da colmeia 30.",
            [{
                "name": "consultar_status_colmeia",
                "arguments": {"colmeia_id": 30},
            }],
        )
        self.assertTrue(result.authorized)

    def test_nova_listagem(self):
        result = validate_v4_1(
            "Liste as colmeias que o sistema marcou com alerta.",
            [{
                "name": "listar_colmeias_alerta",
                "arguments": {},
            }],
        )
        self.assertTrue(result.authorized)

    def test_identificador_divergente(self):
        result = validate_v4_1(
            "Cheque o monitoramento da colmeia 30.",
            [{
                "name": "consultar_status_colmeia",
                "arguments": {"colmeia_id": 31},
            }],
        )
        self.assertFalse(result.authorized)

    def test_negacao(self):
        result = validate_v4_1(
            "Não cheque o monitoramento da colmeia 30.",
            [{
                "name": "consultar_status_colmeia",
                "arguments": {"colmeia_id": 30},
            }],
        )
        self.assertFalse(result.authorized)

    def test_condicional(self):
        result = validate_v4_1(
            "Se necessário, cheque o monitoramento da colmeia 30.",
            [{
                "name": "consultar_status_colmeia",
                "arguments": {"colmeia_id": 30},
            }],
        )
        self.assertFalse(result.authorized)

    def test_ferramenta_divergente(self):
        result = validate_v4_1(
            "Liste as colmeias que o sistema marcou com alerta.",
            [{
                "name": "consultar_status_colmeia",
                "arguments": {"colmeia_id": 3},
            }],
        )
        self.assertFalse(result.authorized)

    def test_atuacao_nao_ampliada(self):
        prompt = (
            "Ligue o modo de inspeção da colmeia 7 "
            "por 5 minutos."
        )
        calls = [{
            "name": "ativar_modo_inspecao",
            "arguments": {
                "colmeia_id": 7,
                "duracao_min": 5,
            },
        }]

        old = validate_v4(prompt, calls)
        new = validate_v4_1(prompt, calls)

        self.assertEqual(old.authorized, new.authorized)
        self.assertEqual(old.calls, new.calls)

    def test_pergunta_sobre_atuacao(self):
        result = validate_v4_1(
            "Poderia ativar a inspeção na colmeia 4 por 10 minutos?",
            [{
                "name": "ativar_modo_inspecao",
                "arguments": {
                    "colmeia_id": 4,
                    "duracao_min": 10,
                },
            }],
        )
        self.assertFalse(result.authorized)


if __name__ == "__main__":
    unittest.main()
