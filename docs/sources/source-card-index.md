# Source Card 索引

本索引用来汇总每张 source card 的状态。source card 只有完成精读和交叉验证后，才能把关键结论迁移进章节正文。

## 已创建卡片

| Source card | 主题 | 类型 | 可信度 | 当前验证状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| [ReAct paper](source-cards/2022-react-paper.md) | Agent 架构 / Tool Use | Paper | A | 摘要/核心模式已精读；与 Agent/Workflow 和架构 evidence 交叉验证；部分验证 | 补真实模型 / 框架任务对比，避免泛化为 ReAct 默认更优 |
| [RAG paper](source-cards/2020-rag-paper.md) | RAG | Paper | A | 摘要和关键动机已精读；RAG / Memory 术语边界已可入正文；工程质量仍部分验证 | 补真实 RAG stack、citation correctness 和成本/延迟实验 |
| [Generative Agents paper](source-cards/2023-generative-agents-paper.md) | Memory / Reflection / Planning | Paper | A | 摘要和 memory/reflection/planning 关系已精读；长期记忆治理 evidence 已引用；部分验证 | 补真实多会话 Agent / memory framework 收益与污染实验 |
| [MemoryBank paper](source-cards/2023-memorybank-paper.md) | Long-term memory | Paper | A | 摘要和长期记忆更新/遗忘方向已精读；长期记忆治理 evidence 已引用；部分验证 | 补真实长期记忆收益、过时和隐私实验 |
| [MemGPT paper](source-cards/2023-memgpt-paper.md) | Memory management / Context | Paper | A | 摘要和显式 memory management 方向已精读；RAG/Memory 与长期记忆 evidence 已引用；部分验证 | 补真实 memory tier / context management 实验 |
| [Toolformer paper](source-cards/2023-toolformer-paper.md) | Tool Use | Paper | A | 摘要和研究式 tool use 边界已精读；Function Calling evidence 已引用；部分验证 | 补真实 API tool-calling validation / retry 实验 |
| [Tree of Thoughts paper](source-cards/2023-tree-of-thoughts-paper.md) | Planning | Paper | A | 摘要和搜索式推理边界已精读；架构模式 evidence 已引用；部分验证 | 补真实 planning/search 与 workflow 对比实验 |
| [Reflexion paper](source-cards/2023-reflexion-paper.md) | Reflection / Eval | Paper | A | 摘要和语言反馈/反思边界已精读；reflection retry 实验已完成；部分验证 | 补真实 critic、长期 episodic memory、成本和人工评审实验 |
| [AgentBench paper](source-cards/2023-agentbench-paper.md) | Eval / Benchmark | Paper | A | 摘要和 benchmark / trajectory 边界已精读；支撑工具/副作用 Agent 不能只看最终答案的窄结论；其余部分验证 | 补真实 Agent trace、LLM-as-judge 和人工复核实验 |
| [WebArena paper](source-cards/2023-webarena-paper.md) | Web Agent / Eval | Paper | A | 摘要和 Web Agent 评测复杂度已精读；支撑过程/交互评测窄结论；其余部分验证 | 补真实 web/tool trace 评测和失败分类实验 |
| [AutoGen docs](source-cards/2026-autogen-docs.md) | Multi-agent / Framework | Framework Docs | A | 关键多 Agent/Teams/GraphFlow 段落已精读；multi-agent evidence、框架能力交叉表和框架 rubric 已引用；部分验证 | 补真实 AutoGen / CrewAI / LangGraph 同任务横向实验 |
| [CrewAI docs](source-cards/2026-crewai-docs.md) | Multi-agent / Framework | Framework Docs | B | Introduction / Flows / Crews 抽象已精读；multi-agent evidence 和框架能力交叉表已引用；部分验证 | 和 AutoGen / LangGraph 做真实横向比较，避免营销式结论 |
| [MCP servers repo](source-cards/2026-mcp-servers-repo.md) | MCP / Examples | Source Code | A | README / reference implementations 已复核；MCP role evidence 已引用；部分验证 | 补真实 MCP server 示例结构、权限假设和 host trace 实验 |
| [OpenAI Function Calling docs](source-cards/2026-openai-function-calling-docs.md) | Tool Use / Function Calling | Official Docs | A | “Function Calling 本身不执行工具”已可入正文；参数校验/重试模拟实验已完成；真实 API harness 已准备；真实修正稳定性仍部分验证 | 实际运行真实模型 / API 实验并补其他框架术语对照 |
| [MCP official docs](source-cards/2026-mcp-official-docs.md) | MCP | Official Docs / Spec | A | host/client/server 职责边界已可入正文；security / authorization 页面已精读；MCP trace 模拟和 stdio harness 已完成；真实 host 行为仍部分验证 | 补真实 MCP SDK / host trace、权限确认、URL mode / OAuth 和恶意 resource/prompt 实验 |
| [LangGraph docs](source-cards/2026-langgraph-docs.md) | Agent 架构 / Orchestration | Framework Docs | A | 关键 stateful workflow / agent / durable execution / HITL 段落已精读；多个 architecture evidence 和框架能力交叉表已引用；部分验证 | 补真实 LangGraph workflow / agent 对比实验 |
| [LangGraph memory docs](source-cards/2026-langgraph-memory-docs.md) | Short-term / Long-term memory | Framework Docs | A | 关键 short-term / long-term memory 边界已精读；RAG / Memory 术语边界已可入正文；真实 memory framework 行为仍部分验证 | 补真实 memory framework、用户编辑/删除和多会话收益实验 |
| [Letta docs](source-cards/2026-letta-docs.md) | Agent memory / Stateful agents | Framework Docs | B | 关键 memory inspection/editing/versioning 段落已精读；长期记忆治理 evidence 和 lifecycle audit 已引用；部分验证 | 和 Zep / LangGraph 做真实 memory governance 对比实验 |
| [LlamaIndex docs](source-cards/2026-llamaindex-docs.md) | RAG / Data framework | Framework Docs | A | 关键页面已精读；RAG pipeline / citation 模拟实验、上下文策略对比实验和框架能力交叉表已完成；真实 LLM citation harness 已准备；部分验证 | 实际运行 LLM citation harness，并补真实 embedding / LlamaIndex pipeline、metadata filter 和 citation correctness 实验 |
| [NIST AI RMF](source-cards/2026-nist-ai-rmf.md) | Risk / Governance | Standard / Guidance | A | 关键风险治理段落已精读；security / memory / production evidence 已引用；支撑生产安全治理边界；安全 regression set 已完成；具体 Agent 控制仍部分验证 | 补真实风险评审清单和生产安全试跑 |
| [OpenAI Agents SDK docs](source-cards/2026-openai-agents-sdk-docs.md) | Agent Framework | Official Docs | A | 关键页面已精读；prompt injection / permission 标准库实验、安全 regression set、审批状态恢复实验和框架能力交叉表已完成；高风险工具权限窄边界可入正文；真实 guardrails/HITL 覆盖仍部分验证 | 补真实 guardrails/HITL/tool permission 和框架横向对比实验 |
| [OpenAI Cookbook](source-cards/2026-openai-cookbook.md) | Examples / Practice | Official Examples | A/B | 具体 recipe 已复核；部分验证 | 本地试跑最小项目并记录成本、失败样例和初学者阻塞点 |
| [OpenAI Evals repo](source-cards/2026-openai-evals-repo.md) | Eval / Source Code | Source Code | A | README 和 custom eval 方向已精读；trace-aware eval 和 trace schema audit 已完成；工具/副作用 Agent 的 trace-aware eval 窄边界可入正文；真实模型 trace harness 已准备 | 实际运行真实 eval harness、LLM-as-judge 误判和人工复核实验 |
| [OpenAI Responses API docs](source-cards/2026-openai-responses-api-docs.md) | LLM 应用接口 | Official Docs | A | 输入/输出、tool、structured output、permission 字段已精读；多个 evidence 已引用；P0 真实 API harness 已准备；部分验证 | 实际运行 Responses API / Structured Outputs / tool validation retry 实验 |
| [OpenAI Structured Outputs docs](source-cards/2026-openai-structured-outputs-docs.md) | Structured Outputs / JSON Schema | Official Docs | A | “schema valid 不等于事实/权限/业务正确”已可入正文；标准库上下文/结构化输出实验已完成；真实 API harness 已准备；真实 refusal/retry 稳定性仍部分验证 | 实际运行真实 Structured Outputs / JSON mode / refusal / semantic validator 实验 |
| [OpenAI Text Generation docs](source-cards/2026-openai-text-generation-docs.md) | Text Generation / Context | Official Docs | A | output array、message roles、instructions 和 context window 边界已精读；上下文治理实验和上下文策略对比实验已完成；部分验证 | 补真实 Responses API 输出结构、长上下文 / RAG / 摘要成本和跨模型稳定性实验 |
| [OWASP LLM Top 10](source-cards/2026-owasp-llm-top-10.md) | Security | Security Guidance | A | 关键风险项已精读；prompt injection / permission evidence 已引用；prompt 不是充分安全边界的窄结论可入正文；安全 regression set 已完成；真实 API harness 已准备 | 实际运行真实攻击样例和框架 guardrail，记录误报/漏报 |
| [Semantic Kernel docs](source-cards/2026-semantic-kernel-docs.md) | Framework / Enterprise integration | Framework Docs | A | 插件、task automation、agent framework、process framework 段落已精读；framework/security evidence、审批状态恢复实验和框架能力交叉表已引用；高风险工具权限窄边界可入正文；真实插件/HITL 行为仍部分验证 | 补真实 Semantic Kernel plugin / HITL / process 对比实验 |
| [LangSmith docs](source-cards/2026-langsmith-docs.md) | Observability / Evaluation | Framework Docs | B | 关键页面已精读；trace-aware eval 和 trace schema audit 标准库实验已完成；trace 作为 eval/审计/回归输入的窄边界可入正文；真实模型 trace harness 已准备 | 实际运行真实平台 traces、LLM-as-judge 误判和人工复核实验 |
| [Arize Phoenix docs](source-cards/2026-arize-phoenix-docs.md) | Observability / Evaluation | Framework Docs | B | 关键页面已精读；trace-aware eval 和 trace schema audit 标准库实验已完成；trace 作为 eval/审计/回归输入的窄边界可入正文；真实模型 trace harness 已准备 | 实际运行真实平台 traces/spans/sessions、token/latency 和人工复核实验 |
| [Zep docs](source-cards/2026-zep-docs.md) | Agent memory / Knowledge graph | Framework Docs | B | 关键 temporal graph / fact invalidation 段落已精读；长期记忆治理 evidence 和 lifecycle audit 已引用；部分验证 | 补真实 Zep / Letta / LangGraph memory governance 对比实验 |

## 待创建高优先级卡片

| 候选来源 | 主题 | 理由 |
| --- | --- | --- |
| Prompt injection papers and security writeups | Security | 已有 OWASP/NIST 和标准库攻击实验；仍需要更多真实攻击样例、防护工程实践和误报/漏报资料 |
| Memory framework implementation case studies | Memory | 已有 Letta/Zep/LangGraph 第一轮资料、标准库写入守门和 lifecycle audit；仍需真实 memory framework 的用户查看/编辑/删除、权限和隐私边界案例 |
