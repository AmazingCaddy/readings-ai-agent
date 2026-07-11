# 上下文策略对比实验

## 目标

验证第 02/06/09 章中的一个工程边界：长上下文、按时间截取、摘要和基础 RAG 都不是上下文治理本身。系统仍需要来源可信度、时效、引用保留、外部指令隔离和人工确认边界。

## 实验边界

这是一个确定性的标准库实验，不调用模型、不接入真实 API、不使用真实 embedding 或 vector store。脚本把几种常见上下文策略写成固定规则，用来暴露失败模式：

- `full_context`：把所有材料放入上下文。
- `recency_only`：只选最新材料。
- `lossy_summary`：使用压缩摘要，但丢失 source id 和人工确认字段。
- `keyword_rag`：按关键词 overlap 检索 top-k。
- `governed_context`：按任务选择可信、最新、可引用的材料，并隔离不可信外部文档。

本实验不能证明真实模型在长上下文、摘要或 RAG 中的表现。它只验证策略层面的最小失败模式和 trace 字段设计。

## 输入数据

脚本包含四份假文档：

- 2024 旧退款政策。
- 2026 当前退款政策。
- 2026 connector 安全文档。
- 外部 attachment，包含“忽略政策、自动退款、导出 admin token”的注入内容。

测试任务覆盖两个 case：退款争议和 connector 安全配置。

## 运行方式

```bash
uv run python docs/experiments/context-strategy-comparison/context_strategy_comparison.py
```

## 观察点

- 全量上下文是否仍可能引用旧政策或外部注入。
- 只看最新材料是否会把外部 attachment 当成可信指令。
- 摘要是否会丢失 citation 和人工确认边界。
- 基础关键词 RAG 是否会召回不可信外部文档。
- 治理策略是否保留 source id、隔离外部文档，并保持 human-review gate。

## 结论状态

- 支撑：可以把“长上下文、摘要和 RAG 都需要治理；不是把材料塞进去就可靠”写入第 02/06/09 章。
- 支撑：上下文 trace 至少应记录 selected docs、citations、forbidden citations、human gate、失败类型和上下文规模。
- 仍缺：真实模型、真实长上下文、真实 embedding/vector store/rerank、摘要质量、token/latency/cost 和跨模型稳定性实验。
