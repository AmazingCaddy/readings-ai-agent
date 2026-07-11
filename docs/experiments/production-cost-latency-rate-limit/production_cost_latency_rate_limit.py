#!/usr/bin/env python3
"""Deterministic production cost, latency, and rate-limit audit.

This script does not call the OpenAI API. It audits toy request records against
the production/cost/latency/rate-limit, Batch, Flex, and Prompt Caching evidence
so the handbook can validate observable fields before a real API exercise.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from statistics import mean
from typing import Any


@dataclass(frozen=True)
class AuditRule:
    rule_id: str
    required_fields: tuple[str, ...]
    reason: str


AUDIT_RULES = [
    AuditRule(
        "usage_and_token_accounting",
        ("model", "input_tokens", "output_tokens", "request_count", "cost_estimate"),
        "Cost is only reviewable when model, token counts, request count, and cost estimate are recorded.",
    ),
    AuditRule(
        "rate_limit_headers",
        ("limit_requests", "remaining_requests", "reset_requests", "limit_tokens", "remaining_tokens", "reset_tokens"),
        "Rate-limit behavior needs request/token limit, remaining, and reset fields.",
    ),
    AuditRule(
        "retry_backoff",
        ("retry_count", "backoff_strategy", "jitter", "max_retries", "retry_stop_reason"),
        "Retries need bounded exponential backoff and a stop reason; infinite retries hide rate-limit failures.",
    ),
    AuditRule(
        "latency_distribution",
        ("latency_ms", "average_latency_ms", "p95_latency_ms", "timeout_ms"),
        "Production latency should track distribution, not a single anecdotal response time.",
    ),
    AuditRule(
        "budget_gate",
        ("budget_threshold", "budget_spent", "budget_action", "degraded_mode"),
        "Budget thresholds need a stop, degrade, or escalation action.",
    ),
    AuditRule(
        "model_and_output_controls",
        ("model_choice_reason", "max_output_tokens", "output_token_policy", "quality_check"),
        "Cost and latency changes need model/output controls plus a quality check.",
    ),
    AuditRule(
        "batch_workload_boundary",
        ("batch_candidate", "batch_status", "custom_id_mapping", "batch_expiration_policy"),
        "Batch workloads need async status, custom id mapping, and expiration handling.",
    ),
    AuditRule(
        "flex_fallback",
        ("service_tier", "resource_unavailable_count", "fallback_strategy", "fallback_cost_note"),
        "Flex processing needs resource-unavailable handling and fallback cost notes.",
    ),
    AuditRule(
        "prompt_cache_observability",
        ("cache_eligible", "cached_tokens", "cache_write_tokens", "cache_miss_reason"),
        "Prompt caching needs read/write token fields and cache-miss explanations.",
    ),
]


RUNS: dict[str, list[dict[str, Any]]] = {
    "naive_run": [
        {
            "request_id": "req_1",
            "model": "gpt-example-large",
            "input_tokens": 2500,
            "output_tokens": 900,
            "latency_ms": 4200,
            "retry_count": 4,
            "budget_spent": 2.4,
            "service_tier": "standard",
        },
        {
            "request_id": "req_2",
            "model": "gpt-example-large",
            "input_tokens": 2600,
            "output_tokens": 1100,
            "latency_ms": 6200,
            "retry_count": 7,
            "budget_spent": 3.1,
            "service_tier": "standard",
        },
        {
            "request_id": "req_3",
            "model": "gpt-example-large",
            "input_tokens": 2550,
            "output_tokens": 1000,
            "latency_ms": 5700,
            "retry_count": 0,
            "budget_spent": 2.9,
            "service_tier": "standard",
        },
    ],
    "governed_run": [
        {
            "request_id": "req_1",
            "model": "gpt-example-mini",
            "model_choice_reason": "meets quality baseline for extraction task",
            "input_tokens": 1800,
            "output_tokens": 420,
            "request_count": 1,
            "cost_estimate": 0.42,
            "limit_requests": 500,
            "remaining_requests": 492,
            "reset_requests": "12s",
            "limit_tokens": 200000,
            "remaining_tokens": 186000,
            "reset_tokens": "12s",
            "retry_count": 0,
            "backoff_strategy": "exponential",
            "jitter": True,
            "max_retries": 3,
            "retry_stop_reason": "not_needed",
            "latency_ms": 1800,
            "average_latency_ms": 1900,
            "p95_latency_ms": 2600,
            "timeout_ms": 10000,
            "budget_threshold": 5.0,
            "budget_spent": 0.42,
            "budget_action": "continue",
            "degraded_mode": "none",
            "max_output_tokens": 600,
            "output_token_policy": "short_answer_with_citations",
            "quality_check": "citation_and_schema_passed",
            "batch_candidate": False,
            "batch_status": "not_applicable",
            "custom_id_mapping": "not_applicable",
            "batch_expiration_policy": "not_applicable",
            "service_tier": "standard",
            "resource_unavailable_count": 0,
            "fallback_strategy": "not_needed",
            "fallback_cost_note": "standard_sync_path",
            "cache_eligible": True,
            "cached_tokens": 1024,
            "cache_write_tokens": 0,
            "cache_miss_reason": "none",
        },
        {
            "request_id": "req_2",
            "model": "gpt-example-mini",
            "model_choice_reason": "low_priority_batchable_eval",
            "input_tokens": 2100,
            "output_tokens": 500,
            "request_count": 1,
            "cost_estimate": 0.5,
            "limit_requests": 500,
            "remaining_requests": 491,
            "reset_requests": "12s",
            "limit_tokens": 200000,
            "remaining_tokens": 183400,
            "reset_tokens": "12s",
            "retry_count": 1,
            "backoff_strategy": "exponential",
            "jitter": True,
            "max_retries": 3,
            "retry_stop_reason": "success_after_retry",
            "latency_ms": 2500,
            "average_latency_ms": 1900,
            "p95_latency_ms": 2600,
            "timeout_ms": 10000,
            "budget_threshold": 5.0,
            "budget_spent": 0.92,
            "budget_action": "continue",
            "degraded_mode": "none",
            "max_output_tokens": 600,
            "output_token_policy": "short_answer_with_citations",
            "quality_check": "citation_and_schema_passed",
            "batch_candidate": True,
            "batch_status": "completed",
            "custom_id_mapping": "custom_id_to_request_id",
            "batch_expiration_policy": "retry_unfinished_after_24h_expiration",
            "service_tier": "flex",
            "resource_unavailable_count": 1,
            "fallback_strategy": "fallback_to_standard_after_429",
            "fallback_cost_note": "fallback_may_reduce_savings",
            "cache_eligible": True,
            "cached_tokens": 0,
            "cache_write_tokens": 1100,
            "cache_miss_reason": "first_request_with_new_prefix",
        },
        {
            "request_id": "req_3",
            "model": "gpt-example-mini",
            "model_choice_reason": "budget_guardrail_triggered",
            "input_tokens": 1700,
            "output_tokens": 250,
            "request_count": 1,
            "cost_estimate": 0.3,
            "limit_requests": 500,
            "remaining_requests": 490,
            "reset_requests": "12s",
            "limit_tokens": 200000,
            "remaining_tokens": 181450,
            "reset_tokens": "12s",
            "retry_count": 0,
            "backoff_strategy": "exponential",
            "jitter": True,
            "max_retries": 3,
            "retry_stop_reason": "not_needed",
            "latency_ms": 1400,
            "average_latency_ms": 1900,
            "p95_latency_ms": 2600,
            "timeout_ms": 10000,
            "budget_threshold": 1.0,
            "budget_spent": 1.22,
            "budget_action": "degrade",
            "degraded_mode": "skip_optional_summary",
            "max_output_tokens": 300,
            "output_token_policy": "terse_answer_only",
            "quality_check": "minimum_answer_passed",
            "batch_candidate": False,
            "batch_status": "not_applicable",
            "custom_id_mapping": "not_applicable",
            "batch_expiration_policy": "not_applicable",
            "service_tier": "standard",
            "resource_unavailable_count": 0,
            "fallback_strategy": "not_needed",
            "fallback_cost_note": "degraded_to_reduce_tokens",
            "cache_eligible": False,
            "cached_tokens": 0,
            "cache_write_tokens": 0,
            "cache_miss_reason": "dynamic_short_prompt",
        },
    ],
}


def percentile_95(values: list[int]) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(round(0.95 * (len(ordered) - 1))))
    return ordered[index]


def audit_run(run_name: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actual_average = int(mean(record["latency_ms"] for record in records))
    actual_p95 = percentile_95([record["latency_ms"] for record in records])
    rows: list[dict[str, Any]] = []
    for rule in AUDIT_RULES:
        missing_by_request = {
            record["request_id"]: [field for field in rule.required_fields if field not in record]
            for record in records
        }
        missing = {request_id: fields for request_id, fields in missing_by_request.items() if fields}
        rows.append(
            {
                "run": run_name,
                "rule_id": rule.rule_id,
                "passed": not missing,
                "missing_by_request": missing,
                "reason": rule.reason,
                "actual_average_latency_ms": actual_average,
                "actual_p95_latency_ms": actual_p95,
            }
        )
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for run in sorted({row["run"] for row in rows}):
        items = [row for row in rows if row["run"] == run]
        summary[run] = {
            "passed": sum(1 for item in items if item["passed"]),
            "total": len(items),
            "failed_rules": [item["rule_id"] for item in items if not item["passed"]],
            "average_latency_ms": items[0]["actual_average_latency_ms"],
            "p95_latency_ms": items[0]["actual_p95_latency_ms"],
        }
    return summary


def main() -> None:
    rows = [row for run, records in RUNS.items() for row in audit_run(run, records)]
    print(json.dumps({"summary": summarize(rows), "results": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
