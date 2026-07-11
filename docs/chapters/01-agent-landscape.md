# AI Agent 是什么

## 本章适合谁

如果你听过 Agent、AI Agent、LLM Agent、Autonomous Agent，但不确定它们和普通聊天机器人、RAG 应用、Workflow 有什么区别，先读这一章。

本章不会先介绍具体框架，而是先建立概念边界。

## 你会学到什么

- Agent 的通俗理解和工作定义。
- Agent、Chatbot、Workflow、RAG 应用的区别。
- 为什么自治程度不是越高越好。
- 初学者判断一个系统是否需要 Agent 的方法。
- 当前结论有哪些 references，哪些还需要继续验证。

## 先用一句话理解

AI Agent 不是“会自己思考的 AI”，而是围绕模型推理、工具调用、状态管理和目标执行设计出来的系统。

## 基础概念

在本手册中，Agent 指围绕模型推理、工具调用、状态管理、控制循环和权限边界构建的任务执行系统。自治程度取决于系统是否允许它持续决策、调用工具、管理状态并处理反馈。

这个定义刻意强调“系统”。原因是：LLM 本身只负责根据输入生成输出。一个 Agent 能不能观察环境、调用工具、记住状态、重试失败、请求人工确认、停止执行，取决于应用层如何设计。

自治程度可以帮助理解 Agent，但它不是能力等级。更高自治通常意味着系统把更多下一步决策、工具选择、失败恢复和停止判断交给模型或 runtime；这可能增加灵活性，也会增加权限、成本、trace 和评测压力。

可以用四个问题判断一个系统是不是更接近 Agent：

1. 它是否有一个明确目标，而不是只回答单轮问题？
2. 它是否能根据中间结果决定下一步？
3. 它是否能调用外部工具或访问外部环境？
4. 它是否有状态、记忆、日志或执行轨迹？

如果答案大多是“是”，它通常比普通聊天机器人更接近 Agent。

## Agent、Chatbot、Workflow、RAG 的区别

### Chatbot

Chatbot 的核心是对话。它可以非常有用，但如果它只是接收用户问题并生成回答，没有持续目标、工具调用和状态管理，就不应该直接叫 Agent。

### Workflow

Workflow 是事先设计好的步骤流程。开发者明确规定步骤、分支、状态转移和工具调用顺序。Workflow 可以使用 LLM，但整体控制流主要由程序定义。

很多任务更适合 workflow，而不是高自治 Agent。比如固定表单处理、固定审批流程、格式转换、批量分类。这些任务需要稳定、可预测、可审计，高自治反而可能增加风险。

Workflow 和 Agent 不是互斥关系。OpenAI Agents SDK 和 LangGraph 的文档都把 agent、workflow、runtime、orchestration 放在同一个工程语境里：有些系统由程序控制主要流程，只在不确定步骤调用模型；有些系统让 Agent runtime 管理工具循环、状态和 handoff。

### RAG 应用

RAG 是先检索外部知识，再让模型基于检索结果回答。RAG 应用可以只是一个问答系统，也可以成为 Agent 的一个组件。

RAG 解决的是“模型如何利用外部知识”的问题；Agent 解决的是“系统如何围绕目标持续决策和执行”的问题。两者可以结合，但不是同一个概念。

### Agent

Agent 更关注任务执行过程：目标、状态、工具、反馈、控制循环和权限。它可能使用 RAG，也可能使用 workflow，也可能调用 MCP 工具或长期记忆系统。

## 通俗例子

假设你要查某个开源项目最近一次 release 的 breaking changes。

普通 Chatbot 可能根据已有知识回答，但可能过时。

RAG 应用可能从项目文档中检索 release notes，再总结。

Workflow 可能固定执行：打开 GitHub releases，找到最新版本，抓取 changelog，总结重点。

Agent 可能先判断该项目在哪里发布 release，再选择查 GitHub、文档站还是包管理器；如果找不到 release notes，它可能继续查 commit、issue 或 migration guide；如果遇到权限或不确定内容，它可能请求人工确认。

这个例子里，Agent 的关键不是“更聪明”，而是它有一个可持续推进任务的控制循环。

## 工作原理

一个最小 Agent 通常包含这些部分：

- 目标：系统要完成什么任务。
- 模型：负责理解上下文、生成决策或输出。
- 工具：搜索、读文件、调用 API、运行代码、查数据库等外部能力。
- 状态：当前任务进展、历史观察、已执行步骤、错误信息。
- 控制循环：决定下一步是继续推理、调用工具、请求用户、重试还是停止。
- 权限边界：哪些工具可以自动调用，哪些必须人工确认。
- 轨迹记录：保存模型推理摘要、工具调用、结果和失败原因，方便评测和调试。

