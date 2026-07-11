# OpenAI Batch, Flex Processing and Prompt Caching Documentation

- 来源链接：
  - https://developers.openai.com/api/docs/guides/batch.md
  - https://developers.openai.com/api/docs/guides/flex-processing.md
  - https://developers.openai.com/api/docs/guides/prompt-caching.md
- 作者 / 机构：OpenAI
- 发布时间：持续更新 documentation
- 最后复核日期：2026-07-12
- 类型：Official Docs / Cost and Latency Engineering
- 主题：Batch API / Flex Processing / Prompt Caching
- 适合阶段：工程实践 / 生产化前检查
- 可信度等级：A
- 是否已验证：Batch、Flex Processing 和 Prompt Caching 三个官方 Markdown 页面已于 2026-07-12 复核，均返回 HTTP 200；关键段落已精读；可支撑异步批处理、低优先级处理、prompt cache key / explicit breakpoint / cache write 计费和提示缓存保留边界；标准库字段 audit 已完成；Real Production Cost / Latency / Rate-Limit harness 已补本地 accounting control，覆盖 `cached_tokens` / `cache_write_tokens` 汇总和 budget action；Real Batch / Flex / Prompt Caching harness 已完成本地 deterministic metadata control，覆盖 cache usage 字段聚合、Flex fallback 记录、Batch JSONL metadata、`custom_id` 唯一性和 required result fields，并标记 `real_api_validated=false`；Batch 提交默认 opt-in；真实节省、命中率、延迟、失败率、质量影响和生产适用性仍部分验证

## 一句话总结

Batch、Flex processing 和 Prompt Caching 都是成本/延迟治理工具，但它们不是通用加速按钮：Batch 适合离线或不需要即时响应的任务，Flex 适合可容忍慢响应和资源不可用的低优先级任务，Prompt Caching 依赖稳定长前缀和 cache read/write 观测。

## 核心结论

- Batch API 用 `.jsonl` 文件提交一组异步请求，适合 evaluations、large dataset classification、embedding repositories、offline jobs 等不需要立即响应的任务。
- Batch API 文档说明 batch 有验证、运行、完成、过期、取消等状态；结果输出顺序不保证和输入顺序一致，应使用 `custom_id` 映射结果。
- Batch 有独立的 rate-limit pool，不消耗 standard per-model rate limits；但有 per-batch request / file size、enqueued prompt tokens per model 和 batch creation rate limit 等限制。
- Batch 的 completion window 当前为 `24h`；超时会进入 `expired`，未完成请求取消，已完成请求结果可用并按已消耗 token 收费。
- Batch 当前 per-batch 上限包括最多 50,000 requests、200 MB input file、embedding batch 50,000 embedding inputs；输出文件会在 batch 完成 30 天后自动删除。
- Batch 当前支持 `/v1/responses`、chat completions、embeddings、completions、moderations、images 和 videos 等端点；视频 batch 只支持 `POST /v1/videos` JSON 请求，生成视频完成后最多可下载 24 小时；moderations batch 不接受 `stream=true`。
- Flex processing 通过 `service_tier: "flex"` 使用，适合 non-production、lower priority、model evaluations、data enrichment 和 asynchronous workloads。
- Flex processing 仍处于 beta，model availability limited；以较慢响应和偶发 `429 Resource Unavailable` 为代价换取较低成本，文档明确指出资源不可用时不收费，并建议指数退避或 fallback 到 standard processing。
- Prompt Caching 对 eligible requests 自动启用；缓存命中要求 exact prompt prefix match，因此应把 static instructions / examples / tools / schemas 放在 prompt 前部，把动态用户内容放在后部。
- Prompt Caching 文档说明 1024 tokens 或更长的 prompt 才有缓存资格；`cached_tokens` 和 `cache_write_tokens` 可用于监控缓存读写。
- GPT-5.6 及后续模型家族引入更明确的 cache write 语义：cache writes 按 1.25x uncached input token rate 计费，`prompt_cache_key` 可改善 shared prefix routing，explicit cache breakpoints 可控制缓存前缀，`prompt_cache_options.ttl` 当前只支持 `30m`。
- 对 GPT-5.6 及后续模型，`prompt_cache_retention` 已不再是保留策略入口；较早模型仍可使用 `in_memory` 或 `24h` retention policy，具体默认值受组织数据保留设置影响。
- Prompt Caching 不改变模型如何生成 output tokens，也不保证相同输出；缓存提示仍计入 TPM rate limits。
- Prompt Caching 的 privacy / retention 行为和模型、retention policy、组织数据设置有关；正文不应把缓存写成长期存储、手动可清除机制或默认隐私解决方案。

## 支撑证据

