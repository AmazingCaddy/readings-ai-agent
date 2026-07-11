# LangGraph Memory Documentation

- 来源链接：https://docs.langchain.com/oss/python/concepts/memory
- 作者 / 机构：LangChain
- 发布时间：持续更新文档；页面 last-modified 复核为 2026-07-03
- 最后复核日期：2026-07-11
- 类型：框架文档
- 主题：Short-term Memory / Long-term Memory / Stateful Agents
- 适合阶段：入门后 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接和 canonical 迁移已复核；关键段落已精读；RAG / Memory 术语边界、短期/长期记忆边界和长期记忆治理窄边界可入正文；真实 memory framework 行为仍部分验证

## 一句话总结

LangGraph memory 文档适合用于解释工程框架中短期记忆、长期记忆和 stateful agent 的边界。

## 核心结论

- 文档将 memory 定义为记住 previous interactions 的系统，并说明它可让 agents 记住过往交互、从反馈中学习、适应用户偏好。
- 文档按 recall scope 区分两类 memory：short-term memory / thread-scoped memory 和 long-term memory。
- Short-term memory 维护单个 thread / conversation 中的 message history，是 agent state 的一部分，并通过 checkpointer 持久化，便于 thread 恢复。
- Long-term memory 跨 conversations 或 sessions 保存 user-specific 或 application-level data，可在任意 thread 中召回，并通过 custom namespace 组织。
- 文档强调 long-term memory 是复杂问题，没有 one-size-fits-all solution，并提出 semantic、episodic、procedural memory 类型。
- 文档说明 memory 写入可发生在 hot path 或 background，两种方式在 latency、透明度、复杂度和时效性上有不同权衡。

## 支撑证据

- 旧链接 `https://langchain-ai.github.io/langgraph/concepts/memory/` 重定向到 `https://docs.langchain.com/oss/python/langgraph/memory`，页面 canonical 指向 `https://docs.langchain.com/oss/python/concepts/memory`。
- 2026-07-11 抓取 `https://docs.langchain.com/oss/python/concepts/memory.md` 成功；页面包含 short-term memory、long-term memory、semantic/episodic/procedural memory 和 writing memories 段落。
- 已与 MemoryBank、MemGPT、Letta、Zep、OWASP/NIST 和标准库 memory governance / lifecycle audit 实验交叉验证长期记忆治理边界；long-term memory 的 one-size-fits-all 风险和 hot path / background 写入权衡支持保守正文写法。

## 可能的问题

- LangGraph 的 memory 分类和接口属于框架抽象，需要和其他资料交叉验证。
- 文档中的 memory store 和 namespace 是 LangGraph/LangChain 实现抽象，不应被写成所有 Agent 系统的通用实现要求。

## 初学者阅读建议

- 适合在学习 Agent 架构和 state 之后阅读，用来理解 memory 如何落地到框架。

## 可复现实验

- 用同一任务比较 thread-local short-term memory 和跨会话 long-term memory 的行为差异。

## 是否进入正文

- 结论：进入；术语边界可入正文
- 原因：Memory 章节需要现代框架文档支撑短期/长期记忆边界和写入治理权衡；真实 memory framework 的收益、污染、用户编辑/删除和权限行为仍需实验。
