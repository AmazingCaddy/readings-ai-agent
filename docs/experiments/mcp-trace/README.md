# MCP 最小 Trace 实验

## 目标

验证手册第 05 章中的一个窄结论：MCP host、client、server 的职责可以通过 `tools/list`、`tools/call`、`resources/list`、`resources/read` 和 `roots/list` 这样的协议事件记录为 trace；高风险工具和不可信资源需要 host 侧策略、用户确认和审计记录配合。

## 实验边界

这不是完整 MCP SDK 实验，也不连接真实 host。脚本只用 Python 标准库模拟 MCP-style JSON-RPC 方法名和最小数据结构，用来验证概念、trace 字段和初学者讲解是否自洽。

不能从本实验推出：某个真实 MCP client、host 或 SDK 默认会实现这些权限策略。

## 输入数据

- 一个只读工具：`lookup_policy_section`。
- 一个模拟写工具：`write_release_note`，host policy 默认拒绝。
- 一个安全资源：`handbook://mcp/security`。
- 一个恶意资源：`handbook://mcp/malicious-note`，包含 prompt injection 风格文本。
- 一个 roots 列表：`file:///workspace/readings-ai-agent`。

## 运行方式

```bash
uv run python docs/experiments/mcp-trace/mcp_trace_simulation.py
```

## 观察点

- `tools/list` 是否能记录 server 暴露了哪些工具。
- `tools/call.approval` 是否能在 host 层记录批准或拒绝原因。
- `resources/read.review` 是否能把不可信资源标记为 prompt injection 候选。
- `roots/list` 是否只是暴露可见范围，不代表真正 sandbox。
- trace 是否避免记录真实 token。脚本里的 `secret=example-token` 是假数据，只用于演示敏感字段不应进入真实日志。

## 结论状态

- 支撑：可以把 MCP 章节中的 trace 字段和职责边界从纯文档推导升级为“本地最小模拟已验证”。
- 仍缺：真实 MCP SDK/host 的行为验证、工具确认 UI、URL mode elicitation、token redaction、remote authorization 和跨 host 差异比较。
