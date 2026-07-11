#!/usr/bin/env python3
"""Deterministic production safety and data-governance checklist audit.

This script does not call OpenAI APIs or inspect a real account. It turns the
OpenAI Moderation and Safety/Data Controls documentation boundaries into a small
project-configuration audit so the handbook can validate checklist fields before
running a real project/account review.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ChecklistItem:
    item_id: str
    source_refs: tuple[str, ...]
    required_fields: tuple[str, ...]
    reason: str


CHECKLIST = [
    ChecklistItem(
        "moderation_policy_signals",
        ("OpenAI Moderation docs", "OpenAI Safety Best Practices"),
        ("moderation_stage", "policy_action", "human_review_queue", "failure_fallback"),
        "Moderation scores should feed policy routing and review, not be treated as a magic safety guarantee.",
    ),
    ChecklistItem(
        "tool_calling_moderation_coverage",
        ("OpenAI Moderation docs",),
        ("tool_arguments_checked", "tool_outputs_checked", "tool_schema_reviewed"),
        "Tool-call arguments and outputs can be covered, but tool names, descriptions, schemas, and response schemas need separate review.",
    ),
    ChecklistItem(
        "streaming_moderation_timing",
        ("OpenAI Moderation docs",),
        ("partial_delta_policy", "final_score_gate", "pre_action_buffer"),
        "Streaming moderation scores arrive after final output, so partial deltas need their own product policy.",
    ),
    ChecklistItem(
        "safety_identifier_logging",
        ("OpenAI Safety Best Practices",),
        ("safety_identifier", "privacy_preserving_hash", "log_join_key"),
        "Safety identifiers help abuse monitoring only if the app sends and logs a stable privacy-preserving identifier.",
    ),
    ChecklistItem(
        "api_key_revoke_runbook",
        ("OpenAI Safety Best Practices",),
        ("owner", "detection_signal", "revoke_step", "replacement_step", "impact_review"),
        "A compromised API key needs a rehearsable revoke and replacement path.",
    ),
    ChecklistItem(
        "abuse_logs_application_state_split",
        ("OpenAI Data Controls",),
        ("abuse_log_fields", "application_state_objects", "retention_owner", "delete_path"),
        "Abuse monitoring logs and application state are different data surfaces and need separate retention and deletion notes.",
    ),
    ChecklistItem(
        "remote_mcp_third_party_data_flow",
        ("OpenAI Data Controls", "Anthropic MCP docs"),
        ("remote_server", "data_sent", "third_party_retention", "allowlist", "user_disclosure"),
        "Remote MCP servers are third-party services, so their data flow and retention owner must be explicit.",
    ),
    ChecklistItem(
        "hosted_tool_application_state",
        ("OpenAI Data Controls",),
        ("hosted_tool", "container_state", "expiration_or_delete", "sensitive_data_policy"),
        "Hosted shell, code, file, or vector capabilities can create application state that needs a cleanup path.",
    ),
    ChecklistItem(
        "data_residency_boundary",
        ("OpenAI Data Controls",),
        ("project_region", "endpoint_supported", "system_data_exclusion", "unsupported_feature_note"),
        "Data residency is a project/endpoint capability boundary and does not apply to all system data or features.",
    ),
    ChecklistItem(
        "red_team_and_user_report_loop",
        ("OpenAI Safety Best Practices",),
        ("red_team_cases", "user_report_channel", "response_owner", "regression_update"),
        "Safety testing should feed a report/review/regression loop instead of remaining a one-time launch checklist.",
    ),
]


PROJECTS: dict[str, dict[str, Any]] = {
    "naive_project": {
        "moderation_stage": "inline",
        "policy_action": "auto_block_flagged_only",
        "tool_arguments_checked": True,
        "partial_delta_policy": "stream_to_user_immediately",
        "safety_identifier": None,
        "owner": "platform-team",
        "abuse_log_fields": ["prompt", "response"],
        "remote_server": "crm.example-mcp.com",
        "data_sent": ["customer_email", "order_notes"],
        "hosted_tool": "code_interpreter",
        "project_region": "eu",
        "red_team_cases": ["basic unsafe content"],
    },
    "governed_project": {
        "moderation_stage": "input_and_generated_output",
        "policy_action": "route_by_category_score_and_business_policy",
        "human_review_queue": "safety-review",
        "failure_fallback": "hold_action_and_log_error",
        "tool_arguments_checked": True,
        "tool_outputs_checked": True,
        "tool_schema_reviewed": True,
        "partial_delta_policy": "buffer_or_mark_unreviewed_until_final_score",
        "final_score_gate": "required_before_display_or_external_action",
        "pre_action_buffer": True,
        "safety_identifier": "hash(user_id, tenant_salt)",
        "privacy_preserving_hash": True,
        "log_join_key": "safety_identifier",
        "owner": "platform-security",
        "detection_signal": "secret-scanner-or-usage-anomaly",
        "revoke_step": "revoke_key_in_dashboard_or_api",
        "replacement_step": "rotate_secret_store_and_redeploy",
        "impact_review": "query_requests_since_last_known_good_time",
        "abuse_log_fields": ["prompt", "response", "classifier_output"],
        "application_state_objects": ["response_store", "vector_store", "hosted_container"],
        "retention_owner": "data-governance",
        "delete_path": "documented_per_object_type",
        "remote_server": "crm.example-mcp.com",
        "data_sent": ["customer_email", "order_notes"],
        "third_party_retention": "vendor_dpa_section_4",
        "allowlist": ["crm.example-mcp.com"],
        "user_disclosure": "admin_config_page",
        "hosted_tool": "code_interpreter",
        "container_state": "temporary_files_and_session_state",
        "expiration_or_delete": "container_expiration_plus_manual_delete",
        "sensitive_data_policy": "no_secrets_or_exported_customer_lists",
        "project_region": "eu",
        "endpoint_supported": True,
        "system_data_exclusion": "system_data_not_covered_by_residency",
        "unsupported_feature_note": "feature_matrix_review_required_before_enablement",
        "red_team_cases": ["prompt injection", "unsafe content", "tool misuse"],
        "user_report_channel": "in_product_report_button",
        "response_owner": "trust-and-safety-oncall",
        "regression_update": "add_confirmed_failure_to_safety_regression_set",
    },
}


def audit_project(project_name: str, config: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in CHECKLIST:
        missing = [field for field in item.required_fields if not config.get(field)]
        results.append(
            {
                "project": project_name,
                "item_id": item.item_id,
                "source_refs": list(item.source_refs),
                "passed": not missing,
                "missing_fields": missing,
                "required_fields": list(item.required_fields),
                "reason": item.reason,
            }
        )
    return results


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for project in sorted({result["project"] for result in results}):
        items = [result for result in results if result["project"] == project]
        summary[project] = {
            "passed": sum(1 for item in items if item["passed"]),
            "total": len(items),
            "failed_items": [item["item_id"] for item in items if not item["passed"]],
            "missing_field_count": sum(len(item["missing_fields"]) for item in items),
        }
    return summary


def main() -> None:
    results = [result for name, config in PROJECTS.items() for result in audit_project(name, config)]
    print(json.dumps({"summary": summarize(results), "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
