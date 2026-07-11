# Tool Calling 参数校验与重试实验

## 目标

验证手册第 03 章中的工程边界：模型生成工具调用请求和参数；应用程序负责校验、权限判断、执行工具、把错误或结果回传给模型；Function Calling 本身不执行函数。

## 实验边界

这是一个确定性的无模型实验。脚本使用 fake model 模拟两轮工具调用：第一轮生成错误参数，第二轮在收到工具错误后修正参数。

本实验不能证明真实模型一定能稳定修正参数，也不能证明某个 API/SDK 的具体错误格式。它只验证应用侧校验、错误回传、重试次数和 trace 设计是否自洽。

## 输入数据

- 用户请求：`What is the weather in Tokyo? Use celsius.`
- 工具：`get_weather(city, unit)`。
- 允许的 `unit`：`celsius`、`fahrenheit`。
- fake model 第一轮参数：`{"city": "Tokyo", "unit": "kelvin"}`。
- fake model 第二轮参数：`{"city": "Tokyo", "unit": "celsius"}`。

## 运行方式

```bash
uv run python docs/experiments/tool-calling-validation/tool_calling_validation.py
```

## 观察点

- 模型第一次只生成 tool call，不执行工具。
- 应用层发现 `unit=kelvin` 不满足业务规则，并生成 tool error。
- fake model 根据错误回传生成第二次 tool call。
- 应用层执行通过校验的工具调用，并把结果放回 history。
- trace 记录 `model.tool_call_requested`、`application.tool_validation_failed`、`application.tool_executed` 和 `model.final_response`。

## 结论状态

- 支撑：可以把“参数校验、错误回传和有限重试属于应用层控制循环”写入 Tool Use 章节。
- 仍缺：真实模型、真实 Function Calling API、严格 JSON schema、权限确认、prompt injection 工具结果隔离和多框架术语对照实验。
