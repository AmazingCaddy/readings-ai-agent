#!/usr/bin/env python3
"""Validate Browser Use package surface without running a browser agent.

This harness checks temporary package installation, console script metadata, and
selected source-file surfaces. It intentionally avoids importing browser_use,
starting Playwright/Chromium, running a model, opening websites, or executing a
Browser Use agent task.
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import time
from pathlib import Path
from typing import Any


SECRET_MARKER = "secret=browser-use-package-demo-token"

SOURCE_CHECKS = {
    "browser_use/agent/service.py": ["class Agent", "allowed_domains", "sensitive"],
    "browser_use/browser/profile.py": ["class BrowserProfile", "allowed_domains", "highlight_elements"],
    "browser_use/tools/service.py": ["class Tools", "sensitive"],
    "browser_use/cli.py": ["def main", "browser-use"],
}

EXPECTED_CONSOLE_SCRIPTS = {"browser-use", "browser", "browseruse", "bu"}


def read_source_checks(distribution: importlib.metadata.Distribution) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for relative_path, needles in SOURCE_CHECKS.items():
        path = Path(distribution.locate_file(relative_path))
        if not path.exists():
            results[relative_path] = {"exists": False, "needles": {needle: False for needle in needles}}
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        results[relative_path] = {
            "exists": True,
            "size_bytes": path.stat().st_size,
            "needles": {needle: needle in text for needle in needles},
        }
    return results


def main() -> int:
    if importlib.util.find_spec("browser_use") is None:
        print(
            json.dumps(
                {
                    "status": "skipped",
                    "reason": "browser_use_not_installed",
                    "install_note": "Run with `uv run --with browser-use python docs/experiments/real-browser-use-package-validation/real_browser_use_package_validation.py`.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    started = time.perf_counter()
    distribution = importlib.metadata.distribution("browser-use")
    console_scripts = {
        entry_point.name: entry_point.value
        for entry_point in distribution.entry_points
        if entry_point.group == "console_scripts"
    }
    source_results = read_source_checks(distribution)
    expected_scripts_present = EXPECTED_CONSOLE_SCRIPTS.issubset(console_scripts)
    source_files_present = all(result["exists"] for result in source_results.values())
    source_needles_present = all(
        all(result["needles"].values()) for result in source_results.values() if result["exists"]
    )
    payload_text = json.dumps(source_results, ensure_ascii=False)
    secret_leaked_in_trace = SECRET_MARKER in payload_text
    all_passed = expected_scripts_present and source_files_present and source_needles_present and not secret_leaked_in_trace

    payload = {
        "status": "completed" if all_passed else "failed",
        "experiment": "real_browser_use_package_validation",
        "package": "browser-use",
        "package_version": distribution.version,
        "console_scripts": console_scripts,
        "expected_console_scripts_present": expected_scripts_present,
        "source_files_present": source_files_present,
        "source_needles_present": source_needles_present,
        "source_results": source_results,
        "browser_started": False,
        "model_called": False,
        "website_opened": False,
        "browser_agent_task_validated": False,
        "secret_leaked_in_trace": secret_leaked_in_trace,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "notes": [
            "This validates package metadata and selected source-file surfaces only.",
            "It does not import browser_use, start a browser, call a model, open a website, or run a Browser Use agent task.",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
