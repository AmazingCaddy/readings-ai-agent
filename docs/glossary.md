# 术语边界表

这份术语边界表用于保证手册的精度。它不是最终百科定义，而是给初学者建立清晰边界：什么是这个概念，什么不是，以及正文需要引用哪些 references。

## Agent

通俗理解：Agent 是一个能围绕目标反复观察、思考、调用工具并推进任务的系统。

精确定义：在本手册中，Agent 指围绕模型推理、工具调用、状态管理、控制循环和权限边界构建的任务执行系统。自治程度取决于系统是否允许它持续决策、调用工具、管理状态、处理反馈和判断何时停止。

不要混淆：

- Agent 不是简单聊天界面。
- Agent 不一定需要多 Agent。
- Agent 不等于“模型自己会思考”。实际自治来自系统设计和权限配置。
- 自治程度是连续谱和风险维度，不是能力等级；越自治越需要权限、trace、eval、成本和停止条件。

主要 references：OpenAI Agents SDK docs、LangGraph docs、ReAct paper、Evidence Note: Agent 自治程度边界。

## Workflow

通俗理解：Workflow 是事先设计好的步骤流程。

精确定义：Workflow 指由开发者明确规定步骤、分支、状态转移和工具调用顺序的系统。模型可以参与某些节点，但整体控制流主要由程序定义。

不要混淆：

- Workflow 可以使用 LLM，但不一定是 Agent。
- 很多任务用 workflow 比用高自治 Agent 更稳定、更便宜、更可调试。

主要 references：LangGraph docs、OpenAI Agents SDK docs。

## Tool Use

通俗理解：Tool Use 是让模型使用外部能力，例如搜索、计算、读文件、查数据库或调用 API。

精确定义：Tool Use 指模型基于上下文选择工具、生成结构化参数、接收工具结果，并把结果纳入后续推理或响应的机制。

不要混淆：

- Tool Use 是能力模式，Function Calling 是常见 API 实现方式之一。
- 工具调用是否安全，取决于 schema、权限、沙箱、确认机制和错误处理。

主要 references：OpenAI Function Calling docs、Toolformer paper、OpenAI Responses API docs。

## Function Calling

通俗理解：Function Calling 是 API 让模型按指定 schema 输出函数调用参数的一种机制。

精确定义：在现代 LLM API 中，Function Calling 通常指开发者提供函数或工具 schema，模型生成符合 schema 的调用请求，应用程序执行函数并把结果返回给模型。

不要混淆：

- Function Calling 本身不执行代码，真正执行发生在应用程序或工具运行时。
- Function Calling 不自动解决权限、安全和结果可信度问题。

主要 references：OpenAI Function Calling docs、OpenAI Responses API docs。

## MCP

通俗理解：MCP 是让模型应用以统一方式连接工具和数据源的协议。

精确定义：Model Context Protocol 用 host、client、server 等角色组织工具、资源和提示等上下文能力，使模型应用可以发现和使用外部能力。

不要混淆：

- MCP 不是 Agent 框架本身。
- MCP server 暴露能力，是否允许模型使用这些能力仍需要 host/client 和权限设计。

主要 references：MCP official docs、MCP servers repo。

## RAG

通俗理解：RAG 是先从外部知识库找相关资料，再让模型基于资料回答。

精确定义：Retrieval-Augmented Generation 指把检索到的外部信息作为生成模型的上下文，以提升知识密集型任务中的可追溯性、可更新性和事实性。

不要混淆：

- RAG 不是长期记忆。
- RAG 不能保证答案正确；检索质量、chunking、reranking、引用处理都会影响结果。

主要 references：RAG paper、LlamaIndex docs。

## Memory

通俗理解：Memory 是 Agent 在当前对话之外保存和使用信息的能力。

精确定义：Memory 指系统对用户、任务、环境或历史交互的状态持久化、检索、更新和治理机制。它可以是短期状态、长期记忆、向量检索、结构化事实、知识图谱或分层上下文管理。

不要混淆：

- Memory 不等于把历史对话全部塞进 prompt。
- Memory 不一定提升表现；错误写入、过时信息、隐私泄露和冲突事实都可能降低可靠性。
- RAG 偏向外部知识检索，Memory 偏向系统状态和历史经验管理，但两者会重叠。

主要 references：MemGPT paper、MemoryBank paper、Generative Agents paper、LangGraph memory docs。

## Planning

通俗理解：Planning 是把目标拆成步骤，并决定下一步做什么。

精确定义：Planning 指模型或系统生成、选择、调整任务步骤的过程。它可以发生在一次推理中，也可以作为 planner/executor 架构中的显式组件。

不要混淆：

- Planning 不等于可靠执行。
- 计划越复杂，越需要状态跟踪、工具反馈、错误恢复和人工确认。

主要 references：Tree of Thoughts paper、ReAct paper、LangGraph docs。

## Orchestration

通俗理解：Orchestration 是把多个步骤、工具、模型或 Agent 编排起来。

精确定义：Orchestration 指系统层面对任务流、状态、工具调用、分支、重试、并发、人工确认和恢复策略的组织。

不要混淆：

- Orchestration 更偏工程控制流，Planning 更偏任务决策。
- 多 Agent 是一种 orchestration 形态，不是唯一形态。

主要 references：LangGraph docs、AutoGen docs、Semantic Kernel docs。

## Evaluation

通俗理解：Evaluation 是判断 Agent 是否真的做得更好。

精确定义：Evaluation 包括离线测试、在线指标、人工评审、任务成功率、工具调用轨迹、错误分类和回归测试。Agent eval 不应只看最终答案，也要看过程是否可控、安全和可恢复。

不要混淆：

- Benchmark 是评测的一种，不等于真实业务质量。
- Observability 是记录和分析运行过程，不等于自动给出质量分数。

主要 references：AgentBench paper、WebArena paper、OpenAI Evals repo。

## Prompt Injection

通俗理解：Prompt Injection 是外部输入试图欺骗模型忽略原本指令或越权调用工具。

精确定义：在 Agent 系统中，Prompt Injection 是攻击者通过用户输入、网页、文档、工具结果或其他上下文注入恶意指令，诱导模型泄露信息、执行越权操作或破坏系统目标的风险。

不要混淆：

- Prompt Injection 不是只靠改 prompt 就能彻底解决。
- 工具权限、数据隔离、确认机制、审计和最小权限原则同样重要。

主要 references：OWASP LLM Top 10、NIST AI RMF。
