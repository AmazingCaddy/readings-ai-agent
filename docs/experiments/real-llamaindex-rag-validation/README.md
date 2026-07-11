# Real LlamaIndex RAG Source-Node Validation

## 目标

用真实 `llama-index-core` runtime 跑一个最小 RAG retrieval / query-engine source-node metadata 检查，验证 `Document`、`VectorStoreIndex`、retriever、QueryEngine、source node metadata、node postprocessor、trust filter 和 citation metadata 的本地可观察流程。

## 实验边界

本实验使用本地 deterministic keyword embedding 和 LlamaIndex `MockLLM`，不调用真实 embedding model、vector database、reranker 或真实 LLM。它验证的是 LlamaIndex 框架中的最小 retrieval / QueryEngine / source-node 结构，不证明答案生成质量、citation faithfulness、chunking 策略优劣、OpenAI File Search 行为、成本、延迟或生产可靠性。

## 运行方式

```bash
uv run --with llama-index-core python docs/experiments/real-llamaindex-rag-validation/real_llamaindex_rag_validation.py
```

没有 `llama-index-core` 时，脚本会返回 `skipped`，不会把框架行为写成已验证结论。

## 观察点

- `VectorStoreIndex.from_documents()` 是否能从本地 `Document` 构建索引。
- retriever 是否返回带 metadata 的 source nodes。
- trusted / untrusted chunk 是否能在应用层被区分。
- 有证据问题是否返回 chunk-level citations。
- 无证据问题是否返回 `grounded=false` 且不编造 citation。
- QueryEngine 是否在 `MockLLM` synthesis 路径上保留 `response.source_nodes`。
- 自定义 node postprocessor 是否能在 QueryEngine 路径上过滤 untrusted 和 zero-score nodes。
- trace 是否避免记录原始恶意文本里的示例 secret。

## 结论状态

- 当前状态：已完成本地 LlamaIndex `VectorStoreIndex` / retriever / QueryEngine / `MockLLM` / source-node metadata run。
- 可支撑：真实框架中 Document、index、retriever、QueryEngine、source node metadata、node postprocessor、应用层 trust filter 和 citation metadata 的最小可观察结构。
- 不能支撑：真实 LLM synthesis 质量、citation faithfulness、真实 embedding / vector DB / reranker / File Search 策略优劣、chunk size / top-k 最佳实践、成本、延迟或生产 RAG 质量。
