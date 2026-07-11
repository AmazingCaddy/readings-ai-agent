# Toolformer: Language Models Can Teach Themselves to Use Tools

- 来源链接：https://arxiv.org/abs/2302.04761
- 作者 / 机构：Timo Schick, Jane Dwivedi-Yu, Roberto Dessi, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom
- 发布时间：2023-02-09
- 最后复核日期：2026-07-11
- 类型：论文
- 主题：Tool Use
- 适合阶段：进阶
- 可信度等级：A
- 是否已验证：来源链接、arXiv 元数据和摘要已复核；与 OpenAI Function Calling docs 完成交叉验证；tool use 可以连接外部工具能力的基础概念可入正文；真实 API 行为仍部分验证

## 一句话总结

Toolformer 是理解语言模型使用外部工具能力的重要论文，可辅助解释 tool use 的研究脉络。

## 核心结论

- 论文研究语言模型如何通过简单 API 学会调用外部工具。
- 摘要列出的工具包括 calculator、QA system、search engines、translation system 和 calendar。
- 摘要强调模型要学习何时调用 API、传什么参数、如何把结果纳入后续 token prediction。
- 摘要说明 Toolformer 使用 self-supervised 方式，只需要每个 API 的少量 demonstrations，目标是训练模型获得工具使用能力。
- 因此 Toolformer 可支撑“tool use 的研究脉络”，但不应被当作现代 API function calling 的定义来源。

## 支撑证据

- 2026-07-11 抓取 arXiv 页面成功；页面显示标题、作者、提交日期、arXiv ID 和摘要。
- arXiv 摘要写明：Toolformer is “a model trained to decide which APIs to call, when to call them, what arguments to pass, and how to best incorporate the results into future token prediction”。

## 是否进入正文

- 结论：进入；tool use 基础概念可入正文
- 原因：适合作为 Tool Use 章节的研究 reference。摘要可支撑模型使用 calculator、QA system、search engines、translation system 和 calendar 等外部工具能力的研究脉络；结合 OpenAI Function Calling / Responses API 文档，可支撑现代工程中 tool use 与 API tool calling 的基础边界。真实 API 稳定性、参数修正、成本和跨框架术语仍需实验。

## 可能的问题

- Toolformer 是研究训练方案，不等同于当前产品 API 中的 function calling 或 tool calling。
- 正文需要明确区分“模型训练出工具使用能力”和“应用层通过 schema 约束工具调用”。
- Toolformer 摘要中的性能结论来自论文实验设置，不应直接泛化到当前模型和 API 产品。
