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

MCP spec 把 tools 设计成 model-controlled：模型可以根据上下文自动发现和调用工具。具体协议里，client 通过 `tools/list` 发现工具，通过 `tools/call` 调用工具。每个 tool 至少需要名字、描述和 `inputSchema`，也可以提供 `outputSchema`，帮助 client 和模型理解结构化输出。

工具是风险最高的部分，因为它们可能改变外部世界。因此工具需要 schema、权限、确认和审计。官方 spec 也要求 server 校验工具输入、访问控制、限流和清理输出；client 应在敏感操作前展示工具输入、让用户确认、校验工具结果、设置 timeout，并记录工具使用日志。

### Resources

Resources 是可读取的上下文资料。比如文件、文档、数据库记录、项目元信息。

MCP spec 把 resources 设计成 application-driven：host application 决定如何把资源放进上下文。client 可以通过 `resources/list` 发现资源，通过 `resources/read` 读取资源，也可以使用 resource templates 或订阅资源变化。

Resources 更像“给模型看的资料”，但仍然需要权限控制。因为资料可能包含敏感信息，也可能包含恶意指令。server 必须校验 resource URI，并应在读取敏感资源前检查权限。

### Prompts

Prompts 是 server 提供的提示模板或可复用任务说明。它们可以帮助 host 组织常见任务。

MCP spec 把 prompts 设计成 user-controlled：通常由用户在界面中显式选择，例如 slash command。client 可以通过 `prompts/list` 发现 prompt，通过 `prompts/get` 获取带参数的 prompt 内容。

Prompts 不应该被当成绝对可信的系统规则。它们仍然需要和 host 的上层指令、权限和用户目标配合，也需要校验输入输出，防止注入攻击或未授权资源访问。

## 授权、Roots、Elicitation、Sampling

MCP 不只定义 server 暴露的 tools、resources、prompts，也定义一些 client 侧和传输层能力。初学者最容易误解的是：这些能力提供协议结构，但不等于自动完成安全设计。

### Authorization

MCP authorization spec 处理 transport-level 授权。它明确说明 authorization 对 MCP implementations 是 optional。使用 HTTP-based transport 且支持授权时，应遵循 MCP authorization spec；使用 STDIO transport 时，不应走这套 OAuth flow，而应从环境中取得凭据。

在 HTTP 授权模型里，protected MCP server 是 OAuth resource server，MCP client 是 OAuth client。client 需要用 `Authorization: Bearer <access-token>` 发送 token，不能把 access token 放在 URL query string 中。server 必须验证 token 是签发给自己的 audience/resource，不能接受或透传其他服务的 token。

因此，不能把“用了 MCP”理解成“已经自动安全”。你仍然要问：当前 transport 是什么？有没有授权？token 的 audience 是否校验？scope 是否最小？错误时是 401、403 还是静默失败？

### Roots

Roots 让 client 告诉 server：当前有哪些 filesystem roots 可见，例如一个项目目录或多个仓库目录。server 可以请求 `roots/list`，client 也可以在 roots 变化时发通知。

Roots 不是万能 sandbox。官方 spec 要求 client 只暴露有适当权限的 roots、校验 root URI、防止 path traversal，并实现 access control；server 应尊重 root boundaries。真正的隔离仍需要 host、操作系统、容器或 sandbox 策略配合。

### Elicitation

Elicitation 允许 server 通过 client 请求用户补充信息。Form mode 适合普通结构化信息；URL mode 适合敏感交互，例如第三方授权或支付流程。

官方 spec 明确要求 server 不得用 form mode 请求密码、API keys、access tokens 或 payment credentials。client 需要清楚展示哪个 server 在请求信息，并提供 decline 和 cancel 选项。URL mode 也不能自动打开 URL，必须让用户看见完整 URL 并明确同意。

### Sampling

Sampling 允许 server 通过 client 请求 LLM generation。这样 server 可以在没有模型 API key 的情况下使用 client 侧模型能力，但 client 仍控制模型访问、模型选择和权限。

