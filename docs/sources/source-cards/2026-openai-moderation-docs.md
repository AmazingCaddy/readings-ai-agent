# OpenAI Moderation Documentation

- 来源链接：https://developers.openai.com/api/docs/guides/moderation.md
- 作者 / 机构：OpenAI
- 发布时间：持续更新 documentation
- 最后复核日期：2026-07-11
- 类型：Official Docs / Safety
- 主题：Moderation / Content Filtering / Safety Signals
- 适合阶段：工程实践 / 生产化前检查
- 可信度等级：A
- 是否已验证：官方 Markdown 页面返回 HTTP 200；关键段落已精读；可支撑 moderation 作为检测信号、输入/输出分类、类别/分数解释、tool-calling 覆盖边界和 streaming 限制的工程边界；真实误报、漏报、策略阈值、人工复核和生产效果仍部分验证

## 一句话总结

OpenAI Moderation 文档适合用来理解内容过滤信号如何进入应用策略：它能检测文本和图像中的 harmful content，但结果应被用于过滤、路由人工复核或账户干预，而不是被当成自动安全保证。

## 核心结论

- Moderation models 可检测文本和图像中的 harmful content；`omni-moderation-latest` 接受 text 和 image inputs，不分类 audio。
- 可以在 Responses API / Chat Completions 生成请求中传入 top-level `moderation` object，同时获得 input 和 generated output 的 moderation scores。
- 生成请求中的 moderation 不会阻止模型正常生成；应用应在展示输出或执行下游动作前检查 moderation results。
- 文档明确说应把 moderation scores 当作应用 policy 的 signals，而不是 automatic blocking decision。
- moderation result 包含 `flagged`、`categories`、`category_scores` 和 `category_applied_input_types`，可用于日志、路由、审计或 human-review queues。
- moderation step 可能失败；相关 input/output moderation field 可能是 error 而不是 scores，应用需要处理这种情况。
- tool-calling 请求中，moderation 覆盖 conversation content 里的 tool-call arguments 和 tool outputs；不覆盖 tool names、tool descriptions、tool schemas 或 response-format schemas。
- streaming 生成时，moderation scores 会在完整 generated output 可用后到达，不包含在 partial output deltas 中。
- 文档说明 moderation endpoint underlying model 会持续升级，因此依赖 `category_scores` 的自定义策略需要随时间重新校准。
- 部分类别只支持 text，部分支持 text and images；图片文件大小有限制。

## 支撑证据

- `moderation.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 13:02:56 GMT`；`content-type: text/markdown; charset=utf-8`。
- 文档列出 4 类 workflow：moderate generated content、classify standalone inputs、understand moderation results、review supported categories。
- 文档的 inline moderation 段落明确：模型仍正常生成；展示给用户或执行下游动作前应 review moderation results。
- 文档明确：treat moderation scores as signals for your application's policy, not as an automatic blocking decision。
- 文档明确 tool-calling 覆盖和不覆盖范围，并说明 streaming 下 scores 到达时机。

## 可能的问题

- Moderation 是检测信号，不是完整安全边界；不能替代权限、参数校验、HITL、审计、red-team 和 regression set。
- `category_scores` 依赖模型版本和阈值策略，随着 moderation model 升级需要重新校准。
- tool name、description、schema 和 response-format schema 不在 moderation 覆盖内；这些仍需要开发者审查。
- streaming 场景不能在 partial deltas 中直接拿到最终 moderation scores；如果需要边生成边控制，需要额外设计。

## 初学者阅读建议

- 先看 generated content moderation，理解“模型生成后仍要先检查再展示或执行动作”。
- 再看 result 字段，把 `flagged` 当第一层信号，把 categories/scores 作为日志、人工复核和策略路由输入。
- 不要只写“接入 moderation 就安全”；要同时设计误报、漏报、人工复核、失败时降级和回归测试。

## 可复现实验

- 后续真实 prompt injection / permission harness 可增加 moderation-only、policy-enforced 和 HITL 对照，记录 `flagged`、categories、scores、误报、漏报、成本、延迟和人工复核负担。
- 后续 tool-calling 实验应验证 tool arguments / tool outputs 被 moderation 处理时，tool schema / tool name / tool description 仍需要独立审查。
- 后续 streaming 实验应记录 partial output 与最终 moderation score 到达时机之间的产品风险。

## 是否进入正文

- 结论：进入；moderation 作为检测信号和生产安全 workflow 一部分的边界可入正文。
- 原因：官方文档直接支撑 moderation 的输入/输出、结果字段、tool-calling 覆盖边界和 streaming 限制。仍需保守写明：它不证明具体阈值、策略、检测层或生产安全效果充分可靠。
