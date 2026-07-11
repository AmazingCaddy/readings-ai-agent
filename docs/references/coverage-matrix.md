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
| AI Agent 定义与边界 | 待补 | OpenAI Agents SDK docs；LangGraph docs；ReAct paper | Agent 自治程度 evidence；Workflow / Hybrid / ReAct-like 对比实验 | Agent/Workflow 控制权连续谱和自治程度不是能力等级的窄边界可入正文；关键段落已精读；标准库 workflow-agent 对比已完成；真实表现仍部分验证 | 需要真实模型 / Agent framework / repo issue 实验和更多框架横向资料 |
| LLM 与上下文工程 | OpenAI Text Generation docs；OpenAI Responses API docs | OpenAI Text Generation docs；OpenAI Structured Outputs docs；OpenAI Responses API docs | 上下文治理与结构化输出实验；上下文策略对比实验；Real Structured Outputs / JSON Mode harness；OpenAI cookbook 候选 | “LLM 应用输入输出不只是字符串”“schema valid 不等于事实/权限/业务正确”和“长上下文不能替代上下文治理”窄边界可入正文；标准库输出解析 / 上下文治理模拟实验和上下文策略对比实验已完成；真实 API harness 已准备；其他上下文行为部分验证 | 需要实际运行真实 Responses API / Structured Outputs、长上下文 / RAG / 摘要 / 成本对比和跨模型稳定性实验 |
| Tool Use / Function Calling | OpenAI function calling docs | Toolformer paper；OpenAI function calling docs；OpenAI Responses API docs | Tool calling 参数校验模拟实验；Real Tool Calling harness；OpenAI cookbook 候选 | “Function Calling 本身不执行工具”窄边界可入正文；参数校验/重试标准库模拟已完成；真实 API harness 已准备；其他工程行为部分验证 | 需要实际运行真实模型 / API 实验、SDK 文档和其他框架术语对照 |
| Agent 架构模式 | 待补 | ReAct paper；Reflexion paper；Tree of Thoughts paper；OpenAI Agents SDK docs；LangGraph docs | Workflow / Hybrid / ReAct-like 对比实验；Planner / Executor 对比实验；Reflection / Retry 实验；多 Agent 对比实验；LangGraph examples 候选 | “复杂 Agent 架构不是默认更可靠，需要用 trace、成本、失败原因和实验比较”的窄边界可入正文；关键论文摘要和框架段落已精读；标准库 workflow / ReAct-like、planner/executor、reflection/retry 和多 Agent 对比已完成；真实表现仍部分验证 | 需要真实模型和真实框架对比实验 |
| MCP | MCP official docs | MCP official docs；MCP 2025-11-25 spec；MCP Security Best Practices | MCP servers repo；MCP 最小 trace 模拟实验；MCP stdio JSON-RPC harness | host/client/server 职责边界可入正文；authorization optional、roots 不是 sandbox、token passthrough 禁止和高风险能力需权限/审计/隔离的安全窄边界可入正文；spec / 安全 / 授权关键段落已精读；标准库模拟实验和本地 stdio harness 已完成；真实 host 行为部分验证 | 需要真实 MCP SDK / host trace、权限确认、URL mode / OAuth、恶意 resource/prompt 实验和 host 实现差异对比 |
| RAG | LlamaIndex RAG docs | RAG paper；LlamaIndex docs；Self-RAG 候选 | RAG / Memory 对比实验；RAG 最小 pipeline / citation 模拟实验；Real RAG Citation Synthesis harness；LlamaIndex examples 候选 | RAG / Memory 术语边界可入正文；RAG 是可观察工程 pipeline 且需要 chunk metadata、retrieval trace、citation/source 绑定和无证据拒答的窄边界可入正文；RAG paper 摘要和 LlamaIndex 核心页面已精读；标准库 RAG / Memory 对比和 RAG pipeline 模拟实验已完成；真实 LLM citation harness 已准备；工程质量部分验证 | 需要实际运行 LLM citation harness，并补真实 embedding / vector store、chunk size/top-k/rerank 对比和 citation correctness 实验 |
| Memory / 知识库治理 | LangGraph memory docs | MemGPT；MemoryBank；Generative Agents；LangGraph memory docs；OWASP LLM Top 10；NIST AI RMF | RAG / Memory 对比实验；Letta docs；Zep docs；长期记忆写入守门模拟实验；长期记忆生命周期与权限审计实验 | RAG / Memory 术语边界可入正文；长期记忆需要写入守门、生命周期权限、跨用户隔离和 trace 脱敏的治理边界可入正文；关键论文、框架文档、风险资料已精读；标准库 RAG / Memory 对比、写入守门模拟和生命周期权限审计已完成；真实收益和框架行为仍部分验证 | 仍缺真实多会话 Agent / memory framework 收益、污染、隐私、权限、查看/编辑/删除实验 |
| Planning / Orchestration | 待补 | Tree of Thoughts；Reflexion；LangGraph docs | Planner / Executor 对比实验；Reflection / Retry 实验；LangGraph docs | Planner/Executor 需要可执行计划、证据校验、失败反馈和重规划 trace 的窄边界可入正文；关键论文摘要、LangGraph 段落、标准库 planner/executor 和 reflection/retry 对比已完成；真实表现仍部分验证 | 需要状态机、真实模型和真实框架对比实验 |
| 多 Agent | 待补 | Multi-agent debate 候选；AutoGen docs；CrewAI docs；AgentBench | AutoGen docs；CrewAI docs；多 Agent / Flow 控制对比实验 | “多 Agent 不是复杂任务默认升级路径，需角色边界/证据分配/冲突处理/review trace/成本预算”的窄边界可入正文；关键段落已精读；标准库多 Agent 对比已完成；真实表现仍部分验证 | 需要真实模型 / AutoGen / CrewAI / LangGraph 横向实验、真实工程边界和成本资料 |
| Evaluation / Observability | LangSmith docs；Phoenix docs | AgentBench；WebArena；LangSmith docs；Phoenix docs | OpenAI Evals；OpenAI Cookbook；LangSmith docs；Phoenix docs；Trace-aware eval 模拟实验；Trace schema audit；Real Trace-Aware Eval harness | 公开 benchmark 不能直接代表真实业务 Agent 质量、工具/副作用 Agent 不能只看最终答案、trace 字段要按 debug/audit/regression/cost/RAG/privacy 用途设计的窄边界可入正文；关键论文/README/工程文档已精读；标准库 trace-aware eval 和 trace schema audit 已完成；真实模型 trace harness 已准备；其余自动评分/平台字段/人工复核仍部分验证 | 需要实际运行真实 Agent trace、自动评分误判分析、人工复核、平台字段映射和回归集工程案例 |
| Production / 安全 / 成本 | OpenAI Agents SDK docs；OpenAI Cookbook | OWASP LLM Top 10；NIST AI RMF；OpenAI Agents SDK docs；Semantic Kernel docs | OpenAI Responses API docs；OpenAI Agents SDK docs；OpenAI Cookbook；Observability docs；Prompt injection / tool permission 模拟实验；安全 regression set 最小实验；审批状态恢复与幂等性实验；Real Prompt Injection / Permission harness | Prompt injection 不能只靠 prompt、高风险工具需系统层权限/审批/审计的窄边界可入正文；风险资料和框架工程资料已精读；标准库攻击模拟、安全 regression set 和审批状态恢复实验已完成；真实 API harness 已准备；真实 guardrail/HITL 效果仍部分验证 | 需要实际运行真实模型 / 框架 guardrail / HITL approval 实验、跨框架权限对比、审计脱敏策略 |
| 框架生态 | 待补 | OpenAI Agents SDK；LangGraph；LlamaIndex；AutoGen；Semantic Kernel；CrewAI | 框架能力交叉表；框架选择 rubric smoke test；官方 examples 候选 | 关键框架定位已精读；框架能力交叉表和标准库 rubric smoke test 已完成；部分验证 | 需要真实同一任务横向实验、observability/permission 对比和官方 examples |
| 实践项目路线 | OpenAI Cookbook | OpenAI Cookbook；OpenAI Function Calling docs；OpenAI Responses API docs；OpenAI Evals repo | 实践路线 smoke harness；OpenAI Cookbook；MCP servers repo；LangGraph examples 候选 | 具体 Cookbook recipe 已精读；标准库 smoke harness 已完成；部分验证 | 需要真实 Cookbook / API 本地试跑最小项目、选择低成本技术栈、补 MCP/LangGraph examples |

