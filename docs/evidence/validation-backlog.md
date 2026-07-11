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
- MCP tools、resources、prompts 的边界如何准确解释？已完成官方 server concepts 和 2025-11-25 spec 第一轮验证：tools 是 model-controlled，resources 是 application-driven，prompts 是 user-controlled；仍需本地 trace 验证具体 host 如何呈现。
- MCP 安全模型和权限边界有哪些官方建议？已完成第一轮验证：authorization 是 optional transport-level capability；HTTP transport 支持授权时遵循 OAuth 2.1 相关规范；STDIO transport 应从环境取得凭据；token passthrough 被禁止；roots 不等于 sandbox；elicitation/sampling 需要用户可见和可拒绝的交互边界；仍需 host/client/server 实验验证实现差异。
- 如何用一个只读 MCP server 复现 host/client/server、`tools/list`、`tools/call`、`resources/list`、`resources/read` 和 trace？
- 如何设计一个最小恶意 resource/prompt 与一个模拟写工具，验证 host 是否展示 tool inputs、允许用户拒绝、记录审计、避免敏感 token/resource 泄露？

## RAG 与 Memory

- 长期记忆是否一定提升 Agent 表现？已完成第一轮验证：不能写成“一定提升”，仍需多会话实验验证在哪些任务中可能造成污染。
- Chunk size、embedding model、reranking 对结果的影响如何验证？LlamaIndex 已完成第一轮工程流程验证，仍需最小 RAG pipeline 实验。
- RAG 答案如何稳定带 source citation / source nodes？本轮 LlamaIndex 文档搜索未找到直接证据，需补具体示例或实验。
- Memory 写入守门有哪些可复用设计？Letta/Zep 已提供第一轮工程模式参考，仍需结合本地实验验证。
- RAG paper 中的 non-parametric memory 与 Agent long-term memory 如何避免术语混淆？

## Eval 与生产化

- 上下文工程中的输出解析、Structured Outputs、JSON mode 和长上下文失败模式如何设计最小实验？已完成 OpenAI 官方文档第一轮验证，仍需本地实验。
- Agent eval 应该优先评估最终结果还是完整 trajectory？已确认 AgentBench/WebArena/OpenAI Evals/LangSmith/Phoenix 支撑过程与交互评测的重要性，仍需补本地实验验证评分差异。
- 通用 benchmark 对真实业务 agent 的代表性有多强？已确认公开 benchmark 可学习评测思想，但业务系统仍需 custom/private eval。
- Trace 字段如何设计，才能同时支持调试、审计、回归和隐私控制？已完成 LangSmith/Phoenix/Cookbook 第一轮验证，候选字段包括输入、输出、中间步骤、工具调用、检索、错误、延迟、token/cost、反馈、版本、metadata；仍需本地实验和隐私脱敏策略。
- LLM-as-judge、online evaluator 和自动化规则的误判率、成本与抽样人工复核比例如何设计？
- Prompt injection 防护有哪些已验证的工程方法？已确认 OWASP/NIST 支撑风险边界，OpenAI Agents SDK/Semantic Kernel/Responses API 支撑 guardrails、approval、require_approval、sensitive trace 控制等工程边界；仍需补最小攻击/失败实验。
- 安全 regression set 应该如何覆盖外部文档注入、工具参数越权、敏感信息泄露和 excessive agency？
- Guardrails、HITL approval、tool approval 和 sensitive trace 配置在不同框架中的覆盖范围有什么差异？OpenAI Agents SDK 已确认 tool guardrails 不覆盖所有工具类型，仍需横向比较。

## 实践路线

- 哪些 OpenAI Cookbook 示例最适合初学者作为项目模板？已完成第一轮验证：Structured Outputs、File Search RAG、OpenAI Evals、Agents SDK trace/eval、Usage/Cost、Rate limits 适合作为候选；仍需本地试跑确认依赖、成本和阻塞点。
- 每个项目应使用哪个最小技术栈，才能降低环境成本？需要基于本地试跑和 GitHub Pages 教程形态决定。
- 如何为项目 7 设计可自动运行的 eval harness？OpenAI Evals repo 和 Cookbook 可提供方向，仍需本地最小实现。
- 如何把 Cookbook recipe 改写成初学者可跟练教程，同时保留 references、trace、失败样例和成本记录？

## 框架生态

- 同一任务在 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen/CrewAI、Semantic Kernel 下的实现成本、trace、权限和错误处理如何比较？框架定位已完成第一轮验证，仍需横向实验。
- Semantic Kernel Process Framework 当前标注 experimental；后续复核时需要确认其稳定性和 API 变化。
