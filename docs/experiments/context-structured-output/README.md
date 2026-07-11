# 上下文治理与结构化输出实验

## 目标

验证第 02/03 章中的两个边界：结构化输出提升解析和 schema 校验可靠性，但不保证事实正确；长上下文能容纳更多资料，但不能替代来源选择、时效判断、权限隔离和评测。

## 实验边界

这是一个确定性的标准库实验，不调用模型、不接入真实 API。脚本包含两部分：

- 输出解析：比较 `free_text`、`json_mode` 和 `schema_validated`。
- 上下文治理：比较 `naive_long_context` 和 `governed_context`。

本实验不能证明真实模型或 OpenAI Structured Outputs 的实际表现。它只验证解析失败、schema mismatch、schema-valid semantic error、旧资料使用和外部文档注入的最小流程。

## 输入数据

输出解析部分使用三张假 ticket：

- 文档安装拼写问题。
- refund / charge dispute，需要 billing route 和 human review。
- 外部文件注入，要求导出 admin token，需要 security route 和 human review。

上下文治理部分使用三份假 context：

- 2024 旧 refund policy。
- 2026 当前 refund policy。
- 外部 ticket attachment，包含恶意指令。

## 运行方式

```bash
uv run python docs/experiments/context-structured-output/context_structured_output.py
```

## 观察点

- 自由文本是否难以稳定解析 enum、required fields 和 human-review 字段。
- JSON mode 是否可能产出 valid JSON 但不符合 schema。
- Schema validation 是否仍可能通过语义错误输出。
- Naive long context 是否会使用旧政策或服从外部文档指令。
- Governed context 是否能选择最新可信资料并隔离外部指令。

## 结论状态

- 支撑：可以把“Structured Outputs / schema validation 改善可解析性，但不保证业务/事实正确”写入第 02/03 章。
- 支撑：可以把“长上下文不是治理方案；仍需要来源、时效、信任、隔离和 trace”写入第 02/06/09 章。
- 仍缺：真实模型、真实 Responses API / Structured Outputs、长上下文 token/latency/cost、真实外部注入样本和跨模型稳定性实验。
