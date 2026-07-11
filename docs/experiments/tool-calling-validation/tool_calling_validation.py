#!/usr/bin/env python3
"""Minimal tool-calling validation and retry simulation.

This is a deterministic no-model experiment. It uses a fake model to show the
application-side boundary: the model proposes a tool call, the application
validates and executes it, then feeds tool errors/results back into the loop.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class TraceEvent:
    step: int
    actor: str
    event: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now)


class FakeModel:
    """Returns one invalid tool call, then fixes it after seeing feedback."""

    def next_message(self, history: list[dict[str, Any]]) -> dict[str, Any]:
        tool_errors = [item for item in history if item.get("role") == "tool" and item.get("is_error")]
        tool_results = [item for item in history if item.get("role") == "tool" and not item.get("is_error")]

        if tool_results:
            return {
                "type": "final",
                "content": "Tokyo is 21 C and cloudy.",
            }

        if tool_errors:
            return {
                "type": "tool_call",
                "call_id": "call_002",
                "name": "get_weather",
                "arguments": {"city": "Tokyo", "unit": "celsius"},
            }

        return {
            "type": "tool_call",
            "call_id": "call_001",
            "name": "get_weather",
            "arguments": {"city": "Tokyo", "unit": "kelvin"},
        }


class ToolRuntime:
    allowed_units = {"celsius", "fahrenheit"}

    def validate_get_weather(self, arguments: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        city = arguments.get("city")
        unit = arguments.get("unit")
        if not isinstance(city, str) or not city.strip():
            errors.append("city must be a non-empty string")
        if unit not in self.allowed_units:
            errors.append("unit must be one of: celsius, fahrenheit")
        return errors

    def execute_get_weather(self, arguments: dict[str, Any]) -> dict[str, Any]:
        unit = arguments["unit"]
        temperature = 21 if unit == "celsius" else 70
        return {
            "city": arguments["city"],
            "temperature": temperature,
            "unit": unit,
            "condition": "cloudy",
        }


class ApplicationLoop:
    def __init__(self, model: FakeModel, runtime: ToolRuntime, max_turns: int = 4) -> None:
        self.model = model
        self.runtime = runtime
        self.max_turns = max_turns
        self.history: list[dict[str, Any]] = [
            {"role": "user", "content": "What is the weather in Tokyo? Use celsius."}
        ]
        self.trace: list[TraceEvent] = []

    def record(self, step: int, actor: str, event: str, **details: Any) -> None:
        self.trace.append(TraceEvent(step=step, actor=actor, event=event, details=details))

    def run(self) -> dict[str, Any]:
        for step in range(1, self.max_turns + 1):
            message = self.model.next_message(self.history)

            if message["type"] == "final":
                self.record(step, "model", "final_response", content=message["content"])
                return {"status": "ok", "final": message["content"], "trace": self.serialized_trace()}

            self.record(
                step,
                "model",
                "tool_call_requested",
                call_id=message["call_id"],
                tool=message["name"],
                arguments=message["arguments"],
            )

            if message["name"] != "get_weather":
                return self.tool_error(step, message, ["unknown tool"])

            errors = self.runtime.validate_get_weather(message["arguments"])
            if errors:
                tool_message = self.tool_error(step, message, errors)
                self.history.append(tool_message)
                continue

            result = self.runtime.execute_get_weather(message["arguments"])
            self.record(step, "application", "tool_executed", call_id=message["call_id"], result=result)
            self.history.append(
                {
                    "role": "tool",
                    "call_id": message["call_id"],
                    "name": message["name"],
                    "is_error": False,
                    "content": result,
                }
            )

        return {"status": "max_turns_exceeded", "trace": self.serialized_trace()}

    def tool_error(self, step: int, message: dict[str, Any], errors: list[str]) -> dict[str, Any]:
        self.record(
            step,
            "application",
            "tool_validation_failed",
            call_id=message["call_id"],
            tool=message["name"],
            errors=errors,
        )
        return {
            "role": "tool",
            "call_id": message["call_id"],
            "name": message["name"],
            "is_error": True,
            "content": {"errors": errors},
        }

    def serialized_trace(self) -> list[dict[str, Any]]:
        return [event.__dict__ for event in self.trace]


def main() -> None:
    result = ApplicationLoop(FakeModel(), ToolRuntime()).run()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
