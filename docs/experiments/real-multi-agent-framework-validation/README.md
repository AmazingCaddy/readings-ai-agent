# Real Multi-Agent Framework Validation

## 目标

用同一个本地确定性研究/复核任务验证 AutoGen AgentChat、CrewAI 和 LangGraph 的真实 Python runtime surface：角色化 agent、team/crew/state graph 编排、终止/任务输出/条件路由、缺证据复核和脱敏 trace。

这个实验补强第 07 章和第 10 章的多 Agent 边界：多 Agent 是编排选择，不是复杂任务的默认升级路径。它不是框架排行榜。

## 实验边界

本实验使用 deterministic fake model / fake LLM，不调用真实模型，不记录 token/cost/latency，不验证真实多 Agent 协作质量、冲突合并质量、生产 tracing、部署恢复、权限 UI 或人工评审负担。

实验只支撑窄观察：框架能否表达一个 researcher/reviewer 任务，能否产生可检查的消息或任务输出，应用层能否在 trace 发布前脱敏测试 secret。

## 运行方式

```bash
uv run --with autogen-agentchat --with crewai --with langgraph python docs/experiments/real-multi-agent-framework-validation/real_multi_agent_framework_validation.py
```

如果缺少某个依赖，对应 adapter 会返回 `skipped`，其他 adapter 仍可运行。统一 runner 的标准临时依赖包含 LangGraph、不包含 AutoGen/CrewAI，因此 full runner 通常完成 LangGraph adapter，并保守跳过 AutoGen/CrewAI adapter。

## 观察点

- AutoGen AgentChat 是否能用 `AssistantAgent`、`RoundRobinGroupChat` 和 `TextMentionTermination` 表达 researcher/reviewer team loop。
- CrewAI 是否能用 `Agent`、`Task`、`Crew(process=sequential)` 表达 researcher/reviewer task sequence。
- LangGraph 是否能用 `StateGraph`、节点函数和 conditional edges 表达 researcher/reviewer state graph。
- 缺少 `feedback.md` 时，reviewer 是否在框架 transcript / task output 中暴露缺证据。
- 发布 trace 是否不泄露示例 secret marker。
- 哪些能力来自框架 runtime，哪些仍由应用层代码负责。

## 结论状态

- 当前状态：已完成 AutoGen AgentChat 0.7.5、CrewAI 1.15.2 和 LangGraph 1.2.9 的本地 fake-model / deterministic-node runtime run，见 [2026-07-12 结果](results-2026-07-12.md)。
- 可支撑：多 Agent / 多角色框架可以提供 agent/team/task/crew/state graph 编排表面和可检查 transcript / task output / state trace；但证据覆盖、缺证据 rubric、审批策略、trace 脱敏和是否值得引入多 Agent 仍需要应用层设计和评估。
- 不能支撑：不能证明 AutoGen、CrewAI 或 LangGraph 在真实模型任务中更好、更安全、更便宜、更快，也不能证明真实冲突解决、token/latency/cost、生产 observability、部署恢复或人工评审负担。
