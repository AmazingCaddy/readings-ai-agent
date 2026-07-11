# OpenAI Function Calling / Tool Calling Documentation

- 来源链接：https://developers.openai.com/api/docs/guides/function-calling
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；页面 last-modified 复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：官方文档
- 主题：Tool Use / Function Calling / Structured Output
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接已复核；关键段落已精读；Tool Use / Function Calling 边界已交叉验证

## 一句话总结

这是解释现代 OpenAI API 中工具调用和函数调用机制的首选官方 reference。

## 核心结论

- 官方文档将 function calling 也称为 tool calling，用于让 OpenAI 模型连接外部系统，并访问训练数据之外的数据和应用提供的动作。
- 文档把 `function` / `tool` 定义为开发者告诉模型可访问的一项功能；模型可能在生成响应时决定需要使用该工具。
- 文档把 `function call` / `tool call` 定义为模型返回的一类特殊响应，表示模型请求使用某个可用工具。
- 文档把 `function call output` / `tool call output` 定义为应用侧工具根据模型工具调用输入生成的结果，并指出该结果需要引用具体 `call_id`。
- 官方工具调用流程包括：请求模型并提供可调用工具、接收模型工具调用、在应用侧执行代码、带工具输出再次请求模型、接收最终响应或更多工具调用。
- 文档明确 function 是 tool 的一种，通常由 JSON schema 定义；除 function tools 外，还有 custom tools 和 OpenAI 平台内置 tools。
- 文档建议启用 strict mode，并说明 strict mode 会让 function calls 更可靠地遵循 schema，而不是 best effort。

## 支撑证据

- 旧入口 `https://platform.openai.com/docs/guides/function-calling` 会 301 到 `https://developers.openai.com/api/docs/guides/function-calling`。
- 最终页面返回 HTTP 200。
- 2026-07-11 抓取 `https://developers.openai.com/api/docs/guides/function-calling.md` 成功；页面包含 “Function calling (also known as tool calling)” 和 “The tool calling flow has five high level steps” 等关键段落。

## 可能的问题

- 官方 API 文档更新频繁，需要记录复核日期。
- 需要和 OpenAI Agents SDK 文档区分：这是 API 层 tool calling，不是完整 Agent SDK 抽象。
- `tool_search`、custom tools、strict mode 等能力与模型和 API 版本有关，正文不应脱离文档版本泛化。

## 初学者阅读建议

- 先理解 tool schema、参数生成、工具结果回传，再看 SDK 框架封装。

## 可复现实验

- 设计一个参数校验失败的工具调用，观察模型是否能根据错误信息修正参数。

## 是否进入正文

- 结论：进入
- 原因：Tool Use / Function Calling 章节需要官方 API reference。
