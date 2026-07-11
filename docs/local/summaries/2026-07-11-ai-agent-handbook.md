# Conversation Summary: AI Agent Handbook
**Date:** 2026-07-11
**Last Updated:** 2026-07-11 16:09 Asia/Shanghai
**Status:** In Progress

## Objective
Build a beginner-friendly Chinese AI Agent learning handbook from verified source cards and publish it as a GitHub Pages/MkDocs site. The handbook should explain concepts progressively, include reliable references, and clearly distinguish validated claims from pending or contextual claims.

## Key Decisions
- **Decision:** Use `uv` and MkDocs Material for the handbook site.
  - *Rationale:* The project already uses this tooling and `uv run mkdocs build --strict` provides a fast validation loop.
- **Decision:** Keep commits logically scoped by chapter batch.
  - *Rationale:* The user wants clean Git history and does not want unfinished mixed changes committed together.
- **Decision:** Treat references as first-class content.
  - *Rationale:* The final handbook should be useful for study and should make source trust and verification status visible.

## Progress
1. Initialized the handbook project structure and committed setup work in earlier turns.
2. Added source cards, coverage matrix, claim ledger, glossary, and learning path.
3. Drafted and committed chapters 00-05.
4. Drafted chapters 06 and 07, then committed them as `6777a2f Draft RAG memory and orchestration chapters`.
5. Verified the site with `uv run mkdocs build --strict`; build passed with only the upstream Material for MkDocs warning about MkDocs 2.0.
6. Drafted chapters 08 and 09 covering Evaluation / Observability and Production / Security with conservative wording around source cards that are link-verified but pending deep content validation.
7. Drafted chapters 10, 11, and 12 covering framework comparison, hands-on project roadmap, and the source/reference map.
8. Started evidence-upgrade goal. Added OpenAI docs MCP globally, but current session still does not expose its tools until restart/new session; used official URL fetching as fallback.
9. Completed first evidence upgrade for Tool Use / Function Calling boundary using OpenAI Function Calling docs, Responses API reference, and Toolformer arXiv abstract.
10. Completed first evidence upgrade for MCP host/client/server boundary using MCP architecture, server concepts, client concepts, and MCP servers README.
11. Completed first evidence upgrade for RAG vs Memory boundary using RAG paper abstract and LangGraph memory docs.
12. Completed first evidence upgrade for Prompt Injection / Production Security boundary using OWASP LLM Top 10 key risk items, NIST AI RMF overview, and existing tool-calling evidence.
13. Completed first evidence upgrade for Agent Eval / Trajectory boundary using AgentBench and WebArena abstracts plus OpenAI Evals README.
14. Completed first evidence upgrade for Agent vs Workflow boundary using OpenAI Agents SDK docs/README, LangGraph overview markdown, and ReAct.
15. Completed first evidence upgrade for Multi-agent default boundary using AutoGen AgentChat docs, CrewAI Introduction markdown, AgentBench, and eval evidence.
16. Completed first evidence upgrade for long-term memory governance and risk boundary using MemoryBank, MemGPT, Generative Agents, Letta memory docs, Zep concepts docs, OWASP LLM Top 10, and NIST AI RMF.
17. Completed first evidence upgrade for LLM context engineering and structured output boundaries using OpenAI Text Generation docs, Structured Outputs docs, Responses API reference, Function Calling docs, and existing RAG/Memory and Prompt Injection evidence.
18. Completed first evidence upgrade for Agent architecture pattern boundaries using ReAct, Reflexion, Tree of Thoughts, LangGraph, OpenAI Agents SDK, and existing Agent/Workflow plus Multi-agent evidence.
19. Completed first evidence upgrade for RAG engineering flow using RAG paper, LlamaIndex framework overview, RAG overview, Documents / Nodes, Indexing, Retriever, and Query Engine docs.

## Technical Context
- Files modified recently: `docs/sources/source-cards/2026-llamaindex-docs.md`, `docs/evidence/rag-engineering-boundary.md`, `docs/evidence/claim-ledger.md`, `docs/evidence/validation-backlog.md`, `docs/references/coverage-matrix.md`, `docs/chapters/06-rag-memory.md`, `docs/local/summaries/2026-07-11-ai-agent-handbook.md`.
- Existing chapter pattern: target audience, learning outcomes, one-sentence intuition, concepts, examples, mechanisms, engineering practice, mistakes, boundaries, verified conclusions, summary, references.
- Dependencies: `uv`, MkDocs Material.

## Open Questions
- Run the minimal tool-calling experiment to upgrade the Function Calling boundary from partial verification toward `可入正文`.
- Run a workflow vs workflow-agent hybrid vs agent loop comparison experiment for the same task.
- Run a fixed workflow vs ReAct tool loop vs planner/executor vs reflection retry experiment for the same issue-analysis task.
- Run an output parsing experiment comparing free text, JSON mode, and Structured Outputs; include refusal and semantic-error handling.
- Run a long-context failure-mode experiment covering irrelevant context, conflicting context, stale context, external prompt injection, truncation behavior, and token cost.
- Run a single-agent vs planner/executor vs multi-agent comparison experiment for the same research/writing task.
- Run a toy Agent eval experiment comparing final-answer-only scoring with trajectory/trace-aware scoring.
- Run a minimal read-only MCP trace experiment to upgrade the MCP role boundary from partial verification toward `可入正文`.
- Run a minimal RAG vs short-term vs long-term memory comparison experiment.
- Run a minimal RAG pipeline experiment comparing chunk size, metadata, top-k, rerank/filter, citation correctness, answer faithfulness, latency, and token cost. LlamaIndex docs search did not directly verify source citation/source_nodes behavior in the latest docs.
- Run a multi-session long-term memory governance experiment covering explicit write confirmation, automatic write failure modes, stale preference invalidation, conflicting facts, and sensitive information handling.
- Run a minimal prompt-injection permission-boundary experiment covering external document injection, read/write tool separation, parameter validation, human confirmation, and audit logs.
- In a new session, verify whether the newly added `openaiDeveloperDocs` MCP tools are exposed.

## Blockers
(none currently)
