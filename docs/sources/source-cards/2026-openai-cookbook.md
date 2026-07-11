# OpenAI Cookbook

- 来源链接：https://developers.openai.com/cookbook
- 作者 / 机构：OpenAI
- 发布时间：持续更新示例；页面 last-modified 复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：Official Examples / Engineering
- 主题：LLM Application Development / Tool Use / RAG / Evals
- 适合阶段：入门 / 工程实践
- 可信度等级：A/B
- 是否已验证：索引页与若干具体 recipe 已复核；适合支撑实践项目模板；不应当作 API 规范或生产最佳实践直接引用

## 一句话总结

OpenAI Cookbook 适合为初学者提供可运行示例和项目模板；正文引用时应指向具体 recipe，并把它定位为“练习参考”，而不是规范文档或生产保证。

## 核心结论

- Cookbook 首页将其描述为面向 OpenAI models 的 notebook examples，适合补充实践项目，而不是替代 API reference。
- `Introduction to Structured Outputs` 包含 response format、function call usage、math tutor、summarization、entity extraction、refusal 等小节，可支撑“最小问答应用”和“结构化输出练习”。
- `Doing RAG on PDFs using File Search in the Responses API` 包含创建 vector store、standalone vector search、单次 API 调用整合搜索结果和 LLM、retrieval evaluation、Recall / Precision / MRR / MAP 等内容，可支撑“带来源的 RAG 问答”和“RAG eval 入门”。
- `Getting Started with OpenAI Evals` 包含设置、创建 eval dataset、运行 evaluation 和查看 eval logs，可支撑小型回归测试路线；页面同时提示 OpenAI 现在有 hosted evals product/API，旧框架材料需要谨慎引用。
- `Evaluating Agents with Langfuse` 包含 OpenAI Agents SDK trace、online/offline evaluation、dataset evaluation 和常见生产指标，可作为 Agent trace/eval 的工程示例，但第三方工具细节需要另行复核。
- `How to use the Usage API and Cost API to monitor your OpenAI usage` 与 `How to handle rate limits` 可支撑生产化前的成本、用量、限流和重试练习。

## 支撑证据

- `https://cookbook.openai.com/` 重定向到 `https://developers.openai.com/cookbook` 并返回 HTTP 200。
- 已复核 recipe 页面：
  - `https://developers.openai.com/cookbook/examples/structured_outputs_intro`
  - `https://developers.openai.com/cookbook/examples/file_search_responses`
  - `https://developers.openai.com/cookbook/examples/evaluation/getting_started_with_openai_evals`
  - `https://developers.openai.com/cookbook/examples/agents_sdk/evaluate_agents`
  - `https://developers.openai.com/cookbook/examples/completions_usage_api`
  - `https://developers.openai.com/cookbook/examples/how_to_handle_rate_limits`

## 可能的问题

- Cookbook 是示例集合，不是规范文档。
- 不同示例可能使用不同版本 API，需要逐个复核。
- 示例通常简化权限、审计、部署、成本上限和安全边界；不能直接代表生产方案。
- 第三方工具示例需要分别核验第三方文档、版本和数据处理边界。

## 初学者阅读建议

- 配合实践项目阅读，优先挑和章节主题直接相关的最小示例。
- 不要从首页随便选一个复杂 demo；先读 Structured Outputs、File Search RAG、Evals、Usage/Cost、Rate limits 这类能形成学习闭环的 recipe。

## 可复现实验

- 从 Cookbook 选一个 Structured Outputs、RAG 或 eval 示例，改造成手册中的最小实践项目，并记录输入、输出、trace、失败样例和成本。

## 是否进入正文

- 结论：进入
- 原因：实践项目路线需要官方示例 reference；具体正文应引用 recipe 页面，而不是笼统引用 Cookbook。
