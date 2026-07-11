# LlamaIndex Documentation

- 来源链接：https://developers.llamaindex.ai/python/framework/
- 作者 / 机构：LlamaIndex
- 发布时间：持续更新文档；页面 last-modified 复核为 2026-07-09
- 最后复核日期：2026-07-11
- 类型：框架文档
- 主题：RAG / Data Framework / Agents
- 适合阶段：入门后 / 工程实践
- 可信度等级：A
- 是否已验证：入口、RAG 总览和核心组件页面已复核；RAG 工程流程边界已完成第一轮交叉验证；标准库最小 pipeline / citation 模拟实验和上下文策略对比实验已完成

## 一句话总结

LlamaIndex 是理解 RAG、数据连接、索引和 agent data framework 的重要工程 reference。

## 核心结论

- LlamaIndex 总览把 context augmentation 定义为让你的数据进入 LLM 可用于解决问题的上下文，并说明工具覆盖 ingest、parse、index、process 和 query workflows。
- Introduction to RAG 页面把 RAG 描述为：数据先 loaded/prepared/indexed，用户 query 在 index 上过滤出最相关 context，再把 context 和 query 一起交给 LLM 生成回答。
- RAG 页面把工程流程拆成五个阶段：Loading、Indexing、Storing、Querying、Evaluation。
- Documents / Nodes 页面定义 `Document` 是数据源容器，`Node` 是源 Document 的 chunk，并包含 metadata 和 relationship 信息。
- Indexing 页面定义 `Index` 是能快速为用户 query 检索相关 context 的数据结构，通常由 Documents 构建，内部存储 Nodes，并暴露 Retriever 接口。
- Retriever 页面定义 retriever 负责根据用户 query 或 chat message 抓取最相关 context，是 query engine 和 chat engine 的关键构件。
- Query Engine 页面定义 query engine 是对数据提问的通用接口，通常基于一个或多个 indexes 和 retrievers 返回 rich response。

## 支撑证据

- `https://docs.llamaindex.ai/` 重定向到 `https://developers.llamaindex.ai/python/framework/` 并返回 HTTP 200。
- 2026-07-11 抓取 `https://developers.llamaindex.ai/llms.txt` 成功；该索引说明文档页面可通过追加 `index.md` 获取 Markdown，并列出 RAG、Documents / Nodes、Indexing、Retriever、Query Engine 等页面。
- 2026-07-11 抓取 `https://developers.llamaindex.ai/python/framework/understanding/rag/index.md` 成功；页面包含 RAG 五阶段、Documents/Nodes、Connectors、Indexes、Embeddings、Retrievers、Routers、Node Postprocessors、Response Synthesizers 等关键内容。
- 2026-07-11 抓取 Documents / Nodes、Indexing、Retriever、Query Engine 页面成功，并与 RAG 论文及 RAG/Memory evidence 完成第一轮交叉验证。

## 可能的问题

- 框架文档会随着版本演进变化，需要记录复核日期。
- 需要区分 RAG 的通用概念和 LlamaIndex 的具体实现抽象。
- LlamaIndex 是框架文档，可支撑现代工程流程和术语，但不能单独证明某个 chunking、embedding、retrieval 或 reranking 策略在具体任务中最优。
- 本次未找到可直接支撑 LlamaIndex `source_nodes` 细节的官方检索结果；标准库实验已验证通用 chunk-level citation 字段设计，但真实 LlamaIndex / LLM synthesis 下的 citation correctness 仍需后续实验。

## 初学者阅读建议

- 先理解 document、chunk、index、retriever、query engine，再看 agent 相关功能。

## 可复现实验

- 已完成标准库最小 RAG pipeline / citation 模拟实验，验证 chunk metadata、retrieval trace、chunk-level citations 和无证据拒答流程。
- 已完成标准库上下文策略对比实验，验证基础 keyword RAG 可能召回不可信外部文档；RAG 需要 trust/freshness metadata、filter、citation 和 human gate trace。
- 已准备真实 LLM citation synthesis harness：本地关键词检索提供 chunk，上游 LLM 生成结构化 answer / grounded / citations，并校验 citation id 和最小语义；结果待跑，不能提前升级结论。
- 后续仍需用真实 embedding / vector store / LlamaIndex pipeline 比较不同 chunking、top-k、rerank 和 LLM synthesis 设置。

## 是否进入正文

- 结论：进入
- 原因：RAG、Memory 和框架生态章节需要现代工程 reference。
