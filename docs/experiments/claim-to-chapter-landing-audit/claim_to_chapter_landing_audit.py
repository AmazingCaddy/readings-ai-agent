#!/usr/bin/env python3
"""Audit whether claim-ledger body-entry claims land in target chapters.

This deterministic harness parses `docs/evidence/claim-ledger.md`, extracts
`可入正文` rows and their target chapters from the 正文写法 column, then checks
that each declared target chapter contains a concrete textual landing for the
claim. It is a text-alignment audit only; it does not validate external facts.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CLAIM_LEDGER = ROOT / "docs/evidence/claim-ledger.md"
CHAPTER_DIR = ROOT / "docs/chapters"

TARGET_CHAPTER_PATTERN = re.compile(r"第\s*([0-9]{2}(?:/[0-9]{2})*)\s*章")

GENERIC_ANCHORS = {
    "Agent",
    "API",
    "LLM",
    "RAG",
    "MCP",
    "Memory",
    "Tool",
    "Function",
    "calling",
    "tool",
    "function",
    "schema",
    "trace",
    "prompt",
    "Responses",
    "Benchmark",
    "Cookbook",
    "recipe",
    "Browser",
    "真实",
    "生产",
    "成本",
    "延迟",
}


@dataclass(frozen=True)
class ClaimRow:
    claim: str
    references: str
    status: str
    chapter_wording: str


@dataclass(frozen=True)
class AuditResult:
    check_id: str
    passed: bool
    observed: Any
    expected: str


def is_cjk(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def parse_claim_rows() -> list[ClaimRow]:
    rows: list[ClaimRow] = []
    for line in CLAIM_LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ") or line.startswith("| ---") or "结论" in line[:20]:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 4:
            rows.append(ClaimRow(cells[0], cells[1], cells[2], cells[3]))
    return rows


def body_entry_rows() -> list[ClaimRow]:
    return [row for row in parse_claim_rows() if row.status == "可入正文"]


def target_chapter_numbers(row: ClaimRow) -> list[str]:
    numbers: list[str] = []
    for match in TARGET_CHAPTER_PATTERN.findall(row.chapter_wording):
        numbers.extend(part.strip() for part in match.split("/") if part.strip())
    return numbers


def chapter_path(number: str) -> Path | None:
    matches = sorted(CHAPTER_DIR.glob(f"{number}-*.md"))
    return matches[0] if matches else None


def candidate_anchors(claim: str) -> list[str]:
    anchors: list[str] = []
    for raw_part in re.split(r"[，；。：“”、,;:()（）/]+|\s+", claim):
        part = raw_part.strip("` ")
        if not part or part in GENERIC_ANCHORS:
            continue
        if is_cjk(part) and len(part) >= 4:
            anchors.append(part)
        elif not is_cjk(part) and len(part) >= 4:
            anchors.append(part)
    return anchors


def landing_evidence(chapter_text: str, claim: str) -> dict[str, Any]:
    anchors = candidate_anchors(claim)
    hits = [anchor for anchor in anchors if anchor in chapter_text]
    strong_hits = [anchor for anchor in hits if is_cjk(anchor) and len(anchor) >= 8]
    return {
        "passed": bool(strong_hits) or len(hits) >= 2,
        "anchors": anchors,
        "hits": hits,
        "strong_hits": strong_hits,
    }


def audit_target_declarations(rows: list[ClaimRow]) -> list[AuditResult]:
    missing_targets = [row.claim for row in rows if not target_chapter_numbers(row)]
    missing_chapter_files: list[dict[str, Any]] = []
    for row in rows:
        for number in target_chapter_numbers(row):
            if chapter_path(number) is None:
                missing_chapter_files.append({"claim": row.claim, "chapter": number})
    return [
        AuditResult(
            "body_entry_claims_declare_target_chapters",
            not missing_targets,
            {"missing_targets": missing_targets},
            "Every 可入正文 row declares target chapters in 正文写法.",
        ),
        AuditResult(
            "declared_target_chapter_files_exist",
            not missing_chapter_files,
            {"missing_chapter_files": missing_chapter_files},
            "Every declared target chapter number resolves to a chapter file.",
        ),
    ]


def audit_chapter_landings(rows: list[ClaimRow]) -> list[AuditResult]:
    missing_landings: list[dict[str, Any]] = []
    landing_records: list[dict[str, Any]] = []
    for row in rows:
        for number in target_chapter_numbers(row):
            path = chapter_path(number)
            if path is None:
                continue
            evidence = landing_evidence(path.read_text(encoding="utf-8"), row.claim)
            record = {
                "claim": row.claim,
                "chapter": path.name,
                "passed": evidence["passed"],
                "hits": evidence["hits"],
                "strong_hits": evidence["strong_hits"],
            }
            landing_records.append(record)
            if not evidence["passed"]:
                missing_landings.append(record | {"anchors": evidence["anchors"]})
    return [
        AuditResult(
            "body_entry_claims_land_in_each_declared_chapter",
            not missing_landings,
            {
                "landing_count": len(landing_records),
                "missing_landings": missing_landings,
            },
            "Each 可入正文 row has a concrete textual landing in every declared target chapter.",
        )
    ]


def main() -> None:
    rows = body_entry_rows()
    audits = audit_target_declarations(rows) + audit_chapter_landings(rows)
    target_count = sum(len(target_chapter_numbers(row)) for row in rows)
    payload = {
        "status": "completed",
        "control": "deterministic_claim_to_chapter_landing_audit",
        "real_fact_validation": False,
        "all_passed": all(audit.passed for audit in audits),
        "check_count": len(audits),
        "body_entry_claim_count": len(rows),
        "declared_target_count": target_count,
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
