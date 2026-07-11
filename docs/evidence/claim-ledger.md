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
| ReAct 的核心思想是交替生成推理轨迹和任务行动。 | ReAct paper；Evidence Note: Agent 架构模式边界 | 部分验证 | 可作为 ReAct 的基础解释，但效果边界需保守。 |
| Agent 和 Workflow 的边界主要在控制权、状态和决策方式；二者可以组合成 workflow-agent hybrid。 | OpenAI Agents SDK docs；LangGraph docs；ReAct paper；Evidence Note: Agent 与 Workflow 边界；Workflow / Hybrid / ReAct-like 对比实验结果 | 部分验证 | 可作为第 01/04 章基础边界；标准库实验支持固定 workflow、hybrid 和 tool loop 的最小比较流程，仍需真实模型/框架实验；需避免写成“Agent 总比 workflow 高级”。 |
| Reflection / Reflexion 可以利用任务反馈和文字反思改进后续尝试，但不保证稳定提升。 | Reflexion paper；Memory governance evidence；Agent eval evidence；Evidence Note: Agent 架构模式边界；Reflection / Retry 实验结果 | 部分验证 | 可作为架构模式解释；标准库实验显示 verified reflection retry 可补齐缺证据，但 unverified reflection memory 会让错误重复；需提醒反馈质量、成本和错误记忆风险。 |
| Tree of Thoughts 支持搜索式推理路径，但不等同于生产 Agent 编排框架。 | Tree of Thoughts paper；LangGraph docs；Evidence Note: Agent 架构模式边界 | 部分验证 | 可作为规划/搜索思路解释；不能写成复杂任务默认应使用 ToT。 |
| 复杂 Agent 架构不是默认更可靠，需用 trace、成本、失败原因和实验比较。 | ReAct；Reflexion；Tree of Thoughts；LangGraph docs；Agent/Workflow evidence；Multi-agent evidence；Workflow / Hybrid / ReAct-like 对比实验结果；Planner / Executor 对比实验结果；Reflection / Retry 实验结果 | 部分验证 | 可作为第 04/07 章核心提醒；标准库实验已覆盖固定 workflow、hybrid、ReAct-like tool loop、planner/executor 和 reflection/retry 的工具调用/失败原因/重规划/错误反思比较，仍需真实框架对比实验。 |
| Planner / Executor 需要可执行计划、证据校验和失败反馈；一次性计划可能传播遗漏。 | Agent 架构模式 evidence；Planner / Executor 对比实验结果；LangGraph docs | 部分验证 | 可作为第 04/07 章工程边界；标准库实验已验证 missing evidence 与 plan revision 流程，真实模型 / 框架 / repo issue 仍待验证。 |
| LLM 应用的输入输出不只是字符串，Responses 等 API 会把 message roles、content items、tool calls、refusals 和 structured outputs 建模为结构化对象。 | OpenAI Text Generation docs；OpenAI Responses API docs；Evidence Note: 上下文工程与结构化输出边界；上下文治理与结构化输出实验结果 | 部分验证 | 可作为第 02 章基础解释；标准库实验支持结构化解析和校验字段设计，其他供应商字段名可能不同。 |
| 结构化输出能提升解析和 schema 校验可靠性，但不保证事实正确。 | OpenAI Structured Outputs docs；OpenAI Responses API docs；OpenAI Function Calling docs；Evidence Note: 上下文工程与结构化输出边界；上下文治理与结构化输出实验结果 | 部分验证 | 可写入第 02/03 章；标准库实验显示 schema valid 仍可能有业务/权限/citation 语义错误；仍需真实 API / 模型实验。 |
| 长上下文不能替代上下文治理。 | OpenAI Text Generation docs；OpenAI Responses API docs；RAG / Memory evidence；Prompt Injection evidence；Evidence Note: 上下文工程与结构化输出边界；上下文治理与结构化输出实验结果 | 部分验证 | 可作为上下文工程核心提醒；标准库实验验证旧资料和外部注入的最小失败模式，仍需真实长上下文 / RAG / 摘要 / 成本对比实验。 |
| Tool use 可以让模型连接外部 API、搜索、计算器等工具。 | Toolformer paper；OpenAI Function Calling docs；OpenAI Responses API docs | 部分验证 | 可入门解释，但要区分研究训练方案和 API schema 机制。 |
| Function calling 本身不执行工具，执行发生在应用程序或工具运行时。 | OpenAI Function Calling docs；OpenAI Responses API docs；Evidence Note: Tool Use 与 Function Calling 边界；Tool Calling 参数校验与重试实验结果 | 部分验证 | 可作为工程边界写入正文；标准库模拟实验已验证参数校验、错误回传和有限重试流程，仍需真实模型 / API 实验。 |
| RAG 的动机包括外部知识访问、知识更新和 provenance。 | RAG paper；LlamaIndex docs；Evidence Note: RAG 与 Memory 边界；Evidence Note: RAG 工程流程边界 | 部分验证 | 可作为 RAG 章节基础动机；现代工程流程需结合框架文档和实验。 |
| 工程 RAG 是 loading、indexing、storing、querying、evaluation 等阶段组成的 pipeline，不是单个 prompt 技巧。 | LlamaIndex docs；RAG paper；Evidence Note: RAG 工程流程边界；RAG 最小 Pipeline 与 Citation 实验结果 | 部分验证 | 可作为第 06 章工程流程解释；标准库模拟实验已验证 chunk metadata、retrieval trace、citation 和无证据拒答流程，真实 embedding / rerank / LLM synthesis 仍需实验。 |
| Memory 不等于 RAG，也不等于把完整历史塞进 prompt。 | RAG paper；MemGPT；MemoryBank；LangGraph memory docs；Evidence Note: RAG 与 Memory 边界 | 部分验证 | 可作为术语边界写入正文；需提醒 RAG paper 中的 non-parametric memory 不是 Agent 长期记忆治理。 |
| 长期记忆可能提升持续交互体验，但也会引入错误写入、过时和隐私风险。 | MemoryBank；MemGPT；Generative Agents；Letta docs；Zep docs；OWASP LLM Top 10；NIST AI RMF；Evidence Note: 长期记忆治理与风险边界；长期记忆写入守门与治理实验结果 | 部分验证 | 可作为长期记忆章节的保守边界；标准库实验已验证自动写入会持久化敏感信息和低置信推断，写入守门可降低污染；不应写成“长期记忆总是提升 Agent”。 |
| Benchmark 不能直接代表真实业务 Agent 质量。 | AgentBench；WebArena；OpenAI Evals repo；Evidence Note: Agent Eval 与 Trajectory 边界 | 部分验证 | 可作为 Eval 章节核心提醒；公开 benchmark 可学习评测思想，但业务系统仍需 custom/private eval 和 trace。 |
| Agent eval 不应只看最终答案，还应检查关键 trajectory / trace。 | AgentBench；WebArena；OpenAI Evals repo；LangSmith docs；Phoenix docs；OpenAI Cookbook；Evidence Note: Agent Eval 与 Trajectory 边界；Evidence Note: Observability 与 Trace 工程边界；Trace-Aware Eval 最小实验结果 | 部分验证 | 可写入 Eval 章节；标准库实验已验证 final-only 会漏掉无审批副作用工具和工具错误未恢复，真实 Agent trace / LLM-as-judge / 人工复核仍待验证。 |
| Agent trace 应记录输入、输出、中间步骤、工具调用、检索、错误、延迟/成本、反馈和版本信息，才能支撑调试、审计、回归和在线/离线评测。 | LangSmith docs；Phoenix docs；OpenAI Cookbook；OpenAI Evals repo；Evidence Note: Observability 与 Trace 工程边界；Trace-Aware Eval 最小实验结果 | 部分验证 | 可作为第 08/09/11 章工程建议；标准库实验覆盖 tool call/result/error/approval/final response，仍需真实 RAG traces、latency/token/cost 和平台对照。 |
| Prompt injection 不能只靠 prompt 解决。 | OWASP LLM Top 10；NIST AI RMF；OpenAI Function Calling docs；OpenAI Agents SDK docs；Semantic Kernel docs；Evidence Note: Prompt Injection 与权限边界；Evidence Note: 工具权限、人工确认与审计边界；Prompt Injection 与工具权限最小实验结果 | 部分验证 | 可作为生产安全章节的核心提醒；标准库实验已验证 prompt-only 会执行注入诱导的写工具并泄露假 secret，仍需真实模型 / 框架 guardrail 实验。 |
| 高风险工具应使用最小权限、参数校验、guardrails、人工确认、审批状态恢复和审计 trace 的组合，而不是只靠模型自觉。 | OWASP LLM Top 10；OpenAI Responses API docs；OpenAI Agents SDK docs；Semantic Kernel docs；Observability evidence；Evidence Note: 工具权限、人工确认与审计边界；Prompt Injection 与工具权限最小实验结果 | 部分验证 | 可作为第 09/11 章工程建议；标准库实验已验证只读/写工具分离、审批拒绝和 trace 脱敏流程，仍需真实框架 guardrail/HITL 覆盖范围实验。 |
| 多 Agent 不是默认更好，会带来成本、调试和协调复杂度。 | AutoGen docs；CrewAI docs；AgentBench；Evidence Note: 多 Agent 不是默认更好；多 Agent 与 Flow 控制对比实验结果 | 部分验证 | 可作为 Planning / Orchestration 和框架生态章节的核心提醒；标准库实验已验证无控制多 Agent 的重复读取、缺证据和冲突风险，仍需真实模型 / 框架 / 成本实验。 |
| Agent 框架应按任务难点比较，不应写成“某个框架默认最好”。 | OpenAI Agents SDK docs；LangGraph docs；LlamaIndex docs；AutoGen docs；CrewAI docs；Semantic Kernel docs；Evidence Note: 框架生态定位边界；框架选择 Rubric Smoke Test 结果 | 部分验证 | 可作为框架生态章节核心边界；标准库 rubric 支撑任务画像和比较维度设计，仍需真实同一任务横向实验。 |
| 实践项目路线可以用 Cookbook 的具体 recipe 作为模板，但 Cookbook 不能替代 API 文档、生产安全指南或本地实验。 | OpenAI Cookbook；OpenAI Function Calling docs；OpenAI Responses API docs；OpenAI Evals repo；Evidence Note: 实践路线与 Cookbook 示例边界；实践路线 Smoke Harness 结果 | 部分验证 | 可作为第 11 章项目 reference；标准库 smoke harness 支撑验收标准、trace 和失败分类设计，仍需真实 Cookbook / API 试跑；必须引用具体 recipe，并提醒示例不是生产保证。 |
| MCP 是连接工具和上下文能力的协议，不是 Agent 框架本身。 | MCP official docs；MCP servers repo；Evidence Note: MCP Host / Client / Server 职责边界；MCP 最小 Trace 实验结果 | 部分验证 | 可作为 MCP 章节核心边界；最小模拟 trace 已验证职责流，仍需真实 MCP SDK / host trace 实验。 |
| MCP 标准化了工具、资源、提示、授权、roots、elicitation 和 sampling 等协议能力，但安全不是协议接入后自动完成。 | MCP official docs；MCP Security Best Practices；Evidence Note: MCP 安全、授权与权限边界；Production permission evidence；MCP 最小 Trace 实验结果 | 部分验证 | 可作为 MCP / Production 章节安全边界；需说明 authorization 是 optional，roots 不等于 sandbox，token passthrough 被禁止，模拟实验已验证 tool approval / resource review trace，仍需真实权限/URL/OAuth 实验。 |

