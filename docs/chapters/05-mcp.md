# MCP 与工具生态

## 本章适合谁

如果你已经理解 Tool Use 和 Function Calling，但还不清楚 MCP 是什么、它和普通 API wrapper 有什么区别、MCP server/client/host 分别负责什么，这一章适合阅读。

本章不会把 MCP 当成神秘的 Agent 框架。我们会把它放回工具生态的位置：它是一种连接模型应用、工具和上下文资源的协议。

## 你会学到什么

- MCP 要解决什么问题。
- MCP host、client、server 的基本边界。
- tools、resources、prompts 的区别。
- MCP 和 Function Calling、Agent Framework 的关系。
- 使用 MCP 时需要关注哪些权限和安全问题。

## 先用一句话理解

MCP 是让模型应用以统一方式发现和使用外部工具、资源和提示的协议；它不是 Agent 本身，也不自动解决权限和安全问题。

## 基础概念

### 为什么需要 MCP

没有统一协议时，每个模型应用都要为每个外部系统写一套连接方式。比如文件系统、GitHub、数据库、日历、Slack、搜索服务，都可能有不同 API、鉴权和数据格式。

MCP 的价值在于提供统一的连接抽象，让工具和上下文能力可以通过 server 暴露给模型应用。这样模型应用不必把所有集成逻辑都写死在自己内部。

### Host

MCP 官方文档把 host 定义为协调和管理一个或多个 MCP clients 的 AI application，例如 IDE、桌面助手、聊天应用或 Agent runtime。它负责把用户、模型和 MCP client 组织起来。

对初学者来说，可以把 host 理解为“用户实际使用的模型应用”。

### Client

Client 是 host 里负责连接特定 MCP server 的协议组件。官方文档说明 host 通常会为每个 MCP server 创建一个 MCP client，每个 client 维护到对应 server 的 dedicated connection。

Client 通常负责建立连接、发现能力、转发请求和接收结果。

### Server

Server 是向 MCP clients 提供上下文和能力的程序。它可以提供 tools、resources、prompts 等能力。例如：读取文件、查询数据库、列出 issue、访问文档、提供模板 prompt。

Server 暴露能力不代表模型可以不受限制地使用这些能力。是否允许调用、是否需要确认、结果如何展示，仍取决于 host/client 和整体权限策略。

## Tools、Resources、Prompts

### Tools

Tools 是可执行能力。比如搜索、创建 issue、读取文件、查询数据库。工具可能只读，也可能有副作用。

工具是风险最高的部分，因为它们可能改变外部世界。因此工具需要 schema、权限、确认和审计。

### Resources

Resources 是可读取的上下文资料。比如文件、文档、数据库记录、项目元信息。

Resources 更像“给模型看的资料”，但仍然需要权限控制。因为资料可能包含敏感信息，也可能包含恶意指令。

### Prompts

Prompts 是 server 提供的提示模板或可复用任务说明。它们可以帮助 host 组织常见任务。

Prompts 不应该被当成绝对可信的系统规则。它们仍然需要和 host 的上层指令、权限和用户目标配合。

## MCP 和 Function Calling 的关系

Function Calling 关注模型如何按 schema 生成工具调用请求。MCP 关注模型应用如何以统一协议连接外部工具和上下文能力。

可以这样理解：

- Function Calling 是模型 API 层的结构化调用机制。
- MCP 是应用和工具生态之间的连接协议。
- Agent Framework 负责更大的任务循环、状态和编排。

它们可以组合在一起：Agent 框架决定下一步要用工具，模型通过 tool calling 生成调用意图，MCP server 提供具体工具能力。

## 通俗例子

假设你在 IDE 里让 Agent “找出当前项目里某个测试为什么失败”。

Host 是 IDE 或 Agent 应用。

Client 是 host 中连接外部能力的组件。

MCP servers 可能包括：

- 文件系统 server：读取项目文件。
- Git server：查看 diff 和提交历史。
- 测试 server：运行或查询测试结果。
- 文档 server：读取项目内部说明。

模型不会直接拥有这些系统权限。它通过 host 和 client 发起工具请求，server 执行能力，host 决定是否允许、如何展示结果、是否需要用户确认。

## 工作原理

一个简化的 MCP 使用流程如下。

