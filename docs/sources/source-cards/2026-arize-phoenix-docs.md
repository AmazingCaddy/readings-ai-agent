# Arize Phoenix Documentation

- 来源链接：https://arize.com/docs/phoenix
- 补充链接：https://arize.com/docs/phoenix/tracing/tutorial
- 作者 / 机构：Arize AI / Phoenix open-source community
- 发布时间：持续更新文档
- 最后复核日期：2026-07-11
- 类型：Framework / Observability Docs
- 主题：AI Observability / Evaluation / Tracing / Experiments
- 适合阶段：工程实践
- 可信度等级：B
- 是否已验证：Overview 与 Tracing Tutorial Markdown 页面已复核；关键段落已精读；已结合 LangSmith / OpenAI Evals、trace-aware eval 和 trace schema audit 标准库实验完成部分验证

## 一句话总结

Phoenix 文档适合学习 AI 应用 tracing、evaluations、datasets/experiments、prompt iteration 和 sessions 的工程形态。

## 核心结论

- Phoenix overview 将 Phoenix 定位为帮助理解和改进 AI applications 的 observability/evaluation workflow。
- Overview 写明可以发送 traces，查看一次 run 中发生了什么，使用 evaluation tests 识别 failures/regressions，用 real production examples 迭代 prompts，并用 experiments 比较相同输入上的改动。
- Overview 写明 Phoenix 基于 OpenTelemetry，并由 OpenInference instrumentation 支撑。
- Tracing 功能说明 trace 捕获 model calls、retrieval、tool use 和 custom logic，用于 debug behavior 和理解 time spent。
- Evaluation 功能说明可以用 LLM-based evaluators、code-based checks 或 human labels 给 traces/spans 打分，用于持续识别 failures。
- Datasets & Experiments 功能说明可将 traces 分组为 datasets，用不同版本重新运行并比较 evaluation results。
- Tracing Tutorial 明确 AI agent 失败可能发生在 reasoning、retrieval、tool calls、generation 等链路中，因此需要捕获 LLM call、tool execution、retrieval operation、generation 及其 inputs、outputs、latency、token usage。
- Tutorial 还覆盖 annotations/evaluation 和 sessions：用 human feedback、LLM-as-judge、aggregate metrics 和 session tracking 分析对话质量。

## 支撑证据

- `https://arize.com/docs/phoenix.md` 返回 Markdown 内容并包含 “AI Observability and Evaluation”。
- Overview 写明 Phoenix built on top of OpenTelemetry and powered by OpenInference instrumentation。
- Overview Tracing 小节写明 trace captures model calls, retrieval, tool use, and custom logic。
- Overview Evaluation 小节写明可以 score traces & spans with LLM-based evaluators, code-based checks, or human labels。
- `https://arize.com/docs/phoenix/tracing/tutorial.md` 返回 Markdown 内容并包含 “trace every operation, measure quality, and debug conversations”。
- Tracing Tutorial 写明 observability means capturing every LLM call, tool execution, retrieval operation, and generation, along with inputs, outputs, latency, and token usage。

## 可能的问题

- Phoenix 是特定平台/开源项目文档，可能突出产品能力；不能把它写成唯一或默认方案。
- Tutorial 中的 agent 是示例项目，不能单独证明所有生产 Agent 都应采用同样技术栈。
- LLM-as-judge、human feedback 和 session metrics 的质量仍需真实任务验证和抽样人工复核。

## 初学者阅读建议

- 先读 Overview 理解 tracing/evaluation/datasets/experiments 的关系，再读 Tracing Tutorial 里的 “Your First Traces” 和 “Annotations and Evaluation”。

## 可复现实验

- 已完成标准库 trace-aware eval 最小实验；已准备真实模型 trace-aware eval harness，可记录 tool call/result/error/approval/final response 并比较 final-only 与 trace-aware scoring；后续仍需扩展为真实客服/RAG/tool traces，记录 LLM call、tool execution、retrieval、latency、token usage、session id，并做 Phoenix 平台对照。
- 已完成标准库 trace schema audit，验证 debug、audit、regression、cost/latency、RAG 和 privacy 用途需要不同字段；后续仍需映射到真实 Phoenix traces/spans/datasets/experiments 字段。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 trace 字段、OpenTelemetry/OpenInference、traces/spans、evaluation 和 sessions 的工程实践；不能证明平台默认最优。