## 待升级为可入正文的优先结论

1. Agent vs Workflow 的边界。已完成第一轮 OpenAI Agents SDK、LangGraph、ReAct 交叉验证和标准库 workflow / hybrid / ReAct-like 对比实验，待补真实模型 / 框架 / repo issue 实验。
2. Tool Use vs Function Calling 的边界。已完成第一轮官方文档交叉验证和标准库参数校验/重试模拟，待补真实模型 / API 实验和其他框架术语对照。
3. RAG vs Memory 的边界与工程 RAG 流程。已完成第一轮论文和框架文档交叉验证及标准库最小 RAG pipeline / citation 模拟，待补真实 embedding / vector store / LLM synthesis、chunk size/top-k/rerank 和成本/延迟实验。
4. MCP server/client/host 的职责边界与安全/授权/权限边界。已完成第一轮官方文档交叉验证和标准库最小 trace 模拟，待补真实 MCP SDK / host 的 trace、权限确认、URL mode / OAuth 和恶意 resource/prompt 实验。
5. Agent eval 为什么要看 trajectory。已完成第一轮 benchmark、eval framework、observability 工程资料交叉验证和标准库 trace-aware eval 模拟，待补真实 Agent trace、LLM-as-judge 误判分析和人工复核实验。
6. Prompt injection 为什么需要权限和隔离，而不是只靠提示词。已完成第一轮风险资料、框架工程资料交叉验证和标准库攻击/权限模拟，待补真实模型 / 框架 guardrail / HITL approval 误报漏报实验。
7. 长期记忆的收益与治理风险边界。已完成第一轮论文、工程文档、安全资料交叉验证和标准库写入守门模拟，待补真实多会话 Agent / memory framework 收益与污染实验。
8. 上下文工程与结构化输出边界。已完成第一轮官方文档交叉验证和标准库输出解析 / 上下文治理模拟实验，待补真实 Responses API / Structured Outputs、真实长上下文、RAG / 摘要 / 成本对比和跨模型稳定性实验。
9. Agent 架构模式边界。已完成 ReAct、Reflexion、Tree of Thoughts、LangGraph、已有 workflow/multi-agent evidence 第一轮交叉验证、标准库 workflow / ReAct-like、planner/executor 和 reflection/retry 对比，待补真实框架实验。
10. 框架生态定位边界。已完成主要框架文档第一轮交叉验证和标准库 rubric smoke test，待补真实同一任务横向实验。
11. 实践项目路线。已完成 OpenAI Cookbook 具体 recipe 第一轮验证和标准库 smoke harness，待补真实 Cookbook / API 最小项目试跑、成本估算和初学者跟练体验验证。

## 升级流程

每条候选结论升级前需要：

1. 找到至少 1 个 A 级 reference 的直接支撑。
2. 找到另一个独立来源做交叉验证，或设计最小实验。
3. 写出适用场景和不适用场景。
4. 写出初学者版表述，避免术语堆叠。
5. 在对应 source card 中记录证据，再迁移到章节正文。
