#!/usr/bin/env python3
"""Audit whether chapter source-card references are represented in the claim ledger.

This deterministic harness checks traceability from content chapters to the
claim ledger: every source card directly referenced by chapters 01-11 should
appear in at least one claim-ledger support column, using either its title,
file-derived name, or a small explicit alias for locally established names.

It is a text traceability audit only. It does not validate the source content,
the truth of the claim, or the correctness of the chapter interpretation.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CHAPTER_DIR = ROOT / "docs/chapters"
SOURCE_CARD_DIR = ROOT / "docs/sources/source-cards"
CLAIM_LEDGER = ROOT / "docs/evidence/claim-ledger.md"

SOURCE_CARD_LINK_PATTERN = re.compile(r"\.\./sources/source-cards/([^\)#]+\.md)")

SOURCE_ALIASES: dict[str, list[str]] = {
    "2026-arize-phoenix-docs.md": ["Phoenix docs", "Arize Phoenix docs"],
    "2026-browser-use-playwright.md": ["Browser Use and Playwright"],
    "2026-google-responsible-ai-docs.md": ["Google Cloud Responsible AI docs", "Google Responsible AI"],
    "2026-mini-swe-agent-docs.md": ["mini-SWE-agent docs"],
    "2026-openai-batch-flex-prompt-caching-docs.md": [
        "OpenAI Batch / Flex / Prompt Caching docs",
        "OpenAI Batch / Flex / Prompt Caching",
    ],
    "2026-openai-file-search-retrieval-docs.md": [
        "OpenAI File Search and Retrieval docs",
        "OpenAI File Search / Retrieval docs",
    ],
    "2026-openai-production-cost-latency-docs.md": [
        "OpenAI Production / Cost / Latency / Rate Limit docs",
        "OpenAI Production / Cost / Latency docs",
    ],
    "2026-openai-safety-data-controls-docs.md": ["OpenAI Safety / Data Controls docs"],
}


@dataclass(frozen=True)
class AuditResult:
    check_id: str
    passed: bool
    observed: Any
    expected: str


def content_chapter_files() -> list[Path]:
    return sorted(
        path
        for path in CHAPTER_DIR.glob("[0-1][0-9]-*.md")
        if path.name not in {"00-preface.md", "12-source-map.md"}
    )


def chapter_source_card_names() -> list[str]:
    names: set[str] = set()
    for path in content_chapter_files():
        names.update(SOURCE_CARD_LINK_PATTERN.findall(path.read_text(encoding="utf-8")))
    return sorted(names)


def source_card_title(card_name: str) -> str:
    path = SOURCE_CARD_DIR / card_name
    if not path.exists():
        return card_name
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    return first_line.removeprefix("# ").strip()


def default_aliases(card_name: str) -> list[str]:
    title = source_card_title(card_name)
    title_prefix = re.sub(r"[:：].*", "", title).strip()
    stem_alias = re.sub(r"^\d{4}-", "", Path(card_name).stem).replace("-", " ").strip()
    aliases = [title, title_prefix, stem_alias]
    aliases.extend(SOURCE_ALIASES.get(card_name, []))
    deduped: list[str] = []
    for alias in aliases:
        if len(alias) >= 4 and alias not in deduped:
            deduped.append(alias)
    return deduped


def claim_ledger_support_text() -> str:
    support_cells: list[str] = []
    for line in CLAIM_LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ") or line.startswith("| ---") or "结论" in line[:20]:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 4:
            support_cells.append(cells[1])
    return "\n".join(support_cells).lower()


def audit_chapter_source_cards_resolve() -> list[AuditResult]:
    missing_files = [name for name in chapter_source_card_names() if not (SOURCE_CARD_DIR / name).exists()]
    return [
        AuditResult(
            "content_chapter_source_cards_resolve",
            not missing_files,
            {"missing_files": missing_files},
            "Every source card linked by chapters 01-11 resolves to an existing source-card file.",
        )
    ]


def audit_chapter_sources_have_claim_support() -> list[AuditResult]:
    support_text = claim_ledger_support_text()
    missing_support: list[dict[str, Any]] = []
    matched_records: list[dict[str, Any]] = []
    for name in chapter_source_card_names():
        aliases = default_aliases(name)
        matched = [alias for alias in aliases if alias.lower() in support_text]
        record = {"source_card": name, "title": source_card_title(name), "matched_aliases": matched}
        matched_records.append(record)
        if not matched:
            missing_support.append(record | {"candidate_aliases": aliases})
    return [
        AuditResult(
            "content_chapter_sources_appear_in_claim_ledger_support",
            not missing_support,
            {
                "content_chapter_source_card_count": len(matched_records),
                "missing_support": missing_support,
            },
            "Every source card directly linked by chapters 01-11 appears in the claim-ledger support column via title, file-derived alias, or explicit local alias.",
        )
    ]


def main() -> None:
    audits = audit_chapter_source_cards_resolve() + audit_chapter_sources_have_claim_support()
    payload = {
        "status": "completed",
        "control": "deterministic_source_to_claim_support_audit",
        "real_fact_validation": False,
        "all_passed": all(audit.passed for audit in audits),
        "check_count": len(audits),
        "content_chapter_count": len(content_chapter_files()),
        "content_chapter_source_card_count": len(chapter_source_card_names()),
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
