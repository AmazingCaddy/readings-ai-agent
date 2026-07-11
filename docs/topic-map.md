# AI Agent 主题地图 v1

这份主题地图用于保证学习手册的广度。每个主题后续都需要至少 2-3 个高可信 references，并区分入门解释、工程实践和进阶阅读。

## 1. 基础认知

核心问题：AI Agent 到底是什么？它和 Chatbot、Workflow、RAG 应用有什么区别？

需要覆盖：

- Agent 的定义和边界
- 自治程度：从工具增强聊天到可执行任务系统
- Agent 与 Workflow 的区别
- Agent 常见应用场景
- 初学者常见误区

## 2. LLM 与上下文工程

核心问题：Agent 为什么依赖 LLM？上下文如何影响 Agent 行为？

需要覆盖：

- 模型输入输出
- Prompt、system message、developer instruction
- Context window 与上下文压缩
- Structured output
- Failure modes：幻觉、遗漏、格式错误、指令冲突

## 3. Tool Use 与 Function Calling

核心问题：模型如何安全、可靠地调用外部能力？

需要覆盖：

- Tool schema
- Function calling 与 tool use 的关系
- 参数生成与校验
- 工具结果回传
- 权限和确认机制
- 工具失败与重试

## 4. Agent 架构模式

核心问题：Agent 的控制循环如何设计？什么时候不该用 Agent？

需要覆盖：

- ReAct
- Plan-and-Execute
- Reflection / Critic
- State machine
- Workflow-agent hybrid
- Human-in-the-loop
- 简单 workflow 替代方案

## 5. MCP 与工具生态

核心问题：MCP 解决什么问题？它如何连接模型、工具和数据源？

需要覆盖：

- MCP Server / Client / Host
- Tools、resources、prompts
- 权限边界
- 本地工具和远程工具
- 与传统 API wrapper 的区别

## 6. RAG、Memory 与知识库治理

核心问题：Agent 如何利用外部知识和长期记忆？

需要覆盖：

- RAG 基础流程
- Embedding、chunking、retrieval、reranking
- Short-term memory
- Long-term memory
- Memory 写入守门
- 过时、冲突和脏数据治理

## 7. Planning、Orchestration 与多 Agent

核心问题：复杂任务如何拆解、分配、恢复和汇总？

需要覆盖：

- Planner / Executor
- Task decomposition
- Queue 与状态持久化
- 多 Agent 协作模式
- 冲突、重复劳动和成本控制
- 人工审批点

## 8. Evaluation 与 Observability

核心问题：如何判断 Agent 是否真的更好？

需要覆盖：

- Offline eval
- Online metrics
- Trace 和 trajectory 分析
- Regression set
- Benchmark 的局限
- 错误分类：模型、工具、检索、权限、业务逻辑

## 9. Production、安全与成本

核心问题：Agent 如何从 demo 走到可维护系统？

需要覆盖：

- 权限模型
- Prompt injection
- 数据隔离
- 审计和日志
- 成本与延迟
- 回滚和降级
- 合规和隐私

## 10. 框架生态

核心问题：主流框架分别适合什么场景？初学者如何选择？

需要覆盖：

- OpenAI Agents SDK
- LangGraph
- LlamaIndex
- Microsoft AutoGen
- CrewAI
- Semantic Kernel
- 框架选择标准

## 11. 实践项目路线

核心问题：如何通过项目把概念变成能力？

需要覆盖：

- Toy tool-calling agent
- RAG 问答助手
- 个人资料整理 agent
- MCP 工具 agent
- 带 eval 的 agent
- 可部署生产 agent

