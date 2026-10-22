"""Extração das chamadas de ferramentas do Needle 2."""

import json
import re


def extract_tool_calls(model_output):
    match = re.search(
        r"<tool_call>\s*(.*?)\s*</tool_call>",
        model_output,
        flags=re.DOTALL,
    )

    if not match:
        return {
            "parsed_calls": None,
            "parse_error": "tool_call_not_found",
        }

    try:
        calls = json.loads(match.group(1).strip())
    except json.JSONDecodeError as exc:
        return {
            "parsed_calls": None,
            "parse_error": str(exc),
        }

    if not isinstance(calls, list):
        return {
            "parsed_calls": None,
            "parse_error": "tool_call_must_be_list",
        }

    return {
        "parsed_calls": calls,
        "parse_error": None,
    }
