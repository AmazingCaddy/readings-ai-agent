# Real smolagents validation

## 目标

用 deterministic fake model 和本地 toy tools 验证 smolagents 的最小 runtime surface：`CodeAgent` 是否会执行 Python code snippet 调用工具，`ToolCallingAgent` 是否会执行 structured tool calls，`LocalPythonExecutor` 是否会阻断未授权 import，以及 `Tool.output_schema` 是否只作为说明信息而不做实际输出校验。

这个实验补强第 10 章和第 11 章中 smolagents 的框架定位与实践路线边界。它不是框架质量、benchmark、真实模型行为或 sandbox 安全测试。

## 运行方式

```bash
uv run --with smolagents python docs/experiments/real-smolagents-validation/real_smolagents_validation.py
```

如果没有安装 `smolagents`，脚本返回 `skipped`，不会把缺少依赖写成实验失败。

## 观察点

- `CodeAgent` 是否能从 fake model 生成的 Python snippet 调用本地 `read_policy` 和 `schema_probe` tools。
- `ToolCallingAgent` 是否能从 fake model 生成的 structured tool calls 依次调用同一组 tools，并看到 `final_answer` tool。
- 声明了 `output_schema` 的 tool 返回 plain string 时，runtime 是否不会自动做 output validation。
- 默认 local Python executor 是否会阻断未授权 `import os`。
- trace 是否避免泄露 untrusted document 中的示例 secret marker。

## 结论状态

- 当前状态：已用 `smolagents==1.26.0` 完成本地 fake-model run。
- 可支撑：smolagents 的 `CodeAgent` / `ToolCallingAgent` runtime surface、tool metadata / `output_schema` 的非强制校验边界、本地 executor 的 import allowlist 表面，以及 untrusted content 仍需应用层过滤/脱敏。
- 不能支撑：真实模型 tool selection、code-agent benchmark、Hub/MCP tool 安全、Docker/E2B/Blaxel/Modal sandbox 隔离、成本、延迟、trace 平台质量或生产可靠性。
