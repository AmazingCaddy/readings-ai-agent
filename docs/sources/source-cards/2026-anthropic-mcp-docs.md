# Anthropic MCP Connector and Tunnels Documentation

- 来源链接：https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md
- 相关链接：https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers.md；https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview.md；https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/concepts.md；https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/security.md
- 作者 / 机构：Anthropic
- 发布时间：持续更新文档；MCP connector、remote MCP servers、MCP tunnels overview/concepts/security 页面复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：官方文档 / 产品集成文档
- 主题：MCP / Tool Use / API Integration / Security
- 适合阶段：工程实践 / 进阶
- 可信度等级：A
- 是否已验证：来源链接和关键段落已复核；旧 Anthropic MCP 概念页已确认重定向到 Model Context Protocol 官方站点；Anthropic-specific MCP connector、remote MCP servers、tool allowlist/denylist、OAuth bearer token、MCP tunnels 和 shared responsibility 边界可作为产品集成证据；不替代 MCP 官方 specification

## 一句话总结

Anthropic 文档适合说明 Claude / Messages API 如何接入远程 MCP tools，以及私有网络 MCP servers 如何通过 MCP tunnels 暴露给 Claude；通用 MCP 概念和协议边界仍应优先引用 MCP 官方文档。

## 核心结论

- 旧 Anthropic MCP 概念链接 `https://docs.anthropic.com/en/docs/agents-and-tools/mcp` 已重定向到 `https://modelcontextprotocol.io/docs/getting-started/intro`；因此通用 MCP 概念证据应归入 MCP 官方文档 source card，而不是重复写成 Anthropic 概念文档。
- Anthropic MCP connector 允许开发者通过 Messages API 直接连接 remote MCP servers，而不需要单独实现 MCP client。
- MCP connector 当前需要 beta header `anthropic-beta: mcp-client-2025-11-20`；此前 `mcp-client-2025-04-04` 已被文档标为 deprecated。
- MCP connector 不适用于 Zero Data Retention；通过 MCP servers 交换的数据、工具定义和执行结果按 Anthropic 标准数据保留政策处理。
- MCP connector 当前只支持 MCP specification 中的 tool calls；如果需要 local stdio servers、MCP prompts、MCP resources 或更细控制，应使用 client-side MCP helpers / SDK 方式。
- MCP connector 要求 server 通过 HTTP 公开暴露，支持 Streamable HTTP 和 SSE transports；local STDIO servers 不能直接连接到该 connector。
- Messages API 中，`mcp_servers` 数组定义 server URL、name 和可选 `authorization_token`；`tools` 数组中的 `mcp_toolset` 指定启用哪个 server 的工具。
- 工具配置支持 enable all、allowlist、denylist 和 per-tool configuration。文档建议 read-only assistant 或需要 human confirmation 的场景 denylist 写入或破坏性工具。
- Remote MCP servers 页面明确说明第三方 remote MCP servers 不由 Anthropic 拥有、运营或背书，用户只应连接信任的 server，并审查其安全实践和服务条款。
- MCP tunnels 允许 Claude 连接私有网络中的 MCP servers，不需要打开 inbound firewall ports 或把服务暴露到公网；但它是 research preview，按文档提供 as-is，没有 uptime、support 或 continuity commitment，并依赖 Cloudflare 作为第三方网络提供商。
- MCP tunnels 的连接方向是 `cloudflared` 从用户网络向 tunnel edge 发起 outbound-only connection；请求方向仍是 Anthropic 经由该连接向用户网络内的 upstream MCP server 发送 MCP requests。
- MCP tunnels stack 包含 `cloudflared` 和 Anthropic proxy。Proxy 终止 inner TLS、校验 upstream IP 是否在 allowed range 内，并按 hostname 路由到 upstream MCP server。
- MCP tunnels security model 包括 outer mTLS、inner TLS 和每个 MCP server 的 OAuth。Cloudflare 不能读取 MCP request/response payload，但会看到连接元数据。
- Shared responsibility table 说明 Anthropic 负责 tunnel access control、CA certificate validation 和确保 Claude 只向组织拥有的 tunnels 发请求；用户组织负责内容和流量、部署加固、保护 tunnel tokens / TLS private keys、证书续期、每个 MCP server 的 OAuth、网络限制和 breach notification。
- Tunnels 文档明确警告：如果攻击者同时获得 tunnel token 和 TLS private key，就可能 impersonate proxy 并读取 MCP request payloads。
- Tunnels security best practices 要求每个 MCP server 使用 OAuth、启用 SSO、把 `upstream.allowed_ips` 限制到最小 CIDR、监控日志、轮换证书和 tunnel token、固定镜像 SHA、限制网络可达范围、限制 MCP server scope 并保护静态凭据。

