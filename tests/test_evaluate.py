import importlib.util
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'src/evaluation/evaluate.py'
spec = importlib.util.spec_from_file_location('evaluate', SOURCE)
evaluate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluate)
SCHEMAS = {
    'consultar_status_colmeia': {'parameters': {'properties': {'colmeia_id': {'type': 'integer', 'minimum': 1, 'maximum': 50}}, 'required': ['colmeia_id']}},
    'ativar_modo_inspecao': {'parameters': {'properties': {'colmeia_id': {'type': 'integer'}, 'duracao_min': {'type': 'integer'}}, 'required': ['colmeia_id', 'duracao_min']}},
}

class EvaluationTests(unittest.TestCase):
    def test_exact(self):
        case = {'id': 1, 'categoria': 'diretos', 'ferramenta_esperada': 'consultar_status_colmeia', 'argumentos_esperados': {'colmeia_id': 3}}
        output = [{'name': 'consultar_status_colmeia', 'arguments': {'colmeia_id': 3}}]
        self.assertEqual(evaluate.assess(case, output, SCHEMAS)['v2'], 'acerto_exato')

    def test_hallucinated_duration(self):
        case = {'id': 17, 'categoria': 'parametro_implicito', 'ferramenta_esperada': 'ativar_modo_inspecao', 'argumentos_esperados': {'colmeia_id': 3}}
        output = [{'name': 'ativar_modo_inspecao', 'arguments': {'colmeia_id': 3, 'duracao_min': 13}}]
        self.assertEqual(evaluate.assess(case, output, SCHEMAS)['v2'], 'requer_esclarecimento_mas_gerou_chamada')

    def test_case23(self):
        case = {'id': 23, 'categoria': 'ambiguos', 'ferramenta_esperada': 'consultar_status_colmeia', 'argumentos_esperados': None}
        result = evaluate.assess(case, evaluate.MULTI[23], SCHEMAS)
        self.assertEqual(result['v2'], 'multiplas_chamadas_corretas')
        self.assertEqual(result['historico'], 'nao_avaliavel')

    def test_reject(self):
        case = {'id': 29, 'categoria': 'fora_escopo', 'ferramenta_esperada': None, 'argumentos_esperados': None}
        self.assertEqual(evaluate.assess(case, [], SCHEMAS)['v2'], 'rejeicao_correta')

    def test_invalid_bool_integer(self):
        calls = [{'name': 'consultar_status_colmeia', 'arguments': {'colmeia_id': True}}]
        self.assertTrue(evaluate.schema_errors(calls, SCHEMAS))

if __name__ == '__main__':
    unittest.main()
