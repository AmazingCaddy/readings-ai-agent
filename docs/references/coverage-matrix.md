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
| Agent 架构模式 | 待补 | ReAct paper；Reflexion paper；Tree of Thoughts paper；OpenAI Agents SDK docs；LangGraph docs | LangGraph examples 候选 | 关键论文摘要和框架段落已精读；部分验证 | 需要固定 workflow、ReAct、planner/executor、reflection 最小对比实验 |
| MCP | MCP official docs | MCP official docs；MCP 2025-11-25 spec；MCP Security Best Practices | MCP servers repo；MCP 最小 trace 模拟实验 | spec / 安全 / 授权关键段落已精读；标准库模拟实验已完成；部分验证 | 需要真实 MCP SDK / host trace、权限确认、URL mode / OAuth、恶意 resource/prompt 实验和 host 实现差异对比 |
| RAG | LlamaIndex RAG docs | RAG paper；LlamaIndex docs；Self-RAG 候选 | LlamaIndex examples 候选 | RAG paper 摘要和 LlamaIndex 核心页面已精读；部分验证 | 需要最小 RAG pipeline 实验和 citation/source 追溯示例 |
| Memory / 知识库治理 | LangGraph memory docs | MemGPT；MemoryBank；Generative Agents；LangGraph memory docs；OWASP LLM Top 10；NIST AI RMF | Letta docs；Zep docs | 关键论文、框架文档和风险资料已精读；部分验证 | 仍缺多会话长期记忆最小实验和更多隐私/权限工程资料 |
| Planning / Orchestration | 待补 | Tree of Thoughts；Reflexion；LangGraph docs | LangGraph docs | 关键论文摘要和 LangGraph 段落已精读；部分验证 | 需要 planner/executor、状态机和 reflection 对比实验 |
| 多 Agent | 待补 | Multi-agent debate 候选；AutoGen docs；CrewAI docs；AgentBench | AutoGen docs；CrewAI docs | 关键段落已精读；部分验证 | 需要最小对比实验、真实工程边界和成本资料 |
| Evaluation / Observability | LangSmith docs；Phoenix docs | AgentBench；WebArena；LangSmith docs；Phoenix docs | OpenAI Evals；OpenAI Cookbook；LangSmith docs；Phoenix docs | 关键论文/README/工程文档已精读；部分验证 | 需要 trace-aware eval 最小实验、自动评分误判分析、回归集工程案例 |
| Production / 安全 / 成本 | OpenAI Agents SDK docs；OpenAI Cookbook | OWASP LLM Top 10；NIST AI RMF；OpenAI Agents SDK docs；Semantic Kernel docs | OpenAI Responses API docs；OpenAI Agents SDK docs；OpenAI Cookbook；Observability docs | 风险资料和框架工程资料已精读；部分验证 | 需要最小 prompt injection / tool permission 实验、跨框架权限对比、审计脱敏策略 |
| 框架生态 | 待补 | OpenAI Agents SDK；LangGraph；LlamaIndex；AutoGen；Semantic Kernel；CrewAI | 官方 examples 候选 | 关键框架定位已精读；部分验证 | 需要同一任务横向实验、observability/permission 对比和官方 examples |
| 实践项目路线 | OpenAI Cookbook | OpenAI Cookbook；OpenAI Function Calling docs；OpenAI Responses API docs；OpenAI Evals repo | OpenAI Cookbook；MCP servers repo；LangGraph examples 候选 | 具体 Cookbook recipe 已精读；部分验证 | 需要本地试跑最小项目、选择低成本技术栈、补 MCP/LangGraph examples |

## 当前优先级

1. 补齐基础定义和术语边界的高可信 references。
2. 精读并提取已经链接复核的论文、官方文档和安全资料。LLM / Context、Tool Use / Function Calling、MCP、RAG / Memory、Production / Security 已完成第一轮。
3. 为 MCP、Tool Use、RAG、Eval 四个主题补齐源码 examples。MCP 已完成官方 spec、安全、授权第一轮和标准库 trace 模拟，仍需真实 MCP SDK / host trace 与权限实验；Eval 已完成 OpenAI Evals README、Cookbook、LangSmith 和 Phoenix 第一轮，仍需本地 trace-aware eval 实验。
4. 为 Memory / 知识库治理补充长期记忆最小实验，并继续扩展隐私/权限工程资料。
5. 为 Production / Security 补充 prompt injection / tool permission 最小实验、跨框架权限对比和审计脱敏策略。
6. 为实践项目路线试跑 Structured Outputs、RAG/File Search、eval harness、成本/限流练习，记录初学者阻塞点。

## 入正文门槛

章节正文中的关键结论必须满足至少一项：

- 有 A 级 reference 直接支撑。
- 有 2 个以上独立 B 级 references 交叉支撑。
- 有源码或最小实验结果支撑。

对于工程建议，优先要求：官方文档 + 源码/example + 失败模式说明。
