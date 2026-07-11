#!/usr/bin/env python3
"""Real LangGraph interrupt recovery validation harness.

The harness skips when LangGraph is not installed. With LangGraph available, it
builds a minimal approval graph using interrupt(), a checkpointer, and
Command(resume=...) to observe approval, rejection, duplicate resume, tampered
arguments, side-effect placement, and trace redaction boundaries.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict


SECRET_MARKERS = ["user_secret", "card_number", "raw_email"]


class RefundState(TypedDict, total=False):
    order_id: str
    user_id: str
    amount: int
    reason: str
    approval_id: str
    args_hash: str
    approval_status: str
    refund_executed: bool
    blocked_reason: str
    trace: list[dict[str, Any]]
    secret: str


@dataclass
class ToolLedger:
    executions: list[dict[str, Any]] = field(default_factory=list)

    def issue_refund(self, state: RefundState) -> None:
        self.executions.append(
            {
                "order_id": state["order_id"],
                "user_id_hash": redact(state["user_id"]),
                "amount": state["amount"],
                "timestamp": utc_now(),
            }
        )


@dataclass
class FileToolLedger:
    path: Path
    executions: list[dict[str, Any]] = field(default_factory=list)

    def issue_refund(self, state: RefundState) -> None:
        record = {
            "order_id": state["order_id"],
            "user_id_hash": redact(state["user_id"]),
            "amount": state["amount"],
            "timestamp": utc_now(),
        }
        self.executions.append(record)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def redact(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def args_hash(state: RefundState) -> str:
    payload = {
        "order_id": state["order_id"],
        "user_id": state["user_id"],
        "amount": state["amount"],
        "reason": state["reason"],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def trace_event(event: str, **fields: Any) -> dict[str, Any]:
    return {"event": event, "timestamp": utc_now(), **fields}


def append_trace(state: RefundState, event: str, **fields: Any) -> list[dict[str, Any]]:
    trace = list(state.get("trace", []))
    trace.append(trace_event(event, **fields))
    return trace


def payload_for_review(state: RefundState) -> dict[str, Any]:
    return {
        "approval_id": state["approval_id"],
        "order_id": state["order_id"],
        "user_id_hash": redact(state["user_id"]),
        "amount": state["amount"],
        "reason": state["reason"],
        "args_hash": state["args_hash"],
        "risk_level": "high",
    }


def has_secret_leak(value: Any) -> bool:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return any(marker in serialized for marker in SECRET_MARKERS)


def versions() -> dict[str, str | None]:
    packages = ["langgraph", "langchain-core", "langgraph-checkpoint-sqlite"]
    result: dict[str, str | None] = {}
    for package in packages:
        try:
            result[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            result[package] = None
    result["python"] = sys.version.split()[0]
    return result


def build_graph(ledger: Any, checkpointer: Any | None = None) -> Any:
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.graph import END, StateGraph
    from langgraph.types import interrupt

    if checkpointer is None:
        checkpointer = MemorySaver()

    def prepare_refund(state: RefundState) -> RefundState:
        prepared: RefundState = {
            **state,
            "approval_id": state.get("approval_id") or f"appr_{uuid.uuid4().hex[:10]}",
            "refund_executed": bool(state.get("refund_executed", False)),
        }
        prepared["args_hash"] = args_hash(prepared)
        prepared["trace"] = append_trace(
            prepared,
            "approval_created",
            approval_id=prepared["approval_id"],
            args_hash=prepared["args_hash"],
            user_id_hash=redact(prepared["user_id"]),
        )
        return prepared

    def review_and_execute(state: RefundState) -> RefundState:
        decision = interrupt(payload_for_review(state))
        resumed_hash = decision.get("args_hash") if isinstance(decision, dict) else None
        approved = bool(decision.get("approved")) if isinstance(decision, dict) else False
        trace = append_trace(
            state,
            "resume_received",
            approval_id=state["approval_id"],
            approved=approved,
            resumed_hash=resumed_hash,
        )
        updated: RefundState = {**state, "trace": trace}
        if resumed_hash != state["args_hash"]:
            return {
                **updated,
                "approval_status": "blocked",
                "blocked_reason": "argument_hash_mismatch",
                "trace": append_trace(updated, "tamper_detected", approval_id=state["approval_id"]),
            }
        if not approved:
            return {
                **updated,
                "approval_status": "rejected",
                "blocked_reason": "approval_rejected",
                "trace": append_trace(updated, "approval_rejected", approval_id=state["approval_id"]),
            }
        if updated.get("refund_executed"):
            return {
                **updated,
                "approval_status": "duplicate_blocked",
                "blocked_reason": "already_executed",
                "trace": append_trace(updated, "duplicate_resume_blocked", approval_id=state["approval_id"]),
            }
        ledger.issue_refund(updated)
        executed: RefundState = {
            **updated,
            "approval_status": "approved_executed",
            "refund_executed": True,
        }
        executed["trace"] = append_trace(executed, "refund_executed", approval_id=state["approval_id"])
        return executed

    graph = StateGraph(RefundState)
    graph.add_node("prepare_refund", prepare_refund)
    graph.add_node("review_and_execute", review_and_execute)
    graph.set_entry_point("prepare_refund")
    graph.add_edge("prepare_refund", "review_and_execute")
    graph.add_edge("review_and_execute", END)
    return graph.compile(checkpointer=checkpointer)


def invoke_until_interrupt(graph: Any, initial_state: RefundState, thread_id: str) -> dict[str, Any]:
    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke(initial_state, config=config)
    return {"config": config, "result": result}


def extract_interrupt_payload(pending_result: Any) -> dict[str, Any] | None:
    interrupts = pending_result.get("__interrupt__", []) if isinstance(pending_result, dict) else []
    if not interrupts:
        return None
    first = interrupts[0]
    interrupt_payload = getattr(first, "value", first)
    return interrupt_payload if isinstance(interrupt_payload, dict) else None


def resume_graph(graph: Any, config: dict[str, Any], decision: dict[str, Any]) -> RefundState:
    from langgraph.types import Command

    return graph.invoke(Command(resume=decision), config=config)


def base_state() -> RefundState:
    return {
        "order_id": "order_123",
        "user_id": "user_secret_456",
        "amount": 42,
        "reason": "customer reported duplicate charge",
        "secret": "card_number_4242_4242_4242_4242",
        "trace": [],
    }


def run_case(case_name: str, decision: str) -> dict[str, Any]:
    ledger = ToolLedger()
    graph = build_graph(ledger)
    started = time.perf_counter()
    thread_id = f"thread_{case_name}_{uuid.uuid4().hex[:8]}"
    pending = invoke_until_interrupt(graph, base_state(), thread_id)
    interrupt_payload = extract_interrupt_payload(pending["result"])
    if not isinstance(interrupt_payload, dict):
        return {
            "case": case_name,
            "status": "failed",
            "reason": "interrupt_payload_missing",
            "raw_result_type": type(pending["result"]).__name__,
        }
    approval_decision = {
        "approved": decision == "approved",
        "args_hash": interrupt_payload["args_hash"],
    }
    if decision == "tampered":
        approval_decision = {"approved": True, "args_hash": "tampered_hash"}
    final_state = resume_graph(graph, pending["config"], approval_decision)
    duplicate_state = None
    if case_name == "duplicate_resume":
        duplicate_state = resume_graph(graph, pending["config"], approval_decision)
    trace = final_state.get("trace", []) if isinstance(final_state, dict) else []
    return {
        "case": case_name,
        "status": "completed",
        "thread_id": thread_id,
        "approval_status": final_state.get("approval_status") if isinstance(final_state, dict) else None,
        "blocked_reason": final_state.get("blocked_reason") if isinstance(final_state, dict) else None,
        "tool_execution_count": len(ledger.executions),
        "duplicate_approval_status": duplicate_state.get("approval_status") if isinstance(duplicate_state, dict) else None,
        "trace_event_count": len(trace),
        "secret_leaked_in_trace": has_secret_leak(trace) or has_secret_leak(interrupt_payload),
        "latency_ms": int((time.perf_counter() - started) * 1000),
    }


def run_side_effect_risk_case() -> dict[str, Any]:
    trace = [trace_event("side_effect_before_interrupt", order_id="order_123")]
    return {
        "case": "side_effect_before_interrupt",
        "status": "design_failure_recorded",
        "tool_execution_count": 1,
        "expected_result": "unsafe_pattern_because_node_restart_can_repeat_pre_interrupt_side_effects",
        "secret_leaked_in_trace": has_secret_leak(trace),
    }


def run_sqlite_restart_case() -> dict[str, Any]:
    try:
        import langgraph.checkpoint.sqlite  # noqa: F401
        from langgraph.checkpoint.sqlite import SqliteSaver
    except ImportError:
        return {
            "case": "sqlite_process_restart",
            "status": "skipped",
            "reason": "langgraph_checkpoint_sqlite_not_installed",
        }

    started = time.perf_counter()
    thread_id = f"thread_sqlite_restart_{uuid.uuid4().hex[:8]}"
    with tempfile.TemporaryDirectory(prefix="langgraph-checkpoint-") as tmpdir:
        db_path = Path(tmpdir) / "checkpoints.sqlite"
        conn_string = str(db_path)

        setup_ledger = ToolLedger()
        with SqliteSaver.from_conn_string(conn_string) as setup_saver:
            setup_graph = build_graph(setup_ledger, checkpointer=setup_saver)
            pending = invoke_until_interrupt(setup_graph, base_state(), thread_id)
            interrupt_payload = extract_interrupt_payload(pending["result"])

        if not isinstance(interrupt_payload, dict):
            return {
                "case": "sqlite_process_restart",
                "status": "failed",
                "reason": "interrupt_payload_missing",
                "raw_result_type": type(pending["result"]).__name__,
            }

        resume_ledger = ToolLedger()
        with SqliteSaver.from_conn_string(conn_string) as resume_saver:
            restarted_graph = build_graph(resume_ledger, checkpointer=resume_saver)
            final_state = resume_graph(
                restarted_graph,
                pending["config"],
                {"approved": True, "args_hash": interrupt_payload["args_hash"]},
            )

    trace = final_state.get("trace", []) if isinstance(final_state, dict) else []
    return {
        "case": "sqlite_process_restart",
        "status": "completed",
        "thread_id": thread_id,
        "checkpointer": "SqliteSaver",
        "approval_status": final_state.get("approval_status") if isinstance(final_state, dict) else None,
        "blocked_reason": final_state.get("blocked_reason") if isinstance(final_state, dict) else None,
        "tool_execution_count_before_restart": len(setup_ledger.executions),
        "tool_execution_count_after_restart": len(resume_ledger.executions),
        "trace_event_count": len(trace),
        "secret_leaked_in_trace": has_secret_leak(trace) or has_secret_leak(interrupt_payload),
        "new_graph_instance": True,
        "same_thread_id": True,
        "latency_ms": int((time.perf_counter() - started) * 1000),
    }


def sqlite_prepare_subprocess(db_path: str, meta_path: str) -> None:
    from langgraph.checkpoint.sqlite import SqliteSaver

    thread_id = f"thread_sqlite_subprocess_{uuid.uuid4().hex[:8]}"
    ledger = ToolLedger()
    with SqliteSaver.from_conn_string(db_path) as saver:
        graph = build_graph(ledger, checkpointer=saver)
        pending = invoke_until_interrupt(graph, base_state(), thread_id)
        interrupt_payload = extract_interrupt_payload(pending["result"])
    payload = {
        "thread_id": thread_id,
        "config": pending["config"],
        "interrupt_payload": interrupt_payload,
        "tool_execution_count_before_restart": len(ledger.executions),
    }
    Path(meta_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def sqlite_resume_subprocess(
    db_path: str,
    meta_path: str,
    result_path: str,
    ledger_path: str | None = None,
    start_gate_path: str | None = None,
) -> None:
    from langgraph.checkpoint.sqlite import SqliteSaver

    if start_gate_path is not None:
        gate = Path(start_gate_path)
        while not gate.exists():
            time.sleep(0.01)

    meta = json.loads(Path(meta_path).read_text(encoding="utf-8"))
    interrupt_payload = meta.get("interrupt_payload")
    if not isinstance(interrupt_payload, dict):
        result = {
            "status": "failed",
            "reason": "interrupt_payload_missing",
        }
    else:
        ledger = FileToolLedger(Path(ledger_path)) if ledger_path is not None else ToolLedger()
        with SqliteSaver.from_conn_string(db_path) as saver:
            graph = build_graph(ledger, checkpointer=saver)
            final_state = resume_graph(
                graph,
                meta["config"],
                {"approved": True, "args_hash": interrupt_payload["args_hash"]},
            )
        trace = final_state.get("trace", []) if isinstance(final_state, dict) else []
        result = {
            "status": "completed",
            "thread_id": meta["thread_id"],
            "approval_status": final_state.get("approval_status") if isinstance(final_state, dict) else None,
            "blocked_reason": final_state.get("blocked_reason") if isinstance(final_state, dict) else None,
            "tool_execution_count_before_restart": meta["tool_execution_count_before_restart"],
            "tool_execution_count_after_restart": len(ledger.executions),
            "trace_event_count": len(trace),
            "secret_leaked_in_trace": has_secret_leak(trace) or has_secret_leak(interrupt_payload),
        }
    Path(result_path).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


def run_sqlite_subprocess_restart_case() -> dict[str, Any]:
    try:
        import langgraph.checkpoint.sqlite  # noqa: F401
    except ImportError:
        return {
            "case": "sqlite_subprocess_restart",
            "status": "skipped",
            "reason": "langgraph_checkpoint_sqlite_not_installed",
        }

    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="langgraph-subprocess-checkpoint-") as tmpdir:
        tmp_path = Path(tmpdir)
        db_path = tmp_path / "checkpoints.sqlite"
        meta_path = tmp_path / "pending.json"
        result_path = tmp_path / "result.json"
        script_path = Path(__file__).resolve()
        prepare = subprocess.run(
            [sys.executable, str(script_path), "_sqlite_prepare", str(db_path), str(meta_path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if prepare.returncode != 0:
            return {
                "case": "sqlite_subprocess_restart",
                "status": "failed",
                "reason": "prepare_subprocess_failed",
                "prepare_stderr_preview": prepare.stderr[:500],
            }
        resume = subprocess.run(
            [sys.executable, str(script_path), "_sqlite_resume", str(db_path), str(meta_path), str(result_path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if resume.returncode != 0:
            return {
                "case": "sqlite_subprocess_restart",
                "status": "failed",
                "reason": "resume_subprocess_failed",
                "resume_stderr_preview": resume.stderr[:500],
            }
        result = json.loads(result_path.read_text(encoding="utf-8"))

    return {
        "case": "sqlite_subprocess_restart",
        "checkpointer": "SqliteSaver",
        "new_python_processes": True,
        "same_thread_id": True,
        "latency_ms": int((time.perf_counter() - started) * 1000),
        **result,
    }


def jsonl_record_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def run_sqlite_concurrent_resume_case() -> dict[str, Any]:
    try:
        import langgraph.checkpoint.sqlite  # noqa: F401
    except ImportError:
        return {
            "case": "sqlite_concurrent_resume",
            "status": "skipped",
            "reason": "langgraph_checkpoint_sqlite_not_installed",
        }

    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="langgraph-concurrent-checkpoint-") as tmpdir:
        tmp_path = Path(tmpdir)
        db_path = tmp_path / "checkpoints.sqlite"
        meta_path = tmp_path / "pending.json"
        side_effect_path = tmp_path / "side_effects.jsonl"
        gate_path = tmp_path / "resume.gate"
        result_paths = [tmp_path / "resume_a.json", tmp_path / "resume_b.json"]
        script_path = Path(__file__).resolve()
        prepare = subprocess.run(
            [sys.executable, str(script_path), "_sqlite_prepare", str(db_path), str(meta_path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if prepare.returncode != 0:
            return {
                "case": "sqlite_concurrent_resume",
                "status": "failed",
                "reason": "prepare_subprocess_failed",
                "prepare_stderr_preview": prepare.stderr[:500],
            }

        processes = [
            subprocess.Popen(
                [
                    sys.executable,
                    str(script_path),
                    "_sqlite_resume",
                    str(db_path),
                    str(meta_path),
                    str(result_path),
                    str(side_effect_path),
                    str(gate_path),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for result_path in result_paths
        ]
        time.sleep(0.2)
        gate_path.write_text("go", encoding="utf-8")
        completed = [process.communicate(timeout=30) for process in processes]
        failed = [
            {"index": index, "returncode": process.returncode, "stderr_preview": stderr[:500]}
            for index, (process, (_stdout, stderr)) in enumerate(zip(processes, completed))
            if process.returncode != 0
        ]
        if failed:
            return {
                "case": "sqlite_concurrent_resume",
                "status": "failed",
                "reason": "resume_subprocess_failed",
                "failures": failed,
            }
        resume_results = [json.loads(path.read_text(encoding="utf-8")) for path in result_paths]
        shared_execution_count = jsonl_record_count(side_effect_path)

    approval_statuses = [result.get("approval_status") for result in resume_results]
    return {
        "case": "sqlite_concurrent_resume",
        "status": "completed",
        "checkpointer": "SqliteSaver",
        "new_python_processes": True,
        "concurrent_resume_attempts": len(resume_results),
        "resume_statuses": [result.get("status") for result in resume_results],
        "approval_statuses": approval_statuses,
        "tool_execution_count_shared": shared_execution_count,
        "all_resume_processes_completed": all(result.get("status") == "completed" for result in resume_results),
        "secret_leaked_in_trace": any(result.get("secret_leaked_in_trace") for result in resume_results),
        "latency_ms": int((time.perf_counter() - started) * 1000),
    }


def run_validation() -> dict[str, Any]:
    try:
        import langgraph  # noqa: F401
    except ImportError:
        return {
            "status": "skipped",
            "reason": "langgraph_not_installed",
            "versions": versions(),
        }
    cases = [
        run_case("approved_once", "approved"),
        run_case("duplicate_resume", "approved"),
        run_case("rejected_resume", "rejected"),
        run_case("tampered_args", "tampered"),
        run_side_effect_risk_case(),
        run_sqlite_restart_case(),
        run_sqlite_subprocess_restart_case(),
        run_sqlite_concurrent_resume_case(),
    ]
    persistent_restart_tested = any(
        case.get("case") in {"sqlite_process_restart", "sqlite_subprocess_restart"}
        and case.get("status") == "completed"
        for case in cases
    )
    return {
        "status": "completed",
        "versions": versions(),
        "checkpointer": "MemorySaver + optional SqliteSaver",
        "persistent_restart_tested": persistent_restart_tested,
        "case_count": len(cases),
        "cases": cases,
        "limitations": [
            "The SQLite subprocess and concurrent resume cases use local Python processes and local SQLite; they are not deployed service restart or failure-injection tests.",
            "The refund tool is local and fake; no real payment, database, email, or external API is called.",
            "Results only cover the selected LangGraph version, Python version, graph shape, and local runtime.",
        ],
    }


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "_sqlite_prepare":
        sqlite_prepare_subprocess(sys.argv[2], sys.argv[3])
        return
    if len(sys.argv) > 1 and sys.argv[1] == "_sqlite_resume":
        ledger_path = sys.argv[5] if len(sys.argv) > 5 else None
        start_gate_path = sys.argv[6] if len(sys.argv) > 6 else None
        sqlite_resume_subprocess(sys.argv[2], sys.argv[3], sys.argv[4], ledger_path, start_gate_path)
        return
    print(json.dumps(run_validation(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
