# Evidence Note: Tool Use 与 Function Calling 边界

## 要验证的结论

Function calling / tool calling 是模型与应用程序协作调用外部工具的 API 机制：模型生成工具调用请求和参数，应用程序负责执行工具并把结果回传；它不等同于模型自己执行函数，也不等同于 Toolformer 论文中的训练方案。

## 资料来源

- Source 1：[OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- Source 2：[OpenAI Responses API Reference](../sources/source-cards/2026-openai-responses-api-docs.md)
- Source 3：[Toolformer: Language Models Can Teach Themselves to Use Tools](../sources/source-cards/2023-toolformer-paper.md)
- Source 4：[Tool Calling 参数校验与重试实验结果](../experiments/tool-calling-validation/results-2026-07-11.md)
- Source 5：[Evidence Note: Tool / Function / Plugin 术语对照边界](tool-terminology-crosswalk.md)

## 交叉验证结果

- 一致点：OpenAI Function Calling docs 和 Responses API reference 都把工具调用表示为 API 层的结构化交互；工具定义包含名称、类型、参数 schema 和 strict 等字段。
- 一致点：OpenAI Function Calling docs 的五步流程明确包含“应用侧执行代码”和“带工具输出再次请求模型”。这支持“模型不直接执行应用函数”的工程边界。
- 一致点：Toolformer 摘要同样关注何时调用 API、传什么参数、如何利用结果，说明 tool use 是更广的研究主题。
- 分歧点：Toolformer 是训练方法和论文实验，OpenAI Function Calling 是现代 API 机制。两者都涉及工具使用，但抽象层级不同。
- 可能原因：研究论文讨论模型能力形成方式，API 文档讨论应用如何把工具暴露给模型并执行工具调用流程。
- 本地实验：标准库模拟实验使用 fake model 生成一次错误参数 `unit=kelvin`，应用层返回可操作校验错误，fake model 第二轮改为 `unit=celsius`，应用层执行工具并记录 trace。这支持“参数校验、错误回传和有限重试是应用控制循环的一部分”的工程边界。
- 术语对照：跨框架文档交叉验证显示，OpenAI API 的 function/tool calling、OpenAI Agents SDK 的 runtime tools / agent-as-tool、Semantic Kernel 的 plugins/functions、LlamaIndex 的 retriever/query engine、LangGraph 的 state graph、AutoGen/CrewAI 的 multi-agent / Flow 抽象处在不同层级。它们都可围绕外部能力组织 Agent 系统，但不能直接当成同义词。

## 实验验证

- 是否需要实验：是
- 实验设计：构建一个最小 `get_weather` mock tool，让模型生成工具调用参数；应用层故意返回参数校验错误，再观察模型是否修正参数。记录工具调用、错误回传和最终输出。
- 结果：已完成标准库模拟实验。trace 包含 `tool_call_requested`、`tool_validation_failed`、第二次 `tool_call_requested`、`tool_executed` 和 `final_response`。实验未调用真实模型或真实 Function Calling API，因此不能证明真实模型稳定修正参数。

## 结论状态

- 可入正文：窄结论“Tool use 可以让模型通过应用或运行时连接外部 API、搜索、计算器、日历、数据库等工具能力”已完成第一轮交叉验证。Toolformer 摘要支撑 calculator、QA system、search engines、translation system 和 calendar 等工具使用研究方向；OpenAI Function Calling / Responses API 文档支撑现代 API 通过工具定义、参数 schema、工具调用请求和工具结果回传来组织这类能力。
- 可入正文：窄结论“Function Calling / Tool Calling 本身不执行工具；工具执行发生在应用程序或工具运行时，并由应用侧把结果回传模型”由 OpenAI 官方文档直接支撑，并被 Responses API source card 和本地参数校验实验交叉支撑。
- 可入正文：窄结论“不同框架的 tool / function / plugin / retriever / flow 等术语不能直接互换；学习时应优先比较执行边界、状态边界、权限边界和 trace 边界”已完成第一轮文档交叉验证。
- 部分验证：Toolformer 的训练式 tool use 效果、现代 API tool-calling 的真实模型稳定性、参数校验失败后真实模型能否稳定修正、真实框架默认错误恢复、权限覆盖、trace 字段和成本表现仍待验证。

## 可进入章节

- 是。可以确定写成：Tool use 是让模型通过系统暴露的工具能力连接外部 API、搜索、计算器等能力；Function Calling 是现代 API 中组织工具调用的结构化协作接口，不是模型直接执行函数。参数校验和重试逻辑应由应用层显式设计。