官方 spec 建议 sampling requests 应保留 human-in-the-loop，让用户能拒绝、查看和修改 prompt，并在结果返回 server 前复核。支持 tool-enabled sampling 时，client 必须显式声明 capability，server 不能把带工具的 sampling request 发给不支持的 client。

## 安全边界

MCP 官方 Security Best Practices 明确列出多类实现风险：confused deputy、token passthrough、SSRF、session hijacking、本地 MCP server compromise、authorization URL validation、stdio proxy escalation 和 scope minimization。

对初学者来说，可以先记住四条。

1. 不要透传 token。MCP server 不应接受或转发不是签发给自己的 token；访问上游 API 时，应使用单独的上游授权。
2. 不要无条件相信 URL。OAuth discovery、authorization URL 和 URL mode elicitation 都可能引入 SSRF、恶意 scheme、redirect 或 phishing 风险。
3. 不要把本地 server 当成普通配置。本地 MCP server 往往是用户机器上运行的进程，可能有文件系统和网络权限，安装或一键配置前必须显示将执行的命令并取得明确同意。
4. 不要一次暴露所有权限。scope、tools、resources 和 roots 都应最小化；敏感操作应采用 step-up authorization、确认和审计。

对于 remote MCP tools，也应优先使用 allowlist 或 denylist 控制暴露面。第三方 remote MCP servers 不应被默认信任；接入前要审查其安全实践、授权范围和数据保留条款。

## MCP 和 Function Calling 的关系

Function Calling 关注模型如何按 schema 生成工具调用请求。MCP 关注模型应用如何以统一协议连接外部工具和上下文能力。

可以这样理解：

- Function Calling 是模型 API 层的结构化调用机制。
- MCP 是应用和工具生态之间的连接协议。
- Agent Framework 负责更大的任务循环、状态和编排。

它们可以组合在一起：Agent 框架决定下一步要用工具，模型通过 tool calling 生成调用意图，MCP server 提供具体工具能力。

## MCP 和具体产品集成

理解 MCP 时，要区分两层资料。

第一层是 MCP 官方 specification：它定义 host、client、server、tools、resources、prompts、authorization、roots、elicitation、sampling 等协议边界。

第二层是具体产品如何接入 MCP。比如 Anthropic 的 MCP connector 允许开发者通过 Messages API 连接 remote MCP servers，并把这些 server 的 tools 作为可调用工具暴露给 Claude。这个 connector 支持 `mcp_servers`、`mcp_toolset`、OAuth bearer token、allowlist、denylist 和 per-tool configuration。

这个能力很有用，但边界也要看清楚：Anthropic 文档说明 MCP connector 当前只支持 MCP tool calls，不等于支持全部 MCP capabilities。Local STDIO servers 也不能直接连接到这个 connector；如果需要 local servers、MCP prompts、MCP resources 或更细控制，应使用 SDK helper 或自建 MCP client。

Anthropic 还提供 MCP tunnels 文档，用来把私有网络内的 MCP servers 连接给 Claude，而不需要打开 inbound firewall ports 或把服务暴露到公网。Tunnels 使用 outbound-only connection、proxy、inner TLS 和 shared responsibility model。但 tunnels 仍处于 research preview，不能写成生产可靠性保证；上游 MCP server 仍需要 OAuth、最小 scope、网络限制、日志监控、凭据轮换和审计。

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

对于 remote server，scope 也应尽量细。官方安全最佳实践建议用较小的初始 scope，在真正需要高风险能力时再通过 scope challenge 或 step-up authorization 提权。

### 明确工具说明

工具名称和描述应该具体。模糊工具会让模型更难选择，也更难审计。例如 `run_command` 比 `list_project_files` 风险高得多。

### 记录调用轨迹

记录哪个 server、哪个 tool、什么参数、什么结果、是否需要确认。没有这些记录，很难分析 Agent 失败原因。

审计记录还应覆盖授权升级、用户拒绝、URL mode elicitation、roots 变化、tool execution errors 和超时。记录时要避免把 access token、API key、密码或敏感 resource 原文写进日志。

