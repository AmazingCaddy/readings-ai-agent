# Production Cost / Latency / Rate-Limit Audit

## 目标

把 OpenAI Production、Cost、Latency、Rate Limits、Token Counting、Batch、Flex 和 Prompt Caching 文档中的生产质量边界，整理成一个可运行的字段审计。这个实验不是为了证明任何真实 API workload 更便宜、更快或更稳定，而是为了验证：上线前应记录哪些字段，哪些优化手段需要质量检查和降级策略。

## 实验边界

当前实验是 Python 标准库 deterministic audit。它不会调用 OpenAI API，不读取真实 rate-limit headers，不提交 Batch job，不使用 Flex，不触发 Prompt Caching，也不计算真实价格。

## 资料来源

- [OpenAI Production, Cost, Latency and Rate Limit Documentation](../../sources/source-cards/2026-openai-production-cost-latency-docs.md)
- [OpenAI Batch, Flex Processing and Prompt Caching Documentation](../../sources/source-cards/2026-openai-batch-flex-prompt-caching-docs.md)
- [OpenAI Cookbook](../../sources/source-cards/2026-openai-cookbook.md)

## 检查项

| rule id | 重点 | 必查字段 |
| --- | --- | --- |
| `usage_and_token_accounting` | 成本要能回放。 | model、input/output tokens、request count、cost estimate |
| `rate_limit_headers` | 限流要能观测。 | request/token limit、remaining、reset fields |
| `retry_backoff` | 重试不能无限循环。 | retry count、backoff、jitter、max retries、stop reason |
| `latency_distribution` | 延迟不能只看单次样本。 | latency、average latency、P95 latency、timeout |
| `budget_gate` | 超预算要有动作。 | threshold、spent、action、degraded mode |
| `model_and_output_controls` | 降成本/延迟不能牺牲质量而不记录。 | model choice reason、max output tokens、output policy、quality check |
| `batch_workload_boundary` | Batch 是异步边界。 | batch candidate、status、custom id mapping、expiration policy |
| `flex_fallback` | Flex 需要资源不可用处理。 | service tier、resource unavailable count、fallback strategy、fallback cost note |
| `prompt_cache_observability` | Prompt Caching 需要缓存读写字段。 | cache eligible、cached tokens、cache write tokens、cache miss reason |

## 运行方式

```bash
uv run python docs/experiments/production-cost-latency-rate-limit/production_cost_latency_rate_limit.py
```

当前标准库结果见 [2026-07-11 结果](results-2026-07-11.md)。

## 对照组

- `naive_run`：记录少量 token、latency、retry 和 budget spent，但缺少 request count、cost estimate、rate-limit headers、bounded backoff、P95、budget action、model/output control、Batch/Flex/Prompt Caching 字段。
- `governed_run`：记录完整字段，包括 rate-limit headers、bounded retry、latency distribution、budget gate、model/output policy、quality check、Batch status、Flex fallback 和 cache read/write。

## 结论状态

- 当前状态：标准库 audit 已完成；真实 API / Cookbook 练习待跑。
- 可支撑：章节和实践路线可以写成“生产成本、延迟和限流检查表应记录 token/usage、rate-limit headers、bounded retry、平均/P95 latency、budget threshold/action、model/output controls、Batch/Flex/Prompt Caching 观测字段和降级策略”。
- 不能支撑：不能证明任何真实模型、Batch、Flex、Prompt Caching、streaming、较小模型或 token 缩减策略一定降低成本、降低 P95 latency、提高吞吐或保持质量。

## 下一步

1. 在真实 API / Cookbook 练习中填同一字段表，记录真实 rate-limit headers、token usage、latency、cost estimate 和失败样例。
2. 对比同一任务的 smaller model、shorter output、streaming、Batch、Flex、Prompt Caching、parallel / sequential 等条件，先看质量和 trace，再谈优化。
3. 把预算超限、rate-limit、timeout、Flex 429、Batch expired 和 cache miss 作为回归样例。
