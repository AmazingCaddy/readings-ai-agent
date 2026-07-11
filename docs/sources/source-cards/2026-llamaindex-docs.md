# LlamaIndex Documentation

- 来源链接：https://developers.llamaindex.ai/python/framework/
- 作者 / 机构：LlamaIndex
- 发布时间：持续更新文档；入口页面 last-modified 复核为 2026-07-09；`llms.txt` / RAG markdown 复核为 2026-07-11
- 最后复核日期：2026-07-12
- 类型：框架文档
- 主题：RAG / Data Framework / Agents
- 适合阶段：入门后 / 工程实践
- 可信度等级：A
- 是否已验证：入口、`llms.txt`、RAG 总览和核心组件 Markdown 页面已于 2026-07-12 复核；RAG 工程 pipeline 窄边界已可入正文；跨框架术语对照第一轮已完成；标准库最小 pipeline / citation / retrieval strategy audit 和上下文策略对比实验已完成；本地 LlamaIndex `VectorStoreIndex` / retriever / QueryEngine / `MockLLM` / source-node metadata run 已完成

## 一句话总结

LlamaIndex 是理解 RAG、数据连接、索引和 agent data framework 的重要工程 reference。

## 核心结论

- LlamaIndex 总览把 context augmentation 定义为让你的数据进入 LLM 可用于解决问题的上下文，并说明工具覆盖 ingest、parse、index、process 和 query workflows。
- Introduction to RAG 页面把 RAG 描述为：数据先 loaded/prepared/indexed，用户 query 在 index 上过滤出最相关 context，再把 context 和 query 一起交给 LLM 生成回答。
- RAG 页面把工程流程拆成五个阶段：Loading、Indexing、Storing、Querying、Evaluation；结合 RAG paper 动机和标准库最小 pipeline 实验，可支撑“RAG 是可观察工程 pipeline，不是单个 prompt 技巧”的窄结论。
- Documents / Nodes 页面定义 `Document` 是数据源容器，`Node` 是源 Document 的 chunk，并包含 metadata 和 relationship 信息。
- Indexing 页面定义 `Index` 是能快速为用户 query 检索相关 context 的数据结构，通常由 Documents 构建，内部存储 Nodes，并暴露 Retriever 接口。
- Retriever 页面定义 retriever 负责根据用户 query 或 chat message 抓取最相关 context，是 query engine 和 chat engine 的关键构件。
- Query Engine 页面定义 query engine 是对数据提问的通用接口，通常基于一个或多个 indexes 和 retrievers 返回 rich response。

## 支撑证据

- `https://developers.llamaindex.ai/python/framework/` 返回 HTTP 200，HEAD 复核显示 `last-modified: Thu, 09 Jul 2026 18:22:34 GMT`。
- 2026-07-12 抓取 `https://developers.llamaindex.ai/llms.txt` 成功；该索引列出 Search API 和 RAG、Documents / Nodes、Indexing、Retriever、Query Engine 等页面。
- 2026-07-12 抓取 `https://developers.llamaindex.ai/python/framework/understanding/rag/index.md` 成功；页面直接说明 RAG 让 LLM 使用你的数据，查询在 index 上过滤最相关 context，再把 context 和 query 交给 LLM，并列出 Loading、Indexing、Storing、Querying、Evaluation 五个阶段。
- 2026-07-12 抓取 Documents / Nodes、Indexing、Retriever、Query Engine Markdown 页面成功：Documents / Nodes 页面定义 `Document` 是任意数据源容器、`Node` 是源 Document 的 chunk 且带 metadata / relationships；Indexing 页面定义 `Index` 是快速检索 query 相关 context 的数据结构，通常由 Documents 构建、内部存储 Nodes、暴露 Retriever；Retriever 页面定义 retriever 负责根据 query 或 chat message 获取最相关 context；Query Engine 页面定义 query engine 是对数据提问并返回 rich response 的通用接口，通常基于 indexes 和 retrievers。
- 2026-07-12 同步复核 LlamaIndex examples repo：正确 raw 路径是 `docs/examples/index.md`；错误路径 `docs/docs/examples/index.md` 返回 404，不能作为证据路径。
- 2026-07-11 运行 Real LlamaIndex RAG Source-Node Validation，并在 2026-07-12 扩展：使用 `llama-index-core`、`VectorStoreIndex`、本地 deterministic keyword embedding、QueryEngine、`MockLLM` 和自定义 node postprocessor 跑通 4 个 `Document`、3 个 retrieval case、3 个 QueryEngine case、retriever / response source-node metadata、应用层 trust filter、chunk-level citation metadata 和无证据 `grounded=false`；结果 `all_passed=true`、`untrusted_chunk_cited=false`、`query_engine_source_nodes_present=true`、`unsupported_query_engine_empty=true`、`secret_leaked_in_trace=false`。

