# Real LangGraph Interrupt Recovery 实验

## 目标

验证 LangGraph current docs 中的 `interrupt()`、checkpointer、`thread_id` 和 `Command(resume=...)` 是否能在一个最小高风险工具审批流程中形成可恢复、可审计、可幂等的执行路径。

这个实验服务第 07、09 和 10 章，用来把 LangGraph 文档里的 HITL / persistence 机制落到可复现检查项，而不是把文档能力直接写成生产安全结论。

## 实验边界

这是一个真实框架实验 harness，当前环境尚未安装 LangGraph，因此只验证了保守 skip 分支。

未运行前，只能支撑“应该如何验证 LangGraph interrupt recovery”的教学边界，不能证明：

- LangGraph 默认提供完整审批安全。
- checkpointer 默认能防止重复执行、拒绝后执行或参数篡改。
- 任意持久化后端都满足生产恢复要求。
- trace 默认脱敏，或默认适合审计。
- LangGraph 比其他框架更可靠、更便宜或更容易上线。

## 最小任务设计

构建一个最小退款审批 graph：

- 用户请求退款。
- graph 生成退款参数：`order_id`、`user_id`、`amount`、`reason`。
- 在执行 `issue_refund` 前调用 `interrupt()`，把待审批参数交给调用方。
- 审批通过后继续执行模拟退款工具。
- 审批拒绝后停止执行。
- 每次执行写入审计 trace，但不能记录敏感字段原文。

推荐先使用本地假工具和内存订单数据，不接真实支付、邮件或数据库。

## 对照场景

至少覆盖这些 case：

| case | 操作 | 期望结果 | 主要验证点 |
| --- | --- | --- | --- |
| approved_once | 创建审批并批准一次 | 执行一次退款 | interrupt / resume 基本路径 |
| duplicate_resume | 对同一审批重复 resume | 不重复退款 | 幂等执行状态 |
| rejected_resume | 拒绝后尝试 resume | 不执行退款 | 审批状态校验 |
| tampered_args | 暂停后篡改 amount 再 resume | 阻断或记录完整差异 | 参数快照 / integrity |
| side_effect_before_interrupt | 在 interrupt 前写入副作用 | 明确失败或重复风险 | node restart 限制 |
| process_restart | 使用持久化 checkpointer 后重启再 resume | 状态仍可恢复 | checkpointer 持久化 |
| in_memory_restart | 使用内存型 checkpointer 后重启再 resume | 状态丢失或不可恢复 | 教程型保存器边界 |

## 运行前检查

- 记录 LangGraph / langchain-core / Python 版本和安装方式。
- 明确 checkpointer 类型：内存型、SQLite、Postgres 或其他。
- 为每个 run 使用唯一 `thread_id`，并记录恢复时是否复用同一个 `thread_id`。
- 不连接真实退款、支付、邮件、数据库或外部 API。
- 写工具必须是本地假实现，并记录执行次数。
- trace 中只保存脱敏参数、approval id、decision、resume attempt、result 和 error。

## 观察点

- `interrupt()` payload 是否只包含 JSON-serializable 数据。
- 恢复时 node 是否从头执行，`interrupt()` 前代码是否重跑。
- side effect 是否发生在 interrupt 之后。
- 拒绝、重复恢复和参数篡改是否被阻断。
- checkpointer 是否能跨进程恢复。
- 长会话 checkpoint 是否需要清理策略。
- trace 是否能区分 approval created、approved、rejected、executed、duplicate_resume、tamper_detected 和 redacted fields。
- 错误是否对初学者可解释。

## 最小结果表

| run | checkpointer | case | result | tool executions | trace redacted | latency | notable failure |
| --- | --- | --- | --- | ---: | --- | ---: | --- |
| TODO | in-memory | approved_once | pending | TBD | TBD | TBD | pending |
| TODO | in-memory | in_memory_restart | pending | TBD | TBD | TBD | pending |
| TODO | persistent | duplicate_resume | pending | TBD | TBD | TBD | pending |
| TODO | persistent | tampered_args | pending | TBD | TBD | TBD | pending |

## 运行方式

```bash
uv run python docs/experiments/real-langgraph-interrupt-recovery/real_langgraph_interrupt_recovery.py
```

当前结果见 [2026-07-11 结果](results-2026-07-11.md)。

## 结论状态

- 当前状态：真实 harness 已准备；当前环境未安装 LangGraph，运行结果为 `skipped`。
- 可支撑：第 07、09 和 10 章可以要求真实 LangGraph HITL 实验记录 interrupt payload、checkpointer、`thread_id`、node restart、side-effect placement、审批状态、参数快照、幂等执行和 trace 脱敏；无依赖时不能伪造真实结果。
- 不可支撑：不能写成 LangGraph interrupt、checkpointer 或任意 HITL 框架默认安全、默认生产可用或默认优于应用层状态机。

## 后续产出

真实 completed run 后应新增或更新：

- 依赖安装记录和版本锁定。
- completed `results-YYYY-MM-DD.md`。
- 脱敏 trace 样例。
- 持久化 checkpointer restart case。
- 对 source card、tool-permission evidence、coverage matrix、validation backlog 和第 07/09/10/12 章的同步更新。
