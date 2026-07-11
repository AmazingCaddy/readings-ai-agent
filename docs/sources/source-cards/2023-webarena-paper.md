# WebArena: A Realistic Web Environment for Building Autonomous Agents

- 来源链接：https://arxiv.org/abs/2307.13854
- 作者 / 机构：Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, Graham Neubig
- 发布时间：2023-07-25；arXiv v4 updated 2024-04-16
- 最后复核日期：2026-07-12
- 类型：论文 / Benchmark
- 主题：Web Agent / Evaluation
- 适合阶段：进阶
- 可信度等级：A
- 是否已验证：arXiv API 元数据、HTTP metadata、摘要、项目页和 GitHub README / raw README 已于 2026-07-12 复核；支撑公开 benchmark 不能直接代表真实业务 Agent 质量、过程/交互评测、Web benchmark 需要 self-hosted environment / reset / auth / trajectory 记录的窄结论；其余结论部分验证

## 一句话总结

WebArena 适合用于理解 Web Agent 的评测环境和真实任务复杂度。

## 核心结论

- 论文构建了一个用于 language-guided web agents 的真实且可复现环境。
- 摘要描述环境包含四类功能网站：e-commerce、social forum discussions、collaborative software development 和 content management。
- 摘要报告其最佳 GPT-4-based agent 端到端任务成功率为 14.41%，低于人类表现 78.24%，显示真实 Web Agent 任务仍很难。
- 摘要强调 benchmark tasks 关注 task completions 的 functional correctness，任务 diverse、long-horizon，并模拟人类日常互联网任务。

## 支撑证据

- 2026-07-12 抓取 arXiv 页面返回 HTTP 200；响应头 `last-modified: Wed, 01 May 2024 16:23:12 GMT`。
- arXiv API 返回有效条目：`2307.13854v4`，published `2023-07-25T22:59:32Z`，updated `2024-04-16T15:13:18Z`，primary category `cs.AI`。
- arXiv comment 标注 code、data、environment reproduction resources 和 video demonstrations 公开于 `https://webarena.dev/`。
- API 摘要写明 WebArena 建立 highly realistic and reproducible 的 language-guided agent 环境，包含 fully functional websites、tools 和 external knowledge bases。
- API 摘要写明任务关注 functional correctness of task completions，且 diverse、long-horizon；摘要中的 14.41% / 78.24% 只能作为论文实验设置下的历史观察，不能外推为当前模型能力。
- `https://webarena.dev/` 于 2026-07-12 返回 HTTP 200；页面列出 WebArena、WebArena-Infinity、VisualWebArena 和 TheAgentCompany 等项目，WebArena 卡片描述为 autonomous web agents 的 realistic web environment。
- GitHub README / raw README 于 2026-07-12 可达，说明 WebArena 是 standalone, self-hostable web environment；2024-12-05 更新提示该 repo 是复现论文结果的 canonical implementation，但 web navigation infrastructure 已由 AgentLab / BrowserGym 增强，README 强烈建议用这些框架做实验。
- README 明确 quick walkthrough / demo sites 只用于教育和理解内容；要做 reproducible / end-to-end evaluation，必须自建 WebArena websites、配置 shopping / admin / reddit / gitlab / map / wikipedia / homepage URL、生成测试数据、获取 auto-login cookies，并在评估 812 examples 后按环境文档 reset 到初始状态。
- README 的 evaluation 命令需要 `OPENAI_API_KEY`，示例只跑第一个 example，并说明 trajectory 会保存到 `<result_dir>/0.html`；这支撑“Web Agent eval 必须保存 trajectory / browser state”，但不证明任何模型当前网页任务能力。

## 是否进入正文

- 结论：进入；benchmark 边界和过程评测窄边界可入正文
- 原因：可支撑真实 Web Agent 任务需要端到端环境、工具、外部知识、long-horizon 评测和 task completion functional correctness，并与 AgentBench、OpenAI Evals 和 trace-aware eval 实验共同支撑“公开 benchmark 不能直接代表真实业务 Agent 质量”和“只看最终答案不足以覆盖过程风险”的窄结论；具体数值不能泛化为当前模型能力。

## 可能的问题

- 具体数值反映当时实验设置，不能直接代表当前模型能力。
- 适合用来说明评测环境复杂度和 functional correctness，而不是作为通用 Agent 能力结论。
- 不能把 WebArena 成绩直接写成产品可用性判断；业务系统还需要自己的权限、数据、工具和回归评测。