本手册的 MCP 最小 trace 模拟实验记录了 `actor`、`method`、`decision`、关键参数摘要和时间戳。实验中，host 批准了只读工具、拒绝了模拟写工具，并把恶意 resource 标记为 prompt injection 候选。

后续的 stdio JSON-RPC harness 又把这个流程放进独立 server 进程和真实 stdin/stdout 消息里，覆盖 `initialize`、`tools/list`、`tools/call`、`resources/list` 和 `resources/read`。它比内存模拟更接近协议通信，但仍是手写 JSON-RPC harness。

Real MCP SDK Trace 再用官方 MCP Python SDK 和 `FastMCP` stdio server 复现同类流程：SDK `ClientSession` 完成 `initialize`、`tools/list`、只读 `tools/call`、`resources/list`、`resources/read`、`prompts/list` 和 `prompts/get`；host policy 在写工具 `write_release_note` 前拒绝并记录 `rejected_write_tool_forwarded=false`，恶意 resource 被标记为 `untrusted_prompt_injection_candidate`，trace 未泄露示例 secret。这个结果验证了官方 SDK 的本地 tools/resources/prompts 流程，但仍不能替代真实 host UI、OAuth、URL mode、sampling、tunnel 或跨 host 行为测试。

### 把 server 示例当示例，不当生产方案

MCP servers repo 可以帮助理解实现方式，但示例 server 不等同于生产级安全设计。生产系统需要更严格的鉴权、隔离和审计。

## 常见误区

- 误区一：MCP 是 Agent 框架。MCP 是协议，不是完整 Agent 架构。
- 误区二：接入 MCP 后模型就安全地拥有工具。安全取决于 host/client/server 的权限和策略设计。
- 误区三：MCP server 暴露得越多越好。能力越多，攻击面和误用风险越大。
- 误区四：Resources 都是安全资料。资源内容可能敏感、过时或包含恶意指令。
- 误区五：示例 server 可以直接用于生产。示例主要用于学习和原型。
- 误区六：Roots 等于 sandbox。Roots 是协议层的可见范围和协作机制，不替代 OS 或容器级隔离。
- 误区七：Authorization 等于所有 MCP 都有 OAuth。Authorization 是 optional，并且 transport 不同，凭据处理方式也不同。

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
- MCP 官方 server concepts 和 2025-11-25 specification 将 tools、resources、prompts 区分为不同 interaction model：tools 是 model-controlled，resources 是 application-driven，prompts 是 user-controlled。
- MCP authorization spec 说明 authorization 是 optional transport-level capability；HTTP-based transport 支持授权时应遵循 MCP authorization spec，STDIO transport 不应走这套 OAuth flow。
- MCP authorization spec 和 Security Best Practices 明确禁止 token passthrough，并要求 server 验证 token audience/resource。
- MCP roots、elicitation 和 sampling spec 支撑了 roots 可见范围、敏感信息交互、server-requested LLM generation 和 human-in-the-loop 的协议边界。
- Anthropic MCP connector / tunnels 文档支撑具体产品集成边界：Messages API 可连接 remote MCP tools，并支持 allowlist、denylist、OAuth bearer token 和 per-tool configuration；connector 当前只支持 MCP tool calls，不支持全部 MCP capabilities；MCP tunnels 可减少私有网络 MCP server 的公网暴露需求，但仍需要 OAuth、最小 scope、allowed IPs、凭据保护、日志和 shared responsibility。
- 本地标准库模拟实验复现了 `roots/list`、`tools/list`、`tools/call`、`resources/list`、`resources/read` 和 host approval/review trace，支撑最小审计字段和职责流设计。
- 本地 stdio JSON-RPC harness 启动独立 server 进程，通过 stdin/stdout 复现 `initialize`、`tools/list`、`tools/call`、`resources/list` 和 `resources/read`，并验证 host approval、resource review 和 trace 脱敏字段设计；它仍不是官方 SDK 或真实 host 行为验证。
- Real MCP SDK Trace 使用官方 MCP Python SDK / FastMCP stdio server 完成 `initialize`、`tools/list`、`tools/call`、`resources/list`、`resources/read`、`prompts/list` 和 `prompts/get`，记录 2 tools、2 resources、1 prompt、12 个 trace 事件、写工具未转发、恶意 resource review 和 `leaked_secret_in_trace=false`；它仍只是本地 toy server 和脚本化 host policy，不是真实 host UI 或 OAuth / URL mode / sampling 验证。
- MCP servers repo README 明确 reference servers 是教育示例，不是 production-ready solutions。
- “MCP 是连接工具和上下文能力的协议，不是 Agent 框架本身”是本章可入正文的职责边界；MCP 可以暴露 tools、resources 和 prompts，但不会替代 Agent 的规划、状态管理、权限策略、评测和生产治理。
- “MCP 是协议层，不是完整 Agent 框架”是可入正文的职责边界；“MCP 不自动完成安全边界”也已升级为可入正文：authorization 是 optional，roots 不等于 sandbox，token passthrough 被禁止，高风险 tools/resources/prompts 仍需要最小权限、用户确认、输入输出校验、audience 校验、sandbox/隔离、审计和 trace 脱敏。本地 JSON-RPC 和官方 Python SDK harness 已覆盖最小进程 / SDK 流程；真实 host UI、权限确认、URL mode / OAuth、sampling、tunnel 和恶意 resource/prompt 呈现仍需实验。

