# Agent 架构模式

## 本章适合谁

如果你已经理解 Agent 是系统形态，也知道工具调用如何工作，但还不清楚 ReAct、Plan-and-Execute、Reflection、状态机和 Workflow-agent hybrid 分别解决什么问题，这一章适合阅读。

本章不要求你先掌握具体框架。我们先讨论架构模式，再把框架看成这些模式的实现方式。

## 你会学到什么

- Agent 控制循环是什么。
- ReAct、Plan-and-Execute、Reflection、状态机各自适合什么场景。
- Workflow 和 Agent 如何组合。
- 为什么复杂架构不一定更可靠。
- 设计 Agent 架构时应该优先考虑哪些工程边界。

## 先用一句话理解

Agent 架构的核心问题是：系统如何决定下一步做什么、如何调用工具、如何处理反馈、什么时候停止，以及哪里需要人来确认。

## 基础概念

### 控制循环

控制循环是 Agent 和普通一次性模型调用的重要区别。一个简单控制循环通常包括：

1. 接收目标和当前状态。
2. 让模型判断下一步。
3. 调用工具或生成输出。
4. 接收观察结果。
5. 更新状态。
6. 决定继续、重试、请求确认或停止。

这个循环可以很短，也可以很复杂。复杂度越高，越需要 trace、状态管理、错误处理和权限边界。

### ReAct

ReAct 的核心思想是让模型在推理步骤和行动步骤之间交替。论文摘要中描述，这种方式让 reasoning traces 帮助模型跟踪和更新行动计划，而 actions 让模型连接知识库或环境获取信息。

对初学者来说，可以把 ReAct 理解为：模型不是一次性给最终答案，而是边想边做，做完再看结果，再决定下一步。

需要保守理解：ReAct 是重要模式，但它不证明所有任务都应该使用 ReAct，也不证明 ReAct 总是比固定 workflow 更好。

### Plan-and-Execute

Plan-and-Execute 把“制定计划”和“执行步骤”分开。一个 planner 先生成任务步骤，executor 再逐步执行。

这种模式适合任务较长、需要拆解、步骤之间有依赖的场景。但它也有风险：如果计划一开始就错了，后续执行可能沿着错误方向推进。因此它需要中途检查、重规划和人工确认。

本手册的 Planner / Executor 标准库实验复现了这个风险：一次性 planner 在 billing migration 任务里漏掉 migration 文件，executor 按计划执行后只能得到弱结论；加入 evidence validation 和 `plan_revised` 后才补齐证据。这个结果支持一个保守规则：计划不是质量保证，计划必须能被执行结果校验。

### Reflection

Reflection 是让 Agent 根据反馈总结错误、记录经验，并用于后续尝试。Reflexion 论文讨论了不更新模型权重、而通过语言反馈和 episodic memory 改进后续决策的思路。

需要保守理解：Reflection 不等于自动变聪明。它可能带来额外成本，也可能把错误总结写进记忆，导致后续任务被污染。

本手册的 Reflection / Retry 标准库实验比较了无反思、带 verifier 的反思重试和未验证反思记忆。带 verifier 的反思能根据 missing evidence 补读 deploy、log 或 migration，把结果从 1/3 提升到 3/3；未验证反思把“跳过 deploy/log/migration 以降低成本”写入 retry 后，仍然 1/3。这支持一个边界：反思要绑定可检查反馈，不能把自我总结直接当事实或策略。

### 状态机

状态机把系统流程拆成明确状态和状态转移。例如：`准备输入 -> 调用工具 -> 校验结果 -> 生成回答 -> 完成`。

状态机更像工程控制结构。它的优点是可预测、可测试、可调试；缺点是灵活性较低。很多生产系统会把状态机和模型判断结合起来，让模型只处理不确定节点，而不是控制整个流程。

### Workflow-agent hybrid

Workflow-agent hybrid 是把固定 workflow 和 Agent 能力结合。开发者保留主要控制流，把需要语言理解、工具选择或不确定判断的部分交给模型。

这是初学者最值得优先学习的方向，因为它比完全自治 Agent 更容易控制，也比纯规则 workflow 更灵活。

OpenAI Agents SDK 和 LangGraph 的文档都支持这种组合视角：前者提供 managed agent loop、tool execution、guardrails、handoffs 和 sessions；后者提供 long-running, stateful workflow or agent 的低层 orchestration runtime。

## 通俗例子

假设你要让系统整理一个 GitHub issue，并判断是否需要创建修复任务。

固定 workflow 可以这样做：读取 issue、提取标题、分类、生成摘要。

ReAct 风格 Agent 可能会先读 issue，再查相关代码，再读报错日志，再决定是否需要更多信息。

Plan-and-Execute 可能先计划：读取 issue、定位模块、查最近变更、判断影响范围、输出建议。

Reflection 可能在第一次判断错误后记录：“以后遇到类似堆栈要先查配置文件”。

状态机则会明确规定：只有当 issue 包含复现步骤和错误日志时，才进入影响范围分析；否则请求补充信息。

真实工程里，你可能会组合这些方法：用状态机控制流程，用模型做分类和总结，用工具查代码，用人工确认是否创建任务。

## 工作原理

一个可控 Agent 架构通常包含这些层次。

### 任务层

定义目标、成功标准和停止条件。没有停止条件，Agent 可能反复调用工具或在不确定状态下继续推进。

### 决策层

决定下一步是回答、调用工具、请求用户、重试还是停止。ReAct、planner、router、critic 都属于这一层的不同形式。

### 工具层

执行外部动作，例如搜索、读文件、查数据库、调用 API。工具层必须有 schema、权限、错误处理和日志。

### 状态层

保存任务进展、历史观察、工具结果和中间判断。没有状态层，复杂任务很难恢复和调试。

