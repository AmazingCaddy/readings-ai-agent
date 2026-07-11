# Real Trace-Aware Eval 实验

## 目标

验证真实模型 tool-calling 运行中，final-answer-only scoring 与 trace-aware scoring 能发现的错误是否不同。实验重点是 trace 字段、工具错误恢复、写工具审批和最终答案之间的差异。

## 实验边界

这是一个需要真实 OpenAI API 的实验 harness。没有 `OPENAI_API_KEY` 时脚本会输出 `skipped`，不写成已验证结果。

脚本使用 toy tools，不访问真实订单系统，也不会执行真实退款。写工具 `issue_refund` 在策略层默认拒绝，用于观察 trace-aware scorer 是否能检查 side-effect tool 的审批边界。

本实验不是 OpenAI Evals、LangSmith 或 Phoenix 的平台对照；它只准备真实模型 trace 和两种评分的最小可复现样例。

## 运行方式

```bash
uv run python docs/experiments/real-trace-aware-eval/real_trace_aware_eval.py
```

可选环境变量：

- `OPENAI_MODEL`：默认 `gpt-4.1-mini`。
- `OPENAI_RESPONSES_URL`：默认 `https://api.openai.com/v1/responses`。

## 观察点

- final-only scorer 是否只看最终文本关键词。
- trace-aware scorer 是否检查 `get_order`、`check_refund_policy`、`tool_error`、`approval_rejected` 和 side-effect tool。
- 模型在工具错误后是否恢复、升级或继续编造。
- 写工具是否被策略阻断，trace 是否记录阻断原因。

## 结论状态

- 当前状态：harness 已准备；真实结果取决于本地是否配置 API key 和模型版本。
- 未完成前不得把真实 Agent trace-aware eval 效果写成正文结论。
