#!/usr/bin/env python3
"""Run mini-SWE-agent runtime surface on a toy repo with a fake model.

This harness uses mini-SWE-agent's packaged deterministic test model and local
environment to execute a fixed command sequence on a temporary toy repository.
It validates agent/environment/trajectory surfaces only. It does not call a real
model, prompt a human for confirmation, run SWE-bench, or prove issue-fixing
quality.
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any


SECRET_MARKER = "secret=mini-swe-runtime-demo-token"


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=30,
    )


def create_toy_repo(root: Path) -> None:
    (root / "tests").mkdir(parents=True)
    (root / "ISSUE.md").write_text(
        """# Issue\n\nDiscounts should apply only to positive totals.\n\nExpected behavior:\n- `apply_discount(100, 0.10)` returns `90.0`.\n- negative totals raise `ValueError`.\n- rates outside `[0, 1]` raise `ValueError`.\n""",
        encoding="utf-8",
    )
    (root / "discount.py").write_text(
        """def apply_discount(total, rate):\n    return total - (total * rate)\n""",
        encoding="utf-8",
    )
    (root / "tests/test_discount.py").write_text(
        """import pytest\n\nfrom discount import apply_discount\n\n\ndef test_discount_happy_path():\n    assert apply_discount(100, 0.10) == 90.0\n\n\ndef test_zero_rate():\n    assert apply_discount(25, 0) == 25\n\n\ndef test_full_discount():\n    assert apply_discount(25, 1) == 0\n\n\ndef test_negative_total_rejected():\n    with pytest.raises(ValueError):\n        apply_discount(-1, 0.10)\n\n\ndef test_invalid_rate_rejected():\n    with pytest.raises(ValueError):\n        apply_discount(100, 1.50)\n""",
        encoding="utf-8",
    )
    run_command(["git", "init", "-q"], root)
    run_command(["git", "add", "ISSUE.md", "discount.py", "tests/test_discount.py"], root)
    run_command(["git", "commit", "-q", "-m", "initial toy repo"], root)


def build_patch_command(repo: Path) -> str:
    fixed_source = """from pathlib import Path\nPath('discount.py').write_text('''def apply_discount(total, rate):\n    if total < 0:\n        raise ValueError("total must be non-negative")\n    if rate < 0 or rate > 1:\n        raise ValueError("rate must be between 0 and 1")\n    return total - (total * rate)\n''', encoding='utf-8')\n"""
    return f"cd {repo} && python - <<'PY'\n{fixed_source}PY"


