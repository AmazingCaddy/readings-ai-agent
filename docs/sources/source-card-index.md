# Source Card 索引

本索引用来汇总每张 source card 的状态。source card 只有完成精读和交叉验证后，才能把关键结论迁移进章节正文。

## 已创建卡片

| Source card | 主题 | 类型 | 可信度 | 当前验证状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| [ReAct paper](source-cards/2022-react-paper.md) | Agent 架构 / Tool Use | Paper | A | 链接已复核；待精读 | 提取作者、摘要、核心结论；与框架文档交叉验证 |
| [RAG paper](source-cards/2020-rag-paper.md) | RAG | Paper | A | 链接已复核；待精读 | 提取 RAG 基本定义和局限；与现代 RAG 文档对比 |
| [Generative Agents paper](source-cards/2023-generative-agents-paper.md) | Memory / Reflection / Planning | Paper | A | 元数据已复核；待精读 | 提取 observation、planning、reflection 与 memory 关系 |
| [MemoryBank paper](source-cards/2023-memorybank-paper.md) | Long-term memory | Paper | A | 元数据已复核；待精读 | 提取长期记忆更新、遗忘和用户画像边界 |
| [MemGPT paper](source-cards/2023-memgpt-paper.md) | Memory management / Context | Paper | A | 元数据已复核；待精读 | 提取 virtual context management 和 memory tier 设计 |
| [Toolformer paper](source-cards/2023-toolformer-paper.md) | Tool Use | Paper | A | 链接已复核；待精读 | 区分研究式 tool use 与现代 function calling |
| [Tree of Thoughts paper](source-cards/2023-tree-of-thoughts-paper.md) | Planning | Paper | A | 链接已复核；待精读 | 判断是否适合作为初学者正文或进阶资料 |
| [Reflexion paper](source-cards/2023-reflexion-paper.md) | Reflection / Eval | Paper | A | 链接已复核；待精读 | 验证 reflection 的适用边界 |
| [AgentBench paper](source-cards/2023-agentbench-paper.md) | Eval / Benchmark | Paper | A | 链接已复核；待精读 | 提取 benchmark 覆盖任务和局限 |
| [WebArena paper](source-cards/2023-webarena-paper.md) | Web Agent / Eval | Paper | A | 链接已复核；待精读 | 归纳 Web Agent 评测复杂度 |
| [AutoGen docs](source-cards/2026-autogen-docs.md) | Multi-agent / Framework | Framework Docs | A | 链接已复核；待精读 | 提取多 Agent 协作抽象和适用边界 |
| [CrewAI docs](source-cards/2026-crewai-docs.md) | Multi-agent / Framework | Framework Docs | B | 链接已复核；待精读 | 和 AutoGen / LangGraph 横向比较 |
| [MCP servers repo](source-cards/2026-mcp-servers-repo.md) | MCP / Examples | Source Code | A | 链接已复核；待精读 | 提取 MCP server 示例结构和权限假设 |
| [OpenAI Function Calling docs](source-cards/2026-openai-function-calling-docs.md) | Tool Use / Function Calling | Official Docs | A | 链接已复核；待精读 | 提取 tool schema、参数生成和工具结果回传机制 |
| [MCP official docs](source-cards/2026-mcp-official-docs.md) | MCP | Official Docs / Spec | A | 关键 spec / security / authorization 页面已精读；部分验证 | 运行最小 MCP trace、权限确认和恶意 resource/prompt 实验 |
| [LangGraph docs](source-cards/2026-langgraph-docs.md) | Agent 架构 / Orchestration | Framework Docs | A | 链接已复核；待精读 | 提取 state graph、workflow 和持久化相关抽象 |
| [LangGraph memory docs](source-cards/2026-langgraph-memory-docs.md) | Short-term / Long-term memory | Framework Docs | A | 链接已复核；待精读 | 提取短期/长期记忆边界和状态管理实践 |
| [Letta docs](source-cards/2026-letta-docs.md) | Agent memory / Stateful agents | Framework Docs | B | 链接已复核；待精读 | 和 MemGPT 论文及其他 memory 框架对照 |
| [LlamaIndex docs](source-cards/2026-llamaindex-docs.md) | RAG / Data framework | Framework Docs | A | 链接已复核；待精读 | 提取 RAG 数据组件和 agent data framework 抽象 |
| [NIST AI RMF](source-cards/2026-nist-ai-rmf.md) | Risk / Governance | Standard / Guidance | A | 链接已复核；待精读 | 提取生产化风险管理检查点 |
| [OpenAI Agents SDK docs](source-cards/2026-openai-agents-sdk-docs.md) | Agent Framework | Official Docs | A | 关键页面已精读；部分验证 | 继续做 guardrails/HITL/tool permission 最小实验和框架横向对比 |
| [OpenAI Cookbook](source-cards/2026-openai-cookbook.md) | Examples / Practice | Official Examples | A/B | 具体 recipe 已复核；部分验证 | 本地试跑最小项目并记录成本、失败样例和初学者阻塞点 |
| [OpenAI Evals repo](source-cards/2026-openai-evals-repo.md) | Eval / Source Code | Source Code | A | 链接已复核；待精读 | 提取 eval 数据结构和回归测试实践 |
| [OpenAI Responses API docs](source-cards/2026-openai-responses-api-docs.md) | LLM 应用接口 | Official Docs | A | 链接已复核；待精读 | 提取输入输出、响应结构和工具调用接口 |
| [OWASP LLM Top 10](source-cards/2026-owasp-llm-top-10.md) | Security | Security Guidance | A | 链接已复核；待精读 | 提取 Agent 安全风险分类和检查清单 |
| [Semantic Kernel docs](source-cards/2026-semantic-kernel-docs.md) | Framework / Enterprise integration | Framework Docs | A | 链接已复核；待精读 | 提取插件、工具和编排抽象 |
| [LangSmith docs](source-cards/2026-langsmith-docs.md) | Observability / Evaluation | Framework Docs | B | 关键页面已精读；部分验证 | 结合本地 trace-aware eval 实验验证字段清单和误判率 |
| [Arize Phoenix docs](source-cards/2026-arize-phoenix-docs.md) | Observability / Evaluation | Framework Docs | B | 关键页面已精读；部分验证 | 结合本地 trace-aware eval 实验验证 traces/spans/sessions 设计 |
| [Zep docs](source-cards/2026-zep-docs.md) | Agent memory / Knowledge graph | Framework Docs | B | 链接已复核；待精读 | 提取工程 memory 系统的冲突和过时信息处理思路 |

## 待创建高优先级卡片

| 候选来源 | 主题 | 理由 |
| --- | --- | --- |
| Prompt injection papers and security writeups | Security | 需要攻击样例和防护工程实践 |
| Memory write-guard and knowledge governance engineering cases | Memory | 仍需专门调查写入守门、冲突治理和隐私边界 |
