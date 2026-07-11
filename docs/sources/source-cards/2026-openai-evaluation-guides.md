# OpenAI Evaluation Guides

- 来源链接：
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices.md
  - https://developers.openai.com/api/docs/guides/agent-evals.md
- 作者 / 机构：OpenAI
- 发布时间：持续更新 documentation
- 最后复核日期：2026-07-12
- 类型：Official Docs / Evaluation
- 主题：Evaluation / Agent Eval / Trace Grading / LLM-as-judge
- 适合阶段：工程实践
- 可信度等级：A
- 是否已验证：Evaluation best practices、Agent evals 和 deprecations 官方 Markdown 页面已于 2026-07-12 复核，均返回 HTTP 200；关键段落已精读；eval process、trace grading、datasets/eval runs、tool/data/handoff 评测点、LLM-as-judge caveats、edge cases、human-label calibration 和 Evals platform deprecation timeline 的窄边界可入正文；标准库 grader misalignment / reward hacking audit 和 Real Trace-Aware Eval 本地 scorer control 已完成；真实 grader / judge / platform 可靠性仍部分验证

## 一句话总结

OpenAI Evaluation Guides 适合用来理解如何为 LLM 应用和 Agent workflow 设计任务级 eval、trace grading、repeatable eval runs 和人工校准流程。

## 核心结论

- Evaluation best practices 将 eval 定义为应对生成式 AI 变动性的 structured tests，并强调传统软件测试不足以覆盖 AI architecture 的 nondeterminism。
- 文档明确区分行业 benchmark、通用数值指标和为具体 use case 实现的 eval，并说明该 guide 关注第三类：designing your own evals。
- 文档建议采用 eval-driven development、task-specific evals、logging、automated scoring 和 continuous evaluation，同时用 human feedback 校准自动评分。
- 文档列出 eval workflow：定义目标、收集 dataset、定义 metrics、运行并比较 eval、持续评估。
- 对 single-agent，文档把 tool selection 和 data precision 列为评测点；对 multi-agent，文档把 agent handoff accuracy 列为评测点，并说明是否采用 multi-agent architecture 应由 eval 驱动。
- 文档明确建议 eval 数据覆盖 typical cases、edge cases 和 adversarial cases，并提示 real-world AI systems 会遇到 input variability、contextual complexity、long-running conversations、multiple tool calls、circular handoffs 和 system-prompt conflict 等边界。
- Agent evals guide 建议调试阶段先从 traces 开始：trace 捕获 model calls、tool calls、guardrails 和 handoffs；trace grading 可用于发现 workflow-level regressions 和 failure modes。
- Agent evals guide 建议在知道“good”是什么之后，再迁移到 repeatable datasets 和 eval runs，用于 benchmark changes、compare prompts 或 larger-scale evaluation over time。
- Evaluation best practices 记录 OpenAI 正在 deprecating the Evals platform：existing evals content 在过渡期可用，2026-10-31 起对 existing users 只读，计划 2026-11-30 关闭。
- 文档说明 LLM-as-judge / model graders 更便宜、更可扩展，但会有 position bias、verbosity bias 等问题，必须和 human labels / human feedback 校准；文档中对 `gpt-5.6` 的 judge / test-data 例子只能作为当前官方示例，不能替代项目自己的模型、成本和人工校准实验。

## 支撑证据

- 2026-07-12 使用 `curl -L -I https://developers.openai.com/api/docs/guides/evaluation-best-practices.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 17:54:17 GMT`。
- 2026-07-12 使用 `curl -L -I https://developers.openai.com/api/docs/guides/agent-evals.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 17:54:17 GMT`。
- 2026-07-12 使用 `curl -L -I https://developers.openai.com/api/docs/deprecations.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 17:54:17 GMT`。
- Evaluation best practices 写明 evals are structured tests for measuring model performance，并强调 model output variability makes traditional software testing methods insufficient。
- Evaluation best practices 的 tips 包含 eval-driven development、task-specific evals、log everything、automate when possible、continuous process 和 maintain agreement with human feedback。
- Evaluation best practices 写明 test data 应包含 typical cases、edge cases 和 adversarial cases，并列出 input variability、contextual complexity、multiple tool calls、multiple/circular handoffs、jailbreak attempts 和 system prompt conflicts 等 edge-case 类型。
- Evaluation best practices 的 LLM-as-judge 段落写明 judge 更便宜、更可扩展，但有 position bias 和 verbosity bias；应先验证与 human labels 的 agreement，再优化 cost 或 latency。
- Agent evals guide 写明 trace captures the end-to-end record of model calls, tool calls, guardrails, and handoffs for one run。
- Agent evals guide 列出 trace grading 可回答 right tool、handoff、instruction/safety policy violation、prompt/routing improvement 等问题。
- Deprecations 页面 `2026-06-03: Evals platform` 段落写明 2026-10-31 existing evals become read-only，2026-11-30 Evals dashboard and API are scheduled to shut down，并说明 graders documented for eval workflows are part of this transition。

## 可能的问题

- OpenAI Evals platform 正在退役；学习时要区分“eval 设计原则”和“某个具体平台/产品入口”。
- 文档可以支撑 eval 流程和 trace grading 形态，但不证明任一 grader、judge model、trace 平台或 metric 在具体业务中可靠。
- 文档中的示例指标、推荐模型和 dashboard/API 入口会随时间变化；引用时应记录复核日期，不应把示例阈值、`gpt-5.6` 示例或旧 Evals API 路线写成通用标准。

## 初学者阅读建议

- 先读 Evaluation best practices，理解为什么 eval 要绑定具体任务和数据集。
- 再读 Agent evals，重点看 trace grading 和 datasets/eval runs 的分工。
- 暂时不要纠结平台按钮和 API 细节；先学会写清楚任务、成功标准、trace 字段、失败分类和人工复核方法。

## 可复现实验

- 已完成标准库 trace-aware eval 模拟实验，比较 final-only 与 trace-aware scoring 能发现的错误类型。
- 已完成标准库 trace schema audit，验证不同用途需要不同 trace 字段。
- 已完成标准库 grader misalignment / reward hacking audit，验证自动评分器需要 edge cases、误判统计和人工校准。
- Real Trace-Aware Eval harness 已完成本地 deterministic scorer control，但当前无 API key，真实模型 trace 未运行；后续应将 trace grading、dataset eval、真实 LLM-as-judge、edge-case suite、成本/延迟和人工抽样复核放到同一实验记录中。

## 是否进入正文

- 结论：进入；eval 流程、trace grading、dataset/eval run 分工、typical / edge / adversarial case 设计、LLM-as-judge human-label 校准和 Evals platform deprecation 的窄边界可入正文。
- 原因：官方文档直接支撑 Agent eval 需要覆盖 tool selection、data precision、handoff accuracy、instruction/safety policy violation、multiple tool calls、circular handoffs、system-prompt conflict、trace、dataset、human feedback calibration 和 continuous evaluation。仍需保守写明：这些资料不证明自动评分器、LLM judge、平台默认 trace 或具体指标在真实业务中可靠。
