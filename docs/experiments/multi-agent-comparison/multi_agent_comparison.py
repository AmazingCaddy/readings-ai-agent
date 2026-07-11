#!/usr/bin/env python3
"""Deterministic multi-agent comparison.

The experiment compares a single checklist workflow, an ungoverned role-based
multi-agent setup, and a flow-controlled multi-agent setup on the same writing
tasks. It uses fake documents and deterministic roles so the result is
reproducible without model or framework dependencies.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Task:
    task_id: str
    prompt: str
    required_docs: tuple[str, ...]
    required_terms: tuple[str, ...]


@dataclass
class TraceEvent:
    strategy: str
    task_id: str
    actor: str
    event: str
    details: dict[str, Any]
    timestamp: str = field(default_factory=utc_now)


DOCS = {
    "spec.md": "Feature: export summaries. Format: CSV. User needs simple spreadsheet review.",
    "security.md": "External sharing requires HITL approval and audit logging before release.",
    "cost.md": "Large exports must include cost budget and rate limit notes.",
    "feedback.md": "Beginners prefer concise steps, examples, and clear failure cases.",
}

TASKS = [
    Task("TASK-1", "Draft CSV export note", ("spec.md",), ("CSV", "export")),
    Task(
        "TASK-2",
        "Draft launch note for external CSV export",
        ("spec.md", "security.md", "cost.md"),
        ("CSV", "HITL", "audit", "cost"),
    ),
    Task(
        "TASK-3",
        "Draft beginner tutorial note for CSV export",
        ("spec.md", "feedback.md"),
        ("CSV", "beginners", "examples"),
    ),
]


class RunContext:
    def __init__(self, strategy: str, task: Task) -> None:
        self.strategy = strategy
        self.task = task
        self.trace: list[TraceEvent] = []
        self.reads: list[str] = []
        self.messages = 0
        self.conflicts = 0

    def record(self, actor: str, event: str, **details: Any) -> None:
        self.trace.append(TraceEvent(strategy=self.strategy, task_id=self.task.task_id, actor=actor, event=event, details=details))

    def read_doc(self, actor: str, path: str) -> str:
        self.record(actor, "tool_call", tool="read_doc", path=path)
        self.reads.append(path)
        result = DOCS[path]
        self.record(actor, "tool_result", tool="read_doc", path=path, result=result)
        return result

    def message(self, actor: str, to: str, content: str) -> None:
        self.messages += 1
        self.record(actor, "message", to=to, content=content)


def synthesize(task: Task, docs: dict[str, str], include_warning: bool = False) -> str:
    text = " ".join(docs.values())
    parts: list[str] = []
    if "CSV" in text:
        parts.append("CSV export")
    if "HITL" in text:
        parts.append("HITL approval")
    if "audit" in text:
        parts.append("audit logging")
    if "cost" in text:
        parts.append("cost budget")
    if "Beginners" in text:
        parts.append("beginners need examples")
    if include_warning:
        parts.append("conflict unresolved")
    return "; ".join(parts) if parts else "Draft is incomplete."


def evaluate(task: Task, output: str, evidence: list[str]) -> tuple[bool, list[str], list[str]]:
    missing_docs = [path for path in task.required_docs if path not in evidence]
    missing_terms = [term for term in task.required_terms if term.lower() not in output.lower()]
    return not missing_docs and not missing_terms and "conflict unresolved" not in output.lower(), missing_docs, missing_terms


def single_checklist(task: Task) -> dict[str, Any]:
    ctx = RunContext("single_checklist", task)
    docs = {path: ctx.read_doc("workflow", path) for path in task.required_docs}
    output = synthesize(task, docs)
    return make_run(ctx, output)


def ungoverned_multi_agent(task: Task) -> dict[str, Any]:
    ctx = RunContext("ungoverned_multi_agent", task)
    docs: dict[str, str] = {}

    # Role agents choose their own context. This intentionally creates duplicate
    # reads and misses cross-cutting evidence for some tasks.
    researcher_docs = ["spec.md"]
    writer_docs = ["spec.md"]
    reviewer_docs = ["security.md"] if "external" in task.prompt.lower() else []

    for path in researcher_docs:
        docs[path] = ctx.read_doc("researcher", path)
    ctx.message("researcher", "writer", "Found product spec context.")

    writer_view = {path: ctx.read_doc("writer", path) for path in writer_docs}
    ctx.message("writer", "reviewer", "Draft prepared from available context.")

    for path in reviewer_docs:
        docs[path] = ctx.read_doc("reviewer", path)
    if reviewer_docs:
        ctx.conflicts += 1
        ctx.message("reviewer", "writer", "Security requirement conflicts with draft scope.")

    merged_docs = {**docs, **writer_view}
    output = synthesize(task, merged_docs, include_warning=ctx.conflicts > 0)
    return make_run(ctx, output)


def flow_controlled_multi_agent(task: Task) -> dict[str, Any]:
    ctx = RunContext("flow_controlled_multi_agent", task)
    ctx.record("flow", "plan_created", required_docs=list(task.required_docs), roles=["researcher", "writer", "reviewer"])

    docs: dict[str, str] = {}
    for path in task.required_docs:
        actor = "researcher" if path in {"spec.md", "feedback.md"} else "reviewer"
        docs[path] = ctx.read_doc(actor, path)
        ctx.message(actor, "flow", f"Evidence ready: {path}")

    ctx.message("flow", "writer", "Write only from verified required evidence.")
    output = synthesize(task, docs)
    success, missing_docs, missing_terms = evaluate(task, output, list(docs))
    ctx.record("reviewer", "review_completed", success=success, missing_docs=missing_docs, missing_terms=missing_terms)
    if not success:
        ctx.conflicts += 1
    return make_run(ctx, output)


def make_run(ctx: RunContext, output: str) -> dict[str, Any]:
    evidence = list(ctx.reads)
    unique_evidence = sorted(set(evidence))
    success, missing_docs, missing_terms = evaluate(ctx.task, output, unique_evidence)
    read_counts = Counter(evidence)
    duplicate_reads = sum(count - 1 for count in read_counts.values() if count > 1)
    return {
        "strategy": ctx.strategy,
        "task_id": ctx.task.task_id,
        "output": output,
        "evidence": unique_evidence,
        "success": success,
        "tool_calls": len(evidence),
        "messages": ctx.messages,
        "conflicts": ctx.conflicts,
        "duplicate_reads": duplicate_reads,
        "missing_docs": missing_docs,
        "missing_terms": missing_terms,
        "trace": [event.__dict__ for event in ctx.trace],
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
            "messages": sum(run["messages"] for run in items),
            "conflicts": sum(run["conflicts"] for run in items),
            "duplicate_reads": sum(run["duplicate_reads"] for run in items),
            "failed_tasks": [run["task_id"] for run in items if not run["success"]],
        }
        for strategy, items in by_strategy.items()
    }


def main() -> None:
    runs: list[dict[str, Any]] = []
    for task in TASKS:
        runs.extend([single_checklist(task), ungoverned_multi_agent(task), flow_controlled_multi_agent(task)])
    print(json.dumps({"summary": summarize(runs), "runs": runs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
