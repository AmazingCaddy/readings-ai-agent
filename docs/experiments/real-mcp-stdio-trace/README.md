# Real MCP Stdio Trace 实验

## 目标

验证 MCP host/client/server 职责边界在真实进程和 stdio JSON-RPC 消息中如何形成 trace：host 启动 server，client 发送 `initialize`、`tools/list`、`tools/call`、`resources/list`、`resources/read`，host 在工具调用和资源读取前后记录审批与审计事件。

## 实验边界

这是一个标准库 stdio JSON-RPC harness，不使用官方 MCP SDK，也不连接真实 MCP host UI。它比内存模拟多验证了进程边界、请求 ID、方法名和 JSON-RPC 消息流，但不能代表任何具体 MCP SDK、host 或产品的默认安全行为。

本实验不覆盖 OAuth、URL mode elicitation、真实 sampling、真实文件 sandbox、token audience 校验或跨 host 差异。

## 运行方式

```bash
uv run python docs/experiments/real-mcp-stdio-trace/mcp_stdio_trace.py
```

## 观察点

- `initialize` 是否记录 server capabilities。
- `tools/list` 是否返回工具 catalog。
- `tools/call` 是否在 host 层先做 approval，再决定是否转发给 server。
- `resources/read` 是否在 host 层进行 resource review。
- roots 是否只作为 host 暴露给 server 的范围提示，而不是 sandbox 证明。
- trace 中是否避免记录真实 token；脚本里的 `secret=example-token` 是假数据。

## 结论状态

- 支撑：可以把 MCP trace 字段和 host/client/server 职责边界从内存模拟升级为“本地 stdio JSON-RPC harness 已验证”。
- 仍缺：官方 MCP SDK / 真实 host UI / OAuth / URL mode elicitation / token redaction / 跨 host 行为实验。
