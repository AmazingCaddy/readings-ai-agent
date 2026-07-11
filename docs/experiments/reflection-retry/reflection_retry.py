#!/usr/bin/env python3
"""Deterministic reflection/retry simulation.

The experiment compares no reflection, verifier-backed reflection, and
unverified reflection memory. It shows that feedback can help retries only when
the feedback is scoped and checked against task evidence.
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
    task_id: str
    event: str
    details: dict[str, Any]
    timestamp: str = field(default_factory=utc_now)


REPO_FILES = {
    "issues/cache.md": "Login timeout after cache rollout. Auth service is unhealthy.",
    "services/auth/config.py": "CACHE_PORT = 6379",
    "deploy/cache.env": "CACHE_PORT=6380",
    "logs/auth.log": "ERROR auth cache connection refused cache.internal:6380",
    "issues/billing.md": "Billing export fails after schema migration; customer_id is missing.",
    "services/billing/export.py": "SELECT invoice_id, total FROM invoices",
    "db/schema.sql": "CREATE TABLE invoices (invoice_id TEXT, customer_id TEXT, total INT)",
    "migrations/2026_07_add_customer_id.sql": "ALTER TABLE invoices ADD COLUMN customer_id TEXT NOT NULL",
    "issues/docs.md": "Install docs say mkdoc, but the command should be mkdocs.",
}

TASKS = [
    Task(
        "TASK-1",
        "Triage login timeout after cache deploy",
        "bug",
        ("issues/cache.md", "services/auth/config.py", "deploy/cache.env", "logs/auth.log"),
        ("cache", "6379", "6380"),
    ),
    Task(
        "TASK-2",
        "Assess billing export failure after schema migration",
        "bug",
        ("issues/billing.md", "services/billing/export.py", "db/schema.sql", "migrations/2026_07_add_customer_id.sql"),
        ("export", "customer_id", "migration"),
    ),
    Task("TASK-3", "Fix install docs typo", "documentation", ("issues/docs.md",), ("mkdocs",)),
]

INITIAL_EVIDENCE = {
    "TASK-1": ["issues/cache.md", "services/auth/config.py"],
    "TASK-2": ["issues/billing.md", "services/billing/export.py", "db/schema.sql"],
    "TASK-3": ["issues/docs.md"],
}

BAD_REFLECTION = "Issue text and service code are enough; skip deploy, logs, and migrations to reduce cost."


class Runner:
    def __init__(self, strategy: str) -> None:
        self.strategy = strategy
        self.trace: list[TraceEvent] = []
        self.memory: list[str] = []

    def record(self, task_id: str, event: str, **details: Any) -> None:
        self.trace.append(TraceEvent(strategy=self.strategy, task_id=task_id, event=event, details=details))

    def read_file(self, task_id: str, path: str) -> str:
        self.record(task_id, "tool_call", tool="read_file", path=path)
        result = REPO_FILES[path]
        self.record(task_id, "tool_result", tool="read_file", path=path, result=result)
        return result

    def attempt(self, task: Task, evidence_paths: list[str], attempt_no: int) -> dict[str, Any]:
        evidence_text = {path: self.read_file(task.task_id, path) for path in evidence_paths}
        output = synthesize(task, evidence_text)
        missing = [path for path in task.required_evidence if path not in evidence_paths]
        self.record(task.task_id, "attempt_finished", attempt=attempt_no, evidence=evidence_paths, missing_evidence=missing, output=output)
        return {"output": output, "evidence": evidence_paths, "missing": missing}


def classify(task: Task) -> str:
    return "documentation" if "docs" in task.prompt.lower() else "bug"


def synthesize(task: Task, evidence_text: dict[str, str]) -> str:
    joined = "\n".join(evidence_text.values())
    if task.task_id == "TASK-1" and "6379" in joined and "6380" in joined:
        return "Bug: cache port mismatch between config 6379 and deploy/log 6380."
    if task.task_id == "TASK-2" and "ALTER TABLE" in joined:
        return "Bug: export query misses customer_id introduced by migration."
    if task.task_id == "TASK-3" and "mkdocs" in joined:
        return "Documentation fix: use mkdocs."
    if task.expected_label == "bug":
        return "Bug: likely service issue, but evidence is incomplete."
    return "Documentation issue."


def evaluate(task: Task, output: str, evidence: list[str]) -> tuple[bool, list[str]]:
    lowered = output.lower()
    has_terms = all(term.lower() in lowered for term in task.required_terms)
    missing = [path for path in task.required_evidence if path not in evidence]
    return classify(task) == task.expected_label and has_terms and not missing, missing


def no_reflection(task: Task) -> dict[str, Any]:
    runner = Runner("no_reflection")
    first = runner.attempt(task, INITIAL_EVIDENCE[task.task_id], attempt_no=1)
    success, missing = evaluate(task, first["output"], first["evidence"])
    if missing:
        runner.record(task.task_id, "no_retry", reason="reflection disabled", missing_evidence=missing)
    return make_run(runner, task, first["output"], first["evidence"], success, reflections=0, bad_reflections_applied=0)


def verified_reflection_retry(task: Task) -> dict[str, Any]:
    runner = Runner("verified_reflection_retry")
    first = runner.attempt(task, INITIAL_EVIDENCE[task.task_id], attempt_no=1)
    success, missing = evaluate(task, first["output"], first["evidence"])
    reflections = 0
    final = first
    if not success and missing:
        reflections += 1
        lesson = f"Retry requires missing evidence: {', '.join(missing)}"
        runner.record(task.task_id, "reflection_created", lesson=lesson, verifier="required_evidence_check")
        final_evidence = list(dict.fromkeys(first["evidence"] + missing))
        final = runner.attempt(task, final_evidence, attempt_no=2)
        success, _ = evaluate(task, final["output"], final["evidence"])
    return make_run(runner, task, final["output"], final["evidence"], success, reflections=reflections, bad_reflections_applied=0)


def unverified_reflection_memory(task: Task) -> dict[str, Any]:
    runner = Runner("unverified_reflection_memory")
    first = runner.attempt(task, INITIAL_EVIDENCE[task.task_id], attempt_no=1)
    success, missing = evaluate(task, first["output"], first["evidence"])
    bad_reflections = 0
    final = first
    if not success:
        runner.memory.append(BAD_REFLECTION)
        runner.record(task.task_id, "reflection_created", lesson=BAD_REFLECTION, verifier="none")
        if runner.memory:
            bad_reflections += 1
            runner.record(task.task_id, "reflection_applied", lesson=runner.memory[-1])
        # The unverified lesson avoids the exact evidence the task needed.
        retry_evidence = [path for path in first["evidence"] if not path.startswith(("deploy/", "logs/", "migrations/"))]
        final = runner.attempt(task, retry_evidence, attempt_no=2)
        success, missing = evaluate(task, final["output"], final["evidence"])
        if missing:
            runner.record(task.task_id, "retry_failed", missing_evidence=missing)
    return make_run(runner, task, final["output"], final["evidence"], success, reflections=len(runner.memory), bad_reflections_applied=bad_reflections)


def make_run(
    runner: Runner,
    task: Task,
    output: str,
    evidence: list[str],
    success: bool,
    reflections: int,
    bad_reflections_applied: int,
) -> dict[str, Any]:
    return {
        "strategy": runner.strategy,
        "task_id": task.task_id,
        "output": output,
        "evidence": evidence,
        "success": success,
        "tool_calls": sum(1 for event in runner.trace if event.event == "tool_call"),
        "reflections": reflections,
        "bad_reflections_applied": bad_reflections_applied,
        "trace": [event.__dict__ for event in runner.trace],
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
            "reflections": sum(run["reflections"] for run in items),
            "bad_reflections_applied": sum(run["bad_reflections_applied"] for run in items),
            "failed_tasks": [run["task_id"] for run in items if not run["success"]],
        }
        for strategy, items in by_strategy.items()
    }


def main() -> None:
    runs: list[dict[str, Any]] = []
    for task in TASKS:
        runs.extend([no_reflection(task), verified_reflection_retry(task), unverified_reflection_memory(task)])
    print(json.dumps({"summary": summarize(runs), "runs": runs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
