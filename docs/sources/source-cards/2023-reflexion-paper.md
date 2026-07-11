# Reflexion: Language Agents with Verbal Reinforcement Learning

- 来源链接：https://arxiv.org/abs/2303.11366
- 作者 / 机构：Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
- 发布时间：2023-03-20；arXiv v4 updated 2023-10-10
- 最后复核日期：2026-07-11
- 类型：论文
- 主题：Reflection / Agent Learning / Evaluation
- 适合阶段：进阶
- 可信度等级：A
- 是否已验证：来源链接、arXiv 元数据和摘要已复核；Agent 架构模式边界已完成第一轮交叉验证

## 一句话总结

Reflexion 可用于理解反思、反馈和错误修正模式，但需要验证它在现代模型和真实任务中的适用边界。

## 核心结论

- 论文提出通过语言反馈强化 language agents，而不是更新模型权重。
- 摘要描述 Reflexion agents 会基于任务反馈进行文字反思，并把 reflective text 保存在 episodic memory buffer 中，以改进后续决策。
- 摘要报告在 sequential decision-making、coding、language reasoning 等任务上有提升。

## 支撑证据

- arXiv API 返回有效条目：`2303.11366v4`。
- 2026-07-11 抓取 arXiv 页面成功；摘要包含 linguistic feedback、reflective text、episodic memory buffer、subsequent trials、sequential decision-making、coding 和 language reasoning 等关键表述。
- 已与 ReAct、Tree of Thoughts、LangGraph、长期记忆治理 evidence 和 eval evidence 交叉验证 reflection 边界。

## 是否进入正文

- 结论：作为进阶资料进入
- 原因：适合 Agent 架构和 Eval 章节讨论。

## 可能的问题

- 摘要中的提升来自特定任务和设置，不应泛化为“reflection 总是有效”。
- 需要结合现代模型和生产任务复核 reflection 的成本、稳定性和错误放大风险。
- Reflection 依赖反馈信号和记忆写入质量，可能把错误总结写入后续状态；正文需要和 memory governance 风险一起解释。
