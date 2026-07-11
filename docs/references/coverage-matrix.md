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
| AI Agent 定义与边界 | 待补 | OpenAI Agents SDK docs；LangGraph docs | 待补 | 部分链接已复核 | 需要官方定义和 workflow 对比来源 |
| LLM 与上下文工程 | OpenAI Responses API docs | OpenAI Responses API docs | OpenAI cookbook 候选 | 部分链接已复核 | 需要结构化输出和上下文失败模式资料 |
| Tool Use / Function Calling | OpenAI function calling docs | Toolformer paper；OpenAI function calling docs | OpenAI cookbook 候选 | 部分链接已复核 | 需要精读现代 API 文档和 SDK 文档 |
| Agent 架构模式 | 待补 | ReAct paper；Reflexion paper；Tree of Thoughts paper；LangGraph docs | LangGraph examples 候选 | 部分链接已复核 | 需要 workflow-agent hybrid 工程来源 |
| MCP | MCP official docs | MCP official docs | MCP example servers 候选 | 部分链接已复核 | 需要官方 spec 细读和安全边界资料 |
| RAG | 待补 | RAG paper；Self-RAG 候选；LlamaIndex docs | LlamaIndex examples 候选 | 部分链接已复核 | 需要现代 RAG 工程实践和 memory 对比 |
| Memory / 知识库治理 | 待补 | 待补 | 待补 | 缺口较大 | 需要长期记忆、写入守门、冲突治理资料 |
| Planning / Orchestration | 待补 | Tree of Thoughts；Reflexion；LangGraph docs | LangGraph docs | 部分链接已复核 | 需要 planner/executor 和状态机工程资料 |
| 多 Agent | 待补 | Multi-agent debate 候选 | AutoGen docs 候选 | 候选 | 需要真实工程边界和成本资料 |
| Evaluation / Observability | 待补 | AgentBench；WebArena | OpenAI Evals；LangSmith；Phoenix 候选 | 部分链接已复核 | 需要 trace、trajectory、回归集资料 |
| Production / 安全 / 成本 | 待补 | OWASP LLM Top 10；NIST AI RMF | 框架安全文档候选 | 部分链接已复核 | 需要 prompt injection、权限、审计资料 |
| 框架生态 | 待补 | OpenAI Agents SDK；LangGraph；LlamaIndex；AutoGen；Semantic Kernel | 官方 examples 候选 | 部分链接已复核 | 需要统一比较维度 |
| 实践项目路线 | 待补 | 待补 | OpenAI cookbook；MCP examples；LangGraph examples 候选 | 候选 | 需要按学习阶段拆项目 |

## 当前优先级

1. 补齐基础定义和术语边界的高可信 references。
2. 精读并提取已经链接复核的论文、官方文档和安全资料。
3. 为 MCP、Tool Use、RAG、Eval 四个主题补齐源码 examples。
4. 为 Memory / 知识库治理单独调查资料，这是当前最大缺口。
5. 为 Production / Security 补充 prompt injection 和工具权限的工程案例。

## 入正文门槛

章节正文中的关键结论必须满足至少一项：

- 有 A 级 reference 直接支撑。
- 有 2 个以上独立 B 级 references 交叉支撑。
- 有源码或最小实验结果支撑。

对于工程建议，优先要求：官方文档 + 源码/example + 失败模式说明。
