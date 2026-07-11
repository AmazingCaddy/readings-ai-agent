# OpenAI Agents SDK Documentation

- 来源链接：https://openai.github.io/openai-agents-python/
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；README 和文档首页复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：官方文档 / 框架文档
- 主题：Agent Framework / Tool Use / Tracing
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接、README 和文档首页关键段落已复核；结论已部分交叉验证

## 一句话总结

OpenAI Agents SDK 文档适合用于解释现代 Agent SDK 的基本抽象、工具调用和 tracing。

## 核心结论

- OpenAI Agents SDK 是用于构建 agentic AI apps / multi-agent workflows 的轻量框架。
- 文档首页把 Agents 定义为 equipped with instructions and tools 的 LLMs；README 进一步列出 instructions、tools、guardrails、handoffs。
- 文档首页强调 SDK 提供 built-in agent loop，负责 tool invocation、把结果发回 LLM，并持续运行直到任务完成。
- 文档首页把 Responses API 和 Agents SDK 区分开：直接用 Responses API 时开发者自己控制 loop、tool dispatch 和 state handling；用 SDK 时 runtime 管理 turns、tool execution、guardrails、handoffs 或 sessions。
- SDK 提供 tracing，用于 visualize、debug、monitor workflows，并支持 evaluation 等后续工作。

## 支撑证据

- 文档首页和 GitHub README 均返回 HTTP 200。
- 文档首页写明 SDK 的 primitives 包括 Agents、Agents as tools / Handoffs、Guardrails，并说明 tracing 可用于 visualize and debug agentic flows。
- 文档首页 features 写明 Agent loop handles tool invocation, sends results back to the LLM, and continues until the task is complete。
- 文档首页建议短生命周期、主要返回模型响应的 workflow 可直接用 Responses API；需要 runtime 管理 turns、tool execution、guardrails、handoffs、sessions 时使用 Agents SDK。
- README core concepts 写明 Tools let agents take actions，Guardrails 是 input/output validation safety checks，Human in the loop 支持跨 agent runs 让人参与。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 Agent runtime、tool loop、guardrails、handoffs、sessions 和 tracing 的工程抽象；不能把 OpenAI SDK 术语直接当成所有 Agent 系统的唯一通用定义。