## 支撑证据

- 2026-07-11 使用 `curl -L -I https://docs.anthropic.com/en/docs/agents-and-tools/mcp` 复核重定向链：`docs.anthropic.com` -> `platform.claude.com/docs/en/docs/agents-and-tools/mcp` -> `platform.claude.com/docs/en/agents-and-tools/mcp` -> `https://modelcontextprotocol.io/` -> `/docs/getting-started/intro`，最终 HTTP 200。
- 2026-07-11 抓取 `https://docs.anthropic.com/llms.txt` 成功；索引列出 MCP connector、remote MCP servers、MCP tunnels overview/concepts/security 等 Anthropic Platform 文档。
- 2026-07-11 抓取 `https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md` 成功；页面包含 beta header、ZDR 限制、key features、limitations、`mcp_servers` / `mcp_toolset` 配置、allowlist / denylist、response content block、client-side helpers 和 data retention 段落。
- 2026-07-11 抓取 `https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers.md` 成功；页面包含第三方 remote MCP servers 信任边界和连接前审查建议。
- 2026-07-11 抓取 `https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview.md` 成功；页面包含 outbound-only、research preview、security layers、shared responsibility、Cloudflare metadata 和 Messages API 使用段落。
- 2026-07-11 抓取 `https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/concepts.md` 成功；页面定义 tunnel stack、proxy、cloudflared、setup component、tunnel edge、inner TLS、upstream MCP server 和 connection/request direction。
- 2026-07-11 抓取 `https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/security.md` 成功；页面包含 OAuth、SSO、`upstream.allowed_ips`、日志监控、证书/token 轮换、镜像固定、网络限制、server scope 和凭据保护建议。

## 可能的问题

- 这是 Anthropic 产品集成文档，不是 MCP 通用 specification；正文不能用它替代 `modelcontextprotocol.io` 的 host/client/server、tools/resources/prompts、authorization、roots、elicitation、sampling 等协议定义。
- MCP connector 当前只支持 MCP tool calls；不能写成 Claude Messages API connector 已支持 MCP 的 resources、prompts、roots、sampling 或 elicitation 全部能力。
- MCP connector 需要公开 HTTP server；local STDIO server 不能直接连到 connector。需要 local server、prompts、resources 或更细控制时，应使用 SDK helper / 自建 MCP client。
- allowlist/denylist 是工具暴露控制，不是完整安全方案；仍需要 server 侧授权、输入输出校验、用户确认、审计和敏感 trace 控制。
- MCP tunnels 降低了公开暴露私有 MCP server 的需求，但不是“自动安全”。它仍要求 OAuth、SSO、allowed IPs、网络限制、凭据保护、日志监控和 shared responsibility。
- Tunnels 是 research preview，不能支撑生产可靠性、可用性或长期支持承诺。

## 初学者阅读建议

- 先读本手册第 05 章和 MCP official docs，弄清 host/client/server、tools/resources/prompts 和 authorization optional 的基本边界。
- 再读 Anthropic MCP connector 页面，理解一个具体模型 API 如何把 remote MCP tools 暴露成可调用工具。
- 如果你所在团队需要把内网 MCP server 给 Claude 用，再读 MCP tunnels overview / concepts / security；初学者不需要一开始就部署 tunnels。

## 可复现实验

- 使用一个只读 remote MCP server，通过 Messages API `mcp_servers` 和 `mcp_toolset` 调用工具，记录 `mcp_tool_use` / `mcp_tool_result`、工具 allowlist/denylist、authorization token handling、错误返回和 trace 脱敏。
- 使用 local stdio MCP server + Anthropic SDK client-side helpers 对照 MCP connector，验证 local tools、prompts、resources 和 unsupported content type 的差异。
- 如获得 MCP tunnels access，部署 sample tunnel，验证 outbound-only 连接、proxy routing、`upstream.allowed_ips`、OAuth、token/cert rotation、Cloudflare metadata 边界和 breach teardown 流程。

## 是否进入正文

- 结论：部分进入
- 原因：可作为第 05/09/12 章中 Anthropic-specific MCP integration、remote MCP tools、tool allowlist/denylist、connector limitation、data retention、MCP tunnels 和 shared responsibility 的产品集成证据。不能用于替代 MCP official docs 的协议定义，也不能推出 MCP connector / tunnels 默认安全、默认生产可靠或支持全部 MCP capability。