## 待验证问题

- 如何用真实 MCP host UI 复现一次 `tools/list`、`tools/call`、`resources/list`、`resources/read`、`prompts/list`、`prompts/get` 和 trace？本地 stdio JSON-RPC harness 已覆盖最小进程消息流，官方 MCP Python SDK harness 已覆盖 SDK flow，仍需真实 host UI 对照。
- 不同 host 对 tool confirmation、roots、elicitation、sampling 和 audit log 的实现差异有多大？
- 如何把当前模拟和 stdio harness 中的恶意 resource/prompt 扩展到真实 host，验证 host 是否会把外部内容当成不可信上下文？
- 如何用真实 Anthropic Messages API MCP connector 复现 `mcp_tool_use` / `mcp_tool_result`、allowlist/denylist、OAuth token、未知工具、错误结果和敏感 trace 脱敏？
- MCP tunnels 的 outbound-only 连接、`upstream.allowed_ips`、OAuth、token/cert rotation 和 breach teardown 在真实部署中如何表现？
- 哪些 MCP server 示例最适合初学者阅读？
- MCP 如何和 OpenAI Agents SDK、LangGraph 等框架组合？

## 本章小结

- MCP 是连接模型应用、工具和上下文资源的协议。
- Host、client、server 分别处在用户应用、连接组件和能力提供者的位置。
- Tools、resources、prompts 解决的问题不同，风险也不同。
- Authorization、roots、elicitation 和 sampling 提供协议能力，但不替代应用层权限、sandbox 和审计。
- MCP 可以和 Function Calling、Agent Framework 组合，但不是它们的替代品。
- 使用 MCP 时，最小权限、确认机制和审计记录比“接入更多工具”更重要。

## References

### Official Docs

- [Model Context Protocol Official Documentation](../sources/source-cards/2026-mcp-official-docs.md)
- [Anthropic MCP Connector and Tunnels Documentation](../sources/source-cards/2026-anthropic-mcp-docs.md)

### Source Code / Examples

- [Model Context Protocol Servers Repository](../sources/source-cards/2026-mcp-servers-repo.md)

### Related

- [OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- [OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)

### Governance

- [术语边界表](../glossary.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [References 覆盖矩阵](../references/coverage-matrix.md)
- [Evidence Note: MCP Host / Client / Server 职责边界](../evidence/mcp-role-boundary.md)
- [Evidence Note: MCP 安全、授权与权限边界](../evidence/mcp-security-permission-boundary.md)
- [MCP 最小 Trace 实验结果](../experiments/mcp-trace/results-2026-07-11.md)
- [Real MCP Stdio Trace 实验](../experiments/real-mcp-stdio-trace/README.md)
- [Real MCP Stdio Trace 结果](../experiments/real-mcp-stdio-trace/results-2026-07-11.md)
