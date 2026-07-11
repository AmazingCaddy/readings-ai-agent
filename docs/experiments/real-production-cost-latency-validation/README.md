# Real Production Cost / Latency / Rate-Limit Validation

## 目标

把标准库 production cost / latency / rate-limit audit 中的字段，迁移到真实 Responses API 最小练习里：记录请求数、token usage、rate-limit headers、平均 / P95 latency、预算阈值、成本估算状态和降级动作。

## 实验边界

这是一个需要真实 OpenAI API 才能验证真实成本和延迟的 harness。没有 `OPENAI_API_KEY` 时脚本会改跑本地 deterministic accounting control，并标记 `api_status=skipped_without_openai_api_key`、`real_api_validated=false`，不写成真实 API 结果。

本实验只验证所选模型、所选 prompt、所选账户限流条件、当前网络路径和当前时间窗口下的观测字段。它不验证 Batch、Flex、Prompt Caching 收益，不验证质量取舍，不验证并发吞吐，也不证明任何生产可靠性。

## 运行方式

```bash
uv run python docs/experiments/real-production-cost-latency-validation/real_production_cost_latency_validation.py
```

可选环境变量：

- `OPENAI_MODEL`：默认 `gpt-4.1-mini`。
- `OPENAI_RESPONSES_URL`：默认 `https://api.openai.com/v1/responses`。
- `OPENAI_COST_LATENCY_RUNS`：默认 `3`，最大 `5`。
- `OPENAI_MAX_OUTPUT_TOKENS`：默认 `80`，最大 `300`。
- `OPENAI_COST_BUDGET_THRESHOLD`：默认 `0.05`。
- `OPENAI_INPUT_PRICE_PER_MILLION`：可选，用于成本估算。
- `OPENAI_OUTPUT_PRICE_PER_MILLION`：可选，用于成本估算。

## 观察点

- API 是否返回 usage 中的 input / output / total tokens。
- HTTP response 是否包含 request/token rate-limit headers。
- 多次小请求的平均 latency 和 P95 latency。
- 成本估算是否有明确价格来源；没有价格环境变量时应标记为 unknown，而不是编造价格。
- budget threshold 是否连接到 `continue`、`degrade` 或 `unknown_without_prices`。
- 结果是否足以回填标准库 audit 的字段表。
- 无 API key 时，本地 deterministic fixture 是否能验证 usage/cache 字段提取、rate-limit header 解析、平均 / P95 latency、成本估算、budget action 和汇总逻辑。

## 结论状态

- 当前状态：harness 已准备；无 API key 时完成本地 deterministic accounting control；真实 API completed run 仍未运行。
- 可支撑：真实练习入口、字段记录模板、保守 API 边界，以及本地 usage/cache/latency/cost/budget 汇总逻辑。
- 不能支撑：真实 API 成本、P95 latency、吞吐、缓存命中率、Batch / Flex / Prompt Caching 收益、质量取舍或生产可靠性。
