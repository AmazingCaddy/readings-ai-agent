# Real OpenAI Agents SDK Guardrail Validation

## 目标

用 OpenAI Agents SDK 的真实 Python runtime surface 验证 input / output / tool input / tool output guardrail 在一个本地退款工具任务中的执行位置和可观察结果。

这个实验服务第 09 和第 10 章，用来把 Agents SDK 文档中的 guardrails / HITL / sensitive trace 边界落到可复现检查项，而不是把文档能力直接写成生产安全结论。

## 实验边界

本实验使用 deterministic fake model，不调用真实 OpenAI API，不验证真实模型 prompt-injection 抵抗、真实 guardrail 检测质量、hosted tools、MCP tools、Shell / ApplyPatch tools、生产 tracing、成本、延迟或真实 HITL UI。

实验只支撑窄观察：Agents SDK 0.18.2 中 blocking input guardrail、output guardrail、function-tool input guardrail、function-tool output guardrail 和 `needs_approval` metadata 的本地 runtime surface。

## 运行方式

```bash
uv run --with openai-agents==0.18.2 python docs/experiments/real-openai-agents-guardrail-validation/real_openai_agents_guardrail_validation.py
```

如果项目环境未安装 `agents` package，脚本会返回 `skipped`，不会把 SDK 行为写成已验证结论。

## 观察点

- Input guardrail tripwire 是否在模型调用前阻断。
- Output guardrail tripwire 是否在模型调用后阻断最终输出。
- Function tool input guardrail 的 `reject_content` 是否能在 Runner 路径上阻止本地函数工具副作用。
- Function tool output guardrail 的 `reject_content` 是否发生在本地函数工具副作用之后，只替换工具输出。
- `needs_approval=True` 是否暴露为 function-tool metadata。
- 发布 trace 是否不泄露示例 secret marker。

## 结论状态

- 当前状态：已完成 OpenAI Agents SDK 0.18.2 本地 fake-model run，见 [2026-07-12 结果](results-2026-07-12.md)。
- 可支撑：input guardrail、output guardrail、function-tool input/output guardrail 和 `needs_approval` metadata 是可观察的 SDK runtime surface；tool input guardrail 更适合阻断副作用前置条件，tool output guardrail 更适合过滤工具输出但不能撤销已经发生的副作用。
- 不能支撑：不能证明真实模型安全、真实 detector / guardrail 质量、hosted/MCP/Shell/ApplyPatch 工具覆盖、生产 trace 字段、真实 HITL UI、成本、延迟或框架默认安全。
