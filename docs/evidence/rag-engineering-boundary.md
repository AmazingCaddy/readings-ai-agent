# Evidence Note: RAG 工程流程边界

## 要验证的结论

工程 RAG 不只是“把文档塞进 prompt”。一个最小可治理的 RAG 流程通常需要数据加载、文档/节点切分、索引、存储、检索、可选 rerank/filter、回答合成和评测。RAG 可以改善外部知识访问和知识更新问题，但它不保证答案正确；检索质量、chunking、metadata、embedding、retriever、postprocessor、response synthesis 和评测都会影响结果。

## 资料来源

- Source 1：[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](../sources/source-cards/2020-rag-paper.md)
- Source 2：[LlamaIndex Documentation](../sources/source-cards/2026-llamaindex-docs.md)
- Source 3：[Evidence Note: RAG 与 Memory 边界](rag-memory-boundary.md)
- Source 4：[Evidence Note: 上下文工程与结构化输出边界](context-structured-output-boundary.md)
- Source 5：[RAG 最小 Pipeline 与 Citation 实验结果](../experiments/rag-pipeline/results-2026-07-11.md)
- Source 6：[上下文策略对比实验结果](../experiments/context-strategy-comparison/results-2026-07-11.md)

## 交叉验证结果

- 一致点：RAG paper 摘要支持外部检索增强生成的基础动机，包括知识密集任务、provenance 和 world knowledge 更新。
- 一致点：LlamaIndex RAG 总览把流程拆成 Loading、Indexing、Storing、Querying、Evaluation 五个阶段；这支持第 06 章的最小 RAG 流程。
- 一致点：LlamaIndex Documents / Nodes 页面定义 Document 是数据源容器，Node 是源 Document 的 chunk，并包含 metadata 和 relationship 信息；这支持“chunk 需要保留来源和上下文关系”的工程解释。
- 一致点：LlamaIndex Indexing 页面把 Index 定义为快速检索相关 context 的数据结构，通常存储 Nodes 并暴露 Retriever 接口。
- 一致点：LlamaIndex Retriever 页面把 retriever 定义为根据 query 或 chat message 抓取最相关 context 的组件；Query Engine 页面说明 query engine 通常基于 indexes 和 retrievers 对数据提问并返回 rich response。
- 一致点：LlamaIndex RAG 总览明确 Evaluation 是关键阶段，用于检查相对其他策略或修改后的效果，并关注 accurate、faithful 和 fast；这支持“RAG 需要评测而不是凭感觉调参”。
- 边界：LlamaIndex 是框架文档，支撑现代工程术语和流程，但不能证明某个 chunk size、embedding、vector store、retriever 或 reranker 在所有任务中最优。
- 边界：本次 LlamaIndex 文档搜索未找到直接可用的 source citation / source_nodes 页面证据，因此“答案必须带可追溯 references”的工程实现仍需后续具体示例或实验补强。
- 本地实验：标准库最小 RAG pipeline 把 3 个文档加载为带 metadata 的 chunks，用关键词 overlap 检索，输出绑定到 `chunk_id`、`source_id`、`title`、`url` 的 citations，并在无检索证据时返回 `grounded=false`。这支持“最小 RAG 应记录 chunk / retrieve / synthesize trace，并把 answer citation 绑定到具体 chunk”的工程建议。
- 本地实验：标准库上下文策略对比实验中，基础 `keyword_rag` 在一个 case 里找对产品文档，但在退款争议 case 中把外部注入 attachment 排到前面，导致错误答案和错误 human-review gate。这支持“RAG retrieval 需要 trust/freshness metadata、filter、citation 校验和权限边界”的工程建议。

## 实验验证

- 是否需要实验：是
- 实验设计：用同一组手册资料建立最小 RAG pipeline，比较不同 chunk size、metadata、top-k、rerank/filter 和无 RAG baseline。记录检索命中率、引用正确率、答案忠实度、延迟、token 成本和无法回答时的处理。
- 结果：已完成标准库最小 pipeline / citation 模拟实验。实验验证了 chunk metadata、retrieval trace、citation 字段和 unsupported question 拒答流程。尚未覆盖真实 embedding、vector store、rerank、LLM synthesis、chunk size 对比、latency 或 token cost。

## 结论状态

- 部分验证：RAG paper 支撑外部检索增强的基础动机，LlamaIndex 支撑现代工程流程和组件边界；标准库模拟实验支撑最小 pipeline trace、chunk-level citation、trust/freshness metadata 和 human gate 设计。仍缺真实 RAG stack、chunk size/top-k/rerank 对比、LLM faithfulness 和成本/延迟实验。

## 可进入章节

- 是。可以写成：RAG 是一条工程 pipeline，而不是单个 prompt 技巧。初学者应先保证加载、切分、索引、检索、回答合成、citation 和评测可观察，再讨论更复杂的 embedding、rerank、hybrid retrieval 或 agentic RAG。
