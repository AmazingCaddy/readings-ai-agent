#!/usr/bin/env python3
"""Run all validation harnesses and summarize their status."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Harness:
    name: str
    path: Path


HARNESSES = [
    Harness("real_tool_calling", ROOT / "docs/experiments/real-tool-calling-validation/real_tool_calling_validation.py"),
    Harness(
        "real_structured_output",
        ROOT / "docs/experiments/real-structured-output-validation/real_structured_output_validation.py",
    ),
    Harness(
        "real_prompt_injection_permission",
        ROOT / "docs/experiments/real-prompt-injection-permission/real_prompt_injection_permission.py",
    ),
    Harness("real_rag_citation", ROOT / "docs/experiments/real-rag-citation-validation/real_rag_citation_validation.py"),
    Harness(
        "real_llamaindex_rag",
        ROOT / "docs/experiments/real-llamaindex-rag-validation/real_llamaindex_rag_validation.py",
    ),
    Harness("real_trace_aware_eval", ROOT / "docs/experiments/real-trace-aware-eval/real_trace_aware_eval.py"),
    Harness(
        "real_production_cost_latency",
        ROOT / "docs/experiments/real-production-cost-latency-validation/real_production_cost_latency_validation.py",
    ),
    Harness(
        "real_browser_playwright",
        ROOT / "docs/experiments/real-browser-playwright-validation/real_browser_playwright_validation.py",
    ),
    Harness(
        "real_batch_flex_caching",
        ROOT / "docs/experiments/real-batch-flex-caching-validation/real_batch_flex_caching_validation.py",
    ),
    Harness(
        "real_langgraph_interrupt_recovery",
        ROOT / "docs/experiments/real-langgraph-interrupt-recovery/real_langgraph_interrupt_recovery.py",
    ),
    Harness(
        "real_langgraph_memory_store",
        ROOT / "docs/experiments/real-langgraph-memory-store-validation/real_langgraph_memory_store_validation.py",
    ),
    Harness(
        "real_moderation_safety",
        ROOT / "docs/experiments/real-moderation-safety-validation/real_moderation_safety_validation.py",
    ),
    Harness("mcp_stdio_trace", ROOT / "docs/experiments/real-mcp-stdio-trace/mcp_stdio_trace.py"),
    Harness("mcp_sdk_trace", ROOT / "docs/experiments/real-mcp-sdk-trace/mcp_sdk_trace.py"),
]


def parse_json(stdout: str) -> dict[str, Any]:
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        return {"status": "parse_error", "error": str(exc), "stdout_preview": stdout[:500]}


def compact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    compact: dict[str, Any] = {
        "status": payload.get("status", "completed" if "trace" in payload else "unknown"),
    }
    for key in [
        "reason",
        "model",
        "api_url",
        "retrieval",
        "framework",
        "store",
        "namespace_policy",
        "index",
        "embedding",
        "llm_synthesis",
        "all_passed",
        "untrusted_chunk_cited",
        "cross_user_broad_prefix_seen",
        "deleted_item_recalled",
        "secret_leaked_in_trace",
        "elapsed_seconds",
        "tool_calls_seen",
        "final_only_passes",
        "trace_aware_passes",
        "request_count",
        "average_latency_ms",
        "p95_latency_ms",
        "rate_limit_headers_seen",
        "record_count",
        "trace_zip_created",
        "trace_zip_member_count",
        "checkpointer",
        "persistent_restart_tested",
        "mismatch_count",
        "sdk",
        "protocol_version",
        "tool_count",
        "resource_count",
        "prompt_count",
        "rejected_write_tool_forwarded",
        "malicious_resource_review",
        "leaked_secret_in_trace",
    ]:
        if key in payload:
            compact[key] = payload[key]
    for key in ["prompt_caching", "flex_processing", "batch_api"]:
        if key in payload:
            value = payload[key]
            compact[key] = value.get("status") if isinstance(value, dict) else value
    if "results" in payload and isinstance(payload["results"], list):
        compact["result_count"] = len(payload["results"])
        compact["result_statuses"] = [
            item.get("status", "passed" if item.get("passed") is True else "failed" if item.get("passed") is False else None)
            for item in payload["results"]
            if isinstance(item, dict)
        ]
    if "cases" in payload and isinstance(payload["cases"], list):
        compact["case_count"] = len(payload["cases"])
    if "trace" in payload and isinstance(payload["trace"], list):
        compact["trace_event_count"] = len(payload["trace"])
    return compact


def run_harness(harness: Harness) -> dict[str, Any]:
    started = time.perf_counter()
    completed = subprocess.run(
        [sys.executable, str(harness.path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    payload = parse_json(completed.stdout.strip()) if completed.stdout.strip() else {"status": "no_output"}
    return {
        "name": harness.name,
        "path": str(harness.path.relative_to(ROOT)),
        "exit_code": completed.returncode,
        "duration_seconds": round(time.perf_counter() - started, 3),
        "summary": compact_payload(payload),
        "stderr_preview": completed.stderr[:500],
    }


def main() -> int:
    results = [run_harness(harness) for harness in HARNESSES]
    failed = [item for item in results if item["exit_code"] != 0 or item["summary"].get("status") in {"error", "api_error"}]
    summary = {
        "status": "failed" if failed else "completed",
        "harness_count": len(results),
        "failed_count": len(failed),
        "results": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
