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

## 交叉验证结果

- 一致点：OWASP 支撑 prompt injection、insecure plugin/tool design、sensitive information disclosure 和 excessive agency 风险；这说明工具权限和外部内容边界必须由系统控制。
- 一致点：OpenAI Function Calling / Tool Calling docs 和 Responses API evidence 已确认工具执行发生在应用侧或工具运行时，模型主要生成工具调用请求；这支持应用侧参数校验、权限判断和审计责任。
- 一致点：Responses API source card 已记录 remote MCP 工具支持 `allowed_tools`、`require_approval`、`authorization`、`server_url` / `connector_id` 等字段；这说明工具权限和审批是 API 层需要表达的边界。
- 一致点：OpenAI Agents SDK guardrails 文档支持 input/output/tool guardrails；tool guardrails 可在 custom function-tool 调用前后验证或阻断工具调用。
- 一致点：OpenAI Agents SDK guardrails 文档明确 blocking guardrails 可在 agent 启动前运行，避免 token consumption 和 tool execution；parallel guardrails 则可能已开始消耗 token 或执行工具。
- 一致点：OpenAI Agents SDK HITL 文档支持敏感 tool calls 暂停执行，等待 approve/reject；`RunState` 可序列化和恢复审批状态，`needs_approval` / `require_approval` 覆盖 function tools、agent-as-tool、Shell/ApplyPatch、本地 MCP 和 Hosted MCP 等工具面。
- 一致点：OpenAI Agents SDK tracing 文档提醒 generation/function spans 可能捕获敏感数据，并支持关闭敏感输入/输出捕获；这支持“审计 trace 也需要隐私治理”。
- 一致点：Semantic Kernel Plugins 文档区分 retrieval functions 和 task automation functions，并指出 task automation functions 往往需要 human-in-the-loop approval processes；这与 OpenAI HITL 机制方向一致。
- 边界：OpenAI Agents SDK tool guardrails 明确不覆盖 hosted tools、built-in execution tools 和 handoffs 等所有执行面；因此框架 guardrail 不能被写成全局安全边界。
- 边界：NIST 和 OWASP 支撑风险治理视角，OpenAI/Semantic Kernel 支撑工程机制，但是否有效仍需对具体工具、数据和权限模型做本地攻击/失败实验。
- 本地实验：标准库 prompt injection / permission 模拟显示，写工具在应用层审批前阻断后不会产生 `refund_issued` 副作用；同一 trace 还演示了敏感字段在写入审计前脱敏。这支持“审批和 trace 隐私治理需要在工具执行路径上实现”的工程表述。
- 本地实验：标准库安全 regression set 把安全 case 拆成 expected decision、actual decision、risk tags、false positive、false negative 和 secret leak 字段；它覆盖外部注入、跨用户读取、高金额退款、敏感邮件、破坏性工具、重复提交和 benign read。这支持“上线前安全 regression set 应同时检查阻断、审批、放行和误伤”的工程表述。

## 实验验证

- 是否需要实验：是
- 实验设计：实现一个最小客服 Agent，包含只读订单查询、发送邮件、取消订单、退款建议四类工具。构造外部文档 prompt injection、错误用户 ID、越权金额、敏感字段泄露、重复提交等 10-20 个安全 case。分别测试：无 guardrail、prompt-only、防护型参数校验、blocking guardrail、tool guardrail、HITL approval、敏感 trace 关闭、审计日志。记录被阻断类型、漏报、误报、成本、延迟和人工处理量。
- 结果：已完成标准库 prompt injection / permission 模拟和安全 regression set，覆盖外部文档注入、只读/写工具分离、模拟审批拒绝、跨用户读取、高金额审批、敏感字段阻断/脱敏、破坏性工具、幂等性、benign case、审计事件和误报/漏报字段。尚未覆盖真实框架 guardrail、HITL 状态恢复、真实成本、真实延迟或跨框架对比。

## 结论状态

- 部分验证：风险资料、OpenAI API/SDK 文档和 Semantic Kernel 文档已经共同支撑工具权限、审批、guardrails 和敏感 trace 控制的工程边界；标准库实验支撑只读/写工具分离、审批拒绝、trace 脱敏和安全 regression set 的最小流程。仍缺真实框架安全实验、真实误报/漏报分析和跨框架对比。

## 可进入章节

- 是。可以写成：高风险工具应默认最小权限，写操作需要确认或审批，工具参数必须由应用层校验，guardrails 应放在正确执行点，trace 应记录可审计信息但避免泄露敏感数据。不能写成“用了 guardrails 或 HITL 就安全”。
