#!/usr/bin/env python3
"""Audit whether toy agent traces support debug, audit, regression, and privacy use cases.

This deterministic harness does not call an observability platform. It checks
field coverage and obvious secret leakage in fixed trace shapes so the handbook
can explain why trace design is more than collecting free-form logs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


TRACE_REQUIREMENTS = {
    "debug": {
        "run_id",
        "timestamp",
        "user_input",
        "model",
        "prompt_version",
        "tool_calls",
        "tool_results",
        "errors",
        "final_output",
    },
    "audit": {
        "run_id",
        "timestamp",
        "user_id_hash",
        "policy_version",
        "approval_events",
        "tool_calls",
        "tool_results",
        "side_effects",
        "redaction_status",
    },
    "regression": {
        "run_id",
        "dataset_id",
        "case_id",
        "expected_behavior",
        "actual_behavior",
        "failure_category",
        "model",
        "prompt_version",
        "tool_schema_version",
        "final_output",
    },
    "cost_latency": {
        "run_id",
        "model",
        "latency_ms",
        "input_tokens",
        "output_tokens",
        "estimated_cost_usd",
        "tool_latency_ms",
    },
    "rag": {
        "run_id",
        "retrieval_query",
        "retrieved_chunks",
        "source_ids",
        "retrieval_scores",
        "citation_ids",
        "grounded",
    },
    "privacy": {
        "run_id",
        "redaction_status",
        "sensitive_fields_removed",
        "retention_policy",
        "access_scope",
    },
}

SENSITIVE_MARKERS = ("sk-example-secret", "internal_secret", "customer@example.com")


@dataclass(frozen=True)
class TraceCase:
    trace_id: str
    description: str
    trace: dict[str, Any]


TRACE_CASES = [
    TraceCase(
        "minimal_log",
        "Only final input/output is saved.",
        {
            "run_id": "run-001",
            "user_input": "Draft refund recommendation for order A100.",
            "final_output": "Refund review drafted.",
        },
    ),
    TraceCase(
        "debug_trace",
        "Enough fields to debug a failed tool call, but not enough for audit or cost analysis.",
        {
            "run_id": "run-002",
            "timestamp": "2026-07-11T10:00:00Z",
            "user_input": "Draft refund recommendation for order A100.",
            "model": "example-model",
            "prompt_version": "refund-v3",
            "tool_calls": [{"tool": "get_order", "args": {"order_id": "A100"}}],
            "tool_results": [{"tool": "get_order", "status": "timeout"}],
            "errors": [{"code": "tool_timeout", "recovered": False}],
            "final_output": "Could not complete order lookup.",
        },
    ),
    TraceCase(
        "audit_ready_trace",
        "Includes approval, side-effect, redaction, and version fields.",
        {
            "run_id": "run-003",
            "timestamp": "2026-07-11T10:01:00Z",
            "user_id_hash": "user-hash-123",
            "user_input": "Draft refund recommendation for order A100.",
            "model": "example-model",
            "prompt_version": "refund-v3",
            "policy_version": "refund-policy-2026-07",
            "tool_schema_version": "orders-tools-v2",
            "tool_calls": [{"tool": "get_order", "args": {"order_id": "A100"}}],
            "tool_results": [{"tool": "get_order", "status": "delivered", "amount": 42}],
            "approval_events": [{"action": "issue_refund", "decision": "not_requested"}],
            "side_effects": [],
            "errors": [],
            "redaction_status": "redacted_before_write",
            "sensitive_fields_removed": True,
            "retention_policy": "30d",
            "access_scope": "support-audit-team",
            "latency_ms": 820,
            "input_tokens": 430,
            "output_tokens": 95,
            "estimated_cost_usd": 0.0012,
            "tool_latency_ms": {"get_order": 120},
            "final_output": "Refund review drafted; no refund issued.",
        },
    ),
    TraceCase(
        "eval_rag_trace",
        "Adds dataset, expected behavior, retrieval, citation, and failure-category fields.",
        {
            "run_id": "run-004",
            "timestamp": "2026-07-11T10:02:00Z",
            "dataset_id": "refund-eval-v1",
            "case_id": "refund-policy-current",
            "expected_behavior": "cite current policy and require human review",
            "actual_behavior": "cited current policy and required review",
            "failure_category": None,
            "user_id_hash": "user-hash-123",
            "user_input": "Should a charge dispute be auto-refunded?",
            "model": "example-model",
            "prompt_version": "refund-v3",
            "policy_version": "refund-policy-2026-07",
            "tool_schema_version": "orders-tools-v2",
            "retrieval_query": "charge dispute refund policy",
            "retrieved_chunks": [{"chunk_id": "chunk-2026", "source_id": "refund_policy_2026"}],
            "source_ids": ["refund_policy_2026"],
            "retrieval_scores": {"chunk-2026": 0.91},
            "citation_ids": ["refund_policy_2026"],
            "grounded": True,
            "tool_calls": [],
            "tool_results": [],
            "approval_events": [{"action": "issue_refund", "decision": "requires_human"}],
            "side_effects": [],
            "errors": [],
            "redaction_status": "redacted_before_write",
            "sensitive_fields_removed": True,
            "retention_policy": "30d",
            "access_scope": "eval-reviewers",
            "latency_ms": 980,
            "input_tokens": 920,
            "output_tokens": 130,
            "estimated_cost_usd": 0.0021,
            "tool_latency_ms": {},
            "final_output": "Charge disputes require human review per refund_policy_2026.",
        },
    ),
    TraceCase(
        "privacy_leaky_trace",
        "Contains useful debug fields but leaks sensitive values into trace.",
        {
            "run_id": "run-005",
            "timestamp": "2026-07-11T10:03:00Z",
            "user_input": "Email customer@example.com about refund. internal_secret=sk-example-secret",
            "model": "example-model",
            "prompt_version": "refund-v3",
            "tool_calls": [
                {
                    "tool": "send_email",
                    "args": {"to": "customer@example.com", "body": "internal_secret=sk-example-secret"},
                }
            ],
            "tool_results": [{"tool": "send_email", "status": "sent"}],
            "errors": [],
            "redaction_status": "not_redacted",
            "sensitive_fields_removed": False,
            "final_output": "Email sent.",
        },
    ),
]


def contains_sensitive_value(trace: dict[str, Any]) -> bool:
    serialized = json.dumps(trace, ensure_ascii=False)
    return any(marker in serialized for marker in SENSITIVE_MARKERS)


def audit_trace(case: TraceCase) -> dict[str, Any]:
    present = set(case.trace)
    use_case_results: dict[str, Any] = {}
    for use_case, required_fields in TRACE_REQUIREMENTS.items():
        missing = sorted(required_fields - present)
        use_case_results[use_case] = {
            "passed": not missing,
            "missing_fields": missing,
        }
    leaked = contains_sensitive_value(case.trace)
    privacy_failed = leaked or case.trace.get("redaction_status") == "not_redacted"
    return {
        "trace_id": case.trace_id,
        "description": case.description,
        "field_count": len(present),
        "use_cases": use_case_results,
        "leaked_sensitive_value": leaked,
        "privacy_failed": privacy_failed,
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    use_cases = sorted(TRACE_REQUIREMENTS)
    return {
        "trace_count": len(results),
        "passes_by_use_case": {
            use_case: sum(1 for result in results if result["use_cases"][use_case]["passed"]) for use_case in use_cases
        },
        "privacy_failed_traces": [result["trace_id"] for result in results if result["privacy_failed"]],
        "fully_supported_traces": [
            result["trace_id"]
            for result in results
            if all(result["use_cases"][use_case]["passed"] for use_case in use_cases) and not result["privacy_failed"]
        ],
    }


def main() -> None:
    results = [audit_trace(case) for case in TRACE_CASES]
    print(json.dumps({"summary": summarize(results), "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
