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

    def retrieve(self, question: str, top_k: int = 2) -> list[dict[str, Any]]:
        query_terms = terms(question)
        scored = []
        for chunk in self.chunks:
            overlap = sorted(query_terms & chunk.keywords)
            score = len(overlap)
            if score:
                scored.append({"chunk": chunk, "score": score, "matched_terms": overlap})
        scored.sort(key=lambda item: (-item["score"], item["chunk"].chunk_id))
        selected = scored[:top_k]
        self.record(
            "retrieve",
            question=question,
            query_terms=sorted(query_terms),
            selected=[
                {
                    "chunk_id": item["chunk"].chunk_id,
                    "score": item["score"],
                    "matched_terms": item["matched_terms"],
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


def main() -> None:
    pipeline = RagPipeline(DOCUMENTS)
    cases = [
        pipeline.answer("How does RAG help with provenance and source tracing?"),
        pipeline.answer("How is RAG different from long-term memory?"),
        pipeline.answer("What is the project deployment command?"),
    ]
    result = {
        "cases": cases,
        "trace": pipeline.serialized_trace(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
