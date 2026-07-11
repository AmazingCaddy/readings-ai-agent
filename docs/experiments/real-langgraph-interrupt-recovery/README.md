# Real LangGraph Interrupt Recovery 实验

## 目标

验证 LangGraph current docs 中的 `interrupt()`、checkpointer、`thread_id` 和 `Command(resume=...)` 是否能在一个最小高风险工具审批流程中形成可恢复、可审计、可幂等的执行路径。

这个实验服务第 07、09 和 10 章，用来把 LangGraph 文档里的 HITL / persistence 机制落到可复现检查项，而不是把文档能力直接写成生产安全结论。

## 实验边界

这是一个真实框架实验 harness。本次使用 `uv run --with langgraph --with langchain-core` 临时依赖运行，已得到 LangGraph 1.2.9 / langchain-core 1.4.9 下的 completed 结果。

当前 completed run 覆盖 `MemorySaver`、`SqliteSaver` 同进程本地恢复、`SqliteSaver` 双 Python 进程本地恢复、本地假退款工具和一个最小 graph shape，不能证明：

- LangGraph 默认提供完整审批安全。
- checkpointer 默认能防止重复执行、拒绝后执行或参数篡改。
- 任意持久化后端都满足生产恢复要求，或部署式服务能在并发和故障中自动安全恢复。
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
| 2026-07-11 | `MemorySaver` | approved_once | completed / approved_executed | 1 | true | 22 ms | local fake tool only |
| 2026-07-11 | `MemorySaver` | duplicate_resume | completed / no second execution | 1 | true | 2 ms | returned completed state, not explicit duplicate block |
| 2026-07-11 | `MemorySaver` | rejected_resume | completed / rejected | 0 | true | 1 ms | local fake tool only |
| 2026-07-11 | `MemorySaver` | tampered_args | completed / argument_hash_mismatch | 0 | true | 1 ms | application-level hash check |
| 2026-07-11 | `SqliteSaver` | sqlite_process_restart | completed / approved_executed after graph rebuild | 1 after restart | true | 14 ms | same Python process; local SQLite only |
| 2026-07-11 | `SqliteSaver` | sqlite_subprocess_restart | completed / approved_executed after subprocess resume | 1 after restart | true | 1501 ms | two local Python processes; local SQLite only |

## 运行方式

```bash
uv run python docs/experiments/real-langgraph-interrupt-recovery/real_langgraph_interrupt_recovery.py
```

如果项目环境未安装 LangGraph，可用临时依赖运行，不修改 `pyproject.toml`：

```bash
uv run --with langgraph --with langchain-core --with langgraph-checkpoint-sqlite python docs/experiments/real-langgraph-interrupt-recovery/real_langgraph_interrupt_recovery.py
```

当前结果见 [2026-07-11 结果](results-2026-07-11.md)。

## 结论状态

- 当前状态：真实 harness 已在临时依赖环境下完成一次 `MemorySaver` run，并用 `langgraph-checkpoint-sqlite` 3.1.0 完成同进程 SQLite graph 重建恢复和双 Python 进程 prepare/resume 的本地最小 case。
- 可支撑：第 07、09 和 10 章可以写成“在最小 LangGraph run 中，`interrupt()` / `Command(resume=...)` / `thread_id` / `MemorySaver` 可跑通审批恢复；应用层参数 hash 可阻断篡改；拒绝不执行工具；重复 resume 未重复执行工具；trace 未泄露示例 secret marker。使用 `SqliteSaver` 和同一个 `thread_id`，同进程重建 graph 或由独立 Python 进程 resume，都可以在本地 SQLite checkpoint 上恢复并执行一次本地假工具”。
- 部分验证：重复 resume 本次返回已完成状态，而不是显式 duplicate-blocked 状态；SQLite restart case 是本地 SQLite 文件和本机 Python 进程，不等于部署服务重启、并发、故障注入或生产恢复；真实副作用、真实审批 UI、状态表、事务幂等、生产审计和跨框架对比仍待验证。
- 不可支撑：不能写成 LangGraph interrupt、checkpointer 或任意 HITL 框架默认安全、默认生产可用、默认脱敏、默认幂等或默认优于应用层状态机。

## 后续产出

真实 completed run 后应新增或更新：

- 脱敏 trace 样例。
- 对 source card、tool-permission evidence、coverage matrix、validation backlog 和第 07/09/10/12 章的同步更新。
