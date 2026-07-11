# Real RAG Citation Synthesis 实验

## 目标

验证 RAG synthesis 阶段和 citation verifier 的边界：只使用检索到的 chunk，答案中的 citation 必须绑定到具体 `chunk_id` 和原文 quote，无证据问题应返回 `grounded=false`。

## 实验边界

有 `OPENAI_API_KEY` 时，本实验会调用真实 OpenAI Responses API 观察 LLM synthesis。没有 `OPENAI_API_KEY` 时，脚本会运行本地 deterministic verifier control：3 个正常 case 必须通过，5 个 adversarial citation fixture 必须被拒绝。

本实验的检索仍使用标准库关键词 overlap，不使用真实 embedding、vector store、reranker 或 LlamaIndex runtime。无 API key completed run 只验证 citation verifier 形状，不证明真实 LLM citation correctness、faithfulness 或真实 RAG 检索质量。

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
- citation quote 是否真的出现在被引用 chunk 中。
- `grounded=false` 时是否避免编造 citation。
- 本地 verifier 是否能拒绝 unknown chunk、missing citation、ungrounded citation、quote mismatch 和 unsupported grounded claim。
- 回答是否包含当前问题所需的最小事实点。
- token、延迟和跨模型稳定性仍需后续扩展。

## 结论状态

- 当前状态：本地 deterministic citation verifier control 已完成；真实 LLM synthesis 结果取决于本地是否配置 API key 和模型版本。
- 不得把本地 verifier control 写成真实模型 citation correctness 或 answer faithfulness 结论。
