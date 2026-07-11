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
- Source 7：[Self-RAG paper](../sources/source-cards/2023-self-rag-paper.md)
- Source 8：[LlamaIndex Examples Repository](../sources/source-cards/2026-llamaindex-examples-repo.md)
- Source 9：[OpenAI File Search and Retrieval Documentation](../sources/source-cards/2026-openai-file-search-retrieval-docs.md)

## 交叉验证结果

- 一致点：RAG paper 摘要支持外部检索增强生成的基础动机，包括知识密集任务、provenance 和 world knowledge 更新。
- 一致点：Self-RAG paper 摘要指出，盲目固定检索并塞入固定数量 passage，即使 retrieval 不必要或 passage 不相关，也可能降低模型 versatility 或产生 unhelpful response；这支持“RAG 需要检索必要性、passage relevance、faithfulness 和 citation correctness 评估”的工程边界。
- 一致点：Self-RAG paper 用 on-demand retrieval、对 retrieved passages 和自身生成的 reflection / critique，以及 citation accuracy 作为实验关注点；这与本手册要求记录 retrieval trace、citation/source 绑定和无证据拒答的方向一致。
- 一致点：LlamaIndex RAG 总览把流程拆成 Loading、Indexing、Storing、Querying、Evaluation 五个阶段；这支持第 06 章的最小 RAG 流程。
- 一致点：LlamaIndex Documents / Nodes 页面定义 Document 是数据源容器，Node 是源 Document 的 chunk，并包含 metadata 和 relationship 信息；这支持“chunk 需要保留来源和上下文关系”的工程解释。
- 一致点：LlamaIndex Indexing 页面把 Index 定义为快速检索相关 context 的数据结构，通常存储 Nodes 并暴露 Retriever 接口。
- 一致点：LlamaIndex Retriever 页面把 retriever 定义为根据 query 或 chat message 抓取最相关 context 的组件；Query Engine 页面说明 query engine 通常基于 indexes 和 retrievers 对数据提问并返回 rich response。
- 一致点：LlamaIndex RAG 总览明确 Evaluation 是关键阶段，用于检查相对其他策略或修改后的效果，并关注 accurate、faithful 和 fast；这支持“RAG 需要评测而不是凭感觉调参”。
- 一致点：LlamaIndex examples repo 中 `workflow/rag.ipynb` 把 RAG + reranking 拆成 indexing、retrieval、rerank 和 synthesis；`query_engine/citation_query_engine.ipynb` 使用 `CitationQueryEngine` 并展示 `response.source_nodes`；`retrievers/bm25_retriever.ipynb` 展示 nodes、docstore、metadata filter、BM25、hybrid retriever 和 `RetrieverQueryEngine`。这补强了“工程 RAG 示例会显式组织 pipeline、retriever 和 source/citation trace”的代码层证据。
- 一致点：OpenAI File Search guide 把 `file_search` 描述为 Responses API 的 hosted tool，基于 vector stores 中已上传文件做 semantic and keyword search，并返回 `file_search_call` 和带 `file_citation` annotations 的 message。这补强了“托管 RAG 工具也应观察工具调用、检索 query 和 citation/source”的 API 层证据。
- 一致点：OpenAI File Search guide 明确 search results 默认不返回，需使用 `include=["file_search_call.results"]`；这与本手册要求保存 retrieval trace、source binding 和可审计证据一致。
- 一致点：OpenAI Retrieval guide 说明 semantic search 基于 vector embeddings，可命中少量或没有关键词重叠的结果；同时支持 query rewriting、attribute filtering、ranking options、hybrid search 权重、vector store attributes、expiration policies 和 chunking strategy。这补强了“RAG 质量来自检索、过滤、排序、chunking 和成本治理组合，而不是单个 prompt”的工程边界。
- 一致点：OpenAI Retrieval guide 说明 vector store file 加入后会自动 chunk、embed 和 index，并给出默认 chunking 参数、chunking 限制、文件大小/token 限制、storage pricing 和删除后 eventual consistency。这支持第 06/11 章把托管 RAG 也纳入成本、延迟、删除一致性和权限验证。
- 边界：LlamaIndex 是框架文档，支撑现代工程术语和流程，但不能证明某个 chunk size、embedding、vector store、retriever 或 reranker 在所有任务中最优。
- 边界：LlamaIndex examples 可以证明框架示例中存在 citation / source node 相关实现形态，但不能证明真实 citation correctness、answer faithfulness、source attribution 稳定性或生产权限边界。
- 边界：OpenAI File Search / Retrieval 是官方产品文档，支撑 API shape 和托管检索能力存在；不能证明默认 chunking/ranking、file citations、semantic search 或 hosted tool 在具体业务中的 citation correctness、faithfulness、成本、延迟或权限治理效果。
- 本地实验：标准库最小 RAG pipeline 把 3 个文档加载为带 metadata 的 chunks，用关键词 overlap 检索，输出绑定到 `chunk_id`、`source_id`、`title`、`url` 的 citations，并在无检索证据时返回 `grounded=false`。这支持“最小 RAG 应记录 chunk / retrieve / synthesize trace，并把 answer citation 绑定到具体 chunk”的工程建议。
- 本地实验：标准库上下文策略对比实验中，基础 `keyword_rag` 在一个 case 里找对产品文档，但在退款争议 case 中把外部注入 attachment 排到前面，导致错误答案和错误 human-review gate。这支持“RAG retrieval 需要 trust/freshness metadata、filter、citation 校验和权限边界”的工程建议。
- 本地实验：Real RAG Citation Synthesis harness 在无 API key 时运行 deterministic citation verifier control。3 个正常 case 通过，5 个 adversarial fixture 被拒绝，覆盖 unknown chunk id、grounded answer missing citation、ungrounded answer with citation、quote not in cited chunk 和 unsupported question marked grounded。这支持“citation verifier 至少要检查 citation id、quote 与 chunk 文本绑定、grounded/ungrounded 状态和最小语义”的字段设计；它不调用真实 LLM。
- 真实框架本地观察：Real LlamaIndex RAG Source-Node Validation 使用 `llama-index-core`、`VectorStoreIndex`、本地 deterministic keyword embedding、QueryEngine、`MockLLM` 和自定义 node postprocessor。retriever case 观察到 untrusted malicious refund note 会被检索到但不会进入 citations；QueryEngine / `MockLLM` case 观察到 `response.source_nodes` 保留 trusted source-node metadata，无证据 browser/captcha query 返回 `Empty Response` 且 source_nodes 为空。该结果支撑 LlamaIndex retrieval / response source-node plumbing、trust filter 和 empty-source behavior 的窄观察，但 `MockLLM` 不证明真实答案忠实性。

