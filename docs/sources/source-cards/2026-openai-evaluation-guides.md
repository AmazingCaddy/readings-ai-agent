# OpenAI Evaluation Guides

- 来源链接：
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices.md
  - https://developers.openai.com/api/docs/guides/agent-evals.md
- 作者 / 机构：OpenAI
- 发布时间：持续更新 documentation
- 最后复核日期：2026-07-11
- 类型：Official Docs / Evaluation
- 主题：Evaluation / Agent Eval / Trace Grading / LLM-as-judge
- 适合阶段：工程实践
- 可信度等级：A
- 是否已验证：两个官方 Markdown 页面均返回 HTTP 200；关键段落已精读；eval process、trace grading、datasets/eval runs、LLM-as-judge caveats 和 Evals platform deprecation timeline 的窄边界可入正文；真实 grader / judge / platform 可靠性仍部分验证

## 一句话总结

OpenAI Evaluation Guides 适合用来理解如何为 LLM 应用和 Agent workflow 设计任务级 eval、trace grading、repeatable eval runs 和人工校准流程。

## 核心结论

- Evaluation best practices 将 eval 定义为应对生成式 AI 变动性的 structured tests，并强调传统软件测试不足以覆盖 AI architecture 的 nondeterminism。
- 文档明确区分行业 benchmark、通用数值指标和为具体 use case 实现的 eval，并说明该 guide 关注第三类：designing your own evals。
- 文档建议采用 eval-driven development、task-specific evals、logging、automated scoring 和 continuous evaluation，同时用 human feedback 校准自动评分。
- 文档列出 eval workflow：定义目标、收集 dataset、定义 metrics、运行并比较 eval、持续评估。
- 对 single-agent，文档把 tool selection 和 data precision 列为评测点；对 multi-agent，文档把 agent handoff accuracy 列为评测点，并说明是否采用 multi-agent architecture 应由 eval 驱动。
- Agent evals guide 建议调试阶段先从 traces 开始：trace 捕获 model calls、tool calls、guardrails 和 handoffs；trace grading 可用于发现 workflow-level regressions 和 failure modes。
- Agent evals guide 建议在知道“good”是什么之后，再迁移到 repeatable datasets 和 eval runs，用于 benchmark changes、compare prompts 或 larger-scale evaluation over time。
- Evaluation best practices 记录 OpenAI 正在 deprecating the Evals platform：existing evals content 在过渡期可用，2026-10-31 起对 existing users 只读，计划 2026-11-30 关闭。
- 文档说明 LLM-as-judge / model graders 更便宜、更可扩展，但会有 position bias、verbosity bias 等问题，必须和 human labels / human feedback 校准。

## 支撑证据

- `evaluation-best-practices.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 07:25:27 GMT`；`content-type: text/markdown; charset=utf-8`。
- `agent-evals.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:18:50 GMT`；`content-type: text/markdown; charset=utf-8`。
- Evaluation best practices 写明 evals are structured tests for measuring model performance，并强调 model output variability makes traditional software testing methods insufficient。
- Evaluation best practices 的 tips 包含 eval-driven development、task-specific evals、log everything、automate when possible、continuous process 和 maintain agreement with human feedback。
- Agent evals guide 写明 trace captures the end-to-end record of model calls, tool calls, guardrails, and handoffs for one run。
- Agent evals guide 列出 trace grading 可回答 right tool、handoff、instruction/safety policy violation、prompt/routing improvement 等问题。

## 可能的问题

- OpenAI Evals platform 正在退役；学习时要区分“eval 设计原则”和“某个具体平台/产品入口”。
- 文档可以支撑 eval 流程和 trace grading 形态，但不证明任一 grader、judge model、trace 平台或 metric 在具体业务中可靠。
- 文档中的示例指标和推荐模型会随时间变化；引用时应记录复核日期，不应把示例阈值写成通用标准。

## 初学者阅读建议

- 先读 Evaluation best practices，理解为什么 eval 要绑定具体任务和数据集。
- 再读 Agent evals，重点看 trace grading 和 datasets/eval runs 的分工。
- 暂时不要纠结平台按钮和 API 细节；先学会写清楚任务、成功标准、trace 字段、失败分类和人工复核方法。

## 可复现实验

- 已完成标准库 trace-aware eval 模拟实验，比较 final-only 与 trace-aware scoring 能发现的错误类型。
- 已完成标准库 trace schema audit，验证不同用途需要不同 trace 字段。
- 已准备真实模型 trace-aware eval harness，但尚未运行；后续应将 trace grading、dataset eval、LLM-as-judge 和人工抽样复核放到同一实验记录中。

## 是否进入正文

- 结论：进入；eval 流程、trace grading、dataset/eval run 分工、LLM-as-judge 校准和 Evals platform deprecation 的窄边界可入正文。
- 原因：官方文档直接支撑 Agent eval 需要覆盖 tool selection、data precision、handoff accuracy、instruction/safety policy violation、trace、dataset 和 continuous evaluation。仍需保守写明：这些资料不证明自动评分器、LLM judge、平台默认 trace 或具体指标在真实业务中可靠。
