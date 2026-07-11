# OpenAI Batch, Flex Processing and Prompt Caching Documentation

- 来源链接：
  - https://developers.openai.com/api/docs/guides/batch.md
  - https://developers.openai.com/api/docs/guides/flex-processing.md
  - https://developers.openai.com/api/docs/guides/prompt-caching.md
- 作者 / 机构：OpenAI
- 发布时间：持续更新 documentation
- 最后复核日期：2026-07-11
- 类型：Official Docs / Cost and Latency Engineering
- 主题：Batch API / Flex Processing / Prompt Caching
- 适合阶段：工程实践 / 生产化前检查
- 可信度等级：A
- 是否已验证：三个官方 Markdown 页面均返回 HTTP 200；关键段落已精读；可支撑异步批处理、低优先级处理和提示缓存的工程边界；真实节省、命中率、延迟、失败率、质量影响和生产适用性仍部分验证

## 一句话总结

Batch、Flex processing 和 Prompt Caching 都是成本/延迟治理工具，但它们不是通用加速按钮：Batch 适合离线或不需要即时响应的任务，Flex 适合可容忍慢响应和资源不可用的低优先级任务，Prompt Caching 依赖稳定长前缀和 cache read/write 观测。

## 核心结论

- Batch API 用 `.jsonl` 文件提交一组异步请求，适合 evaluations、large dataset classification、embedding repositories、offline jobs 等不需要立即响应的任务。
- Batch API 文档说明 batch 有验证、运行、完成、过期、取消等状态；结果输出顺序不保证和输入顺序一致，应使用 `custom_id` 映射结果。
- Batch 有独立的 rate-limit pool，不消耗 standard per-model rate limits；但有 per-batch request / file size、enqueued prompt tokens per model 和 batch creation rate limit 等限制。
- Batch 的 completion window 当前为 `24h`；超时会进入 `expired`，未完成请求取消，已完成请求结果可用并按已消耗 token 收费。
- Flex processing 通过 `service_tier: "flex"` 使用，适合 non-production、lower priority、model evaluations、data enrichment 和 asynchronous workloads。
- Flex processing 以较慢响应和偶发 `429 Resource Unavailable` 为代价换取较低成本；文档明确指出资源不可用时不收费，并建议指数退避或 fallback 到 standard processing。
- Prompt Caching 对 eligible requests 自动启用；缓存命中要求 exact prompt prefix match，因此应把 static instructions / examples / tools / schemas 放在 prompt 前部，把动态用户内容放在后部。
- Prompt Caching 文档说明 1024 tokens 或更长的 prompt 才有缓存资格；`cached_tokens` 和 `cache_write_tokens` 可用于监控缓存读写。
- Prompt Caching 不改变模型如何生成 output tokens，也不保证相同输出；缓存提示仍计入 TPM rate limits。
- Prompt Caching 的 privacy / retention 行为和模型、retention policy、组织数据设置有关；正文不应把缓存写成长期存储、手动可清除机制或默认隐私解决方案。

## 支撑证据

- `batch.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:48:00 GMT`；`content-type: text/markdown; charset=utf-8`。
- `flex-processing.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 10:31:31 GMT`；`content-type: text/markdown; charset=utf-8`。
- `prompt-caching.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:23:41 GMT`；`content-type: text/markdown; charset=utf-8`。
- Batch API 文档列出支持端点、`.jsonl` input file、Files API upload、Batch object status、output / error files、`custom_id`、cancel 和 list 操作。
- Flex processing 文档明确说它以 slower response times 和 occasional resource unavailability 换取 lower costs，并要求对 timeout / `429 Resource Unavailable` 设计处理。
- Prompt Caching 文档明确要求 exact prefix match、1024-token minimum、记录 `cached_tokens` / `cache_write_tokens`，并说明 caching does not affect rate limits。

## 可能的问题

- Batch、Flex 和 Prompt Caching 的成本、可用模型、费率和产品能力会变化；不要在正文硬编码具体价格或长期可用性。
- Batch 不适合需要即时用户交互的路径；结果顺序不稳定和过期处理需要进入 trace / eval。
- Flex 不适合高优先级生产同步路径，除非应用能接受慢响应、timeout、resource unavailable 和 fallback 成本。
- Prompt Caching 需要真实 workload 验证 cache hit rate；少量或高度动态 prompt 可能看不到收益。
- Prompt Caching 不提升输出质量，不消除 nondeterminism，也不减少 TPM rate-limit 影响。

## 初学者阅读建议

- 先把 Batch 当成“离线任务队列”，只在 eval、批量分类、批量 embedding 这类不需要马上回复用户的任务里练习。
- Flex 先放在低优先级练习中，不要放到必须即时响应的核心路径。
- Prompt Caching 先学会记录 `cached_tokens` 和 `cache_write_tokens`，再讨论是否值得调整 prompt 结构。

## 可复现实验

- 已完成标准库 production cost / latency / rate-limit audit：它检查 Batch candidate/status/`custom_id`/expiration、Flex service tier/resource unavailable/fallback 和 Prompt Caching cache eligible/`cached_tokens`/`cache_write_tokens`/miss reason 字段。该实验不提交 Batch job、不使用 Flex、不触发 Prompt Caching，因此不证明真实收益、命中率、延迟或失败率。
- 后续可选一个小型 eval dataset，用同步请求与 Batch API 对比：提交文件、batch status、completed / failed / expired request、`custom_id` 映射、成本估算和等待时间。
- 后续可用同一低优先级任务对比 standard vs flex：成功率、timeout、`429 Resource Unavailable`、fallback 次数、等待时间和成本估算。
- 后续可用一个长稳定 system prompt / tool schema 对比缓存前后：`cached_tokens`、`cache_write_tokens`、latency、cost estimate 和 cache miss 原因。

## 是否进入正文

- 结论：进入；作为成本/延迟治理工具的适用边界可入正文。
- 原因：官方文档直接支撑 Batch / Flex / Prompt Caching 的接口形态、适用场景、限制和观测字段。仍需保守写明：它们不证明真实应用一定更便宜、更快或更可靠，具体收益必须用真实 workload 和 eval 记录。
