# Real MCP SDK Trace 实验

## 目标

用官方 MCP Python SDK 复现最小 host / client / server stdio 流程，和已有标准库 JSON-RPC harness 形成对照：SDK server 暴露 tools、resources 和 prompts，SDK client 通过 `ClientSession` 调用，host policy 在写工具调用前做审批，在 resource read 后做不可信内容 review，并记录脱敏 trace。

## 实验边界

本实验使用官方 Python SDK 的 `FastMCP`、`stdio_client` 和 `ClientSession`，但仍是本地 toy server 和脚本化 host policy，不是真实桌面 host UI、remote connector、OAuth flow、URL mode elicitation、sampling 或 tunnel 部署。

## 运行方式

```bash
uv run --with mcp python docs/experiments/real-mcp-sdk-trace/mcp_sdk_trace.py
```

没有 `mcp` Python package 时，脚本返回 `skipped`，不伪造 SDK 结果。

## 观察点

- `initialize` 是否返回 protocol version、server info 和 capabilities。
- `tools/list` 是否返回 SDK tool catalog 和 input/output schema。
- `tools/call` 是否可以调用只读工具。
- 写工具是否在 host approval 阶段被拒绝，并且不转发给 server。
- `resources/list` / `resources/read` 是否返回 SDK resource metadata 和 contents。
- 恶意 resource 是否被 host review 标记为 `untrusted_prompt_injection_candidate`。
- `prompts/list` / `prompts/get` 是否返回 prompt catalog 和 prompt message。
- trace 中是否脱敏示例 secret marker。

## 结论状态

- 支撑：官方 MCP Python SDK 可以在本地 stdio 中完成 initialize、tools、resources 和 prompts 的最小流程；host 层仍需要单独实现工具审批、resource review 和 trace 脱敏。
- 仍缺：真实 host UI、OAuth / URL mode elicitation、sampling、token audience validation、roots / filesystem sandbox、remote MCP connector、tunnel 和跨 host 行为实验。
