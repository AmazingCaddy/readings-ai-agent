# Real RAG Citation Synthesis 实验

## 目标

验证真实 LLM synthesis 阶段是否能遵守 chunk-level citation 要求：只使用检索到的 chunk，答案中的 citation 必须绑定到具体 `chunk_id`，无证据问题应返回 `grounded=false`。

## 实验边界

这是一个需要真实 OpenAI API 的实验 harness。没有 `OPENAI_API_KEY` 时脚本会输出 `skipped`，不写成已验证结果。

本实验的检索仍使用标准库关键词 overlap，不使用真实 embedding、vector store、reranker 或 LlamaIndex runtime。因此它只验证 LLM synthesis 和 citation 字段，不证明真实 RAG 检索质量。

## 运行方式

```bash
uv run python docs/experiments/real-rag-citation-validation/real_rag_citation_validation.py
```

可选环境变量：

- `OPENAI_MODEL`：默认 `gpt-4.1-mini`。
- `OPENAI_RESPONSES_URL`：默认 `https://api.openai.com/v1/responses`。

## 观察点

- 模型是否输出符合 schema 的 JSON。
- `grounded=true` 时 citations 是否只引用检索到的 `chunk_id`。
- `grounded=false` 时是否避免编造 citation。
- 回答是否包含当前问题所需的最小事实点。
- token、延迟和跨模型稳定性仍需后续扩展。

## 结论状态

- 当前状态：harness 已准备；真实结果取决于本地是否配置 API key 和模型版本。
- 未完成前不得把真实 RAG citation correctness 写成正文结论。
