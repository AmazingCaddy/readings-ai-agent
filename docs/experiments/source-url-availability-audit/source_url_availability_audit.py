#!/usr/bin/env python3
"""Live snapshot audit for primary source-card URLs.

This harness checks whether the primary URLs listed in source-card metadata are
currently reachable from the local environment. Network availability can change,
so failures are reported as attention items instead of process failures.
"""

from __future__ import annotations

import json
import re
import socket
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SOURCE_CARD_DIR = ROOT / "docs/sources/source-cards"
URL_PATTERN = re.compile(r'https?://[^\s`；;，,）)>"]+')
TIMEOUT_SECONDS = 8
USER_AGENT = "readings-ai-agent-source-url-audit/1.0"


@dataclass(frozen=True)
class UrlCheck:
    source_card: str
    url: str
    status: str
    http_status: int | None
    final_url: str | None
    error: str | None


def source_card_files() -> list[Path]:
    return sorted(path for path in SOURCE_CARD_DIR.glob("*.md") if path.name != "index.md")


def extract_primary_urls(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    collecting = False
    collected: list[str] = []
    for line in lines:
        if line.startswith("- 来源链接"):
            collecting = True
            collected.extend(URL_PATTERN.findall(line))
            continue
        if collecting:
            if line.startswith("- ") and not line.startswith("- 来源链接"):
                break
            collected.extend(URL_PATTERN.findall(line))
    return list(dict.fromkeys(url.rstrip(".") for url in collected))


def request_url(url: str, method: str) -> tuple[int, str]:
    request = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return response.status, response.geturl()


def check_url(source_card: str, url: str) -> UrlCheck:
    try:
        http_status, final_url = request_url(url, "HEAD")
    except urllib.error.HTTPError as exc:
        if exc.code in {405, 501}:
            try:
                http_status, final_url = request_url(url, "GET")
            except Exception as fallback_exc:  # noqa: BLE001 - report exact network issue.
                return UrlCheck(source_card, url, "attention", None, None, type(fallback_exc).__name__)
        else:
            return UrlCheck(source_card, url, "attention", exc.code, exc.geturl(), "HTTPError")
    except (urllib.error.URLError, TimeoutError, socket.timeout, ssl.SSLError) as exc:
        return UrlCheck(source_card, url, "attention", None, None, type(exc).__name__)
    except Exception as exc:  # noqa: BLE001 - live URL audit should classify, not crash.
        return UrlCheck(source_card, url, "attention", None, None, type(exc).__name__)

    status = "reachable" if 200 <= http_status < 400 else "attention"
    return UrlCheck(source_card, url, status, http_status, final_url, None)


def main() -> None:
    checks: list[UrlCheck] = []
    source_cards_without_primary_urls: list[str] = []
    for path in source_card_files():
        urls = extract_primary_urls(path)
        if not urls:
            source_cards_without_primary_urls.append(path.name)
            continue
        for url in urls:
            checks.append(check_url(path.name, url))

    attention_items = [check for check in checks if check.status != "reachable"]
    payload = {
        "status": "completed",
        "control": "live_primary_source_url_snapshot",
        "live_network_checked": True,
        "timeout_seconds": TIMEOUT_SECONDS,
        "source_card_count": len(source_card_files()),
        "url_count": len(checks),
        "reachable_count": sum(1 for check in checks if check.status == "reachable"),
        "attention_count": len(attention_items) + len(source_cards_without_primary_urls),
        "source_cards_without_primary_urls": source_cards_without_primary_urls,
        "attention_items": [
            {
                "source_card": check.source_card,
                "url": check.url,
                "http_status": check.http_status,
                "final_url": check.final_url,
                "error": check.error,
            }
            for check in attention_items
        ],
        "results": [
            {
                "source_card": check.source_card,
                "url": check.url,
                "status": check.status,
                "http_status": check.http_status,
                "final_url": check.final_url,
                "error": check.error,
            }
            for check in checks
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
