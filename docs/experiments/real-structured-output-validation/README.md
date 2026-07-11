# Real Structured Outputs / JSON Mode 对比实验

## 目标

验证真实 Responses API 下 free text、JSON mode 和 Structured Outputs 的差异，尤其是：格式可解析不等于业务语义正确。

## 实验边界

这是一个需要真实 OpenAI API 的实验 harness。没有 `OPENAI_API_KEY` 时脚本会输出 `skipped`，不写成已验证结果。

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

- 当前状态：harness 已准备；真实结果取决于本地是否配置 API key 和模型版本。
- 未完成前不得把 Structured Outputs 的真实稳定性写成正文结论。
