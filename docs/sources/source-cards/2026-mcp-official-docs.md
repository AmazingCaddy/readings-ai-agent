# Model Context Protocol Official Documentation

- 来源链接：https://modelcontextprotocol.io/
- 作者 / 机构：Model Context Protocol project
- 发布时间：待复核
- 最后复核日期：2026-07-11
- 类型：官方文档 / 协议文档
- 主题：MCP / Tools / Resources / Prompts
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接已复核；architecture、server concepts、client concepts 关键段落已精读；核心职责边界已交叉验证

## 一句话总结

MCP 官方文档是解释 MCP 组件、能力边界和工具生态的首选 reference。

## 核心结论

- MCP 官方 architecture overview 将 MCP 定位为 context exchange 协议；文档明确说明 MCP focuses solely on the protocol for context exchange，不规定 AI applications 如何使用 LLM 或管理提供的上下文。
- MCP follows a client-server architecture：MCP host 是协调和管理一个或多个 MCP clients 的 AI application；MCP client 是维护到 MCP server 连接并获取上下文的组件；MCP server 是向 MCP clients 提供上下文的程序。
- 官方文档说明 host 会为每个 MCP server 创建一个 MCP client，每个 client 维护到对应 server 的 dedicated connection。
- MCP data layer 包括 lifecycle management、server features、client features 和 utility features；server features 包括 tools、resources、prompts。
- 官方 server concepts 将 tools、resources、prompts 区分为三类 building blocks：tools 是模型可主动调用的函数，resources 是应用可读取的只读上下文数据源，prompts 是用户显式调用的可复用指令模板。
- 官方 client concepts 说明 sampling 可让 servers 通过 client 请求 LLM completions，并强调这种方式让 client 控制用户权限和安全措施。

## 支撑证据

- 2026-07-11 抓取 `https://modelcontextprotocol.io/docs/learn/architecture.md` 成功；页面包含 Scope、Participants、Data layer、Primitives 等定义。
- 2026-07-11 抓取 `https://modelcontextprotocol.io/docs/learn/server-concepts.md` 成功；页面包含 Tools、Resources、Prompts 的表格定义和 user interaction model。
- 2026-07-11 抓取 `https://modelcontextprotocol.io/docs/learn/client-concepts.md` 成功；页面包含 Elicitation、Roots、Sampling 的定义和安全说明。

## 可能的问题

- MCP 官方文档正在快速演进，spec version、roadmap 和 SDK 行为需要记录复核日期。
- 官方 docs 的教程示例常使用特定 host 或模型供应商，正文应抽取协议边界，不绑定单一产品。
- Roots 是协调机制而不是安全边界；正文不能把它写成强制 sandbox。

## 是否进入正文

- 结论：进入
- 原因：MCP 章节必须优先引用官方文档。
