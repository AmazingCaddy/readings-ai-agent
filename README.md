# AI Agent 学习手册

这是一个面向初学者的 AI Agent 中文学习手册项目。目标不是收集链接，而是系统性调查、校验并组织学习材料，最终发布为 GitHub Pages。

## 项目目标

为初学者构建一本由浅入深、带可靠 references 的 AI Agent 中文学习手册。内容需要同时满足：

- **广度**：覆盖 AI Agent 的主要主题和工程组件。
- **深度**：解释原理、适用场景、失败模式、工程取舍和实践方法。
- **精度**：准确区分 Agent、Workflow、RAG、Memory、Tool Use、Planning、MCP、Eval 等概念。
- **正确性**：关键结论必须有 references、交叉验证或实验验证支撑。

## 当前阶段

当前阶段是内容蓝图和资料治理体系，不急于写完整正文或做页面视觉设计。

第一阶段交付物：

- 主题地图
- 章节目录 v1
- 资料可信度分级标准
- 资料卡片模板
- 章节写作模板
- references 标注规范
- 候选高质量资料来源清单
- 待验证问题清单
- 候选实验/复现清单

## 目录

- [项目 Goal](docs/governance/goal.md)
- [质量标准](docs/governance/quality-standard.md)
- [References 规范](docs/governance/references-style.md)
- [References 覆盖矩阵](docs/references/coverage-matrix.md)
- [主题地图](docs/topic-map.md)
- [章节目录](docs/chapter-outline.md)
- [候选资料清单](docs/sources/seed-candidates.md)
- [Source Card 索引](docs/sources/source-card-index.md)
- [待验证问题](docs/evidence/validation-backlog.md)
- [资料卡片模板](docs/templates/source-card.md)
- [章节模板](docs/templates/chapter-template.md)

## 内容原则

1. 面向初学者，先讲直觉，再讲术语，再讲工程实现。
2. References 是一等内容，不是最后附录。
3. 正文默认只采用 A/B 级资料。
4. C 级资料必须交叉验证后才能作为补充。
5. D 级资料不进入正文，只作为线索或丢弃。
6. 对工程结论尽量设计最小复现实验。