不同框架会用不同术语表达这些组件。比如 OpenAI Agents SDK、LangGraph、AutoGen、Semantic Kernel 和 CrewAI 都有自己的抽象。因此本章只讲概念边界，不把某个框架的术语当成通用定义。

## 工程实践

设计 Agent 前，先问三个问题。

第一，任务是否真的需要动态决策？如果步骤固定，用 workflow 通常更稳。

第二，失败代价有多高？如果工具会发邮件、删数据、花钱或改生产系统，就必须有权限控制和人工确认。

第三，如何评估它是否完成任务？如果无法定义成功标准，就很难判断 Agent 是否真的有用。

一个保守的工程路线是：

1. 先做固定 workflow。
2. 再把不确定步骤交给模型判断。
3. 再加入工具调用。
4. 再加入状态和 trace。
5. 最后才考虑更高自治程度或多 Agent。

这条路线的重点不是“先低级、后高级”，而是先把可预测部分固定住，再把真正需要语言理解、工具选择或动态决策的部分交给模型。

## 常见误区

- Agent 不是所有 LLM 应用的高级形态。
- 自治程度越高，不代表系统越可靠。
- 多 Agent 不是默认架构。
- RAG、Memory、MCP 都可以是 Agent 的组件，但它们本身不等于 Agent。
- Demo 能跑通不代表可以上线。

## 什么时候不该用 Agent

以下场景通常不应优先使用高自治 Agent：

- 步骤固定且业务规则清楚。
- 输出必须严格可预测。
- 错误执行代价高，且缺少人工确认机制。
- 没有日志、trace 和回归测试。
- 团队还无法定义任务成功标准。

这些场景可以先用 workflow、规则系统、RAG 问答或人工审核流程。

## 已验证结论

- ReAct 论文直接支持“推理和行动可以交替进行”这一基础模式，但它不证明 ReAct 总是优于 workflow。
- OpenAI Agents SDK 文档支持“Agent runtime 可以管理工具循环、turns、guardrails、handoffs、sessions 和 tracing”的工程抽象，但它不是所有 Agent 系统的唯一通用定义。
- LangGraph 文档支持“底层 orchestration runtime 可以服务 long-running, stateful workflow or agent”的边界，因此 Agent 和 Workflow 更像控制权连续谱，而不是严格二分。
- “Agent vs Workflow”的边界已完成第一轮 OpenAI Agents SDK、LangGraph 和 ReAct 交叉验证，并完成标准库 workflow / hybrid / ReAct-like 对比实验。实验显示固定 workflow 工具调用最少但会漏掉需要证据查询的 root cause，hybrid 和 ReAct-like loop 可以补证据但成本更高；真实模型和框架实验仍待验证。
- “自治程度可以作为分类维度，但不是能力等级”已完成第一轮交叉验证：Agent/Workflow evidence 支持控制权连续谱，Prompt Injection evidence 支持 unchecked autonomy 的风险边界，标准库 workflow / hybrid / ReAct-like 对比实验支持灵活性与工具调用成本的权衡。

## 待验证问题

- workflow-agent hybrid 在具体任务中如何比纯 workflow 或高自治 Agent 更稳？
- 哪些任务类型有公开案例证明 Agent 优于固定 workflow？
- 初学者是否应该先学 workflow-agent hybrid，而不是直接学 autonomous agent？已完成第一轮边界验证，仍需真实模型 / 框架 / 成本实验。
- 多 Agent 的收益在哪些任务中能稳定超过额外成本？

## 本章小结

- Agent 是系统形态，不是单独的模型能力。
- Agent 的关键组件包括目标、模型、工具、状态、控制循环、权限边界和轨迹记录。
- Chatbot、Workflow、RAG 应用都可能使用 LLM，但它们和 Agent 的关注点不同。
- 选择 Agent 前要先判断任务是否真的需要动态决策。
- 工程上应先追求可控、可评测，再追求自治。

## References

### Official Docs

- [OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- [LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- [Microsoft AutoGen Documentation](../sources/source-cards/2026-autogen-docs.md)
- [Microsoft Semantic Kernel Documentation](../sources/source-cards/2026-semantic-kernel-docs.md)
- [CrewAI Documentation](../sources/source-cards/2026-crewai-docs.md)

### Papers

- [ReAct: Synergizing Reasoning and Acting in Language Models](../sources/source-cards/2022-react-paper.md)
- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](../sources/source-cards/2023-tree-of-thoughts-paper.md)

### Governance

- [术语边界表](../glossary.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [Evidence Note: Agent 与 Workflow 边界](../evidence/agent-workflow-boundary.md)
- [Evidence Note: Agent 自治程度边界](../evidence/autonomy-level-boundary.md)
- [Workflow、Hybrid 与 ReAct-like Tool Loop 对比实验结果](../experiments/workflow-agent-comparison/results-2026-07-11.md)
