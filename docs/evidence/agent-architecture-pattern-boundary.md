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
- Source 9：[Planner / Executor 与单循环对比实验结果](../experiments/planner-executor-comparison/results-2026-07-11.md)
- Source 10：[Reflection / Retry 与错误反思实验结果](../experiments/reflection-retry/results-2026-07-11.md)
- Source 11：[LangGraph Examples Repository](../sources/source-cards/2026-langgraph-examples-repo.md)
- Source 12：[Voyager: An Open-Ended Embodied Agent with Large Language Models](../sources/source-cards/2023-voyager-paper.md)

## 交叉验证结果

- 一致点：ReAct 摘要支持“模型交替生成 reasoning traces 和 task-specific actions”的模式；reasoning traces 用于跟踪、更新计划和处理异常，actions 用于连接知识库或外部环境。
- 一致点：Reflexion 摘要支持“语言反馈 + reflective text + episodic memory buffer”用于后续尝试的模式，但这依赖反馈信号和记忆质量。
- 一致点：Tree of Thoughts 摘要支持“多个中间 thought、搜索不同推理路径、自我评估、前瞻和回溯”的搜索式推理方向。
- 一致点：LangGraph 文档把自己定位为 low-level orchestration framework and runtime，强调 durable execution、human-in-the-loop、persistence 和 trace/debug；这支持“状态图和编排属于工程控制层”的正文表述。
- 一致点：LangGraph current quickstart 展示 `StateGraph`、state、node、conditional edge、tool node、compile 和 invoke；历史 plan-and-execute notebook 展示 planner / agent / replan 节点和 `PlanExecute` state；历史 human-in-the-loop notebook 展示 `interrupt()`、checkpointer 和 `Command(resume=...)`。这些示例补强状态图、planner/executor 和 HITL 的代码形态。
- 一致点：Voyager 摘要支持开放式具身 Agent 的另一种结构：automatic curriculum、executable skill library 和 iterative prompting。它把 environment feedback、execution errors 和 self-verification 放进程序改进循环，说明具身 / 环境交互型 Agent 需要动作接口、环境反馈、长期状态和技能复用，而不只是单轮工具调用。
- 一致点：Agent/Workflow evidence 支持 workflow-agent hybrid：固定控制流和模型决策可以组合，不必在纯 workflow 和高自治 Agent 之间二选一。
- 一致点：Multi-agent evidence 支持复杂协作不是默认升级路径；架构复杂度需要用 trace、成本、失败原因和人工介入评估。
- 边界：LangGraph `examples/` 目录已归档，不代表当前推荐 API；示例只能作为架构形态 reference，不能证明真实效果或复杂架构默认更可靠。
- 边界：Voyager 的性能结论来自 Minecraft、特定环境接口、特定依赖和当时 GPT-4 设置；它能支撑 embodied lifelong learning 的研究机制边界，不能证明技能库、开放式探索或无人工干预在业务 Agent 中默认可靠或默认更优。
- 本地实验：标准库 workflow / hybrid / ReAct-like 对比显示，固定 workflow 在简单任务中工具调用最少，hybrid 可以在受控分支补证据，ReAct-like loop 能动态查询但工具调用更多。这支持“从可控 workflow-agent hybrid 起步”的工程建议，但不证明 ReAct 或复杂架构在真实任务中稳定更优。
- 本地实验：标准库 planner/executor 对比显示，一次性 planner/executor 在 billing migration 任务中漏掉 migration evidence，成功率为 2/3；带 validation feedback 的 planner/executor 通过 `validation_failed` 和 `plan_revised` 补齐证据，恢复到 3/3。这支持“计划必须可校验、失败必须反馈、必要时重规划”的工程建议。
- 本地实验：标准库 reflection/retry 对比显示，`verified_reflection_retry` 通过 required evidence verifier 把成功率从 1/3 提升到 3/3，但工具调用从 6 增加到 14；`unverified_reflection_memory` 两次应用错误反思后仍为 1/3。这支持“反思需要证据校验和范围控制，错误反思可能污染后续尝试”的保守表述。
- 边界：论文摘要中的效果提升来自特定任务、模型和 baseline；框架文档说明能力和抽象，不等于提供严格对照实验。因此正文只能写成“适用方向和风险边界”，不能写成“复杂架构总能提升可靠性”。

## 实验验证

