# 框架生态比较

## 本章适合谁

如果你已经知道 Agent 的核心组件，但面对 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI、Semantic Kernel 等框架不知道怎么选，这一章适合阅读。

本章不做“最佳框架排行榜”。框架更新很快，初学者更应该先学会比较维度，再根据任务选择。

## 你会学到什么

- 为什么不要从框架名开始学习 Agent。
- 比较 Agent 框架时应该看哪些维度。
- 常见框架大致适合解决什么问题。
- 如何用同一个小任务评估多个框架。
- 为什么框架文档不能直接替代基础概念学习。

## 先用一句话理解

框架是把模型、工具、状态、数据、编排和可观测性组织起来的工程外壳；选框架前，先明确你要控制什么。

## 基础概念

### SDK

SDK 通常提供较轻量的开发抽象，让你更方便地调用模型、定义工具、组织 agent、记录 trace。

它适合从最小 Agent 开始，逐步理解工具调用和运行过程。

### Workflow / Graph Framework

Workflow 或 graph framework 更强调状态、节点、边、条件分支、持久化和恢复。

它适合步骤较多、需要可控流程、需要重试和中断恢复的任务。

### Data / RAG Framework

Data 或 RAG framework 更强调文档接入、切分、索引、检索、reranking、query engine 和知识库治理。

如果你的 Agent 主要问题是“如何可靠使用外部知识”，这类框架通常更相关。

### Multi-agent Framework

Multi-agent framework 强调角色、协作、对话、任务分配和结果合并。

它适合研究或构建多角色任务，但初学者不应把多 Agent 作为默认起点。

### Enterprise Integration

Enterprise integration 更强调和现有系统、权限、插件、业务流程、监控和治理结合。

这类框架可能更适合企业应用，但学习曲线和环境复杂度也更高。

## 比较维度

选择框架时，可以用下面这些问题逐项比较。

### 学习成本

你能否在一天内做出一个最小可运行 demo？核心概念是否容易解释？错误信息是否清楚？

### 控制力

你能否明确控制模型输入、工具调用、状态更新、重试、人工确认和输出格式？

框架越自动，初学者越要小心：自动化能提高效率，也可能隐藏失败原因。

### 状态和编排

系统是否支持任务状态、分支、循环、中断恢复和持久化？复杂任务通常需要这些能力。

### 工具生态

工具定义是否清晰？是否容易做参数校验、权限控制和错误处理？是否能接入 MCP 或现有服务？

### RAG 和 Memory

框架是否擅长文档接入、检索、记忆写入、长期状态和知识更新？如果任务重依赖知识库，这一点比多 Agent 更重要。

### Observability

是否能看到 trace、工具调用、状态变化、成本和错误？没有可观测性，复杂 Agent 很难调试。

### 生产化边界

框架是否支持权限、审计、部署、版本管理、回滚和人类确认？如果不支持，应用层需要自己补齐。

## 常见框架的学习定位

下面是基于当前 source cards 和第一轮 evidence notes 的保守定位。关键框架定位已经完成第一轮精读，但仍不能写成“最佳框架排行榜”，因为还缺同一任务的横向实验。

框架能力交叉表把这些框架先按“主轴”粗分：OpenAI Agents SDK 偏轻量 agent runtime，LangGraph 偏状态编排，LlamaIndex 偏 RAG / data framework，AutoGen 和 CrewAI 偏多 Agent 协作，Semantic Kernel 偏企业插件和业务流程集成。这个表适合帮助初学者缩小阅读范围，但不等于性能、成本或可靠性排名。

| 任务难点 | 优先观察的框架方向 | 仍要检查什么 |
| --- | --- | --- |
| 最小工具调用、trace、handoff | 轻量 SDK / agent runtime | 工具权限、错误恢复、成本和 eval。 |
| 状态、分支、审批、恢复 | Workflow / graph runtime | 状态持久化、HITL、重试和 trace 可读性。 |
| 文档、检索、引用、知识库 | RAG / data framework | chunk metadata、citation correctness、rerank 和无证据拒答。 |
| 角色协作、多视角 review | Multi-agent framework | 协调成本、冲突处理、重复工作和最终责任边界。 |
| 企业插件、OpenAPI/MCP、流程治理 | Enterprise integration framework | 权限、审批、插件安全、部署和维护复杂度。 |