1. Host 启动并连接一个或多个 MCP servers。
2. Client 发现 server 暴露的 tools、resources、prompts。
3. Host 把可用能力整理给模型或 Agent runtime。
4. 模型根据任务提出使用某个工具或资源的请求。
5. Host/client 根据权限策略决定是否执行。
6. Server 执行请求并返回结果。
7. Host 把结果作为上下文交给模型继续处理。

这个流程里，权限边界非常重要。MCP 让能力更容易接入，也意味着错误暴露的能力更容易被误用。

## 工程实践

### 先接只读 server

初学者项目应优先接只读能力，例如读文档、查 issue、列文件。写操作、删除操作、发送消息、部署操作应放到后面，并要求确认。

### 最小权限原则

MCP server 不应该暴露超出任务需要的能力。比如只需要读 docs，就不要暴露整个 home 目录；只需要查 issue，就不要暴露写权限。

### 明确工具说明

工具名称和描述应该具体。模糊工具会让模型更难选择，也更难审计。例如 `run_command` 比 `list_project_files` 风险高得多。

### 记录调用轨迹

记录哪个 server、哪个 tool、什么参数、什么结果、是否需要确认。没有这些记录，很难分析 Agent 失败原因。

### 把 server 示例当示例，不当生产方案

MCP servers repo 可以帮助理解实现方式，但示例 server 不等同于生产级安全设计。生产系统需要更严格的鉴权、隔离和审计。

## 常见误区

- 误区一：MCP 是 Agent 框架。MCP 是协议，不是完整 Agent 架构。
- 误区二：接入 MCP 后模型就安全地拥有工具。安全取决于 host/client/server 的权限和策略设计。
- 误区三：MCP server 暴露得越多越好。能力越多，攻击面和误用风险越大。
- 误区四：Resources 都是安全资料。资源内容可能敏感、过时或包含恶意指令。
- 误区五：示例 server 可以直接用于生产。示例主要用于学习和原型。

## 什么时候不该用 MCP

以下场景可以先不引入 MCP：

- 只有一个简单内部 API，直接调用更清晰。
- 团队还没有权限边界和审计需求。
- 工具只在单一应用里使用，没有复用需求。
- 你还没有弄清楚 host、client、server 的职责。

MCP 更适合工具和数据源较多、希望跨模型应用复用、需要标准化暴露上下文能力的场景。

## 已验证结论

- MCP 官方 architecture overview 明确说明 MCP 只关注 context exchange protocol，不规定 AI applications 如何使用 LLM 或管理提供的上下文。
- MCP 官方文档定义了 host、client、server 的职责：host 是 AI application，client 维护到 server 的连接并获取上下文，server 向 clients 提供上下文。
- MCP 官方 server concepts 将 tools、resources、prompts 区分为 server 暴露的三类核心 building blocks。
- MCP servers repo README 明确 reference servers 是教育示例，不是 production-ready solutions。
- “MCP 不是 Agent 框架本身”已完成第一轮官方文档交叉验证，但仍建议补一个最小 MCP trace 实验。

## 待验证问题

- MCP specification 对 host、client、server、tools、resources、prompts 的字段级定义有哪些容易误解的细节？
- MCP 对权限、安全、roots、sampling 和用户确认有哪些官方建议？
- 如何用只读 server 复现一次 `tools/list`、`tools/call` 和 trace？
- 哪些 MCP server 示例最适合初学者阅读？
- MCP 如何和 OpenAI Agents SDK、LangGraph 等框架组合？

## 本章小结

- MCP 是连接模型应用、工具和上下文资源的协议。
- Host、client、server 分别处在用户应用、连接组件和能力提供者的位置。
- Tools、resources、prompts 解决的问题不同，风险也不同。
- MCP 可以和 Function Calling、Agent Framework 组合，但不是它们的替代品。
- 使用 MCP 时，最小权限、确认机制和审计记录比“接入更多工具”更重要。

## References

### Official Docs

- [Model Context Protocol Official Documentation](../sources/source-cards/2026-mcp-official-docs.md)

### Source Code / Examples

- [Model Context Protocol Servers Repository](../sources/source-cards/2026-mcp-servers-repo.md)

### Related

- [OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- [OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)

### Governance

- [术语边界表](../glossary.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [Evidence Note: MCP Host / Client / Server 职责边界](../evidence/mcp-role-boundary.md)
