# OpenAI File Search and Retrieval Documentation

- 来源链接：https://developers.openai.com/api/docs/guides/tools-file-search.md
- 相关链接：https://developers.openai.com/api/docs/guides/retrieval.md
- 作者 / 机构：OpenAI
- 发布时间：文档持续更新；File Search 页面 HTTP `last-modified` 为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：Official Docs / API Guide / Retrieval Engineering
- 主题：File Search / Retrieval API / Vector Stores / RAG / Citations
- 适合阶段：入门后 / RAG 实践
- 可信度等级：A
- 是否已验证：官方 Markdown 页面已抓取；File Search guide、Retrieval guide 和 File Search 页面 HTTP metadata 已复核；支撑 Responses API `file_search` hosted tool、vector stores、semantic + keyword search、`file_search_call`、file citations、`include=["file_search_call.results"]`、metadata filtering、query rewriting、ranking options、vector store attributes、expiration policies、chunking defaults/limits、supported file types、rate limits、pricing/data links 的工程边界；不证明真实 citation correctness、answer faithfulness、默认 chunking/ranking 最优、成本、延迟、权限隔离或生产可靠性

## 一句话总结

OpenAI File Search / Retrieval 文档适合把初学者从“RAG 是自己拼 prompt”带到“托管检索工具也有可观察对象和治理参数”：文件要进入 vector store，检索会产生 `file_search_call` 和 citations，结果、metadata filter、ranking、chunking、过期策略和成本都需要被记录和评估。

## 核心结论

- File Search 是 Responses API 中的 hosted tool，用于让模型在生成前从已上传文件构成的 knowledge base 中检索信息。
- 使用 File Search 前，需要创建 vector store、上传文件、把文件加入 vector store，并等待文件处理状态完成。
- File Search 调用返回多个 output item：`file_search_call` 记录搜索调用，`message` 中的 output text 可以包含 `file_citation` annotations。
- 默认情况下 `file_search_call` 不返回 search results；如需观察检索结果，需要在 Responses API 请求中使用 `include=["file_search_call.results"]`。
- `max_num_results` 可以限制返回结果数，有助于降低 token usage 和 latency，但可能牺牲 answer quality。
- File Search 支持 metadata filtering；Retrieval guide 进一步说明 vector store file attributes 可用于过滤。
- Retrieval guide 把 semantic search 解释为基于 vector embeddings 的语义相关检索，可以找到少量或没有关键词重叠的结果。
- Retrieval guide 提供 query rewriting、attribute filtering 和 ranking options；`ranking_options` 可配置 ranker、score threshold 和 hybrid search 中 embedding / text 权重。
- Vector stores 是 Retrieval API 和 File Search tool 的索引容器；添加文件后会自动 chunk、embed 和 index。
- Vector store file operations 有异步处理和 eventually consistent 边界；删除文件后 search results 短时间内仍可能包含已移除文件内容。
- Vector store 有 storage pricing、expiration policies、file size / token limits 和默认 chunking 参数；默认 chunking 使用 `max_chunk_size_tokens=800`、`chunk_overlap_tokens=400`，也可通过 `chunking_strategy` 调整。
- 对本手册而言，稳妥结论是：File Search 能降低自建 RAG pipeline 的实现负担，但不能替代检索评测、citation correctness、权限/数据治理、成本/延迟记录和失败样例回放。

## 支撑证据

