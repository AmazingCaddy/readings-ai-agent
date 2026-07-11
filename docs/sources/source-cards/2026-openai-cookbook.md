# OpenAI Cookbook

- 来源链接：https://developers.openai.com/cookbook
- 作者 / 机构：OpenAI
- 发布时间：持续更新示例；页面 last-modified 复核为 2026-07-11；Usage/Cost recipe 发布时间为 2025-01-13
- 最后复核日期：2026-07-11
- 类型：Official Examples / Engineering
- 主题：LLM Application Development / Tool Use / RAG / Evals
- 适合阶段：入门 / 工程实践
- 可信度等级：A/B
- 是否已验证：索引页与若干具体 recipe 已复核；支撑“Cookbook 具体 recipe 可作为实践项目参考，但不能替代 API 文档、生产安全指南或本地实验”的窄边界可入正文；Usage/Cost 和 rate limit recipe 可支撑练习字段设计；实践路线 smoke harness 已补 project readiness audit，验证跟练项目需要 prerequisites、commands、acceptance checks、trace fields、failure examples、references 和 boundaries；真实试跑体验、账户数据和 API 行为仍部分验证

## 一句话总结

OpenAI Cookbook 适合为初学者提供可运行示例和项目模板；正文引用时应指向具体 recipe，并把它定位为“练习参考”，而不是规范文档或生产保证。

## 核心结论

- Cookbook 首页将其描述为面向 OpenAI models 的 notebook examples，适合补充实践项目，而不是替代 API reference。
- `Introduction to Structured Outputs` 包含 response format、function call usage、math tutor、summarization、entity extraction、refusal 等小节，可支撑“最小问答应用”和“结构化输出练习”。
- `Doing RAG on PDFs using File Search in the Responses API` 包含创建 vector store、standalone vector search、单次 API 调用整合搜索结果和 LLM、retrieval evaluation、Recall / Precision / MRR / MAP 等内容，可支撑“带来源的 RAG 问答”和“RAG eval 入门”。
- `Getting Started with OpenAI Evals` 包含设置、创建 eval dataset、运行 evaluation 和查看 eval logs，可支撑小型回归测试路线；页面同时提示 OpenAI 现在有 hosted evals product/API，旧框架材料需要谨慎引用。
- `Evaluating Agents with Langfuse` 包含 OpenAI Agents SDK trace、online/offline evaluation、dataset evaluation 和常见生产指标，可作为 Agent trace/eval 的工程示例，但第三方工具细节需要另行复核。
- `How to use the Usage API and Cost API to monitor your OpenAI usage` 可支撑生产化前的 usage/cost 练习字段：`start_time`、`end_time`、`bucket_width`、`group_by`、`project_id`、`line_item`、`amount.value` 和 `amount.currency`；它还示例了按日和 `line_item` 聚合、timestamp 转换和第三方 dashboard 集成。
- `How to handle rate limits` 可支撑生产化前的限流和重试练习字段：429 / `RateLimitError`、exponential backoff、最大重试约束、主动节流、batching、`max_tokens` 估算影响、fallback model 的质量/成本/延迟差异和并发请求脚本入口；它不证明任何重试策略或 fallback 默认有效。

## 支撑证据

- `https://cookbook.openai.com/` 重定向到 `https://developers.openai.com/cookbook` 并返回 HTTP 200。
- 已复核 recipe 页面：
  - `https://developers.openai.com/cookbook/examples/structured_outputs_intro`
  - `https://developers.openai.com/cookbook/examples/file_search_responses`
  - `https://developers.openai.com/cookbook/examples/evaluation/getting_started_with_openai_evals`
  - `https://developers.openai.com/cookbook/examples/agents_sdk/evaluate_agents`
  - `https://developers.openai.com/cookbook/examples/completions_usage_api`
  - `https://developers.openai.com/cookbook/examples/how_to_handle_rate_limits`

### Usage / Cost recipe 复核

