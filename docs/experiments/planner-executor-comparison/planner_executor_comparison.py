#!/usr/bin/env python3
"""Deterministic planner/executor comparison.

The experiment compares a single checklist loop, a one-shot planner/executor,
and a planner/executor with validation feedback on the same triage tasks. It
uses fake issues and repository files so the result is reproducible without a
model or framework dependency.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Task:
    task_id: str
    prompt: str
    expected_label: str
    required_evidence: tuple[str, ...]
    required_terms: tuple[str, ...]


@dataclass
class TraceEvent:
    strategy: str
    event: str
    details: dict[str, Any]
    timestamp: str = field(default_factory=utc_now)


REPO_FILES = {
    "issues/docs.md": "Install docs mention mkdoc, but the real command is mkdocs.",
    "issues/cache.md": "Login timeout after cache rollout. Health check red for auth service.",
    "services/auth/config.py": "CACHE_PORT = 6379",
    "deploy/cache.env": "CACHE_PORT=6380",
    "logs/auth.log": "ERROR auth cache connection refused cache.internal:6380",
    "issues/billing.md": "Billing export fails after schema migration; invoices show missing customer_id.",
    "services/billing/export.py": "SELECT invoice_id, total FROM invoices",
    "db/schema.sql": "CREATE TABLE invoices (invoice_id TEXT, customer_id TEXT, total INT)",
    "migrations/2026_07_add_customer_id.sql": "ALTER TABLE invoices ADD COLUMN customer_id TEXT NOT NULL",
}

TASKS = [
    Task("TASK-1", "Fix install docs typo", "documentation", ("issues/docs.md",), ("mkdocs",)),
    Task(
        "TASK-2",
        "Triage login timeout after cache deploy",
        "bug",
        ("issues/cache.md", "services/auth/config.py", "deploy/cache.env", "logs/auth.log"),
        ("cache", "6379", "6380"),
    ),
    Task(
        "TASK-3",
        "Assess billing export failure after schema migration",
        "bug",
        ("issues/billing.md", "services/billing/export.py", "db/schema.sql", "migrations/2026_07_add_customer_id.sql"),
        ("customer_id", "migration", "export"),
    ),
]


class ToolBox:
    def __init__(self, strategy: str) -> None:
        self.strategy = strategy
        self.trace: list[TraceEvent] = []

    def record(self, event: str, **details: Any) -> None:
        self.trace.append(TraceEvent(strategy=self.strategy, event=event, details=details))

    def read_file(self, path: str) -> str:
        self.record("tool_call", tool="read_file", path=path)
        result = REPO_FILES[path]
        self.record("tool_result", tool="read_file", path=path, result=result)
        return result


def classify(task: Task) -> str:
    text = task.prompt.lower()
    if "docs" in text or "typo" in text:
        return "documentation"
    if "timeout" in text or "fails" in text or "failure" in text:
        return "bug"
    return "triage"


def checklist_paths(task: Task) -> list[str]:
    if task.task_id == "TASK-1":
        return ["issues/docs.md"]
    if task.task_id == "TASK-2":
        return ["issues/cache.md", "services/auth/config.py", "deploy/cache.env", "logs/auth.log"]
    if task.task_id == "TASK-3":
        return ["issues/billing.md", "services/billing/export.py", "db/schema.sql", "migrations/2026_07_add_customer_id.sql"]
    return []


def one_shot_plan(task: Task) -> list[str]:
    if task.task_id == "TASK-1":
        return ["issues/docs.md"]
    if task.task_id == "TASK-2":
        return ["issues/cache.md", "services/auth/config.py", "deploy/cache.env", "logs/auth.log"]
    if task.task_id == "TASK-3":
        # The planner misses migrations because the plan is generated once from
        # a shallow template: issue -> service code -> schema.
        return ["issues/billing.md", "services/billing/export.py", "db/schema.sql"]
    return []


def recommendation(task: Task, label: str, evidence_text: dict[str, str]) -> str:
    joined = "\n".join(evidence_text.values())
    if task.task_id == "TASK-1":
        return "Documentation fix: use mkdocs in the install command."
    if task.task_id == "TASK-2" and "6379" in joined and "6380" in joined:
        return "Bug: cache port mismatch between config 6379 and deploy/log 6380."
    if task.task_id == "TASK-3" and "customer_id" in joined and "ALTER TABLE" in joined:
        return "Bug: billing export query misses customer_id added by migration."
    if task.task_id == "TASK-3" and "customer_id" in joined:
        return "Bug: billing export may be affected by schema customer_id, but migration evidence is missing."
    return f"{label}: evidence is incomplete."


def single_checklist_loop(task: Task) -> dict[str, Any]:
    tools = ToolBox("single_checklist_loop")
    label = classify(task)
    evidence_text: dict[str, str] = {}
    for path in checklist_paths(task):
        evidence_text[path] = tools.read_file(path)
    return make_run("single_checklist_loop", task, label, recommendation(task, label, evidence_text), list(evidence_text), tools.trace, plan_steps=0, replans=0)


def planner_executor_once(task: Task) -> dict[str, Any]:
    tools = ToolBox("planner_executor_once")
    label = classify(task)
    plan = one_shot_plan(task)
    tools.record("plan_created", steps=plan)
    evidence_text = {path: tools.read_file(path) for path in plan}
    return make_run("planner_executor_once", task, label, recommendation(task, label, evidence_text), list(evidence_text), tools.trace, plan_steps=len(plan), replans=0)


def planner_executor_with_feedback(task: Task) -> dict[str, Any]:
    tools = ToolBox("planner_executor_with_feedback")
    label = classify(task)
    plan = one_shot_plan(task)
    tools.record("plan_created", steps=plan)
    evidence_text = {path: tools.read_file(path) for path in plan}

    missing = [path for path in task.required_evidence if path not in evidence_text]
    replans = 0
    if missing:
        replans += 1
        tools.record("validation_failed", missing_evidence=missing)
        tools.record("plan_revised", added_steps=missing)
        for path in missing:
            evidence_text[path] = tools.read_file(path)

    return make_run(
        "planner_executor_with_feedback",
        task,
        label,
        recommendation(task, label, evidence_text),
        list(evidence_text),
        tools.trace,
        plan_steps=len(plan) + len(missing),
        replans=replans,
    )


def make_run(
    strategy: str,
    task: Task,
    label: str,
    output: str,
    evidence: list[str],
    trace: list[TraceEvent],
    plan_steps: int,
    replans: int,
) -> dict[str, Any]:
    lowered = output.lower()
    has_terms = all(term.lower() in lowered for term in task.required_terms)
    has_evidence = all(path in evidence for path in task.required_evidence)
    success = label == task.expected_label and has_terms and has_evidence
    return {
        "strategy": strategy,
        "task_id": task.task_id,
        "label": label,
        "output": output,
        "evidence": evidence,
        "success": success,
        "tool_calls": sum(1 for event in trace if event.event == "tool_call"),
        "plan_steps": plan_steps,
        "replans": replans,
        "trace": [event.__dict__ for event in trace],
    }


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    by_strategy: dict[str, list[dict[str, Any]]] = {}
    for run in runs:
        by_strategy.setdefault(run["strategy"], []).append(run)
    return {
        strategy: {
            "successes": sum(1 for run in items if run["success"]),
            "total": len(items),
            "tool_calls": sum(run["tool_calls"] for run in items),
            "plan_steps": sum(run["plan_steps"] for run in items),
            "replans": sum(run["replans"] for run in items),
            "failed_tasks": [run["task_id"] for run in items if not run["success"]],
        }
        for strategy, items in by_strategy.items()
    }


def main() -> None:
    runs: list[dict[str, Any]] = []
    for task in TASKS:
        runs.extend([single_checklist_loop(task), planner_executor_once(task), planner_executor_with_feedback(task)])
    print(json.dumps({"summary": summarize(runs), "runs": runs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
