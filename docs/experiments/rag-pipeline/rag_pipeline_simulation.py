#!/usr/bin/env python3
"""Minimal RAG pipeline and citation trace simulation.

This deterministic experiment uses keyword retrieval instead of embeddings. The
goal is to validate the handbook's engineering boundary: documents become
chunks with source metadata, retrieval selects evidence, answer synthesis should
cite source chunks, and unsupported questions should not be answered as facts.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


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
class Document:
    source_id: str
    title: str
    url: str
    text: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_id: str
    title: str
    url: str
    text: str
    keywords: set[str]


@dataclass
class TraceEvent:
    stage: str
    details: dict[str, Any]
    timestamp: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class RetrievalCase:
    case_id: str
    question: str
    expected_source_ids: tuple[str, ...]
    unsupported: bool = False


@dataclass(frozen=True)
class RetrievalStrategy:
    strategy_id: str
    chunk_size_words: int
    top_k: int
    allowed_source_ids: tuple[str, ...] = ()
    rerank_terms: tuple[str, ...] = ()
    expected_failure_case_ids: tuple[str, ...] = ()


DOCUMENTS = [
    Document(
        source_id="rag-paper",
        title="RAG paper abstract note",
        url="docs/sources/source-cards/2020-rag-paper.md",
        text=(
            "Retrieval-Augmented Generation combines parametric memory with an explicit "
            "non-parametric memory such as a dense vector index. The paper highlights "
            "knowledge-intensive tasks, provenance, and updating world knowledge."
        ),
    ),
    Document(
        source_id="llamaindex-rag",
        title="LlamaIndex RAG overview note",
        url="docs/sources/source-cards/2026-llamaindex-docs.md",
        text=(
            "Engineering RAG is commonly organized into loading, indexing, storing, "
            "querying, and evaluation. Documents are split into nodes or chunks with "
            "metadata so retrievers can return source context."
        ),
    ),
    Document(
        source_id="langgraph-memory",
        title="LangGraph memory note",
        url="docs/sources/source-cards/2026-langgraph-memory-docs.md",
        text=(
            "Short-term memory is thread scoped state for one conversation. Long-term "
            "memory stores cross-session user-specific or application-level data and "
            "requires governance for writing, updating, and deletion."
        ),
    ),
]


class RagPipeline:
    def __init__(self, documents: list[Document], chunk_size_words: int = 28) -> None:
        self.documents = documents
        self.chunk_size_words = chunk_size_words
        self.trace: list[TraceEvent] = []
        self.chunks = self.chunk_documents(documents)

    def record(self, stage: str, **details: Any) -> None:
        self.trace.append(TraceEvent(stage=stage, details=details))

    def chunk_documents(self, documents: list[Document]) -> list[Chunk]:
        chunks: list[Chunk] = []
        for document in documents:
            words = document.text.split()
            for index in range(0, len(words), self.chunk_size_words):
                text = " ".join(words[index : index + self.chunk_size_words])
                chunk_number = index // self.chunk_size_words + 1
                chunks.append(
                    Chunk(
                        chunk_id=f"{document.source_id}#{chunk_number}",
                        source_id=document.source_id,
                        title=document.title,
                        url=document.url,
                        text=text,
                        keywords=terms(text),
                    )
                )
        self.record("chunk", documents=len(documents), chunks=len(chunks), chunk_size_words=self.chunk_size_words)
        return chunks

    def retrieve(
        self,
        question: str,
        top_k: int = 2,
        allowed_source_ids: tuple[str, ...] = (),
        rerank_terms: tuple[str, ...] = (),
    ) -> list[dict[str, Any]]:
        query_terms = terms(question)
        scored = []
        for chunk in self.chunks:
            if allowed_source_ids and chunk.source_id not in allowed_source_ids:
                continue
            overlap = sorted(query_terms & chunk.keywords)
            score = len(overlap)
            if score:
                rerank_overlap = sorted(set(rerank_terms) & chunk.keywords)
                scored.append(
                    {
                        "chunk": chunk,
                        "score": score,
                        "matched_terms": overlap,
                        "rerank_score": len(rerank_overlap),
                        "rerank_matched_terms": rerank_overlap,
                    }
                )
        scored.sort(key=lambda item: (-item["score"], -item["rerank_score"], item["chunk"].chunk_id))
        selected = scored[:top_k]
        self.record(
            "retrieve",
            question=question,
            query_terms=sorted(query_terms),
            allowed_source_ids=list(allowed_source_ids),
            rerank_terms=list(rerank_terms),
            selected=[
                {
                    "chunk_id": item["chunk"].chunk_id,
                    "score": item["score"],
                    "matched_terms": item["matched_terms"],
                    "rerank_score": item["rerank_score"],
                    "rerank_matched_terms": item["rerank_matched_terms"],
                }
                for item in selected
            ],
        )
        return selected

    def answer(self, question: str, top_k: int = 2) -> dict[str, Any]:
        selected = self.retrieve(question, top_k=top_k)
        if not selected:
            answer = "I do not have enough retrieved evidence to answer this question."
            citations: list[dict[str, str]] = []
            self.record("synthesize", answer=answer, citations=citations, grounded=False)
            return {"question": question, "answer": answer, "citations": citations, "grounded": False}

        chunks = [item["chunk"] for item in selected]
        citations = [
            {
                "chunk_id": chunk.chunk_id,
                "source_id": chunk.source_id,
                "title": chunk.title,
                "url": chunk.url,
            }
            for chunk in chunks
        ]
        answer = self.compose_answer(question, chunks)
        self.record("synthesize", answer=answer, citations=citations, grounded=True)
        return {"question": question, "answer": answer, "citations": citations, "grounded": True}

    def compose_answer(self, question: str, chunks: list[Chunk]) -> str:
        joined = " ".join(chunk.text for chunk in chunks).lower()
        if "provenance" in terms(question) or "source" in terms(question):
            return "RAG helps with provenance by retrieving external source chunks and attaching citations to the answer."
        if "memory" in terms(question):
            return "RAG retrieves external knowledge, while long-term memory stores cross-session user or application data that needs governance."
        if "pipeline" in terms(question) or "stages" in terms(question):
            return "A minimal engineering RAG pipeline includes loading, chunking/indexing, retrieval, answer synthesis, citations, and evaluation."
        return "The retrieved chunks provide partial context, but the answer should stay conservative."

    def serialized_trace(self) -> list[dict[str, Any]]:
        return [event.__dict__ for event in self.trace]


RETRIEVAL_CASES = [
    RetrievalCase(
        case_id="multi_source_provenance",
        question="How does RAG help with provenance and source tracing?",
        expected_source_ids=("rag-paper", "llamaindex-rag"),
    ),
    RetrievalCase(
        case_id="memory_governance",
        question="How is RAG different from long-term memory governance?",
        expected_source_ids=("langgraph-memory", "llamaindex-rag"),
    ),
    RetrievalCase(
        case_id="unsupported_deployment",
        question="What is the project deployment command?",
        expected_source_ids=(),
        unsupported=True,
    ),
]


RETRIEVAL_STRATEGIES = [
    RetrievalStrategy(
        strategy_id="balanced_top2",
        chunk_size_words=28,
        top_k=2,
    ),
    RetrievalStrategy(
        strategy_id="top1_misses_multi_source",
        chunk_size_words=28,
        top_k=1,
        expected_failure_case_ids=("multi_source_provenance", "memory_governance"),
    ),
    RetrievalStrategy(
        strategy_id="wrong_metadata_filter_hides_memory",
        chunk_size_words=28,
        top_k=2,
        allowed_source_ids=("rag-paper", "llamaindex-rag"),
        expected_failure_case_ids=("memory_governance",),
    ),
    RetrievalStrategy(
        strategy_id="fine_chunks_top3_rerank_still_needs_eval",
        chunk_size_words=10,
        top_k=3,
        rerank_terms=("provenance", "metadata", "memory", "governance"),
        expected_failure_case_ids=("memory_governance",),
    ),
]


def evaluate_retrieval_strategy(case: RetrievalCase, strategy: RetrievalStrategy) -> dict[str, Any]:
    pipeline = RagPipeline(DOCUMENTS, chunk_size_words=strategy.chunk_size_words)
    selected = pipeline.retrieve(
        case.question,
        top_k=strategy.top_k,
        allowed_source_ids=strategy.allowed_source_ids,
        rerank_terms=strategy.rerank_terms,
    )
    retrieved_source_ids = [item["chunk"].source_id for item in selected]
    unique_retrieved_source_ids = sorted(set(retrieved_source_ids))
    expected_source_ids = set(case.expected_source_ids)
    retrieved_expected = expected_source_ids & set(retrieved_source_ids)
    recall = 1.0 if not expected_source_ids else len(retrieved_expected) / len(expected_source_ids)
    unsupported_passed = not case.unsupported or not selected
    passed = recall == 1.0 and unsupported_passed
    expected_outcome = "expected_failure" if case.case_id in strategy.expected_failure_case_ids else "pass"
    expectation_met = passed if expected_outcome == "pass" else not passed
    return {
        "case_id": case.case_id,
        "strategy_id": strategy.strategy_id,
        "expected_outcome": expected_outcome,
        "expectation_met": expectation_met,
        "passed": passed,
        "unsupported": case.unsupported,
        "expected_source_ids": sorted(expected_source_ids),
        "retrieved_source_ids": unique_retrieved_source_ids,
        "recall_expected_sources": recall,
        "selected_chunks": [
            {
                "chunk_id": item["chunk"].chunk_id,
                "source_id": item["chunk"].source_id,
                "score": item["score"],
                "matched_terms": item["matched_terms"],
                "rerank_score": item["rerank_score"],
                "rerank_matched_terms": item["rerank_matched_terms"],
            }
            for item in selected
        ],
    }


def run_strategy_audit() -> dict[str, Any]:
    results = [
        evaluate_retrieval_strategy(case, strategy)
        for case in RETRIEVAL_CASES
        for strategy in RETRIEVAL_STRATEGIES
    ]
    expected_failures = [item for item in results if item["expected_outcome"] == "expected_failure"]
    return {
        "status": "completed",
        "control": "deterministic_retrieval_strategy_fixtures",
        "real_embedding_validated": False,
        "real_vector_store_validated": False,
        "real_llm_validated": False,
        "case_count": len(RETRIEVAL_CASES),
        "strategy_count": len(RETRIEVAL_STRATEGIES),
        "result_count": len(results),
        "expected_failure_count": len(expected_failures),
        "expectations_met": all(item["expectation_met"] for item in results),
        "results": results,
        "limitations": [
            "This audit uses deterministic keyword overlap, not embeddings, vector stores, rerankers, or LLM synthesis.",
            "It validates retrieval-eval record shape and predictable failure modes only; it does not prove a chunk size, top-k, filter, or rerank strategy is best for real RAG.",
        ],
    }


def main() -> None:
    pipeline = RagPipeline(DOCUMENTS)
    cases = [
        pipeline.answer("How does RAG help with provenance and source tracing?"),
        pipeline.answer("How is RAG different from long-term memory?"),
        pipeline.answer("What is the project deployment command?"),
    ]
    result = {
        "status": "completed",
        "control": "deterministic_rag_pipeline_and_retrieval_strategy_fixtures",
        "cases": cases,
        "trace": pipeline.serialized_trace(),
        "strategy_audit": run_strategy_audit(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
