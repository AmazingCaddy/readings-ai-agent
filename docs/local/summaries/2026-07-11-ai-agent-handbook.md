# Conversation Summary: AI Agent Handbook
**Date:** 2026-07-11
**Last Updated:** 2026-07-11 00:45 Asia/Shanghai
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

## Technical Context
- Files modified recently: `docs/sources/source-cards/2026-openai-function-calling-docs.md`, `docs/sources/source-cards/2026-openai-responses-api-docs.md`, `docs/sources/source-cards/2023-toolformer-paper.md`, `docs/evidence/tool-use-function-calling-boundary.md`, `docs/evidence/claim-ledger.md`, `docs/evidence/validation-backlog.md`, `docs/references/coverage-matrix.md`, `docs/chapters/03-tool-use.md`, `docs/local/summaries/2026-07-11-ai-agent-handbook.md`.
- Existing chapter pattern: target audience, learning outcomes, one-sentence intuition, concepts, examples, mechanisms, engineering practice, mistakes, boundaries, verified conclusions, summary, references.
- Dependencies: `uv`, MkDocs Material.

## Open Questions
- Run the minimal tool-calling experiment to upgrade the Function Calling boundary from partial verification toward `可入正文`.
- In a new session, verify whether the newly added `openaiDeveloperDocs` MCP tools are exposed.

## Blockers
(none currently)
