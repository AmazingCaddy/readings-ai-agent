#!/usr/bin/env python3
"""Audit chapter evidence alignment and boundary wording.

This deterministic harness checks chapter-level evidence hygiene: content
chapters should expose verified conclusions, pending questions, and links back
to the claim ledger / coverage matrix. It also checks that body-level claims
about 可入正文 or real-system behavior keep explicit boundary wording.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CHAPTER_DIR = ROOT / "docs/chapters"

BOUNDARY_MARKERS = (
    "仍需",
    "仍待",
    "仍属部分验证",
    "仍部分验证",
    "待验证",
    "未验证",
    "不证明",
    "不支持",
    "不支撑",
    "不等同",
    "不能",
    "不应",
    "不是",
    "没有被",
    "保守",
    "边界",
    "窄结论",
)

REAL_SYSTEM_TERMS = ("真实", "生产", "成本", "延迟", "可靠", "稳定", "默认")


@dataclass(frozen=True)
class AuditResult:
    check_id: str
    passed: bool
    observed: Any
    expected: str


def content_chapter_files() -> list[Path]:
    return sorted(
        path
        for path in CHAPTER_DIR.glob("[0-9][0-9]-*.md")
        if path.name not in {"00-preface.md", "12-source-map.md"}
    )


def section_body(text: str, heading: str) -> str:
    pattern = re.compile(rf"^{re.escape(heading)}\n(?P<body>.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def bullet_lines(section: str) -> list[str]:
    return [line.strip() for line in section.splitlines() if line.strip().startswith("- ")]


def has_boundary(text: str) -> bool:
    return any(marker in text for marker in BOUNDARY_MARKERS)


def audit_required_chapter_sections() -> list[AuditResult]:
    missing_verified: list[str] = []
    missing_pending: list[str] = []
    empty_verified: list[str] = []
    empty_pending: list[str] = []
    for path in content_chapter_files():
        text = path.read_text(encoding="utf-8")
        verified = section_body(text, "## 已验证结论")
        pending = section_body(text, "## 待验证问题")
        if not verified:
            missing_verified.append(path.name)
        elif not bullet_lines(verified):
            empty_verified.append(path.name)
        if not pending:
            missing_pending.append(path.name)
        elif not bullet_lines(pending):
            empty_pending.append(path.name)
    return [
        AuditResult(
            "content_chapters_have_verified_conclusions",
            not missing_verified and not empty_verified,
            {"missing_verified": missing_verified, "empty_verified": empty_verified},
            "Every content chapter has a non-empty 已验证结论 section.",
        ),
        AuditResult(
            "content_chapters_have_pending_questions",
            not missing_pending and not empty_pending,
            {"missing_pending": missing_pending, "empty_pending": empty_pending},
            "Every content chapter has a non-empty 待验证问题 section.",
        ),
    ]


def audit_reference_control_links() -> list[AuditResult]:
    missing_claim_ledger: list[str] = []
    missing_coverage_matrix: list[str] = []
    for path in content_chapter_files():
        text = path.read_text(encoding="utf-8")
        if "../evidence/claim-ledger.md" not in text:
            missing_claim_ledger.append(path.name)
        if "../references/coverage-matrix.md" not in text:
            missing_coverage_matrix.append(path.name)
    return [
        AuditResult(
            "content_chapters_link_claim_ledger",
            not missing_claim_ledger,
            {"missing_claim_ledger": missing_claim_ledger},
            "Every content chapter links to the claim ledger from References.",
        ),
        AuditResult(
            "content_chapters_link_coverage_matrix",
            not missing_coverage_matrix,
            {"missing_coverage_matrix": missing_coverage_matrix},
            "Every content chapter links to the coverage matrix from References.",
        ),
    ]


def audit_verified_conclusion_boundaries() -> list[AuditResult]:
    body_entry_without_boundary: list[dict[str, str]] = []
    real_system_without_boundary: list[dict[str, str]] = []
    for path in content_chapter_files():
        verified = section_body(path.read_text(encoding="utf-8"), "## 已验证结论")
        for line in bullet_lines(verified):
            if "可入正文" in line and not has_boundary(line):
                body_entry_without_boundary.append({"chapter": path.name, "line": line})
            if any(term in line for term in REAL_SYSTEM_TERMS) and not has_boundary(line):
                real_system_without_boundary.append({"chapter": path.name, "line": line})
    return [
        AuditResult(
            "body_entry_conclusion_bullets_keep_boundaries",
            not body_entry_without_boundary,
            {"body_entry_without_boundary": body_entry_without_boundary},
            "Verified-conclusion bullets mentioning 可入正文 keep explicit boundary wording.",
        ),
        AuditResult(
            "real_system_conclusion_bullets_keep_boundaries",
            not real_system_without_boundary,
            {"real_system_without_boundary": real_system_without_boundary},
            "Verified-conclusion bullets mentioning real production/model/cost/reliability behavior keep explicit boundary wording.",
        ),
    ]


def main() -> None:
    audits = audit_required_chapter_sections() + audit_reference_control_links() + audit_verified_conclusion_boundaries()
    payload = {
        "status": "completed",
        "control": "deterministic_chapter_evidence_alignment_audit",
        "real_fact_validation": False,
        "all_passed": all(audit.passed for audit in audits),
        "check_count": len(audits),
        "content_chapter_count": len(content_chapter_files()),
        "failed_checks": [audit.check_id for audit in audits if not audit.passed],
        "results": [
            {
                "check_id": audit.check_id,
                "passed": audit.passed,
                "observed": audit.observed,
                "expected": audit.expected,
            }
            for audit in audits
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