### OpenAI Agents SDK

适合作为理解现代 Agent SDK 抽象、工具调用和 tracing 的入口。它和 OpenAI API 生态结合紧密，适合先做最小 tool-calling agent。

需要注意：SDK 抽象不等于 Agent 的全部理论，也不替代权限和评测设计。

### LangGraph

适合学习状态图、workflow-agent hybrid、可控编排、持久化和复杂流程。

如果你的任务需要分支、循环、中断、重试和状态恢复，LangGraph 这类 graph 抽象很有学习价值。

当前 LangGraph interrupts / persistence 文档还适合用来学习审批和恢复的工程细节：`interrupt()` 可以暂停 graph，resume 依赖 checkpointer 和 `thread_id`；approval workflow、review/edit state 和 tool 内中断可放在关键动作前。需要注意的是，恢复时 node 会从头执行，确认点前代码可能重跑，副作用需要幂等或放在确认之后，内存型 checkpointer 不等于生产持久化。

本手册的 Real LangGraph Interrupt Recovery 最小 run 已在 LangGraph 1.2.9 和 `MemorySaver` 下跑通一个退款审批 graph：批准后执行 1 次本地假工具，拒绝和参数 hash 不匹配时不执行，重复 resume 没有造成第二次执行，trace 未泄露实验 secret marker。它还用 `langgraph-checkpoint-sqlite` 3.1.0 / `SqliteSaver` 跑通了本地 SQLite checkpoint 恢复和并发 resume case：同进程重建 graph、双本地 Python 进程恢复都能执行 1 次本地假工具；两个本地 Python resume 进程同时恢复同一暂停审批时，共享副作用日志只有 1 条记录，但两个 resume 都返回 `approved_executed`。这个结果适合说明“框架机制需要用具体 case 验证”，但仍不能说明 LangGraph 默认具备生产级审批、安全、部署式服务恢复或真实服务并发恢复能力。

需要注意：LangGraph 的术语是框架抽象，不应直接当作所有 Agent 系统的通用定义。

### LlamaIndex

适合学习 RAG、数据连接、索引、retriever、query engine 和 agent data framework。

如果你的核心问题是“让 Agent 正确使用文档和知识库”，LlamaIndex 这类 data framework 比多 Agent 框架更直接。

需要注意：RAG 的通用概念和框架实现细节要分开理解。

### AutoGen

适合学习多 Agent 对话、协作和角色化任务组织。

它适合在理解单 Agent 和编排之后阅读，用来分析多 Agent 的价值和复杂度。

AutoGen 文档已确认它提供 AgentChat、Teams、Selector Group Chat、Swarm、GraphFlow、logging 等多 Agent 协调抽象。需要注意：多 Agent 示例容易显得强大，但要评估成本、调试、失败恢复和最终决策责任。

本手册的多 Agent 标准库实验显示，无 Flow 控制的 researcher/writer/reviewer 组合会重复读取、漏掉 cost 或 beginner feedback，并留下未解决冲突；Flow 控制能恢复成功率，但会带来消息协调开销。这个实验不能证明 AutoGen 或 CrewAI 的真实表现，只用于说明选择 multi-agent framework 时应检查控制流、证据分配和 review trace。

Real Multi-Agent Framework Validation 进一步用 fake `ChatCompletionClient` 跑通了 AutoGen AgentChat 0.7.5 的 `AssistantAgent` + `RoundRobinGroupChat` + `TextMentionTermination`。它说明 AutoGen 可以提供 team scheduling、termination condition 和 message transcript 这样的 runtime surface；但缺证据判断和 trace 脱敏仍是实验代码实现，不能推出真实模型协作质量。

### CrewAI

适合作为多 Agent 工程生态的补充资料。它的文档可用于横向比较角色、任务和协作抽象。

CrewAI 文档已确认它把系统拆成 Flows 和 Crews：Flow 管理状态和执行控制，Crew 是 Flow 内协作完成特定任务的 agent team。需要注意：当前 source card 将其可信度标为 B，正文应重点用来比较抽象和适用场景，而不是引用营销式结论。

