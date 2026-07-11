# Real Tool Calling 参数校验与重试实验

## 目标

验证标准库模拟实验尚未覆盖的真实 API 边界：模型通过 Responses API 生成 tool call，应用层执行业务参数校验，并把错误或结果回传给模型。

## 实验边界

这是一个需要真实 OpenAI API 的实验 harness。没有 `OPENAI_API_KEY` 时脚本会输出 `skipped`，不写成已验证结果。

本实验只验证所选模型、所选工具 schema 和当前 API 版本下的行为，不能代表所有模型都能稳定修正工具参数。

## 运行方式

```bash
uv run python docs/experiments/real-tool-calling-validation/real_tool_calling_validation.py
```

可选环境变量：

- `OPENAI_MODEL`：默认 `gpt-4.1-mini`。
- `OPENAI_RESPONSES_URL`：默认 `https://api.openai.com/v1/responses`。

## 观察点

- API 是否返回 function tool call。
- tool call arguments 是否满足 JSON schema。
- 应用层业务校验是否发现 schema 之外的非法值。
- 把 tool error 回传后，模型是否修正参数、拒绝请求或直接给出说明。
- trace 是否足以记录 request、tool call、validation error、tool result 和 final response。

## 结论状态

- 当前状态：harness 已准备；真实结果取决于本地是否配置 API key 和模型版本。
- 未完成前不得把真实 API 稳定性写成正文结论。
