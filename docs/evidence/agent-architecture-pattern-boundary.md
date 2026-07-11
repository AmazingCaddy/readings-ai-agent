# Evidence Note: Agent 架构模式边界

## 要验证的结论

ReAct、Reflection / Reflexion、Tree of Thoughts、状态图和 workflow-agent hybrid 是不同层级的 Agent 架构模式：它们分别解决推理-行动交替、反馈反思、搜索式推理、工程编排和控制权分配问题。它们可以组合，但任何一种模式都不应被写成复杂任务的默认最优解；是否采用需要结合任务类型、失败代价、成本、trace、状态管理和实验结果判断。

## 资料来源

- Source 1：[ReAct: Synergizing Reasoning and Acting in Language Models](../sources/source-cards/2022-react-paper.md)
- Source 2：[Reflexion: Language Agents with Verbal Reinforcement Learning](../sources/source-cards/2023-reflexion-paper.md)
- Source 3：[Tree of Thoughts: Deliberate Problem Solving with Large Language Models](../sources/source-cards/2023-tree-of-thoughts-paper.md)
- Source 4：[LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- Source 5：[OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- Source 6：[Evidence Note: Agent 与 Workflow 边界](agent-workflow-boundary.md)
- Source 7：[Evidence Note: 多 Agent 不是默认更好](multi-agent-default-boundary.md)
- Source 8：[Workflow、Hybrid 与 ReAct-like Tool Loop 对比实验结果](../experiments/workflow-agent-comparison/results-2026-07-11.md)

## 交叉验证结果

- 一致点：ReAct 摘要支持“模型交替生成 reasoning traces 和 task-specific actions”的模式；reasoning traces 用于跟踪、更新计划和处理异常，actions 用于连接知识库或外部环境。
- 一致点：Reflexion 摘要支持“语言反馈 + reflective text + episodic memory buffer”用于后续尝试的模式，但这依赖反馈信号和记忆质量。
- 一致点：Tree of Thoughts 摘要支持“多个中间 thought、搜索不同推理路径、自我评估、前瞻和回溯”的搜索式推理方向。
- 一致点：LangGraph 文档把自己定位为 low-level orchestration framework and runtime，强调 durable execution、human-in-the-loop、persistence 和 trace/debug；这支持“状态图和编排属于工程控制层”的正文表述。
- 一致点：Agent/Workflow evidence 支持 workflow-agent hybrid：固定控制流和模型决策可以组合，不必在纯 workflow 和高自治 Agent 之间二选一。
- 一致点：Multi-agent evidence 支持复杂协作不是默认升级路径；架构复杂度需要用 trace、成本、失败原因和人工介入评估。
- 本地实验：标准库 workflow / hybrid / ReAct-like 对比显示，固定 workflow 在简单任务中工具调用最少，hybrid 可以在受控分支补证据，ReAct-like loop 能动态查询但工具调用更多。这支持“从可控 workflow-agent hybrid 起步”的工程建议，但不证明 ReAct 或复杂架构在真实任务中稳定更优。
- 边界：论文摘要中的效果提升来自特定任务、模型和 baseline；框架文档说明能力和抽象，不等于提供严格对照实验。因此正文只能写成“适用方向和风险边界”，不能写成“复杂架构总能提升可靠性”。

## 实验验证

- 是否需要实验：是
- 实验设计：用同一个“读取 issue -> 定位资料 -> 生成建议 -> 自检”的任务实现四个 baseline：固定 workflow、ReAct tool loop、planner/executor、reflection retry。记录成功率、工具调用次数、token 成本、总耗时、失败类型、trace 可读性、人工介入次数和错误传播情况。
- 结果：已完成第一步标准库 workflow / hybrid / ReAct-like tool loop 对比。尚未覆盖 planner/executor、reflection retry、真实模型、token 成本、真实工具错误或人工介入。

## 结论状态

- 部分验证：三篇论文支撑关键架构模式的研究脉络；LangGraph 和 OpenAI Agents SDK 支撑现代工程编排边界；已有 Agent/Workflow、多 Agent evidence 和标准库 workflow / ReAct-like 对比支撑“从可控 workflow-agent hybrid 起步”的保守路线。仍缺 planner/executor、reflection retry 和真实模型 / 框架对比实验。

## 可进入章节

- 是。可以写成：ReAct、Reflection、Tree of Thoughts、状态图和 workflow-agent hybrid 解决的问题不同；初学者应先理解任务边界、状态、工具权限、trace 和停止条件，再决定是否引入更复杂的规划、反思或搜索机制。