- 2026-07-12 使用 `curl -L -I https://developers.openai.com/api/docs/guides/batch.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 07:43:48 GMT`，`content-length: 16472`。
- 2026-07-12 使用 `curl -L -I https://developers.openai.com/api/docs/guides/flex-processing.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 09:23:14 GMT`，`content-length: 4005`。
- 2026-07-12 使用 `curl -L -I https://developers.openai.com/api/docs/guides/prompt-caching.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 06:30:11 GMT`，`content-length: 15350`。
- Batch API 文档列出支持端点、`.jsonl` input file、Files API upload、Batch object status、output / error files、`custom_id`、cancel 和 list 操作。
- Batch API 文档写明 requests per batch、input file size、embedding input、enqueued prompt tokens per model 和 batch creation rate limit；并写明 output file automatically deleted 30 days after batch complete。
- Batch API 文档补充 `/v1/videos` 和 `/v1/moderations` batch 边界：video batch 不支持 multipart uploads，batch-generated videos 最多可下载 24 小时；moderations batch 接受 text / image input，但拒绝 `stream=true`。
- Flex processing 文档明确说它以 slower response times 和 occasional resource unavailability 换取 lower costs，并要求对 timeout / `429 Resource Unavailable` 设计处理。
- Flex processing 文档写明 Flex is in beta with limited model availability，supported models 应看 pricing page；官方 SDK 默认 timeout 是 10 minutes，复杂任务可能需要提高 timeout。
- Prompt Caching 文档明确要求 exact prefix match、1024-token minimum、记录 `cached_tokens` / `cache_write_tokens`，并说明 caching does not affect rate limits。
- Prompt Caching 文档写明 `prompt_cache_key` 可改善 shared prefix routing；GPT-5.6 及后续模型必须设置 key 才能使用更可靠 matching；每个 key 总流量建议约 15 requests/minute，过高可能 miss cache。
- Prompt Caching 文档写明 explicit cache breakpoints 可放在 Responses / Chat Completions 的受支持 content block 上；每次请求最多产生 4 个 new cache writes，cache reads 最多考虑最新 50 个 breakpoints。
- Prompt Caching 文档写明 GPT-5.6 及后续模型 cache writes 按 1.25x uncached input token rate 计费，`prompt_cache_options.ttl` 当前只支持 `30m`；旧 `prompt_cache_retention` 对 GPT-5.6 及后续模型不适用。

## 可能的问题

- Batch、Flex 和 Prompt Caching 的成本、可用模型、费率和产品能力会变化；不要在正文硬编码具体价格或长期可用性。
- Batch 不适合需要即时用户交互的路径；结果顺序不稳定和过期处理需要进入 trace / eval。
- Flex 不适合高优先级生产同步路径，除非应用能接受慢响应、timeout、resource unavailable 和 fallback 成本。
- Prompt Caching 需要真实 workload 验证 cache hit rate 和 net cost；GPT-5.6 及后续模型 cache writes 可能增加成本，少量或高度动态 prompt 可能看不到收益。
- Prompt Caching 不提升输出质量，不消除 nondeterminism，也不减少 TPM rate-limit 影响。
- `gpt-5.6`、pricing、supported models、TTL 和 cache-write 计费属于当前文档状态；正文应记录复核日期，不应写成跨模型永久规则。

## 初学者阅读建议

- 先把 Batch 当成“离线任务队列”，只在 eval、批量分类、批量 embedding 这类不需要马上回复用户的任务里练习。
- Flex 先放在低优先级练习中，不要放到必须即时响应的核心路径。
- Prompt Caching 先学会记录 `prompt_cache_key`、explicit breakpoints、`cached_tokens`、`cache_write_tokens` 和 cache write cost，再讨论是否值得调整 prompt 结构。

## 可复现实验

- 已完成标准库 production cost / latency / rate-limit audit：它检查 Batch candidate/status/`custom_id`/expiration、Flex service tier/resource unavailable/fallback 和 Prompt Caching cache eligible/`cached_tokens`/`cache_write_tokens`/miss reason 字段。Real Production Cost / Latency / Rate-Limit harness 的本地 accounting control 进一步验证 usage/cache 字段提取和汇总逻辑。两者都不提交 Batch job、不使用 Flex、不触发真实 Prompt Caching，因此不证明真实收益、命中率、延迟或失败率。
- 已准备 [Real Batch / Flex / Prompt Caching Validation](../../experiments/real-batch-flex-caching-validation/README.md) harness：无 API key 时运行本地 deterministic metadata control；有 API key 时可观测 Prompt Caching usage 字段和 Flex response / API error；Batch JSONL metadata 默认只准备不提交，只有 `OPENAI_SUBMIT_BATCH=1` 才会创建 batch job。当前尚未产生真实 API completed run。
- 后续可选一个小型 eval dataset，用同步请求与 Batch API 对比：提交文件、batch status、completed / failed / expired request、`custom_id` 映射、成本估算和等待时间。
- 后续可用同一低优先级任务对比 standard vs flex：成功率、timeout、`429 Resource Unavailable`、fallback 次数、等待时间和成本估算。
- 后续可用一个长稳定 system prompt / tool schema 对比缓存前后：`prompt_cache_key`、explicit breakpoints、`cached_tokens`、`cache_write_tokens`、latency、cost estimate、cache write cost 和 cache miss 原因。

## 是否进入正文

- 结论：进入；作为成本/延迟治理工具的适用边界可入正文。
- 原因：官方文档直接支撑 Batch / Flex / Prompt Caching 的接口形态、适用场景、限制、计费/retention 变化和观测字段；标准库 audit 和本地 deterministic metadata control 支撑记录模板。仍需保守写明：它们不证明真实应用一定更便宜、更快或更可靠，具体收益必须用真实 workload 和 eval 记录。