- 2026-07-11 使用 `curl -L --no-progress-meter` 抓取 `tools-file-search.md` 成功，页面标题为 `File search`。
- 2026-07-11 使用 `curl -L -I` 复核 File Search 页面 URL，返回 HTTP 200，HTTP header 包含 `last-modified: Sat, 11 Jul 2026 06:08:23 GMT`。
- File Search guide 说明该工具 available in the Responses API，可通过 semantic and keyword search 检索 previously uploaded files，并通过 vector stores / knowledge bases 增强模型知识。
- File Search guide 明确这是 hosted tool managed by OpenAI；模型决定使用时会自动调用工具、从文件检索信息并返回 output。
- File Search guide 展示创建 vector store、上传文件、把 file 加入 vector store、检查状态，以及在 `tools` 中传入 `type: "file_search"` 和 `vector_store_ids` 的流程。
- File Search response 示例包含 `file_search_call` output item、`queries`、`status`，以及 assistant message 中的 `file_citation` annotations。
- File Search guide 说明默认不会返回 search results；使用 `include=["file_search_call.results"]` 才能包含检索结果。
- File Search guide 展示 `max_num_results` 和 `filters` 参数，并说明结果数量限制会影响 token usage、latency 和 answer quality。
- 2026-07-11 抓取 `retrieval.md` 成功；Retrieval guide 说明 Retrieval API 支持 semantic search，vector stores serve as indices for your data。
- Retrieval guide 说明 vector store search 默认最多 10 个结果，可设置到最多 50 个；支持 `rewrite_query=true`，并在结果中提供 rewritten `search_query`。
- Retrieval guide 说明 `attribute_filter` 可按 attributes 限制搜索范围，`ranking_options` 可调整 ranker、score threshold 和 hybrid semantic / keyword 权重。
- Retrieval guide 说明 vector stores 中的 file 会被自动 chunk、embed 和 index；vector store files 支持 attributes、expiration、limits 和 chunking strategy。
- Retrieval guide 说明 vector store storage 超过免费额度后按 GB/day 收费；expiration policies 可用于降低成本。
- Retrieval guide 说明文件删除存在 eventually consistent 边界，search results 可能短时间包含已移除文件内容。

## 可能的问题

- File Search 是 OpenAI 托管工具文档，不是 RAG 质量评测；不能证明默认检索、默认 chunking、默认 ranker 或 citations 在具体业务中正确。
- `file_citation` annotation 表示模型输出带文件引用，不等于引用文本一定支持答案，也不等于答案 faithful。
- Hosted tool 降低了实现成本，但检索结果默认不返回；如果不显式 `include` search results，调试、审计和评测会缺关键证据。
- Storage pricing、expiration、rate limits、data residency/ZDR 等需要结合当前账号、组织设置和实际用量复核。
- Vector store 删除存在 eventually consistent 边界，生产权限和删除后召回测试不能只看 API 返回的 delete 成功。

## 初学者阅读建议

- 先读本手册第 06 章，理解 RAG pipeline、chunk、retrieval trace 和 citation/source 绑定。
- 再读 File Search guide 的 How to use、File search response、Retrieval customization 和 Usage notes。
- 进阶时读 Retrieval guide 的 Semantic search、Attribute filtering、Ranking、Vector stores、Pricing、Expiration policies 和 Chunking。
- 对初学者最重要的 takeaway 是：托管 File Search 省掉了很多底层代码，但仍需要记录检索结果、引用、过滤条件、成本、延迟和失败样例。

## 可复现实验

- 用同一组 PDF/Markdown 文档建立 vector store，运行 File Search 问答，保存 `file_search_call`、included search results、citations、latency、token usage 和费用。
- 对比 `max_num_results`、metadata filters、query rewriting、score threshold、chunking strategy 和 expiration policy 对 recall、citation correctness、faithfulness、latency 和成本的影响。
- 加入过期文档、冲突文档、权限不应访问的文档、删除后立即搜索、无答案问题和 prompt injection 文档，记录检索是否命中、答案是否拒答、trace 是否足够复盘。

## 是否进入正文

- 结论：部分进入
- 原因：可作为第 06/11/12 章中“托管 File Search / vector stores 是一种 RAG 工程实现方式，仍需检索结果可观察、citation/source 校验、metadata filtering、成本/延迟记录和权限治理”的官方 reference；不能支撑 File Search 默认高质量、默认正确引用、默认低成本、默认满足生产权限或优于自建 RAG 的结论。
