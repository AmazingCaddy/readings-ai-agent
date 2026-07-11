# OpenAI Structured Outputs Documentation

- 来源链接：https://developers.openai.com/api/docs/guides/structured-outputs
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；Markdown 页面 last-modified 复核为 2026-07-11 06:34:03 GMT
- 最后复核日期：2026-07-12
- 类型：官方文档
- 主题：Structured Outputs / JSON Schema / Response Format / Function Calling
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：Structured Outputs HTML 与 Markdown 页面均于 2026-07-12 返回 HTTP 200；关键段落已复核；“schema valid 不等于事实/权限/业务正确”边界已可入正文；上下文治理与结构化输出标准库实验已完成；Real Structured Outputs / JSON Mode harness 已准备并接入统一 runner，当前无 API key 时完成本地 deterministic schema/semantic control，并标记 `real_api_validated=false`

## 一句话总结

Structured Outputs 文档适合解释为什么程序消费的模型输出应该优先用 schema 约束，而不是只靠自然语言提示或普通 JSON mode。

## 核心结论

- 文档说明 Structured Outputs 会让模型输出遵循开发者提供的 JSON Schema，用于避免遗漏 required key 或产生无效 enum value。
- 文档说明 Structured Outputs 从 GPT-4o 起可用于最新大模型；新项目建议使用当前推荐模型，较旧模型可能只能使用 JSON mode；`response_format: {type: "json_schema"}` 的支持也受模型 snapshot 限制。
- Structured Outputs 有两种形式：function calling，以及 `json_schema` response format / `text.format`。
- 文档区分 function calling 和 structured response：连接模型到工具、函数或系统数据时用 function calling；只是约束模型回复给用户的结构时用 structured output。
- 文档明确 Structured Outputs 是 JSON mode 的演进；JSON mode 只保证 valid JSON，不保证符合 schema。
- 文档说明 user-generated input 可能触发 refusal，应用需要用 `refusal` 字段或条件逻辑处理。
- 文档提醒 Structured Outputs 仍可能包含 mistakes；如果输入与 schema 完全无关，模型为了遵守 schema 可能 hallucinate，需要指令、示例、拆分任务或校验处理。
- 文档建议避免 JSON schema 和代码类型定义 divergence，可使用 Pydantic/Zod 或 CI 检查。
- JSON mode 仍可能产生 edge cases；使用 JSON mode 时必须在 conversation 中明确要求模型输出 JSON，否则可能出现持续 whitespace 直到 token limit，API 也会检查上下文中是否出现 “JSON”。

## 支撑证据

- `https://developers.openai.com/api/docs/guides/structured-outputs` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:08:21 GMT`；`content-type: text/html; charset=utf-8`。
- `https://developers.openai.com/api/docs/guides/structured-outputs.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:34:03 GMT`；`content-type: text/markdown; charset=utf-8`。
- 2026-07-12 抓取 Markdown 成功；页面包含 supported models、schema adherence、function calling vs `text.format`、Structured Outputs vs JSON mode、refusal、handling user-generated input、mistakes、schema divergence、JSON mode explicit instruction 和 edge cases 等关键段落。
- 已与 Responses API reference、Function Calling docs 和 Text Generation docs 交叉验证结构化输出与工具调用边界。

## 可能的问题

- Structured Outputs 的可用性和支持的 JSON Schema 子集与模型/API 版本有关，正文不应写成所有模型都支持。
- Schema adherence 不等于事实正确；结构化输出可以让系统更容易解析和校验，但不能单独保证业务答案正确。
- JSON mode 仍可能在兼容性场景中有用，正文不应写成“绝对不能用 JSON mode”。
- JSON mode 的 valid JSON 保证仍需要应用检测 incomplete JSON、whitespace/token-limit edge cases，并用 validation library / retry 补 schema 检查；不能把 JSON mode 当成 schema adherence。
- Pydantic/Zod 或 CI 只能减少 schema 与代码类型分叉，不证明真实输出语义正确、引用可信、权限判断正确或 refusal 策略可靠。

## 初学者阅读建议

- 先理解普通 JSON、JSON Schema、程序校验，再读 function calling 和 structured outputs 的区别。

## 可复现实验

- 已完成标准库上下文治理与结构化输出实验：对比自由文本、JSON-mode-like 输出和 schema validation，并记录 schema-valid semantic error。
- 已准备 [Real Structured Outputs / JSON Mode 对比实验](../../experiments/real-structured-output-validation/README.md) harness：无 API key 时运行本地 deterministic schema/semantic control，覆盖 parse failure、schema-valid semantic error 和 schema-valid semantic-ok；配置后可记录 free text、JSON mode、json_schema 的真实 schema valid / semantic valid / refusal 行为。当前尚未产生真实 API completed run，不能提前升级真实模型结论。

## 是否进入正文

- 结论：进入；窄边界可入正文
- 原因：第 02/03 章需要官方文档支撑结构化输出、JSON mode、function calling、refusal 和 schema/type drift 的边界；官方文档、标准库实验和本地 schema/semantic control 共同支撑“schema adherence 不等于事实/业务正确”的应用层校验边界。真实 Responses API refusal、retry、跨模型稳定性、模型支持差异和成本仍需实测。
