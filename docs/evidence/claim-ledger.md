# 结论证据台账

本台账用于控制正文正确性。只有状态为 `可入正文` 的结论，才能在章节中写成确定性表述。其他结论必须标注“待验证”“适用边界”或只放入资料卡片。

状态定义：

- `候选结论`：来自可信资料，但尚未精读或交叉验证。
- `部分验证`：有 1 个 A 级来源或多个来源方向一致，但仍缺工程验证或反例分析。
- `可入正文`：有清晰 references、边界说明，并经过交叉验证或实验设计。
- `不应确定表述`：容易误导初学者，必须保守表达。

## 当前台账

| 结论 | 支撑资料 | 当前状态 | 正文写法 |
| --- | --- | --- | --- |
| ReAct 的核心思想是交替生成推理轨迹和任务行动。 | ReAct paper | 部分验证 | 可作为 ReAct 的基础解释，但效果边界需保守。 |
| Tool use 可以让模型连接外部 API、搜索、计算器等工具。 | Toolformer paper；OpenAI Function Calling docs；OpenAI Responses API docs | 部分验证 | 可入门解释，但要区分研究训练方案和 API schema 机制。 |
| Function calling 本身不执行工具，执行发生在应用程序或工具运行时。 | OpenAI Function Calling docs；OpenAI Responses API docs；Evidence Note: Tool Use 与 Function Calling 边界 | 部分验证 | 可作为工程边界写入正文；仍建议用最小实验验证错误回传和重试流程。 |
| RAG 的动机包括外部知识访问、知识更新和 provenance。 | RAG paper | 部分验证 | 可作为 RAG 章节基础动机，但现代工程实现需另引框架文档。 |
| Memory 不等于 RAG，也不等于把完整历史塞进 prompt。 | MemGPT；MemoryBank；LangGraph memory docs | 候选结论 | 可作为术语边界，但需要精读后给出更严谨表述。 |
| 长期记忆可能提升持续交互体验，但也会引入错误写入、过时和隐私风险。 | MemoryBank；MemGPT；OWASP LLM Top 10；NIST AI RMF | 候选结论 | 不应写成“长期记忆总是提升 Agent”。 |
| Benchmark 不能直接代表真实业务 Agent 质量。 | AgentBench；WebArena；OpenAI Evals repo | 候选结论 | 可作为 Eval 章节核心提醒，需补 trace/业务 eval references。 |
| Prompt injection 不能只靠 prompt 解决。 | OWASP LLM Top 10；NIST AI RMF | 候选结论 | 待补工具权限和隔离案例后升级。 |
| 多 Agent 不是默认更好，会带来成本、调试和协调复杂度。 | AutoGen docs；CrewAI docs；AgentBench | 候选结论 | 需要工程案例或实验对比后再写成正文建议。 |
| MCP 是连接工具和上下文能力的协议，不是 Agent 框架本身。 | MCP official docs；MCP servers repo | 候选结论 | 待精读 MCP docs 后升级。 |

## 待升级为可入正文的优先结论

1. Agent vs Workflow 的边界。
2. Tool Use vs Function Calling 的边界。已完成第一轮官方文档交叉验证，待补最小实验。
3. RAG vs Memory 的边界。
4. MCP server/client/host 的职责边界。
5. Agent eval 为什么要看 trajectory。
6. Prompt injection 为什么需要权限和隔离，而不是只靠提示词。

## 升级流程

每条候选结论升级前需要：

1. 找到至少 1 个 A 级 reference 的直接支撑。
2. 找到另一个独立来源做交叉验证，或设计最小实验。
3. 写出适用场景和不适用场景。
4. 写出初学者版表述，避免术语堆叠。
5. 在对应 source card 中记录证据，再迁移到章节正文。
