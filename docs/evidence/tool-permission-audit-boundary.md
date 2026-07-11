# Evidence Note: 工具权限、人工确认与审计边界

## 要验证的结论

生产化 Agent 的工具安全不能只依靠提示词。更可靠的边界通常由工具分类、最小权限、参数校验、guardrails、人工确认、可恢复审批状态、敏感 trace 控制、审计日志和安全 regression cases 共同构成。框架提供的 guardrails / approval / tracing 是有用机制，但不自动等于完整安全方案。

## 资料来源

- Source 1：[OWASP Top 10 for Large Language Model Applications](../sources/source-cards/2026-owasp-llm-top-10.md)
- Source 2：[NIST AI Risk Management Framework](../sources/source-cards/2026-nist-ai-rmf.md)
- Source 3：[OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- Source 4：[OpenAI Responses API Documentation](../sources/source-cards/2026-openai-responses-api-docs.md)
- Source 5：[OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- Source 6：[Microsoft Semantic Kernel Documentation](../sources/source-cards/2026-semantic-kernel-docs.md)
- Source 7：[Evidence Note: Prompt Injection 与权限边界](prompt-injection-permission-boundary.md)
- Source 8：[Evidence Note: Observability 与 Trace 工程边界](observability-trace-boundary.md)
- Source 9：[Prompt Injection 与工具权限最小实验结果](../experiments/prompt-injection-permission/results-2026-07-11.md)
- Source 10：[安全 Regression Set 最小实验结果](../experiments/security-regression-set/results-2026-07-11.md)
- Source 11：[审批状态恢复与幂等性实验结果](../experiments/approval-state-recovery/results-2026-07-11.md)
- Source 12：[Anthropic MCP Connector and Tunnels Documentation](../sources/source-cards/2026-anthropic-mcp-docs.md)
- Source 13：[LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- Source 14：[OWASP Agentic AI Security Resources](../sources/source-cards/2026-owasp-agentic-ai-security.md)
- Source 15：[MITRE ATLAS](../sources/source-cards/2026-mitre-atlas.md)
- Source 16：[Real Agentic Security Regression Set 标准库结果](../experiments/real-agentic-security-regression-set/results-2026-07-11.md)
- Source 17：[Real OpenAI Agents SDK Guardrail Validation 结果](../experiments/real-openai-agents-guardrail-validation/results-2026-07-12.md)

## 交叉验证结果

- 一致点：OWASP GenAI LLM Top 10 2025 archive 支撑 `LLM01 Prompt Injection`、`LLM02 Sensitive Information Disclosure`、`LLM05 Improper Output Handling`、`LLM06 Excessive Agency` 和 `LLM08 Vector and Embedding Weaknesses` 风险；这说明工具权限、外部内容、模型输出、敏感数据和 RAG/vector store 边界必须由系统控制。
- 一致点：OpenAI Function Calling / Tool Calling docs 和 Responses API evidence 已确认工具执行发生在应用侧或工具运行时，模型主要生成工具调用请求；这支持应用侧参数校验、权限判断和审计责任。
- 一致点：Responses API source card 已记录 remote MCP 工具支持 `allowed_tools`、`require_approval`、`authorization`、`server_url` / `connector_id` 等字段；这说明工具权限和审批是 API 层需要表达的边界。
- 一致点：OpenAI Agents SDK guardrails 文档支持 input/output/tool guardrails；tool guardrails 可在 custom function-tool 调用前后验证或阻断工具调用。2026-07-12 复核进一步确认 tool guardrails 只覆盖 `function_tool` 创建的 function tools，不覆盖 hosted tools、built-in execution tools、handoff call 本身或 `Agent.as_tool()` 的直接 tool-guardrail options。
- 一致点：OpenAI Agents SDK guardrails 文档明确 blocking guardrails 可在 agent 启动前运行，避免 token consumption 和 tool execution；parallel guardrails 则可能已开始消耗 token 或执行工具。
- 一致点：OpenAI Agents SDK HITL 文档支持敏感 tool calls 暂停执行，等待 approve/reject；`RunState` 可序列化和恢复审批状态，`needs_approval` / `require_approval` 覆盖 function tools、agent-as-tool、Shell/ApplyPatch、本地 MCP 和 Hosted MCP 等工具面。但 Tools 页面同时说明 hosted-container `ShellTool` 不支持 `needs_approval` 或 `on_approval`。
- 一致点：OpenAI Agents SDK tracing 文档提醒 generation/function spans 可能捕获敏感数据，并支持关闭敏感输入/输出捕获；2026-07-12 复核确认 `trace_include_sensitive_data` 默认是 `True`。HITL 文档还说明 serialized `RunState` 包含 app context、approvals、usage、serialized `tool_input`、nested resumptions 和 trace metadata。这支持“审计 trace 和可恢复状态都需要隐私治理”。
- 一致点：Anthropic MCP connector 文档支持 remote MCP tools 的 allowlist、denylist、per-tool configuration 和 OAuth bearer token，并建议 read-only assistant 或需要 human confirmation 的场景禁用写入/破坏性工具；这与高风险工具默认最小权限和人类确认的工程边界一致。
- 一致点：Anthropic MCP connector 文档说明该功能不适用于 Zero Data Retention，MCP server 交换的数据、工具定义和执行结果按标准 retention policy 保留；这补强了“工具调用 trace / 外部工具数据也需要数据保留和隐私治理”的边界。
- 一致点：Semantic Kernel Plugins 文档区分 retrieval functions 和 task automation functions，并指出 task automation functions 往往需要 human-in-the-loop approval processes；这与 OpenAI HITL 机制方向一致。
- 一致点：LangGraph interrupts 文档支持用 `interrupt()` 暂停 graph execution，将 JSON-serializable payload 暴露给调用方，再用 `Command(resume=...)` 恢复；approval workflows、review/edit state 和 tool 内中断可放在 API calls、database changes、financial transactions 等 critical actions 前。
- 一致点：LangGraph persistence 文档支持 checkpointer 按 `thread_id` 保存 graph state snapshots，用于 conversation continuity、HITL、time travel 和 fault tolerance；thinking-in-langgraph 文档也建议 user-fixable errors 用 `interrupt()` 暂停，并在 human review node 开头放置 `interrupt()`。
- 一致点：OWASP Agentic AI resources 把 tool misuse、identity / privilege abuse、memory poisoning、insecure inter-agent communication、cascading failures、trust exploitation 和 rogue agents 列为 agentic-specific 风险方向；这补强了“工具权限、身份、记忆、多 Agent 通信、级联失败和停止条件都应进入安全测试矩阵”的边界。
- 一致点：OWASP Agentic AI crosswalk 摘要把 runtime containment、architectural monitoring、supply chain attestation 和 schema controls 列为 priority gap areas；这与运行时隔离、trace / monitoring、依赖 / 工具供应链审查和 schema 校验的工程边界一致。
- 一致点：MITRE ATLAS latest v6 YAML 把 Agentic AI 定义为可自主 plan、decide、execute multi-step actions 的平台，并包含 `AI Agent Tool Invocation`、`AI Agent Tool Poisoning`、MCP / remote tool、memory poisoning、computer-use destructive action 等 technique / case-study 线索；这补强了工具权限、远程工具、记忆和 computer-use action 都应进入安全 regression set 的边界。
- 边界：OpenAI Agents SDK tool guardrails 明确不覆盖 hosted tools、built-in execution tools、handoff call 和 `Agent.as_tool()` 直接选项等所有执行面；hosted-container ShellTool 也不支持同一 HITL approval callback 面。因此框架 guardrail / approval 不能被写成全局安全边界。
- 边界：LangGraph interrupt/resume 不是“任意位置安全暂停”。文档明确 resume 时 node 会从头重新执行，`interrupt()` 前的代码会再次运行；不要重排或条件跳过同一 node 的 interrupt；不要把 interrupt 包在 broad try/except 中；interrupt payload 必须 JSON-serializable；side effects before interrupt 必须幂等，最好放在 interrupt 之后或拆到独立 node。
- 边界：LangGraph 内存型 checkpointer 只适合教程或进程内实验，进程重启后不会保留 checkpoints；生产恢复需要持久化 checkpointer，并考虑长会话 checkpoint 增长、保留和清理策略。
- 边界：OWASP Agentic AI resources 当前只复核公开摘要；白皮书全文未精读，不能直接支撑完整控制清单或 mitigation 有效性。
- 边界：MITRE ATLAS mitigations 只能作为控制候选和 checklist 来源；不能单独证明任何权限继承、工具确认、segmentation、memory hardening、validation 或 monitoring 在真实 Agent 系统中有效。
- 边界：NIST 和 OWASP 支撑风险治理视角，OpenAI/Semantic Kernel 支撑工程机制，但是否有效仍需对具体工具、数据和权限模型做本地攻击/失败实验。
- 本地实验：标准库 prompt injection / permission 模拟显示，写工具在应用层审批前阻断后不会产生 `refund_issued` 副作用；同一 trace 还演示了敏感字段在写入审计前脱敏。这支持“审批和 trace 隐私治理需要在工具执行路径上实现”的工程表述。
- 本地实验：标准库安全 regression set 把安全 case 拆成 expected decision、actual decision、risk tags、false positive、false negative 和 secret leak 字段；它覆盖外部注入、跨用户读取、高金额退款、敏感邮件、破坏性工具、重复提交和 benign read。这支持“上线前安全 regression set 应同时检查阻断、审批、放行和误伤”的工程表述。
- 本地实验：标准库 approval state recovery audit 比较 `naive_resume` 和 `governed_resume`。`naive_resume` 在重复恢复、拒绝后恢复和参数篡改恢复上失败，并产生重复副作用和敏感 trace 泄露；`governed_resume` 通过 7/7 个操作，覆盖审批状态、执行状态、参数快照 hash、拒绝阻断、幂等恢复和 trace 脱敏。这支持“人工审批必须是可恢复、可审计、可幂等的执行流程”的工程表述。
- 本地实验：Real Agentic Security Regression Set 的标准库 toy runtime 覆盖 tool invocation、tool poisoning、memory poisoning、MCP / remote tool、computer-use destructive action、runaway loop 和 inter-agent message。`policy_enforced_hitl` 通过 8/9，但仍未阻断 computer-use destructive action；`sandboxed_runtime` 通过 9/9。这支持“HITL 与 sandbox/runtime containment 是不同边界”的工程表述，但不证明真实 sandbox、HITL 或 guardrail 有效。
- 真实框架本地观察：Real OpenAI Agents SDK Guardrail Validation 使用 `openai-agents==0.18.2` / deterministic fake model 跑通 5 个 case：input guardrail tripwire 在模型调用前触发，output guardrail tripwire 在模型调用后触发，function-tool input guardrail 的 `reject_content` 在 Runner 路径上阻止本地函数工具副作用，function-tool output guardrail 的 `reject_content` 发生在本地函数工具执行之后，只替换工具输出；`needs_approval` metadata 可观察；发布 trace 未泄露示例 secret。该结果支撑 guardrail 运行位置和 side-effect 边界的窄观察，但 guardrail policy、阈值、fake model response、serialized RunState 存储和 trace 脱敏仍由应用层代码负责。

## 实验验证

- 是否需要实验：是
- 实验设计：实现一个最小客服 Agent，包含只读订单查询、发送邮件、取消订单、退款建议四类工具。构造外部文档 prompt injection、错误用户 ID、越权金额、敏感字段泄露、重复提交、拒绝后恢复、参数篡改恢复等 10-20 个安全 case。分别测试：无 guardrail、prompt-only、防护型参数校验、blocking guardrail、tool guardrail、HITL approval、审批状态恢复、敏感 trace 关闭、审计日志。记录被阻断类型、漏报、误报、成本、延迟和人工处理量。
- 结果：已完成标准库 prompt injection / permission 模拟、安全 regression set、agentic security regression set 和 approval state recovery audit，覆盖外部文档注入、只读/写工具分离、模拟审批拒绝、跨用户读取、高金额审批、敏感字段阻断/脱敏、破坏性工具、幂等性、benign case、tool poisoning、memory poisoning、MCP / remote tool、computer-use destructive action、runaway loop、inter-agent message、审批状态恢复、拒绝后阻断、参数快照校验、审计事件和误报/漏报字段。LangGraph current docs 已补 interrupt / checkpointer / `thread_id` / node restart / side-effect idempotency 的框架机制证据。Real LangGraph Interrupt Recovery completed run 已在 LangGraph 1.2.9 / `MemorySaver` / 本地假退款工具下验证最小审批恢复、拒绝、参数 hash、重复恢复不重复执行和 trace 脱敏观察；也用 `langgraph-checkpoint-sqlite` 3.1.0 / `SqliteSaver` 验证同进程本地恢复、双本地 Python 进程恢复和双本地 Python 进程并发 resume。本次并发 resume 中两个进程都返回 `approved_executed`，共享副作用日志记录 1 次假工具执行。Real OpenAI Agents SDK Guardrail Validation 已完成 input/output/tool guardrail 本地 fake-model run，补强 guardrail 运行位置和本地函数工具 side-effect 边界。尚未覆盖真实模型 guardrail、hosted/MCP/Shell/ApplyPatch 工具覆盖、部署式服务重启、真实服务并发恢复、真实 sandbox/runtime containment、真实成本、真实延迟或跨框架对比。

## 结论状态

- 可入正文：窄结论“高风险工具不能只依赖模型自觉或安全 prompt；最小权限、应用层参数校验、写操作确认/审批、审批状态恢复、sandbox/runtime containment 和审计 trace 应进入工具执行路径”已完成第一轮交叉验证。风险资料、OpenAI API/SDK 文档、Anthropic MCP connector 文档、Semantic Kernel 文档、LangGraph 文档、OWASP Agentic AI resources 和 MITRE ATLAS 共同支撑工具权限、审批、guardrails、remote tool allowlist/denylist、data retention、interrupt/resume、checkpointer、`thread_id` 恢复、runtime containment、agent identity、memory poisoning、多 Agent 通信风险、Agentic AI tool invocation / tool poisoning / computer-use action 和敏感 trace 控制的工程边界；标准库实验支撑只读/写工具分离、审批拒绝、trace 脱敏、安全 regression set、agentic-specific regression set、审批状态恢复、参数快照校验、幂等执行，以及 HITL 与 sandbox/runtime containment 的不同边界；Real LangGraph completed run 支撑一个最小真实框架 pause/resume 观察和本地 SQLite checkpoint 恢复代理观察；Real OpenAI Agents SDK Guardrail completed run 支撑 input/output/tool guardrail 的本地 runtime surface 和 tool output guardrail 不能撤销已发生副作用的边界；OpenAI Agents SDK 2026-07-12 复核进一步支撑 function-tool-only guardrail、hosted shell approval 限制、trace 默认敏感数据捕获和 serialized RunState 治理边界。
- 部分验证：真实框架 guardrail/HITL 的完整覆盖范围、真实误报/漏报、hosted/MCP/Shell/ApplyPatch 工具行为、RunState 持久化治理、成本、延迟和跨框架对比仍待实际运行验证。

## 可进入章节

- 是。可以写成：高风险工具应默认最小权限，写操作需要确认或审批，工具参数必须由应用层校验，guardrails / interrupt 应放在正确执行点，审批恢复要校验状态、参数快照和幂等性，trace 应记录可审计信息但避免泄露敏感数据。不能写成“用了 guardrails、interrupt 或 HITL 就安全”，也不能写成某个框架默认覆盖所有工具执行面。
