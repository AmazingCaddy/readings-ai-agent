#!/usr/bin/env python3
"""Run a tiny official MCP Python SDK stdio trace harness."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SERVER = Path(__file__).with_name("mcp_sdk_server.py")
SENSITIVE_MARKERS = ["secret=example-token"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return to_jsonable(value.model_dump(mode="json"))
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [to_jsonable(item) for item in value]
    return value


def redact(value: Any) -> Any:
    value = to_jsonable(value)
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        redacted = value
        for marker in SENSITIVE_MARKERS:
            redacted = redacted.replace(marker, "[REDACTED]")
        return redacted
    return value


@dataclass
class TraceEvent:
    actor: str
    method: str
    decision: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now)


class HostPolicy:
    denied_tools = {"write_release_note"}

    def approve_tool(self, name: str, arguments: dict[str, Any]) -> tuple[bool, str]:
        if name in self.denied_tools:
            return False, "requires explicit user approval; simulated user rejected"
        return True, "read-only tool allowed"

    def classify_resource(self, text: str) -> str:
        lowered = text.lower()
        if "ignore previous instructions" in lowered or "secret=" in lowered:
            return "untrusted_prompt_injection_candidate"
        return "ordinary_context"


class SdkTraceHost:
    def __init__(self) -> None:
        self.policy = HostPolicy()
        self.trace: list[TraceEvent] = []

    def record(self, actor: str, method: str, decision: str, **details: Any) -> None:
        self.trace.append(TraceEvent(actor=actor, method=method, decision=decision, details=redact(details)))

    async def guarded_tool_call(
        self, session: ClientSession, name: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        approved, reason = self.policy.approve_tool(name, arguments)
        self.record(
            "host",
            "tools/call.approval",
            "approved" if approved else "rejected",
            tool=name,
            reason=reason,
            arguments=arguments,
        )
        if not approved:
            return {"content": [{"type": "text", "text": reason}], "isError": True, "forwarded_to_server": False}
        result = await session.call_tool(name, arguments)
        self.record("client", "tools/call", "sdk_result_received", tool=name, result=result)
        return redact(result)

    async def reviewed_resource_read(self, session: ClientSession, uri: str) -> dict[str, Any]:
        result = await session.read_resource(uri)
        text = "\n".join(item.text for item in result.contents if getattr(item, "text", None))
        classification = self.policy.classify_resource(text)
        self.record("client", "resources/read", "sdk_result_received", uri=uri, result=result)
        self.record("host", "resources/read.review", classification, uri=uri)
        return redact(result)


async def run_validation() -> dict[str, Any]:
    try:
        from mcp import ClientSession
        from mcp.client.stdio import StdioServerParameters, stdio_client
    except ImportError:
        return {
            "status": "skipped",
            "reason": "mcp_python_sdk_not_installed",
            "install_note": "Run with `uv run --with mcp ...` to collect official SDK traces.",
        }

    host = SdkTraceHost()
    server_params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    with open(os.devnull, "w", encoding="utf-8") as errlog:
        async with stdio_client(server_params, errlog=errlog) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                initialize = await session.initialize()
                host.record("client", "initialize", "sdk_result_received", result=initialize)

                tools = await session.list_tools()
                host.record("client", "tools/list", "sdk_result_received", result=tools)

                read_only_tool = await host.guarded_tool_call(
                    session, "lookup_policy_section", {"section": "mcp-security"}
                )
                rejected_write_tool = await host.guarded_tool_call(
                    session, "write_release_note", {"title": "MCP", "body": "secret=example-token"}
                )

                resources = await session.list_resources()
                host.record("client", "resources/list", "sdk_result_received", result=resources)

                safe_resource = await host.reviewed_resource_read(session, "handbook://mcp/security")
                malicious_resource = await host.reviewed_resource_read(session, "handbook://mcp/malicious-note")

                prompts = await session.list_prompts()
                host.record("client", "prompts/list", "sdk_result_received", result=prompts)
                prompt_result = await session.get_prompt("security_review_prompt", {"topic": "tool approval"})
                host.record("client", "prompts/get", "sdk_result_received", result=prompt_result)

    trace = [event.__dict__ for event in host.trace]
    trace_json = json.dumps(trace, ensure_ascii=False)
    return {
        "status": "completed",
        "sdk": "mcp Python SDK",
        "server": "FastMCP stdio",
        "server_name": initialize.serverInfo.name,
        "protocol_version": initialize.protocolVersion,
        "tool_count": len(tools.tools),
        "resource_count": len(resources.resources),
        "prompt_count": len(prompts.prompts),
        "read_only_tool_is_error": bool(getattr(read_only_tool, "isError", False)),
        "rejected_write_tool_forwarded": rejected_write_tool["forwarded_to_server"],
        "safe_resource_contents": len(safe_resource["contents"]),
        "malicious_resource_review": next(
            event.decision
            for event in host.trace
            if event.method == "resources/read.review" and event.details.get("uri") == "handbook://mcp/malicious-note"
        ),
        "prompt_messages": len(prompt_result.messages),
        "trace_event_count": len(trace),
        "leaked_secret_in_trace": any(marker in trace_json for marker in SENSITIVE_MARKERS),
        "trace": trace,
    }


def main() -> None:
    print(json.dumps(asyncio.run(run_validation()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
