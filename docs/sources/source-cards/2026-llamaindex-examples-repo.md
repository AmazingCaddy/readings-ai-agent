# LlamaIndex Examples Repository

- 来源链接：https://github.com/run-llama/llama_index/tree/main/docs/examples
- 仓库链接：https://github.com/run-llama/llama_index
- 作者 / 机构：LlamaIndex / run-llama
- 发布时间：仓库创建于 2022-11-02；持续更新
- 最后复核日期：2026-07-12
- 类型：Source Code / Examples / Framework repository
- 主题：RAG examples / Query engines / Retrievers / Citation / Agent workflows
- 适合阶段：入门后 / 工程实践
- 可信度等级：A/B
- 是否已验证：GitHub 仓库元数据、README、正确的 `docs/examples/index.md` raw 路径、`docs/examples` 目录 API 和 3 个 notebook 抽样已于 2026-07-12 复核；可支撑“LlamaIndex examples 覆盖 RAG、agent workflow、query engine、retriever、citation 等实践形态”的窄边界；不支撑 production-ready、最佳 chunk/top-k/rerank 参数，真实质量结论仍未验证

## 一句话总结

LlamaIndex examples repo 适合初学者在理解 RAG 概念之后，看真实框架示例如何把加载、索引、检索、rerank、回答合成、source nodes 和 agent workflow 组织成代码结构。

## 核心结论

- LlamaIndex README 明确说 examples 位于 `docs/examples`，并给出 `VectorStoreIndex`、`SimpleDirectoryReader`、`query_engine`、persist/reload 等最小用法。
- README 也提醒它不如正式文档更新频繁，因此 source card 应优先把 examples 作为代码示例 reference，而不是最新 API 规范。
- `docs/examples/index.md` 把 examples 分成 Agents、Agentic Workflows、LLM Integrations、Embedding Models、Vector Stores 等入口，适合补充实践路线的广度；注意 raw 路径是 `docs/examples/index.md`，不是 `docs/docs/examples/index.md`。
- `docs/examples/workflow/rag.ipynb` 把 RAG + reranking 拆成 indexing、retrieval、rerank、synthesis 等步骤，和本手册的 RAG pipeline 解释一致。
- `docs/examples/query_engine/citation_query_engine.ipynb` 使用 `CitationQueryEngine`，并展示 `response.source_nodes` 和 `citation_chunk_size`；这能补强“真实框架示例存在 source node / citation 相关实现形态”的证据。
- `docs/examples/retrievers/bm25_retriever.ipynb` 展示 nodes、docstore persistence、metadata filtering、BM25、hybrid retriever 和 `RetrieverQueryEngine`；这能帮助初学者理解检索不是只有向量检索一种形式。

## 支撑证据

