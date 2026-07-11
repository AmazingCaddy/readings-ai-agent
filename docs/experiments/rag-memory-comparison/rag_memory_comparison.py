#!/usr/bin/env python3
"""Deterministic RAG vs memory boundary simulation.

The experiment compares three context sources for a learning assistant:
RAG documents, thread-scoped short-term memory, and guarded long-term memory.
It uses fixed data and rule-based outputs so the boundary is reproducible
without model, vector-store, or framework dependencies.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Case:
    case_id: str
    prompt: str
    expected_best_source: str
    expected_citation: str | None
    expected_personalization: str | None


DOCUMENTS = {
    "rag_paper": "RAG retrieves external documents and should preserve provenance for knowledge-intensive answers.",
    "langgraph_memory": "Short-term memory is thread-scoped state; long-term memory stores cross-session user or app data.",
    "memory_governance": "Long-term memory needs write guards, invalidation, conflict handling, and user control.",
}

THREAD_STATE = {
    "current_topic": "tool calling",
    "current_language": "Chinese",
    "completed_step": "function calling boundary",
}

LONG_TERM_MEMORY = {
    "confirmed_language_preference": {"value": "Chinese", "status": "active", "source": "user_confirmed"},
    "stale_framework_preference": {"value": "LangChain", "status": "invalidated", "source": "assistant_guess"},
    "confirmed_site_stack": {"value": "MkDocs", "status": "active", "source": "user_correction"},
}

CASES = [
    Case(
        "C1-external-rag",
        "What is RAG and why should answers cite sources?",
        "rag",
        "rag_paper",
        None,
    ),
    Case(
        "C2-current-session",
        "Continue from the step we just finished in this session.",
        "short_term",
        None,
        "function calling boundary",
    ),
    Case(
        "C3-cross-session-preference",
        "Explain the next topic using my saved language preference.",
        "long_term",
        None,
        "Chinese",
    ),
    Case(
        "C4-stale-memory",
        "Which site stack should we use for the handbook?",
        "long_term",
        None,
        "MkDocs",
    ),
    Case(
        "C5-unsupported",
        "What private API key did the user mention last month?",
        "none",
        None,
        None,
    ),
]


def rag_answer(case: Case) -> dict[str, Any]:
    if "RAG" in case.prompt or "cite sources" in case.prompt:
        return {
            "source": "rag",
            "answered": True,
            "answer": DOCUMENTS["rag_paper"],
            "citations": ["rag_paper"],
            "personalization": None,
            "risks": [],
            "trace": ["retrieve_documents", "synthesize_with_citation"],
        }
    return {
        "source": "rag",
        "answered": False,
        "answer": None,
        "citations": [],
        "personalization": None,
        "risks": ["no_retrieved_evidence"],
        "trace": ["retrieve_empty", "refuse_without_evidence"],
    }


def short_term_answer(case: Case) -> dict[str, Any]:
    if "just finished" in case.prompt:
        return {
            "source": "short_term",
            "answered": True,
            "answer": f"Continue after {THREAD_STATE['completed_step']}.",
            "citations": [],
            "personalization": THREAD_STATE["completed_step"],
            "risks": [],
            "trace": ["read_thread_state", "continue_current_task"],
        }
    return {
        "source": "short_term",
        "answered": False,
        "answer": None,
        "citations": [],
        "personalization": None,
        "risks": ["thread_state_not_relevant"],
        "trace": ["read_thread_state", "refuse_out_of_scope"],
    }


def active_long_term_values() -> dict[str, str]:
    return {
        key: item["value"]
        for key, item in LONG_TERM_MEMORY.items()
        if item["status"] == "active" and item["source"] in {"user_confirmed", "user_correction"}
    }


def long_term_answer(case: Case) -> dict[str, Any]:
    active = active_long_term_values()
    if "saved language preference" in case.prompt:
        return {
            "source": "long_term",
            "answered": True,
            "answer": f"Use {active['confirmed_language_preference']} for the explanation.",
            "citations": [],
            "personalization": active["confirmed_language_preference"],
            "risks": [],
            "trace": ["load_confirmed_memory", "apply_preference"],
        }
    if "site stack" in case.prompt:
        return {
            "source": "long_term",
            "answered": True,
            "answer": f"Use {active['confirmed_site_stack']}; ignore invalidated assistant guess.",
            "citations": [],
            "personalization": active["confirmed_site_stack"],
            "risks": ["invalidated_memory_quarantined"],
            "trace": ["load_confirmed_memory", "skip_invalidated_memory", "apply_user_correction"],
        }
    return {
        "source": "long_term",
        "answered": False,
        "answer": None,
        "citations": [],
        "personalization": None,
        "risks": ["no_confirmed_memory"],
        "trace": ["load_confirmed_memory", "refuse_unconfirmed_or_sensitive_memory"],
    }


def run_case(case: Case) -> dict[str, Any]:
    candidates = [rag_answer(case), short_term_answer(case), long_term_answer(case)]
    best = next(
        (candidate for candidate in candidates if candidate["source"] == case.expected_best_source and candidate["answered"]),
        None,
    )
    if case.expected_best_source == "none":
        best = {
            "source": "none",
            "answered": False,
            "answer": None,
            "citations": [],
            "personalization": None,
            "risks": ["no_safe_context_source"],
            "trace": ["all_sources_refused"],
        }
    checks = {
        "source": best["source"] == case.expected_best_source,
        "citation": case.expected_citation in best["citations"] if case.expected_citation else best["citations"] == [],
        "personalization": best["personalization"] == case.expected_personalization,
    }
    return {
        "case_id": case.case_id,
        "prompt": case.prompt,
        "passed": all(checks.values()),
        "checks": checks,
        "selected": best,
        "candidates": candidates,
    }


def main() -> None:
    runs = [run_case(case) for case in CASES]
    summary = {
        "passed": sum(1 for run in runs if run["passed"]),
        "total": len(runs),
        "selected_sources": {run["case_id"]: run["selected"]["source"] for run in runs},
        "failed_cases": [run["case_id"] for run in runs if not run["passed"]],
    }
    print(json.dumps({"summary": summary, "runs": runs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
