# References 覆盖矩阵 v1

本矩阵用于检查学习手册的广度和正确性。每个核心主题至少需要 2-3 个高可信 references，其中至少 1 个应为官方文档、论文、协议规范或源码。

状态说明：

- `候选`：已列入资料清单，但未完成链接复核。
- `链接已复核`：URL 可访问，但内容尚未精读。
- `待交叉验证`：已确认来源有效，但关键结论还需要其他来源或实验支撑。
- `可入正文`：关键结论完成交叉验证，可支撑章节正文。

## 主题覆盖

| 主题 | 入门资料 | 高可信 reference | 工程/源码 reference | 当前状态 | 缺口 |
| --- | --- | --- | --- | --- | --- |
| AI Agent 定义与边界 | 待补 | OpenAI Agents SDK docs；LangGraph docs；ReAct paper | 待补 | 关键段落已精读；部分验证 | 需要 workflow-agent hybrid 最小实验和更多框架横向资料 |
| LLM 与上下文工程 | OpenAI Text Generation docs；OpenAI Responses API docs | OpenAI Text Generation docs；OpenAI Structured Outputs docs；OpenAI Responses API docs | OpenAI cookbook 候选 | 关键段落已精读；部分验证 | 需要输出解析、结构化输出和长上下文失败模式最小实验 |
| Tool Use / Function Calling | OpenAI function calling docs | Toolformer paper；OpenAI function calling docs；OpenAI Responses API docs | OpenAI cookbook 候选 | 关键段落已精读；部分验证 | 需要最小实验、SDK 文档和其他框架术语对照 |
| Agent 架构模式 | 待补 | ReAct paper；Reflexion paper；Tree of Thoughts paper；OpenAI Agents SDK docs；LangGraph docs | LangGraph examples 候选 | Agent/workflow 边界已部分验证 | 需要 Plan-and-Execute、Reflection、workflow-agent hybrid 实验 |
| MCP | MCP official docs | MCP official docs | MCP servers repo | 关键段落已精读；部分验证 | 需要 spec 细节、安全边界和最小 trace 实验 |
| RAG | 待补 | RAG paper；Self-RAG 候选；LlamaIndex docs | LlamaIndex examples 候选 | RAG paper 摘要已精读；部分验证 | 需要现代 RAG 工程实践和最小实验 |
| Memory / 知识库治理 | LangGraph memory docs | MemGPT；MemoryBank；Generative Agents；LangGraph memory docs；OWASP LLM Top 10；NIST AI RMF | Letta docs；Zep docs | 关键论文、框架文档和风险资料已精读；部分验证 | 仍缺多会话长期记忆最小实验和更多隐私/权限工程资料 |
| Planning / Orchestration | 待补 | Tree of Thoughts；Reflexion；LangGraph docs | LangGraph docs | 部分链接已复核 | 需要 planner/executor 和状态机工程资料 |
| 多 Agent | 待补 | Multi-agent debate 候选；AutoGen docs；CrewAI docs；AgentBench | AutoGen docs；CrewAI docs | 关键段落已精读；部分验证 | 需要最小对比实验、真实工程边界和成本资料 |
| Evaluation / Observability | 待补 | AgentBench；WebArena | OpenAI Evals；LangSmith；Phoenix 候选 | 关键摘要/README 已精读；部分验证 | 需要 trace observability 资料、trajectory 最小实验、回归集工程案例 |
| Production / 安全 / 成本 | 待补 | OWASP LLM Top 10；NIST AI RMF | 框架安全文档候选 | 关键风险项已精读；部分验证 | 需要最小 prompt injection 实验、框架安全资料、审计资料 |
| 框架生态 | 待补 | OpenAI Agents SDK；LangGraph；LlamaIndex；AutoGen；Semantic Kernel；CrewAI | 官方 examples 候选 | 部分链接已复核 | 需要统一比较维度 |
| 实践项目路线 | OpenAI Cookbook | 待补 | OpenAI Cookbook；MCP servers repo；LangGraph examples 候选 | 部分链接已复核 | 需要按学习阶段拆项目 |

## 当前优先级

1. 补齐基础定义和术语边界的高可信 references。
2. 精读并提取已经链接复核的论文、官方文档和安全资料。LLM / Context、Tool Use / Function Calling、MCP、RAG / Memory、Production / Security 已完成第一轮。
3. 为 MCP、Tool Use、RAG、Eval 四个主题补齐源码 examples。Eval 已完成 OpenAI Evals README 第一轮，仍需 trace/observability 工程资料。
4. 为 Memory / 知识库治理补充长期记忆最小实验，并继续扩展隐私/权限工程资料。
5. 为 Production / Security 补充 prompt injection 最小实验、工具权限工程案例和审计资料。

## 入正文门槛

章节正文中的关键结论必须满足至少一项：

- 有 A 级 reference 直接支撑。
- 有 2 个以上独立 B 级 references 交叉支撑。
- 有源码或最小实验结果支撑。

对于工程建议，优先要求：官方文档 + 源码/example + 失败模式说明。
