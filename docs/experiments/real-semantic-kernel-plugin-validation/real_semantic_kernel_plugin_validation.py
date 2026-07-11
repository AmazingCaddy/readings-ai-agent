#!/usr/bin/env python3
"""Run a local Semantic Kernel native plugin validation harness."""

from __future__ import annotations

import asyncio
import json
from typing import Any


SECRET_MARKER = "secret=example-sk-token"


def redact(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace(SECRET_MARKER, "[REDACTED_SECRET]")
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


async def run_validation_async() -> dict[str, Any]:
    try:
        import semantic_kernel as sk
        from semantic_kernel import Kernel
        from semantic_kernel.functions import kernel_function
    except ImportError as exc:
        reason = "semantic_kernel_not_installed" if "No module named" in str(exc) else "semantic_kernel_import_error"
        return {
            "status": "skipped",
            "reason": reason,
            "error": str(exc),
            "install_note": "Run with `uv run --with semantic-kernel ...` to collect local Semantic Kernel plugin traces.",
        }

    side_effects: list[dict[str, Any]] = []

    class RefundPlugin:
        @kernel_function(name="read_order", description="Read order summary")
        def read_order(self, order_id: str) -> str:
            return f"order={order_id};status=paid"

        @kernel_function(name="issue_refund", description="Issue a refund after application approval")
        def issue_refund(self, order_id: str, amount: float) -> str:
            side_effects.append({"order_id": order_id, "amount": amount})
            return f"refund_issued:{order_id}:{amount:.2f}"

    kernel = Kernel()
    kernel.add_plugin(RefundPlugin(), plugin_name="refund")
    metadata = kernel.get_full_list_of_function_metadata()
    issue_refund = kernel.get_function("refund", "issue_refund")
    read_order = kernel.get_function("refund", "read_order")

    trace: list[dict[str, Any]] = []

    async def invoke_with_policy(function: Any, approved: bool, **kwargs: Any) -> str:
        if function.metadata.name == "issue_refund" and not approved:
            trace.append(
                {
                    "op": "policy_reject",
                    "plugin": function.metadata.plugin_name,
                    "function": function.metadata.name,
                    "forwarded_to_kernel": False,
                    "arguments": redact(kwargs),
                }
            )
            return "blocked_by_application_policy"
        trace.append(
            {
                "op": "kernel_invoke",
                "plugin": function.metadata.plugin_name,
                "function": function.metadata.name,
                "arguments": redact(kwargs),
            }
        )
        result = await kernel.invoke(function, **kwargs)
        return str(result)

    read_result = await invoke_with_policy(read_order, approved=True, order_id="order-1")
    blocked_result = await invoke_with_policy(issue_refund, approved=False, order_id="order-1", amount=25.0)
    side_effect_count_after_blocked = len(side_effects)

    missing_required_rejected = False
    invalid_type_rejected = False
    coerced_amount_result = ""
    approved_result = ""
    try:
        await kernel.invoke(issue_refund, order_id="order-1")
    except Exception as exc:  # Semantic Kernel raises a version-specific invoke exception type.
        missing_required_rejected = "amount" in str(exc) or exc.__class__.__name__.endswith("Exception")
        trace.append({"op": "kernel_error", "case": "missing_required", "error_type": exc.__class__.__name__})
    try:
        await kernel.invoke(issue_refund, order_id="order-1", amount="not-a-number")
    except Exception as exc:
        invalid_type_rejected = "amount" in str(exc) or exc.__class__.__name__.endswith("Exception")
        trace.append({"op": "kernel_error", "case": "invalid_type", "error_type": exc.__class__.__name__})

    coerced_amount_result = await invoke_with_policy(issue_refund, approved=True, order_id="order-2", amount="12.5")
    approved_result = await invoke_with_policy(issue_refund, approved=True, order_id="order-3", amount=30.0)

    function_names = sorted(f"{item.plugin_name}.{item.name}" for item in metadata)
    issue_metadata = next(item for item in metadata if item.name == "issue_refund")
    amount_parameter = next(item for item in issue_metadata.parameters if item.name == "amount")

    cases = [
        {
            "name": "metadata_exposes_plugin_functions",
            "passed": function_names == ["refund.issue_refund", "refund.read_order"]
            and amount_parameter.type_ == "float"
            and amount_parameter.is_required is True,
        },
        {"name": "read_function_invokes", "passed": read_result == "order=order-1;status=paid"},
        {
            "name": "application_policy_blocks_write_before_kernel",
            "passed": blocked_result == "blocked_by_application_policy" and side_effect_count_after_blocked == 0,
        },
        {"name": "missing_required_argument_rejected", "passed": missing_required_rejected},
        {"name": "invalid_argument_type_rejected", "passed": invalid_type_rejected},
        {"name": "coercible_argument_invokes", "passed": coerced_amount_result == "refund_issued:order-2:12.50"},
        {"name": "approved_write_invokes_once", "passed": approved_result == "refund_issued:order-3:30.00"},
    ]

    trace_json = json.dumps(trace, ensure_ascii=False)
    return {
        "status": "completed",
        "framework": "semantic-kernel",
        "version": getattr(sk, "__version__", "unknown"),
        "plugin_count": len(kernel.plugins),
        "function_count": len(metadata),
        "function_names": function_names,
        "missing_required_rejected": missing_required_rejected,
        "invalid_type_rejected": invalid_type_rejected,
        "coercible_argument_invoked": coerced_amount_result == "refund_issued:order-2:12.50",
        "rejected_write_forwarded": any(item.get("op") == "kernel_invoke" and item.get("function") == "issue_refund" and item.get("arguments", {}).get("order_id") == "order-1" for item in trace),
        "approved_write_count": len(side_effects),
        "case_count": len(cases),
        "passed_count": sum(1 for case in cases if case["passed"]),
        "all_passed": all(case["passed"] for case in cases),
        "secret_leaked_in_trace": SECRET_MARKER in trace_json,
        "cases": cases,
        "trace": trace,
    }


def run_validation() -> dict[str, Any]:
    return asyncio.run(run_validation_async())


def main() -> None:
    print(json.dumps(run_validation(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
