# WebArena: A Realistic Web Environment for Building Autonomous Agents

- 来源链接：https://arxiv.org/abs/2307.13854
- 作者 / 机构：Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, Graham Neubig
- 发布时间：2023-07-25；arXiv v4 updated 2024-04-16
- 最后复核日期：2026-07-11
- 类型：论文 / Benchmark
- 主题：Web Agent / Evaluation
- 适合阶段：进阶
- 可信度等级：A
- 是否已验证：来源链接和 arXiv 元数据已复核；摘要已精读；支撑过程/交互评测窄结论；其余结论部分验证

## 一句话总结

WebArena 适合用于理解 Web Agent 的评测环境和真实任务复杂度。

## 核心结论

- 论文构建了一个用于 language-guided web agents 的真实且可复现环境。
- 摘要描述环境包含四类功能网站：e-commerce、social forum discussions、collaborative software development 和 content management。
- 摘要报告其最佳 GPT-4-based agent 端到端任务成功率为 14.41%，低于人类表现 78.24%，显示真实 Web Agent 任务仍很难。
- 摘要强调 benchmark tasks 关注 task completions 的 functional correctness，任务 diverse、long-horizon，并模拟人类日常互联网任务。

## 支撑证据

- arXiv 页面返回 HTTP 200；metadata 显示 submitted on 2023-07-25，last revised 2024-04-16。
- 摘要写明 WebArena 建立 highly realistic and reproducible 的 language-guided agent 环境。
- 摘要写明环境包含 fully functional websites，并配有 tools 和 external knowledge bases。
- 摘要写明任务关注 functional correctness of task completions，且 diverse、long-horizon。
- 摘要报告最佳 GPT-4-based agent end-to-end task success rate 为 14.41%，human performance 为 78.24%。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑真实 Web Agent 任务需要端到端环境、工具、外部知识和 long-horizon 评测，并与 trace-aware eval 实验共同支撑“只看最终答案不足以覆盖过程风险”的窄结论；具体数值不能泛化为当前模型能力。

## 可能的问题

- 具体数值反映当时实验设置，不能直接代表当前模型能力。
- 适合用来说明评测环境复杂度和 functional correctness，而不是作为通用 Agent 能力结论。
