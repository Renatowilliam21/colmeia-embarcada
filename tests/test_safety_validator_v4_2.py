#!/usr/bin/env python3

import unittest

from src.safety.safety_validator_v4_2 import validate_v4_2


class TestSafetyValidatorV42(unittest.TestCase):

    def call(self, hive=7, duration=5):
        return [{
            "name": "ativar_modo_inspecao",
            "arguments": {
                "colmeia_id": hive,
                "duracao_min": duration,
            },
        }]

    def test_comando_explicito(self):
        result = validate_v4_2(
            "Ligue o modo de inspeção da colmeia 7 por 5 minutos.",
            self.call(),
        )
        self.assertTrue(result.authorized)

    def test_habilitar_inspecao(self):
        result = validate_v4_2(
            "Habilite o modo de inspeção da colmeia 40 durante 60 minutos.",
            self.call(40, 60),
        )
        self.assertTrue(result.authorized)

    def test_negacao(self):
        result = validate_v4_2(
            "Não ligue o modo de inspeção da colmeia 7 por 5 minutos.",
            self.call(),
        )
        self.assertFalse(result.authorized)

    def test_condicional(self):
        result = validate_v4_2(
            "Se necessário, ligue o modo de inspeção da colmeia 7 por 5 minutos.",
            self.call(),
        )
        self.assertFalse(result.authorized)

    def test_pergunta(self):
        result = validate_v4_2(
            "Ligue o modo de inspeção da colmeia 7 por 5 minutos?",
            self.call(),
        )
        self.assertFalse(result.authorized)

    def test_colmeia_divergente(self):
        result = validate_v4_2(
            "Ligue o modo de inspeção da colmeia 7 por 5 minutos.",
            self.call(8, 5),
        )
        self.assertFalse(result.authorized)

    def test_duracao_divergente(self):
        result = validate_v4_2(
            "Ligue o modo de inspeção da colmeia 7 por 5 minutos.",
            self.call(7, 10),
        )
        self.assertFalse(result.authorized)

    def test_duracao_invalida(self):
        result = validate_v4_2(
            "Ligue o modo de inspeção da colmeia 7 por 0 minutos.",
            self.call(7, 0),
        )
        self.assertFalse(result.authorized)

    def test_consulta_nao_pode_acionar(self):
        result = validate_v4_2(
            "Gostaria de ver as leituras dos sensores na colmeia 19.",
            self.call(19, 10),
        )
        self.assertFalse(result.authorized)

    def test_solicitacao_indireta(self):
        result = validate_v4_2(
            "Pode ativar agora o modo de inspeção da colmeia 22 por 25 minutos.",
            self.call(22, 25),
        )
        self.assertFalse(result.authorized)


if __name__ == "__main__":
    unittest.main()
