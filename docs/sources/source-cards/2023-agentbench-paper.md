# AgentBench: Evaluating LLMs as Agents

- 来源链接：https://arxiv.org/abs/2308.03688
- 作者 / 机构：Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, Jie Tang
- 发布时间：2023-08-07；arXiv v3 updated 2025-10-04；published in ICLR 2024
- 最后复核日期：2026-07-11
- 类型：论文 / Benchmark
- 主题：Evaluation / Benchmark
- 适合阶段：进阶 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接和 arXiv 元数据已复核；内容待精读；结论待交叉验证

## 一句话总结

AgentBench 是评估 LLM 作为 Agent 的代表性 benchmark 资料之一，适合 Eval 章节讨论 benchmark 的价值和局限。

## 核心结论

- 论文提出多维 benchmark，用 8 个不同环境评估 LLM-as-Agent 的推理和决策能力。
- 摘要指出复杂环境中的 agent 能力存在明显差距，并归因到长期推理、决策和指令遵循等问题。
- 摘要给出项目仓库：`https://github.com/THUDM/AgentBench`。

## 是否进入正文

- 结论：进入
- 原因：Eval 章节需要 benchmark 类 reference。

## 可能的问题

- Benchmark 结果依赖被测模型、任务环境和时间点，需要避免把旧结果直接当成当前模型能力判断。
- 初学者正文应重点使用它解释“如何评估 Agent”，而不是背具体排名。
