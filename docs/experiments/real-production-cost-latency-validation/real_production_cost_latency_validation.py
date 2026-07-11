#!/usr/bin/env python3
"""Responses API cost, latency, and rate-limit observation harness.

This harness intentionally records production fields without claiming that any
optimization is effective. Without OPENAI_API_KEY it runs deterministic local
accounting fixtures instead of claiming real API behavior.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean
from typing import Any


API_URL = os.environ.get("OPENAI_RESPONSES_URL", "https://api.openai.com/v1/responses")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
RUN_COUNT = max(1, min(5, int(os.environ.get("OPENAI_COST_LATENCY_RUNS", "3"))))
MAX_OUTPUT_TOKENS = max(16, min(300, int(os.environ.get("OPENAI_MAX_OUTPUT_TOKENS", "80"))))
BUDGET_THRESHOLD = float(os.environ.get("OPENAI_COST_BUDGET_THRESHOLD", "0.05"))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Observation:
    request_id: str | None
    latency_ms: int
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    cached_tokens: int | None
    cache_write_tokens: int | None
    rate_limit_headers: dict[str, str | None]
    timestamp: str = field(default_factory=utc_now)


def percentile_95(values: list[int]) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(round(0.95 * (len(ordered) - 1))))
    return ordered[index]


def price_per_token(env_name: str) -> float | None:
    raw = os.environ.get(env_name)
    if raw is None or raw.strip() == "":
        return None
    return float(raw) / 1_000_000


def estimate_cost(input_tokens: int, output_tokens: int) -> tuple[float | None, str]:
    input_price = price_per_token("OPENAI_INPUT_PRICE_PER_MILLION")
    output_price = price_per_token("OPENAI_OUTPUT_PRICE_PER_MILLION")
    if input_price is None or output_price is None:
        return None, "price_env_not_configured"
    return round((input_tokens * input_price) + (output_tokens * output_price), 8), "estimated_from_env_prices"


def estimate_cost_from_prices(
    input_tokens: int,
    output_tokens: int,
    input_price_per_million: float,
    output_price_per_million: float,
) -> float:
    input_price = input_price_per_million / 1_000_000
    output_price = output_price_per_million / 1_000_000
    return round((input_tokens * input_price) + (output_tokens * output_price), 8)


def rate_limit_headers(headers: Any) -> dict[str, str | None]:
    keys = [
        "x-ratelimit-limit-requests",
        "x-ratelimit-remaining-requests",
        "x-ratelimit-reset-requests",
        "x-ratelimit-limit-tokens",
        "x-ratelimit-remaining-tokens",
        "x-ratelimit-reset-tokens",
    ]
    return {key: headers.get(key) for key in keys}


def post_response(api_key: str, index: int) -> tuple[dict[str, Any], dict[str, str | None], int]:
    payload = {
        "model": MODEL,
        "store": False,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "input": [
            {
                "role": "developer",
                "content": "Answer briefly with one practical sentence. Do not include markdown.",
            },
            {
                "role": "user",
                "content": f"Production observation request {index}: name one field an AI agent should log before launch.",
            },
        ],
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=60) as response:
        latency_ms = int((time.perf_counter() - started) * 1000)
        body = json.loads(response.read().decode("utf-8"))
        headers = rate_limit_headers(response.headers)
    return body, headers, latency_ms


def usage_value(usage: dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        value = usage.get(key)
        if isinstance(value, int):
            return value
    return None


def cache_values(usage: dict[str, Any]) -> tuple[int | None, int | None]:
    input_details = usage.get("input_tokens_details", {})
    cached_tokens = input_details.get("cached_tokens") if isinstance(input_details, dict) else None
    cache_write_tokens = input_details.get("cache_write_tokens") if isinstance(input_details, dict) else None
    return (
        cached_tokens if isinstance(cached_tokens, int) else None,
        cache_write_tokens if isinstance(cache_write_tokens, int) else None,
    )


def observe_response(body: dict[str, Any], headers: dict[str, str | None], latency_ms: int) -> Observation:
    usage = body.get("usage", {})
    usage = usage if isinstance(usage, dict) else {}
    input_tokens = usage_value(usage, "input_tokens", "prompt_tokens")
    output_tokens = usage_value(usage, "output_tokens", "completion_tokens")
    total_tokens = usage_value(usage, "total_tokens")
    cached_tokens, cache_write_tokens = cache_values(usage)
    return Observation(
        request_id=body.get("id") if isinstance(body.get("id"), str) else None,
        latency_ms=latency_ms,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        cached_tokens=cached_tokens,
        cache_write_tokens=cache_write_tokens,
        rate_limit_headers=headers,
    )


def deterministic_control_inputs() -> list[tuple[dict[str, Any], dict[str, str | None], int]]:
    return [
        (
            {
                "id": "resp_control_1",
                "usage": {
                    "input_tokens": 1200,
                    "output_tokens": 180,
                    "total_tokens": 1380,
                    "input_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 1200},
                },
            },
            {
                "x-ratelimit-limit-requests": "500",
                "x-ratelimit-remaining-requests": "499",
                "x-ratelimit-reset-requests": "1s",
                "x-ratelimit-limit-tokens": "30000",
                "x-ratelimit-remaining-tokens": "28620",
                "x-ratelimit-reset-tokens": "1s",
            },
            120,
        ),
        (
            {
                "id": "resp_control_2",
                "usage": {
                    "input_tokens": 1200,
                    "output_tokens": 160,
                    "total_tokens": 1360,
                    "input_tokens_details": {"cached_tokens": 900, "cache_write_tokens": 0},
                },
            },
            {
                "x-ratelimit-limit-requests": "500",
                "x-ratelimit-remaining-requests": "498",
                "x-ratelimit-reset-requests": "1s",
                "x-ratelimit-limit-tokens": "30000",
                "x-ratelimit-remaining-tokens": "27260",
                "x-ratelimit-reset-tokens": "1s",
            },
            250,
        ),
        (
            {
                "id": "resp_control_3",
                "usage": {
                    "input_tokens": 1300,
                    "output_tokens": 260,
                    "total_tokens": 1560,
                    "input_tokens_details": {"cached_tokens": 900, "cache_write_tokens": 0},
                },
            },
            {
                "x-ratelimit-limit-requests": "500",
                "x-ratelimit-remaining-requests": "497",
                "x-ratelimit-reset-requests": "1s",
                "x-ratelimit-limit-tokens": "30000",
                "x-ratelimit-remaining-tokens": "25700",
                "x-ratelimit-reset-tokens": "1s",
            },
            900,
        ),
    ]


def run_accounting_control() -> dict[str, Any]:
    observations = [observe_response(body, headers, latency_ms) for body, headers, latency_ms in deterministic_control_inputs()]
    latencies = [item.latency_ms for item in observations]
    input_tokens = sum(item.input_tokens or 0 for item in observations)
    output_tokens = sum(item.output_tokens or 0 for item in observations)
    total_tokens = sum(item.total_tokens or 0 for item in observations)
    cached_tokens = sum(item.cached_tokens or 0 for item in observations)
    cache_write_tokens = sum(item.cache_write_tokens or 0 for item in observations)
    cost_estimate = estimate_cost_from_prices(
        input_tokens,
        output_tokens,
        input_price_per_million=2.0,
        output_price_per_million=8.0,
    )
    budget_threshold = 0.005
    headers_seen = any(value is not None for item in observations for value in item.rate_limit_headers.values())
    average_latency_ms = int(mean(latencies))
    p95_latency_ms = percentile_95(latencies)
    checks = {
        "usage_tokens_recorded": input_tokens == 3700 and output_tokens == 600 and total_tokens == 4300,
        "cache_fields_recorded": cached_tokens == 1800 and cache_write_tokens == 1200,
        "rate_limit_headers_seen": headers_seen,
        "latency_distribution_recorded": average_latency_ms == 423 and p95_latency_ms == 900,
        "budget_action_degrades": cost_estimate > budget_threshold,
    }
    return {
        "status": "completed",
        "api_status": "skipped_without_openai_api_key",
        "reason": "OPENAI_API_KEY is not set",
        "model": MODEL,
        "accounting_control": "deterministic_usage_latency_fixtures",
        "real_api_validated": False,
        "request_count": len(observations),
        "average_latency_ms": average_latency_ms,
        "p95_latency_ms": p95_latency_ms,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cached_tokens": cached_tokens,
        "cache_write_tokens": cache_write_tokens,
        "cost_estimate": cost_estimate,
        "cost_estimate_status": "deterministic_fixture_prices",
        "budget_threshold": budget_threshold,
        "budget_action": "degrade" if cost_estimate > budget_threshold else "continue",
        "rate_limit_headers_seen": headers_seen,
        "accounting_control_passed": all(checks.values()),
        "all_passed": all(checks.values()),
        "checks": checks,
        "observations": [item.__dict__ for item in observations],
        "limitations": [
            "Deterministic fixtures only validate local field extraction and aggregation logic.",
            "They do not validate real API usage, rate-limit behavior, latency, cost, retry, quality, or production reliability.",
        ],
    }


def run(api_key: str) -> dict[str, Any]:
    started = time.perf_counter()
    observations: list[Observation] = []
    for index in range(1, RUN_COUNT + 1):
        body, headers, latency_ms = post_response(api_key, index)
        observations.append(observe_response(body, headers, latency_ms))

    latencies = [item.latency_ms for item in observations]
    input_tokens = sum(item.input_tokens or 0 for item in observations)
    output_tokens = sum(item.output_tokens or 0 for item in observations)
    cost_estimate, cost_estimate_status = estimate_cost(input_tokens, output_tokens)
    headers_seen = any(value is not None for item in observations for value in item.rate_limit_headers.values())
    budget_action = "unknown_without_prices" if cost_estimate is None else "degrade" if cost_estimate > BUDGET_THRESHOLD else "continue"

    return {
        "status": "completed",
        "api_status": "completed",
        "model": MODEL,
        "api_url": API_URL,
        "real_api_validated": True,
        "request_count": RUN_COUNT,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "average_latency_ms": int(mean(latencies)),
        "p95_latency_ms": percentile_95(latencies),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_estimate": cost_estimate,
        "cost_estimate_status": cost_estimate_status,
        "budget_threshold": BUDGET_THRESHOLD,
        "budget_action": budget_action,
        "rate_limit_headers_seen": headers_seen,
        "observations": [item.__dict__ for item in observations],
        "limitations": [
            "Single harness run only reflects the selected model, prompts, account tier, network path, and time window.",
            "Cost estimate is only produced when OPENAI_INPUT_PRICE_PER_MILLION and OPENAI_OUTPUT_PRICE_PER_MILLION are configured.",
            "This harness does not test Batch, Flex, Prompt Caching benefit, quality, concurrency, or production reliability.",
        ],
    }


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(json.dumps(run_accounting_control(), ensure_ascii=False, indent=2))
        return 0

    try:
        result = run(api_key)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print(json.dumps({"status": "api_error", "code": error.code, "body": body}, indent=2))
        return 1
    except Exception as error:  # noqa: BLE001 - this is a CLI experiment harness.
        print(json.dumps({"status": "error", "error": str(error)}, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
