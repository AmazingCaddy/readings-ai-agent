#!/usr/bin/env python3
"""Deterministic approval state recovery audit.

This harness compares a naive approval runtime with a governed approval runtime
for high-risk tool calls. It does not call a model or execute real tools. The
goal is to make pause/resume, approval decisions, idempotency, argument
integrity, and trace redaction concrete for the handbook.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal


Mode = Literal["naive_resume", "governed_resume"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class PendingApproval:
    approval_id: str
    tool_name: str
    args: dict[str, Any]
    requester_user_id: str
    status: str = "pending"
    decision_by: str | None = None
    args_hash: str = ""
    executed: bool = False
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class Operation:
    op_id: str
    action: str
    approval_id: str
    tool_name: str | None = None
    args: dict[str, Any] | None = None
    decision_by: str | None = None
    mutate_args: dict[str, Any] | None = None
    expected_effect: str = "allowed"


OPERATIONS = [
    Operation(
        op_id="create_refund_approval",
        action="create",
        approval_id="approval-refund-1",
        tool_name="issue_refund",
        args={"order_id": "order-123", "amount_usd": 250, "reason": "policy exception"},
        expected_effect="pending_created",
    ),
    Operation(
        op_id="approve_and_resume_refund",
        action="decide_and_resume",
        approval_id="approval-refund-1",
        decision_by="manager-1",
        expected_effect="executed_once",
    ),
    Operation(
        op_id="duplicate_resume_refund",
        action="resume",
        approval_id="approval-refund-1",
        expected_effect="already_executed",
    ),
    Operation(
        op_id="create_sensitive_email_approval",
        action="create",
        approval_id="approval-email-1",
        tool_name="send_email",
        args={
            "to": "customer@example.com",
            "subject": "Account update",
            "body": "Please store internal_secret=sk-example-secret for later use.",
        },
        expected_effect="pending_created",
    ),
    Operation(
        op_id="reject_and_resume_email",
        action="reject_and_resume",
        approval_id="approval-email-1",
        decision_by="manager-1",
        expected_effect="blocked_rejected",
    ),
    Operation(
        op_id="create_tamper_refund_approval",
        action="create",
        approval_id="approval-refund-2",
        tool_name="issue_refund",
        args={"order_id": "order-456", "amount_usd": 200, "reason": "manual review"},
        expected_effect="pending_created",
    ),
    Operation(
        op_id="tampered_resume_refund",
        action="decide_and_resume",
        approval_id="approval-refund-2",
        decision_by="manager-1",
        mutate_args={"amount_usd": 900},
        expected_effect="blocked_argument_mismatch",
    ),
]


class ApprovalRuntime:
    def __init__(self, mode: Mode) -> None:
        self.mode = mode
        self.pending: dict[str, PendingApproval] = {}
        self.side_effects: list[dict[str, Any]] = []
        self.trace: list[dict[str, Any]] = []

    def record_event(self, operation: Operation, effect: str, details: dict[str, Any]) -> None:
        safe_details = redact(details) if self.mode == "governed_resume" else details
        self.trace.append(
            {
                "timestamp": utc_now(),
                "mode": self.mode,
                "op_id": operation.op_id,
                "action": operation.action,
                "effect": effect,
                "details": json.loads(json.dumps(safe_details, ensure_ascii=False)),
            }
        )

    def run_operation(self, operation: Operation) -> dict[str, Any]:
        if operation.action == "create":
            effect = self.create_pending(operation)
            self.record_event(operation, effect, {"approval": approval_dict(self.pending[operation.approval_id])})
            return result(operation, effect)

        approval = self.pending.get(operation.approval_id)
        if approval is None:
            self.record_event(operation, "missing_approval", {"approval_id": operation.approval_id})
            return result(operation, "missing_approval")

        if operation.mutate_args:
            approval.args.update(operation.mutate_args)
            self.record_event(operation, "approval_args_mutated", {"approval": approval_dict(approval)})

        if operation.action == "decide_and_resume":
            approval.status = "approved"
            approval.decision_by = operation.decision_by
            effect = self.resume(operation, approval)
            self.record_event(operation, effect, {"approval": approval_dict(approval), "side_effects": self.side_effects})
            return result(operation, effect)

        if operation.action == "reject_and_resume":
            approval.status = "rejected"
            approval.decision_by = operation.decision_by
            effect = self.resume(operation, approval)
            self.record_event(operation, effect, {"approval": approval_dict(approval), "side_effects": self.side_effects})
            return result(operation, effect)

        if operation.action == "resume":
            effect = self.resume(operation, approval)
            self.record_event(operation, effect, {"approval": approval_dict(approval), "side_effects": self.side_effects})
            return result(operation, effect)

        self.record_event(operation, "unknown_action", {})
        return result(operation, "unknown_action")

    def create_pending(self, operation: Operation) -> str:
        approval = PendingApproval(
            approval_id=operation.approval_id,
            tool_name=operation.tool_name or "unknown_tool",
            args=dict(operation.args or {}),
            requester_user_id="user-1",
        )
        approval.args_hash = stable_hash(approval.tool_name, approval.args, approval.requester_user_id)
        self.pending[approval.approval_id] = approval
        return "pending_created"

    def resume(self, operation: Operation, approval: PendingApproval) -> str:
        if self.mode == "governed_resume":
            if approval.status == "rejected":
                return "blocked_rejected"
            if approval.status != "approved":
                return "blocked_no_approval"
            if approval.executed:
                return "already_executed"
            current_hash = stable_hash(approval.tool_name, approval.args, approval.requester_user_id)
            if current_hash != approval.args_hash:
                return "blocked_argument_mismatch"

        side_effect = {
            "tool_name": approval.tool_name,
            "approval_id": approval.approval_id,
            "args": redact(approval.args) if self.mode == "governed_resume" else dict(approval.args),
            "executed_at": utc_now(),
        }
        self.side_effects.append(side_effect)
        approval.executed = True
        return "executed_once"

    def summarize(self, operation_results: list[dict[str, Any]]) -> dict[str, Any]:
        leaked_secret = any("sk-example-secret" in json.dumps(event, ensure_ascii=False) for event in self.trace)
        duplicate_side_effects = len(self.side_effects) - len({item["approval_id"] for item in self.side_effects})
        return {
            "mode": self.mode,
            "passed_operations": sum(1 for item in operation_results if item["passed"]),
            "total_operations": len(operation_results),
            "failed_operations": [item["op_id"] for item in operation_results if not item["passed"]],
            "side_effect_count": len(self.side_effects),
            "duplicate_side_effects": duplicate_side_effects,
            "leaked_secret_in_trace": leaked_secret,
            "operation_results": operation_results,
            "side_effects": self.side_effects,
            "trace": self.trace,
        }


def stable_hash(tool_name: str, args: dict[str, Any], requester_user_id: str) -> str:
    payload = json.dumps(
        {"tool_name": tool_name, "args": args, "requester_user_id": requester_user_id},
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def approval_dict(approval: PendingApproval) -> dict[str, Any]:
    return {
        "approval_id": approval.approval_id,
        "tool_name": approval.tool_name,
        "args": approval.args,
        "requester_user_id": approval.requester_user_id,
        "status": approval.status,
        "decision_by": approval.decision_by,
        "args_hash": approval.args_hash,
        "executed": approval.executed,
        "created_at": approval.created_at,
    }


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return value.replace("sk-example-secret", "[REDACTED]")
    return value


def result(operation: Operation, effect: str) -> dict[str, Any]:
    return {
        "op_id": operation.op_id,
        "action": operation.action,
        "expected_effect": operation.expected_effect,
        "actual_effect": effect,
        "passed": operation.expected_effect == effect,
    }


def run_mode(mode: Mode) -> dict[str, Any]:
    runtime = ApprovalRuntime(mode)
    operation_results = [runtime.run_operation(operation) for operation in OPERATIONS]
    return runtime.summarize(operation_results)


def main() -> None:
    cases = [run_mode("naive_resume"), run_mode("governed_resume")]
    print(json.dumps({"cases": cases}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
