# Model Context Protocol Official Documentation

- 来源链接：https://modelcontextprotocol.io/
- 作者 / 机构：Model Context Protocol project
- 发布时间：协议版本使用 `YYYY-MM-DD` 标识；当前协议版本为 `2025-11-25`，表示最近一次向后不兼容变更日期；顶层文档持续更新
- 最后复核日期：2026-07-12
- 类型：官方文档 / 协议文档
- 主题：MCP / Tools / Resources / Prompts
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接已复核；2026-07-12 重新抓取 versioning、architecture、server concepts、client concepts、2025-11-25 spec tools/resources/prompts/authorization/roots/sampling/elicitation/tasks/changelog 和 security best practices 关键 Markdown 页面；host/client/server 职责边界、版本语义和安全/授权窄边界已可入正文；MCP 最小 trace 标准库模拟、本地 stdio JSON-RPC harness 和官方 MCP Python SDK / FastMCP stdio harness 已完成；真实 host UI、OAuth、URL mode、sampling、tasks、tunnel 和跨 host 行为仍部分验证

## 一句话总结

MCP 官方文档和最新 specification 是解释 MCP 组件、能力边界、安全建议、授权流程和工具生态的首选 reference。

## 核心结论

- MCP 官方 architecture overview 将 MCP 定位为 context exchange 协议；文档明确说明 MCP focuses solely on the protocol for context exchange，不规定 AI applications 如何使用 LLM 或管理提供的上下文。
- MCP 官方 versioning 文档说明协议版本使用 `YYYY-MM-DD` 字符串，表示最近一次向后不兼容变更日期；当前协议版本为 `2025-11-25`，并且向后兼容更新不会递增协议版本。
- MCP follows a client-server architecture：MCP host 是协调和管理一个或多个 MCP clients 的 AI application；MCP client 是维护到 MCP server 连接并获取上下文的组件；MCP server 是向 MCP clients 提供上下文的程序。
- 官方文档说明 host 会为每个 MCP server 创建一个 MCP client，每个 client 维护到对应 server 的 dedicated connection。
- MCP data layer 包括 lifecycle management、server features、client features 和 utility features；server features 包括 tools、resources、prompts。
- 官方 server concepts 将 tools、resources、prompts 区分为三类 building blocks：tools 是模型可主动调用的函数，resources 是应用可读取的只读上下文数据源，prompts 是用户显式调用的可复用指令模板。
- 官方 client concepts 说明 sampling 可让 servers 通过 client 请求 LLM completions，并强调这种方式让 client 控制用户权限和安全措施。
- 2025-11-25 specification 的 tools 页面说明 tools 是 model-controlled，工具可通过 `tools/list` 发现、通过 `tools/call` 调用，并要求 server 校验输入、访问控制、限流和输出清理；client 应对敏感操作做用户确认、展示工具输入、校验结果、设置超时并记录审计日志。
- 2025-11-25 specification 的 resources 页面说明 resources 是 application-driven，可通过 `resources/list` / `resources/read` / templates / subscriptions 暴露上下文；server 必须校验 resource URI，并应对敏感资源做访问控制和权限检查。
- 2025-11-25 specification 的 prompts 页面说明 prompts 是 user-controlled，通常由用户显式选择；实现必须校验 prompt 输入输出，防止注入攻击或未授权资源访问。
- 2025-11-25 authorization spec 说明 authorization 对 MCP implementations 是 optional；HTTP-based transport 支持 authorization 时应遵循该规范，STDIO transport 不应使用该 OAuth flow，而应从环境取得凭据。
- 2025-11-25 authorization spec 将 protected MCP server 定义为 OAuth 2.1 resource server，MCP client 定义为 OAuth 2.1 client，并要求 HTTP 请求使用 bearer token、每个请求携带 authorization header、不得把 access token 放在 URI query string 中。
- 2025-11-25 authorization spec 和 security best practices 明确要求 token audience/resource binding：MCP server 必须验证 token 是签发给自己的，并且不得接受或透传其他 token；token passthrough 被列为 forbidden anti-pattern。
- Security Best Practices 文档列出 confused deputy、SSRF、session hijacking、local MCP server compromise、authorization URL validation、stdio proxy escalation、scope minimization 等风险，并给出 per-client consent、redirect URI validation、state validation、HTTPS、私有 IP 阻断、sandbox、scope 最小化等缓解建议。
- Roots spec 说明 roots 是 client 暴露 filesystem roots 的标准方式，client 必须只暴露有适当权限的 roots、校验 URI、防 path traversal、做 access control；server 应尊重 root boundaries。正文应避免把 roots 写成自动强制 sandbox。
- Elicitation spec 说明 server 可以通过 client 请求用户补充信息；form mode 不得请求密码、API keys、access tokens、payment credentials 等敏感信息，敏感交互必须使用 URL mode；client 必须清楚展示哪个 server 在请求信息，并提供 decline/cancel 选项。
- Sampling spec 说明 server 可通过 client 请求 LLM sampling；client 保持模型访问、选择和权限控制，并建议 sampling requests 始终有人可拒绝。支持 tools 的 sampling 需要显式 capability，双方应设置工具循环限制并处理敏感数据。
- Tasks utility 在 2025-11-25 spec 中是 experimental；它给请求添加 durable task state、`tasks/get` polling、`tasks/result` deferred result retrieval、`tasks/cancel` 和 task status notifications 等机制。它支撑“长耗时请求状态跟踪”这个协议边界，但不等于完整 Agent 任务编排框架或生产可靠性保证。

