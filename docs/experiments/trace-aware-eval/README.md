# Trace-Aware Eval 最小实验

## 目标

验证手册第 08 章中的工程边界：Agent eval 不能只看最终答案。对于会调用工具或产生外部副作用的 Agent，trace-aware scoring 能发现 final-answer-only scoring 看不到的过程错误。

## 实验边界

这是一个确定性的标准库实验，不调用模型、不调用真实工具、不使用 LangSmith、Phoenix 或 OpenAI Evals。脚本内置 3 条 toy refund Agent runs，并分别使用 final-answer-only scorer 和 trace-aware scorer 评分。

本实验不能证明某个自动评分器可靠，也不能证明真实业务 eval 的覆盖率。它只验证过程评分能捕捉哪些类型的错误，以及 trace 字段应该覆盖哪些事件。

## 输入数据

3 条 toy runs：

- `safe_refund_review`：查订单、查退款政策、只草拟建议，没有执行退款。
- `unsafe_direct_refund`：最终文本看似安全，但 trace 中直接调用 `issue_refund`，且没有审批。
- `ignored_tool_error`：最终文本看似合理，但 trace 中 `get_order` 返回 `not_found` 后没有恢复或升级处理。

## 运行方式

```bash
uv run python docs/experiments/trace-aware-eval/trace_aware_eval.py
```

## 观察点

- final-answer-only scorer 是否只能检查最终文本关键词。
- trace-aware scorer 是否能检查工具调用、退款政策检查、审批事件和工具错误恢复。
- 同一最终答案通过时，trace-aware scorer 是否能暴露过程风险。

## 结论状态

- 支撑：可以把“Agent eval 应检查关键 trajectory / trace，而不是只看最终答案”写入第 08 章。
- 仍缺：真实模型 / 工具 / RAG trace，LLM-as-judge 误判分析，人工抽样复核，成本/延迟统计和真实 observability 平台对照。
