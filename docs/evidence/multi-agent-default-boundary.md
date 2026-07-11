# Evidence Note: 多 Agent 不是默认更好

## 要验证的结论

多 Agent 是一种任务编排方式，不是 Agent 系统的默认升级路径。它适合角色边界清楚、任务可拆分、需要协作或审查且能记录成本和 trace 的场景；如果任务能被单 Agent、固定 workflow 或 workflow-agent hybrid 稳定完成，多 Agent 可能只会增加通信成本、协调复杂度和调试难度。

## 资料来源

- Source 1：[Microsoft AutoGen Documentation](../sources/source-cards/2026-autogen-docs.md)
- Source 2：[CrewAI Documentation](../sources/source-cards/2026-crewai-docs.md)
- Source 3：[AgentBench: Evaluating LLMs as Agents](../sources/source-cards/2023-agentbench-paper.md)
- Source 4：[Evidence Note: Agent Eval 与 Trajectory 边界](agent-eval-trajectory-boundary.md)
- Source 5：[多 Agent 与 Flow 控制对比实验结果](../experiments/multi-agent-comparison/results-2026-07-11.md)
- Source 6：[Multiagent Debate paper](../sources/source-cards/2023-multiagent-debate-paper.md)

## 交叉验证结果

- 一致点：AutoGen 文档明确提供 AgentChat、Teams、Selector Group Chat、Swarm、GraphFlow、logging 等多 Agent 抽象，说明多 Agent 是成熟工程生态的一部分。
- 一致点：Multiagent Debate paper 摘要展示了多个模型实例提出、辩论各自答案和推理过程、多轮后形成共同答案的研究机制；这支持“多视角和互相审查可能有价值”的窄边界。
- 一致点：Multiagent Debate paper 同时是研究任务和提示流程，不是生产框架指南；它不能证明工程多 Agent 对所有复杂任务默认更可靠。
- 一致点：AutoGen Core 被描述为 event-driven framework for scalable multi-agent AI systems，适用场景包括 deterministic/dynamic workflows、multi-agent collaboration 和 distributed agents。
- 一致点：CrewAI 文档把 Flows 和 Crews 分开，并明确 production-ready application 应 start with a Flow；Crew 只在需要特定复杂自治任务时作为 Flow 中的团队能力使用。
- 一致点：AgentBench 和 Eval evidence note 支持对 Agent 系统进行交互环境、失败原因、trajectory/trace 和成本评估；这说明多 Agent 是否值得需要被评测，而不是只看架构图。
- 分歧点：AutoGen 更强调多 Agent 应用和设计模式，CrewAI 明确强调 Flow 控制和 Crew 协作的组合。二者都说明多 Agent 可实现，但都不能证明多 Agent 对所有复杂任务默认更优。
- 可能原因：框架文档通常展示能力和抽象，而不是针对单 Agent、workflow、多 Agent 做严格对照实验。是否采用多 Agent 取决于任务分解、协调成本、可观测性和失败代价。
- 本地实验：标准库多 Agent 对比中，`single_checklist` 以 6 次工具调用完成 3/3 个任务；`ungoverned_multi_agent` 只完成 1/3，出现 7 条 messages、1 个 unresolved conflict、3 次 duplicate reads，并漏掉 `cost.md` / `feedback.md`；`flow_controlled_multi_agent` 通过 `plan_created` 和 `review_completed` 恢复到 3/3，但有 9 条 messages。该结果支持“多 Agent 需要 Flow / workflow 控制，否则角色化本身会增加协调和缺证据风险”的保守表述。

## 实验验证

- 是否需要实验：是
- 实验设计：用同一个研究+写作小任务分别实现单 Agent、planner/executor、multi-agent researcher/writer/reviewer。记录成功率、人工修正次数、工具调用次数、token 成本、总耗时、冲突处理次数和 trace 可读性。
- 结果：已完成标准库单流程 / 无控制多 Agent / Flow 控制多 Agent 对比。实验覆盖 success、tool calls、messages、conflicts、duplicate reads 和 missing evidence。尚未覆盖真实模型、真实 AutoGen/CrewAI/LangGraph、token/latency/cost、工具错误或人工评审。

## 结论状态

- 可入正文：窄结论“多 Agent 是一种编排选择，不是复杂任务的默认升级路径；只有在角色边界、证据分配、冲突处理、review trace、成本和延迟可控时才值得引入”已完成第一轮交叉验证。Multiagent Debate paper 支撑多实例辩论和互相审查的研究机制；AutoGen 和 CrewAI 文档直接支撑多 Agent/Teams/Crews/GraphFlow/coordination patterns 的工程存在；CrewAI 还直接支撑“先用 Flow 控制，再在需要时调用 Crew”的保守路线；标准库实验支撑无控制多 Agent 的重复读取、缺证据和冲突风险。
- 部分验证：多 Agent 在真实模型 / AutoGen / CrewAI / LangGraph / 真实复杂任务中的收益、成本、延迟、冲突合并质量和人工评审负担仍需同任务对比实验。

## 可进入章节

- 是。可以确定写成：多 Agent 是有用的编排工具，但不应作为默认起点。只有当任务确实需要多个角色，且已有明确协作边界、证据分配、冲突处理规则、成本预算和可观测 trace 时，才值得引入。仍需保守写明：真实框架表现必须用同一任务对比验证。
