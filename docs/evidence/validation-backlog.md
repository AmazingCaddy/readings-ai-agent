# 待验证问题清单

这些问题后续需要通过 references 交叉验证或最小实验确认。未完成验证前，不应写成确定性结论。

## 概念边界

- Agent 和 Workflow 的边界如何定义才准确？已完成第一轮 OpenAI Agents SDK、LangGraph 和 ReAct 交叉验证，仍需补最小对比实验。
- “自治程度”是否可以作为分类维度？有哪些可靠来源支持？
- RAG 和 Memory 的边界如何解释给初学者？已完成第一轮验证，仍需补最小实验。

## 架构模式

- ReAct 在哪些任务中确实优于单次提示或简单 workflow？已完成论文摘要第一轮验证，仍需本地对比实验。
- Plan-and-Execute 的收益是否足以抵消额外成本和错误传播？已完成相关架构模式第一轮验证，仍需 planner/executor 最小实验。
- Reflection / Critic 模式在真实任务中是否稳定提升质量？Reflexion 已完成论文摘要第一轮验证，仍需结合现代模型、成本和错误记忆风险实验。
- 多 Agent 的收益是否足以抵消通信成本、协调复杂度和调试难度？已完成 AutoGen/CrewAI 第一轮资料验证，仍需最小对比实验。

## 工具调用

- Function calling、tool use、structured output 在不同框架中的术语差异是什么？OpenAI API 层和 Structured Outputs 边界已完成第一轮验证，仍需补其他框架术语对照。
- 工具参数校验和重试的最佳实践有哪些官方或工程 references？
- 工具调用权限应该如何设计确认边界？
- 最小 tool-calling 实验中，参数校验失败后模型能否稳定修正？

## MCP

- MCP 相比传统 API wrapper 的核心价值是什么？
- MCP tools、resources、prompts 的边界如何准确解释？官方 server concepts 已完成第一轮验证，仍需结合 spec 细节。
- MCP 安全模型和权限边界有哪些官方建议？已确认 roots 不是安全边界，仍需补 auth/approval/permission 资料。
- 如何用一个只读 MCP server 复现 host/client/server、`tools/list` 和 `tools/call` trace？

## RAG 与 Memory

- 长期记忆是否一定提升 Agent 表现？已完成第一轮验证：不能写成“一定提升”，仍需多会话实验验证在哪些任务中可能造成污染。
- Chunk size、embedding model、reranking 对结果的影响如何验证？LlamaIndex 已完成第一轮工程流程验证，仍需最小 RAG pipeline 实验。
- RAG 答案如何稳定带 source citation / source nodes？本轮 LlamaIndex 文档搜索未找到直接证据，需补具体示例或实验。
- Memory 写入守门有哪些可复用设计？Letta/Zep 已提供第一轮工程模式参考，仍需结合本地实验验证。
- RAG paper 中的 non-parametric memory 与 Agent long-term memory 如何避免术语混淆？

## Eval 与生产化

- 上下文工程中的输出解析、Structured Outputs、JSON mode 和长上下文失败模式如何设计最小实验？已完成 OpenAI 官方文档第一轮验证，仍需本地实验。
- Agent eval 应该优先评估最终结果还是完整 trajectory？已确认 AgentBench/WebArena/OpenAI Evals 支撑过程与交互评测的重要性，仍需补本地实验验证评分差异。
- 通用 benchmark 对真实业务 agent 的代表性有多强？已确认公开 benchmark 可学习评测思想，但业务系统仍需 custom/private eval。
- Trace 字段如何设计，才能同时支持调试、审计、回归和隐私控制？
- Prompt injection 防护有哪些已验证的工程方法？已确认 OWASP/NIST 支撑风险边界，仍需补最小实验和框架级权限/隔离资料。
- 安全 regression set 应该如何覆盖外部文档注入、工具参数越权、敏感信息泄露和 excessive agency？
