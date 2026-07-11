#!/usr/bin/env python3
"""Responses API tool-calling validation harness.

The script intentionally separates JSON-schema validity from application-level
business validation. The function schema only requires ``unit`` to be a string;
the application accepts only celsius/fahrenheit.

Without OPENAI_API_KEY this harness runs deterministic local fixtures that reuse
the tool-call parser, business validator, and toy tool execution path instead of
claiming real Responses API behavior.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


API_URL = os.environ.get("OPENAI_RESPONSES_URL", "https://api.openai.com/v1/responses")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
ALLOWED_UNITS = {"celsius", "fahrenheit"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class TraceEvent:
    event: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now)


def post_response(payload: dict[str, Any], api_key: str) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def function_tool() -> dict[str, Any]:
    return {
        "type": "function",
        "name": "get_weather",
        "description": "Return a toy weather report for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "unit": {"type": "string"},
            },
            "required": ["city", "unit"],
            "additionalProperties": False,
        },
        "strict": True,
    }


def find_function_call(response: dict[str, Any]) -> dict[str, Any] | None:
    for item in response.get("output", []):
        if item.get("type") in {"function_call", "tool_call"}:
            return item
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") in {"function_call", "tool_call"}:
                    return content
    return None


def parse_arguments(call: dict[str, Any]) -> dict[str, Any]:
    arguments = call.get("arguments", {})
    if isinstance(arguments, str):
        return json.loads(arguments)
    if isinstance(arguments, dict):
        return arguments
    raise ValueError(f"Unsupported arguments type: {type(arguments).__name__}")


def validate_weather_args(arguments: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    city = arguments.get("city")
    unit = arguments.get("unit")
    if not isinstance(city, str) or not city.strip():
        errors.append("city must be a non-empty string")
    if unit not in ALLOWED_UNITS:
        errors.append("unit must be one of: celsius, fahrenheit")
    return errors


def execute_weather(arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        "city": arguments["city"],
        "temperature": 21 if arguments["unit"] == "celsius" else 70,
        "unit": arguments["unit"],
        "condition": "cloudy",
        "source": "toy_runtime",
    }


def response_text(response: dict[str, Any]) -> str:
    texts: list[str] = []
    for item in response.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if "text" in content:
                    texts.append(str(content["text"]))
    return "\n".join(texts)


def fake_function_response(response_id: str, call_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": response_id,
        "output": [
            {
                "type": "function_call",
                "name": "get_weather",
                "call_id": call_id,
                "arguments": json.dumps(arguments),
            }
        ],
    }


def run_tool_calling_control() -> dict[str, Any]:
    trace: list[TraceEvent] = []
    first = fake_function_response("resp_control_1", "call_weather_1", {"city": "Tokyo", "unit": "kelvin"})
    trace.append(TraceEvent("first_response_fixture", {"id": first["id"]}))

    call = find_function_call(first)
    if call is None:
        raise AssertionError("control fixture should contain a function call")
    arguments = parse_arguments(call)
    trace.append(
        TraceEvent(
            "tool_call_received",
            {"name": call.get("name"), "call_id": call.get("call_id"), "arguments": arguments},
        )
    )
    errors = validate_weather_args(arguments)
    trace.append(TraceEvent("tool_validation_failed", {"ok": False, "errors": errors}))

    second = fake_function_response("resp_control_2", "call_weather_2", {"city": "Tokyo", "unit": "celsius"})
    trace.append(TraceEvent("second_response_fixture", {"id": second["id"]}))
    second_call = find_function_call(second)
    if second_call is None:
        raise AssertionError("second control fixture should contain a function call")
    second_args = parse_arguments(second_call)
    second_errors = validate_weather_args(second_args)
    trace.append(
        TraceEvent(
            "second_tool_call_received",
            {"name": second_call.get("name"), "call_id": second_call.get("call_id"), "arguments": second_args},
        )
    )
    if second_errors:
        trace.append(TraceEvent("second_tool_validation_failed", {"ok": False, "errors": second_errors}))
        tool_execution_count = 0
    else:
        trace.append(TraceEvent("tool_executed", {"ok": True, "result": execute_weather(second_args)}))
        tool_execution_count = 1

    validation_failed_count = 1 if errors else 0
    corrected_tool_call_count = 1 if errors and not second_errors else 0
    all_passed = (
        validation_failed_count == 1
        and corrected_tool_call_count == 1
        and tool_execution_count == 1
        and arguments["unit"] == "kelvin"
        and second_args["unit"] == "celsius"
    )
    return {
        "status": "completed",
        "api_status": "skipped_without_openai_api_key",
        "reason": "OPENAI_API_KEY is not set",
        "model": MODEL,
        "tool_call_control": "deterministic_validation_retry_fixtures",
        "real_api_validated": False,
        "tool_calls_seen": 2,
        "validation_failed_count": validation_failed_count,
        "corrected_tool_call_count": corrected_tool_call_count,
        "tool_execution_count": tool_execution_count,
        "tool_call_control_passed": all_passed,
        "all_passed": all_passed,
        "trace": [event.__dict__ for event in trace],
        "limitations": [
            "Deterministic fixtures only validate local tool-call parsing, business validation, retry feedback shape, and toy tool execution logic.",
            "They do not validate real Responses API tool-call generation, model correction behavior, schema adherence, latency, cost, or cross-model reliability.",
        ],
    }


def run(api_key: str) -> dict[str, Any]:
    trace: list[TraceEvent] = []
    started = time.perf_counter()
    first_payload = {
        "model": MODEL,
        "input": [
            {
                "role": "developer",
                "content": (
                    "Use get_weather for weather questions. If tool validation returns "
                    "an error, choose a valid unit or explain why the request cannot be completed."
                ),
            },
            {"role": "user", "content": "What is the weather in Tokyo? Use kelvin."},
        ],
        "tools": [function_tool()],
    }
    trace.append(TraceEvent("request_created", {"model": MODEL, "tool": "get_weather"}))
    first = post_response(first_payload, api_key)
    trace.append(TraceEvent("first_response_received", {"id": first.get("id")}))

    call = find_function_call(first)
    if call is None:
        trace.append(TraceEvent("no_tool_call", {"text": response_text(first)}))
        return finish("no_tool_call", trace, first, None)

    arguments = parse_arguments(call)
    call_id = call.get("call_id") or call.get("id")
    trace.append(
        TraceEvent(
            "tool_call_received",
            {"name": call.get("name"), "call_id": call_id, "arguments": arguments},
        )
    )
    errors = validate_weather_args(arguments)
    if errors:
        tool_output = {"ok": False, "errors": errors}
        trace.append(TraceEvent("tool_validation_failed", tool_output))
    else:
        tool_output = {"ok": True, "result": execute_weather(arguments)}
        trace.append(TraceEvent("tool_executed", tool_output))

    second_payload = {
        "model": MODEL,
        "previous_response_id": first.get("id"),
        "input": [
            {
                "type": "function_call_output",
                "call_id": call_id,
                "output": json.dumps(tool_output),
            }
        ],
        "tools": [function_tool()],
    }
    second = post_response(second_payload, api_key)
    trace.append(TraceEvent("second_response_received", {"id": second.get("id")}))
    second_call = find_function_call(second)
    if second_call is not None:
        second_args = parse_arguments(second_call)
        trace.append(
            TraceEvent(
                "second_tool_call_received",
                {"name": second_call.get("name"), "arguments": second_args},
            )
        )
        second_errors = validate_weather_args(second_args)
        status = "corrected_tool_call" if not second_errors else "repeated_invalid_tool_call"
    else:
        trace.append(TraceEvent("final_response_received", {"text": response_text(second)}))
        status = "final_response_after_tool_feedback"

    result = finish(status, trace, first, second)
    result["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    return result


def finish(
    status: str,
    trace: list[TraceEvent],
    first_response: dict[str, Any],
    second_response: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "status": status,
        "model": MODEL,
        "api_url": API_URL,
        "trace": [event.__dict__ for event in trace],
        "response_ids": [item.get("id") for item in [first_response, second_response] if item],
    }


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(json.dumps(run_tool_calling_control(), ensure_ascii=False, indent=2))
        return 0

    try:
        result = run(api_key)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print(json.dumps({"status": "api_error", "code": error.code, "body": body}, indent=2))
        return 1
    except Exception as error:  # noqa: BLE001 - this is a CLI experiment harness.
        print(json.dumps({"status": "error", "error": str(error)}, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
