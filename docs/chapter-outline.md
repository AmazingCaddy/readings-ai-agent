# 章节目录 v1

本目录按初学者学习曲线组织，先建立直觉，再逐步进入工程机制和生产化。

## 00. 序言：如何学习 AI Agent

- 适合谁：没有系统学过 Agent 的工程师或学习者。
- 核心问题：为什么需要这本手册？如何判断资料是否可靠？
- 输出物：学习路线、资料校验方法、实践项目路径。

## 01. AI Agent 是什么

- 先解释 Agent、Chatbot、Workflow、RAG 应用的区别。
- 再讨论自治程度和常见应用场景。
- 最后列出初学者最容易误解的概念。

## 02. LLM 基础与上下文工程

- 解释模型输入输出和上下文窗口。
- 介绍 prompt、system instruction、structured output。
- 说明上下文污染、遗漏和格式失败。

## 03. Tool Use、Function Calling 与 Structured Output

- 解释工具 schema、参数生成、工具结果回传。
- 说明工具调用失败如何处理。
- 讨论权限、确认和 sandbox。

## 04. Agent 架构模式

- 介绍 ReAct、Plan-and-Execute、Reflection、状态机。
- 对比 workflow 和 agent。
- 说明什么时候不用 agent 更好。

## 05. MCP 与工具生态

- 解释 MCP 的目标和基本组件。
- 区分 MCP server、client、host。
- 讨论 tools、resources、prompts 和权限边界。

## 06. RAG、Memory 与知识库治理

- 解释 RAG 和 memory 的区别。
- 介绍 embedding、chunking、retrieval、reranking。
- 讨论长期记忆写入、冲突和过时治理。

## 07. Planning、Orchestration 与多 Agent

- 解释任务拆解和编排。
- 介绍 planner/executor、critic、human-in-the-loop。
- 讨论多 agent 的成本和复杂度。

## 08. Evaluation 与 Observability

- 解释 eval、benchmark、observability 的区别。
- 介绍 trace、trajectory、regression set。
- 给出错误分类方法。

## 09. Production：安全、权限、成本与部署

- 讨论 prompt injection、权限模型和数据边界。
- 介绍审计、日志、成本和延迟优化。
- 说明上线后的回滚和降级策略。

## 10. 框架生态比较

- 比较 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI、Semantic Kernel。
- 从学习成本、控制力、生态、可观测性、生产化角度评估。

## 11. 实践项目路线

- 从最小 tool-calling agent 开始。
- 逐步加入 RAG、memory、MCP、eval、部署。
- 每个项目给出学习目标、验收标准和 references。

## 12. 论文、文档与资料地图

- 按主题整理官方文档、论文、框架文档、工程博客和课程。
- 标注可信度、适合阶段和验证状态。

