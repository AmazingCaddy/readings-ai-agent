# Evidence Note: MCP Host / Client / Server 职责边界

## 要验证的结论

MCP 是模型应用和外部上下文/工具能力之间的协议层；它定义 host、client、server、tools、resources、prompts 等通信和能力边界，但不是完整 Agent 框架，也不规定 AI 应用如何使用 LLM 或管理上下文。

## 资料来源

- Source 1：[Model Context Protocol Official Documentation](../sources/source-cards/2026-mcp-official-docs.md)
- Source 2：[Model Context Protocol Servers Repository](../sources/source-cards/2026-mcp-servers-repo.md)
- Source 3：[OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- Source 4：[MCP 最小 Trace 实验结果](../experiments/mcp-trace/results-2026-07-11.md)

## 交叉验证结果

- 一致点：MCP 官方 architecture overview 明确把 MCP 定位为 context exchange protocol，并说明它不规定 AI applications 如何使用 LLM 或管理提供的上下文。
- 一致点：官方文档定义 host 是 AI application，client 是连接特定 server 的协议组件，server 是提供上下文的程序。
- 一致点：官方 server concepts 将 tools、resources、prompts 分成不同 primitives；这支持正文中把 MCP 放在工具和上下文生态层，而不是 Agent runtime 层。
- 一致点：servers repository README 明确 reference servers 是教育示例，不是 production-ready solutions；这支持正文中对示例 server 的保守边界。
- 分歧点：OpenAI Function Calling docs 位于模型 API 工具调用层，MCP 位于应用和外部工具/上下文能力连接层。二者可组合，但不是同一抽象。
- 可能原因：Function Calling 解决模型如何表示工具调用，MCP 解决应用如何通过标准协议连接和发现外部能力。

## 实验验证

- 是否需要实验：是
- 实验设计：接入一个只读 MCP server，记录 host 配置、client 连接、server 暴露的 tools/resources，以及一次 `tools/list` 和 `tools/call` trace。
- 结果：已完成标准库模拟实验。脚本复现了 `roots/list`、`tools/list`、`tools/call`、`resources/list`、`resources/read` 和 host approval/review trace。它支持职责边界和 trace 字段设计，但不是完整 MCP SDK 或真实 host 行为验证。

## 结论状态

- 部分验证：官方文档直接支撑职责定义和协议边界；servers README 支撑 reference implementation 边界；标准库模拟实验支撑最小 trace 字段和职责流。仍缺真实 MCP SDK / host trace 实验。

## 可进入章节

- 是。可以写成：MCP 是 context exchange protocol 和工具/资源连接层，不是完整 Agent 框架；host/client/server 职责有官方定义；最小 trace 可记录 actor、method、decision、关键参数摘要和时间戳，但真实 host 行为仍需实测。
