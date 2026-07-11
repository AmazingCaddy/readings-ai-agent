# Evidence Note: Agent 与 Workflow 边界

## 要验证的结论

Agent 和 Workflow 不是互斥概念。Workflow 更强调开发者预先定义的控制流、状态转移和工具调用顺序；Agent 更强调由模型参与多轮决策、工具调用、状态更新和反馈处理。实际工程中常见做法是 workflow-agent hybrid：保留可控流程，把不确定判断交给模型或 Agent runtime。

## 资料来源

- Source 1：[OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- Source 2：[LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- Source 3：[ReAct: Synergizing Reasoning and Acting in Language Models](../sources/source-cards/2022-react-paper.md)

## 交叉验证结果

- 一致点：OpenAI Agents SDK 文档把 SDK 定位为 agentic AI apps / multi-agent workflows 的框架，并将 Agent loop 描述为处理工具调用、把结果回传给 LLM、持续运行直到任务完成的 runtime 行为。
- 一致点：OpenAI 文档明确区分 Responses API 与 Agents SDK：如果开发者想自己控制 loop、tool dispatch 和 state handling，可以直接用 Responses API；如果希望 runtime 管理 turns、tool execution、guardrails、handoffs 或 sessions，则使用 Agents SDK。
- 一致点：LangGraph 文档把 LangGraph 定位为 low-level orchestration framework and runtime，用于 long-running, stateful agents，并明确它支持 any long-running, stateful workflow or agent。
- 一致点：LangGraph 文档说明它不抽象 prompts 或 architecture，这支持“框架提供编排能力，不自动决定架构是否适合任务”的保守表述。
- 一致点：ReAct 论文支持推理和行动交替这一 Agent 控制循环模式，但不证明 ReAct 或高自治 Agent 总是优于 workflow。
- 分歧点：OpenAI Agents SDK 提供较高层 agent runtime，LangGraph 更偏低层 orchestration runtime；二者都可以实现 workflow-agent hybrid，但抽象层级不同。
- 可能原因：Agent/Workflow 是控制权和编排方式的连续谱，而不是严格二分。固定流程、模型路由、工具调用循环、状态图、多 Agent 协作可以组合。

## 实验验证

- 是否需要实验：是
- 实验设计：实现同一个“读取 issue -> 分类 -> 查询相关文件 -> 生成建议”的任务，分别用固定 workflow、workflow 中嵌入模型判断、Agent tool loop 三种方式完成。比较成功率、可调试性、工具调用次数、失败原因和权限控制难度。
- 结果：待执行

## 结论状态

- 部分验证：OpenAI Agents SDK 和 LangGraph 官方文档直接支撑 agent loop、runtime-managed workflow、stateful workflow/agent 和 orchestration 边界；ReAct 支撑推理-行动循环的研究脉络。仍缺本地对比实验和更多框架横向资料。

## 可进入章节

- 是。可以写成：如果任务步骤固定，workflow 通常更稳；如果任务需要根据中间结果持续决策、调用工具和处理反馈，可以逐步引入 Agent 能力。初学者应优先理解 workflow-agent hybrid，而不是直接追求完全自治。
