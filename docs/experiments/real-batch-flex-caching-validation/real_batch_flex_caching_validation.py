#!/usr/bin/env python3
"""Batch / Flex / Prompt Caching observation harness.

Without OPENAI_API_KEY this harness runs deterministic local fixtures for cache
usage fields, Flex fallback recording, and Batch JSONL metadata instead of
claiming real API behavior. With a key, it can run small Responses API
observations for Prompt Caching and Flex processing, and it prepares Batch JSONL
metadata. Actual Batch submission is opt-in because it creates asynchronous
server-side work.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RESPONSES_URL = os.environ.get("OPENAI_RESPONSES_URL", "https://api.openai.com/v1/responses")
FILES_URL = os.environ.get("OPENAI_FILES_URL", "https://api.openai.com/v1/files")
BATCHES_URL = os.environ.get("OPENAI_BATCHES_URL", "https://api.openai.com/v1/batches")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
RUN_CACHE = os.environ.get("OPENAI_RUN_PROMPT_CACHING", "1") == "1"
RUN_FLEX = os.environ.get("OPENAI_RUN_FLEX", "1") == "1"
SUBMIT_BATCH = os.environ.get("OPENAI_SUBMIT_BATCH", "0") == "1"
MAX_OUTPUT_TOKENS = max(16, min(120, int(os.environ.get("OPENAI_BATCH_FLEX_MAX_OUTPUT_TOKENS", "40"))))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class HttpResult:
    status_code: int
    headers: dict[str, str | None]
    body: dict[str, Any]
    latency_ms: int


def auth_headers(api_key: str, extra: dict[str, str] | None = None) -> dict[str, str]:
    headers = {"Authorization": f"Bearer {api_key}"}
    if extra:
        headers.update(extra)
    return headers


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


def post_json(url: str, api_key: str, payload: dict[str, Any]) -> HttpResult:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=auth_headers(api_key, {"Content-Type": "application/json"}),
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=90) as response:
        latency_ms = int((time.perf_counter() - started) * 1000)
        body = json.loads(response.read().decode("utf-8"))
        return HttpResult(response.status, rate_limit_headers(response.headers), body, latency_ms)


def prompt_caching_payload(run_index: int) -> dict[str, Any]:
    static_policy = "\n".join(
        [
            "You are validating prompt caching observability for an AI agent handbook.",
            "Static instruction block: log input tokens, output tokens, cached tokens, cache write tokens, latency, and model.",
            "Static instruction block: do not treat cache hits as quality improvements.",
            "Static instruction block: cite no external sources in this short synthetic answer.",
        ]
        * 40
    )
    return {
        "model": MODEL,
        "store": False,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "input": [
            {"role": "developer", "content": static_policy},
            {"role": "user", "content": f"Run {run_index}: name one cache observation field."},
        ],
    }


def flex_payload() -> dict[str, Any]:
    return {
        "model": MODEL,
        "store": False,
        "service_tier": "flex",
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "input": "In one sentence, name one fallback field to log for a low-priority flex request.",
    }


def usage_summary(body: dict[str, Any]) -> dict[str, int | None]:
    usage = body.get("usage")
    usage = usage if isinstance(usage, dict) else {}
    input_details = usage.get("input_tokens_details")
    input_details = input_details if isinstance(input_details, dict) else {}
    return {
        "input_tokens": usage.get("input_tokens") if isinstance(usage.get("input_tokens"), int) else None,
        "output_tokens": usage.get("output_tokens") if isinstance(usage.get("output_tokens"), int) else None,
        "total_tokens": usage.get("total_tokens") if isinstance(usage.get("total_tokens"), int) else None,
        "cached_tokens": input_details.get("cached_tokens") if isinstance(input_details.get("cached_tokens"), int) else None,
        "cache_write_tokens": input_details.get("cache_write_tokens")
        if isinstance(input_details.get("cache_write_tokens"), int)
        else None,
    }


def observe_prompt_caching(api_key: str) -> dict[str, Any]:
    if not RUN_CACHE:
        return {"status": "skipped", "reason": "OPENAI_RUN_PROMPT_CACHING is not 1"}
    observations = []
    for index in (1, 2):
        result = post_json(RESPONSES_URL, api_key, prompt_caching_payload(index))
        observations.append(
            {
                "run_index": index,
                "status_code": result.status_code,
                "latency_ms": result.latency_ms,
                "response_id": result.body.get("id"),
                "usage": usage_summary(result.body),
                "rate_limit_headers": result.headers,
            }
        )
    return {
        "status": "completed",
        "observation_count": len(observations),
        "observations": observations,
        "cache_fields_seen": any(
            item["usage"].get("cached_tokens") is not None or item["usage"].get("cache_write_tokens") is not None
            for item in observations
        ),
    }


def observe_flex(api_key: str) -> dict[str, Any]:
    if not RUN_FLEX:
        return {"status": "skipped", "reason": "OPENAI_RUN_FLEX is not 1"}
    try:
        result = post_json(RESPONSES_URL, api_key, flex_payload())
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        return {
            "status": "api_error_observed",
            "code": error.code,
            "body_preview": body[:500],
            "expected_handling": "record_timeout_or_resource_unavailable_and_fallback",
        }
    return {
        "status": "completed",
        "status_code": result.status_code,
        "latency_ms": result.latency_ms,
        "response_id": result.body.get("id"),
        "usage": usage_summary(result.body),
        "rate_limit_headers": result.headers,
        "fallback_action": "not_needed_for_successful_response",
    }


def batch_jsonl_lines() -> list[dict[str, Any]]:
    return [
        {
            "custom_id": "agent-handbook-batch-001",
            "method": "POST",
            "url": "/v1/responses",
            "body": {
                "model": MODEL,
                "store": False,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
                "input": "Name one field a Batch API result should map back with custom_id.",
            },
        },
        {
            "custom_id": "agent-handbook-batch-002",
            "method": "POST",
            "url": "/v1/responses",
            "body": {
                "model": MODEL,
                "store": False,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
                "input": "Name one expired-or-failed batch status field to log.",
            },
        },
    ]


def prepare_batch_file() -> dict[str, Any]:
    lines = batch_jsonl_lines()
    payload = "\n".join(json.dumps(item, ensure_ascii=False) for item in lines) + "\n"
    return {
        "status": "prepared",
        "request_count": len(lines),
        "custom_ids": [item["custom_id"] for item in lines],
        "jsonl_bytes": len(payload.encode("utf-8")),
        "endpoint": "/v1/responses",
        "completion_window": "24h",
        "submit_batch": SUBMIT_BATCH,
        "required_result_fields": ["id", "status", "output_file_id", "error_file_id", "request_counts", "custom_id"],
    }


def control_prompt_caching() -> dict[str, Any]:
    observations = [
        {
            "run_index": 1,
            "status_code": 200,
            "latency_ms": 620,
            "usage": {
                "input_tokens": 1800,
                "output_tokens": 28,
                "total_tokens": 1828,
                "cached_tokens": 0,
                "cache_write_tokens": 1400,
            },
            "rate_limit_headers": {
                "x-ratelimit-remaining-requests": "499",
                "x-ratelimit-remaining-tokens": "198200",
            },
        },
        {
            "run_index": 2,
            "status_code": 200,
            "latency_ms": 410,
            "usage": {
                "input_tokens": 1750,
                "output_tokens": 26,
                "total_tokens": 1776,
                "cached_tokens": 1400,
                "cache_write_tokens": 0,
            },
            "rate_limit_headers": {
                "x-ratelimit-remaining-requests": "498",
                "x-ratelimit-remaining-tokens": "196450",
            },
        },
    ]
    cached_tokens = sum(item["usage"]["cached_tokens"] for item in observations)
    cache_write_tokens = sum(item["usage"]["cache_write_tokens"] for item in observations)
    return {
        "status": "completed",
        "control": "deterministic_cache_usage_fixtures",
        "observation_count": len(observations),
        "observations": observations,
        "cache_fields_seen": cached_tokens > 0 and cache_write_tokens > 0,
        "cached_tokens": cached_tokens,
        "cache_write_tokens": cache_write_tokens,
    }


def control_flex() -> dict[str, Any]:
    return {
        "status": "completed",
        "control": "deterministic_flex_fallback_fixture",
        "simulated_api_error": {
            "code": 429,
            "type": "resource_unavailable",
            "service_tier": "flex",
        },
        "fallback_action": "retry_standard_tier_or_queue_batch",
        "fallback_recorded": True,
    }


def run_batch_flex_cache_control() -> dict[str, Any]:
    prompt_caching = control_prompt_caching()
    flex_processing = control_flex()
    batch_api = prepare_batch_file() | {
        "status": "prepared_not_submitted",
        "control": "deterministic_batch_jsonl_metadata",
        "reason": "OPENAI_API_KEY is not set; OPENAI_SUBMIT_BATCH is not used in no-key control",
    }
    custom_ids = batch_api["custom_ids"]
    required_result_fields = set(batch_api["required_result_fields"])
    expected_result_fields = {"id", "status", "output_file_id", "error_file_id", "request_counts", "custom_id"}
    required_batch_fields_present = expected_result_fields.issubset(required_result_fields)
    all_passed = (
        prompt_caching["cache_fields_seen"]
        and flex_processing["fallback_recorded"]
        and batch_api["request_count"] == 2
        and len(custom_ids) == len(set(custom_ids))
        and batch_api["endpoint"] == "/v1/responses"
        and required_batch_fields_present
    )
    return {
        "status": "completed",
        "api_status": "skipped_without_openai_api_key",
        "reason": "OPENAI_API_KEY is not set",
        "model": MODEL,
        "batch_flex_cache_control": "deterministic_cache_flex_batch_fixtures",
        "batch_flex_cache_control_passed": all_passed,
        "real_api_validated": False,
        "prompt_cache_fields_seen": prompt_caching["cache_fields_seen"],
        "cached_tokens": prompt_caching["cached_tokens"],
        "cache_write_tokens": prompt_caching["cache_write_tokens"],
        "flex_fallback_recorded": flex_processing["fallback_recorded"],
        "batch_jsonl_prepared": batch_api["status"] == "prepared_not_submitted",
        "batch_request_count": batch_api["request_count"],
        "batch_custom_id_count": len(custom_ids),
        "required_batch_fields_present": required_batch_fields_present,
        "all_passed": all_passed,
        "prompt_caching": prompt_caching,
        "flex_processing": flex_processing,
        "batch_api": batch_api,
        "limitations": [
            "Deterministic fixtures only validate local cache usage field aggregation, Flex fallback recording, and Batch JSONL metadata checks.",
            "They do not validate real Prompt Caching hits, real Flex availability or latency, real Batch submission/completion, cost savings, quality, throughput, or production reliability.",
        ],
    }


def upload_file(api_key: str, file_path: Path) -> str:
    boundary = "----agent-handbook-boundary"
    file_bytes = file_path.read_bytes()
    body = b"".join(
        [
            f"--{boundary}\r\n".encode(),
            b'Content-Disposition: form-data; name="purpose"\r\n\r\n',
            b"batch\r\n",
            f"--{boundary}\r\n".encode(),
            b'Content-Disposition: form-data; name="file"; filename="batch.jsonl"\r\n',
            b"Content-Type: application/jsonl\r\n\r\n",
            file_bytes,
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    request = urllib.request.Request(
        FILES_URL,
        data=body,
        headers=auth_headers(api_key, {"Content-Type": f"multipart/form-data; boundary={boundary}"}),
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))["id"]


def submit_batch(api_key: str) -> dict[str, Any]:
    prepared = prepare_batch_file()
    if not SUBMIT_BATCH:
        return {**prepared, "status": "prepared_not_submitted", "reason": "OPENAI_SUBMIT_BATCH is not 1"}
    lines = batch_jsonl_lines()
    with tempfile.TemporaryDirectory(prefix="openai-batch-") as tmp:
        path = Path(tmp) / "batch.jsonl"
        path.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in lines) + "\n", encoding="utf-8")
        input_file_id = upload_file(api_key, path)
    payload = {"input_file_id": input_file_id, "endpoint": "/v1/responses", "completion_window": "24h"}
    result = post_json(BATCHES_URL, api_key, payload)
    return {
        **prepared,
        "status": "submitted",
        "status_code": result.status_code,
        "batch_id": result.body.get("id"),
        "batch_status": result.body.get("status"),
        "input_file_id": input_file_id,
        "request_counts": result.body.get("request_counts"),
    }


def run(api_key: str) -> dict[str, Any]:
    started = time.perf_counter()
    return {
        "status": "completed",
        "timestamp": utc_now(),
        "model": MODEL,
        "responses_url": RESPONSES_URL,
        "elapsed_seconds": None,
        "prompt_caching": observe_prompt_caching(api_key),
        "flex_processing": observe_flex(api_key),
        "batch_api": submit_batch(api_key),
        "limitations": [
            "Prompt Caching observations only reflect two small requests with one static prefix.",
            "Flex observations only reflect the selected model, account, request, network path, and time window.",
            "Batch submission is opt-in; prepared JSONL metadata is not evidence of Batch runtime behavior.",
            "This harness does not prove lower cost, lower latency, better throughput, quality preservation, or production reliability.",
        ],
    } | {"elapsed_seconds": round(time.perf_counter() - started, 3)}


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(json.dumps(run_batch_flex_cache_control(), ensure_ascii=False, indent=2))
        return 0

    try:
        result = run(api_key)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print(json.dumps({"status": "api_error", "code": error.code, "body_preview": body[:500]}, indent=2))
        return 1
    except Exception as error:  # noqa: BLE001 - this is a CLI experiment harness.
        print(json.dumps({"status": "error", "error": str(error)}, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
