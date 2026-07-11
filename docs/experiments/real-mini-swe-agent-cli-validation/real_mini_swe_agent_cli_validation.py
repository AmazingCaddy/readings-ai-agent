#!/usr/bin/env python3
"""Validate the local mini-SWE-agent CLI surface without running an agent task.

The harness intentionally stops at import/help/config inspection. It verifies
that the package can be installed as a temporary dependency, that the public CLI
advertises the expected safety-relevant options, and that the packaged default
config still exposes confirm mode and a cost limit. It does not configure an API
key, ask a model to act, edit a repository, or validate issue-fixing quality.
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


SECRET_MARKER = "secret=mini-swe-cli-demo-token"


def strip_ansi(value: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", value)


def summarize_help(help_text: str) -> dict[str, Any]:
    expected_options = [
        "--model",
        "--task",
        "--yolo",
        "--cost-limit",
        "--config",
        "--output",
        "--model-class",
        "--agent-class",
        "--environment-class",
        "--exit-immediately",
    ]
    expected_terms = ["confirm", "yolo", "trajectory", "local environment"]
    return {
        "expected_options": {option: option in help_text for option in expected_options},
        "expected_terms": {term: term.lower() in help_text.lower() for term in expected_terms},
    }


def read_default_config() -> dict[str, Any]:
    distribution = importlib.metadata.distribution("mini-swe-agent")
    config_path = distribution.locate_file("minisweagent/config/mini.yaml")
    config_text = config_path.read_text(encoding="utf-8")
    return {
        "path_suffix": str(config_path).split("minisweagent")[-1],
        "mode_confirm_present": "mode: confirm" in config_text,
        "cost_limit_present": "cost_limit:" in config_text,
        "trajectory_present": "trajectory" in config_text,
        "independent_subshell_note_present": "subshell" in config_text.lower(),
    }


def main() -> int:
    if importlib.util.find_spec("minisweagent") is None:
        print(
            json.dumps(
                {
                    "status": "skipped",
                    "reason": "mini_swe_agent_not_installed",
                    "install_note": "Run with `uv run --with mini-swe-agent python docs/experiments/real-mini-swe-agent-cli-validation/real_mini_swe_agent_cli_validation.py`.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    cli_path = shutil.which("mini-swe-agent")
    if cli_path is None:
        print(
            json.dumps(
                {
                    "status": "skipped",
                    "reason": "mini_swe_agent_cli_not_on_path",
                    "package_version": importlib.metadata.version("mini-swe-agent"),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="mini-swe-agent-cli-") as temp_dir:
        temp_root = Path(temp_dir)
        env = os.environ.copy()
        env.update(
            {
                "HOME": str(temp_root / "home"),
                "XDG_CONFIG_HOME": str(temp_root / "xdg-config"),
                "XDG_DATA_HOME": str(temp_root / "xdg-data"),
                "MINI_SWE_AGENT_CLI_SECRET": SECRET_MARKER,
            }
        )
        completed = subprocess.run(
            [cli_path, "--help"],
            cwd=temp_root,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=20,
        )

    help_text = strip_ansi(completed.stdout + completed.stderr)
    help_summary = summarize_help(help_text)
    default_config = read_default_config()
    expected_options_present = all(help_summary["expected_options"].values())
    core_config_present = default_config["mode_confirm_present"] and default_config["cost_limit_present"]
    secret_leaked_in_trace = SECRET_MARKER in help_text
    all_passed = completed.returncode == 0 and expected_options_present and core_config_present and not secret_leaked_in_trace

    payload = {
        "status": "completed" if all_passed else "failed",
        "experiment": "real_mini_swe_agent_cli_validation",
        "package": "mini-swe-agent",
        "cli": "mini-swe-agent",
        "cli_version": importlib.metadata.version("mini-swe-agent"),
        "help_returncode": completed.returncode,
        "help_validated": completed.returncode == 0,
        "expected_options_present": expected_options_present,
        "expected_terms_present": all(help_summary["expected_terms"].values()),
        "default_config_validated": core_config_present,
        "default_config": default_config,
        "help_summary": help_summary,
        "real_model_validated": False,
        "coding_agent_validated": False,
        "toy_repo_validated": False,
        "secret_leaked_in_trace": secret_leaked_in_trace,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "notes": [
            "This validates package import, CLI help, and packaged default config surface only.",
            "It does not run mini-SWE-agent on a repo issue, call a model, validate sandbox isolation, or measure cost/latency.",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