Real Multi-Agent Framework Validation 也用 fake `BaseLLM` 跑通了 CrewAI 1.15.2 的 `Agent` + `Task` + `Crew(process=sequential)`。它说明 CrewAI 可以提供 agent/task/crew 和 sequential task output surface；但 evidence policy、review rubric、模型质量、成本和生产 tracing 都没有被验证。

### Semantic Kernel

适合理解企业应用中模型、插件、工具和编排集成，尤其是 Microsoft 生态内的实践。

Semantic Kernel 文档已确认它把自身定位为 lightweight open-source development kit 和 enterprise-grade middleware。Plugins 页面支持 native code、OpenAPI specification 和 MCP Server 三种 plugin 导入方式，并强调 retrieval functions 和 task automation functions 的使用边界。Agent Framework 页面支持 agents、human inputs、multi-agent collaboration 和 process orchestration。

Real Semantic Kernel Plugin Validation 已跑通 Python 1.36.0 的 native plugin 最小 runtime：`@kernel_function` 暴露 plugin/function/parameter metadata，`Kernel.invoke()` 会拒绝缺少 required 参数和不可解析类型，可解析字符串数值会被转换后执行；未审批写函数由应用层 wrapper 阻断且不转发给 kernel。这个结果只能支撑 native plugin/function 的窄边界，不能代表 OpenAPI/MCP plugin、Agent Framework、Process Framework、HITL UI 或真实模型 tool selection。

需要注意：Process Framework 当前标注为 experimental。企业集成概念较多，初学者应先掌握工具调用、状态和编排，再读复杂集成文档。

## 通俗例子

假设你要做“读取公司 FAQ，并在必要时查询订单系统”的客服 Agent。

如果你主要想学习最小工具调用，可以从 SDK 开始。

如果你最难的是文档检索质量，可以优先看 RAG/data framework。

如果流程包含多个状态、审批和失败恢复，可以看 graph/workflow framework。

如果任务天然需要多个角色协作，例如 researcher、writer、reviewer，再考虑 multi-agent framework。

同一个任务可以用不同框架完成。比较时不要只看代码行数，还要看 trace 是否清楚、失败是否容易定位、权限是否可控、后续维护是否简单。

本手册的 Real Framework Same-Task Comparison 用同一个“退款政策检索 + 审批退款”本地任务跑通了 OpenAI Agents SDK、LangGraph、LlamaIndex 和 Semantic Kernel：OpenAI Agents SDK 主要提供 `FunctionTool` schema、`needs_approval` metadata、tool argument validation、direct `ToolContext` invocation，以及 fake-model `Runner` approval / resume loop，LangGraph 主要提供 `StateGraph`、节点和条件路由，LlamaIndex 主要提供 `VectorStoreIndex`、retriever 和 source-node metadata，Semantic Kernel 主要提供 plugin catalog、kernel function metadata 和 `Kernel.invoke()`。同一个任务虽然都能跑通，但审批 policy、side effect、trace redaction，以及部分检索 / trust filter，仍是应用层代码。初学者比较框架时，应先问“这一步是框架帮我做的，还是我自己写的？”

## 工程实践

### 用同一个小任务比较框架

设计一个固定任务，例如：用户提出问题，系统检索文档，必要时调用一个查询工具，最后输出带来源的答案。

在真正写代码前，可以先做任务画像：哪些能力是必需的，哪些只是加分项，哪些抽象反而会增加学习成本。本手册的框架选择 rubric smoke test 用 5 个任务画像比较了轻量 tool agent、RAG 问答、审批 workflow、多角色 review 和企业插件集成。它能说明任务难点会把选择方向推向不同框架，但它不运行真实框架，不能证明任何框架真实更快、更便宜或更可靠。Real Framework Same-Task Comparison 则提供了一个窄口径真实 runtime 对照：同一任务要记录 framework-owned capabilities 和 application-owned capabilities，避免把应用层写的权限、redaction 或 side effect 误当成框架默认能力。该实验中的 OpenAI Agents SDK adapter 已运行 fake-model `Runner` approval / resume loop，但尚未运行真实模型、hosted tracing 或生产审批 UI。

同样，Real Multi-Agent Framework Validation 提供的是 multi-agent runtime surface 对照，不是质量对照。它可以帮助你检查 transcript、task output、终止条件和角色边界是否清楚；不能替代真实模型、多轮冲突合并、token/latency/cost 和人工复核实验。

