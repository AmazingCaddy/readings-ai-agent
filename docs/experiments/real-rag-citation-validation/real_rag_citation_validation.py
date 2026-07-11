#!/usr/bin/env python3
"""Real LLM RAG citation synthesis harness with local keyword retrieval."""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


API_URL = os.environ.get("OPENAI_RESPONSES_URL", "https://api.openai.com/v1/responses")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "by",
    "can",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "or",
    "the",
    "to",
    "what",
    "when",
    "why",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def terms(text: str) -> set[str]:
    return {term for term in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", text.lower()) if term not in STOPWORDS}


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_id: str
    title: str
    url: str
    text: str
    keywords: set[str]


@dataclass(frozen=True)
class EvalCase:
    question: str
    expected_grounded: bool
    required_terms: set[str]


@dataclass
class CaseResult:
    question: str
    status: str
    schema_valid: bool
    citation_valid: bool
    semantic_valid: bool
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now)


CHUNKS = [
    Chunk(
        chunk_id="rag-paper#1",
        source_id="rag-paper",
        title="RAG paper abstract note",
        url="docs/sources/source-cards/2020-rag-paper.md",
        text=(
            "Retrieval-Augmented Generation combines parametric memory with an explicit "
            "non-parametric memory such as a dense vector index. The paper highlights "
            "knowledge-intensive tasks, provenance, and updating world knowledge."
        ),
        keywords=set(),
    ),
    Chunk(
        chunk_id="llamaindex-rag#1",
        source_id="llamaindex-rag",
        title="LlamaIndex RAG overview note",
        url="docs/sources/source-cards/2026-llamaindex-docs.md",
        text=(
            "Engineering RAG is commonly organized into loading, indexing, storing, "
            "querying, and evaluation. Documents are split into nodes or chunks with "
            "metadata so retrievers can return source context."
        ),
        keywords=set(),
    ),
    Chunk(
        chunk_id="langgraph-memory#1",
        source_id="langgraph-memory",
        title="LangGraph memory note",
        url="docs/sources/source-cards/2026-langgraph-memory-docs.md",
        text=(
            "Short-term memory is thread scoped state for one conversation. Long-term "
            "memory stores cross-session user-specific or application-level data and "
            "requires governance for writing, updating, and deletion."
        ),
        keywords=set(),
    ),
]
CHUNKS = [
    Chunk(chunk.chunk_id, chunk.source_id, chunk.title, chunk.url, chunk.text, terms(chunk.text)) for chunk in CHUNKS
]

CASES = [
    EvalCase(
        question="Which stages make up the engineering RAG pipeline?",
        expected_grounded=True,
        required_terms={"loading", "indexing", "storing", "querying", "evaluation"},
    ),
    EvalCase(
        question="What does RAG use to update world knowledge and show provenance?",
        expected_grounded=True,
        required_terms={"provenance", "world", "knowledge"},
    ),
    EvalCase(
        question="Which database vendor has the best managed vector index pricing in 2026?",
        expected_grounded=False,
        required_terms=set(),
    ),
]


def retrieve(question: str, top_k: int = 2) -> list[dict[str, Any]]:
    query_terms = terms(question)
    scored: list[dict[str, Any]] = []
    for chunk in CHUNKS:
        overlap = sorted(query_terms & chunk.keywords)
        if overlap:
            scored.append({"chunk": chunk, "score": len(overlap), "matched_terms": overlap})
    scored.sort(key=lambda item: (-item["score"], item["chunk"].chunk_id))
    return scored[:top_k]


def post_response(payload: dict[str, Any], api_key: str) -> dict[str, Any]:
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def output_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "grounded": {"type": "boolean"},
            "citations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "chunk_id": {"type": "string"},
                        "quote": {"type": "string"},
                    },
                    "required": ["chunk_id", "quote"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["answer", "grounded", "citations"],
        "additionalProperties": False,
    }


def response_text(response: dict[str, Any]) -> str:
    texts: list[str] = []
    for item in response.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if "text" in content:
                    texts.append(str(content["text"]))
    if "output_text" in response:
        texts.append(str(response["output_text"]))
    return "\n".join(texts).strip()


