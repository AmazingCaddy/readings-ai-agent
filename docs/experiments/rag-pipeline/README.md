# RAG 最小 Pipeline 与 Citation 实验

## 目标

验证手册第 06 章中的工程边界：RAG 不是把整篇文档塞进 prompt，而是把文档加载为 chunk，保留 source metadata，检索相关 chunk，用检索证据合成回答，并在没有证据时保守拒答。

## 实验边界

这是一个确定性的标准库实验。脚本使用关键词 overlap 做检索，不使用 embedding、向量数据库、reranker、LLM 或 LlamaIndex。

本实验不能证明真实 RAG 系统的召回率、faithfulness、latency、token cost 或某个 chunk size 最优。它只验证最小 pipeline、citation 字段和 unsupported question 处理是否自洽。

## 输入数据

脚本内置 3 个小型文档：

- `rag-paper`：RAG paper source card 摘要笔记。
- `llamaindex-rag`：LlamaIndex RAG overview source card 摘要笔记。
- `langgraph-memory`：LangGraph memory source card 摘要笔记。

每个文档带有：`source_id`、`title`、`url`、`text`。

## 运行方式

```bash
uv run python docs/experiments/rag-pipeline/rag_pipeline_simulation.py
```

## 观察点

- `chunk` 阶段是否记录文档数、chunk 数和 chunk size。
- `retrieve` 阶段是否记录 query terms、selected chunks、score 和 matched terms。
- `synthesize` 阶段是否输出 citations，并把每条 citation 绑定到 `chunk_id`、`source_id`、`title`、`url`。
- unsupported question 是否返回 `grounded=false` 和空 citations。

## 结论状态

- 支撑：可以把“最小 RAG 应保留 source metadata、输出 citations、记录检索 trace、无证据时拒答”写入第 06 章。
- 仍缺：真实 embedding / vector store / rerank / LLM synthesis 实验，chunk size 对比，citation correctness 评测和 token/latency 记录。