用不同框架实现同一任务，记录这些指标：

- 完成最小 demo 的时间。
- 工具 schema 是否清晰。
- 错误处理是否自然。
- trace 是否容易阅读。
- 状态是否容易恢复。
- 增加人工确认是否方便。
- 加入 eval 是否方便。

### 先掌握底层概念

不要把框架教程当成 Agent 概念本身。先理解 tool use、RAG、memory、planning、eval、security，再看框架如何封装这些概念。

### 避免过早框架锁定

早期学习项目可以选择简单工具，但不要把所有章节都绑定到一个框架。手册的目标是建立可迁移知识。

### 记录版本和复核日期

框架文档变化很快。引用时应该记录复核日期，避免读者拿旧抽象理解新版本。

## 常见误区

- 误区一：最流行的框架就是最适合自己的框架。任务边界比流行度更重要。
- 误区二：框架能自动解决 Agent 安全问题。权限、审计和 eval 仍需要系统设计。
- 误区三：多 Agent 框架适合所有复杂任务。很多任务更需要 workflow、RAG 或回归测试。
- 误区四：示例跑通就代表可生产。示例通常没有覆盖权限、成本、失败恢复和审计。
- 误区五：框架抽象就是行业标准术语。框架术语需要和通用概念区分。

## 已验证结论

- OpenAI Agents SDK、LangGraph、AutoGen 均已完成关键段落第一轮精读，可支撑 SDK runtime、orchestration runtime 和多 Agent 协调抽象的保守表述。
- CrewAI source card 当前可信度为 B，但其 Introduction Markdown 可作为 Flows / Crews 抽象的补充证据；不宜单独支撑关键结论或营销式效果判断。
- LangGraph source card 明确其适合状态图、可控 workflow 和复杂任务编排；interrupts / persistence 文档补强了 pause/resume、checkpointer、`thread_id` 和 side-effect idempotency 边界；Real LangGraph Interrupt Recovery harness 已完成 `MemorySaver` 最小 run 和 `SqliteSaver` 本地 SQLite 同进程 graph 重建恢复 case、双本地 Python 进程 prepare/resume case 和双本地 Python 进程并发 resume case。LangGraph 是特定框架，不应被写成通用定义，也不证明真实生产审批流程默认安全。
- 多 Agent 框架适合学习角色协作和任务分配，但“多 Agent 默认更好”没有被框架文档证明。“多 Agent 不是复杂任务默认升级路径；引入前应明确角色边界、证据分配、冲突处理、review trace 和成本预算”已升级为可入正文。标准库多 Agent 对比实验已验证无控制角色协作会带来重复读取、缺证据和冲突风险；Real Multi-Agent Framework Validation 已补 AutoGen AgentChat / CrewAI 的本地 fake-model runtime surface 观察。真实模型、多轮冲突合并、成本、延迟、trace 可读性和成功率仍需同任务对比验证。
- LlamaIndex source card 明确其适合 RAG、数据连接、索引和 agent data framework；需区分通用 RAG 概念和框架实现。
- Semantic Kernel source card 已完成第一轮精读，可支撑 enterprise integration、plugins/functions、native/OpenAPI/MCP plugin 导入、agent framework、human-in-the-loop 和 process orchestration 的框架定位；Real Semantic Kernel Plugin Validation 已补 native plugin runtime 的 metadata、参数处理和应用层审批 wrapper 观察；其 Process Framework 当前仍标注 experimental。
- “Agent 框架应按任务难点和能力边界比较，不应写成某个框架默认最好”已升级为可入正文：框架生态定位边界、框架能力交叉表和标准库 rubric smoke test 支撑各框架适合解决不同工程难点，任务画像应记录 required、nice-to-have、avoid、missing required 和 cautions；Real Framework Same-Task Comparison 和 Real Multi-Agent Framework Validation 进一步支撑同任务 run 应拆分 framework-owned capabilities 和 application-owned capabilities；但不能从文档、rubric 或本地 fake-model run 直接推出真实成本、可靠性或性能排名，也不能把 fake-model Agents SDK `Runner`、AutoGen team loop 或 CrewAI sequential crew 行为等同于真实模型、hosted tracing 或生产审批 UI。
- 框架能力交叉表已把 6 个常见框架的主轴、适合学习内容、不应误读点和真实实验缺口整理到 evidence note；它支撑本章的定位表，但仍不能替代真实框架横向实验。
- Tool / Function / Plugin 术语对照已完成第一轮文档交叉验证，可支撑“框架术语不能直接当成行业通用定义”的保守表述。OpenAI API 的 function/tool calling、OpenAI Agents SDK 的 runtime tools / agent-as-tool、Semantic Kernel 的 plugins/functions、LlamaIndex 的 retriever/query engine、LangGraph 的 state graph、AutoGen/CrewAI 的 multi-agent / Flow 抽象处在不同层级；Semantic Kernel native plugin 已有本地 runtime 观察，但真实框架默认错误处理、权限、HITL、trace 和成本仍需同任务实验。

