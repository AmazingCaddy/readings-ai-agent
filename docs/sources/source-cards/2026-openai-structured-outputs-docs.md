# OpenAI Structured Outputs Documentation

- 来源链接：https://developers.openai.com/api/docs/guides/structured-outputs
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；页面 last-modified 复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：官方文档
- 主题：Structured Outputs / JSON Schema / Response Format / Function Calling
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：Structured Outputs 页面已复核；“schema valid 不等于事实/权限/业务正确”边界已可入正文；上下文治理与结构化输出标准库实验已完成；Real Structured Outputs / JSON Mode harness 已准备并接入统一 runner，当前无 API key 时完成本地 deterministic schema/semantic control，并标记 `real_api_validated=false`

## 一句话总结

Structured Outputs 文档适合解释为什么程序消费的模型输出应该优先用 schema 约束，而不是只靠自然语言提示或普通 JSON mode。

## 核心结论

- 文档说明 Structured Outputs 会让模型输出遵循开发者提供的 JSON Schema，用于避免遗漏 required key 或产生无效 enum value。
- Structured Outputs 有两种形式：function calling，以及 `json_schema` response format / `text.format`。
- 文档区分 function calling 和 structured response：连接模型到工具、函数或系统数据时用 function calling；只是约束模型回复给用户的结构时用 structured output。
- 文档明确 Structured Outputs 是 JSON mode 的演进；JSON mode 只保证 valid JSON，不保证符合 schema。
- 文档说明 user-generated input 可能触发 refusal，应用需要用 `refusal` 字段或条件逻辑处理。
- 文档提醒 Structured Outputs 仍可能包含 mistakes；如果输入与 schema 完全无关，模型为了遵守 schema 可能 hallucinate，需要指令、示例、拆分任务或校验处理。
- 文档建议避免 JSON schema 和代码类型定义 divergence，可使用 Pydantic/Zod 或 CI 检查。

## 支撑证据

- 2026-07-11 抓取 `https://developers.openai.com/api/docs/guides/structured-outputs.md` 成功；页面包含 schema adherence、function calling vs `text.format`、Structured Outputs vs JSON mode、refusal、mistakes 和 schema divergence 等关键段落。
- 已与 Responses API reference、Function Calling docs 和 Text Generation docs 交叉验证结构化输出与工具调用边界。

## 可能的问题

- Structured Outputs 的可用性和支持的 JSON Schema 子集与模型/API 版本有关，正文不应写成所有模型都支持。
- Schema adherence 不等于事实正确；结构化输出可以让系统更容易解析和校验，但不能单独保证业务答案正确。
- JSON mode 仍可能在兼容性场景中有用，正文不应写成“绝对不能用 JSON mode”。

## 初学者阅读建议

- 先理解普通 JSON、JSON Schema、程序校验，再读 function calling 和 structured outputs 的区别。

## 可复现实验

- 已完成标准库上下文治理与结构化输出实验：对比自由文本、JSON-mode-like 输出和 schema validation，并记录 schema-valid semantic error。
- 已准备 [Real Structured Outputs / JSON Mode 对比实验](../../experiments/real-structured-output-validation/README.md) harness：无 API key 时运行本地 deterministic schema/semantic control，覆盖 parse failure、schema-valid semantic error 和 schema-valid semantic-ok；配置后可记录 free text、JSON mode、json_schema 的真实 schema valid / semantic valid / refusal 行为。当前尚未产生真实 API completed run，不能提前升级真实模型结论。

## 是否进入正文

- 结论：进入；窄边界可入正文
- 原因：第 02/03 章需要官方文档支撑结构化输出、JSON mode 和 function calling 的边界；官方文档、标准库实验和本地 schema/semantic control 共同支撑“schema adherence 不等于事实/业务正确”的应用层校验边界。真实 Responses API refusal、retry、跨模型稳定性和成本仍需实测。
