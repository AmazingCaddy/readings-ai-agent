# Real Framework Same-Task Comparison

## 目标

用同一个本地确定性任务对比 LangGraph、LlamaIndex 和 Semantic Kernel 的真实 Python runtime surface：读取退款政策、阻断未审批退款、执行一次已审批退款，并记录脱敏 trace。

这个实验补强第 10 章“框架应按任务难点和能力边界比较”的证据。它不是框架排行榜。

## 实验边界

本实验不调用模型，不记录 token/cost/latency，不验证 hosted tracing、真实权限 UI、部署式恢复、真实模型 tool selection 或生产安全。

重要边界：同一个任务在不同框架中可以跑通，但跑通的能力不一定都是框架原生能力。本实验明确区分：

- framework-owned capabilities：框架 runtime 直接提供的表面，例如 `StateGraph`、retriever source nodes、kernel function metadata。
- application-owned capabilities：实验代码自己实现的部分，例如审批 policy、trust filter、side effect、trace redaction。

## 运行方式

完整 3 框架对比：

```bash
uv run --with langgraph --with llama-index-core --with semantic-kernel python docs/experiments/real-framework-same-task-comparison/real_framework_same_task_comparison.py
```

如果缺少某个依赖，对应 adapter 会返回 `skipped`，其他 adapter 仍可运行。

## 观察点

- LangGraph 是否能把同一任务表达为 state graph、node 和 conditional edge。
- LlamaIndex 是否能把同一任务中的文档检索部分表达为 `VectorStoreIndex` / retriever / source-node metadata。
- Semantic Kernel 是否能把同一任务表达为 native plugin functions 和 `Kernel.invoke()`。
- 未审批退款是否不会产生 side effect。
- 已审批退款是否只产生一次 side effect。
- untrusted 文档是否不会进入 citations。
- trace 是否不会泄露示例 secret marker。

## 结论状态

- 当前状态：已完成 LangGraph 1.2.9、LlamaIndex Core 0.14.23、Semantic Kernel 1.36.0 的本地同任务 run。
- 可支撑：同一任务可以拆成框架原生 runtime surface 与应用层治理代码两部分观察；框架比较应记录 native surface、framework-owned capabilities、application-owned capabilities、trace 和失败边界。
- 不能支撑：不能证明任一框架默认更好、更安全、更便宜、更快，也不能证明真实模型 tool selection、真实 RAG answer quality、真实 HITL UI、部署恢复、hosted tracing 或生产可靠性。