## 可能的问题

- 框架文档会随着版本演进变化，需要记录复核日期。
- 需要区分 RAG 的通用概念和 LlamaIndex 的具体实现抽象。
- LlamaIndex 是框架文档，可支撑现代工程流程和术语，但不能单独证明某个 chunking、embedding、retrieval、citation 或 reranking 策略在具体任务中最优。
- LlamaIndex docs 本身主要支撑工程流程和组件边界；`source_nodes` / citation 的代码形态已由 LlamaIndex examples repo source card 抽样补强。本地 `VectorStoreIndex` / QueryEngine / `MockLLM` run 只支撑真实框架 retrieval、response source-node metadata 和 node postprocessor 的最小观察；真实 LlamaIndex / LLM synthesis 下的 citation correctness、faithfulness、embedding / vector DB / reranker 表现仍需后续实验。

## 初学者阅读建议

- 先理解 document、chunk、index、retriever、query engine，再看 agent 相关功能。

## 可复现实验

- 已完成标准库最小 RAG pipeline / citation / retrieval strategy 模拟实验，验证 chunk metadata、retrieval trace、chunk-level citations、无证据拒答 / `grounded=false` 流程，以及 top-k 过小、metadata filter 错配、细 chunk + rerank terms 仍可能漏召回的固定失败样例。
- 已完成标准库上下文策略对比实验，验证基础 keyword RAG 可能召回不可信外部文档；RAG 需要 trust/freshness metadata、filter、citation 和 human gate trace。
- 已纳入框架能力交叉表，用于支撑“RAG / data framework / Documents / Nodes / Indexes / Retrievers / Query Engines”的保守定位；与其他框架卡片和 rubric smoke test 共同支撑“框架应按任务难点比较，不能写成某个框架默认最好”的窄边界；不代表真实横向性能结论。
- 已纳入 Tool / Function / Plugin 术语对照 evidence，用于说明 LlamaIndex 的 retriever / query engine 属于数据检索和问答 pipeline 抽象，可作为 Agent 工具使用，但本身不等同于通用工具调用协议或 Agent runtime。
- Real RAG Citation Synthesis harness 已完成本地 deterministic citation verifier control：本地关键词检索提供 chunk，deterministic synthesis 生成结构化 answer / grounded / citations，校验 citation id、quote 是否出现在 cited chunk、grounded/ungrounded citation 规则和最小语义；当前无 API key，真实 LLM synthesis 未运行，不能提前升级真实 citation correctness 结论。
- 已完成 Real LlamaIndex RAG Source-Node Validation：本地 `llama-index-core` / `VectorStoreIndex` / retriever / QueryEngine / `MockLLM` run 验证 source-node metadata、trust filter、node postprocessor、citation metadata 和无证据 `grounded=false` / empty source nodes 的最小结构；没有运行真实 LLM synthesis。
- 已补 LlamaIndex examples repo source card：抽样验证 `CitationQueryEngine`、`response.source_nodes`、RAG workflow with reranking、BM25 / hybrid retrieval 示例；这些示例只能作为代码结构参考，不证明真实效果。
- 后续仍需用真实 embedding / vector store / reranker / LLM synthesis 比较不同 chunking、top-k、rerank 和 citation correctness 设置。

## 是否进入正文

- 结论：进入；工程 pipeline 窄边界可入正文
- 原因：RAG、Memory 和框架生态章节需要现代工程 reference。当前已可支撑 RAG 的 loading、indexing、storing、querying/retrieval、response synthesis、evaluation、chunk metadata、retrieval trace、citation/source 绑定、retriever/query engine 术语边界，以及本地 LlamaIndex retrieval / QueryEngine source-node metadata 的最小观察；真实 LLM citation correctness、answer faithfulness、embedding / vector store、chunk size/top-k/rerank、latency、token cost 和生产权限边界仍需实验。
