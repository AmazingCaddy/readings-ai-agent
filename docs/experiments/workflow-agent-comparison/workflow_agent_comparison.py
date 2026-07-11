#!/usr/bin/env python3
"""Deterministic workflow vs agent-loop comparison.

This experiment uses fake issues, fake repository files, and deterministic
policies. It compares a fixed workflow, a workflow-agent hybrid, and a
ReAct-like tool loop on the same issue-triage tasks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Issue:
    issue_id: str
    title: str
    body: str


@dataclass(frozen=True)
class Task:
    issue: Issue
    expected_label: str
    required_terms: tuple[str, ...]
    required_evidence: tuple[str, ...]


@dataclass
class TraceEvent:
    strategy: str
    event: str
    details: dict[str, Any]
    timestamp: str = field(default_factory=utc_now)


ISSUES = {
    "ISSUE-1": Issue(
        issue_id="ISSUE-1",
        title="Typo in install command",
        body="The README says uv run mkdoc build, but the command should be uv run mkdocs build.",
    ),
    "ISSUE-2": Issue(
        issue_id="ISSUE-2",
        title="Login timeout after cache deploy",
        body="Users report login timeouts after the cache rollout. Auth service health check is red.",
    ),
    "ISSUE-3": Issue(
        issue_id="ISSUE-3",
        title="Export conversation summary as CSV",
        body="A customer asks for a CSV export option for the conversation summary page.",
    ),
}

REPO_FILES = {
    "README.md": "Install with: uv run mkdocs build --strict",
    "services/auth/config.py": "CACHE_HOST = 'cache.internal'\nCACHE_PORT = 6379\nTIMEOUT_SECONDS = 2",
    "deploy/cache.env": "CACHE_PORT=6380\nCACHE_VERSION=2026-07-11",
    "logs/auth.log": "ERROR auth cache connection refused cache.internal:6380 during login",
    "product/export.md": "CSV export is a proposed feature, not an incident fix.",
}

TASKS = [
    Task(ISSUES["ISSUE-1"], "documentation", ("mkdocs", "README"), ("issue_body",)),
    Task(ISSUES["ISSUE-2"], "bug", ("cache", "6379", "6380", "config"), ("logs/auth.log", "services/auth/config.py", "deploy/cache.env")),
    Task(ISSUES["ISSUE-3"], "feature", ("CSV", "feature"), ("issue_body",)),
]


class ToolBox:
    def __init__(self, strategy: str) -> None:
        self.strategy = strategy
        self.trace: list[TraceEvent] = []

    def record(self, event: str, **details: Any) -> None:
        self.trace.append(TraceEvent(strategy=self.strategy, event=event, details=details))

    def read_issue(self, issue: Issue) -> dict[str, str]:
        self.record("tool_call", tool="read_issue", issue_id=issue.issue_id)
        result = {"title": issue.title, "body": issue.body}
        self.record("tool_result", tool="read_issue", result=result)
        return result

    def search_repo(self, query: str) -> list[str]:
        self.record("tool_call", tool="search_repo", query=query)
        terms = query.lower().split()
        matches = [path for path, text in REPO_FILES.items() if any(term in (path + " " + text).lower() for term in terms)]
        self.record("tool_result", tool="search_repo", result=matches)
        return matches

    def read_file(self, path: str) -> str:
        self.record("tool_call", tool="read_file", path=path)
        result = REPO_FILES[path]
        self.record("tool_result", tool="read_file", path=path, result=result)
        return result


def classify(issue_text: str) -> str:
    lowered = issue_text.lower()
    if "typo" in lowered or "readme" in lowered or "mkdocs" in lowered:
        return "documentation"
    if "timeout" in lowered or "health check" in lowered or "error" in lowered:
        return "bug"
    if "export" in lowered or "csv" in lowered or "customer asks" in lowered:
        return "feature"
    return "triage"


def fixed_workflow(task: Task) -> dict[str, Any]:
    tools = ToolBox("fixed_workflow")
    issue = tools.read_issue(task.issue)
    issue_text = issue["title"] + "\n" + issue["body"]
    label = classify(issue_text)
    if label == "documentation":
        recommendation = "Fix README command to use uv run mkdocs build."
    elif label == "bug":
        recommendation = "Route to engineering as a login timeout bug; root cause not inspected."
    elif label == "feature":
        recommendation = "Treat CSV export as a feature request for product triage."
    else:
        recommendation = "Needs manual triage."
    return make_run("fixed_workflow", task, label, recommendation, ["issue_body"], tools.trace)


def workflow_agent_hybrid(task: Task) -> dict[str, Any]:
    tools = ToolBox("workflow_agent_hybrid")
    issue = tools.read_issue(task.issue)
    issue_text = issue["title"] + "\n" + issue["body"]
    label = classify(issue_text)
    evidence = ["issue_body"]
    recommendation = ""

    if label == "bug":
        tools.search_repo("cache timeout auth")
        log = tools.read_file("logs/auth.log")
        config = tools.read_file("services/auth/config.py")
        deploy = tools.read_file("deploy/cache.env")
        evidence.extend(["logs/auth.log", "services/auth/config.py", "deploy/cache.env"])
        recommendation = f"Investigate cache config port mismatch: {config.splitlines()[1]} but deploy uses {deploy.splitlines()[0]}; log says {log}."
    elif label == "documentation":
        recommendation = "Fix README command to use uv run mkdocs build."
    elif label == "feature":
        recommendation = "Treat CSV export as a feature request for product triage."
    else:
        recommendation = "Needs manual triage."

    return make_run("workflow_agent_hybrid", task, label, recommendation, evidence, tools.trace)


def react_like_loop(task: Task) -> dict[str, Any]:
    tools = ToolBox("react_like_loop")
    issue = tools.read_issue(task.issue)
    issue_text = issue["title"] + "\n" + issue["body"]
    label = classify(issue_text)
    evidence = ["issue_body"]

    tools.record("decision", action="classify", label=label)
    if label == "bug":
        matches = tools.search_repo("cache timeout auth")
        for path in ["logs/auth.log", "services/auth/config.py", "deploy/cache.env"]:
            if path in matches:
                tools.read_file(path)
                evidence.append(path)
        recommendation = "Cache config mismatch likely causes login timeout: service uses 6379 while deploy/logs show 6380."
    elif label == "feature":
        tools.record("decision", action="seek_extra_context", reason="feature request may need product context")
        tools.search_repo("CSV export")
        tools.read_file("product/export.md")
        recommendation = "CSV export is a feature request; add product review rather than incident fix."
    elif label == "documentation":
        recommendation = "Fix README command to use uv run mkdocs build."
    else:
        recommendation = "Needs manual triage."

    tools.record("decision", action="stop", reason="recommendation prepared")
    return make_run("react_like_loop", task, label, recommendation, evidence, tools.trace)


def make_run(strategy: str, task: Task, label: str, recommendation: str, evidence: list[str], trace: list[TraceEvent]) -> dict[str, Any]:
    text = (label + " " + recommendation).lower()
    has_terms = all(term.lower() in text for term in task.required_terms)
    has_evidence = all(item in evidence for item in task.required_evidence)
    success = label == task.expected_label and has_terms and has_evidence
    return {
        "strategy": strategy,
        "issue_id": task.issue.issue_id,
        "label": label,
        "recommendation": recommendation,
        "evidence": evidence,
        "success": success,
        "tool_calls": sum(1 for event in trace if event.event == "tool_call"),
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
            "failed_issues": [run["issue_id"] for run in items if not run["success"]],
        }
        for strategy, items in by_strategy.items()
    }


def main() -> None:
    runs: list[dict[str, Any]] = []
    for task in TASKS:
        runs.extend([fixed_workflow(task), workflow_agent_hybrid(task), react_like_loop(task)])
    result = {"summary": summarize(runs), "runs": runs}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
