# LangSmith Documentation

- 来源链接：https://docs.langchain.com/langsmith/observability
- 补充链接：https://docs.langchain.com/langsmith/evaluation-concepts
- 作者 / 机构：LangChain
- 发布时间：持续更新文档
- 最后复核日期：2026-07-12
- 类型：Framework / Observability Docs
- 主题：Observability / Evaluation / Tracing
- 适合阶段：工程实践
- 可信度等级：B
- 是否已验证：Observability 与 Evaluation concepts Markdown 页面已于 2026-07-12 复核，均返回 HTTP 200；关键段落已精读；已结合 Phoenix / OpenAI Evals、trace-aware eval、trace schema audit 和 grader audit 标准库实验将 trace 作为 eval/审计/回归输入和 trace 字段用途设计的窄边界升级为可入正文；真实平台字段映射、在线 evaluator 表现、LLM-as-judge 和人工复核流程仍部分验证

## 一句话总结

LangSmith 文档适合学习 LLM/Agent 应用的 tracing、offline eval、online eval、datasets、experiments 和 human feedback 工作流。

## 核心结论

- Observability 页面将 LangSmith 定位为给 LLM 应用提供从 individual traces 到 production-wide performance metrics 的可见性。
- Observability 页面覆盖 set up tracing、trace a RAG application、view traces、monitor performance、configure automations 和 collect feedback。
- Evaluation concepts 页面建议先识别关键组件，例如 LLM calls、retrieval steps、tool invocations、output formatting，并为每个组件定义质量标准。
- Evaluation concepts 页面建议从 5-10 个手工整理的“good” examples 开始，作为 ground truth 和评测方法选择依据。
- 文档区分 offline evaluations 和 online evaluations：offline 用于 pre-deployment testing、benchmarking、regression testing、unit testing 和 backtesting；online 用于 production monitoring、anomaly detection 和 production feedback。
- 文档把 offline evaluation 的目标定义为 datasets/examples，把 online evaluation 的目标定义为 production runs/threads；run 包含 inputs、outputs、intermediate steps、metadata、feedback、latency 等信息。
- 文档列出 Human、Code、LLM-as-judge、Pairwise 等 evaluator 类型，并提醒 LLM-as-judge 需要仔细 review scores 和 prompt tuning。
- 文档说明 examples 可包含 inputs、optional reference outputs 和 metadata；experiments 捕获 dataset 上每个 example 的 outputs、evaluator scores 和 execution traces。
- 文档说明 online evaluators 在没有 reference outputs 的 runs/threads 上工作，因此更偏向 quality patterns、safety、real-world behavior、heuristics 和 anomaly detection，而不是直接判定标准答案正确性。
- 文档说明 annotation queues 可收集 human feedback、配置 reviewers，并把 annotated runs 导出为 datasets；这支撑“人工复核样例可回流离线回归集”的工作流边界。

## 支撑证据

- 2026-07-12 使用 `curl -L -I https://docs.langchain.com/langsmith/observability.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 21:12:59 GMT`。
- 2026-07-12 使用 `curl -L -I https://docs.langchain.com/langsmith/evaluation-concepts.md` 复核，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`last-modified: Sat, 11 Jul 2026 21:12:58 GMT`。
- `https://docs.langchain.com/langsmith/observability.md` 返回 Markdown 内容并包含页面描述：Instrument your LLM application, investigate traces, and monitor performance in production with LangSmith。
- Observability 页面写明 LangSmith Observability provides full visibility into your LLM application: from individual traces to production-wide performance metrics。
- `https://docs.langchain.com/langsmith/evaluation-concepts.md` 返回 Markdown 内容并包含 offline/online evaluations、datasets、runs、threads、evaluators 等关键段落。
- Evaluation concepts 页面写明 offline evaluations target examples from datasets；online evaluations target runs and threads from tracing。
- Evaluation concepts 页面写明 run contains inputs、outputs、intermediate steps、metadata 等。
- Evaluation concepts 页面写明 each experiment captures outputs, evaluator scores, and execution traces for every example in the dataset。
- Evaluation concepts 页面写明 online evaluators must assess quality without knowing the correct answer，依赖 quality heuristics、safety checks 和 reference-free evaluation techniques。
- Evaluation concepts 页面写明 annotation queues 支持 structured collection of human feedback、multiple reviewers、reservations 和 exporting annotated runs directly to datasets。

## 可能的问题

- LangSmith 是 LangChain 生态产品文档，可能偏产品能力介绍；不能把它写成行业通用标准。
- 文档能支撑 eval/observability workflow，但不能证明某个 evaluator 或平台默认最优。
- LLM-as-judge、online evaluation 和自动化规则仍需要在真实任务中校验误判率、成本和隐私边界。
- Online evaluation 无 reference output 时更适合监控模式、异常和安全信号；不能把 online evaluator 分数直接写成业务正确性真值。

## 初学者阅读建议

- 先读 Evaluation concepts，理解 offline vs online、dataset、run、evaluator，再看具体平台操作。

## 可复现实验

- 已完成标准库 trace-aware eval 最小实验和 Real Trace-Aware Eval 本地 scorer control；后者记录 tool call/result/error/approval/final response 并比较 final-only 与 trace-aware scoring，当前无 API key，真实模型 trace 未运行；后续仍需扩展为真实 RAG/tool-calling traces、LLM-as-judge、人工抽样复核和 LangSmith 平台对照。
- 已完成标准库 trace schema audit，验证 debug、audit、regression、cost/latency、RAG 和 privacy 用途需要不同字段；该结果支撑“字段要按用途设计”的窄边界，后续仍需映射到真实 LangSmith runs/threads/datasets/evaluators/annotation queues 字段。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 observability、offline/online eval、datasets、experiments、runs/threads、human feedback 和 evaluator 工程流程，并与 trace-aware eval / trace schema audit / grader audit 实验共同支撑“trace 不只是 debug 日志，也是工具/副作用 Agent 的 eval、审计和回归输入”以及“trace 字段要按用途设计”的窄结论；不应作为唯一平台推荐、online evaluator 业务正确性或自动评分正确性的证明。
