#!/usr/bin/env python3
"""Deterministic memory lifecycle and permission audit.

This harness compares a naive memory store with a governed memory store across
inspect, edit, delete, and recall operations. It does not run a model or a real
memory framework. The goal is to make lifecycle and permission requirements
concrete for the handbook.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal


Mode = Literal["naive_memory", "governed_memory"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class MemoryRecord:
    key: str
    value: str
    owner_user_id: str
    kind: str
    source: str
    status: str = "active"
    version: int = 1
    sensitive: bool = False
    updated_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class Operation:
    op_id: str
    actor_user_id: str
    action: str
    key: str | None = None
    value: str | None = None
    target_user_id: str | None = None
    expected_allowed: bool = True
    expected_effect: str = "allowed"


INITIAL_MEMORY = [
    MemoryRecord("language_preference", "Chinese", "user-1", "preference", "user_explicit"),
    MemoryRecord("project_framework", "MkDocs", "user-1", "fact", "user_correction"),
    MemoryRecord("api_key", "sk-example-secret", "user-1", "secret", "user_message", sensitive=True),
    MemoryRecord("language_preference", "English", "user-2", "preference", "user_explicit"),
]


OPERATIONS = [
    Operation("inspect_own", "user-1", "inspect", target_user_id="user-1", expected_allowed=True, expected_effect="inspected"),
    Operation("inspect_other_user", "user-1", "inspect", target_user_id="user-2", expected_allowed=False, expected_effect="blocked_cross_user"),
    Operation(
        "edit_preference",
        "user-1",
        "edit",
        key="language_preference",
        value="English",
        expected_allowed=True,
        expected_effect="old_version_invalidated",
    ),
    Operation("delete_secret", "user-1", "delete", key="api_key", expected_allowed=True, expected_effect="deleted"),
    Operation(
        "recall_after_delete",
        "user-1",
        "recall",
        target_user_id="user-1",
        expected_allowed=True,
        expected_effect="secret_absent",
    ),
    Operation(
        "cross_user_recall",
        "user-1",
        "recall",
        target_user_id="user-2",
        expected_allowed=False,
        expected_effect="blocked_cross_user",
    ),
]


class MemoryLifecycleStore:
    def __init__(self, mode: Mode) -> None:
        self.mode = mode
        self.records = [copy_record(record) for record in INITIAL_MEMORY]
        self.history: list[MemoryRecord] = []
        self.trace: list[dict[str, Any]] = []

    def record_event(self, operation: Operation, allowed: bool, effect: str, details: dict[str, Any]) -> None:
        self.trace.append(
            {
                "timestamp": utc_now(),
                "mode": self.mode,
                "op_id": operation.op_id,
                "action": operation.action,
                "actor_user_id": operation.actor_user_id,
                "allowed": allowed,
                "effect": effect,
                "details": redact(details) if self.mode == "governed_memory" else details,
            }
        )

    def run_operation(self, operation: Operation) -> dict[str, Any]:
        if self.mode == "governed_memory" and not self.is_authorized(operation):
            self.record_event(operation, False, "blocked_cross_user", {"target_user_id": operation.target_user_id})
            return result(operation, False, "blocked_cross_user")

        if operation.action == "inspect":
            visible = self.visible_records(operation.actor_user_id, operation.target_user_id)
            effect = "inspected"
            self.record_event(operation, True, effect, {"records": [record.__dict__ for record in visible]})
            return result(operation, True, effect)

        if operation.action == "edit":
            effect = self.edit_record(operation)
            self.record_event(operation, True, effect, {"key": operation.key, "value": operation.value})
            return result(operation, True, effect)

        if operation.action == "delete":
            effect = self.delete_record(operation)
            self.record_event(operation, True, effect, {"key": operation.key})
            return result(operation, True, effect)

        if operation.action == "recall":
            recalled = self.recall(operation)
            effect = "secret_absent" if not any(record.key == "api_key" for record in recalled) else "secret_recalled"
            self.record_event(operation, True, effect, {"recalled": [record.__dict__ for record in recalled]})
            return result(operation, True, effect)

        self.record_event(operation, False, "unknown_action", {})
        return result(operation, False, "unknown_action")

    def is_authorized(self, operation: Operation) -> bool:
        target_user_id = operation.target_user_id or operation.actor_user_id
        return target_user_id == operation.actor_user_id

    def visible_records(self, actor_user_id: str, target_user_id: str | None) -> list[MemoryRecord]:
        if self.mode == "naive_memory":
            return [record for record in self.records if record.status == "active"]
        return [
            record
            for record in self.records
            if record.status == "active" and record.owner_user_id == (target_user_id or actor_user_id) and not record.sensitive
        ]

    def edit_record(self, operation: Operation) -> str:
        existing = self.find_record(operation.actor_user_id, operation.key)
        if existing is None:
            self.records.append(
                MemoryRecord(operation.key or "unknown", operation.value or "", operation.actor_user_id, "preference", "user_edit")
            )
            return "created"
        if self.mode == "governed_memory":
            old = copy_record(existing)
            old.status = "invalidated"
            self.history.append(old)
            existing.version += 1
        existing.value = operation.value or ""
        existing.source = "user_edit"
        existing.updated_at = utc_now()
        return "old_version_invalidated" if self.mode == "governed_memory" else "overwritten_without_history"

    def delete_record(self, operation: Operation) -> str:
        existing = self.find_record(operation.actor_user_id, operation.key)
        if existing is None:
            return "not_found"
        if self.mode == "governed_memory":
            old = copy_record(existing)
            old.status = "deleted"
            self.history.append(old)
            existing.status = "deleted"
            existing.value = "[DELETED]"
            return "deleted"
        return "delete_not_supported"

    def recall(self, operation: Operation) -> list[MemoryRecord]:
        target_user_id = operation.target_user_id or operation.actor_user_id
        if self.mode == "naive_memory":
            return [record for record in self.records if record.status == "active"]
        return [
            record
            for record in self.records
            if record.status == "active" and record.owner_user_id == target_user_id and not record.sensitive
        ]

    def find_record(self, owner_user_id: str, key: str | None) -> MemoryRecord | None:
        for record in self.records:
            if record.owner_user_id == owner_user_id and record.key == key and record.status == "active":
                return record
        return None

    def summarize(self, operation_results: list[dict[str, Any]]) -> dict[str, Any]:
        leaked_secret = any("sk-example-secret" in json.dumps(event, ensure_ascii=False) for event in self.trace)
        active_records = [record for record in self.records if record.status == "active"]
        return {
            "mode": self.mode,
            "passed_operations": sum(1 for item in operation_results if item["passed"]),
            "total_operations": len(operation_results),
            "failed_operations": [item["op_id"] for item in operation_results if not item["passed"]],
            "active_memory": [redact(record.__dict__) for record in active_records],
            "history": [redact(record.__dict__) for record in self.history],
            "leaked_secret_in_trace": leaked_secret,
            "operation_results": operation_results,
            "trace": self.trace,
        }


def copy_record(record: MemoryRecord) -> MemoryRecord:
    return MemoryRecord(
        key=record.key,
        value=record.value,
        owner_user_id=record.owner_user_id,
        kind=record.kind,
        source=record.source,
        status=record.status,
        version=record.version,
        sensitive=record.sensitive,
        updated_at=record.updated_at,
    )


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return value.replace("sk-example-secret", "[REDACTED]")
    return value


def result(operation: Operation, allowed: bool, effect: str) -> dict[str, Any]:
    return {
        "op_id": operation.op_id,
        "action": operation.action,
        "expected_allowed": operation.expected_allowed,
        "actual_allowed": allowed,
        "expected_effect": operation.expected_effect,
        "actual_effect": effect,
        "passed": allowed == operation.expected_allowed and effect == operation.expected_effect,
    }


def run_mode(mode: Mode) -> dict[str, Any]:
    store = MemoryLifecycleStore(mode)
    operation_results = [store.run_operation(operation) for operation in OPERATIONS]
    return store.summarize(operation_results)


def main() -> None:
    cases = [run_mode("naive_memory"), run_mode("governed_memory")]
    print(json.dumps({"cases": cases}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
