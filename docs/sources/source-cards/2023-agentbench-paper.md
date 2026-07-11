# AgentBench: Evaluating LLMs as Agents

- 来源链接：https://arxiv.org/abs/2308.03688
- 作者 / 机构：Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, Jie Tang
- 发布时间：2023-08-07；arXiv v3 updated 2025-10-04；published in ICLR 2024
- 最后复核日期：2026-07-11
- 类型：论文 / Benchmark
- 主题：Evaluation / Benchmark
- 适合阶段：进阶 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接和 arXiv 元数据已复核；摘要已精读；支撑公开 benchmark 不能直接代表真实业务 Agent 质量、工具/副作用 Agent 不能只看最终答案的窄结论；其余结论部分验证

## 一句话总结

AgentBench 是评估 LLM 作为 Agent 的代表性 benchmark 资料之一，适合 Eval 章节讨论 benchmark 的价值和局限。

## 核心结论

- 论文提出多维 benchmark，用 8 个不同环境评估 LLM-as-Agent 的推理和决策能力。
- 摘要指出复杂环境中的 agent 能力存在明显差距，并归因到长期推理、决策和指令遵循等问题。
- 摘要给出项目仓库：`https://github.com/THUDM/AgentBench`。
- 摘要强调需要在 challenging tasks in interactive environments 中定量评估 LLM-as-Agent，这支持正文中“Agent eval 不能只看静态问答”的保守表述。

## 支撑证据

- arXiv 页面返回 HTTP 200；metadata 显示 submitted on 2023-08-07，last revised 2025-10-04。
- 摘要写明 AgentBench 是 multi-dimensional benchmark，包含 8 distinct environments，用于评估 LLM-as-Agent 的 reasoning and decision-making abilities。
- 摘要写明 typical reasons of failures 包括 poor long-term reasoning、decision-making 和 instruction following abilities。
- 摘要写明 datasets、environments 和 integrated evaluation package 已发布。

## 是否进入正文

- 结论：进入；benchmark 边界和过程评测窄边界可入正文
- 原因：可支撑 Agent eval 需要交互环境、长期推理、决策和失败原因分析，并与 WebArena、OpenAI Evals 和 trace-aware eval 实验共同支撑“公开 benchmark 不能直接代表真实业务 Agent 质量”和“工具/副作用 Agent 不能只看最终答案”的窄结论；具体 trajectory 自动评分方法仍需补资料或实验。

## 可能的问题

- Benchmark 结果依赖被测模型、任务环境和时间点，需要避免把旧结果直接当成当前模型能力判断。
- 初学者正文应重点使用它解释“如何评估 Agent”，而不是背具体排名。
- 不能把 AgentBench 分数直接写成业务系统可用性判断；真实系统仍需要自己的任务集、权限检查、trace 和回归评测。
