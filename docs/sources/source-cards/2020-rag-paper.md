# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

- 来源链接：https://arxiv.org/abs/2005.11401
- 作者 / 机构：Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuettler, Mike Lewis, Wen-tau Yih, Tim Rocktaeschel, Sebastian Riedel, Douwe Kiela
- 发布时间：2020-05-22；arXiv v4 updated 2021-04-12；accepted at NeurIPS 2020
- 最后复核日期：2026-07-11
- 类型：论文
- 主题：RAG / Retrieval / Knowledge-intensive NLP
- 适合阶段：入门后 / 进阶
- 可信度等级：A
- 是否已验证：来源链接、arXiv 元数据和摘要已复核；与 LangGraph memory docs 完成边界交叉验证；RAG / Memory 术语边界已可入正文；与 LlamaIndex docs 和最小 pipeline 实验共同支撑 RAG 工程 pipeline 窄边界可入正文

## 一句话总结

RAG 基础论文，用于解释为什么生成模型需要外部检索来处理知识密集型任务。

## 核心结论

- 论文提出 retrieval-augmented generation，将参数化记忆与显式非参数化记忆结合。
- 摘要描述的 RAG 形态使用预训练 seq2seq 模型作为 parametric memory，并用 Wikipedia dense vector index 作为 non-parametric memory。
- 摘要强调 provenance、知识更新和知识密集型任务是 RAG 的关键动机。
- 摘要指出大型预训练模型虽然把事实知识存储在参数中，但访问和精确操纵知识的能力仍有限；provenance 和 world knowledge 更新仍是开放问题。
- 因此本手册可把 RAG 作为“外部知识检索增强生成”的基础机制，并把 provenance 和知识更新作为 RAG 工程 pipeline 的基础动机；但需要提醒初学者：RAG 论文中的 non-parametric memory 术语不等同于 Agent 长期记忆治理。

## 支撑证据

- arXiv API 返回有效条目：`2005.11401v4`。
- 2026-07-11 抓取 arXiv 页面成功；页面显示 v4 accepted at NeurIPS 2020，并包含摘要中关于 provenance、world knowledge 更新、parametric / non-parametric memory 和 dense vector index of Wikipedia 的描述。

## 可能的问题

- 原始论文设定和当前工程 RAG 系统已有差异，需要结合现代框架文档说明。
- 初学者正文中应区分“RAG 论文中的模型训练方案”和“工程实践中的检索增强应用架构”。
- 论文不证明现代 RAG stack 的 citation correctness、chunk 策略、rerank 效果、成本或延迟表现。

## 初学者阅读建议

- 先理解“检索再生成”的直觉，再读论文方法。

## 是否进入正文

- 结论：进入；术语边界和工程 pipeline 窄边界可入正文
- 原因：RAG 章节基础 reference；可支撑 RAG 的外部检索、provenance、知识更新动机，以及 non-parametric memory 不等同于 Agent long-term memory 的边界。结合 LlamaIndex 工程流程资料和最小 pipeline 实验后，可支撑“RAG 是可观察工程 pipeline，不是单个 prompt 技巧”的窄结论。真实工程 RAG 质量仍需现代框架和实验补充。