## 实验验证

- 是否需要实验：是
- 实验设计：用同一组手册资料建立最小 RAG pipeline，比较不同 chunk size、metadata、top-k、rerank/filter、OpenAI File Search / vector store 和无 RAG baseline。记录检索命中率、included search results、引用正确率、答案忠实度、延迟、token / storage 成本、删除一致性和无法回答时的处理。
- 结果：已完成标准库最小 pipeline / citation / retrieval strategy 模拟实验、Real RAG Citation Synthesis deterministic verifier control 和 Real LlamaIndex RAG Source-Node Validation。标准库实验验证了 chunk metadata、retrieval trace、citation 字段、unsupported question 拒答流程，并用 3 个 case / 4 个 strategy 暴露 top-k 过小、metadata filter 错配、细 chunk + rerank terms 仍可能漏召回的固定失败样例；citation verifier control 验证了 citation id / quote / groundedness / unsupported-claim 的最小校验器和失败样例；LlamaIndex run 验证了真实框架中的 retriever source nodes、QueryEngine `response.source_nodes`、node postprocessor、trust filter、empty source nodes 和 trace 脱敏。尚未覆盖真实 embedding、vector store、rerank、真实 LLM synthesis、真实 chunk size 对比、latency 或 token cost。

## 结论状态

- 可入正文：窄结论“RAG 的基础动机包括外部知识访问、知识更新和 provenance / source traceability”已完成第一轮交叉验证。RAG paper 摘要直接支撑知识密集任务、外部检索、provenance 和 world knowledge 更新动机；LlamaIndex RAG 文档支撑现代工程中通过 loading / indexing / retrieval / response synthesis / evaluation 把外部数据接入 LLM 上下文。
- 可入正文：窄结论“工程 RAG 是 loading、indexing、storing、querying/retrieval、response synthesis 和 evaluation 等阶段组成的可观察 pipeline，不是单个 prompt 技巧；最小可治理 RAG 应保留 chunk metadata、retrieval trace、citation/source 绑定、检索必要性/相关性判断、citation verifier 和无证据拒答或 `grounded=false` 标记”已完成第一轮交叉验证。RAG paper 支撑外部检索、provenance 和知识更新动机，Self-RAG paper 支撑不要盲目固定检索、需要评估 retrieval necessity / passage relevance / critique / citation accuracy，LlamaIndex docs 支撑现代工程流程和组件边界，LlamaIndex examples repo 补强 citation/source node、retriever 和 RAG workflow 的代码示例证据，OpenAI File Search / Retrieval docs 补强 hosted file search、vector stores、included search results、metadata filtering、ranking、chunking、expiration 和成本边界，标准库最小 pipeline 实验复现了 chunk / retrieve / synthesize trace、chunk-level citations 和 unsupported question 拒答流程，Real RAG Citation Synthesis control 补强 citation id、quote matching、groundedness 和 unsupported grounded claim 的校验器失败样例，Real LlamaIndex run 补强真实框架 source-node / QueryEngine metadata plumbing 的最小观察。
- 部分验证：真实 RAG stack、OpenAI File Search / vector store、embedding、chunk size/top-k/rerank 对比、真实 LLM synthesis faithfulness、citation correctness、latency、token / storage cost、删除一致性和生产权限边界仍需实验；不能写成某个检索、托管工具或 chunk 策略默认最优。本地 verifier control 不证明真实模型引用忠实性。

## 可进入章节

- 是。可以确定写成：RAG 的动机是让生成系统能使用外部知识、处理知识更新并保留 provenance / source traceability；工程 RAG 是一条 pipeline，而不是单个 prompt 技巧。初学者应先保证加载、切分、索引、检索、回答合成、citation/source 绑定和评测可观察；使用托管 File Search / vector store 时，也要显式记录检索结果、citations、metadata filters、ranking/chunking 设置、成本和延迟。真实 embedding、rerank、hybrid retrieval、Self-RAG/agentic RAG、File Search 的质量和成本仍需要实验比较。
