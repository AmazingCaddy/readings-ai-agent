#!/usr/bin/env python3
"""Audit source-card evidence and boundary wording quality.

This deterministic harness checks whether source cards that feed handbook body
claims keep explicit evidence and limitation sections. It does not validate the
external source content or whether the interpretation is factually correct.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE_CARD_DIR = ROOT / "docs/sources/source-cards"

BODY_ENTRY_MARKERS = ("结论：进入", "可入正文", "进入；")
EVIDENCE_MARKERS = (
    "HTTP",
    "抓取",
    "复核",
    "arXiv",
    "README",
    "运行",
    "completed run",
    "harness",
    "标准库",
    "官方",
    "摘要",
    "metadata",
    "source",
)
BOUNDARY_MARKERS = (
    "仍需",
    "仍待",
    "仍属部分验证",
    "仍部分验证",
    "部分验证",
    "待验证",
    "未验证",
    "不证明",
    "不能",
    "不应",
    "避免",
)


@dataclass(frozen=True)
class AuditResult:
    check_id: str
    passed: bool
    observed: Any
    expected: str


def source_card_files() -> list[Path]:
    return sorted(path for path in SOURCE_CARD_DIR.glob("*.md") if path.name != "index.md")


def section_body(text: str, heading: str) -> str:
    pattern = re.compile(rf"^{re.escape(heading)}\n(?P<body>.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def enters_body(text: str) -> bool:
    body = section_body(text, "## 是否进入正文")
    return any(marker in body for marker in BODY_ENTRY_MARKERS)


def has_marker(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)


def audit_body_entry_cards_have_evidence() -> list[AuditResult]:
    missing_evidence: list[str] = []
    weak_evidence: list[str] = []
    body_entry_count = 0
    for path in source_card_files():
        text = path.read_text(encoding="utf-8")
        if not enters_body(text):
            continue
        body_entry_count += 1
        evidence = section_body(text, "## 支撑证据")
        if not evidence:
            missing_evidence.append(path.name)
            continue
        if len([line for line in evidence.splitlines() if line.strip().startswith("-")]) < 1 or not has_marker(
            evidence, EVIDENCE_MARKERS
        ):
            weak_evidence.append(path.name)
    return [
        AuditResult(
            "body_entry_cards_have_supporting_evidence",
            not missing_evidence,
            {"body_entry_cards": body_entry_count, "missing_evidence": missing_evidence},
            "Every source card marked for body inclusion has a 支撑证据 section.",
        ),
        AuditResult(
            "supporting_evidence_has_observable_markers",
            not weak_evidence,
            {"weak_evidence": weak_evidence},
            "Supporting evidence contains at least one bullet and an observable evidence marker such as HTTP, fetch/review, run, README, arXiv, or official docs.",
        ),
    ]


def audit_body_entry_cards_keep_boundaries() -> list[AuditResult]:
    missing_boundary: list[str] = []
    missing_risk_section: list[str] = []
    for path in source_card_files():
        text = path.read_text(encoding="utf-8")
        if not enters_body(text):
            continue
        inclusion = section_body(text, "## 是否进入正文")
        risk = section_body(text, "## 可能的问题")
        if not risk:
            missing_risk_section.append(path.name)
        boundary_context = "\n".join([inclusion, risk, section_body(text, "## 后续验证")])
        if not has_marker(boundary_context, BOUNDARY_MARKERS):
            missing_boundary.append(path.name)
    return [
        AuditResult(
            "body_entry_cards_have_risk_sections",
            not missing_risk_section,
            {"missing_risk_section": missing_risk_section},
            "Every body-entry source card has a 可能的问题 section.",
        ),
        AuditResult(
            "body_entry_cards_keep_boundary_wording",
            not missing_boundary,
            {"missing_boundary": missing_boundary},
            "Every body-entry source card keeps explicit limitation wording in inclusion, risk, or follow-up sections.",
        ),
    ]


def audit_validation_status_boundaries() -> list[AuditResult]:
    broad_status_without_boundary: list[str] = []
    for path in source_card_files():
        text = path.read_text(encoding="utf-8")
        status_line = next((line for line in text.splitlines() if line.startswith("- 是否已验证：")), "")
        if "真实" in status_line and not has_marker(status_line, BOUNDARY_MARKERS):
            broad_status_without_boundary.append(path.name)
    return [
        AuditResult(
            "validation_status_limits_real_system_claims",
            not broad_status_without_boundary,
            {"broad_status_without_boundary": broad_status_without_boundary},
            "Validation status lines that mention real systems keep explicit limitation wording.",
        )
    ]


def main() -> None:
    audits = (
        audit_body_entry_cards_have_evidence()
        + audit_body_entry_cards_keep_boundaries()
        + audit_validation_status_boundaries()
    )
    payload = {
        "status": "completed",
        "control": "deterministic_source_card_evidence_quality_audit",
        "real_fact_validation": False,
        "all_passed": all(audit.passed for audit in audits),
        "check_count": len(audits),
        "source_card_count": len(source_card_files()),
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
