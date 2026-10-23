#!/usr/bin/env python3
"""Testes iniciais do validador V4."""

import unittest

from src.safety.safety_validator_v4 import validate_v4


class TestSafetyValidatorV4(unittest.TestCase):

    def test_consulta_interrogativa(self):
        decision = validate_v4(
            "Qual é a situação da colmeia 3?",
            [{
                "name": "consultar_status_colmeia",
                "arguments": {"colmeia_id": 3},
            }],
        )
        self.assertTrue(decision.authorized)

    def test_consulta_indireta(self):
        decision = validate_v4(
            "Preciso conferir os sensores da caixa 17.",
            [{
                "name": "consultar_status_colmeia",
                "arguments": {"colmeia_id": 17},
            }],
        )
        self.assertTrue(decision.authorized)

    def test_listagem(self):
        decision = validate_v4(
            "Quais colmeias estão apresentando alerta agora?",
            [{
                "name": "listar_colmeias_alerta",
                "arguments": {},
            }],
        )
        self.assertTrue(decision.authorized)

    def test_inspecao_explicita(self):
        decision = validate_v4(
            "Ative o modo de inspeção na colmeia 4 durante 10 minutos.",
            [{
                "name": "ativar_modo_inspecao",
                "arguments": {
                    "colmeia_id": 4,
                    "duracao_min": 10,
                },
            }],
        )
        self.assertTrue(decision.authorized)

    def test_pergunta_sobre_atuacao(self):
        decision = validate_v4(
            "Poderia ativar a inspeção na colmeia 4 por 10 minutos?",
            [{
                "name": "ativar_modo_inspecao",
                "arguments": {
                    "colmeia_id": 4,
                    "duracao_min": 10,
                },
            }],
        )
        self.assertFalse(decision.authorized)

    def test_parametro_divergente(self):
        decision = validate_v4(
            "Ative o modo de inspeção na colmeia 4 durante 10 minutos.",
            [{
                "name": "ativar_modo_inspecao",
                "arguments": {
                    "colmeia_id": 5,
                    "duracao_min": 10,
                },
            }],
        )
        self.assertFalse(decision.authorized)

    def test_negacao(self):
        decision = validate_v4(
            "Não ative o modo de inspeção na colmeia 4 por 10 minutos.",
            [{
                "name": "ativar_modo_inspecao",
                "arguments": {
                    "colmeia_id": 4,
                    "duracao_min": 10,
                },
            }],
        )
        self.assertFalse(decision.authorized)

    def test_condicional(self):
        decision = validate_v4(
            "Se necessário, ative o modo de inspeção na colmeia 4 por 10 minutos.",
            [{
                "name": "ativar_modo_inspecao",
                "arguments": {
                    "colmeia_id": 4,
                    "duracao_min": 10,
                },
            }],
        )
        self.assertFalse(decision.authorized)

    def test_id_invalido(self):
        decision = validate_v4(
            "Ative o modo de inspeção na colmeia 0 por 10 minutos.",
            [{
                "name": "ativar_modo_inspecao",
                "arguments": {
                    "colmeia_id": 0,
                    "duracao_min": 10,
                },
            }],
        )
        self.assertFalse(decision.authorized)

    def test_duracao_invalida(self):
        decision = validate_v4(
            "Ative o modo de inspeção na colmeia 4 por 0 minutos.",
            [{
                "name": "ativar_modo_inspecao",
                "arguments": {
                    "colmeia_id": 4,
                    "duracao_min": 0,
                },
            }],
        )
        self.assertFalse(decision.authorized)

    def test_chamada_vazia(self):
        decision = validate_v4(
            "Não ative nenhuma inspeção.",
            [],
        )
        self.assertTrue(decision.authorized)
        self.assertEqual(decision.calls, [])

    def test_multiplas_chamadas(self):
        decision = validate_v4(
            "Consulte o status da colmeia 3.",
            [
                {
                    "name": "consultar_status_colmeia",
                    "arguments": {"colmeia_id": 3},
                },
                {
                    "name": "listar_colmeias_alerta",
                    "arguments": {},
                },
            ],
        )
        self.assertFalse(decision.authorized)


if __name__ == "__main__":
    unittest.main()