- URL：`https://developers.openai.com/cookbook/examples/completions_usage_api`
- HTTP metadata：2026-07-11 复核返回 HTTP 200；canonical URL 为上述页面；content-type 为 `text/html`；last-modified 为 `Sat, 11 Jul 2026 06:19:49 GMT`。
- 页面 title：`How to use the Usage API and Cost API to monitor your OpenAI usage`。
- 页面定位：默认 usage/cost dashboard 对多数用户足够；需要更详细数据或自定义 dashboard 时，可使用 Completions Usage API 和 Costs API 拉取并可视化数据。
- 可支撑字段：usage 请求示例包含 `start_time`、可选 `end_time`、`bucket_width`、`project_ids`、`models`、`user_ids`、`api_key_ids`、`group_by`、`limit`；cost 示例包含 `start_time`、`bucket_width`、`group_by: ["line_item"]`、`limit`，并从结果中提取 `amount.value`、`amount.currency`、`line_item`、`project_id`。
- 可支撑实践：把 usage/cost 数据按日期、模型、项目、用户、API key 或 line item 聚合；把 Unix timestamp 转成日期；用 pandas/matplotlib 或第三方 dashboard 做监控原型。
- 边界：本 repo 没有用真实组织账户运行该 notebook，没有验证真实账单、项目过滤、dashboard 刷新、成本归因准确性或权限配置；只能把它作为生产化练习的字段和流程参考。

### Rate limits recipe 复核

- URL：`https://developers.openai.com/cookbook/examples/how_to_handle_rate_limits`
- HTTP metadata：2026-07-11 复核返回 HTTP 200；canonical URL 为上述页面；content-type 为 `text/html`；last-modified 为 `Sat, 11 Jul 2026 06:25:48 GMT`。
- 页面 title：`How to handle rate limits`。
- 页面定位：重复调用 API 时可能遇到 429 / `RateLimitError`；recipe 介绍如何用 exponential backoff、主动节流、batching 和并发处理脚本降低限流影响。
- 可支撑字段：错误类型、重试次数、最大等待/最大尝试、失败请求是否消耗预算、主动 sleep 间隔、RPM/RPD/TPM 区分、`max_tokens` 对 token 估算的影响、fallback model 是否共享限额、fallback 的 accuracy/latency/cost 差异、batching 后的单请求任务数和结构化输出 schema。
- 可支撑实践：为项目 8 设计 retry / throttle / batching 练习，记录 429、重试、等待、失败、fallback、延迟和质量影响；并把 `api_request_parallel_processor.py` 作为大批量请求处理脚本的进一步阅读入口。
- 边界：Tenacity/backoff 属于第三方工具，页面示例不能保证其可靠性或安全性；本 repo 没有真实触发 rate limit，也没有验证 retry、主动节流、batching、fallback 或并发脚本在当前账户和 workload 下的效果。

## 可能的问题

- Cookbook 是示例集合，不是规范文档。
- 不同示例可能使用不同版本 API，需要逐个复核。
- 示例通常简化权限、审计、部署、成本上限和安全边界；不能直接代表生产方案。
- 第三方工具示例需要分别核验第三方文档、版本和数据处理边界。
- Usage/Cost 和 rate limit recipe 可支撑练习字段，不可支撑真实成本、P95 latency、吞吐、限流阈值、fallback 质量或 dashboard 可靠性的结论。

## 初学者阅读建议

- 配合实践项目阅读，优先挑和章节主题直接相关的最小示例。
- 不要从首页随便选一个复杂 demo；先读 Structured Outputs、File Search RAG、Evals、Usage/Cost、Rate limits 这类能形成学习闭环的 recipe。

## 可复现实验

- 已完成标准库实践路线 smoke harness，验证结构化输出、refusal、工具参数校验、RAG 引用、无证据拒答和预算阻断可以组织成可重复 eval cases；扩展后的 project readiness audit 验证 6 个跟练项目卡片具备 prerequisites、setup/run commands、acceptance checks、trace fields、failure examples、references 和 boundaries；该结果不代表真实 Cookbook / API 行为。
- 后续从 Cookbook 选一个 Structured Outputs、RAG 或 eval 示例，改造成手册中的最小实践项目，并记录输入、输出、trace、失败样例、成本、依赖阻塞和故障排查步骤。

## 是否进入正文

- 结论：进入；实践参考边界可入正文
- 原因：实践项目路线需要官方示例 reference；具体正文应引用 recipe 页面，而不是笼统引用 Cookbook。Cookbook 可以支撑 Structured Outputs、File Search RAG、Evals、Agents trace/eval、Usage/Cost 和 Rate limits 等练习方向；其中 Usage/Cost 和 Rate limits recipe 可进一步支撑项目 8 的字段设计。实践路线 readiness audit 可支撑“跟练项目必须写清 prerequisites、命令、验收、trace、失败样例、references 和边界”的教程结构要求。它不能替代 API 文档、安全治理、本地验收、真实成本记录、真实限流实验或生产验证。
