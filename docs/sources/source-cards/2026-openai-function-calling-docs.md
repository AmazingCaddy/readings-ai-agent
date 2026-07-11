# OpenAI Function Calling / Tool Calling Documentation

- 来源链接：https://developers.openai.com/api/docs/guides/function-calling
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；Markdown 页面 last-modified 复核为 2026-07-11 06:28:07 GMT
- 最后复核日期：2026-07-12
- 类型：官方文档
- 主题：Tool Use / Function Calling / Structured Output
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：HTML 与 Markdown 来源链接均于 2026-07-12 返回 HTTP 200；关键段落已复核；“Function Calling 本身不执行工具”边界已可入正文；参数校验/重试标准库模拟实验和跨框架术语对照第一轮已完成；Real Tool Calling harness 已准备并接入统一 runner，当前无 API key 时完成本地 deterministic validation/retry control，并标记 `real_api_validated=false`

## 一句话总结

这是解释现代 OpenAI API 中工具调用和函数调用机制的首选官方 reference。

## 核心结论

- 官方文档将 function calling 也称为 tool calling，用于让 OpenAI 模型连接外部系统，并访问训练数据之外的数据和应用提供的动作。
- 文档把 `function` / `tool` 定义为开发者告诉模型可访问的一项功能；模型可能在生成响应时决定需要使用该工具。
- 文档把 `function call` / `tool call` 定义为模型返回的一类特殊响应，表示模型请求使用某个可用工具。
- 文档把 `function call output` / `tool call output` 定义为应用侧工具根据模型工具调用输入生成的结果，并指出该结果需要引用具体 `call_id`。
- 官方工具调用流程包括：请求模型并提供可调用工具、接收模型工具调用、在应用侧执行代码、带工具输出再次请求模型、接收最终响应或更多工具调用。
- 文档明确 function 是 tool 的一种，通常由 JSON schema 定义；除 function tools 外，还有 custom tools 和 OpenAI 平台内置 tools。
- 文档说明 reasoning models 返回的 reasoning items 如果和 tool calls 一起出现，也必须随 tool call outputs 一起回传。
- 文档新增或明确 namespace / `tool_search` 边界：可用 namespace 按 domain 分组工具；工具面较大时可用 `tool_search` 延迟加载少用工具，但当前只有 `gpt-5.4` 及之后模型支持。
- 文档说明 function definitions 会注入 system message，计入 context limit 并按 input tokens 计费；工具多或 schema 大时应减少初始工具、缩短描述或使用 tool search，而不是无限暴露工具面。
- 文档说明 `tool_choice` 可以设为 auto、required、forced function、allowed tools 或 none；allowed tools 可在不改完整工具列表的情况下限制当前请求可调用子集。
- 文档说明 parallel function calling 不适用于 built-in tools；模型可能单轮调用多个函数，可用 `parallel_tool_calls=false` 限制为零或一个。
- 文档建议启用 strict mode，并说明 strict mode 会让 function calls 更可靠地遵循 schema，而不是 best effort；同时说明 Responses API 会在可行时尝试把 schema 规范化为 strict mode，无法兼容时回落到 `strict: false`，Chat Completions 默认仍是非 strict。
- 文档说明 custom tools 可以使用自由文本输入输出，也可用 Lark 或 regex CFG 约束输入；这些 grammar 能力有受支持语法和复杂度限制，不能当作语义正确性保证。

## 支撑证据

- 旧入口 `https://platform.openai.com/docs/guides/function-calling` 会 301 到 `https://developers.openai.com/api/docs/guides/function-calling`。
- `https://developers.openai.com/api/docs/guides/function-calling` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:08:21 GMT`；`content-type: text/html; charset=utf-8`。
- `https://developers.openai.com/api/docs/guides/function-calling.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:28:07 GMT`；`content-type: text/markdown; charset=utf-8`。
- 2026-07-12 抓取 Markdown 成功；页面包含 “Function calling (also known as tool calling)”、“The tool calling flow has five high level steps”、namespace、tool search、token usage、tool choice、parallel function calling、strict mode default differences、streaming function-call events 和 custom tools / CFG 等关键段落。

## 可能的问题

- 官方 API 文档更新频繁，需要记录复核日期。
- 需要和 OpenAI Agents SDK 文档区分：这是 API 层 tool calling，不是完整 Agent SDK 抽象。
- `tool_search`、custom tools、strict mode、parallel tool calls、allowed tools 和 grammar 等能力与模型和 API 版本有关，正文不应脱离文档版本泛化。
- strict mode、schema、grammar 和 tool choice 只能约束接口形态或可选工具范围，不证明业务权限、事实正确、工具结果可信、参数语义正确或真实模型会稳定修正错误。
- 大量工具或大型 schema 会带来 token、上下文和路由准确率成本；正文不应写成“工具越多越强”。

## 初学者阅读建议

- 先理解 tool schema、参数生成、工具结果回传，再看 SDK 框架封装。

## 可复现实验

- 已完成一个参数校验失败的标准库模拟实验：fake model 第一轮生成错误参数，应用层返回可操作错误，第二轮修正后执行工具。该实验支撑应用层校验/错误回传/有限重试流程，但不证明真实模型稳定修正参数。
- 已完成跨框架术语对照 evidence：OpenAI API 的 function/tool calling、OpenAI Agents SDK 的 runtime tools / agent-as-tool、Semantic Kernel plugins/functions、LlamaIndex retriever/query engine、LangGraph state graph、AutoGen/CrewAI multi-agent / Flow 抽象不能直接互换；应按执行、状态、权限和 trace 边界比较。该对照不证明真实框架默认行为。
- 已准备 [Real Tool Calling 参数校验与重试实验](../../experiments/real-tool-calling-validation/README.md) harness：无 API key 时运行本地 deterministic validation/retry control，覆盖 schema-valid 但业务非法参数、validation error、corrected tool call 和 toy tool execution；配置后可记录真实 tool call、validation error、tool result、最终响应、成本/延迟相关字段。当前尚未产生真实 API completed run，不能提前升级真实模型结论。

## 是否进入正文

- 结论：进入；窄边界可入正文
- 原因：Tool Use / Function Calling 章节需要官方 API reference；官方五步流程直接支撑“模型生成工具调用请求，应用侧执行工具并回传结果”。跨框架术语对照已补第一轮文档交叉验证；标准库模拟和本地 validation/retry control 支撑应用层校验、错误反馈和有限重试的固定样例边界。真实模型参数修正稳定性和跨框架默认行为仍需实测。
