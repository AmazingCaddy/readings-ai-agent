# OpenAI Agents SDK Documentation

- 来源链接：https://openai.github.io/openai-agents-python/
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；README、文档首页、guardrails、tools、tracing、human-in-the-loop 页面复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：官方文档 / 框架文档
- 主题：Agent Framework / Tool Use / Tracing
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接、README、文档首页、guardrails、tools、tracing、human-in-the-loop 关键段落已复核；结论已部分交叉验证；安全 regression set 已完成

## 一句话总结

OpenAI Agents SDK 文档适合用于解释现代 Agent SDK 的基本抽象、工具调用和 tracing。

## 核心结论

- OpenAI Agents SDK 是用于构建 agentic AI apps / multi-agent workflows 的轻量框架。
- 文档首页把 Agents 定义为 equipped with instructions and tools 的 LLMs；README 进一步列出 instructions、tools、guardrails、handoffs。
- 文档首页强调 SDK 提供 built-in agent loop，负责 tool invocation、把结果发回 LLM，并持续运行直到任务完成。
- 文档首页把 Responses API 和 Agents SDK 区分开：直接用 Responses API 时开发者自己控制 loop、tool dispatch 和 state handling；用 SDK 时 runtime 管理 turns、tool execution、guardrails、handoffs 或 sessions。
- SDK 提供 tracing，用于 visualize、debug、monitor workflows，并支持 evaluation 等后续工作。
- Guardrails 文档区分 input、output 和 tool guardrails；tool guardrails 可在 custom function-tool 调用前后验证或阻断工具调用。
- Guardrails 文档说明 blocking input guardrails 可以在 agent 启动前运行，避免 token consumption 和潜在工具副作用；parallel guardrails 可能在失败前已消耗 tokens 或开始工具执行。
- Human-in-the-loop 文档说明敏感 tool calls 可以暂停 agent execution，等待人工 approve 或 reject；`needs_approval` / `require_approval` 支持 function tools、agent-as-tool、Shell/ApplyPatch、本地 MCP 和 Hosted MCP 等不同工具面。
- Tracing 文档说明 SDK 默认记录 LLM generations、tool calls、handoffs、guardrails 等 spans；同时提醒 generation/function spans 可能捕获敏感数据，可通过 `trace_include_sensitive_data` 关闭输入/输出捕获。
- Tools 文档区分 hosted tools、local/runtime tools、function tools、agent-as-tool 和 Codex tool；local runtime tools 仍由应用或配置环境执行。

## 支撑证据

- 文档首页和 GitHub README 均返回 HTTP 200。
- 文档首页写明 SDK 的 primitives 包括 Agents、Agents as tools / Handoffs、Guardrails，并说明 tracing 可用于 visualize and debug agentic flows。
- 文档首页 features 写明 Agent loop handles tool invocation, sends results back to the LLM, and continues until the task is complete。
- 文档首页建议短生命周期、主要返回模型响应的 workflow 可直接用 Responses API；需要 runtime 管理 turns、tool execution、guardrails、handoffs、sessions 时使用 Agents SDK。
- README core concepts 写明 Tools let agents take actions，Guardrails 是 input/output validation safety checks，Human in the loop 支持跨 agent runs 让人参与。
- `guardrails.md` 写明 tool guardrails wrap function tools and let you validate or block tool calls before and after execution。
- `guardrails.md` 写明 blocking execution 在 guardrail tripwire 触发时 agent never executes，可防止 token consumption 和 tool execution。
- `human_in_the_loop.md` 写明 HITL flow pauses agent execution until a person approves or rejects sensitive tool calls；pending approvals surface as interruptions and RunState can serialize/resume runs。
- `human_in_the_loop.md` 写明 `needs_approval` 可用于 function_tool、Agent.as_tool、ShellTool、ApplyPatchTool；本地/Hosted MCP 也有 require_approval / approval callback 机制。
- `tracing.md` 写明默认 tracing 包含 Runner run、agent_span、generation_span、function_span、guardrail_span、handoff_span。
- `tracing.md` 写明 generation_span 和 function_span 可能包含敏感数据，可通过 RunConfig.trace_include_sensitive_data 或环境变量控制。

## 可能的问题

- Agents SDK 是 OpenAI Python SDK 生态中的具体实现，不是所有 Agent 框架的通用标准。
- Guardrails 和 approvals 是工程控制机制，但仍需按具体工具、数据和权限模型做本地安全测试。
- Tool guardrails 不覆盖所有工具类型；文档明确 hosted tools、built-in execution tools、handoffs 等不走同一 tool-guardrail pipeline，需要单独处理。
- Tracing 默认可能包含敏感输入输出，生产系统需要显式配置脱敏、保留期限和访问控制。

## 初学者阅读建议

- 先读 Tools、Guardrails 和 Human-in-the-loop 的概念段落，再看复杂 multi-agent 或 hosted tool 示例。

## 可复现实验

- 构建一个最小 tool-calling 任务，对比 Responses API 自己管理 loop 与 Agents SDK 管理 loop 的 trace、guardrails、human approval、敏感 trace 数据配置和状态管理成本。
- 已完成标准库安全 regression set，可作为后续迁移到 Agents SDK guardrails / HITL 的 case matrix：记录 `allow`、`block`、`require_approval`、false positive、false negative 和 trace secret 泄漏。当前结果不代表 Agents SDK 的真实拦截率。
- 已纳入框架能力交叉表，用于支撑“轻量 agent runtime / tool loop / tracing / guardrails / sessions”的保守定位；不代表真实横向性能结论。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 Agent runtime、tool loop、guardrails、human approval、handoffs、sessions 和 tracing 的工程抽象；不能把 OpenAI SDK 术语直接当成所有 Agent 系统的唯一通用定义。
