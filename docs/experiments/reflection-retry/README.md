# Reflection / Retry 与错误反思实验

## 目标

验证第 04 章和第 07 章中的 Reflection / Critic 边界：反思不是自动变聪明。反馈如果能被证据校验，可以帮助重试补齐缺失信息；未验证的反思如果写入后续尝试，可能让系统重复错误。

## 实验边界

这是一个确定性的标准库实验，不调用模型、不接入真实 Agent framework。脚本比较三种策略：

- `no_reflection`：只执行一次，不根据失败反馈重试。
- `verified_reflection_retry`：用 required evidence verifier 找出缺失证据，生成范围明确的 reflection，再重试。
- `unverified_reflection_memory`：把未验证的宽泛经验写入本轮 retry，导致继续跳过关键证据。

本实验不能证明 Reflexion、真实 critic、真实模型或真实框架的效果。它只验证 feedback scope、evidence verifier、retry trace 和错误反思污染的最小流程。

## 输入数据

三类假任务：

- cache rollout 后登录超时，需要 issue、service config、deploy env 和 log。
- billing export 在 schema migration 后失败，需要 issue、service code、schema 和 migration。
- 文档命令拼写错误，只需要 issue 文本。

前两个任务的初始尝试故意缺证据，用来观察 reflection 是否能补齐证据，或是否会把错误经验带入下一次尝试。

## 运行方式

```bash
uv run python docs/experiments/reflection-retry/reflection_retry.py
```

## 观察点

- 没有 reflection 时，缺证据任务是否停留在弱结论。
- verified reflection 是否记录缺失证据并在 retry 中补齐。
- unverified reflection 是否把“跳过 deploy/log/migration”这种错误经验带入 retry。
- Trace 是否记录 `reflection_created`、`reflection_applied`、`retry_failed` 和 missing evidence。

## 结论状态

- 支撑：可以把“Reflection / Critic 需要 evidence verifier、范围控制和 trace；错误反思可能污染后续尝试”写入第 04/07 章。
- 支撑：比较 reflection 架构时应记录成功率、工具调用数、reflection 数量、错误 reflection 应用次数和失败原因。
- 仍缺：真实模型、真实 critic、真实 Agent framework、长期 episodic memory、token/latency/cost、人工评审和多轮任务实验。
