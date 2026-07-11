# Tree of Thoughts: Deliberate Problem Solving with Large Language Models

- 来源链接：https://arxiv.org/abs/2305.10601
- 作者 / 机构：Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan
- 发布时间：2023-05-17；arXiv v2 updated 2023-12-03；NeurIPS 2023 camera-ready version
- 最后复核日期：2026-07-12
- 类型：论文
- 主题：Planning / Search / Reasoning
- 适合阶段：进阶
- 可信度等级：A
- 是否已验证：来源链接、arXiv API 元数据、摘要和代码仓库可达性已于 2026-07-12 复核；ToT 搜索式推理路径不是生产 Agent 编排框架、复杂架构不是默认更可靠的窄边界可入正文；ToT 真实效果仍部分验证

## 一句话总结

Tree of Thoughts 可用于解释搜索式规划和多候选推理路径，但需要谨慎区分研究方法和生产 Agent 架构。

## 核心结论

- 论文提出 Tree of Thoughts，将 Chain of Thought 泛化为对多个中间“thoughts”的搜索。
- 摘要声称 ToT 允许模型考虑不同推理路径、自我评估选择，并在需要时前瞻或回溯。
- 摘要中的实验任务包括 Game of 24、Creative Writing 和 Mini Crosswords。

## 支撑证据

- 2026-07-12 抓取 arXiv 页面返回 HTTP 200；响应头 `last-modified: Mon, 29 Jan 2024 20:07:14 GMT`。
- arXiv API 返回有效条目：`2305.10601v2`，published `2023-05-17T23:16:17Z`，updated `2023-12-03T22:50:35Z`，primary category `cs.CL`。
- arXiv comment 标注 NeurIPS 2023 camera ready version，并给出代码仓库 `https://github.com/princeton-nlp/tree-of-thought-llm`。
- 2026-07-12 复核 GitHub 仓库页面返回 HTTP 200；GitHub API 显示仓库 public、MIT、Python、default branch `master`、archived=false、pushed_at `2025-01-16T20:02:00Z`。
- API 摘要包含 multiple different reasoning paths、self-evaluating choices、looking ahead、backtracking、Game of 24、Creative Writing 和 Mini Crosswords 等关键表述。
- API 摘要报告 Game of 24 等任务上的成功率数字；这些只能作为论文实验设置下的效果声明，不能外推为当前真实模型或生产编排默认收益。
- 已与 ReAct、Reflexion、LangGraph 和 Agent/Workflow evidence 交叉验证架构模式边界。

## 是否进入正文

- 结论：进入；搜索式推理边界可入正文
- 原因：适合 Planning 章节，不宜作为初学者第一篇材料。摘要可支撑多个中间 thought、不同推理路径、自我评估、前瞻和回溯等搜索式推理机制；结合 LangGraph / workflow evidence，可支撑“研究式搜索推理不等同于生产 Agent 编排框架”的边界。

## 可能的问题

- ToT 是推理/搜索框架，不应直接等同于生产 Agent 的任务编排、状态管理、权限控制或持久化 runtime。
- 已和实际 orchestration 框架资料完成第一轮交叉验证；可支撑“搜索式推理不是复杂任务默认升级路径”的窄边界。Planner / Executor 可执行计划边界已由标准库实验和 orchestration evidence 支撑，但这不等于验证 ToT-style search。仍需 ToT-style search 实验验证搜索式规划的成本和收益。
