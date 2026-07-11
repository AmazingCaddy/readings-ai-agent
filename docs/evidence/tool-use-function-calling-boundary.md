# Evidence Note: Tool Use 与 Function Calling 边界

## 要验证的结论

Function calling / tool calling 是模型与应用程序协作调用外部工具的 API 机制：模型生成工具调用请求和参数，应用程序负责执行工具并把结果回传；它不等同于模型自己执行函数，也不等同于 Toolformer 论文中的训练方案。

## 资料来源

- Source 1：[OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- Source 2：[OpenAI Responses API Reference](../sources/source-cards/2026-openai-responses-api-docs.md)
- Source 3：[Toolformer: Language Models Can Teach Themselves to Use Tools](../sources/source-cards/2023-toolformer-paper.md)

## 交叉验证结果

- 一致点：OpenAI Function Calling docs 和 Responses API reference 都把工具调用表示为 API 层的结构化交互；工具定义包含名称、类型、参数 schema 和 strict 等字段。
- 一致点：OpenAI Function Calling docs 的五步流程明确包含“应用侧执行代码”和“带工具输出再次请求模型”。这支持“模型不直接执行应用函数”的工程边界。
- 一致点：Toolformer 摘要同样关注何时调用 API、传什么参数、如何利用结果，说明 tool use 是更广的研究主题。
- 分歧点：Toolformer 是训练方法和论文实验，OpenAI Function Calling 是现代 API 机制。两者都涉及工具使用，但抽象层级不同。
- 可能原因：研究论文讨论模型能力形成方式，API 文档讨论应用如何把工具暴露给模型并执行工具调用流程。

## 实验验证

- 是否需要实验：是
- 实验设计：构建一个最小 `get_weather` mock tool，让模型生成工具调用参数；应用层故意返回参数校验错误，再观察模型是否修正参数。记录工具调用、错误回传和最终输出。
- 结果：待执行

## 结论状态

- 部分验证：官方文档直接支撑 API 流程和应用侧执行边界；Toolformer 支撑研究脉络区分。仍缺最小实验结果。

## 可进入章节

- 是，但应保留工程边界说明：Function Calling 是结构化协作接口，不是模型直接执行函数。
