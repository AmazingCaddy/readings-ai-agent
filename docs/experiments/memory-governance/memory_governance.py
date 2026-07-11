#!/usr/bin/env python3
"""Minimal long-term memory governance simulation.

The experiment compares auto-write memory with a guarded write policy. It shows
how inferred, stale, conflicting, or sensitive memories can contaminate later
tasks when every candidate is stored without review.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class MemoryCandidate:
    key: str
    value: str
    source: str
    kind: str
    confidence: str
    sensitive: bool = False


@dataclass
class MemoryRecord:
    key: str
    value: str
    source: str
    kind: str
    status: str = "active"
    version: int = 1
    updated_at: str = field(default_factory=utc_now)


@dataclass
class TraceEvent:
    strategy: str
    event: str
    details: dict[str, Any]
    timestamp: str = field(default_factory=utc_now)


SESSION_CANDIDATES = [
    MemoryCandidate("language_preference", "Chinese", "user_explicit", "preference", "high"),
    MemoryCandidate("skill_level", "beginner", "model_inferred", "profile", "low"),
    MemoryCandidate("api_key", "sk-example-secret", "user_message", "secret", "high", sensitive=True),
    MemoryCandidate("language_preference", "English", "user_explicit_change", "preference", "high"),
    MemoryCandidate("project_framework", "LangChain", "assistant_guess", "fact", "low"),
    MemoryCandidate("project_framework", "MkDocs", "user_correction", "fact", "high"),
]


class MemoryStore:
    def __init__(self, strategy: str) -> None:
        self.strategy = strategy
        self.records: dict[str, MemoryRecord] = {}
        self.history: list[MemoryRecord] = []
        self.trace: list[TraceEvent] = []

    def record(self, event: str, **details: Any) -> None:
        self.trace.append(TraceEvent(strategy=self.strategy, event=event, details=details))

    def write(self, candidate: MemoryCandidate) -> None:
        if self.strategy == "guarded_write":
            allowed, reason = self.guard(candidate)
            self.record("candidate_reviewed", candidate=self.candidate_payload(candidate, redact=True), allowed=allowed, reason=reason)
            if not allowed:
                return
        else:
            self.record("candidate_auto_written", candidate=self.candidate_payload(candidate, redact=False))

        existing = self.records.get(candidate.key)
        if existing and existing.value != candidate.value:
            existing.status = "invalidated"
            self.history.append(existing)
            self.record(
                "memory_invalidated",
                key=existing.key,
                old_value=existing.value,
                new_value=candidate.value,
                old_version=existing.version,
            )
            version = existing.version + 1
        else:
            version = existing.version if existing else 1

        self.records[candidate.key] = MemoryRecord(
            key=candidate.key,
            value=candidate.value,
            source=candidate.source,
            kind=candidate.kind,
            version=version,
        )
        self.record("memory_written", key=candidate.key, value=self.redact(candidate.value), version=version)

    def guard(self, candidate: MemoryCandidate) -> tuple[bool, str]:
        if candidate.sensitive or candidate.kind == "secret":
            return False, "sensitive data must not enter long-term memory"
        if candidate.confidence != "high":
            return False, "low-confidence inferred memory requires user confirmation"
        if candidate.source not in {"user_explicit", "user_explicit_change", "user_correction"}:
            return False, "memory write requires explicit user signal"
        return True, "explicit non-sensitive memory accepted"

    def answer_context(self) -> dict[str, str]:
        return {key: record.value for key, record in sorted(self.records.items()) if record.status == "active"}

    def contamination_flags(self) -> list[str]:
        flags: list[str] = []
        context = self.answer_context()
        if "api_key" in context:
            flags.append("sensitive_secret_persisted")
        if context.get("skill_level") == "beginner":
            flags.append("low_confidence_profile_persisted")
        if context.get("project_framework") == "LangChain":
            flags.append("stale_wrong_project_framework_used")
        return flags

    def redact(self, value: str) -> str:
        return value.replace("sk-example-secret", "[REDACTED]")

    def candidate_payload(self, candidate: MemoryCandidate, redact: bool) -> dict[str, Any]:
        payload = candidate.__dict__.copy()
        if redact:
            payload["value"] = self.redact(payload["value"])
        return payload

    def serialized(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy,
            "active_memory": {key: self.redact(value) for key, value in self.answer_context().items()},
            "invalidated_history": [record.__dict__ for record in self.history],
            "contamination_flags": self.contamination_flags(),
            "leaked_secret_in_trace": any("sk-example-secret" in json.dumps(event.__dict__) for event in self.trace),
            "trace": [event.__dict__ for event in self.trace],
        }


def run_strategy(strategy: str) -> dict[str, Any]:
    store = MemoryStore(strategy)
    for candidate in SESSION_CANDIDATES:
        store.write(candidate)
    return store.serialized()


def main() -> None:
    result = {
        "cases": [run_strategy("auto_write"), run_strategy("guarded_write")],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
