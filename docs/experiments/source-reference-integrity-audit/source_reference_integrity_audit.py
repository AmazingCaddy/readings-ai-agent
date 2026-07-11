#!/usr/bin/env python3
"""Audit local source-card and reference link integrity.

This deterministic harness checks handbook reference structure, not source truth.
It verifies that source-card files are indexed, contain required metadata and
sections, chapter reference blocks exist, and local Markdown links resolve to
files in the repository.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[3]
SOURCE_CARD_DIR = ROOT / "docs/sources/source-cards"
SOURCE_CARD_INDEX = ROOT / "docs/sources/source-card-index.md"

REQUIRED_METADATA = (
    "来源链接",
    "最后复核日期",
    "类型",
    "主题",
    "可信度等级",
    "是否已验证",
)

REQUIRED_SECTIONS = (
    "## 一句话总结",
    "## 核心结论",
    "## 是否进入正文",
)

LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class AuditResult:
    check_id: str
    passed: bool
    observed: Any
    expected: str


def source_card_files() -> list[Path]:
    return sorted(path for path in SOURCE_CARD_DIR.glob("*.md") if path.name != "index.md")


def markdown_links(path: Path) -> list[str]:
    return [match.group(1).strip() for match in LINK_PATTERN.finditer(path.read_text(encoding="utf-8"))]


def is_external_link(link: str) -> bool:
    return link.startswith(("http://", "https://", "mailto:"))


def resolve_local_link(path: Path, link: str) -> Path | None:
    if is_external_link(link) or link.startswith("#"):
        return None
    raw_target = link.split("#", 1)[0].split("?", 1)[0].strip()
    if not raw_target:
        return None
    raw_target = raw_target.strip("<>")
    return (path.parent / unquote(raw_target)).resolve()


def audit_source_card_index() -> list[AuditResult]:
    card_files = {path.name for path in source_card_files()}
    index_links = [link for link in markdown_links(SOURCE_CARD_INDEX) if link.startswith("source-cards/")]
    linked_files = {Path(link.split("#", 1)[0]).name for link in index_links}
    missing_files = sorted(link for link in index_links if not (SOURCE_CARD_INDEX.parent / link).exists())
    unindexed_files = sorted(card_files - linked_files)
    return [
        AuditResult(
            "source_card_index_links_exist",
            not missing_files,
            {"index_links": len(index_links), "missing_files": missing_files},
            "Every source-card link in docs/sources/source-card-index.md resolves to an existing card file.",
        ),
        AuditResult(
            "source_card_files_are_indexed",
            not unindexed_files,
            {"source_card_files": len(card_files), "unindexed_files": unindexed_files},
            "Every source-card Markdown file except source-cards/index.md is listed in the source-card index.",
        ),
    ]


def audit_source_card_shape() -> list[AuditResult]:
    missing_metadata: dict[str, list[str]] = {}
    missing_sections: dict[str, list[str]] = {}
    missing_url: list[str] = []
    for path in source_card_files():
        text = path.read_text(encoding="utf-8")
        metadata_gaps = [field for field in REQUIRED_METADATA if f"- {field}" not in text]
        section_gaps = [section for section in REQUIRED_SECTIONS if section not in text]
        if metadata_gaps:
            missing_metadata[path.name] = metadata_gaps
        if section_gaps:
            missing_sections[path.name] = section_gaps
        if not re.search(r"https?://", text):
            missing_url.append(path.name)
    return [
        AuditResult(
            "source_cards_have_required_metadata",
            not missing_metadata,
            {"checked_files": len(source_card_files()), "missing_metadata": missing_metadata},
            "Every source card has required metadata fields for source, review date, type, topic, trust level, and validation status.",
        ),
        AuditResult(
            "source_cards_have_required_sections",
            not missing_sections,
            {"checked_files": len(source_card_files()), "missing_sections": missing_sections},
            "Every source card has summary, core conclusions, and body-inclusion decision sections.",
        ),
        AuditResult(
            "source_cards_include_external_url",
            not missing_url,
            {"missing_url": missing_url},
            "Every source card contains at least one external URL for traceability.",
        ),
    ]


def audit_chapter_references() -> list[AuditResult]:
    chapters = sorted((ROOT / "docs/chapters").glob("[0-9][0-9]-*.md"))
    missing_references = [str(path.relative_to(ROOT)) for path in chapters if "## References" not in path.read_text(encoding="utf-8")]
    missing_source_card_link: list[str] = []
    for path in chapters:
        if path.name in {"00-preface.md", "12-source-map.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "../sources/source-cards/" not in text:
            missing_source_card_link.append(str(path.relative_to(ROOT)))
    return [
        AuditResult(
            "chapters_have_references_sections",
            not missing_references,
            {"chapters": len(chapters), "missing_references": missing_references},
            "Every numbered chapter has a References section.",
        ),
        AuditResult(
            "content_chapters_link_source_cards",
            not missing_source_card_link,
            {"missing_source_card_link": missing_source_card_link},
            "Every content chapter from 01 through 11 links to at least one source card.",
        ),
    ]


def audit_local_markdown_links() -> list[AuditResult]:
    scanned_paths = [SOURCE_CARD_INDEX, *source_card_files(), *sorted((ROOT / "docs/chapters").glob("[0-9][0-9]-*.md"))]
    broken_links: list[dict[str, str]] = []
    local_link_count = 0
    for path in scanned_paths:
        for link in markdown_links(path):
            target = resolve_local_link(path, link)
            if target is None:
                continue
            local_link_count += 1
            if not target.exists():
                broken_links.append({"path": str(path.relative_to(ROOT)), "link": link})
    return [
        AuditResult(
            "local_markdown_links_resolve",
            not broken_links,
            {"scanned_files": len(scanned_paths), "local_links": local_link_count, "broken_links": broken_links},
            "Local Markdown links from source cards, source-card index, and chapters resolve to existing files.",
        )
    ]


def main() -> None:
    audits = audit_source_card_index() + audit_source_card_shape() + audit_chapter_references() + audit_local_markdown_links()
    payload = {
        "status": "completed",
        "control": "deterministic_source_reference_integrity_audit",
        "external_url_checked": False,
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
