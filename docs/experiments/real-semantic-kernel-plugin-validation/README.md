# Real Semantic Kernel Plugin Validation

## 目标

用真实 Semantic Kernel Python runtime 跑一个最小 native plugin / kernel function 验证，观察 plugin 注册、function metadata、参数 required/type 处理、应用层写工具审批和 side-effect trace。

## 实验边界

本实验不调用模型，不验证 Semantic Kernel Agent Framework、Process Framework、OpenAPI plugin、MCP plugin 或真实 human-in-the-loop UI。它只验证 Python Semantic Kernel native plugin 的本地 runtime 行为。

重要边界：Semantic Kernel 能从 native function 暴露 plugin/function metadata，并在 `kernel.invoke()` 时处理 required/type parsing；但高风险写操作是否转发、是否需要审批、是否幂等和是否脱敏，仍需要应用层 policy / wrapper / process 设计，不能写成框架默认自动保证。

## 运行方式

```bash
uv run --with semantic-kernel python docs/experiments/real-semantic-kernel-plugin-validation/real_semantic_kernel_plugin_validation.py
```

没有 Semantic Kernel 时，脚本会返回 `skipped`。

## 观察点

- `@kernel_function` 是否暴露 plugin/function metadata。
- `Kernel.add_plugin()` / `Kernel.get_function()` 是否能注册和查找 native plugin function。
- 缺少 required argument 是否被 runtime 拒绝。
- 不可解析的参数类型是否被 runtime 拒绝。
- 可解析的字符串数值是否会被解析并执行。
- 未审批写工具是否被应用层 policy 阻断且不转发给 kernel。
- 已审批写工具是否只产生预期 side effect。

## 结论状态

- 当前状态：已完成本地 Semantic Kernel 1.36.0 native plugin run。
- 可支撑：Semantic Kernel native plugin / kernel function metadata、runtime 参数解析、应用层审批 wrapper 和 side-effect trace 的窄观察。
- 不能支撑：真实模型 tool selection、function calling 修正、OpenAPI/MCP plugin 行为、Agent Framework、Process Framework、HITL UI、参数快照、持久化恢复、幂等性、成本、延迟或生产安全。
