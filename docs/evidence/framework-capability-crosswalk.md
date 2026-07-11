# Evidence Note: 框架能力交叉表与选择边界

## 要验证的结论

Agent 框架比较应从任务难点和能力边界出发，而不是从框架名或排行榜出发。不同框架的文档可以支撑“适合学习什么抽象”的定位，但不能证明真实项目中的成本、可靠性、trace 质量、权限边界或维护复杂度。

## 资料来源

- Source 1：[OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- Source 2：[LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- Source 3：[LlamaIndex Documentation](../sources/source-cards/2026-llamaindex-docs.md)
- Source 4：[Microsoft AutoGen Documentation](../sources/source-cards/2026-autogen-docs.md)
- Source 5：[CrewAI Documentation](../sources/source-cards/2026-crewai-docs.md)
- Source 6：[Microsoft Semantic Kernel Documentation](../sources/source-cards/2026-semantic-kernel-docs.md)
- Source 7：[Hugging Face smolagents Documentation and Source](../sources/source-cards/2026-smolagents-docs.md)
- Source 8：[框架选择 Rubric Smoke Test 结果](../experiments/framework-selection-rubric/results-2026-07-11.md)
- Source 9：[Real Framework Same-Task Comparison 结果](../experiments/real-framework-same-task-comparison/results-2026-07-12.md)
- Source 10：[Real Multi-Agent Framework Validation 结果](../experiments/real-multi-agent-framework-validation/results-2026-07-12.md)

## 能力交叉表

| 框架 | 文档支撑的主轴 | 初学者适合用来学习 | 不应误读为 | 仍需真实实验 |
| --- | --- | --- | --- | --- |
| OpenAI Agents SDK | managed agent loop、tools、guardrails、handoffs、sessions、tracing | 最小 tool-calling agent、OpenAI 生态下的 trace / approval 入门 | 不等于所有 Agent 的通用定义；tool guardrails 只覆盖 `function_tool`，hosted shell approval 和 serialized state 治理需单独处理；也不自动完成权限和 eval | 真实 tool permission、HITL、trace 敏感数据、serialized state、成本/延迟 |
| smolagents | `CodeAgent` code snippets、`ToolCallingAgent` JSON/text tool calls、tool metadata、Hub/MCP tools、local/remote code execution | code action vs structured tool calling 对照、sandbox / `trust_remote_code` / Hub-MCP tool 信任边界；Real smolagents validation 已补本地 fake-model runtime surface | 不等于 code agents 默认更好；`LocalPythonExecutor` 不是 security boundary；`output_schema` 只作 informational use 且本地 run 观察到不做 runtime output validation；Hub/MCP tools 可能下载并本地执行代码；API experimental | 真实模型 `CodeAgent` / `ToolCallingAgent` 对照、Docker/E2B/Blaxel/Modal sandbox、MCP/Hub tool trust review、真实模型成本/延迟/trace |
| LangGraph | low-level orchestration runtime、state graph、durable execution、persistence、HITL、trace/debug | 状态图、可恢复 workflow、复杂分支、重试和多角色 state graph | 不等于复杂架构默认更可靠；框架术语不是通用术语；deterministic-node run 不代表真实模型协作质量 | 真实模型多角色协作、同一 workflow 的恢复、trace、错误处理和学习成本 |
| LlamaIndex | context augmentation、RAG 五阶段、Documents / Nodes、Indexes、Retrievers、Query Engines | RAG、数据接入、chunk / metadata / retrieval / query engine | 不证明某个 chunking、embedding、rerank 策略最优 | 真实 RAG citation correctness、embedding/vector store/rerank、latency/cost |
| AutoGen | AgentChat、single/multi-agent apps、Agents、Teams、Selector Group Chat、Swarm、Magentic-One、GraphFlow、logging/tracing | 多 Agent 对话、团队协调、角色协作、workflow-shaped agent graph | 不证明多 Agent 默认优于 workflow 或单 Agent；fake-model run 不代表真实模型协作质量；tracing/logging 入口不等于生产审计完整覆盖 | 真实模型成本、冲突处理、trace 可读性、最终责任边界 |
| CrewAI | Flows 管理 state/control execution；Crews 作为 Flow 内 agent teams；First Flow 组合 regular code、direct LLM calls 和 crew-based processing；First Crew 使用 JSON-first agents/tasks/crew 配置 | Flow + Crew 的多 Agent workflow 抽象、JSON-first crew/task/context 组织方式 | 不应引用 enterprise-ready / production-ready / security-focused / cost-efficient 等营销式效果；JSON crew project 可加载本地 Python，配置也是执行面；当前 source card 可信度为 B；fake-model run 不代表真实模型协作质量 | 与 AutoGen / LangGraph 真实模型同任务比较、成本、调试、失败恢复和配置执行安全 |
| Semantic Kernel | enterprise middleware、plugins/functions、native/OpenAPI/MCP plugins、task automation function invocation filter、agent framework、HITL、process orchestration | 企业插件集成、OpenAPI/MCP plugin、task automation approval 实现模式 | 不等于入门首选；function invocation filter 不等于完整审批状态机；Process Framework 当前 experimental，且当前入口为 `frameworks/process/process-framework` | 插件权限、HITL、MCP/OpenAPI 集成复杂度、process 稳定性 |

## 交叉验证结果

- 一致点：所有框架文档都支撑“框架是工程抽象”，但它们抽象的主轴不同。OpenAI Agents SDK 偏轻量 runtime，smolagents 偏 code action / structured tool-calling 对照和代码执行安全边界，LangGraph 偏状态编排，LlamaIndex 偏数据/RAG，AutoGen 和 CrewAI 偏多 Agent 协作，Semantic Kernel 偏企业插件和业务流程集成。
- 一致点：第 10 章的比较维度应覆盖控制流、状态、工具、RAG/memory、multi-agent、observability、权限/审批和部署治理。
- 一致点：rubric smoke test 显示，同一个框架会因任务画像不同而成为 top choice 或低分项；低分不代表框架差，只代表任务不匹配。
- 一致点：Real Framework Same-Task Comparison 显示，同一个“退款政策检索 + 审批退款”任务在 OpenAI Agents SDK、LangGraph、LlamaIndex 和 Semantic Kernel 中可以跑通，但每个 adapter 的框架原生能力不同：OpenAI Agents SDK 主要提供 `FunctionTool` schema、`needs_approval` metadata、tool argument validation、direct `ToolContext` invocation 和 fake-model `Runner` approval / resume loop；LangGraph 主要提供 state graph / conditional routing；LlamaIndex 主要提供 retriever / source-node metadata；Semantic Kernel 主要提供 plugin catalog / kernel function metadata / `Kernel.invoke()`。Agents SDK 2026-07-12 文档复核进一步说明 function-tool guardrail、hosted shell approval 和 serialized RunState 是不同边界。审批 policy、side effect、trace redaction、state storage 和部分 retrieval / trust filter 仍是应用层代码。
- 一致点：2026-07-12 AutoGen/CrewAI 文档复核补强了本地 runtime 观察之外的官方抽象边界：AutoGen AgentChat `_sources` Markdown 明确列出 Selector Group Chat、Swarm、Magentic-One、GraphFlow、Memory、Logging、Serialize Components 和 Tracing；CrewAI Introduction / First Flow / First Crew Markdown 明确 Flow-first、regular code + direct LLM calls + crew-based processing、JSON-first crew 配置、task context 和本地 Python 执行风险。
- 一致点：2026-07-12 smolagents 文档复核补强了 code-action 框架样本：`CodeAgent` 把 actions 写成 Python code snippets，`ToolCallingAgent` 使用 JSON/text tool calls；Secure Code Execution 和 README 明确本地 LLM-generated code 有风险，`LocalPythonExecutor` 不是安全边界，远程/容器 sandbox 与 whole-agent sandbox 有不同 state/secret/multi-agent 取舍；Tools reference 明确 Hub/MCP tools、`trust_remote_code` 和 `output_schema` 的信任/验证边界。Real smolagents validation 进一步用 `smolagents==1.26.0` 观察到 fake-model `CodeAgent` / `ToolCallingAgent` 可跑通同一 toy tools，`output_schema` 不做 runtime output validation，默认 local executor 会阻断未授权 `import os`。
- 一致点：Real Multi-Agent Framework Validation 显示，同一个 researcher/reviewer 缺证据复核任务可以用 AutoGen AgentChat 的 `AssistantAgent` + `RoundRobinGroupChat` + `TextMentionTermination`、CrewAI 的 `Agent` + `Task` + `Crew(process=sequential)` 和 LangGraph 的 `StateGraph` + node functions + conditional edges 表达。三者都能产生可检查 transcript / task output / state trace，但 fake model response、deterministic node behavior、evidence policy、missing-evidence rubric 和 trace redaction 仍是应用层代码。
- 边界：框架文档主要证明“提供哪些抽象”，不能证明真实实现中的速度、成本、稳定性、权限覆盖、sandbox isolation 或可维护性。
- 边界：CrewAI source card 可信度为 B，适合作为生态对照；其产品化 claim 不能作为生产可靠性、安全或成本结论。Semantic Kernel Process Framework 标注 experimental，只能写成方向性参考；旧 `frameworks/process/` 路径已返回 404，正文应使用当前 `frameworks/process/process-framework` 入口。
- 边界：多 Agent 和企业集成容易增加学习成本、依赖复杂度和调试难度，需要在真实任务中记录 trace、成本、失败恢复和人工确认，而不是只看 demo。

## 使用方式

初学者可以按任务难点先做粗选：

- 只想理解工具调用和 trace：先看轻量 SDK。
- 任务需要可恢复状态、分支和审批：看 workflow / graph runtime。
- 主要难点是文档和知识库：看 RAG / data framework。
- 学习角色协作：先用受控流程包住 multi-agent，而不是直接堆角色。
- 企业插件、OpenAPI/MCP 和业务流程集成是主难点：再看企业集成框架。

## 实验验证

- 是否需要实验：是
- 已完成：标准库 framework-selection rubric smoke test。它验证任务画像、能力标签、missing required 和 cautions 的记录方式。
- 已完成：Real Framework Same-Task Comparison 用同一个本地任务跑通 OpenAI Agents SDK、LangGraph、LlamaIndex 和 Semantic Kernel adapter，并记录 framework-owned / application-owned capabilities、case 结果和 trace 脱敏；OpenAI Agents SDK adapter 覆盖 direct `FunctionTool` / `ToolContext` 和 fake-model `Runner` approval interruption / `RunState.approve()` resume。
- 已完成：Real Multi-Agent Framework Validation 用同一个本地缺证据复核任务跑通 AutoGen AgentChat、CrewAI 和 LangGraph adapter，并记录 framework-owned / application-owned capabilities、transcript / task output / state trace、缺证据暴露和 trace 脱敏。
- 仍缺：真实模型、smolagents `CodeAgent` / `ToolCallingAgent` 同任务对照、OpenAI Agents SDK hosted tracing / 真实 approval UI、serialized RunState 存储治理、部署式恢复、OpenAPI/MCP plugin、Hub/MCP tool trust review、sandbox isolation、实现时间、LOC、token/latency/cost 和维护复杂度的完整横向比较。

## 结论状态

- 可入正文：窄结论“框架比较应从任务难点、能力边界和约束出发，而不是从框架名、流行度或排行榜出发”已完成第一轮交叉验证。框架 source cards 支撑各自主轴定位；rubric smoke test 支撑任务画像式比较方法，并明确低分只表示任务不匹配，不表示框架差；Real Framework Same-Task Comparison 和 Real Multi-Agent Framework Validation 进一步支撑同任务 run 应拆分框架原生能力和应用层治理能力。
- 部分验证：本地同任务 run 不含模型、成本、延迟、hosted tracing、真实 HITL UI 或生产部署，因此不能写成“某个框架默认最好”，也不能断言真实 tracing、permission、HITL、RAG citation、tool error recovery、deployment、latency、token cost 或维护复杂度表现。

## 可进入章节

- 是。可以作为第 10 章的框架定位表和选型方法依据。正文可以确定写：框架定位和比较维度应服务于任务画像；框架排名不能写。真实项目选择必须回到任务、团队、权限、trace、成本和维护约束。
