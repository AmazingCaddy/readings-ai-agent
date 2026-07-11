# RAG、短期记忆与长期记忆对比实验

## 目标

验证第 06 章的术语边界：RAG、thread-scoped short-term memory 和 guarded long-term memory 都能给模型补上下文，但它们适合解决的问题不同，风险也不同。

## 实验边界

这是一个确定性的 Python 标准库实验，不调用模型、不使用 embedding、不接入 vector store 或真实 memory framework。它不能证明真实 RAG 或真实长期记忆系统的质量，只验证最小任务分流、trace 和风险字段设计。

## 输入数据

实验包含三类上下文来源：

- RAG documents：`rag_paper`、`langgraph_memory`、`memory_governance`。
- Thread state：当前主题、当前语言、本轮已完成步骤。
- Long-term memory：用户确认的语言偏好、被失效的助手猜测、用户纠正后的站点技术栈。

实验包含 5 个 case：

- 外部知识和 citation。
- 当前会话进度。
- 跨会话语言偏好。
- 过时/冲突记忆纠正。
- 敏感且未确认的信息请求。

## 运行方式

```bash
uv run python docs/experiments/rag-memory-comparison/rag_memory_comparison.py
```

## 观察点

- RAG 是否只在有外部资料证据时回答，并带 citation。
- Short-term memory 是否只服务当前 thread/task state。
- Long-term memory 是否只使用用户确认或用户纠正的 active memory。
- Invalidated memory 是否被跳过。
- 无安全上下文来源时是否拒答。

## 结论状态

- 支撑：RAG 偏外部知识和 provenance；短期记忆偏当前任务状态；长期记忆偏跨会话偏好/事实，但需要写入守门、失效和用户纠正。
- 支撑：RAG、短期记忆和长期记忆应在 trace 中区分来源、citation、personalization 和风险。
- 仍缺：真实 embedding / vector store / LLM synthesis、真实 memory framework、真实多会话质量提升、token/latency/cost 和隐私权限实验。
