# Tree of Thoughts: Deliberate Problem Solving with Large Language Models

- 来源链接：https://arxiv.org/abs/2305.10601
- 作者 / 机构：Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan
- 发布时间：2023-05-17；arXiv v2 updated 2023-12-03；NeurIPS 2023 camera-ready version
- 最后复核日期：2026-07-11
- 类型：论文
- 主题：Planning / Search / Reasoning
- 适合阶段：进阶
- 可信度等级：A
- 是否已验证：来源链接和 arXiv 元数据已复核；内容待精读；结论待交叉验证

## 一句话总结

Tree of Thoughts 可用于解释搜索式规划和多候选推理路径，但需要谨慎区分研究方法和生产 Agent 架构。

## 核心结论

- 论文提出 Tree of Thoughts，将 Chain of Thought 泛化为对多个中间“thoughts”的搜索。
- 摘要声称 ToT 允许模型考虑不同推理路径、自我评估选择，并在需要时前瞻或回溯。
- 摘要中的实验任务包括 Game of 24、Creative Writing 和 Mini Crosswords。

## 是否进入正文

- 结论：作为进阶资料进入
- 原因：适合 Planning 章节，不宜作为初学者第一篇材料。

## 可能的问题

- ToT 是推理/搜索框架，不应直接等同于生产 Agent 的任务编排。
- 需要和实际 orchestration 框架资料交叉验证。
