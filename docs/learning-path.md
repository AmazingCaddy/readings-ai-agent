# 初学者学习路径

这份路径用于保证手册由浅入深。读者不需要先读论文，也不需要一开始就选框架。

## 阶段 1：建立地图

目标：知道 AI Agent 是什么，以及它和 Chatbot、Workflow、RAG 应用的区别。

先读：

- [主题地图](topic-map.md)
- [章节目录](chapter-outline.md)
- [术语边界表](glossary.md)

需要能回答：

- Agent 和普通聊天机器人有什么区别？
- 为什么很多任务用 workflow 比 Agent 更合适？
- Tool Use、RAG、Memory 分别解决什么问题？

不要求：

- 不要求理解所有框架。
- 不要求读完整论文。

## 阶段 2：理解最小 Agent

目标：理解一个最小工具型 Agent 的组成。

重点主题：

- LLM 输入输出
- Tool schema
- Function calling
- 工具执行和结果回传
- 状态和错误处理

建议 references：

- OpenAI Function Calling docs
- OpenAI Responses API docs
- Toolformer paper 作为研究背景

实践输出：

- 设计一个只会调用 1 个工具的 Agent。
- 写出工具失败时的处理策略。

## 阶段 3：理解架构模式

目标：理解为什么 Agent 需要控制循环、状态和编排。

重点主题：

- ReAct
- Plan-and-Execute
- State machine
- Workflow-agent hybrid
- Human-in-the-loop

建议 references：

- ReAct paper
- LangGraph docs
- Tree of Thoughts paper 作为进阶规划资料

实践输出：

- 比较固定 workflow 和 ReAct 风格工具循环在同一任务上的差异。

## 阶段 4：理解知识与记忆

目标：区分 RAG、短期记忆、长期记忆和知识库治理。

重点主题：

- Retrieval
- Chunking
- Reranking
- Short-term memory
- Long-term memory
- Memory 写入守门
- 冲突、过时和隐私风险

建议 references：

- RAG paper
- LlamaIndex docs
- MemGPT paper
- MemoryBank paper
- LangGraph memory docs

实践输出：

- 设计一个知识库问答 baseline。
- 设计一个 memory 写入规则，说明哪些信息不能自动写入。

## 阶段 5：理解评测和安全

目标：能判断 Agent 是否真的可靠，而不是只看 demo 效果。

重点主题：

- Offline eval
- Trace / trajectory
- Regression set
- Prompt injection
- Tool permissions
- Audit log

建议 references：

- AgentBench paper
- WebArena paper
- OpenAI Evals repo
- OWASP LLM Top 10
- NIST AI RMF

实践输出：

- 为一个最小 Agent 建 10 条回归测试。
- 设计一个 prompt injection 基线测试。

## 阶段 6：比较框架并做项目

目标：能根据任务选择框架，而不是跟风选最热门的。

比较维度：

- 学习成本
- 控制力
- 可观测性
- 状态管理
- 多 Agent 支持
- 部署和安全边界

建议 references：

- OpenAI Agents SDK docs
- LangGraph docs
- LlamaIndex docs
- AutoGen docs
- Semantic Kernel docs
- CrewAI docs

实践输出：

- 选一个小项目，用至少两个框架做方案对比。
- 写清楚为什么选择其中一个，而不是只列功能。

