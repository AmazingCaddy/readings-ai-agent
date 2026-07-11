# Arize Phoenix Documentation

- 来源链接：https://arize.com/docs/phoenix
- 补充链接：https://arize.com/docs/phoenix/tracing/tutorial
- 作者 / 机构：Arize AI / Phoenix open-source community
- 发布时间：持续更新文档
- 最后复核日期：2026-07-12
- 类型：Framework / Observability Docs
- 主题：AI Observability / Evaluation / Tracing / Experiments
- 适合阶段：工程实践
- 可信度等级：B
- 是否已验证：Overview 与 Tracing Tutorial Markdown 页面已于 2026-07-12 复核，均返回 HTTP 200；关键段落已精读；已结合 LangSmith / OpenAI Evals、trace-aware eval、trace schema audit 和 grader audit 标准库实验将 trace 作为 eval/审计/回归输入和 trace 字段用途设计的窄边界升级为可入正文；真实平台字段映射、Phoenix UI / PXI 行为、LLM-as-judge 和自动评分仍部分验证

## 一句话总结

Phoenix 文档适合学习 AI 应用 tracing、evaluations、datasets/experiments、prompt iteration 和 sessions 的工程形态。

## 核心结论

- Phoenix overview 将 Phoenix 定位为帮助理解和改进 AI applications 的 observability/evaluation workflow。
- Overview 写明可以发送 traces，查看一次 run 中发生了什么，使用 evaluation tests 识别 failures/regressions，用 real production examples 迭代 prompts，并用 experiments 比较相同输入上的改动。
- Overview 写明 Phoenix 基于 OpenTelemetry，并由 OpenInference instrumentation 支撑。
- Tracing 功能说明 trace 捕获 model calls、retrieval、tool use 和 custom logic，用于 debug behavior 和理解 time spent。
- Overview 写明 Phoenix 通过 OTLP 接收 traces，并提供 LlamaIndex、LangChain、DSPy、Mastra、Vercel AI SDK、OpenAI、Bedrock、Anthropic 等框架 / provider 的 auto-instrumentation 入口；这支撑集成形态，不证明默认字段完备。
- Evaluation 功能说明可以用 LLM-based evaluators、code-based checks 或 human labels 给 traces/spans 打分，用于持续识别 failures。
- Datasets & Experiments 功能说明可将 traces 分组为 datasets，用不同版本重新运行并比较 evaluation results。
- Prompt iteration 功能说明可 version prompts、在 datasets 上测试 variants，并 replay LLM calls；这支撑 prompt/version/experiment 工作流，不证明某个 prompt 改动实际变好。
- Tracing Tutorial 明确 AI agent 失败可能发生在 reasoning、retrieval、tool calls、generation 等链路中，因此需要捕获 LLM call、tool execution、retrieval operation、generation 及其 inputs、outputs、latency、token usage。
- Tutorial 还覆盖 annotations/evaluation 和 sessions：用 human feedback、LLM-as-judge、aggregate metrics 和 session tracking 分析对话质量。
- Tutorial 明确 trace 显示 `200 OK` 不代表答案正确；需要 annotations/evaluation 才能衡量 response quality，这支撑 trace 与质量评估分层的边界。

## 支撑证据

- 2026-07-12 使用 `curl -L -I https://arize.com/docs/phoenix.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 21:12:58 GMT`。
- 2026-07-12 使用 `curl -L -I https://arize.com/docs/phoenix/tracing/tutorial.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 21:12:58 GMT`。
- `https://arize.com/docs/phoenix.md` 返回 Markdown 内容并包含 “AI Observability and Evaluation”。
- Overview 写明 Phoenix built on top of OpenTelemetry and powered by OpenInference instrumentation。
- Overview Tracing 小节写明 trace captures model calls, retrieval, tool use, and custom logic。
- Overview Evaluation 小节写明可以 score traces & spans with LLM-based evaluators, code-based checks, or human labels。
- Overview Datasets & Experiments 小节写明可以 group traces into datasets、rerun through different versions、compare evaluation results。
- Overview Prompt iteration 小节写明可以 version prompts、test variants across datasets 和 replay calls。
- `https://arize.com/docs/phoenix/tracing/tutorial.md` 返回 Markdown 内容并包含 “trace every operation, measure quality, and debug conversations”。
- Tracing Tutorial 写明 observability means capturing every LLM call, tool execution, retrieval operation, and generation, along with inputs, outputs, latency, and token usage。
- Tracing Tutorial 写明 “A trace showing `200 OK` doesn't mean the answer was right”，并把 human feedback、user reactions、LLM-as-Judge、aggregate metrics 和 session tracking 放在质量分析流程中。

## 可能的问题

- Phoenix 是特定平台/开源项目文档，可能突出产品能力；不能把它写成唯一或默认方案。
- Tutorial 中的 agent 是示例项目，不能单独证明所有生产 Agent 都应采用同样技术栈。
- LLM-as-judge、human feedback 和 session metrics 的质量仍需真实任务验证和抽样人工复核。
- Auto-instrumentation、OTLP、OpenTelemetry/OpenInference 只能支撑集成与语义形态；真实字段覆盖、脱敏、保留策略、成本和 UI 操作仍需平台实测。

## 初学者阅读建议

- 先读 Overview 理解 tracing/evaluation/datasets/experiments 的关系，再读 Tracing Tutorial 里的 “Your First Traces” 和 “Annotations and Evaluation”。

## 可复现实验

- 已完成标准库 trace-aware eval 最小实验和 Real Trace-Aware Eval 本地 scorer control；后者记录 tool call/result/error/approval/final response 并比较 final-only 与 trace-aware scoring，当前无 API key，真实模型 trace 未运行；后续仍需扩展为真实客服/RAG/tool traces，记录 LLM call、tool execution、retrieval、latency、token usage、session id，并做 Phoenix 平台对照。
- 已完成标准库 trace schema audit，验证 debug、audit、regression、cost/latency、RAG 和 privacy 用途需要不同字段；该结果支撑“字段要按用途设计”的窄边界，后续仍需映射到真实 Phoenix traces/spans/datasets/experiments/sessions/annotations 字段。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 trace 字段、OpenTelemetry/OpenInference、traces/spans、evaluation、datasets/experiments、prompt replay 和 sessions 的工程实践，并与 trace-aware eval / trace schema audit / grader audit 实验共同支撑“trace 不只是 debug 日志，也是工具/副作用 Agent 的 eval、审计和回归输入”以及“trace 字段要按用途设计”的窄结论；不能证明平台默认最优、默认字段完备、LLM-as-judge 准确或 prompt 改动实际有效。
