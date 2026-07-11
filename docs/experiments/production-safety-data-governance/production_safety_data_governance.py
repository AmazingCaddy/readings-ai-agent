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


@dataclass(frozen=True)
class DataFlowItem:
    surface_id: str
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


DATA_FLOW_CHECKS = [
    DataFlowItem(
        "remote_mcp_tool",
        ("OpenAI Data Controls", "Anthropic MCP docs"),
        (
            "data_sent",
            "third_party_retention",
            "authorization_owner",
            "allowlist_or_denylist",
            "user_disclosure",
            "trace_redaction",
        ),
        "Remote MCP tools are third-party data flows and need explicit authorization, exposure, retention, and trace notes.",
    ),
    DataFlowItem(
        "hosted_code_or_shell",
        ("OpenAI Data Controls",),
        (
            "input_artifacts",
            "container_state",
            "expiration_or_delete",
            "secret_policy",
            "audit_owner",
        ),
        "Hosted execution tools can create temporary application state and need cleanup and secret-handling boundaries.",
    ),
    DataFlowItem(
        "file_or_vector_store",
        ("OpenAI Data Controls", "OpenAI File Search / Retrieval docs"),
        (
            "uploaded_objects",
            "vector_store_owner",
            "expiration_policy",
            "delete_path",
            "citation_trace",
            "residency_review",
        ),
        "Files and vector stores are application-state objects, not just prompt text, so retention, deletion, and citation trace need separate records.",
    ),
    DataFlowItem(
        "prompt_caching",
        ("OpenAI Batch / Flex / Prompt Caching docs", "OpenAI Data Controls"),
        (
            "cache_eligible_prefix",
            "sensitive_prefix_policy",
            "cache_usage_fields",
            "retention_boundary_review",
        ),
        "Prompt caching changes observability and retention questions for repeated prefixes; sensitive prefixes need an explicit policy.",
    ),
    DataFlowItem(
        "browser_or_computer_use",
        ("Anthropic Computer Use docs", "Browser Use / Playwright docs"),
        (
            "profile_scope",
            "uploaded_files",
            "external_site_data",
            "approval_required_actions",
            "screenshot_redaction",
            "failure_review_owner",
        ),
        "Browser and computer-use runs expose profile state, uploads, screenshots, and external sites, so they need an object-level data-flow review.",
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


DATA_FLOW_CONFIGS: dict[str, dict[str, dict[str, Any]]] = {
    "naive_project": {
        "remote_mcp_tool": {
            "data_sent": ["customer_email", "order_notes"],
            "allowlist_or_denylist": ["crm.example-mcp.com"],
        },
        "hosted_code_or_shell": {
            "input_artifacts": ["support_export.csv"],
            "container_state": "temporary_files",
        },
        "file_or_vector_store": {
            "uploaded_objects": ["policy.pdf"],
            "citation_trace": "file_citation_annotations",
        },
        "prompt_caching": {
            "cache_eligible_prefix": "shared_system_prompt_and_tool_schema",
            "cache_usage_fields": ["cached_tokens", "cache_write_tokens"],
        },
        "browser_or_computer_use": {
            "profile_scope": "default_browser_profile",
            "uploaded_files": ["invoice.csv"],
            "approval_required_actions": ["submit_order"],
        },
    },
    "governed_project": {
        "remote_mcp_tool": {
            "data_sent": ["customer_email", "order_notes"],
            "third_party_retention": "vendor_dpa_section_4",
            "authorization_owner": "security-platform",
            "allowlist_or_denylist": ["crm.example-mcp.com"],
            "user_disclosure": "admin_config_page",
            "trace_redaction": "hash_customer_email_and_drop_oauth_token",
        },
        "hosted_code_or_shell": {
            "input_artifacts": ["support_export.csv"],
            "container_state": "temporary_files_and_process_logs",
            "expiration_or_delete": "container_expiration_plus_delete_runbook",
            "secret_policy": "block_env_secret_export_and_scan_uploads",
            "audit_owner": "data-governance",
        },
        "file_or_vector_store": {
            "uploaded_objects": ["policy.pdf"],
            "vector_store_owner": "knowledge-platform",
            "expiration_policy": "90_day_expiration_or_document_owner_delete",
            "delete_path": "delete_file_and_vector_store_object",
            "citation_trace": "file_search_call_results_and_file_citations",
            "residency_review": "project_region_and_feature_support_checked",
        },
        "prompt_caching": {
            "cache_eligible_prefix": "stable_public_policy_prompt_and_tool_schema",
            "sensitive_prefix_policy": "no_customer_secrets_or_unique_personal_data_in_cached_prefix",
            "cache_usage_fields": ["cached_tokens", "cache_write_tokens"],
            "retention_boundary_review": "review_current_data_controls_before_enablement",
        },
        "browser_or_computer_use": {
            "profile_scope": "ephemeral_context_with_domain_allowlist",
            "uploaded_files": ["redacted_invoice.csv"],
            "external_site_data": "only_approved_demo_domain",
            "approval_required_actions": ["submit_order", "send_email", "purchase"],
            "screenshot_redaction": "mask_account_and_customer_identifiers",
            "failure_review_owner": "browser-automation-oncall",
        },
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


def audit_data_flows(project_name: str, config: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in DATA_FLOW_CHECKS:
        surface_config = config.get(item.surface_id, {})
        missing = [field for field in item.required_fields if not surface_config.get(field)]
        results.append(
            {
                "project": project_name,
                "surface_id": item.surface_id,
                "source_refs": list(item.source_refs),
                "passed": not missing,
                "missing_fields": missing,
                "required_fields": list(item.required_fields),
                "reason": item.reason,
            }
        )
    return results


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    def result_id(item: dict[str, Any]) -> str:
        return item["item_id"] if "item_id" in item else item["surface_id"]

    summary: dict[str, Any] = {}
    for project in sorted({result["project"] for result in results}):
        items = [result for result in results if result["project"] == project]
        summary[project] = {
            "passed": sum(1 for item in items if item["passed"]),
            "total": len(items),
            "failed_items": [result_id(item) for item in items if not item["passed"]],
            "missing_field_count": sum(len(item["missing_fields"]) for item in items),
        }
    return summary


def main() -> None:
    checklist_results = [result for name, config in PROJECTS.items() for result in audit_project(name, config)]
    data_flow_results = [
        result for name, config in DATA_FLOW_CONFIGS.items() for result in audit_data_flows(name, config)
    ]
    all_passed = all(item["passed"] for item in checklist_results if item["project"] == "governed_project") and all(
        item["passed"] for item in data_flow_results if item["project"] == "governed_project"
    )
    print(
        json.dumps(
            {
                "status": "completed",
                "control": "deterministic_safety_data_governance_fixtures",
                "real_project_validated": False,
                "all_passed": all_passed,
                "summary": summarize(checklist_results),
                "data_flow_summary": summarize(data_flow_results),
                "results": checklist_results,
                "data_flow_results": data_flow_results,
                "limitations": [
                    "This deterministic audit validates checklist and object-level data-flow fields only.",
                    "It does not inspect a real OpenAI project, organization settings, API logs, third-party tool retention, object deletion, data residency, moderation quality, or compliance status.",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
