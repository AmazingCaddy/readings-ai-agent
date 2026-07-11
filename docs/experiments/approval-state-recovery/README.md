# 审批状态恢复与幂等性实验

## 目标

验证第 09 章中的工具权限边界：高风险工具不仅需要人工审批，还需要可恢复的审批状态、参数快照校验、幂等执行、拒绝后不执行，以及 trace 脱敏。

## 实验边界

这是一个确定性的 Python 标准库实验，不调用模型、不执行真实工具、不使用真实框架 guardrail。脚本比较两种策略：

- `naive_resume`：创建待审批记录后，恢复执行时只看 approval id，不检查是否已经执行、是否被拒绝、参数是否被篡改，也不对 trace 脱敏。
- `governed_resume`：恢复执行时检查审批状态、是否已执行、参数快照 hash、拒绝状态，并对 trace 脱敏。

本实验不能证明真实 OpenAI Agents SDK、Semantic Kernel、MCP host 或其他框架的 HITL 行为。它只验证审批状态恢复的最小 case 结构和记录字段。

## 覆盖 case

- 创建退款待审批记录。
- 批准后恢复执行退款。
- 重复恢复同一个已执行审批。
- 创建含敏感字段的邮件待审批记录。
- 拒绝后尝试恢复执行邮件。
- 创建第二个退款待审批记录。
- 恢复前篡改退款金额。

## 运行方式

```bash
uv run python docs/experiments/approval-state-recovery/approval_state_recovery.py
```

## 观察点

- 审批通过后是否只执行一次。
- 拒绝后的待审批动作是否仍可能产生副作用。
- 恢复执行时是否验证参数快照，避免审批的是 A 参数、执行的是 B 参数。
- trace 中是否泄露合成敏感值。
- 每个恢复结果是否能区分 `executed_once`、`already_executed`、`blocked_rejected` 和 `blocked_argument_mismatch`。

## 结论状态

- 支撑：可以把“human approval 必须包含可恢复状态、幂等执行、参数快照校验和拒绝后阻断”写入第 09 章。
- 仍缺：真实框架 HITL pause/resume、真实工具副作用、审批 UI、权限模型、成本、延迟、人工审批负担和跨框架覆盖范围实验。
