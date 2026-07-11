# LangGraph Documentation

- 来源链接：https://docs.langchain.com/oss/python/langgraph/overview
- 关键页面：https://docs.langchain.com/oss/python/langgraph/interrupts.md；https://docs.langchain.com/oss/python/langgraph/persistence.md；https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph.md
- 作者 / 机构：LangChain
- 发布时间：持续更新文档；旧入口 `https://langchain-ai.github.io/langgraph/` 已重定向到 docs.langchain.com
- 最后复核日期：2026-07-11
- 类型：框架文档
- 主题：Agent Architecture / State Graph / Orchestration
- 适合阶段：进阶 / 工程实践
- 可信度等级：A
- 是否已验证：新文档入口和 Markdown 页面已复核；关键段落已精读；Agent/Workflow、自治程度、复杂架构默认可靠性、Planner/Executor trace、HITL interrupt / persistence 边界和跨框架术语对照窄边界可入正文；Real LangGraph Interrupt Recovery harness 已在 LangGraph 1.2.9 / langchain-core 1.4.9 / `MemorySaver` 下完成最小 run；真实持久化、生产审批和跨框架行为仍部分验证

## 一句话总结

LangGraph 是理解状态图、可控 workflow-agent hybrid 和复杂任务编排的重要工程 reference。

## 核心结论

- LangGraph 文档将其定位为 low-level orchestration framework and runtime，用于 building、managing、deploying long-running, stateful agents。
- 文档明确 LangGraph focused entirely on agent orchestration，不抽象 prompts 或 architecture。
- 文档把 LangGraph 描述为支持 any long-running, stateful workflow or agent 的低层基础设施。
- 核心能力包括 durable execution、streaming、human-in-the-loop、persistence、memory 和 trace/debug 支持。
- Interrupts 页面说明 `interrupt()` 会暂停 graph execution，把 JSON-serializable payload 暴露给调用方，并通过 `Command(resume=...)` 恢复执行；恢复依赖 persistence / checkpointer 和相同 `thread_id`。
- Interrupts 页面把 approval workflow、review/edit state 和 tool 内中断作为常见模式；适合在 API 调用、数据库修改、金融交易等 critical actions 前暂停等待人类决定。
- 文档也给出明确限制：resume 时 node 会从头重新执行，`interrupt()` 前的代码会再次运行；不要在同一个 node 中重排或条件跳过 interrupt；side effects 应放在 interrupt 之后或设计为幂等。
- Persistence 页面区分 checkpointers 和 stores：checkpointer 保存 thread graph state snapshots，用于会话连续性、HITL、time travel 和 fault tolerance；store 保存跨 thread 的应用自定义数据。
- 文档说明内存型 checkpointer 不会在进程重启后保留 checkpoints；生产持久化需要 PostgresSaver、SqliteSaver 等持久化 checkpointer，并考虑长会话 checkpoint 增长和保留策略。
- 文档建议刚开始学习或需要更高层抽象时使用 LangChain agents；这支持正文中“不要一开始就追求复杂底层编排”的保守建议。
- 当前 quickstart 展示 Graph API 和 Functional API 两条入门路径；Graph API 通过 `StateGraph`、state、model node、tool node、conditional edge、compile 和 invoke 组织工具循环。

## 支撑证据

- 新文档入口和 `.md` 页面返回 HTTP 200；旧 GitHub Pages 入口返回重定向页面。
- Markdown 页面写明 LangGraph 是 low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents。
- Markdown 页面写明 LangGraph provides low-level supporting infrastructure for any long-running, stateful workflow or agent。
- Markdown 页面写明 LangGraph does not abstract prompts or architecture。
- Markdown 页面列出 persistence、human-in-the-loop、memory、debugging/trace execution paths、state transitions 等核心收益。
- Quickstart Markdown 返回 HTTP 200，并展示 calculator agent 的 tools、`MessagesState`、conditional edge 和 tool node；它可作为当前代码入口。
- Interrupts Markdown 页面返回 HTTP 200，HTTP metadata 显示 `last-modified: Fri, 10 Jul 2026 19:41:30 GMT`；旧 human-in-the-loop 路径重定向到 interrupts 页面。
- Interrupts Markdown 页面写明 interrupt pauses execution and surfaces data to caller，resume 使用 `Command(resume=...)`，并展示 `thread_id`、checkpointer、approval、review/edit 和 tool 内 interrupt 示例。
- Interrupts Markdown 页面明确列出 rules of interrupts：resume 会重新执行 node、interrupt payload 必须 JSON-serializable、不要在 broad try/except 中包住 interrupt、不要重排或条件跳过同一 node 的 interrupt，side effects before interrupt 必须幂等。
- Persistence Markdown 页面写明 checkpointers persist graph state snapshots by thread，用于 conversation continuity、human-in-the-loop、time travel 和 fault-tolerance；stores persist application-defined data across threads。
- Persistence / thinking-in-langgraph 页面共同支撑：HITL 需要编译时配置 checkpointer，human input 可以作为 first-class input 恢复 graph，user-fixable errors 可以用 `interrupt()` 暂停处理；human review node 应把 `interrupt()` 放在开头，因为恢复时前置代码会重跑。
- LangGraph examples repo 已另建 source card；该 repo 的 `examples/README.md` 明确说明 examples 目录已经归档，不再更新，应优先使用当前 docs。

