# Source Card 索引

本索引用来汇总每张 source card 的状态。source card 只有完成精读和交叉验证后，才能把关键结论迁移进章节正文。

## 已创建卡片

| Source card | 主题 | 类型 | 可信度 | 当前验证状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| [ReAct paper](source-cards/2022-react-paper.md) | Agent 架构 / Tool Use | Paper | A | 链接已复核；待精读 | 提取作者、摘要、核心结论；与框架文档交叉验证 |
| [RAG paper](source-cards/2020-rag-paper.md) | RAG | Paper | A | 链接已复核；待精读 | 提取 RAG 基本定义和局限；与现代 RAG 文档对比 |
| [Toolformer paper](source-cards/2023-toolformer-paper.md) | Tool Use | Paper | A | 链接已复核；待精读 | 区分研究式 tool use 与现代 function calling |
| [Tree of Thoughts paper](source-cards/2023-tree-of-thoughts-paper.md) | Planning | Paper | A | 链接已复核；待精读 | 判断是否适合作为初学者正文或进阶资料 |
| [Reflexion paper](source-cards/2023-reflexion-paper.md) | Reflection / Eval | Paper | A | 链接已复核；待精读 | 验证 reflection 的适用边界 |
| [AgentBench paper](source-cards/2023-agentbench-paper.md) | Eval / Benchmark | Paper | A | 链接已复核；待精读 | 提取 benchmark 覆盖任务和局限 |
| [WebArena paper](source-cards/2023-webarena-paper.md) | Web Agent / Eval | Paper | A | 链接已复核；待精读 | 归纳 Web Agent 评测复杂度 |
| [MCP official docs](source-cards/2026-mcp-official-docs.md) | MCP | Official Docs | A | 链接已复核；待精读 | 提取 MCP 组件定义和安全边界 |
| [OpenAI Agents SDK docs](source-cards/2026-openai-agents-sdk-docs.md) | Agent Framework | Official Docs | A | 链接已复核；待精读 | 提取 SDK 抽象、tools、handoffs、tracing |

## 待创建高优先级卡片

| 候选来源 | 主题 | 理由 |
| --- | --- | --- |
| OpenAI tool calling / function calling docs | Tool Use | 需要现代 API 官方定义 |
| OpenAI Responses API docs | LLM 应用架构 | 需要现代接口上下文 |
| LangGraph docs | Agent 架构 / 状态图 | 需要工程化 orchestration reference |
| LlamaIndex docs | RAG / Agent / Data framework | 需要 RAG 和数据连接工程 reference |
| OWASP Top 10 for LLM Applications | Security | 需要安全章节基础 reference |
| NIST AI RMF | Risk / Governance | 需要生产化风险管理 reference |
| OpenAI Evals repository | Evaluation | 需要 eval 实践和源码 reference |
| MCP example servers | MCP / Tools | 需要工具生态源码 reference |

