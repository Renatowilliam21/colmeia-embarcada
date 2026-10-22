"""Testes unitários da camada determinística de segurança."""

import unittest

from src.safety.safety_validator import validate


def status(hive_id):
    return [{
        "name": "consultar_status_colmeia",
        "arguments": {"colmeia_id": hive_id},
    }]


def alerts():
    return [{
        "name": "listar_colmeias_alerta",
        "arguments": {},
    }]


def inspection(hive_id, duration):
    return [{
        "name": "ativar_modo_inspecao",
        "arguments": {
            "colmeia_id": hive_id,
            "duracao_min": duration,
        },
    }]


class TestValidCommands(unittest.TestCase):

    def test_valid_status(self):
        result = validate(
            "Consulte o status da colmeia 12.",
            status(12),
        )
        self.assertTrue(result.authorized)

    def test_valid_alerts(self):
        result = validate(
            "Liste todas as colmeias em alerta.",
            alerts(),
        )
        self.assertTrue(result.authorized)

    def test_valid_inspection(self):
        result = validate(
            "Ative o modo inspeção da colmeia 42 por 15 minutos.",
            inspection(42, 15),
        )
        self.assertTrue(result.authorized)

    def test_minimum_duration(self):
        result = validate(
            "Ative inspeção na colmeia 1 por 5 minutos.",
            inspection(1, 5),
        )
        self.assertTrue(result.authorized)

    def test_maximum_duration(self):
        result = validate(
            "Ative inspeção na colmeia 50 por 60 minutos.",
            inspection(50, 60),
        )
        self.assertTrue(result.authorized)


class TestInvalidParameters(unittest.TestCase):

    def test_invalid_requested_duration(self):
        result = validate(
            "Ative inspeção na colmeia 33 por 3 minutos.",
            inspection(33, 33),
        )
        self.assertFalse(result.authorized)

    def test_excessive_requested_duration(self):
        result = validate(
            "Ative inspeção na colmeia 3 por 90 minutos.",
            inspection(3, 19),
        )
        self.assertFalse(result.authorized)

    def test_missing_duration(self):
        result = validate(
            "Ative inspeção na colmeia 23.",
            inspection(23, 13),
        )
        self.assertFalse(result.authorized)

    def test_indeterminate_duration(self):
        result = validate(
            "Ative inspeção na colmeia 23 por alguns minutos.",
            inspection(23, 13),
        )
        self.assertFalse(result.authorized)

    def test_missing_hive_id(self):
        result = validate(
            "Ative a inspeção por 20 minutos.",
            inspection(2, 20),
        )
        self.assertFalse(result.authorized)

    def test_different_hive_id(self):
        result = validate(
            "Consulte o status da colmeia 12.",
            status(13),
        )
        self.assertFalse(result.authorized)

    def test_different_duration(self):
        result = validate(
            "Ative inspeção na colmeia 12 por 20 minutos.",
            inspection(12, 13),
        )
        self.assertFalse(result.authorized)

    def test_hive_id_outside_range(self):
        result = validate(
            "Consulte o status da colmeia 51.",
            status(51),
        )
        self.assertFalse(result.authorized)


class TestSemanticSafety(unittest.TestCase):

    def test_negative_inspection(self):
        result = validate(
            "Não ative inspeção na colmeia 12 por 20 minutos.",
            inspection(12, 20),
        )
        self.assertFalse(result.authorized)

    def test_conditional_inspection(self):
        result = validate(
            "Se necessário, ative inspeção na colmeia 12 "
            "por 20 minutos.",
            inspection(12, 20),
        )
        self.assertFalse(result.authorized)

    def test_status_changed_to_inspection(self):
        result = validate(
            "Consulte o status da colmeia 12.",
            inspection(12, 13),
        )
        self.assertFalse(result.authorized)

    def test_inspection_changed_to_status(self):
        result = validate(
            "Ative inspeção na colmeia 12 por 20 minutos.",
            status(12),
        )
        self.assertFalse(result.authorized)

    def test_general_conversation(self):
        result = validate(
            "Bom dia, como você está?",
            status(12),
        )
        self.assertFalse(result.authorized)

    def test_multiple_actions(self):
        result = validate(
            "Ative inspeção nas colmeias 12 e 13 "
            "por 20 minutos.",
            inspection(12, 20) + inspection(13, 20),
        )
        self.assertFalse(result.authorized)

    def test_negative_alert_listing(self):
        result = validate(
            "Não liste as colmeias em alerta.",
            alerts(),
        )
        self.assertFalse(result.authorized)

    def test_question_about_inspection(self):
        result = validate(
            "Você pode ativar a inspeção da colmeia 12 "
            "por 20 minutos?",
            inspection(12, 20),
        )
        self.assertFalse(result.authorized)

    def test_unrelated_numbers(self):
        result = validate(
            "Ative inspeção na colmeia 12 por 20 minutos "
            "e registre o lote 35.",
            inspection(12, 20),
        )
        self.assertFalse(result.authorized)

    def test_negation_after_valid_command(self):
        result = validate(
            "Ative inspeção na colmeia 12 por 20 minutos, "
            "mas não execute agora.",
            inspection(12, 20),
        )
        self.assertFalse(result.authorized)


class TestStructuralSafety(unittest.TestCase):

    def test_unknown_tool(self):
        result = validate(
            "Consulte o status da colmeia 12.",
            [{
                "name": "excluir_colmeia",
                "arguments": {"colmeia_id": 12},
            }],
        )
        self.assertFalse(result.authorized)

    def test_non_list_response(self):
        result = validate(
            "Consulte o status da colmeia 12.",
            "consultar_status_colmeia",
        )
        self.assertFalse(result.authorized)

    def test_missing_argument(self):
        result = validate(
            "Consulte o status da colmeia 12.",
            [{
                "name": "consultar_status_colmeia",
                "arguments": {},
            }],
        )
        self.assertFalse(result.authorized)

    def test_extra_argument(self):
        result = validate(
            "Consulte o status da colmeia 12.",
            [{
                "name": "consultar_status_colmeia",
                "arguments": {
                    "colmeia_id": 12,
                    "admin": True,
                },
            }],
        )
        self.assertFalse(result.authorized)

    def test_boolean_as_integer(self):
        result = validate(
            "Consulte o status da colmeia 12.",
            status(True),
        )
        self.assertFalse(result.authorized)

    def test_invalid_duration_type(self):
        result = validate(
            "Ative inspeção na colmeia 12 por 20 minutos.",
            inspection(12, "20"),
        )
        self.assertFalse(result.authorized)

    def test_empty_calls(self):
        result = validate(
            "Bom dia.",
            [],
        )
        self.assertTrue(result.authorized)
        self.assertEqual(result.calls, [])

    def test_no_partial_authorization(self):
        result = validate(
            "Consulte o status da colmeia 12.",
            status(12) + inspection(12, 20),
        )
        self.assertFalse(result.authorized)
        self.assertEqual(result.calls, [])


if __name__ == "__main__":
    unittest.main()
