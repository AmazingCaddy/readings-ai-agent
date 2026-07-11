# OpenAI Responses API Reference

- 来源链接：https://developers.openai.com/api/reference/resources/responses
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；页面 last-modified 复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：官方文档 / API Reference
- 主题：LLM Application Architecture / Responses API / Tool Use
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接已复核；关键字段已抽样精读；工具调用与上下文工程相关结论已交叉验证

## 一句话总结

Responses API 是理解现代 OpenAI 应用接口、模型调用、工具调用和响应结构的重要官方 reference。

## 核心结论

- Responses API reference 将 `input` 定义为给模型生成响应的文本、图像或文件输入，并链接到 Function Calling guide。
- `tools` 参数包含多种工具类型，包括 function、custom、namespace、tool_search、web search、file search、remote MCP、code interpreter、computer use 等。
- Function tool 在 Responses reference 中包含 `name`、`type: "function"`、`parameters` 和 `strict` 等字段。
- Responses reference 对 `strict` 的说明与 Function Calling guide 一致：当 schema 兼容时可启用严格参数验证；不兼容时会回退或需要显式处理。
- Remote MCP 工具支持 `allowed_tools`、`require_approval`、`authorization`、`server_url` / `connector_id` 等字段，说明工具权限和审批是 API 层需要表达的边界之一。
- Responses reference 把 message input 建模为带 role 和 content 的结构化对象，并说明 developer/system instructions 优先于 user instructions。
- Reference 包含 `context_management`、`truncation`、`text.format` / `json_schema` 和 refusal 等字段，说明上下文管理、结构化输出和拒绝处理都是应用层需要显式处理的边界。

## 支撑证据

- `https://developers.openai.com/api/docs/api-reference/responses` 重定向到 `/api/reference/resources/responses` 并返回 HTTP 200。
- 旧 guide 入口 `https://developers.openai.com/api/docs/guides/responses` 返回 404，不应作为 reference 使用。
- 2026-07-11 抓取 `https://developers.openai.com/api/reference/resources/responses/index.md` 成功；页面包含 `input`、`tools`、function tool、MCP tool、`require_approval` 和 `strict` 等字段说明。
- 2026-07-11 复核同一页面中 message roles、`context_management`、`truncation`、`text.format`、`json_schema` 和 refusal 字段；已与 Text Generation 和 Structured Outputs 文档交叉验证第 02 章上下文工程边界。

## 可能的问题

- API reference 页面较长，初学者不适合从头阅读。
- 需要从章节正文中抽取最小必要概念，而不是堆 API 字段。
- API reference 是接口定义，不等同于完整工程安全指南；权限、审计和人工确认仍需结合生产化章节讨论。

## 初学者阅读建议

- 先读手册中的“模型输入输出”和“工具调用”章节，再把 API reference 当作查询资料。

## 可复现实验

- 已准备三个最小 Responses API harness：tool-calling 参数校验/重试、Structured Outputs / JSON mode 对比、prompt injection / permission。无 API key 时跳过，配置后可记录输入、输出、工具调用、错误处理、权限策略和 trace；结果待跑，不能提前升级结论。

## 是否进入正文

- 结论：进入
- 原因：LLM 基础、工具调用和实践项目都需要当前官方 API reference。
