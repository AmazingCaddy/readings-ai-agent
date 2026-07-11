# RAG、Memory 与知识库治理

## 本章适合谁

如果你已经理解上下文工程和工具调用，但还不清楚 RAG、短期记忆、长期记忆、知识库治理之间的区别，这一章适合阅读。

本章会先讲直觉，再讲工程结构。重点不是追求复杂方案，而是避免把所有“给模型补信息”的方法都混成一个概念。

## 你会学到什么

- RAG 解决什么问题。
- Memory 解决什么问题。
- RAG 和 Memory 的区别与重叠。
- 知识库治理为什么重要。
- 长期记忆为什么既有价值也有风险。
- 初学者如何设计最小可验证实验。

## 先用一句话理解

RAG 更像“从外部资料里找证据”，Memory 更像“保存和使用系统历史经验”；两者都能给模型补上下文，但治理问题完全不同。

## 基础概念

### RAG

RAG 是 Retrieval-Augmented Generation 的缩写。通俗地说，就是先检索相关资料，再让模型基于资料生成回答。

RAG 论文使用 parametric memory 和 non-parametric memory 这样的术语：前者指模型参数中存储的知识，后者在论文设定中指可检索的外部索引，例如 Wikipedia dense vector index。初学者需要注意，这里的 non-parametric memory 不等同于 Agent 工程里的长期记忆治理。

RAG 的核心动机包括：

- 让模型访问外部知识。
- 让知识可以更新，而不是完全依赖模型参数。
- 让答案能追溯到资料来源。

RAG 论文中的设定和现代工程 RAG 系统不完全相同。初学者可以先掌握工程直觉：文档进入知识库，系统把文档切成片段，建立索引，用户提问时检索相关片段，再把片段放进模型上下文。

### Memory

Memory 是 Agent 保存和使用历史状态的机制。它可以包括当前任务状态、用户偏好、历史对话、工具结果、反思总结、结构化事实或知识图谱。

Memory 不等于把全部聊天历史塞进 prompt。那只是最简单也最脆弱的做法。

### 短期记忆

短期记忆通常服务于当前任务或当前会话。例如：当前步骤、刚刚调用过的工具、用户这轮对话里的约束。LangGraph memory 文档把这类记忆称为 thread-scoped memory，并把它作为 agent state 的一部分管理。

短期记忆的生命周期短，重点是帮助 Agent 保持任务连续性。

### 长期记忆

长期记忆跨会话存在。例如：用户长期偏好、项目约定、历史决策、常见错误、业务实体信息。LangGraph memory 文档把它描述为跨 conversations 或 sessions 的 user-specific 或 application-level data，并强调它没有通用的一刀切方案。

长期记忆更难治理，因为它涉及写入、更新、遗忘、冲突、隐私和过时信息。

## RAG 和 Memory 的区别

RAG 偏向“外部知识检索”。Memory 偏向“系统状态和历史经验管理”。

可以用几个问题区分：

- 这条信息来自外部资料库，还是来自历史交互？
- 这条信息是否需要被更新或遗忘？
- 这条信息是否涉及用户隐私或偏好？
- 这条信息是否应该影响未来任务？
- 这条信息是否需要可追溯引用？

比如项目 README、API 文档、论文适合进入 RAG 知识库。用户说“我以后都想用中文解释”可能是长期记忆候选。当前任务已经完成第 2 步，这是短期状态。

## 通俗例子

假设你做一个学习助手。

RAG 会帮它查资料：比如查 ReAct 论文摘要、OpenAI 文档、MCP 官方说明。

短期记忆会帮它记住当前任务：你正在学习 Tool Use，本轮已经解释过 Function Calling。

长期记忆可能帮它记住你的偏好：你是初学者，希望由浅入深，喜欢中文解释。

知识库治理会决定：哪些资料可以进入知识库，哪些用户偏好可以保存，哪些过时内容要标记，哪些冲突内容要人工确认。

## 工作原理

### 一个最小 RAG 流程

1. 收集文档。
2. 清洗和切分文档。
3. 为片段建立索引。
4. 用户提问时生成查询。
5. 检索相关片段。
6. 可选：rerank 或过滤片段。
7. 把片段和问题一起交给模型。
8. 输出答案和 references。

这个流程的风险在于：检索错了，模型可能基于错误资料回答；检索太多，模型可能忽略重点；资料过时，答案也会过时。

### 一个最小 Memory 流程

1. 从交互或工具结果中发现候选记忆。
2. 判断是否值得写入。
3. 写入结构化或非结构化存储。
4. 后续任务中根据上下文召回。
5. 使用前检查是否冲突、过时或敏感。
6. 必要时更新、删除或请求用户确认。

