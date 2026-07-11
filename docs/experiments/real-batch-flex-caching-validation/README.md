# Real Batch / Flex / Prompt Caching Validation

## 目标

把 OpenAI Batch、Flex Processing 和 Prompt Caching 文档中的观测字段迁移到真实 API harness：记录 Batch `custom_id` / status / output-error file 边界、Flex resource-unavailable / fallback 边界，以及 Prompt Caching `cached_tokens` / `cache_write_tokens` 观测字段。

这个实验用于准备真实验证入口，并在没有 API key 时验证本地记录字段模板；不用于证明 Batch、Flex 或 Prompt Caching 一定更便宜、更快或更可靠。

## 当前状态

- Harness 已准备：`real_batch_flex_caching_validation.py`
- 当前本地运行状态：`completed`；未设置 `OPENAI_API_KEY` 时运行 deterministic local control，并标记 `api_status=skipped_without_openai_api_key` / `real_api_validated=false`。
- 结果页：[2026-07-11 结果](results-2026-07-11.md)

## 运行方式

```bash
uv run python docs/experiments/real-batch-flex-caching-validation/real_batch_flex_caching_validation.py
```

可选环境变量：

- `OPENAI_API_KEY`：未设置时运行本地 deterministic control，不调用真实 API。
- `OPENAI_MODEL`：默认 `gpt-4.1-mini`。
- `OPENAI_RESPONSES_URL`：默认 `https://api.openai.com/v1/responses`。
- `OPENAI_FILES_URL`：默认 `https://api.openai.com/v1/files`。
- `OPENAI_BATCHES_URL`：默认 `https://api.openai.com/v1/batches`。
- `OPENAI_RUN_PROMPT_CACHING`：默认 `1`；设为 `0` 可跳过缓存观测请求。
- `OPENAI_RUN_FLEX`：默认 `1`；设为 `0` 可跳过 Flex 请求。
- `OPENAI_SUBMIT_BATCH`：默认 `0`；设为 `1` 才会上传 Batch JSONL 并创建 batch job。
- `OPENAI_BATCH_FLEX_MAX_OUTPUT_TOKENS`：默认 `40`，最大 `120`。

## 观察点

### 无 API key control

- Prompt Caching fixtures 记录 `cached_tokens` 和 `cache_write_tokens` 字段，并验证字段聚合逻辑。
- Flex fixture 记录模拟 `429 resource_unavailable` 和 fallback action。
- Batch fixture 复用 JSONL metadata 生成逻辑，验证 `custom_id` 唯一性、request count、endpoint 和 required result fields。

### Prompt Caching

- 使用两次具有相同长静态前缀的小请求。
- 记录 usage 中的 `input_tokens`、`output_tokens`、`total_tokens`、`cached_tokens`、`cache_write_tokens`。
- 记录 latency 和 rate-limit headers。

### Flex Processing

- 使用 `service_tier: "flex"` 的小请求。
- 成功时记录 latency、usage 和 rate-limit headers。
- `429 Resource Unavailable` 或其他 API error 会被记录为可观察事件，并提示应走 fallback。

### Batch API

- 默认只生成 Batch JSONL metadata，不提交异步 job。
- 记录 `custom_id`、endpoint、completion window、JSONL size 和 required result fields。
- 只有设置 `OPENAI_SUBMIT_BATCH=1` 时，才上传 file 并创建 batch job。

## 结论边界

- 可支撑：真实 API 验证入口、观测字段模板、无 API key 本地字段控制和 Batch opt-in 行为。
- 当前不能支撑：当前环境未设置 API key，没有真实 API completed run。本地 control 只验证 cache usage 字段聚合、Flex fallback 记录和 Batch JSONL metadata 检查；即使后续真实运行成功，也只能验证所选模型、prompt、账号、网络和时间窗口，不能证明 Batch / Flex / Prompt Caching 默认更便宜、更快、更稳定或保持质量。

## 下一步

1. 配置 API key 后运行 Prompt Caching 和 Flex 小样本。
2. 人工确认成本和异步任务边界后，用 `OPENAI_SUBMIT_BATCH=1` 跑最小 Batch job。
3. 把 completed run 的 Batch status、completed/failed/expired、`custom_id` 映射、cache read/write、Flex fallback、latency 和 cost estimate 同步回 source card、coverage matrix 和章节正文。
