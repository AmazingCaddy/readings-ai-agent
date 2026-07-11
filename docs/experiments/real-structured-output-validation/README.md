# Real Structured Outputs / JSON Mode 对比实验

## 目标

验证真实 Responses API 下 free text、JSON mode 和 Structured Outputs 的差异，尤其是：格式可解析不等于业务语义正确。

## 实验边界

这是一个可连接真实 OpenAI API 的实验 harness。没有 `OPENAI_API_KEY` 时，脚本会运行 deterministic local control：复用同一套 JSON extraction、schema validation 和 semantic validation 逻辑，验证“可解析 / schema-valid / semantic-valid”的本地判断边界，但显式标记 `real_api_validated=false`。

本实验只验证所选模型、所选 schema、所选输入和当前 API 版本下的行为，不能代表所有模型或所有业务场景。

## 运行方式

```bash
uv run python docs/experiments/real-structured-output-validation/real_structured_output_validation.py
```

可选环境变量：

- `OPENAI_MODEL`：默认 `gpt-4.1-mini`。
- `OPENAI_RESPONSES_URL`：默认 `https://api.openai.com/v1/responses`。

## 观察点

- free text 是否难以稳定解析。
- JSON mode 是否能输出合法 JSON。
- Structured Outputs 是否满足 schema。
- schema-valid 输出是否仍可能违反业务规则。
- API 是否返回 refusal，以及 refusal 是否被应用层识别。

## 结论状态

- 当前状态：无 API key 时已完成本地 deterministic schema/semantic control；真实 Responses API 结果取决于本地是否配置 API key 和模型版本。
- 本地 control 可支撑“schema-valid 仍可能业务错误”的应用层校验边界；不得把它写成 Structured Outputs、JSON mode、refusal 或 retry 的真实 API 稳定性结论。
