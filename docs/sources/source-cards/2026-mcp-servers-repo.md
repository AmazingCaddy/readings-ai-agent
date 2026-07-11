# Model Context Protocol Servers Repository

- 来源链接：https://github.com/modelcontextprotocol/servers
- 作者 / 机构：Model Context Protocol project
- 发布时间：持续更新 repository
- 最后复核日期：2026-07-12
- 类型：Source Code / Examples
- 主题：MCP / Tools / Server Examples
- 适合阶段：工程实践
- 可信度等级：A
- 是否已验证：GitHub repo metadata、README、`src` directory API 和 Everything / Filesystem / Git reference server README 已于 2026-07-12 复核；与 MCP official docs、MCP stdio harness 和 MCP SDK harness 完成交叉验证；支撑 reference server / educational example / client configuration / tool annotation 的窄边界；真实 host、真实 server 运行、安全效果和生产可靠性仍部分验证

## 一句话总结

MCP servers repository 是理解 MCP 工具服务实现和示例生态的重要源码 reference。

## 核心结论

- README 将该 repository 定义为 MCP reference implementations 的集合，也包含 community-built servers 和额外资源引用。
- README 明确说明如果要找 MCP servers 列表，应浏览 MCP Registry；该 repository 只容纳 MCP steering group 维护的少量 reference servers。
- README warning 明确说明这些 servers 用于展示 MCP features 和 SDK usage，是教育示例，不是 production-ready solutions。
- 2026-07-12 `src` directory API 复核确认当前 reference server 目录为 Everything、Fetch、Filesystem、Git、Memory、Sequential Thinking、Time。
- README 说明单独运行 server 并不太有用，server 应配置到 MCP client 中使用；示例包含 `npx`、`uvx`、Claude Desktop 和 VS Code 配置片段。
- Everything README 明确它是用于 exercise MCP protocol features 的测试 server，不是 useful server；它展示 prompts、tools、resources、sampling、stdio、SSE 和 Streamable HTTP 等能力形态。
- Filesystem README 支撑一个权限示例边界：server 通过命令行参数或 MCP Roots 限制 allowed directories，要求至少一个 allowed directory，并用 ToolAnnotations 区分 read-only、idempotent、destructive 和 open-world hints；但这些 hints 只是 client 可参考的协议提示，不等于 host 已经强制审批或 sandbox。
- Git README 明确 `mcp-server-git` 仍处 early development，工具包括 status / diff / log 等只读操作，也包括 add / commit / reset / checkout / branch 等会改变仓库状态的操作；因此 git server 适合作为高风险工具权限示例，不应被初学者直接当成安全默认配置。

## 支撑证据

- 2026-07-12 使用 `curl -L -I https://github.com/modelcontextprotocol/servers` 复核 GitHub 页面，返回 HTTP 200，`content-type: text/html; charset=utf-8`。
- 2026-07-12 使用 GitHub API 复核 repo metadata：`full_name=modelcontextprotocol/servers`，`default_branch=main`，`archived=false`，`language=TypeScript`，`updated_at=2026-07-11T20:43:19Z`，`pushed_at=2026-07-10T03:30:19Z`。
- 2026-07-12 抓取 `https://raw.githubusercontent.com/modelcontextprotocol/servers/main/README.md` 成功；README 包含 MCP Registry 提示、reference implementation 定位、non-production warning、reference server list、`npx` / `uvx` / Claude Desktop 配置示例和 releasing/security/license 链接。
- 2026-07-12 使用 `https://api.github.com/repos/modelcontextprotocol/servers/contents/src?ref=main` 复核 `src` 目录，返回 7 个 reference server 目录：`everything`、`fetch`、`filesystem`、`git`、`memory`、`sequentialthinking`、`time`。
- 2026-07-12 抽样抓取 `src/everything/README.md`、`src/filesystem/README.md` 和 `src/git/README.md` 成功；分别补强测试 server、filesystem allowed-directory / annotations 和 git write-tool / early-development 边界。

## 可能的问题

- 示例 server 不等同于生产级安全设计。
- 需要结合 MCP 官方文档和安全资料分析权限边界。
- repository 内容和 reference server 列表可能随时间变化，引用时需要记录复核日期。
- Filesystem 的 roots / allowed directories 和 tool annotations 可作为权限设计学习材料，但不能证明 host 会正确展示、审批或强制这些 hints。
- Git server 暴露会改变仓库状态的工具，必须作为高风险工具示例处理；当前未验证真实 client UI、审批、参数快照、rollback 或审计日志。

## 初学者阅读建议

- 先理解 MCP server/client/host 概念，再挑一个简单 server 看代码结构。

## 可复现实验

- 已完成本地 stdio JSON-RPC harness 和官方 MCP Python SDK / FastMCP stdio harness，记录 tools/resources/prompts 暴露方式、host approval、resource review、写工具不转发和 trace 脱敏；它们不等同于这些 reference servers 或真实 host 行为验证。

## 是否进入正文

- 结论：进入
- 原因：MCP 和实践项目章节需要官方源码 examples；但这些 examples 只能支撑 server 目录形态、SDK usage 和教育示例边界，不能写成生产安全、权限完整或真实 host 行为已经验证。
