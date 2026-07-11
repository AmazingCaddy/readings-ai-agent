# OpenAI Graders Documentation

- 来源链接：https://developers.openai.com/api/docs/guides/graders.md
- 作者 / 机构：OpenAI
- 发布时间：持续更新 documentation
- 最后复核日期：2026-07-12
- 类型：Official Docs / Evaluation
- 主题：Graders / LLM-as-judge / Reward Hacking
- 适合阶段：工程实践
- 可信度等级：A
- 是否已验证：官方 Markdown 页面和 deprecations 页面返回 HTTP 200；关键段落已精读；grader 类型、tool-call grading、score model grader、Python grader、multigrader、reward hacking 和 deprecation 边界可入正文；标准库 grader misalignment / reward hacking audit 已完成；真实 grader 稳定性、成本、误判率和生产适用性仍部分验证

## 一句话总结

OpenAI Graders 文档适合用来理解自动评分器的形态、适用边界和风险：grader 可以帮助组织 eval，但不能替代人工真值和任务级验证。

## 核心结论

- 文档将 graders 定义为评估 model performance against reference answers 的方式，并可返回 0 到 1 的分数。
- 文档明确说明 OpenAI 正在 deprecating graders as part of the evals and fine-tuning workflows they support；deprecations 页面进一步说明 Evals platform 将在 2026-10-31 对既有用户变为 read-only，并计划在 2026-11-30 关闭，graders documented for eval workflows 属于该过渡。fine-tuning 相关时间线另见 self-serve fine-tuning 条目。因此具体 graders / Evals API workflow 不能被写成长期稳定实践入口。
- Grader 类型包括 string check、text similarity、score model grader、Python code execution 和 multigraders；当前文档同时说明 multigrader currently only used for reinforcement fine-tuning，不能泛化为所有 eval workflow 的默认组合方式。
- 对 tool-calling 行为，文档建议用 `sample.output_tools` 评分，并可分别检查 tool name 和 function arguments。
- 文档提醒 string check 可能因为细微格式差异 under-reward，例如 `1` 和 `1.0` 或缩写与完整州名；可考虑 text similarity 或 score model grader，但这仍需要验证。
- Score model grader 使用另一个 model 给输出打分；这属于 LLM-as-judge 的一种具体实现形态。
- Python grader 可以执行评分代码，但文档列出代码大小、无网络、运行时间、内存、磁盘和 CPU 限制。
- 文档明确提示 grader hacking / reward hacking：模型可能学会利用 grader 弱点，在 model grader eval 上高分但在人类专家评估中表现差。
- 文档建议构建 grader 时使用高质量 human expert answers、ground truth grades、edge cases，并持续迭代 grader prompt。

## 支撑证据

- `graders.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 17:54:17 GMT`；`content-type: text/markdown; charset=utf-8`。
- `deprecations.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 17:54:17 GMT`；Evals platform 条目写明 2026-10-31 read-only、2026-11-30 shutdown，并说明 eval workflow 的 graders 属于该过渡。
- 文档写明 graders compare reference answers to model-generated answer and return a grade in the range from 0 to 1。
- 文档列出 string check、text similarity、score model grader、Python code execution 和 multigraders，并标注 multigrader 当前只用于 reinforcement fine-tuning。
- 文档写明 grading tool calls 时需要让 grader operate over `sample.output_tools`，并给出 function name / arguments 两个子 grader 的示例。
- 文档写明 grader hacking / reward hacking 可通过对比 model grader evals 和 expert human evals 检测。
- 文档写明 designing and creating graders is an iterative process，并建议 start small、guard against reward hacking、avoid skewed data、在 code falls short 时使用 LLM-as-a-judge 并检查稳定性和偏好对齐。

## 可能的问题

- Graders 文档是官方文档，但它描述的 eval workflow 正在随 Evals platform 退役；本手册只能采用评分器设计和风险边界，不能把旧 API 写成长期路线。
- Grader 能返回分数，不表示分数等于真实质量。尤其是 LLM-as-judge 和 text similarity 对复杂任务可能误判。
- Python grader 有执行约束，也会带来评分代码质量、sandbox、依赖和可维护性问题。
- Reward hacking 是核心风险：自动评分器被优化目标利用时，表面分数可能上升，真实人工质量可能下降。

## 初学者阅读建议

- 先理解 string check / text similarity / score model / Python grader 各自适合什么类型的任务。
- 对工具型 Agent，重点看 `sample.output_tools`，理解为什么工具名称和参数都要评分。
- 不要一开始就用复杂 LLM judge。先用少量人工标注样例校准，再逐步自动化。

## 可复现实验

- 已完成标准库 trace-aware eval 模拟实验，证明 final-only scoring 会漏掉副作用工具和错误恢复问题。
- 已完成标准库 grader misalignment / reward hacking audit：string check、关键词式 judge、tool-call rule 和 majority multigrader 都会出现不同误报/漏报，reward-hacked 输出可骗过脆弱关键词 rubric。
- 后续应加入真实 grader 对照实验：规则 grader、真实 LLM-as-judge、Python grader 和人工评审在同一批 tool/RAG traces 上的误判、成本、延迟和人工复核比例。

## 是否进入正文

- 结论：进入；grader 类型、tool-call grading、LLM-as-judge / score model grader、Python grader 执行约束、multigrader 的 RFT-only 边界和 reward hacking 风险的窄边界可入正文。
- 原因：官方文档直接支撑 grader 形态和风险，但仍需真实实验验证 grader 稳定性、成本、误判率、人工校准比例和平台迁移路径。
