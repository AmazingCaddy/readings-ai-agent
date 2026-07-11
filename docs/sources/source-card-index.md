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
| [OpenAI Function Calling docs](source-cards/2026-openai-function-calling-docs.md) | Tool Use / Function Calling | Official Docs | A | 链接已复核；待精读 | 提取 tool schema、参数生成和工具结果回传机制 |
| [MCP official docs](source-cards/2026-mcp-official-docs.md) | MCP | Official Docs | A | 链接已复核；待精读 | 提取 MCP 组件定义和安全边界 |
| [LangGraph docs](source-cards/2026-langgraph-docs.md) | Agent 架构 / Orchestration | Framework Docs | A | 链接已复核；待精读 | 提取 state graph、workflow 和持久化相关抽象 |
| [LlamaIndex docs](source-cards/2026-llamaindex-docs.md) | RAG / Data framework | Framework Docs | A | 链接已复核；待精读 | 提取 RAG 数据组件和 agent data framework 抽象 |
| [NIST AI RMF](source-cards/2026-nist-ai-rmf.md) | Risk / Governance | Standard / Guidance | A | 链接已复核；待精读 | 提取生产化风险管理检查点 |
| [OpenAI Agents SDK docs](source-cards/2026-openai-agents-sdk-docs.md) | Agent Framework | Official Docs | A | 链接已复核；待精读 | 提取 SDK 抽象、tools、handoffs、tracing |
| [OpenAI Responses API docs](source-cards/2026-openai-responses-api-docs.md) | LLM 应用接口 | Official Docs | A | 链接已复核；待精读 | 提取输入输出、响应结构和工具调用接口 |
| [OWASP LLM Top 10](source-cards/2026-owasp-llm-top-10.md) | Security | Security Guidance | A | 链接已复核；待精读 | 提取 Agent 安全风险分类和检查清单 |

## 待创建高优先级卡片

| 候选来源 | 主题 | 理由 |
| --- | --- | --- |
| OpenAI Evals repository | Evaluation | 需要 eval 实践和源码 reference |
| MCP example servers | MCP / Tools | 需要工具生态源码 reference |
