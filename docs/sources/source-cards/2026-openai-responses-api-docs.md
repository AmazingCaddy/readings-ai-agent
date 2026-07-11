# OpenAI Responses API Reference

- 来源链接：https://developers.openai.com/api/reference/resources/responses
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；Markdown 页面 last-modified 复核为 2026-07-11 17:53:14 GMT
- 最后复核日期：2026-07-12
- 类型：官方文档 / API Reference
- 主题：LLM Application Architecture / Responses API / Tool Use
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：HTML 与 Markdown reference 均于 2026-07-12 返回 HTTP 200；关键字段已抽样精读；输入输出结构化接口、上下文治理、tool choice / permissions 和 JSON response-format 窄边界可入正文；工具调用与上下文工程相关结论已交叉验证；真实运行行为仍部分验证

## 一句话总结

Responses API 是理解现代 OpenAI 应用接口、模型调用、工具调用和响应结构的重要官方 reference。

## 核心结论

- Responses API reference 将 `input` 定义为给模型生成响应的文本、图像或文件输入；message input 具有 role / content / type 等结构，developer/system instructions 优先于 user instructions。
- `conversation` 会把对话 item 自动加入上下文；`previous_response_id` 可用于多轮，但不能和 `conversation` 同用；`instructions` 与 `previous_response_id` 同用时，上一轮 instructions 不会自动带到下一轮。
- `include` 可显式要求返回 web/file search results、code interpreter outputs、computer call output image URL、input image URL、reasoning encrypted content 和 output text logprobs 等附加数据；应用不能只假设最终可见文本就是完整响应。
- `tools` 参数包含多种工具类型，包括 function、custom、namespace、tool_search、web search、file search、remote MCP、code interpreter、computer use、shell / local_shell、apply_patch、image generation 等；这说明 Responses 是工具接口集合，不等于某一种安全运行时。
- Function tool 在 Responses reference 中包含 `name`、`type: "function"`、`parameters`、`strict`、`allowed_callers`、`defer_loading` 和 `output_schema` 等字段。
- Responses reference 对 `strict` 的说明与 Function Calling guide 一致：当 schema 兼容时可启用严格参数验证；namespace 内 function tool 若省略 `strict`，Responses 会在兼容时尝试 strict validation，不兼容时回落到 non-strict。
- Remote MCP 工具支持 `allowed_tools`、`require_approval`、`authorization`、`server_url` / `connector_id` 等字段，说明工具权限和审批是 API 层需要表达的边界之一。
- `tool_choice` 可设为 none / auto / required、allowed tools、强制 function / MCP / custom tool，或强制某些 hosted execution tools；它约束候选工具，不证明工具选择质量或业务安全。
- Reference 包含 `context_management`、`truncation`、`text.format` / `json_schema` 和 refusal 等字段，说明上下文管理、结构化输出和拒绝处理都是应用层需要显式处理的边界；`truncation` 默认 disabled，超出上下文会 400，auto 会从对话开头丢弃 items。
- `text.format` 中 `json_schema` 用于 Structured Outputs；`json_object` 是较旧 JSON mode，新模型优先使用 `json_schema`，且 JSON mode 仍需要 system/user message 明确要求 JSON。

## 支撑证据

- `https://developers.openai.com/api/reference/resources/responses` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:13:03 GMT`；`content-type: text/html; charset=utf-8`。
- `https://developers.openai.com/api/reference/resources/responses/index.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 17:53:14 GMT`；`content-type: text/markdown; charset=utf-8`。
- `https://developers.openai.com/api/docs/api-reference/responses` 重定向到 `/api/reference/resources/responses` 并返回 HTTP 200。
- 旧 guide 入口 `https://developers.openai.com/api/docs/guides/responses` 返回 404，不应作为 reference 使用。
- 2026-07-12 抓取 Markdown 成功；页面包含 `input`、`include`、`conversation`、`previous_response_id`、`instructions`、`tools`、function/custom/namespace/tool_search/MCP/hosted execution tools、`tool_choice`、`require_approval`、`strict`、`context_management`、`truncation`、`text.format`、`json_schema`、JSON mode 和 refusal 等字段说明。
- 2026-07-12 已与 Text Generation、Function Calling 和 Structured Outputs 文档交叉验证第 02/03 章上下文工程与工具接口边界，并支撑“LLM 应用输入输出不只是字符串”“长上下文不能替代治理”“schema/tool choice 不是业务安全保证”的窄结论。

## 可能的问题

- API reference 页面较长，初学者不适合从头阅读。
- 需要从章节正文中抽取最小必要概念，而不是堆 API 字段。
- API reference 是接口定义，不等同于完整工程安全指南；权限、审计和人工确认仍需结合生产化章节讨论。
- `include`、`tool_choice`、`allowed_tools`、`require_approval`、`truncation` 和 `json_schema` 是接口控制面，不证明真实模型选择、拒绝、重试、成本、延迟、trace 或生产可靠性已经验证。
- Reference 中出现 shell、local_shell、apply_patch、computer use 等 hosted / execution tools，应在安全章节明确 sandbox、审批、数据保留和 trace 边界，不能简单等同于本地 function calling。

## 初学者阅读建议

- 先读手册中的“模型输入输出”和“工具调用”章节，再把 API reference 当作查询资料。

## 可复现实验

- 已准备三个最小 Responses API harness：tool-calling 参数校验/重试、Structured Outputs / JSON mode 对比、prompt injection / permission。当前无 API key 时，Tool Calling harness 已完成本地 deterministic validation/retry control，Structured Outputs harness 已完成本地 deterministic schema/semantic control，Prompt Injection / Permission harness 已完成本地 deterministic tool-permission control；这些 no-key 分支都显式标记未验证真实模型或真实 API。配置 API key 后可记录输入、输出、工具调用、错误处理、权限策略和 trace。真实 API completed run 仍待跑，不能提前升级结论。

## 是否进入正文

- 结论：进入
- 原因：LLM 基础、工具调用和实践项目都需要当前官方 API reference；可与 Text Generation、Function Calling 和 Structured Outputs 文档共同支撑输入、输出、tool call、refusal、structured output、include、conversation / previous response state、context management、truncation、tool choice 和 permission fields 的结构化接口与上下文治理边界。
