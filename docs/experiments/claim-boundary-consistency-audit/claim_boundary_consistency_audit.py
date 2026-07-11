#!/usr/bin/env python3
"""Audit claim boundary wording across the handbook evidence control files.

This deterministic harness does not validate factual correctness by itself. It
checks that the evidence control documents keep a machine-checkable separation
between narrow "可入正文" conclusions and broader real-model/API claims that
remain partial or pending.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]

BOUNDARY_MARKERS = (
    "仍属部分验证",
    "仍部分验证",
    "部分验证",
    "仍待",
    "待验证",
    "未验证",
    "不证明",
    "不能",
    "避免",
    "不应",
)

STALE_PHRASES = (
    "Real Prompt Injection / Permission harness 已准备入口，但 completed run 仍待做",
    "Real Tool Calling harness 已准备入口但 completed run 仍待做",
    "Real Moderation Safety harness 已准备入口，但 completed run 仍待做",
    "Real Prompt Injection / Permission harness 仍只支撑观测入口和记录模板已准备",
)


@dataclass(frozen=True)
class AuditResult:
    check_id: str
    passed: bool
    observed: Any
    expected: str


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def iter_table_rows(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| "):
            cells = split_markdown_row(line)
            if cells and all(set(cell) <= {"-", " ", ":"} for cell in cells):
                in_table = True
                continue
            if in_table:
                rows.append(cells)
            continue
        if in_table:
            break
    return rows


def has_boundary(text: str) -> bool:
    return any(marker in text for marker in BOUNDARY_MARKERS)


def audit_claim_ledger() -> list[AuditResult]:
    path = ROOT / "docs/evidence/claim-ledger.md"
    rows = iter_table_rows(path)
    claim_rows = [row for row in rows if len(row) >= 4 and row[2] == "可入正文"]
    missing_boundary = [row[0] for row in claim_rows if not has_boundary(row[3])]
    real_claims_without_boundary = [row[0] for row in claim_rows if "真实" in row[3] and not has_boundary(row[3])]
    return [
        AuditResult(
            "claim_ledger_rows_have_boundaries",
            not missing_boundary,
            {"claim_rows": len(claim_rows), "missing_boundary": missing_boundary},
            "Every 可入正文 row keeps a boundary marker in the 正文写法 cell.",
        ),
        AuditResult(
            "claim_ledger_real_claims_are_limited",
            not real_claims_without_boundary,
            {"real_claims_without_boundary": real_claims_without_boundary},
            "Rows mentioning 真实 model/API/framework behavior keep an explicit limitation marker.",
        ),
    ]


def audit_coverage_matrix() -> list[AuditResult]:
    path = ROOT / "docs/references/coverage-matrix.md"
    rows = iter_table_rows(path)
    theme_rows = [row for row in rows if len(row) >= 6 and row[0] != "主题"]
    missing_gap = [row[0] for row in theme_rows if not row[5].strip()]
    status_without_boundary = [row[0] for row in theme_rows if "可入正文" in row[4] and not has_boundary(row[4])]
    return [
        AuditResult(
            "coverage_matrix_rows_have_gaps",
            not missing_gap,
            {"theme_rows": len(theme_rows), "missing_gap": missing_gap},
            "Every coverage row keeps a non-empty 缺口 cell.",
        ),
        AuditResult(
            "coverage_matrix_statuses_have_boundaries",
            not status_without_boundary,
            {"status_without_boundary": status_without_boundary},
            "可入正文 status summaries keep partial/pending boundary wording.",
        ),
    ]


def audit_stale_phrases() -> list[AuditResult]:
    scanned_paths = [
        ROOT / "docs/evidence/claim-ledger.md",
        ROOT / "docs/references/coverage-matrix.md",
        ROOT / "docs/evidence/validation-backlog.md",
        ROOT / "docs/chapters/12-source-map.md",
        ROOT / "docs/chapters/09-production-security.md",
        ROOT / "docs/chapters/11-practice-roadmap.md",
    ]
    matches: list[dict[str, str]] = []
    for path in scanned_paths:
        text = path.read_text(encoding="utf-8")
        for phrase in STALE_PHRASES:
            if phrase in text:
                matches.append({"path": str(path.relative_to(ROOT)), "phrase": phrase})
    return [
        AuditResult(
            "stale_boundary_phrases_absent",
            not matches,
            {"matches": matches, "scanned_files": [str(path.relative_to(ROOT)) for path in scanned_paths]},
            "Known stale phrases that contradict completed no-key controls are absent.",
        )
    ]


def main() -> None:
    audits = audit_claim_ledger() + audit_coverage_matrix() + audit_stale_phrases()
    payload = {
        "status": "completed",
        "control": "deterministic_claim_boundary_text_audit",
        "real_fact_validation": False,
        "all_passed": all(audit.passed for audit in audits),
        "check_count": len(audits),
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
