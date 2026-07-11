#!/usr/bin/env python3
"""Run a tiny MCP-like stdio JSON-RPC trace harness."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SERVER = Path(__file__).with_name("mcp_stdio_server.py")
SENSITIVE_MARKERS = ["secret=example-token"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def redact(value: Any) -> Any:
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
    roots = [{"uri": "file:///workspace/readings-ai-agent", "name": "workspace"}]

    def approve_tool(self, name: str, arguments: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
        if name in self.denied_tools:
            return False, "requires explicit user approval; simulated user rejected", redact(arguments)
        return True, "read-only tool allowed", redact(arguments)

    def classify_resource(self, text: str) -> str:
        lowered = text.lower()
        if "ignore previous instructions" in lowered or "secret=" in lowered:
            return "untrusted_prompt_injection_candidate"
        return "ordinary_context"


class StdioClient:
    def __init__(self) -> None:
        self.policy = HostPolicy()
        self.next_id = 1
        self.trace: list[TraceEvent] = []
        self.process = subprocess.Popen(
            [sys.executable, str(SERVER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def close(self) -> None:
        if self.process.stdin:
            self.process.stdin.close()
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()

    def record(self, actor: str, method: str, decision: str, **details: Any) -> None:
        self.trace.append(TraceEvent(actor=actor, method=method, decision=decision, details=redact(details)))

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        request_id = self.next_id
        self.next_id += 1
        payload = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            payload["params"] = params
        self.record("client", method, "request_sent", id=request_id, params=params or {})
        assert self.process.stdin is not None
        assert self.process.stdout is not None
        self.process.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        response = json.loads(line)
        self.record("server", method, "response_received", id=response.get("id"), response=response)
        return response

    def roots_list(self) -> dict[str, Any]:
        result = {"roots": self.policy.roots}
        self.record("host", "roots/list", "returned_allowed_roots", roots=result["roots"])
        return result

    def tool_call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        approved, reason, reviewed_args = self.policy.approve_tool(name, arguments)
        self.record(
            "host",
            "tools/call.approval",
            "approved" if approved else "rejected",
            tool=name,
            reason=reason,
            arguments=reviewed_args,
        )
        if not approved:
            return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": reason}], "isError": True}}
        return self.request("tools/call", {"name": name, "arguments": arguments})

    def resource_read(self, uri: str) -> dict[str, Any]:
        response = self.request("resources/read", {"uri": uri})
        text = "\n".join(item.get("text", "") for item in response.get("result", {}).get("contents", []))
        classification = self.policy.classify_resource(text)
        self.record("host", "resources/read.review", classification, uri=uri)
        return response


def main() -> int:
    client = StdioClient()
    try:
        summary = {
            "initialize": client.request("initialize", {"clientInfo": {"name": "handbook-host", "version": "0.1.0"}}),
            "roots": client.roots_list(),
            "tools": client.request("tools/list"),
            "readOnlyToolResult": client.tool_call("lookup_policy_section", {"section": "mcp-security"}),
            "rejectedWriteToolResult": client.tool_call(
                "write_release_note", {"title": "MCP", "body": "secret=example-token"}
            ),
            "resources": client.request("resources/list"),
            "safeResource": client.resource_read("handbook://mcp/security"),
            "maliciousResource": client.resource_read("handbook://mcp/malicious-note"),
        }
        summary["trace"] = [event.__dict__ for event in client.trace]
        trace_json = json.dumps(summary["trace"], ensure_ascii=False)
        summary["leaked_secret_in_trace"] = any(marker in trace_json for marker in SENSITIVE_MARKERS)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
