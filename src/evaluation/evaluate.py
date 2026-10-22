#!/usr/bin/env python3
"""Avaliador offline de tool-calling; não executa ferramentas nem inferência."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / 'dataset/colmeia-needle2-dataset-teste.json'
SCHEMA = ROOT / 'firmware/tools/colmeia.json'
OUTPUT = ROOT / 'results/avaliacao/avaliacao_v2.json'

# Contrato experimental v2; gabaritos originais permanecem intactos.
CLARIFY = {17, 18, 19, 20, 22, 24, 25, 26, 27}
MULTI = {23: [
    {'name': 'consultar_status_colmeia', 'arguments': {'colmeia_id': 3}},
    {'name': 'consultar_status_colmeia', 'arguments': {'colmeia_id': 4}},
]}


def normalize_output(value):
    """Aceita [] ou lista de {name,arguments}; também envelope {tool_calls: [...]}.

    Strings JSON são aceitas; texto livre é marcado como formato inválido.
    """
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return None, 'json_invalido'
    if isinstance(value, dict) and 'tool_calls' in value:
        value = value['tool_calls']
    if not isinstance(value, list):
        return None, 'saida_nao_e_lista'
    for call in value:
        if not isinstance(call, dict) or not isinstance(call.get('name'), str) or not isinstance(call.get('arguments'), dict):
            return None, 'chamada_malformada'
    return value, None


def schema_errors(calls, schemas):
    errors = []
    for index, call in enumerate(calls):
        name, args = call['name'], call['arguments']
        if name not in schemas:
            errors.append(f'{index}:ferramenta_desconhecida')
            continue
        spec = schemas[name]['parameters']
        props = spec.get('properties', {})
        for key in spec.get('required', []):
            if key not in args:
                errors.append(f'{index}:obrigatorio_ausente:{key}')
        for key, value in args.items():
            if key not in props:
                errors.append(f'{index}:argumento_desconhecido:{key}')
                continue
            field = props[key]
            if field.get('type') == 'integer':
                if type(value) is not int:
                    errors.append(f'{index}:tipo_invalido:{key}')
                elif not (field.get('minimum', value) <= value <= field.get('maximum', value)):
                    errors.append(f'{index}:fora_intervalo:{key}')
    return errors


def assess(case, raw, schemas):
    calls, format_error = normalize_output(raw)
    result = {'id': case['id'], 'categoria': case['categoria'],
              'formato_valido': format_error is None,
              'erro_formato': format_error, 'schema_valido': False,
              'erros_schema': [], 'historico': 'nao_avaliavel',
              'v2': 'nao_avaliavel', 'executavel_sem_confirmacao': False}
    if format_error:
        result['v2'] = 'formato_invalido'
        return result
    errors = schema_errors(calls, schemas)
    result['erros_schema'] = errors
    result['schema_valido'] = not errors
    expected_name = case['ferramenta_esperada']
    expected_args = case['argumentos_esperados']
    if expected_name is None:
        result['historico'] = 'acerto_exato' if calls == [] else 'erro'
    elif expected_args is not None:
        result['historico'] = ('acerto_exato' if calls == [{'name': expected_name, 'arguments': expected_args}]
                               else 'erro')
    # Sem forçar equivalência para gabaritos indefinidos.
    cid = case['id']
    if cid in CLARIFY:
        result['v2'] = 'abstencao_segura' if calls == [] else 'requer_esclarecimento_mas_gerou_chamada'
    elif cid in MULTI:
        expected = MULTI[cid]
        result['v2'] = ('multiplas_chamadas_corretas' if calls == expected or calls == expected[::-1]
                        else 'multiplas_chamadas_incorretas')
    elif expected_name is None:
        result['v2'] = 'rejeicao_correta' if calls == [] else 'falso_acionamento'
    else:
        result['v2'] = ('acerto_exato' if calls == [{'name': expected_name, 'arguments': expected_args}]
                        else 'erro')
    # Política conservadora: nenhum comando é executado automaticamente pelo avaliador.
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=Path,
                        help='JSON com lista de {id, saida}; saida = lista de chamadas ou string JSON')
    parser.add_argument('--output', default=OUTPUT, type=Path)
    args = parser.parse_args()
    cases = json.loads(DATASET.read_text(encoding='utf-8'))['casos']
    schemas = {f['name']: f for f in json.loads(SCHEMA.read_text(encoding='utf-8'))}
    observations = json.loads(args.input.read_text(encoding='utf-8'))
    if not isinstance(observations, list):
        parser.error('O arquivo de entrada deve ser uma lista JSON')
    known = {c['id'] for c in cases}
    outputs = {}
    for item in observations:
        if not isinstance(item, dict) or type(item.get('id')) is not int or 'saida' not in item:
            parser.error('Cada observação precisa conter id inteiro e saida')
        if item['id'] not in known or item['id'] in outputs:
            parser.error(f"ID desconhecido ou repetido: {item['id']}")
        outputs[item['id']] = item['saida']
    results = [assess(c, outputs[c['id']], schemas) for c in cases if c['id'] in outputs]
    summary = {'casos_dataset': len(cases), 'casos_avaliados': len(results),
               'historico': dict(Counter(r['historico'] for r in results)),
               'v2': dict(Counter(r['v2'] for r in results)),
               'schema_valido': sum(r['schema_valido'] for r in results)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({'resumo': summary, 'casos': results}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f'Relatório: {args.output}')


if __name__ == '__main__':
    main()
