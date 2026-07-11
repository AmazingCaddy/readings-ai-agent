# Evidence Note: Agent 与 Workflow 边界

## 要验证的结论

Agent 和 Workflow 不是互斥概念。Workflow 更强调开发者预先定义的控制流、状态转移和工具调用顺序；Agent 更强调由模型参与多轮决策、工具调用、状态更新和反馈处理。实际工程中常见做法是 workflow-agent hybrid：保留可控流程，把不确定判断交给模型或 Agent runtime。

## 资料来源

- Source 1：[OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- Source 2：[LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- Source 3：[ReAct: Synergizing Reasoning and Acting in Language Models](../sources/source-cards/2022-react-paper.md)
- Source 4：[Workflow、Hybrid 与 ReAct-like Tool Loop 对比实验结果](../experiments/workflow-agent-comparison/results-2026-07-11.md)
- Source 5：[LangGraph Examples Repository](../sources/source-cards/2026-langgraph-examples-repo.md)
- Source 6：[Building effective agents](../sources/source-cards/2024-anthropic-building-effective-agents.md)

## 交叉验证结果

- 一致点：OpenAI Agents SDK 文档把 SDK 定位为 agentic AI apps / multi-agent workflows 的框架，并将 Agent loop 描述为处理工具调用、把结果回传给 LLM、持续运行直到任务完成的 runtime 行为。
- 一致点：OpenAI 文档明确区分 Responses API 与 Agents SDK：如果开发者想自己控制 loop、tool dispatch 和 state handling，可以直接用 Responses API；如果希望 runtime 管理 turns、tool execution、guardrails、handoffs 或 sessions，则使用 Agents SDK。
- 一致点：LangGraph 文档把 LangGraph 定位为 low-level orchestration framework and runtime，用于 long-running, stateful agents，并明确它支持 any long-running, stateful workflow or agent。
- 一致点：LangGraph 文档说明它不抽象 prompts 或 architecture，这支持“框架提供编排能力，不自动决定架构是否适合任务”的保守表述。
- 一致点：LangGraph current quickstart 用 `StateGraph`、state、model node、tool node、conditional edge、compile 和 invoke 组织一个 tool loop；这补强“workflow / agent 可以用显式状态和条件边表达”的代码层证据。
- 一致点：Anthropic `Building effective agents` 把 workflows 定义为通过 predefined code paths 编排 LLM 和工具的系统，把 agents 定义为由 LLM dynamically direct process and tool usage 的系统。这与本手册把 Agent / Workflow 写成控制权连续谱的边界一致。
- 一致点：Anthropic 文章建议先寻找 simplest solution possible，只有在需要时才增加复杂度，并指出 agentic systems 往往用更高 latency / cost 换取任务表现。这补强“从固定 workflow 或 workflow-agent hybrid 起步，再按真实任务证据提高自治程度”的初学者路线。
- 一致点：ReAct 论文支持推理和行动交替这一 Agent 控制循环模式，但不证明 ReAct 或高自治 Agent 总是优于 workflow。
- 分歧点：OpenAI Agents SDK 提供较高层 agent runtime，LangGraph 更偏低层 orchestration runtime；二者都可以实现 workflow-agent hybrid，但抽象层级不同。
- 边界：Anthropic 文章是工程博客，不是标准规范或 benchmark；它支撑 workflow / agent 定义、简单优先和成本/延迟权衡的工程边界，不支撑任意模型、框架或 agent loop 在真实任务中更可靠。
- 边界：LangGraph `examples/` 目录已由 README 标注为归档、不再更新；它可以作为历史结构参考，但真实跟练应优先使用当前 docs。
- 可能原因：Agent/Workflow 是控制权和编排方式的连续谱，而不是严格二分。固定流程、模型路由、工具调用循环、状态图、多 Agent 协作可以组合。
- 本地实验：标准库 issue triage 模拟中，`fixed_workflow` 以 3 次工具调用完成 2/3 个任务，但无法定位需要 log/config/deploy evidence 的登录超时根因；`workflow_agent_hybrid` 以固定分类加受控证据查询完成 3/3 个任务；`react_like_loop` 也完成 3/3，但工具调用增加到 9 次，并在 feature request 上额外查询了产品文档。这支持“固定 workflow 便宜可控，Agent loop 更灵活但需要预算、停止条件和 trace”的保守表述。

## 实验验证

- 是否需要实验：是
- 实验设计：实现同一个“读取 issue -> 分类 -> 查询相关文件 -> 生成建议”的任务，分别用固定 workflow、workflow 中嵌入模型判断、Agent tool loop 三种方式完成。比较成功率、可调试性、工具调用次数、失败原因和权限控制难度。
- 结果：已完成标准库最小模拟实验。实验覆盖固定 workflow、workflow-agent hybrid 和 ReAct-like tool loop 的成功数、工具调用数、失败 issue、trace decision 和 stop reason。尚未覆盖真实模型、真实 Agent framework、真实代码库、token/latency/cost、权限确认或工具错误恢复。

## 结论状态

- 可入正文：窄结论“Agent 和 Workflow 不是互斥概念，而是控制权、状态推进、工具调用顺序和运行时决策方式的连续谱；实际系统可以组合成 workflow-agent hybrid”已完成第一轮交叉验证。OpenAI Agents SDK 和 LangGraph 官方文档直接支撑 agent loop、runtime-managed workflow、stateful workflow/agent 和 orchestration 边界；Anthropic `Building effective agents` 直接支撑 workflows / agents 定义、简单优先和成本/延迟权衡；LangGraph current quickstart 补强显式 state/node/edge/conditional edge 的代码形态；ReAct 支撑推理-行动循环的研究脉络；标准库实验支撑固定 workflow、hybrid 和 tool loop 的最小比较流程。
- 部分验证：workflow-agent hybrid 是否在真实任务中稳定优于纯 workflow 或更开放 tool loop，仍缺真实模型 / 框架 / repo issue、成本、延迟、权限和工具错误恢复实验。

## 可进入章节

- 是。可以确定写成：Agent 和 Workflow 是控制权与编排方式的连续谱，不是互斥阵营；如果任务步骤固定，workflow 通常更容易测试和控制；如果任务需要根据中间结果持续决策、调用工具和处理反馈，可以逐步引入 Agent 能力。仍需保守写明：具体架构收益必须用真实任务、trace、成本和失败原因验证。
