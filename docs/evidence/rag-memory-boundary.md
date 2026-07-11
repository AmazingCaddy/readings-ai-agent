# Evidence Note: RAG 与 Memory 边界

## 要验证的结论

RAG 和 Memory 都能给模型补充上下文，但它们解决的问题不同：RAG 主要围绕外部知识检索、provenance 和知识更新；Agent memory 主要围绕会话状态、跨会话用户/应用数据、写入策略、召回范围、冲突和治理。

## 资料来源

- Source 1：[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](../sources/source-cards/2020-rag-paper.md)
- Source 2：[LangGraph Memory Documentation](../sources/source-cards/2026-langgraph-memory-docs.md)
- Source 3：[MemGPT: Towards LLMs as Operating Systems](../sources/source-cards/2023-memgpt-paper.md)
- Source 4：[RAG、短期记忆与长期记忆对比实验结果](../experiments/rag-memory-comparison/results-2026-07-11.md)
- Source 5：[长期记忆写入守门与治理实验结果](../experiments/memory-governance/results-2026-07-11.md)

## 交叉验证结果

- 一致点：RAG paper 摘要把 RAG 描述为结合 parametric memory 和 explicit non-parametric memory 的生成模型，并用 Wikipedia dense vector index 作为 non-parametric memory。
- 一致点：RAG paper 的动机包括知识密集任务、provenance 和 world knowledge 更新；这支持“RAG 更像外部资料检索与引用”的入门解释。
- 一致点：LangGraph memory docs 按 recall scope 区分 short-term/thread-scoped memory 和 long-term/cross-session memory；这支持“Memory 更像状态和历史经验管理”的入门解释。
- 一致点：LangGraph memory docs 明确 long-term memory 没有 one-size-fits-all solution，且写入可在 hot path 或 background 中发生；这支持“Memory 治理重点在写入、更新、召回和风险”的表述。
- 分歧点：RAG paper 使用 non-parametric memory 术语描述外部检索索引；工程 Agent 语境中的 long-term memory 往往指跨会话用户/应用数据。两者都叫 memory，但语义层级不同。
- 可能原因：RAG 论文来自模型架构/检索增强生成研究，LangGraph memory 文档来自 agent 应用状态和持久化工程实践。
- 本地实验：标准库 RAG / Memory 对比实验中，外部知识问题由 RAG 回答并带 citation；当前任务进度由 short-term memory 回答；跨会话偏好和用户纠正事实由 guarded long-term memory 回答；敏感未确认问题没有安全上下文来源并拒答。这支持“RAG、短期状态和长期记忆应按来源、生命周期、citation、personalization 和风险分层治理”。

## 实验验证

- 是否需要实验：是
- 实验设计：用同一学习助手任务分别实现三个 baseline：只用 RAG 文档库、只用 thread-scoped short-term memory、加入用户显式确认的 long-term memory。比较引用正确率、个性化准确性、误写入和过时信息风险。
- 结果：已完成标准库最小对比实验。真实 embedding / vector store / LLM synthesis、真实 memory framework、多会话质量、token/latency/cost 和隐私权限仍待验证。

## 结论状态

- 可入正文：窄结论“RAG 偏外部知识检索、provenance 和知识更新；Agent memory 偏会话状态、跨会话数据和治理；RAG paper 中的 non-parametric memory 不应直接等同于 Agent long-term memory”由 RAG paper、LangGraph memory docs 和标准库 RAG / Memory 对比实验共同支撑。
- 部分验证：真实 RAG / memory framework 的质量、成本、隐私、长期收益和多会话污染风险仍待验证。

## 可进入章节

- 是。可以写成：RAG 偏外部知识检索和 provenance，Memory 偏状态、历史经验和跨会话数据治理；不要把 RAG paper 中的 non-parametric memory 和 Agent long-term memory 混为一谈。
