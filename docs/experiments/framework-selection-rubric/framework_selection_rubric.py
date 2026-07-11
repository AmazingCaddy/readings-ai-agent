#!/usr/bin/env python3
"""Deterministic framework-selection rubric simulation.

This experiment does not run real frameworks. It checks whether the handbook's
framework-comparison dimensions can produce traceable recommendations from a
fixed task profile. The output supports a learning rubric, not claims about
real framework performance.
"""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class FrameworkProfile:
    name: str
    capabilities: set[str]
    cautions: tuple[str, ...]


@dataclass(frozen=True)
class TaskProfile:
    task_id: str
    description: str
    required: set[str]
    nice_to_have: set[str]
    avoid: set[str]


FRAMEWORKS = [
    FrameworkProfile(
        "OpenAI Agents SDK",
        {"tool_loop", "tracing", "guardrails", "handoff", "sessions", "lightweight_sdk"},
        ("OpenAI ecosystem coupling", "application still owns permissions and eval"),
    ),
    FrameworkProfile(
        "LangGraph",
        {"state_graph", "durable_execution", "human_in_loop", "persistence", "branching", "retries", "tracing"},
        ("graph concepts add learning cost", "framework terms are not universal definitions"),
    ),
    FrameworkProfile(
        "LlamaIndex",
        {"rag", "data_connectors", "indexing", "retrieval", "query_engine", "metadata", "evaluation"},
        ("data/RAG strength does not automatically solve workflow permissions",),
    ),
    FrameworkProfile(
        "AutoGen",
        {"multi_agent", "agent_chat", "teams", "group_chat", "coordination", "tracing"},
        ("multi-agent coordination can increase cost and debugging complexity",),
    ),
    FrameworkProfile(
        "CrewAI",
        {"multi_agent", "crews", "flows", "coordination", "role_tasks"},
        ("source confidence is lower than official API specs", "marketing examples need validation"),
    ),
    FrameworkProfile(
        "Semantic Kernel",
        {"enterprise_integration", "plugins", "openapi", "mcp", "process", "human_in_loop", "multi_agent"},
        ("process framework may be experimental", "enterprise integration adds concept load"),
    ),
]


TASKS = [
    TaskProfile(
        "T1-minimal-tool-agent",
        "Beginner project with one read-only tool, schema validation, and trace.",
        {"tool_loop", "tracing", "lightweight_sdk"},
        {"guardrails", "sessions"},
        {"multi_agent", "enterprise_integration"},
    ),
    TaskProfile(
        "T2-rag-qa",
        "Markdown knowledge-base Q&A with retrieval metadata and source citations.",
        {"rag", "indexing", "retrieval", "metadata"},
        {"evaluation", "query_engine"},
        {"multi_agent"},
    ),
    TaskProfile(
        "T3-approval-workflow",
        "Refund workflow with branching, retries, persistence, and human approval.",
        {"state_graph", "branching", "retries", "persistence", "human_in_loop"},
        {"tracing", "durable_execution"},
        {"multi_agent"},
    ),
    TaskProfile(
        "T4-role-review",
        "Researcher/writer/reviewer exercise where role separation is the learning goal.",
        {"multi_agent", "coordination"},
        {"teams", "group_chat", "role_tasks", "flows"},
        {"enterprise_integration"},
    ),
    TaskProfile(
        "T5-enterprise-plugin",
        "Enterprise plugin experiment with OpenAPI/MCP integration and process governance.",
        {"enterprise_integration", "plugins", "openapi", "mcp"},
        {"human_in_loop", "process"},
        {"lightweight_sdk"},
    ),
]


def score(framework: FrameworkProfile, task: TaskProfile) -> dict[str, object]:
    required_matches = sorted(task.required & framework.capabilities)
    nice_matches = sorted(task.nice_to_have & framework.capabilities)
    avoid_hits = sorted(task.avoid & framework.capabilities)
    missing_required = sorted(task.required - framework.capabilities)
    value = len(required_matches) * 3 + len(nice_matches) - len(avoid_hits) * 2 - len(missing_required) * 2
    return {
        "framework": framework.name,
        "score": value,
        "required_matches": required_matches,
        "nice_matches": nice_matches,
        "avoid_hits": avoid_hits,
        "missing_required": missing_required,
        "cautions": framework.cautions,
    }


def evaluate_task(task: TaskProfile) -> dict[str, object]:
    scored = sorted((score(framework, task) for framework in FRAMEWORKS), key=lambda item: (-int(item["score"]), str(item["framework"])))
    top = scored[0]
    return {
        "task_id": task.task_id,
        "description": task.description,
        "required": sorted(task.required),
        "nice_to_have": sorted(task.nice_to_have),
        "avoid": sorted(task.avoid),
        "top_choice": top["framework"],
        "top_choice_score": top["score"],
        "top_choice_missing_required": top["missing_required"],
        "needs_real_experiment": True,
        "ranked": scored,
    }


def main() -> None:
    runs = [evaluate_task(task) for task in TASKS]
    summary = {
        "tasks": len(runs),
        "top_choices": {run["task_id"]: run["top_choice"] for run in runs},
        "all_need_real_experiment": all(run["needs_real_experiment"] for run in runs),
    }
    print(json.dumps({"summary": summary, "runs": runs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
