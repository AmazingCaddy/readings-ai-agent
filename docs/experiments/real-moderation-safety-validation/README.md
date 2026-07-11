# Real Moderation Safety Validation

## 目标

把 OpenAI Moderation 文档中的安全信号边界迁移到真实 API harness：记录 `flagged`、categories、category scores、latency、误报 / 漏报样本、tool arguments / tool output 覆盖和应用层 policy decision。

这个实验不是为了证明 Moderation API 足够安全，而是为了验证项目中应该如何把 moderation 结果当作 policy signal、审计字段和人工复核输入。

## 当前状态

- Harness 已准备：`real_moderation_safety_validation.py`
- 当前运行状态：`skipped`，因为未设置 `OPENAI_API_KEY`。
- 结果页：[2026-07-11 结果](results-2026-07-11.md)

## 运行方式

```bash
uv run python docs/experiments/real-moderation-safety-validation/real_moderation_safety_validation.py
```

可选环境变量：

- `OPENAI_API_KEY`：未设置时返回 `skipped`。
- `OPENAI_MODERATION_MODEL`：默认 `omni-moderation-latest`。
- `OPENAI_MODERATION_URL`：默认 `https://api.openai.com/v1/moderations`。

## 样本覆盖

- benign support question。
- obvious self-harm instruction request。
- high-risk tool-call arguments。
- benign tool output。

## 观察字段

- `flagged`。
- `flagged_categories`。
- top category scores。
- `category_applied_input_types` 是否出现。
- latency。
- expected vs actual flagged mismatch。
- policy decision：allow、human review、possible false positive review、possible false negative fallback。

## 结论边界

- 可支撑：真实 Moderation API 观测入口、结果字段模板、误报 / 漏报记录方式和应用层 policy signal 设计。
- 当前不能支撑：当前环境未设置 API key，没有真实 completed run。即使后续运行成功，也只能验证所选 moderation model、样本、账号、网络和时间窗口；不能证明阈值策略、检测层、人工复核流程、tool permission 或生产安全充分有效。

## 不覆盖

- tool name、tool description、tool schema 和 response-format schema 的安全审查。
- streaming partial deltas 的实时控制。
- Prompt injection / tool permission 真实模型对照。
- HITL 成本、延迟和人工复核负担。
- 业务政策、合规义务或第三方工具数据保留。

## 下一步

1. 配置 API key 后运行 completed case。
2. 把结果同步到 OpenAI Moderation source card、production security chapter、validation backlog 和 coverage matrix。
3. 扩展到 prompt-only / moderation-only / policy-enforced / HITL 对照，记录 false positive、false negative、成本、延迟和人工复核负担。
