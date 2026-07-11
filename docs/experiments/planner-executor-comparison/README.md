# Planner / Executor 与单循环对比实验

## 目标

验证第 04 章和第 07 章中的规划边界：Planner / Executor 可以让职责更清楚，但计划不是自动可靠。计划必须足够具体，executor 的失败或缺证据必须能反馈给 planner，否则错误计划会传播到最终输出。

## 实验边界

这是一个确定性的标准库实验，不调用模型、不接入真实 Agent framework。脚本比较三种策略：

- `single_checklist_loop`：单个循环按任务类型读取固定 checklist 中的证据。
- `planner_executor_once`：planner 一次性生成执行步骤，executor 只执行初始计划，不重规划。
- `planner_executor_with_feedback`：executor 执行初始计划后校验 required evidence；缺证据时反馈给 planner 并补充步骤。

本实验不能证明 Planner / Executor 在真实模型、真实代码库或真实框架中稳定提升质量。它只验证计划遗漏、证据校验、反馈重规划和 trace 字段设计。

## 输入数据

三类假任务：

- 文档安装命令拼写问题。
- 登录超时和 cache port mismatch。
- billing export 在 schema migration 后失败，需要同时读取 issue、service code、schema 和 migration。

其中第三个任务故意让 `planner_executor_once` 漏掉 `migrations/2026_07_add_customer_id.sql`，用于观察计划遗漏如何污染最终结论。

## 运行方式

```bash
uv run python docs/experiments/planner-executor-comparison/planner_executor_comparison.py
```

## 观察点

- 单循环 checklist 是否足够完成清晰任务。
- 一次性 plan 是否会遗漏关键证据。
- executor 校验是否能发现 missing evidence。
- 重规划是否能补上缺失步骤。
- Trace 是否记录 `plan_created`、`validation_failed`、`plan_revised` 和 tool call/result。

## 结论状态

- 支撑：可以把“Planner / Executor 需要明确接口、证据校验和反馈重规划”写入第 04/07 章。
- 支撑：计划步骤本身不是质量保证；比较架构时要看计划遗漏、重规划次数、工具调用数和失败原因。
- 仍缺：真实模型、真实 framework、真实 repo、token/latency/cost、工具错误、权限确认、人工评审和 reflection retry 对比。
