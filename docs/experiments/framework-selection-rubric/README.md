# 框架选择 Rubric Smoke Test

## 目标

验证第 10 章的框架比较方法是否能被拆成可解释的任务画像、能力标签、评分和 cautions。这个实验用于支撑“先看任务难点，再选框架”的学习边界。

## 实验边界

这是一个确定性的 Python 标准库实验，不安装或运行真实框架，不调用模型，不联网。它不能证明 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI 或 Semantic Kernel 的真实成本、延迟、trace、权限或稳定性。

它只验证：如果把任务需求明确写成 `required`、`nice_to_have` 和 `avoid`，框架比较就能比“哪个框架最好”更可追溯。

## 输入数据

实验包含 5 个任务画像：

- 最小 tool agent。
- RAG knowledge-base Q&A。
- 带人工审批的 workflow。
- 多角色 researcher/writer/reviewer 练习。
- 企业插件和 MCP/OpenAPI 集成实验。

实验包含 6 个框架画像：

- OpenAI Agents SDK。
- LangGraph。
- LlamaIndex。
- AutoGen。
- CrewAI。
- Semantic Kernel。

## 运行方式

```bash
uv run python docs/experiments/framework-selection-rubric/framework_selection_rubric.py
```

## 观察点

- top choice 是否能显示 matched capabilities 和 missing required capabilities。
- multi-agent 任务是否暴露协调成本 caution。
- enterprise 任务是否暴露概念复杂度和 experimental caution。
- 所有结果是否都保留 `needs_real_experiment=true`，避免把 rubric 写成真实 benchmark。

## 结论状态

- 支撑：第 10 章可以继续强调按任务难点比较框架，而不是做排行榜。
- 支撑：框架选择需要记录 required capability、nice-to-have、avoid、missing required 和 cautions。
- 仍缺：真实同一任务横向实验，包括依赖、实现时间、trace 可读性、权限/人工确认、错误恢复、token/latency/cost 和维护复杂度。