def payload_for(case: EvalCase, retrieved: list[dict[str, Any]]) -> dict[str, Any]:
    context = [
        {
            "chunk_id": item["chunk"].chunk_id,
            "source_id": item["chunk"].source_id,
            "title": item["chunk"].title,
            "url": item["chunk"].url,
            "text": item["chunk"].text,
        }
        for item in retrieved
    ]
    return {
        "model": MODEL,
        "input": [
            {
                "role": "developer",
                "content": (
                    "Answer only from the provided chunks. If the chunks do not support the answer, "
                    "set grounded=false, use an empty citations array, and say the evidence is insufficient. "
                    "Every factual claim in a grounded answer needs a chunk citation."
                ),
            },
            {
                "role": "user",
                "content": json.dumps({"question": case.question, "chunks": context}, ensure_ascii=False),
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "rag_answer",
                "schema": output_schema(),
                "strict": True,
            }
        },
    }


def parse_json(text: str) -> dict[str, Any]:
    return json.loads(text)


def validate_schema(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data.get("answer"), str):
        errors.append("answer must be string")
    if not isinstance(data.get("grounded"), bool):
        errors.append("grounded must be boolean")
    citations = data.get("citations")
    if not isinstance(citations, list):
        errors.append("citations must be array")
    else:
        for citation in citations:
            if not isinstance(citation, dict):
                errors.append("citation must be object")
                continue
            if not isinstance(citation.get("chunk_id"), str):
                errors.append("citation.chunk_id must be string")
            if not isinstance(citation.get("quote"), str):
                errors.append("citation.quote must be string")
    return errors


def validate_citations(data: dict[str, Any], retrieved_ids: set[str]) -> list[str]:
    errors: list[str] = []
    citations = data.get("citations", [])
    cited_ids = {citation.get("chunk_id") for citation in citations if isinstance(citation, dict)}
    unknown = sorted(cited_id for cited_id in cited_ids if cited_id not in retrieved_ids)
    if unknown:
        errors.append(f"unknown citations: {unknown}")
    if data.get("grounded") is True and not citations:
        errors.append("grounded answer must include citations")
    if data.get("grounded") is False and citations:
        errors.append("ungrounded answer should not include citations")
    return errors


def validate_semantics(case: EvalCase, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("grounded") != case.expected_grounded:
        errors.append(f"grounded should be {case.expected_grounded}")
    answer_terms = terms(str(data.get("answer", "")))
    missing = sorted(case.required_terms - answer_terms)
    if missing:
        errors.append(f"missing required answer terms: {missing}")
    return errors


def run_case(case: EvalCase, api_key: str) -> CaseResult:
    retrieved = retrieve(case.question)
    response = post_response(payload_for(case, retrieved), api_key)
    text = response_text(response)
    retrieved_ids = {item["chunk"].chunk_id for item in retrieved}
    details: dict[str, Any] = {
        "response_id": response.get("id"),
        "retrieved": [
            {
                "chunk_id": item["chunk"].chunk_id,
                "score": item["score"],
                "matched_terms": item["matched_terms"],
            }
            for item in retrieved
        ],
        "text": text,
    }
    try:
        data = parse_json(text)
    except Exception as error:  # noqa: BLE001 - experiment reports parse failures.
        details["parse_error"] = str(error)
        return CaseResult(case.question, "parse_failed", False, False, False, details)

    schema_errors = validate_schema(data)
    citation_errors = validate_citations(data, retrieved_ids) if not schema_errors else ["schema invalid"]
    semantic_errors = validate_semantics(case, data) if not schema_errors else ["schema invalid"]
    details["parsed"] = data
    details["schema_errors"] = schema_errors
    details["citation_errors"] = citation_errors
    details["semantic_errors"] = semantic_errors
    status = "ok" if not schema_errors and not citation_errors and not semantic_errors else "invalid"
    return CaseResult(case.question, status, not schema_errors, not citation_errors, not semantic_errors, details)


def run(api_key: str) -> dict[str, Any]:
    started = time.perf_counter()
    results = [run_case(case, api_key).__dict__ for case in CASES]
    return {
        "status": "completed",
        "model": MODEL,
        "api_url": API_URL,
        "retrieval": "local_keyword_overlap",
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "results": results,
    }


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print(
            json.dumps(
                {
                    "status": "skipped",
                    "reason": "OPENAI_API_KEY is not set",
                    "model": MODEL,
                    "retrieval": "local_keyword_overlap",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
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
