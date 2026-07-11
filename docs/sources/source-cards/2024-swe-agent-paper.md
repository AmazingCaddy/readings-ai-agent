# SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering

- 来源链接：https://arxiv.org/abs/2405.15793
- DOI：https://doi.org/10.48550/arXiv.2405.15793
- 作者 / 机构：John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press
- 发布时间：2024-05-06；v3 更新于 2024-11-11
- 最后复核日期：2026-07-11
- 类型：论文 / Source / Software engineering agent
- 主题：SWE-agent / Agent-computer interface / Repo issue fixing / Software engineering agents
- 适合阶段：进阶 / 实践扩展
- 可信度等级：A
- 是否已验证：来源链接、HTTP metadata、arXiv 元数据、摘要和 GitHub README 已复核；支撑“软件工程 Agent 需要面向 Agent 的计算机/仓库接口，覆盖创建/编辑代码、导航仓库、运行测试和程序”的窄边界；SWE-agent README 已提示当前推荐使用 mini-SWE-agent；真实 repo issue 成功率、成本、延迟、安全隔离和当前 leaderboard 表现仍部分验证

## 一句话总结

SWE-agent 适合用来理解软件工程 Agent 的真实复杂度：它不是让模型直接“写一段代码”就结束，而是让 Agent 在仓库里导航、编辑文件、运行测试，并通过专门设计的 agent-computer interface 与开发环境交互。

## 核心结论

- 摘要提出 LM agents 是一种 new category of end users，有自己的 needs and abilities，因此需要 specially-built interfaces。
- SWE-agent 的 custom agent-computer interface 用于让 Agent 创建和编辑代码文件、导航整个仓库、执行测试和其他程序。
- 论文评估 SWE-agent 在 SWE-bench 和 HumanEvalFix 上的表现，并报告当时的 state-of-the-art 结果。
- 对本手册而言，稳妥结论是：软件工程 Agent 需要把 repo 导航、文件编辑、命令执行、测试反馈、隔离环境和 trace 作为系统能力设计；不能只靠 prompt 或一次性代码生成。
- GitHub README 明确提示当前主要开发转向 mini-SWE-agent，并建议 going forward 使用 mini-SWE-agent；因此原 SWE-agent 更适合作为概念和历史 reference，真实试跑应复核当前推荐工具。

## 支撑证据

- arXiv 页面返回 HTTP 200；HTTP `last-modified` 为 2024-11-13。
- arXiv 元数据显示 v1 submitted on 2024-05-06，v3 updated on 2024-11-11。
- 摘要写明 SWE-agent facilitates LM agents to autonomously use computers to solve software engineering tasks。
- 摘要写明 custom ACI enhances ability to create and edit code files, navigate entire repositories, and execute tests and other programs。
- arXiv metadata comments 写明 code, data, and demo available at `https://swe-agent.com`。
- GitHub README 写明 SWE-agent 可以 autonomously use tools to fix issues in real GitHub repositories，并提供 docs / usage / benchmarking links。
- GitHub README 警告：Most current development effort is on mini-swe-agent, which has superseded SWE-agent，并建议 use mini-SWE-agent going forward。

## 是否进入正文

- 结论：进入；作为 Software Engineering Agent / 实践路线 / repo issue 工作流的进阶 reference。
- 原因：它能支撑“真实代码库 Agent 需要专门接口、测试反馈和环境隔离”的学习边界；但不能证明某个当前模型、框架或 agent 在用户本地仓库中稳定可靠。

## 可能的问题

- README 当前推荐 mini-SWE-agent，原 SWE-agent 的工程入口可能不再是最适合初学者试跑的路径。
- 论文中的 benchmark 数字来自当时版本、任务集和模型环境，不应写成当前能力事实。
- 软件工程 Agent 涉及写文件、运行命令、安装依赖和可能访问敏感代码，真实试跑必须有 sandbox、只读/写权限分离、成本限制和回滚策略。
- SWE-agent / mini-SWE-agent 能帮助学习 repo issue 工作流，但不能替代本手册中对权限、trace、eval 和人工确认的要求。

## 初学者阅读建议

- 先读本手册第 04、08、09 和 11 章，理解架构、eval、安全和实践路线。
- 阅读 SWE-agent 摘要时重点看 ACI 为什么重要：文件编辑、仓库导航、测试执行都是工具接口，不只是自然语言能力。
- 不建议初学者直接在重要仓库上运行软件工程 Agent；应先用 toy repo、只读任务或隔离 sandbox。

## 可复现实验

- 本手册已完成标准库 workflow / hybrid / ReAct-like 对比、planner/executor 对比和 trace-aware eval 实验，可作为 repo issue 任务实验设计的起点。
- 后续真实实验可选择 toy repo issue：固定 workflow、workflow-agent hybrid、SWE-agent / mini-SWE-agent 或其他 coding agent 进行对比，记录文件读写、测试执行、失败原因、token、latency、cost、权限确认、回滚和 trace 可读性。