- 是否需要实验：是
- 实验设计：用同一个“读取 issue -> 定位资料 -> 生成建议 -> 自检”的任务实现四个 baseline：固定 workflow、ReAct tool loop、planner/executor、reflection retry。记录成功率、工具调用次数、token 成本、总耗时、失败类型、trace 可读性、人工介入次数和错误传播情况。
- 结果：已完成标准库 workflow / hybrid / ReAct-like tool loop 对比、planner/executor vs single checklist / feedback replanning 对比，以及 reflection/retry 错误反思模拟。尚未覆盖真实模型、token 成本、真实工具错误或人工介入。

## 结论状态

- 可入正文：窄结论“ReAct 的核心思想是交替生成 reasoning traces 和 task-specific actions，用推理轨迹跟踪/更新计划、处理异常，用行动连接知识库或外部环境”已完成第一轮交叉验证。ReAct 摘要直接支撑 reasoning / acting interleaving；标准库 workflow / hybrid / ReAct-like 对比实验支撑把 ReAct-like tool loop 作为控制流形态解释，但不支撑 ReAct 默认优于 workflow。
- 可入正文：窄结论“Tree of Thoughts 支持搜索式推理路径，但不等同于生产 Agent 编排框架”已完成第一轮交叉验证。ToT 摘要直接支撑多个中间 thought、不同推理路径、自我评估、前瞻和回溯；LangGraph / workflow evidence 支撑把工程编排、状态持久化和 HITL 与研究式搜索推理区分开。
- 可入正文：窄结论“复杂 Agent 架构不是默认更可靠；是否引入 ReAct、Planner / Executor、Reflection、Tree of Thoughts、状态图、embodied lifelong learning 或多 Agent，需要看任务边界、trace、成本、失败原因、权限和实验结果”已完成第一轮交叉验证。论文支撑不同研究模式，Voyager 补强 automatic curriculum / skill library / environment feedback 的开放式具身 Agent 机制，LangGraph 和 OpenAI Agents SDK 支撑现代工程编排、状态和 trace 边界，LangGraph current docs / historical examples 补强 state graph、planner/replan 和 HITL 的代码形态；多组标准库实验显示复杂控制结构会带来额外工具调用、错误传播、错误反思、重复读取或冲突风险。
- 可入正文：窄结论“Planner / Executor 不能只停留在一次性计划；计划需要可执行，执行结果需要证据校验，失败需要反馈给 planner 并记录重规划 trace”已完成第一轮交叉验证。标准库 planner/executor 对比复现了一次性计划漏掉 migration evidence，而带 validation feedback 的流程通过 `validation_failed` 和 `plan_revised` 补齐证据。
- 可入正文：窄结论“Reflection / Reflexion 可以把任务反馈和文字反思用于后续尝试，但反思必须绑定可校验反馈、范围控制和 trace；未验证反思不应直接写入长期记忆或后续策略”已完成第一轮交叉验证。Reflexion 摘要支撑 linguistic feedback、reflective text 和 episodic memory buffer 的研究机制；标准库 reflection/retry 实验显示 verified feedback 可以补齐 missing evidence，而 unverified reflection memory 会让错误重复。
- 部分验证：ReAct、Reflection / Reflexion、Tree of Thoughts、Voyager-style embodied lifelong learning、状态图和 workflow-agent hybrid 的真实任务收益、成本、延迟、工具错误恢复和人工介入仍缺真实模型 / 框架 / 环境对比实验；不能写成某个复杂架构在真实任务中稳定更优，不能写成 ReAct / ToT / skill library 是复杂任务默认选择，也不能写成 reflection 或技能复用总能提升质量。

## 可进入章节

- 是。可以确定写成：ReAct 是推理轨迹和行动步骤交替的研究/架构模式；Tree of Thoughts 是搜索多个推理路径的研究/规划模式，不等同于生产编排框架；Voyager 是开放式具身 Agent 的研究案例，展示 automatic curriculum、可执行技能库、环境反馈、执行错误和自我验证如何组成长期学习循环。复杂 Agent 架构不是默认升级路径；初学者应先理解任务边界、状态、工具权限、trace、成本和停止条件，再决定是否引入更复杂的规划、反思、搜索、技能库、开放式探索或多 Agent 机制。Planner / Executor 可以确定写成：要有可执行计划、证据校验、失败反馈和重规划 trace；计划本身不是质量保证。Reflection 可以确定写成：反馈和反思只有在可校验、可追踪、范围明确时才适合进入 retry 或记忆；未验证反思可能污染后续尝试。