Memory 的关键不只是“能存”，而是“该不该存、怎么用、什么时候不用”。

## 工程实践

### RAG 先做可追溯

初学者做 RAG 时，不要只追求答案看起来流畅。先保证答案能追溯到资料片段。没有引用和来源，RAG 很难被校验。

### Chunking 需要实验

文档切得太碎，片段可能缺上下文；切得太大，检索可能不精准。chunk size、overlap、embedding model 和 reranking 都需要实验，而不是凭感觉确定。

### Memory 写入需要守门

不要把模型觉得“重要”的内容自动写入长期记忆。写入前至少判断：

- 是否稳定长期有效？
- 是否来自用户明确表达？
- 是否涉及隐私？
- 是否和已有记忆冲突？
- 是否可以被用户查看和删除？

### 区分事实、偏好和推断

“用户说他喜欢中文解释”是偏好。“用户是初学者”可能是推断。推断写入长期记忆前需要更谨慎。

### 记忆需要过期和纠错

长期记忆不是永久真理。用户偏好会变，项目规范会变，技术文档会过时。系统需要支持更新、废弃和人工纠错。

## 常见误区

- 误区一：RAG 能保证答案正确。检索错、资料错、引用错都会导致错误答案。
- 误区二：Memory 就是聊天历史。长期记忆需要结构、写入规则和治理。
- 误区三：记得越多越好。错误、过时和敏感信息会降低系统可靠性。
- 误区四：Embedding 一建好就结束。知识库需要持续更新、去重和过期处理。
- 误区五：用户画像可以随便自动推断。用户画像涉及隐私和误判风险。

## 什么时候不该加长期记忆

以下场景不建议先加长期记忆：

- 任务是一次性的。
- 用户没有明确同意保存偏好或历史。
- 记忆无法被查看、修改或删除。
- 没有冲突处理策略。
- 没有评测证明记忆提升了任务质量。

可以先使用会话内短期状态、RAG 或用户显式配置。

## 已验证结论

- RAG 论文摘要支持“外部检索可以帮助知识密集型生成任务”这一基础动机，并明确提到 provenance 和 world knowledge 更新问题。
- RAG 论文中的 non-parametric memory 指外部可检索索引一类机制，不应和 Agent 长期记忆治理直接混同。
- LangGraph memory 文档按 recall scope 区分 short-term/thread-scoped memory 和 long-term/cross-session memory，可作为短期/长期记忆工程边界的参考。
- LangGraph memory 文档强调 long-term memory 没有 one-size-fits-all solution，写入方式有 hot path 和 background 两类权衡。
- MemGPT、MemoryBank、Generative Agents 支持长期记忆和记忆管理的研究方向，但不能泛化为“加长期记忆总是更好”。

## 待验证问题

- 对初学者项目，最小 RAG baseline 应该包含哪些指标？
- 长期记忆在哪些任务中有稳定收益？
- Memory 写入守门有哪些可复用工程模式？
- 冲突记忆、过时记忆和隐私记忆应该如何处理？
- RAG 和 Memory 组合时，优先召回哪个信息源？
- 如何设计最小实验对比 RAG、thread-scoped memory 和 long-term memory？

## 本章小结

- RAG 主要解决外部知识检索，Memory 主要解决状态和历史经验管理。
- RAG 不保证正确，Memory 不保证提升表现。
- 长期记忆的难点在写入、更新、遗忘、冲突和隐私。
- 初学者应先做可追溯 RAG，再考虑长期记忆。
- 任何记忆机制都需要评测和用户可控性。

## References

### Papers

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](../sources/source-cards/2020-rag-paper.md)
- [MemGPT: Towards LLMs as Operating Systems](../sources/source-cards/2023-memgpt-paper.md)
- [MemoryBank: Enhancing Large Language Models with Long-Term Memory](../sources/source-cards/2023-memorybank-paper.md)
- [Generative Agents: Interactive Simulacra of Human Behavior](../sources/source-cards/2023-generative-agents-paper.md)

### Framework Docs

- [LlamaIndex Documentation](../sources/source-cards/2026-llamaindex-docs.md)
- [LangGraph Memory Documentation](../sources/source-cards/2026-langgraph-memory-docs.md)
- [Letta Documentation](../sources/source-cards/2026-letta-docs.md)
- [Zep Documentation](../sources/source-cards/2026-zep-docs.md)

### Governance

- [术语边界表](../glossary.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [Evidence Note: RAG 与 Memory 边界](../evidence/rag-memory-boundary.md)