- `https://github.com/run-llama/llama_index` 返回 HTTP 200。
- 2026-07-12 GitHub API 元数据显示仓库 `run-llama/llama_index` 为 public，MIT license，默认分支 `main`，语言为 Python，`archived=false`，创建时间为 2022-11-02，`updated_at=2026-07-11T21:07:53Z`，`pushed_at=2026-07-11T01:31:58Z`。
- README 写明 LlamaIndex OSS 是 open-source framework to build agentic applications，并说明 examples 在 `docs/examples` folder。
- README 的 Overview 提醒：`This README is not updated as frequently as the documentation`，需要以正式文档获取最新更新。
- 2026-07-12 GitHub contents API 复核 `docs/examples` 目录，确认存在 `agent`、`citation`、`evaluation`、`query_engine`、`retrievers`、`vector_stores`、`workflow` 等子目录，以及 `docs/examples/index.md` 文件。`https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/index.md` 返回 404，说明旧笔记中的 `docs/docs/examples/index.md` raw 路径不可作为证据。
- `https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/index.md` 返回 HTTP 200；页面说明 examples 是 rich collection of examples，并列出 Function Calling Agent、ReAct Agent、Multi-Agent Workflow、Basic RAG、Advanced Text-to-SQL、OpenAI/Anthropic/Ollama integrations、OpenAI/HuggingFace/Ollama embeddings、Pinecone/Chroma/Qdrant/Azure AI Search vector stores 等入口。
- `docs/examples/agent` 目录复核到 `agent_workflow_basic.ipynb`、`agent_workflow_multi.ipynb`、`agents_as_tools.ipynb`、`openai_agent_retrieval.ipynb`、`openai_agent_with_query_engine.ipynb`、`react_agent.ipynb`、`react_agent_with_query_engine.ipynb` 等 notebook。
- `docs/examples/query_engine` 目录复核到 `citation_query_engine.ipynb`、`RouterQueryEngine.ipynb`、`RetrieverRouterQueryEngine.ipynb`、`knowledge_graph_rag_query_engine.ipynb`、`sub_question_query_engine.ipynb` 等 notebook。
- `docs/examples/retrievers` 目录复核到 `bm25_retriever.ipynb`、`auto_merging_retriever.ipynb`、`ensemble_retrieval.ipynb`、`reciprocal_rerank_fusion.ipynb`、`router_retriever.ipynb`、`recursive_retriever_nodes.ipynb` 等 notebook。
- 2026-07-12 抽样复核 `docs/examples/query_engine/citation_query_engine.ipynb` raw 文件返回 HTTP 200；notebook 导入 `CitationQueryEngine`，通过 `CitationQueryEngine.from_args(index, similarity_top_k=3, citation_chunk_size=512)` 创建 query engine，并打印 `len(response.source_nodes)` 与 source node 文本。
- 2026-07-12 抽样复核 `docs/examples/workflow/rag.ipynb` raw 文件返回 HTTP 200；notebook 标题为 `RAG Workflow with Reranking`，说明 RAG + reranking 由 indexing、retrieval、rerank、synthesizing final response 等步骤组成，并定义 `RetrieverEvent`、`RerankEvent` 与 workflow steps。
- 2026-07-12 抽样复核 `docs/examples/retrievers/bm25_retriever.ipynb` raw 文件成功；notebook 使用 `SentenceSplitter(chunk_size=512)` 生成 nodes，使用 `BM25Retriever`、docstore persistence、metadata filter、Chroma vector store 和 `QueryFusionRetriever` 展示 sparse/dense hybrid retrieval。

## 是否进入正文

- 结论：部分进入；作为 RAG 工程示例和实践路线 reference。
- 原因：它能补强“RAG 示例通常会显式组织加载、索引、检索、rerank、source node / citation 和 response synthesis”等代码层面的学习参考；但本手册仍不能把这些 examples 写成生产方案、默认最佳实践或真实质量证明。

## 可能的问题

- examples 会随仓库版本变化，notebook 依赖、API 参数和默认模型可能失效，需要记录复核日期和具体路径。
- 当前正确 evidence path 是仓库根目录下的 `docs/examples/...`；不要把 `docs/docs/examples/...` 这类错误 raw 路径继续写成已验证来源。
- examples 通常为了教学而简化密钥管理、成本、权限、错误恢复、审计、部署、数据隐私和测试覆盖。
- `CitationQueryEngine` 和 `source_nodes` 示例可以证明框架有 citation/source node 相关实现形态，但不能证明 citation correctness、answer faithfulness 或 source attribution 在真实任务中稳定可靠。
- BM25、hybrid retrieval、rerank、metadata filter 等示例可以作为实验设计参考，不能直接推导某个检索策略优于其他策略。

## 初学者阅读建议

- 先读本手册第 06 章，理解 RAG 的加载、切分、索引、检索、回答合成、citation 和 evaluation 边界。
- 再看 `docs/examples/index.md`，只挑 2-3 个 notebook：Basic RAG workflow、Citation Query Engine、BM25 Retriever。
- 运行真实 notebook 前，先确认 API key、模型成本、依赖版本和输出 trace；不要把示例直接接入私有资料库或生产工具。

## 可复现实验

- 本手册已完成标准库最小 RAG pipeline / citation 模拟实验，验证 chunk metadata、retrieval trace、chunk-level citations 和无证据拒答流程。
- 后续真实实验应基于 LlamaIndex 或等价真实 RAG stack，比较 chunk size、top-k、metadata filter、BM25 / vector / hybrid retrieval、rerank、citation correctness、faithfulness、latency 和 token cost。
