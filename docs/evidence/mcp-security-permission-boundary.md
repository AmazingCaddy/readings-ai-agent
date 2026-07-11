# Evidence Note: MCP 安全、授权与权限边界

## 要验证的结论

MCP 提供标准化的工具、资源、提示、授权、roots、elicitation 和 sampling 协议能力，但这些能力本身不是完整安全边界。生产系统仍需要 host、client、server 在授权、最小权限、用户确认、token audience 校验、输入输出校验、sandbox 和审计方面共同实现控制。

## 资料来源

- Source 1：[Model Context Protocol Official Documentation](../sources/source-cards/2026-mcp-official-docs.md)
- Source 2：[Evidence Note: MCP Host / Client / Server 职责边界](mcp-role-boundary.md)
- Source 3：[Evidence Note: 工具权限、人工确认与审计边界](tool-permission-audit-boundary.md)
- Source 4：[Evidence Note: Prompt Injection 与权限边界](prompt-injection-permission-boundary.md)

## 交叉验证结果

- 一致点：MCP tools spec 将 tools 定义为 model-controlled，并建议应用提供清晰的工具暴露 UI、工具调用视觉提示和敏感操作确认；security considerations 要求 server 校验 tool input、访问控制、限流、输出清理，client 做用户确认、展示 tool inputs、校验 tool results、设置 timeout 和记录审计日志。
- 一致点：MCP resources spec 将 resources 定义为 application-driven，由 host application 决定如何把上下文纳入任务；server 必须校验 resource URI，并应对敏感资源做访问控制和权限检查。这支持正文中“resources 也可能泄露敏感信息或携带恶意内容”的保守表述。
- 一致点：MCP prompts spec 将 prompts 定义为 user-controlled，通常由用户显式选择；prompt 输入输出也必须校验，以防 injection attacks 或未授权资源访问。这支持正文中“server prompt 不应被当成绝对可信系统规则”的边界。
- 一致点：MCP authorization spec 说明 authorization 是 transport-level optional capability。HTTP-based transport 支持 authorization 时应遵循 OAuth 2.1 相关规范；STDIO transport 不应使用该 OAuth flow，而应从环境取得凭据。这说明“接入 MCP”不等于“自动具备统一 OAuth 安全”。
- 一致点：MCP authorization spec 把 protected MCP server 定义为 OAuth resource server，把 MCP client 定义为 OAuth client；client 必须用 bearer token 的 `Authorization` header，不能把 access token 放在 URI query string 中，server 必须验证 token 是发给自己的 audience/resource。
- 一致点：MCP authorization spec 和 Security Best Practices 都禁止 token passthrough。MCP server 不应接受或转发不是明确签发给自己的 token；如果要访问上游 API，应使用单独的上游 token。
- 一致点：Security Best Practices 针对 MCP 实现列出 confused deputy、SSRF、session hijacking、local MCP server compromise、authorization URL validation、stdio proxy escalation、scope minimization 等风险，并给出 per-client consent、redirect URI exact matching、state validation、HTTPS、私有 IP 阻断、sandbox、scope 最小化、egress proxy 和审计等缓解方向。
- 一致点：Roots spec 让 client 向 server 暴露 filesystem roots，但也要求 client 只暴露有权限的 roots、校验 URI、防 path traversal、实现 access control；server 应尊重 root boundaries。它更像协议协作和可见范围提示，不能替代 OS sandbox 或 host 权限控制。
- 一致点：Elicitation spec 要求 form mode 不得请求密码、API keys、access tokens、payment credentials 等敏感信息，敏感交互应走 URL mode；client 必须明确展示哪个 server 请求信息，并提供 decline/cancel 选项。
- 一致点：Sampling spec 允许 server 通过 client 请求 LLM generation，并强调 client 仍控制模型访问、选择和权限；sampling requests 建议保留 human-in-the-loop，可被用户拒绝。tool-enabled sampling 需要显式 capability，工具循环应有限制。
- 一致点：OpenAI Agents SDK 与 Responses API 的工具权限 evidence 也显示，高风险工具需要 `require_approval`、guardrails、pause/resume、trace 和审计配合；这与 MCP 官方安全建议方向一致，但具体 API 字段不同。

## 实验验证

- 是否需要实验：是
- 实验设计：实现或接入一个只读 MCP server，记录 `tools/list`、`tools/call`、`resources/list`、`resources/read`；再加入一个需要确认的模拟写操作和一个恶意 resource/prompt，观察 host 是否展示工具输入、是否可拒绝、是否记录审计 trace、是否阻断越权路径或 token/URL 风险。
- 结果：待执行

## 结论状态

- 部分验证：官方 spec 和 security best practices 已直接支撑 MCP 安全、授权和权限边界的正文表述；仍缺本地 host/client/server trace、最小权限实验和不同 host 实现差异对比。

## 可进入章节

- 是。可以写成：MCP 标准化了工具、资源、提示和部分授权/交互机制，但安全不是“协议一接就自动完成”；高风险能力仍需要最小权限、用户确认、token audience 校验、输入输出校验、sandbox、审计和本地实验验证。