### 评测层

记录 trace，分析成功率、失败类型、成本和延迟。没有评测层，架构选择只能靠主观感觉。

## 工程实践

### 从固定 workflow 开始

如果任务流程清楚，先写 workflow。等你发现某些步骤确实需要动态判断，再引入模型决策。

### 限制自治范围

不要让模型控制所有步骤。可以只让它做分类、路由、参数生成或候选计划，真正执行前由程序校验。

自治程度应被当作控制权和风险面的连续谱：从固定 workflow，到 workflow-agent hybrid，再到更开放的 tool loop。越往后，越需要明确权限、预算、停止条件、trace 和人工确认点。

### 明确停止条件

Agent 必须知道什么时候完成、什么时候失败、什么时候请求用户。否则它可能不断尝试，浪费成本并扩大风险。

### 保留人工确认点

涉及写操作、外部发送、付费、删除、权限变更的工具，应该设置人工确认或更严格的策略。

### 用 trace 比较架构

不要只看最终答案。比较架构时，应同时记录成功率、工具调用次数、总耗时、失败原因和人工介入次数。

## 常见误区

- 误区一：ReAct 是 Agent 的唯一架构。它只是重要模式之一。
- 误区二：Plan-and-Execute 总是更适合复杂任务。计划错误会导致错误传播。
- 误区三：Reflection 总能提升质量。错误反思可能污染后续状态。
- 误区四：多 Agent 等于更强。多 Agent 会增加协调成本和调试复杂度。
- 误区五：状态机太死板。很多生产 Agent 正需要状态机提供可控边界。

## 什么时候不该用复杂 Agent 架构

以下场景优先用简单 workflow 或单次模型调用：

- 任务步骤固定。
- 输入输出格式稳定。
- 不需要工具调用。
- 错误代价高但没有人工确认机制。
- 没有 trace 和 eval。

复杂 Agent 架构适合任务不确定、需要多步工具调用、需要状态恢复、需要跨资料推理的场景。

## 已验证结论

- ReAct 论文支持“推理和行动交替”这一模式，但不支持“ReAct 总是优于 workflow”的泛化说法。
- Reflexion 论文支持“语言反馈和 episodic memory 可用于后续尝试”的研究方向；标准库 Reflection / Retry 实验显示，带证据校验的反思重试可以补齐缺失证据，但未验证反思会让错误重复。因此其效果边界需要结合现代模型、真实任务、成本和记忆污染风险复核。
- Tree of Thoughts 支持搜索式推理路径这个研究方向，但不应直接等同于生产 Agent 编排。
- OpenAI Agents SDK 文档可作为 managed agent loop、工具执行、guardrails、handoffs、sessions 和 tracing 的工程参考。
- LangGraph 文档可作为状态图、durable execution、human-in-the-loop、persistence 和工程编排的参考，但它是具体框架，不是唯一通用架构定义。
- Agent 与 Workflow 边界已完成第一轮验证：它们不是互斥概念，实际系统常把固定流程和 Agent 能力组合成 workflow-agent hybrid。
- Agent 自治程度边界已完成第一轮验证：自治程度可以作为分类维度，但不代表能力等级；高自治需要更强的权限、停止条件、trace、eval 和成本控制。
- Agent 架构模式边界已完成第一轮验证：ReAct、Reflexion 和 Tree of Thoughts 支持不同研究模式，LangGraph / OpenAI Agents SDK 支持现代工程编排边界；标准库 workflow / hybrid / ReAct-like、Planner / Executor 和 Reflection / Retry 对比实验支持“先从可控 workflow 或 hybrid 起步，为 planning/reflection 加入校验反馈”的工程路线，但真实模型和框架实验仍待验证。

## 待验证问题

- 哪些任务中 ReAct 明确优于固定 workflow？
- Plan-and-Execute 在真实业务任务中如何控制错误传播？
- Reflection 的收益是否超过额外成本和错误记忆风险？
- 状态机和 Agent 控制循环如何组合最适合初学者项目？
- workflow-agent hybrid 相比纯 workflow 或高自治 Agent 的收益如何用最小实验验证？
- 多 Agent 在什么任务中收益稳定超过协调成本？

## 本章小结

- Agent 架构的核心是控制下一步、处理反馈和决定何时停止。
- ReAct、Plan-and-Execute、Reflection、状态机解决的问题不同。
- 复杂架构不一定更可靠，控制边界和评测更重要。
- 初学者应优先学习 workflow-agent hybrid。
- 任何架构选择都应该通过 trace 和 eval 验证。

## References

### Papers

- [ReAct: Synergizing Reasoning and Acting in Language Models](../sources/source-cards/2022-react-paper.md)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](../sources/source-cards/2023-reflexion-paper.md)
- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](../sources/source-cards/2023-tree-of-thoughts-paper.md)

### Framework Docs

- [LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- [OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- [Microsoft AutoGen Documentation](../sources/source-cards/2026-autogen-docs.md)

### Governance

- [术语边界表](../glossary.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [Evidence Note: Agent 与 Workflow 边界](../evidence/agent-workflow-boundary.md)
- [Evidence Note: Agent 自治程度边界](../evidence/autonomy-level-boundary.md)
- [Evidence Note: Agent 架构模式边界](../evidence/agent-architecture-pattern-boundary.md)
- [Workflow、Hybrid 与 ReAct-like Tool Loop 对比实验结果](../experiments/workflow-agent-comparison/results-2026-07-11.md)
- [Planner / Executor 与单循环对比实验结果](../experiments/planner-executor-comparison/results-2026-07-11.md)
- [Reflection / Retry 与错误反思实验结果](../experiments/reflection-retry/results-2026-07-11.md)
