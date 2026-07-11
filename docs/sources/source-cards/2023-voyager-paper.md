# Voyager: An Open-Ended Embodied Agent with Large Language Models

- 来源链接：https://arxiv.org/abs/2305.16291
- 项目链接：https://voyager.minedojo.org/
- 代码链接：https://github.com/MineDojo/Voyager
- 作者 / 机构：Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar
- 发布时间：2023-05-25；arXiv v2 updated 2023-10-19
- 最后复核日期：2026-07-12
- 类型：论文 / Source / Embodied agent
- 主题：Embodied Agent / Lifelong Learning / Minecraft / Skill Library / Self-improvement
- 适合阶段：进阶
- 可信度等级：A
- 是否已验证：arXiv API 元数据、HTTP metadata、项目站点、GitHub repo metadata 和 README 已于 2026-07-12 复核；摘要和 README 关键段落已精读；支撑开放式具身 Agent 的 automatic curriculum、executable skill library、environment feedback、execution error、自我验证和程序改进的研究机制边界；标准库 Voyager-style toy environment 已完成，支撑 curriculum、技能修正、verified skill library、sandbox rejection 和 trace 形状的窄观察；真实复现、成本、环境依赖、Minecraft 以外泛化能力和当前模型表现仍部分验证

## 一句话总结

Voyager 适合用来理解开放式具身 Agent：它把环境探索、技能库、代码执行、错误反馈和自我验证组织成长期学习循环，而不是只做一次性问答。

## 核心结论

- 论文提出 Voyager 是一个 LLM-powered embodied lifelong learning agent，在 Minecraft 中持续探索、获得多样技能并发现新内容。
- 摘要将 Voyager 拆成三个关键组件：automatic curriculum、ever-growing skill library of executable code、iterative prompting mechanism。
- Automatic curriculum 的目标是最大化探索，而不是只完成一个固定任务。
- Skill library 用 executable code 存储和检索复杂行为；README 和摘要都强调这些 skills 是 temporally extended、interpretable 和 compositional。
- Iterative prompting mechanism 会利用 environment feedback、execution errors 和 self-verification 来改进程序。
- Voyager 通过 blackbox GPT-4 queries 与模型交互，不需要微调模型参数。
- 摘要报告 Voyager 在 Minecraft 中获得更多 unique items、移动更远距离、解锁 tech tree milestones 更快，并能把 learned skill library 用到新的 Minecraft world 中处理新任务。
- 对本手册来说，稳妥结论是：开放式具身 Agent 需要环境接口、可执行动作、反馈循环、技能复用、长期状态和评测环境；不能把一次性聊天或单轮 tool call 直接等同于 embodied lifelong learning。
- 这些结果来自 Minecraft、特定环境、特定工具链和当时的 GPT-4 设置；不能泛化成“技能库一定提升所有 Agent 表现”或“开放式 Agent 默认适合业务生产系统”。

## 支撑证据

- 2026-07-12 抓取 arXiv 页面返回 HTTP 200；响应头 `last-modified: Fri, 20 Oct 2023 00:34:29 GMT`。
- arXiv API 返回有效条目：`2305.16291v2`，published `2023-05-25T17:46:38Z`，updated `2023-10-19T16:27:03Z`，primary category `cs.AI`。
- API 摘要写明 Voyager is the first LLM-powered embodied lifelong learning agent in Minecraft that continuously explores the world, acquires diverse skills, and makes novel discoveries without human intervention。
- API 摘要列出三个组件：automatic curriculum、ever-growing skill library of executable code、iterative prompting mechanism；并写明 iterative prompting incorporates environment feedback, execution errors, and self-verification for program improvement。
- API 摘要写明 Voyager interacts with GPT-4 via blackbox queries，bypasses the need for model parameter fine-tuning。
- API 摘要报告 3.3x more unique items、2.3x longer distances、15.3x faster key tech tree milestones，并说明 learned skill library 可迁移到新 Minecraft world 处理新任务；这些只能作为论文实验设置下的 Minecraft 观察，不能外推为当前模型能力、其他环境泛化能力或生产可靠性。
- 项目站点 `https://voyager.minedojo.org/` 于 2026-07-12 返回 HTTP 200；响应头 `last-modified: Sun, 04 Jan 2026 18:17:52 GMT`。
- GitHub API 返回 repo `MineDojo/Voyager` metadata：public、MIT license、default branch `main`、`archived=false`、language `JavaScript`、`updated_at=2026-07-11T16:51:13Z`、`pushed_at=2024-04-03T18:51:36Z`，topics 包含 `embodied-learning`、`large-language-models`、`minecraft`、`open-ended-learning`。
- GitHub README 于 2026-07-12 可达，重复论文摘要的三组件说明，并说明运行需要 Python >= 3.9、Node.js >= 16.13.0、Minecraft instance、Fabric mods、OpenAI API key 和 GPT-4。
- GitHub README 明确声明：This project is strictly for research purposes, and not an official product from NVIDIA。
- [Voyager-style Toy Embodied Agent 实验](../../experiments/voyager-style-toy-agent/results-2026-07-11.md) 用标准库 toy environment 跑通 3 个 curriculum task；治理策略通过环境反馈修正 `craft_pickaxe`、拒绝并修正 `unsafe_spawn_stone`、自我验证后保存 3 个 verified skills，成功 3/3；无技能库和未验证技能库策略均只成功 1/3。

## 可能的问题

- 论文结果来自 Minecraft 环境，不能直接代表网页、代码、企业系统或真实机器人场景的可靠性。
- README 安装依赖重，包括 Minecraft、Fabric mods、Node.js、Python、OpenAI API key 和游戏登录流程；这不适合作为初学者第一阶段实践项目。
- Skill library 的有效性依赖任务环境、动作接口、错误反馈和检索方式；不能写成“给 Agent 加一个技能库就会持续变强”。
- 自主探索和无人工干预会扩大权限、成本、停止条件和安全问题；真实系统需要 sandbox、预算、trace、回滚和人工确认。
- 性能倍数是论文报告的特定 benchmark 结果，不应写成当前模型能力或生产可用性结论。

## 初学者阅读建议

- 先读本手册第 01、04、08、09 章，再读 Voyager 摘要；重点看它为什么需要环境、动作、反馈和技能库。
- 不建议初学者直接试跑完整 Voyager；可以先用 toy environment 模拟“任务 -> 动作 -> 环境反馈 -> 错误修正 -> 技能复用”的最小循环。
- 阅读性能数字时只把它们当成论文实验结果，不要当成通用 Agent 能力排行。

## 可复现实验

- 已完成一个小型 toy environment，见 [Voyager-style Toy Embodied Agent 实验结果](../../experiments/voyager-style-toy-agent/results-2026-07-11.md)。后续可扩展真实模型生成/修正 skill、step budget 耗尽、循环动作、错误技能污染和跨环境 skill transfer case。
- 如要试跑 Voyager 原仓库，应记录环境安装步骤、Minecraft / Fabric / Node / Python 版本、API 成本、失败样例、checkpoint、技能库内容、sandbox 和停止条件。

## 是否进入正文

- 结论：部分进入
- 原因：可作为第 04/12 章中 embodied lifelong agent、automatic curriculum、skill library、environment feedback 和 self-verification 的研究参考；也能补强“复杂 Agent 架构需要环境、状态、反馈、trace 和成本评估，不能默认更可靠”的边界。不能支撑 Minecraft 以外的通用效果、生产可靠性或长期记忆 / 技能库默认提升表现。
