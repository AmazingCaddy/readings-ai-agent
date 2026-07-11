# Evidence Note: Agent 自治程度边界

## 要验证的结论

自治程度可以作为理解 Agent 系统的一个维度，但不应被写成“自治越高越高级”或“越自治越可靠”。更准确的说法是：自治程度描述系统把多少下一步决策、工具调用、状态推进、失败恢复和停止判断交给模型或 agent runtime；自治越高，越需要权限、停止条件、trace、eval、成本控制和人工确认。

## 资料来源

- Source 1：[OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- Source 2：[LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- Source 3：[ReAct: Synergizing Reasoning and Acting with Language Models](../sources/source-cards/2022-react-paper.md)
- Source 4：[Evidence Note: Agent 与 Workflow 边界](agent-workflow-boundary.md)
- Source 5：[Evidence Note: Prompt Injection 与权限边界](prompt-injection-permission-boundary.md)
- Source 6：[Workflow、Hybrid 与 ReAct-like Tool Loop 对比实验结果](../experiments/workflow-agent-comparison/results-2026-07-11.md)

## 交叉验证结果

- 一致点：Agent/Workflow evidence 已确认 Agent 和 Workflow 是控制权与编排方式的连续谱，而不是严格二分；固定 workflow、workflow-agent hybrid 和 tool loop 可以组合。
- 一致点：OpenAI Agents SDK source card 支撑 managed agent loop、tool execution、guardrails、handoffs、sessions 和 tracing，这说明较高自治通常意味着 runtime 管理更多 turns 和工具执行细节。
- 一致点：LangGraph source card 支撑 long-running, stateful workflow or agent、durable execution、persistence 和 human-in-the-loop，这说明自治程度和状态/恢复/人工介入设计密切相关。
- 一致点：ReAct 支撑“推理和行动交替”这一 agent loop 思路，但不证明所有任务都应该采用高自治 loop。
- 一致点：Prompt injection evidence 中 OWASP excessive agency 风险支持“unchecked autonomy to take action”会带来可靠性、隐私和信任风险；因此自治程度必须和权限边界一起讨论。
- 本地实验：workflow / hybrid / ReAct-like 标准库实验中，固定 workflow 工具调用最少但漏掉动态证据查询；hybrid 和 ReAct-like 都完成 3/3 任务，但 ReAct-like 工具调用更多。这支持“更高自治可能提升灵活性，但同时增加成本、trace 和停止条件要求”的边界。

## 实验验证

- 是否需要实验：是
- 实验设计：用同一任务比较固定 workflow、workflow-agent hybrid 和高自治 tool loop。记录成功率、工具调用数、失败原因、trace、停止条件和权限确认。
- 结果：已完成标准库最小模拟实验。真实模型、真实框架、真实工具错误、token/latency/cost 和权限确认仍待验证。

## 结论状态

- 可入正文：窄结论“自治程度可以作为解释 Agent 系统的维度，但它描述的是控制权分配和风险面，不是能力等级，也不代表越高越可靠”已完成第一轮交叉验证。OpenAI Agents SDK、LangGraph、ReAct、Agent/Workflow evidence、Prompt Injection evidence 和标准库 workflow / hybrid / ReAct-like 实验共同支撑该边界。
- 部分验证：不同自治程度在真实模型 / 框架 / 成本 / 权限 / 工具错误恢复中的收益和风险，仍需实际运行验证。

## 可进入章节

- 是。可以确定写成：Agent 的自治程度是连续谱，从固定 workflow、workflow-agent hybrid 到更开放的 tool loop；它是控制权和风险面的维度，不是能力等级。初学者应先从可控、可评测、低风险的设计开始，再逐步增加模型决策范围。