## 待验证问题

- 各框架的 tracing 和 observability 能力如何实际比较？
- 哪些框架更容易实现权限隔离和人工确认？LangGraph 文档机制已补 interrupt / persistence 边界，Real LangGraph Interrupt Recovery 已完成一个最小真实框架 run、本地 SQLite 同进程恢复、双本地 Python 进程恢复和双本地 Python 进程并发 resume case；Real Framework Same-Task Comparison 已补一个本地同任务 runtime 对照，但审批 policy 多数仍是应用层代码；仍需真实同任务对比 OpenAI Agents SDK、LangGraph、Semantic Kernel、MCP 等工具面的审批状态、参数快照、部署式服务恢复、真实服务并发恢复、幂等执行和 trace 脱敏。
- 同一任务在不同真实框架下的成本、延迟和可调试性差异有多大？
- 框架版本演进是否改变了核心抽象？
- 如何为初学者设计不被框架绑定的实践项目？

## 本章小结

- 选框架前，先明确任务的核心难点。
- SDK、graph/workflow、RAG/data、multi-agent、enterprise integration 各有侧重。
- 比较框架时要看控制力、状态、工具、RAG/memory、observability 和生产化边界。
- 初学者应先学底层概念，再用框架提高工程效率。
- 框架文档适合做 reference，但关键结论仍需要精读和交叉验证。

## References

### Framework Docs

- [OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- [LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- [Real LangGraph Interrupt Recovery](../experiments/real-langgraph-interrupt-recovery/README.md)
- [LlamaIndex Documentation](../sources/source-cards/2026-llamaindex-docs.md)
- [Microsoft AutoGen Documentation](../sources/source-cards/2026-autogen-docs.md)
- [CrewAI Documentation](../sources/source-cards/2026-crewai-docs.md)
- [Microsoft Semantic Kernel Documentation](../sources/source-cards/2026-semantic-kernel-docs.md)
- [Real Semantic Kernel Plugin Validation](../experiments/real-semantic-kernel-plugin-validation/README.md)
- [Real Semantic Kernel Plugin Validation 结果](../experiments/real-semantic-kernel-plugin-validation/results-2026-07-12.md)
- [Real Framework Same-Task Comparison](../experiments/real-framework-same-task-comparison/README.md)
- [Real Framework Same-Task Comparison 结果](../experiments/real-framework-same-task-comparison/results-2026-07-12.md)
- [Real Multi-Agent Framework Validation](../experiments/real-multi-agent-framework-validation/README.md)
- [Real Multi-Agent Framework Validation 结果](../experiments/real-multi-agent-framework-validation/results-2026-07-12.md)

### Governance

- [References 覆盖矩阵](../references/coverage-matrix.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [Evidence Note: 多 Agent 不是默认更好](../evidence/multi-agent-default-boundary.md)
- [多 Agent 与 Flow 控制对比实验结果](../experiments/multi-agent-comparison/results-2026-07-11.md)
- [Evidence Note: 框架生态定位边界](../evidence/framework-landscape-boundary.md)
- [Evidence Note: 框架能力交叉表与选择边界](../evidence/framework-capability-crosswalk.md)
- [Evidence Note: Tool / Function / Plugin 术语对照边界](../evidence/tool-terminology-crosswalk.md)
- [框架选择 Rubric Smoke Test 结果](../experiments/framework-selection-rubric/results-2026-07-11.md)
