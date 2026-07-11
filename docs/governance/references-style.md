# References 规范

References 是正文的一等内容，用于支撑关键定义、结论、工程建议和争议判断。

## 基本规则

- 关键定义必须给来源。
- 框架用法优先链接官方文档。
- 论文观点链接论文原文或 arXiv 页面。
- 工程实践链接原始博客、源码、示例或案例。
- 同一段落不要堆太多链接，优先给 1-3 个最高质量 references。
- 每章末尾保留 `References` 列表，按类型分组。

## 来源类型

- Paper
- Official Docs
- Spec
- Source Code
- Engineering Blog
- Course
- Benchmark
- Security Guidance

## 可信度等级

```text
A 级：官方文档、论文、标准规范、源码、可复现实验。
B 级：知名团队工程实践，有代码、数据或清晰上下文。
C 级：个人博客、课程、访谈、总结文章，需要交叉验证。
D 级：营销文、无来源观点、过时内容，只能作为线索。
```

## 引用示例

```md
ReAct 的核心思想是让模型在推理步骤和行动步骤之间交替，从而把语言推理和工具使用结合起来。这个模式适合需要多步搜索、观察外部结果并继续决策的任务。[ReAct paper](https://arxiv.org/abs/2210.03629)

## References

- Paper: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- Official Docs: [OpenAI Function Calling / Tool Calling docs](待复核)
- Framework Docs: [LangGraph agent examples](待复核)
```

## 收录门槛

正文默认只采用 A/B 级资料。C 级资料必须交叉验证后才能作为补充。D 级资料不进入正文。

