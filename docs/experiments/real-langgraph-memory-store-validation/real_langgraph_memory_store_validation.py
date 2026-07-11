#!/usr/bin/env python3
"""Run a local LangGraph memory store validation harness."""

from __future__ import annotations

import json
from typing import Any


SECRET_MARKER = "secret=example-memory-token"


def redact_value(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace(SECRET_MARKER, "[REDACTED_SECRET]")
    if isinstance(value, dict):
        return {key: redact_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    return value


def run_validation() -> dict[str, Any]:
    try:
        from langgraph.store.memory import InMemoryStore
    except ImportError:
        return {
            "status": "skipped",
            "reason": "langgraph_not_installed",
            "install_note": "Run with `uv run --with langgraph --with langchain-core ...` to collect local LangGraph memory store traces.",
        }

    store = InMemoryStore()
    trace: list[dict[str, Any]] = []

    def remember(user_id: str, key: str, value: dict[str, Any]) -> None:
        namespace = ("memories", user_id)
        store.put(namespace, key, value)
        trace.append({"op": "put", "namespace": namespace, "key": key, "value": redact_value(value)})

    def edit_with_history(user_id: str, key: str, new_value: dict[str, Any]) -> None:
        namespace = ("memories", user_id)
        current = store.get(namespace, key)
        if current is not None:
            history_key = f"{key}:v{current.value.get('version', 1)}"
            history_value = {**current.value, "status": "invalidated"}
            store.put(("memory_history", user_id), history_key, history_value)
            trace.append({"op": "history", "namespace": ("memory_history", user_id), "key": history_key})
        store.put(namespace, key, new_value)
        trace.append({"op": "edit", "namespace": namespace, "key": key, "value": redact_value(new_value)})

    def recall_user(user_id: str) -> list[dict[str, Any]]:
        items = store.search(("memories", user_id))
        trace.append({"op": "search", "namespace_prefix": ("memories", user_id), "count": len(items)})
        return [{"namespace": item.namespace, "key": item.key, "value": item.value} for item in items]

    remember("user-1", "language_preference", {"kind": "preference", "value": "Chinese", "version": 1})
    remember("user-1", "api_token", {"kind": "secret", "value": SECRET_MARKER, "version": 1})
    remember("user-2", "language_preference", {"kind": "preference", "value": "English", "version": 1})

    own_recall = recall_user("user-1")
    broad_prefix = store.search(("memories",))
    trace.append({"op": "search", "namespace_prefix": ("memories",), "count": len(broad_prefix)})

    edit_with_history("user-1", "language_preference", {"kind": "preference", "value": "English", "version": 2})
    edited = store.get(("memories", "user-1"), "language_preference")
    history = store.search(("memory_history", "user-1"))

    store.delete(("memories", "user-1"), "api_token")
    trace.append({"op": "delete", "namespace": ("memories", "user-1"), "key": "api_token"})
    deleted_get = store.get(("memories", "user-1"), "api_token")
    after_delete = recall_user("user-1")

    cases = [
        {
            "name": "own_namespace_recall",
            "passed": any(item["key"] == "language_preference" for item in own_recall)
            and all(item["namespace"] == ("memories", "user-1") for item in own_recall),
            "observation": "user-specific namespace recall returns only user-1 memories",
        },
        {
            "name": "broad_prefix_cross_user_visible",
            "passed": any(item.namespace == ("memories", "user-2") for item in broad_prefix),
            "observation": "searching the broad ('memories',) prefix can see multiple user namespaces; authorization must be application policy",
        },
        {
            "name": "edit_records_invalidated_history",
            "passed": edited is not None
            and edited.value["value"] == "English"
            and any(item.value.get("status") == "invalidated" for item in history),
            "observation": "application wrapper can preserve invalidated history before overwriting active memory",
        },
        {
            "name": "delete_removes_active_recall",
            "passed": deleted_get is None and all(item["key"] != "api_token" for item in after_delete),
            "observation": "delete removes the active item from get/search in the local store",
        },
    ]

    trace_json = json.dumps(trace, ensure_ascii=False)
    return {
        "status": "completed",
        "framework": "langgraph",
        "store": "InMemoryStore",
        "namespace_policy": "application_scoped_user_namespace",
        "case_count": len(cases),
        "passed_count": sum(1 for case in cases if case["passed"]),
        "all_passed": all(case["passed"] for case in cases),
        "cross_user_broad_prefix_seen": any(item.namespace == ("memories", "user-2") for item in broad_prefix),
        "deleted_item_recalled": any(item["key"] == "api_token" for item in after_delete),
        "secret_leaked_in_trace": SECRET_MARKER in trace_json,
        "cases": cases,
        "trace": trace,
    }


def main() -> None:
    print(json.dumps(run_validation(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