## 当前优先级

1. 补齐基础定义和术语边界的高可信 references。Agent/Workflow 控制权连续谱和自治程度不是能力等级的窄边界已可入正文；标准库 workflow / hybrid / ReAct-like 对比已完成，仍需真实模型 / 框架 / repo issue 实验。
2. 精读并提取已经链接复核的论文、官方文档和安全资料。LLM / Context、Tool Use / Function Calling、MCP、RAG / Memory、Production / Security 已完成第一轮；LLM / Context、Tool Use 和 Production / Security 已补 P0 真实 API harness，仍需实际运行真实 API 和长上下文成本实验。
3. 为 MCP、Tool Use、RAG、Eval 四个主题补齐源码 examples。MCP 职责边界和安全/授权窄边界已可入正文，官方 spec、标准库 trace 模拟和本地 stdio JSON-RPC harness 已完成，仍需真实 MCP SDK / host trace 与权限实验；Tool Use 的 Function Calling 执行边界已可入正文，参数校验/重试标准库模拟已完成，仍需真实模型 / API 实验和框架对照；Eval 的工具/副作用 Agent 过程安全边界已可入正文，OpenAI Evals README、Cookbook、LangSmith、Phoenix、标准库 trace-aware eval、trace schema audit 和真实模型 trace harness 已完成第一轮，仍需实际运行真实 Agent trace、自动评分误判和人工复核实验。
4. 为 Memory / 知识库治理补充真实多会话 Agent / memory framework 实验。标准库写入守门模拟和生命周期权限审计已完成，仍需扩展真实框架中的隐私、权限、查看、编辑和删除工程资料。
5. 为 Production / Security 补充真实模型 / 框架 guardrail / HITL approval 实验、跨框架权限对比和审计脱敏策略。Prompt injection 和高风险工具权限窄边界已可入正文；标准库 prompt injection / tool permission 模拟、安全 regression set 和审批状态恢复实验已完成。
6. 为实践项目路线试跑 Structured Outputs、RAG/File Search、eval harness、成本/限流练习，记录初学者阻塞点。标准库 smoke harness 已完成，可作为无模型验收结构；仍需真实 Cookbook / API 试跑。

## 入正文门槛

章节正文中的关键结论必须满足至少一项：

- 有 A 级 reference 直接支撑。
- 有 2 个以上独立 B 级 references 交叉支撑。
- 有源码或最小实验结果支撑。

对于工程建议，优先要求：官方文档 + 源码/example + 失败模式说明。