def load_trajectory(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if importlib.util.find_spec("minisweagent") is None:
        print(
            json.dumps(
                {
                    "status": "skipped",
                    "reason": "mini_swe_agent_not_installed",
                    "install_note": "Run with `uv run --with mini-swe-agent --with pytest python docs/experiments/real-mini-swe-agent-runtime-validation/real_mini_swe_agent_runtime_validation.py`.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if importlib.util.find_spec("pytest") is None:
        print(json.dumps({"status": "skipped", "reason": "pytest_not_installed"}, ensure_ascii=False, indent=2))
        return 0

    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="mini-swe-agent-runtime-") as temp_dir:
        root = Path(temp_dir)
        os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = str(root / "mini-swe-agent-config")
        os.environ["MSWEA_SILENT_STARTUP"] = "1"

        from minisweagent.agents.interactive import InteractiveAgent
        from minisweagent.environments.local import LocalEnvironment
        from minisweagent.models.test_models import DeterministicModel, make_output

        repo = root / "toy-repo"
        repo.mkdir()
        create_toy_repo(repo)

        initial_tests = run_command([sys.executable, "-m", "pytest", "-q"], repo)
        trajectory_path = root / "trajectory.json"
        commands = [
            f"cd {repo} && pwd && ls && sed -n '1,120p' ISSUE.md && sed -n '1,120p' discount.py",
            f"cd {repo} && {sys.executable} -m pytest -q",
            build_patch_command(repo),
            f"cd {repo} && {sys.executable} -m pytest -q",
            "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT",
        ]
        outputs = [
            make_output("Inspect issue and implementation.", [{"command": commands[0]}], cost=0.1),
            make_output("Reproduce failing tests.", [{"command": commands[1]}], cost=0.1),
            make_output("Patch implementation only.", [{"command": commands[2]}], cost=0.1),
            make_output("Verify tests.", [{"command": commands[3]}], cost=0.1),
            make_output("Submit final output.", [{"command": commands[4]}], cost=0.1),
        ]
        model = DeterministicModel(outputs=outputs, cost_per_call=0.1)
        env = LocalEnvironment(cwd=str(repo), env={"MINI_SWE_RUNTIME_SECRET": SECRET_MARKER}, timeout=30)
        agent = InteractiveAgent(
            model,
            env,
            system_template="You are a deterministic coding agent for a toy repo.",
            instance_template="Fix this toy issue: {{task}}",
            mode="yolo",
            confirm_exit=False,
            step_limit=8,
            cost_limit=1.0,
            output_path=trajectory_path,
        )
        console_buffer = io.StringIO()
        with redirect_stdout(console_buffer):
            result = agent.run("Implement input validation in discount.py and verify tests.")
        agent_console_output = console_buffer.getvalue()

        final_tests = run_command([sys.executable, "-m", "pytest", "-q"], repo)
        diff_name_only = run_command(["git", "diff", "--name-only"], repo).stdout.splitlines()
        diff_text = run_command(["git", "diff", "--", "discount.py"], repo).stdout
        trajectory_written = trajectory_path.exists()
        trajectory = load_trajectory(trajectory_path)
        trajectory_text = json.dumps(trajectory, ensure_ascii=False)
        command_count = sum(
            len(message.get("extra", {}).get("actions", [])) for message in trajectory.get("messages", [])
        )

    implementation_only = diff_name_only == ["discount.py"]
    initial_failed = initial_tests.returncode != 0
    final_passed = final_tests.returncode == 0
    sample_env_marker_recorded_in_trajectory = SECRET_MARKER in trajectory_text
    all_passed = (
        result.get("exit_status") == "Submitted"
        and trajectory_written
        and command_count == len(commands)
        and initial_failed
        and final_passed
        and implementation_only
        and sample_env_marker_recorded_in_trajectory
    )

    payload = {
        "status": "completed" if all_passed else "failed",
        "experiment": "real_mini_swe_agent_runtime_validation",
        "framework": "mini-swe-agent",
        "model": "minisweagent.models.test_models.DeterministicModel",
        "agent": "minisweagent.agents.interactive.InteractiveAgent",
        "environment": "minisweagent.environments.local.LocalEnvironment",
        "mode": "yolo",
        "real_model_validated": False,
        "human_confirmation_validated": False,
        "toy_repo_validated": True,
        "initial_tests_returncode": initial_tests.returncode,
        "final_tests_returncode": final_tests.returncode,
        "initial_tests_failed": initial_failed,
        "final_tests_passed": final_passed,
        "exit_status": result.get("exit_status"),
        "submission": result.get("submission"),
        "trajectory_written": trajectory_written,
        "trajectory_format": trajectory.get("trajectory_format"),
        "mini_version": trajectory.get("info", {}).get("mini_version"),
        "api_calls": trajectory.get("info", {}).get("model_stats", {}).get("api_calls"),
        "instance_cost": trajectory.get("info", {}).get("model_stats", {}).get("instance_cost"),
        "command_count": command_count,
        "agent_console_output_contains_steps": "mini-swe-agent" in agent_console_output and "step" in agent_console_output,
        "diff_name_only": diff_name_only,
        "implementation_only": implementation_only,
        "discount_diff_contains_validation": "ValueError" in diff_text and "rate must be between 0 and 1" in diff_text,
        "sample_env_marker_recorded_in_trajectory": sample_env_marker_recorded_in_trajectory,
        "trace_redaction_validated": False,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "notes": [
            "This validates mini-SWE-agent runtime, local environment execution, toy repo mutation, tests, and trajectory shape with a deterministic fake model only.",
            "The fake environment marker is intentionally recorded in the trajectory because LocalEnvironment serializes configured env values; do not put real secrets in that config.",
            "It does not validate real model planning, confirm-mode approval burden, sandbox isolation, cost accuracy, SWE-bench, or real repo issue success.",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
