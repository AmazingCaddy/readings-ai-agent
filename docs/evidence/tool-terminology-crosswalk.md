# Evidence Note: Tool / Function / Plugin 术语对照边界

## 要验证的结论

不同 Agent 框架都会提供“让模型或 Agent 使用外部能力”的抽象，但 `tool`、`function`、`plugin`、`handoff`、`agent-as-tool`、`retriever`、`query engine`、`Flow` 和 `Crew` 等术语不能直接互换。初学者应先看执行边界：谁生成调用请求、谁校验参数、谁执行代码、谁保存状态、谁处理权限和 trace。

## 资料来源

- Source 1：[OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- Source 2：[OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- Source 3：[LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- Source 4：[LlamaIndex Documentation](../sources/source-cards/2026-llamaindex-docs.md)
- Source 5：[Microsoft AutoGen Documentation](../sources/source-cards/2026-autogen-docs.md)
- Source 6：[CrewAI Documentation](../sources/source-cards/2026-crewai-docs.md)
- Source 7：[Microsoft Semantic Kernel Documentation](../sources/source-cards/2026-semantic-kernel-docs.md)
- Source 8：[Evidence Note: Tool Use 与 Function Calling 边界](tool-use-function-calling-boundary.md)
- Source 9：[Evidence Note: 框架能力交叉表与选择边界](framework-capability-crosswalk.md)

## 术语对照

| 来源 | 相关术语 | 可保守写入正文的边界 | 不应误读为 |
| --- | --- | --- | --- |
| OpenAI Function Calling / Responses API | tool calling、function calling、function tool、tool call output | API 层结构化协作接口；模型生成工具调用请求，应用侧执行并回传结果 | 模型自己执行函数；完整 Agent runtime |
| OpenAI Agents SDK | tools、function tools、hosted tools、local/runtime tools、agent-as-tool、handoffs、guardrails、HITL、tracing | SDK runtime 可管理 agent loop、工具执行、guardrails、handoffs、sessions 和 tracing | 所有工具类型共享同一 guardrail / approval 行为；自动完成安全和 eval |
| LangGraph | state graph、node、edge、stateful workflow or agent、durable execution、persistence、HITL | 低层 orchestration runtime，用状态和转移组织 workflow / agent | `tool` 术语与 OpenAI API 一一对应；状态图默认更可靠 |
| LlamaIndex | Documents、Nodes、Indexes、Retrievers、Query Engines、context augmentation、RAG pipeline | 数据 / RAG 框架抽象，重点是 loading、indexing、retrieval、response synthesis 和 evaluation | retriever/query engine 等同于通用 Agent tool；某个检索策略默认最优 |
| AutoGen | AgentChat、Agents、Teams、Group Chat、Swarm、GraphFlow、logging/tracing | 多 Agent 应用和协作模式抽象，强调团队、对话和协调机制 | 多 Agent 默认优于 workflow 或单 Agent |
| CrewAI | Flows、Crews、agent teams | Flow 管理 state/control execution，Crew 是 Flow 内协作完成特定任务的 agent team | Crew 可以替代受控流程；生产应用默认从 Crew 开始 |
| Semantic Kernel | plugins、functions、native/OpenAPI/MCP plugins、task automation functions、function invocation filters、Process Framework | 企业集成中把 existing APIs 暴露给模型；task automation 往往需要 HITL approval，且可用 function invocation filter 在函数调用前请求用户同意 | plugin 等于 OpenAI function tool；function invocation filter 等于完整审批状态机；experimental Process Framework 是稳定通用能力 |

## 交叉验证结果

- 一致点：这些资料都支持“外部能力需要由应用、runtime 或框架暴露给模型 / Agent”，但它们抽象层级不同。
- 一致点：OpenAI Function Calling 和 Semantic Kernel Plugins 都明确把函数 / 插件请求连接到应用代码执行；这支持“调用请求”和“执行代码”分离。
- 一致点：OpenAI Agents SDK、LangGraph、AutoGen、CrewAI 和 Semantic Kernel 都提供比单次 API 调用更高层的 runtime / orchestration / workflow 抽象，因此不能把 API 层 `function calling` 直接等同于完整 Agent 框架。
- 一致点：LlamaIndex 的 retriever / query engine 属于数据检索和问答 pipeline 的工程抽象，可作为 Agent 工具使用，但本身不等同于通用工具调用协议。
- 分歧点：同一个英文词在不同框架里粒度不同。例如 `function` 在 OpenAI API 中通常是 tool 类型，在 Semantic Kernel 中常出现在 plugin / Kernel Function 语境；`Flow` 在 CrewAI 中是产品抽象，在 LangGraph 中更接近开发者构建的状态图 / workflow 思路。
- 可能原因：API 文档关注请求 / 响应格式，Agent SDK 关注 runtime 管理，RAG 框架关注数据上下文，多 Agent 框架关注协作模式，企业集成框架关注插件和业务流程。

## 实验验证

- 是否需要实验：是。
- 已完成：本 note 完成第一轮文档交叉验证，可支撑术语边界和学习解释。
- 仍缺：同一任务在 2-3 个框架下的最小实现，对比工具定义、参数校验、错误回传、权限确认、trace 字段和恢复行为。当前 note 不证明任何框架的默认 runtime 行为。

## 结论状态

- 可入正文：窄结论“不同框架的 tool / function / plugin / retriever / flow 等术语不能直接互换；学习时应优先比较执行边界、状态边界、权限边界和 trace 边界”已完成第一轮文档交叉验证。
- 部分验证：真实框架默认错误处理、重试策略、权限覆盖、HITL、trace 字段、成本和延迟仍需同任务实验。不能写成某个框架术语更标准，也不能把一个框架的术语当成行业通用定义。

## 可进入章节

- 是。可以作为第 03 章的术语对照补充、第 10 章框架比较方法和 validation backlog 中“跨框架术语差异”的第一轮回答。正文应保持保守：术语对照帮助学习，不替代真实框架试跑。
