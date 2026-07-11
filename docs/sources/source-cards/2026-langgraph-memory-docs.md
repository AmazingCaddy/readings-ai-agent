# LangGraph Memory Documentation

- 来源链接：https://docs.langchain.com/oss/python/concepts/memory
- 作者 / 机构：LangChain
- 发布时间：持续更新文档；页面 last-modified 复核为 2026-07-11
- 最后复核日期：2026-07-12
- 类型：框架文档
- 主题：Short-term Memory / Long-term Memory / Stateful Agents
- 适合阶段：入门后 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接、canonical 迁移、HTTP metadata 和 Markdown 已于 2026-07-12 复核；关键段落已精读；RAG / Memory 术语边界、短期/长期记忆边界和长期记忆治理窄边界可入正文；本地 LangGraph `InMemoryStore` run 已完成；真实 memory framework 质量和生产行为仍部分验证

## 一句话总结

LangGraph memory 文档适合用于解释工程框架中短期记忆、长期记忆和 stateful agent 的边界。

## 核心结论

- 文档将 memory 定义为记住 previous interactions 的系统，并说明它可让 agents 记住过往交互、从反馈中学习、适应用户偏好。
- 文档按 recall scope 区分两类 memory：short-term memory / thread-scoped memory 和 long-term memory。
- Short-term memory 维护单个 thread / conversation 中的 message history，是 agent state 的一部分，并通过 checkpointer 持久化，便于 thread 恢复。
- Long-term memory 跨 conversations 或 sessions 保存 user-specific 或 application-level data，可在任意 thread 中召回，并通过 custom namespace 组织。
- 文档强调 long-term memory 是复杂问题，没有 one-size-fits-all solution，并提出 semantic、episodic、procedural memory 类型。
- 文档说明 memory 写入可发生在 hot path 或 background，两种方式在 latency、透明度、复杂度和时效性上有不同权衡。
- 文档进一步区分 semantic memory 的 profile 和 collection 两种管理方式：profile 需要持续更新同一 JSON 文档，collection 更易新增但会把 delete/update 和 search 复杂度转移到应用和 store。
- 文档说明 long-term memory 以 JSON documents 存在 store 中，用 custom `namespace` 和 `key` 组织；`InMemoryStore` 示例明确提示生产使用应替换为 DB-backed store。

## 支撑证据

- 旧链接 `https://langchain-ai.github.io/langgraph/concepts/memory/` 于 2026-07-12 返回 HTTP 200；响应头 `last-modified: Fri, 03 Jul 2026 22:45:44 GMT`，内容指向迁移后的 docs 入口。
- 2026-07-12 抓取 `https://docs.langchain.com/oss/python/concepts/memory` 返回 HTTP 200；响应头 `last-modified: Sat, 11 Jul 2026 19:12:42 GMT`。
- 2026-07-12 抓取 `https://docs.langchain.com/oss/python/concepts/memory.md` 成功；页面包含 short-term memory、long-term memory、semantic/episodic/procedural memory、profile / collection、writing memories、hot path / background 和 memory storage 段落。
- Markdown 写明 short-term memory 是 thread-scoped、作为 agent state 的一部分并通过 checkpointer 持久化；long-term memory 跨 sessions / threads，保存于 custom namespaces，并可任意 thread 中召回。
- Markdown 写明 long-term memory has no one-size-fits-all solution；profile 更新容易随文档变大而 error-prone，collection 会增加 delete / update / search 复杂度，模型可能 over-inserting 或 over-updating。
- Markdown 的 `InMemoryStore` 示例明确注释：`InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production use.`
- 已与 MemoryBank、MemGPT、Letta、Zep、OWASP/NIST 和标准库 memory governance / lifecycle audit 实验交叉验证长期记忆治理边界；long-term memory 的 one-size-fits-all 风险和 hot path / background 写入权衡支持保守正文写法。
- 2026-07-12 运行 Real LangGraph Memory Store Validation：使用 LangGraph `InMemoryStore` 跑通 namespace、`put`、`get`、`search`、`delete`、应用层 invalidated history wrapper 和 trace 脱敏；结果 `all_passed=true`、`cross_user_broad_prefix_seen=true`、`deleted_item_recalled=false`、`secret_leaked_in_trace=false`。

## 可能的问题

- LangGraph 的 memory 分类和接口属于框架抽象，需要和其他资料交叉验证。
- 文档中的 memory store 和 namespace 是 LangGraph/LangChain 实现抽象，不应被写成所有 Agent 系统的通用实现要求。
- 本地 `InMemoryStore` run 显示 broad prefix search 可看到多个 user namespace；跨用户授权、敏感过滤、编辑历史、合规删除和 trace 脱敏不能写成 store 默认自动保证。

## 初学者阅读建议

- 适合在学习 Agent 架构和 state 之后阅读，用来理解 memory 如何落地到框架。

## 可复现实验

- 已完成本地 `InMemoryStore` namespace / put / get / search / delete harness。
- 后续仍需用同一任务比较 thread-local short-term memory 和跨会话 long-term memory 的行为差异。

## 是否进入正文

- 结论：进入；术语边界可入正文
- 原因：Memory 章节需要现代框架文档支撑短期/长期记忆边界和写入治理权衡；本地 `InMemoryStore` run 可支撑 store 原语和应用层 namespace/删除/历史包装的窄观察；真实 memory framework 的收益、污染、用户编辑/删除 UI、权限、持久化和生产行为仍需实验。
