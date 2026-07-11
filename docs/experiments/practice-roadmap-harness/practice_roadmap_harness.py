#!/usr/bin/env python3
"""Deterministic smoke harness for beginner practice projects.

The goal is not to reproduce OpenAI Cookbook behavior. It verifies that a
beginner-friendly local practice route can express structured output, tool
validation, grounded answers, eval cases, and a cost guard with traceable
pass/fail results using only the Python standard library.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    project: str
    expected: dict[str, Any]


CASES = [
    EvalCase("P1-structured-ok", "structured_output", {"schema_valid": True, "refusal_recorded": False}),
    EvalCase("P1-refusal", "structured_output", {"schema_valid": True, "refusal_recorded": True}),
    EvalCase("P2-tool-retry", "tool_calling", {"tool_executed": True, "validation_errors": 1}),
    EvalCase("P3-rag-grounded", "rag", {"grounded": True, "citations": ["source-card-rag"]}),
    EvalCase("P3-rag-unknown", "rag", {"grounded": False, "citations": []}),
    EvalCase("P8-budget-block", "production_check", {"allowed": False, "reason": "budget_exceeded"}),
]


def run_structured_output(case_id: str) -> dict[str, Any]:
    if case_id == "P1-refusal":
        payload = {"answer": None, "confidence": "low", "refusal": "outside supported scope"}
    else:
        payload = {"answer": "Start with a minimal JSON response.", "confidence": "medium", "refusal": None}
    schema_valid = set(payload) == {"answer", "confidence", "refusal"} and payload["confidence"] in {"low", "medium", "high"}
    return {
        "schema_valid": schema_valid,
        "refusal_recorded": payload["refusal"] is not None,
        "trace": ["model_output", "schema_check"],
    }


def run_tool_calling() -> dict[str, Any]:
    first_call = {"tool": "add", "arguments": {"a": 2, "b": "3"}}
    validation_errors = []
    if not isinstance(first_call["arguments"].get("b"), int):
        validation_errors.append("b must be integer")
    corrected_call = {"tool": "add", "arguments": {"a": 2, "b": 3}}
    result = corrected_call["arguments"]["a"] + corrected_call["arguments"]["b"]
    return {
        "tool_executed": result == 5,
        "validation_errors": len(validation_errors),
        "trace": ["tool_call_invalid", "validation_error", "tool_call_corrected", "tool_result"],
    }


def run_rag(case_id: str) -> dict[str, Any]:
    docs = {"source-card-rag": "RAG answers should cite retrieved source chunks."}
    if case_id == "P3-rag-unknown":
        return {"grounded": False, "citations": [], "trace": ["retrieve_empty", "refuse_unsupported"]}
    return {
        "grounded": True,
        "citations": ["source-card-rag"],
        "answer": docs["source-card-rag"],
        "trace": ["retrieve", "synthesize", "citation_check"],
    }


def run_production_check() -> dict[str, Any]:
    request = {"estimated_cost_usd": 1.75, "remaining_budget_usd": 1.00}
    allowed = request["estimated_cost_usd"] <= request["remaining_budget_usd"]
    return {
        "allowed": allowed,
        "reason": None if allowed else "budget_exceeded",
        "trace": ["estimate_cost", "budget_check", "deny_or_continue"],
    }


def run_case(case: EvalCase) -> dict[str, Any]:
    if case.project == "structured_output":
        observed = run_structured_output(case.case_id)
    elif case.project == "tool_calling":
        observed = run_tool_calling()
    elif case.project == "rag":
        observed = run_rag(case.case_id)
    elif case.project == "production_check":
        observed = run_production_check()
    else:
        raise ValueError(case.project)

    checks = {
        key: {"expected": expected, "observed": observed.get(key), "passed": observed.get(key) == expected}
        for key, expected in case.expected.items()
    }
    return {
        "case_id": case.case_id,
        "project": case.project,
        "passed": all(check["passed"] for check in checks.values()),
        "checks": checks,
        "observed": observed,
    }


def main() -> None:
    runs = [run_case(case) for case in CASES]
    summary = {
        "passed": sum(1 for run in runs if run["passed"]),
        "total": len(runs),
        "projects": sorted({case.project for case in CASES}),
        "failed_cases": [run["case_id"] for run in runs if not run["passed"]],
    }
    print(json.dumps({"summary": summary, "runs": runs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