## 可能的问题

- LangGraph 属于特定框架，不能把它的抽象直接当成所有 Agent 系统的通用定义。
- 需要和 OpenAI Agents SDK、AutoGen、Semantic Kernel 等框架比较。
- LangGraph 更偏底层 orchestration runtime；初学者需要先理解 model、tool、state 和 workflow，再读复杂 API。
- 需要区分当前 docs / quickstart 与归档 examples；旧 notebooks 可帮助理解架构形态，但不能作为最新 API 指南。
- LangGraph interrupt / persistence 是框架机制证据，不证明具体业务审批流程已经安全。真实系统仍要验证审批状态、参数快照、拒绝后恢复、重复恢复、幂等执行、trace 脱敏、成本和延迟。
- `InMemorySaver` / `MemorySaver` 适合教程和进程内实验，不应被写成生产持久化方案。

## 初学者阅读建议

- 先理解 workflow、state、edge、node 的直觉，再看复杂多 agent 示例。

## 可复现实验

- 构建一个带状态持久化的两步 tool workflow，对比无状态单 Agent 的可调试性。
- Real LangGraph Interrupt Recovery harness 已完成一次临时依赖 run：LangGraph 1.2.9 / langchain-core 1.4.9 / Python 3.12.13 / `MemorySaver` / 本地假退款工具。结果覆盖 `approved_once`、`duplicate_resume`、`rejected_resume`、`tampered_args` 和 `side_effect_before_interrupt`；批准执行 1 次工具，拒绝和参数 hash 不匹配均不执行工具，重复 resume 未产生第二次执行，trace / interrupt payload 未泄露示例 secret marker。重复 resume 本次返回已完成状态而不是显式 duplicate-blocked 状态；持久化 checkpointer restart 未测试。
- 已纳入框架能力交叉表，用于支撑“state graph / durable execution / persistence / HITL / trace”的保守定位；与其他框架卡片和 rubric smoke test 共同支撑“框架应按任务难点比较，不能写成某个框架默认最好”的窄边界；不代表真实横向性能结论。
- 已纳入 Tool / Function / Plugin 术语对照 evidence，用于区分 LangGraph 的 state graph、node、edge、stateful workflow / agent 和 durable execution 抽象与 API 层 function/tool calling、RAG retriever 或多 Agent team 抽象；不代表真实 LangGraph 默认工具错误处理或权限行为。
- Agent/Workflow 和自治程度窄边界已升级为可入正文：LangGraph 文档直接支撑 long-running, stateful workflow or agent、orchestration runtime、state transitions 和 trace/debug execution paths 的工程边界。真实 LangGraph workflow / agent 表现、成本和失败恢复仍需实验。
- 复杂架构默认可靠性窄边界已升级为可入正文：LangGraph 支撑 durable execution、state、trace/debug 等工程控制能力，但这些能力是选择和验证架构的依据，不证明状态图、Agent 或更复杂编排在真实任务中默认更可靠。
- Planner/Executor 窄边界已升级为可入正文：LangGraph 支撑状态、转移、持久化和 trace/debug 的工程编排边界；标准库 planner/executor 实验补充了 validation_failed / plan_revised 的最小流程。真实 LangGraph planner/executor 实现仍需实验。
- 已补 LangGraph examples repo source card：current quickstart 补强 `StateGraph` tool loop 的代码形态，历史 plan-and-execute / human-in-the-loop notebooks 补强 planner/replan 和 interrupt/resume 的架构参考；但 examples 目录已归档，真实试跑应使用当前 docs。
- HITL interrupt / persistence 窄边界已升级为可入正文：LangGraph current docs 直接支撑 pause/resume、approval workflow、review/edit state、tool 内中断、checkpointer、thread state snapshot 和 `thread_id` 恢复边界；同时文档明确 side effects、node restart、interrupt 顺序和持久化 checkpointer 的限制。Real LangGraph Interrupt Recovery completed run 支撑一个最小 `MemorySaver` graph 的审批恢复、拒绝、参数 hash 和不重复执行观察；真实生产 HITL 安全、持久化恢复、并发恢复、真实副作用事务、默认脱敏和跨框架对比仍需实验。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 stateful workflow/agent、orchestration runtime、persistence、human-in-the-loop、interrupt/resume、trace 和跨框架术语区分的工程边界，并与 OpenAI Agents SDK/ReAct/标准库实验共同支撑 Agent/Workflow、自治程度、复杂架构默认可靠性、Planner/Executor trace 和高风险工具审批恢复窄边界；completed harness 可补充最小真实框架观察，但不能单独证明任何复杂 Agent 架构默认更好，也不能证明真实生产审批流程默认安全。