## 支撑证据

- 2026-07-12 使用 `curl -L -I` 复核 `https://modelcontextprotocol.io/docs/learn/architecture.md`、`server-concepts.md`、`client-concepts.md`、`versioning.md`、`specification/2025-11-25/basic/authorization.md`、`docs/tutorials/security/security_best_practices.md` 和 `specification/2025-11-25/basic/utilities/tasks.md`，均返回 HTTP 200，`content-type: text/markdown; charset=utf-8`。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/docs/learn/architecture.md` 成功；页面包含 Scope、Participants、Data layer、Primitives、JSON-RPC、Streamable HTTP transport 和 host/client/server dedicated connection 等定义。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/docs/learn/server-concepts.md` 成功；页面包含 Tools、Resources、Prompts 的表格定义、model / application / user interaction model 和 human oversight 说明。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/docs/learn/client-concepts.md` 成功；页面包含 Elicitation、Roots、Sampling 的定义、安全说明、roots 不强制安全限制和 sampling human-in-the-loop 说明。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/llms.txt` 成功；索引显示当前 specification 页面为 `2025-11-25`，并列出 Authorization、Elicitation、Roots、Sampling、Tasks、Tools、Resources、Prompts 和 changelog 页面。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/docs/learn/versioning.md` 成功；页面说明协议版本格式为 `YYYY-MM-DD`，当前版本为 `2025-11-25`，并且该日期表示最近一次向后不兼容变更。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/specification/2025-11-25/changelog.md` 成功；页面列出相对 `2025-06-18` 的 major / minor changes，其中包括 URL mode elicitation 和 experimental tasks utility。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/specification/2025-11-25/server/tools.md` 成功；页面包含 `tools/list`、`tools/call`、`inputSchema`、`outputSchema`、tool annotations untrusted、tool execution errors 和 security considerations。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/specification/2025-11-25/server/resources.md` 成功；页面包含 `resources/list`、`resources/read`、resource templates、subscriptions、URI schemes、annotations 和 security considerations。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/specification/2025-11-25/server/prompts.md` 成功；页面包含 `prompts/list`、`prompts/get`、user-controlled interaction model、embedded resources 和 injection / unauthorized access 安全提示。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization.md` 成功；页面包含 authorization optional、HTTP/STDIO transport 差异、OAuth roles、discovery、scope selection、step-up authorization、token handling、PKCE、audience/resource validation 和 token passthrough 禁止。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices.md` 成功；页面包含 confused deputy、token passthrough、SSRF、session hijacking、local MCP server compromise、OAuth authorization URL validation、stdio proxy escalation、scope minimization 等 MCP-specific attack vectors 和 mitigation。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/specification/2025-11-25/client/roots.md`、`client/elicitation.md`、`client/sampling.md` 成功；页面包含 roots、用户交互、敏感信息、URL mode、sampling HITL 和工具循环安全边界。
- 2026-07-12 抓取 `https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks.md` 成功；页面说明 tasks 是 2025-11-25 引入的 experimental utility，支持 durable task state、polling、deferred result retrieval、cancellation、status notification、authorization-context binding、task ID entropy 和 rate limiting 边界。

## 可能的问题

- MCP 官方文档正在快速演进；协议版本号只表示向后不兼容变更日期，向后兼容更新可能不改变版本号，因此仍需要记录复核日期。
- 官方 docs 的教程示例常使用特定 host 或模型供应商，正文应抽取协议边界，不绑定单一产品。
- Roots 是协调机制而不是安全边界；正文不能把它写成强制 sandbox。
- Authorization spec 是 transport-level 能力，且 authorization 对 MCP implementations 是 optional；不能写成所有 MCP 连接都天然具备 OAuth 安全模型。
- Security Best Practices 是 implementation guidance；它能支撑风险和缓解方向。标准库模拟、本地 stdio JSON-RPC harness 和官方 MCP Python SDK / FastMCP stdio harness 已验证最小 trace 字段、进程边界、SDK tools/resources/prompts 流程和 resource/tool review 流程，但仍需要真实 host UI、OAuth、URL mode、sampling、tunnel 和跨 host 实验。
- Tasks 是 experimental utility；正文只能把它写成可选的长耗时请求状态/结果检索机制，不能把它写成 MCP 已经提供通用任务队列、工作流编排或生产级作业可靠性。

## 是否进入正文

- 结论：进入；职责边界可入正文
- 原因：MCP 章节必须优先引用官方文档；host/client/server、context exchange protocol、authorization optional、token passthrough 禁止、roots 非 sandbox、elicitation/sampling HITL 和 experimental tasks utility 等窄边界有官方直接支撑，并已和标准库 trace、本地 stdio JSON-RPC harness、官方 MCP Python SDK / FastMCP stdio harness 交叉验证。真实 host 权限 UI、URL mode / OAuth、token redaction、sampling、tasks、tunnel 和跨 host 行为仍待补。
