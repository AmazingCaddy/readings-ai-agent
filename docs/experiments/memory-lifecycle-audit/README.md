# 长期记忆生命周期与权限审计实验

## 目标

验证第 06 章中的长期记忆 lifecycle 边界：长期记忆系统不只需要“写入守门”，还需要用户可检查、可编辑、可删除、跨用户隔离、删除后不再召回，以及 trace 脱敏。

## 实验边界

这是一个确定性的 Python 标准库实验，不调用模型、不接入真实 memory framework。脚本比较两种策略：

- `naive_memory`：所有 active 记忆都可见；编辑直接覆盖；删除不生效；召回不做敏感字段过滤或跨用户隔离。
- `governed_memory`：按 actor / target user 做权限判断；inspect / recall 过滤敏感记录；edit 保留 invalidated history；delete 把记录标为 deleted 并脱敏；trace 也做脱敏。

本实验不能证明长期记忆能提升任务质量，也不能证明 Letta、Zep、LangGraph 或其他真实框架的行为。它只把 lifecycle 和权限要求变成可运行的最小验收样例。

## 输入数据

初始记忆包括：

- `user-1` 的语言偏好和项目框架事实。
- `user-1` 的一条合成敏感记录。
- `user-2` 的语言偏好。

操作序列包括：

- 用户查看自己的记忆。
- 用户尝试查看其他用户的记忆。
- 用户编辑自己的偏好。
- 用户删除自己的敏感记录。
- 删除后再次召回。
- 用户尝试召回其他用户的记忆。

## 运行方式

```bash
uv run python docs/experiments/memory-lifecycle-audit/memory_lifecycle_audit.py
```

## 观察点

- 是否阻断跨用户 inspect / recall。
- edit 是否保留旧版本 invalidated history。
- delete 是否真的让敏感记录退出 active memory 和后续 recall。
- trace 是否避免泄露敏感值。
- naive 策略会把哪些缺失治理能力暴露出来。

## 结论状态

- 支撑：可以把“长期记忆需要用户可查看/可编辑/可删除、跨用户权限隔离、删除后不召回和 trace 脱敏”写入第 06 章。
- 仍缺：真实 memory framework、多会话真实任务、UI / API 层用户控制、权限模型、长期污染概率、收益指标、成本和延迟。
