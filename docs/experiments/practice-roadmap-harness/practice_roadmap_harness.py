#!/usr/bin/env python3
"""Deterministic smoke harness for beginner practice projects.

The goal is not to reproduce OpenAI Cookbook behavior. It verifies that a
beginner-friendly local practice route can express structured output, tool
validation, grounded answers, eval cases, and a cost guard with traceable
pass/fail results using only the Python standard library. It also audits whether
practice-project cards contain the minimum fields a beginner needs before
following a recipe: prerequisites, commands, acceptance checks, trace fields,
failure examples, references, and boundary notes.
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


@dataclass(frozen=True)
class ProjectCard:
    project_id: str
    title: str
    prerequisites: tuple[str, ...]
    setup_commands: tuple[str, ...]
    run_commands: tuple[str, ...]
    acceptance_checks: tuple[str, ...]
    trace_fields: tuple[str, ...]
    failure_examples: tuple[str, ...]
    references: tuple[str, ...]
    boundaries: tuple[str, ...]


CASES = [
    EvalCase("P1-structured-ok", "structured_output", {"schema_valid": True, "refusal_recorded": False}),
    EvalCase("P1-refusal", "structured_output", {"schema_valid": True, "refusal_recorded": True}),
    EvalCase("P2-tool-retry", "tool_calling", {"tool_executed": True, "validation_errors": 1}),
    EvalCase("P3-rag-grounded", "rag", {"grounded": True, "citations": ["source-card-rag"]}),
    EvalCase("P3-rag-unknown", "rag", {"grounded": False, "citations": []}),
    EvalCase("P8-budget-block", "production_check", {"allowed": False, "reason": "budget_exceeded"}),
]

PROJECT_CARDS = [
    ProjectCard(
        project_id="P1",
        title="structured_output_minimal_qa",
        prerequisites=("uv", "python>=3.11", "optional_openai_api_key"),
        setup_commands=("uv run python --version",),
        run_commands=("uv run python docs/experiments/practice-roadmap-harness/practice_roadmap_harness.py",),
        acceptance_checks=("schema_valid", "refusal_recorded_when_needed", "five_test_questions"),
        trace_fields=("input", "output", "schema_check", "refusal"),
        failure_examples=("schema_missing_refusal", "unsupported_scope_refusal"),
        references=("openai_structured_outputs_docs", "openai_cookbook_structured_outputs"),
        boundaries=("local_control_does_not_validate_real_api", "schema_valid_is_not_fact_valid"),
    ),
    ProjectCard(
        project_id="P2",
        title="tool_calling_with_validation",
        prerequisites=("uv", "python>=3.11", "mock_tool"),
        setup_commands=("uv run python --version",),
        run_commands=("uv run python docs/experiments/tool-calling-validation/tool_calling_validation.py",),
        acceptance_checks=("schema_present", "invalid_args_rejected", "corrected_tool_call_executed"),
        trace_fields=("tool_call", "validation_error", "tool_result"),
        failure_examples=("schema_valid_business_invalid_argument",),
        references=("openai_function_calling_docs", "tool_calling_validation_result"),
        boundaries=("function_calling_does_not_execute_tools", "real_model_retry_unvalidated"),
    ),
    ProjectCard(
        project_id="P3",
        title="rag_with_citations",
        prerequisites=("uv", "python>=3.11", "local_markdown_sources"),
        setup_commands=("uv run python --version",),
        run_commands=("uv run python docs/experiments/rag-pipeline/rag_pipeline_simulation.py",),
        acceptance_checks=("retrieval_trace_present", "citation_present", "unsupported_question_refused"),
        trace_fields=("query", "retrieved_chunks", "citations", "grounded"),
        failure_examples=("missing_citation", "unsupported_grounded_claim", "top_k_misses_required_source"),
        references=("rag_paper", "llamaindex_docs", "openai_file_search_docs"),
        boundaries=("keyword_control_does_not_validate_embeddings", "real_llm_faithfulness_unvalidated"),
    ),
    ProjectCard(
        project_id="P7",
        title="trace_aware_eval_harness",
        prerequisites=("uv", "python>=3.11", "saved_trace_fixtures"),
        setup_commands=("uv run python --version",),
        run_commands=("uv run python docs/experiments/trace-aware-eval/trace_aware_eval.py",),
        acceptance_checks=("cases_have_expected_behavior", "trace_aware_errors_detected", "failure_category_recorded"),
        trace_fields=("tool_call", "tool_result", "tool_error", "approval", "final_response"),
        failure_examples=("final_answer_passes_but_missing_approval", "tool_error_not_recovered"),
        references=("openai_evaluation_guides", "langsmith_docs", "phoenix_docs"),
        boundaries=("automatic_scorer_is_not_truth", "real_llm_judge_unvalidated"),
    ),
    ProjectCard(
        project_id="P8",
        title="production_readiness_check",
        prerequisites=("uv", "python>=3.11", "budget_threshold", "redaction_policy"),
        setup_commands=("uv run python --version",),
        run_commands=(
            "uv run python docs/experiments/production-cost-latency-rate-limit/production_cost_latency_rate_limit.py",
            "uv run python docs/experiments/production-safety-data-governance/production_safety_data_governance.py",
        ),
        acceptance_checks=("budget_gate", "rate_limit_fields", "data_flow_fields", "trace_redaction"),
        trace_fields=("usage", "latency", "rate_limit_headers", "data_flow", "redaction"),
        failure_examples=("budget_exceeded", "missing_delete_path", "secret_in_trace"),
        references=("openai_production_docs", "openai_safety_data_controls_docs", "openai_cookbook_cost_rate_limit"),
        boundaries=("field_audit_does_not_validate_real_account", "cost_and_latency_require_real_logs"),
    ),
    ProjectCard(
        project_id="ADV-REPO",
        title="repo_issue_agent_toy",
        prerequisites=("uv", "python>=3.11", "pytest", "isolated_toy_repo"),
        setup_commands=("uv run python --version",),
        run_commands=("uv run --with pytest python docs/experiments/real-repo-issue-agent-toy/real_repo_issue_agent_toy.py",),
        acceptance_checks=("initial_tests_fail", "final_tests_pass", "implementation_only_diff", "approval_recorded"),
        trace_fields=("command", "diff", "test_output", "approval", "redaction"),
        failure_examples=("tests_modified_instead_of_code", "unapproved_env_read", "secret_marker_in_trace"),
        references=("swe_agent_paper", "mini_swe_agent_docs", "real_repo_issue_agent_toy_result"),
        boundaries=("toy_repo_does_not_validate_real_coding_agent", "real_model_confirm_mode_unvalidated"),
    ),
]

REQUIRED_CARD_FIELDS = (
    "prerequisites",
    "setup_commands",
    "run_commands",
    "acceptance_checks",
    "trace_fields",
    "failure_examples",
    "references",
    "boundaries",
)


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


def audit_project_card(card: ProjectCard) -> dict[str, Any]:
    checks = {
        field_name: {
            "count": len(getattr(card, field_name)),
            "passed": len(getattr(card, field_name)) > 0,
        }
        for field_name in REQUIRED_CARD_FIELDS
    }
    checks["has_repeatable_command"] = {
        "count": sum(1 for command in card.run_commands if command.startswith("uv run ")),
        "passed": any(command.startswith("uv run ") for command in card.run_commands),
    }
    checks["has_boundary_note"] = {
        "count": len(card.boundaries),
        "passed": any("unvalidated" in note or "does_not_validate" in note for note in card.boundaries),
    }
    return {
        "project_id": card.project_id,
        "title": card.title,
        "passed": all(check["passed"] for check in checks.values()),
        "checks": checks,
    }


def main() -> None:
    runs = [run_case(case) for case in CASES]
    card_audits = [audit_project_card(card) for card in PROJECT_CARDS]
    summary = {
        "passed": sum(1 for run in runs if run["passed"]),
        "total": len(runs),
        "projects": sorted({case.project for case in CASES}),
        "failed_cases": [run["case_id"] for run in runs if not run["passed"]],
    }
    readiness_summary = {
        "passed": sum(1 for audit in card_audits if audit["passed"]),
        "total": len(card_audits),
        "required_fields": list(REQUIRED_CARD_FIELDS),
        "failed_projects": [audit["project_id"] for audit in card_audits if not audit["passed"]],
    }
    print(
        json.dumps(
            {"summary": summary, "readiness_summary": readiness_summary, "runs": runs, "project_card_audits": card_audits},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
