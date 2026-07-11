# Toolformer: Language Models Can Teach Themselves to Use Tools

- 来源链接：https://arxiv.org/abs/2302.04761
- 作者 / 机构：Timo Schick, Jane Dwivedi-Yu, Roberto Dessi, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom
- 发布时间：2023-02-09
- 最后复核日期：2026-07-11
- 类型：论文
- 主题：Tool Use
- 适合阶段：进阶
- 可信度等级：A
- 是否已验证：来源链接和 arXiv 元数据已复核；内容待精读；结论待交叉验证

## 一句话总结

Toolformer 是理解语言模型使用外部工具能力的重要论文，可辅助解释 tool use 的研究脉络。

## 核心结论

- 论文研究语言模型如何通过简单 API 学会调用外部工具。
- 摘要列出的工具包括 calculator、QA system、search engines、translation system 和 calendar。
- 摘要强调模型要学习何时调用 API、传什么参数、如何把结果纳入后续 token prediction。

## 是否进入正文

- 结论：进入
- 原因：适合作为 Tool Use 章节的研究 reference。

## 可能的问题

- Toolformer 是研究训练方案，不等同于当前产品 API 中的 function calling 或 tool calling。
- 正文需要明确区分“模型训练出工具使用能力”和“应用层通过 schema 约束工具调用”。
