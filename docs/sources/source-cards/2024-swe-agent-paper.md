# SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering

- 来源链接：https://arxiv.org/abs/2405.15793
- DOI：https://doi.org/10.48550/arXiv.2405.15793
- 作者 / 机构：John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press
- 发布时间：2024-05-06；v3 更新于 2024-11-11
- 最后复核日期：2026-07-12
- 类型：论文 / Source / Software engineering agent
- 主题：SWE-agent / Agent-computer interface / Repo issue fixing / Software engineering agents
- 适合阶段：进阶 / 实践扩展
- 可信度等级：A
- 是否已验证：来源链接、HTTP metadata、arXiv API 元数据、GitHub API / README、SWE-agent docs index / hello_world / architecture Markdown 已于 2026-07-12 复核；支撑“软件工程 Agent 需要面向 Agent 的计算机/仓库接口，覆盖创建/编辑代码、导航仓库、运行测试和程序”的窄边界；官方 README、docs banner 和站点弹窗均提示当前推荐使用 mini-SWE-agent，SWE-agent 处于 maintenance-only 方向；Real Repo Issue Agent Toy 已完成固定 workflow baseline 和确定性 workflow-agent hybrid baseline，但尚未运行 SWE-agent；真实 repo issue 成功率、成本、延迟、安全隔离、当前 leaderboard 表现和维护模式下的实践适配仍部分验证

## 一句话总结

SWE-agent 适合用来理解软件工程 Agent 的真实复杂度：它不是让模型直接“写一段代码”就结束，而是让 Agent 在仓库里导航、编辑文件、运行测试，并通过专门设计的 agent-computer interface 与开发环境交互。

## 核心结论

- 摘要提出 LM agents 是一种 new category of end users，有自己的 needs and abilities，因此需要 specially-built interfaces。
- SWE-agent 的 custom agent-computer interface 用于让 Agent 创建和编辑代码文件、导航整个仓库、执行测试和其他程序。
- 论文评估 SWE-agent 在 SWE-bench 和 HumanEvalFix 上的表现，并报告当时的 state-of-the-art 结果。
- 对本手册而言，稳妥结论是：软件工程 Agent 需要把 repo 导航、文件编辑、命令执行、测试反馈、隔离环境和 trace 作为系统能力设计；不能只靠 prompt 或一次性代码生成。
- GitHub README、docs index warning 和站点弹窗均明确提示当前主要开发转向 mini-SWE-agent，并建议 going forward 使用 mini-SWE-agent；站点弹窗还写明 SWE-agent is now in maintenance-only mode。因此原 SWE-agent 更适合作为概念、论文和历史 reference，真实试跑应优先复核当前推荐工具 mini-SWE-agent。

## 支撑证据

- arXiv 页面于 2026-07-12 返回 HTTP 200；HTTP `last-modified` 为 2024-11-13。
- arXiv API 于 2026-07-12 返回 v3 元数据：published `2024-05-06T17:41:33Z`，updated `2024-11-11T20:01:15Z`，primary category `cs.SE`。
- 摘要写明 SWE-agent facilitates LM agents to autonomously use computers to solve software engineering tasks。
- 摘要写明 custom ACI enhances ability to create and edit code files, navigate entire repositories, and execute tests and other programs。
- 摘要报告 SWE-bench / HumanEvalFix pass@1 数字，但这些是论文时点结果，只能作为论文背景，不能写成当前本地能力或当前 leaderboard 事实。
- arXiv metadata comments 写明 code, data, and demo available at `https://swe-agent.com`。
- GitHub API 于 2026-07-12 显示 `SWE-agent/SWE-agent` 为 public、MIT、默认分支 `main`、language `Python`、`archived=false`、`updated_at=2026-07-11T20:21:13Z`、`pushed_at=2026-07-07T15:57:40Z`。
- GitHub README 写明 SWE-agent 可以 autonomously use tools to fix issues in real GitHub repositories，并提供 docs / usage / benchmarking links；同时警告 Most current development effort is on mini-swe-agent, which has superseded SWE-agent，并建议 use mini-SWE-agent going forward。
- `https://swe-agent.com/` 于 2026-07-12 返回 HTTP 200，`last-modified` 为 2026-07-07；`https://swe-agent.com/latest/` HTML 和 raw `docs/index.md` 都包含推荐 mini-swe-agent 的 warning，站点弹窗写明 SWE-agent is now in maintenance-only mode。
- `docs/usage/hello_world.md` 写明 `sweagent run` 需要模型 key，可针对 GitHub issue 运行，默认执行环境是 Docker sandbox，也可 modal / AWS fargate / 直接本机；它还说明运行过程包括 deployment、tools、prompts、main loop、submission，并保存 trajectory。
- `docs/background/architecture.md` 写明 SWE-agent 1.0 中 `SWEEnv` 是 SWE-ReX Deployment 的 thin wrapper，Deployment 可启动本地 Docker container 或远程系统，SWE-ReX 在容器内启动 shell session 并安装 ACI custom tools，Agent 通过 model output parser 提取 action 后交给 shell session 执行。

## 是否进入正文

- 结论：进入；作为 Software Engineering Agent / 实践路线 / repo issue 工作流的进阶 reference。
- 原因：它能支撑“真实代码库 Agent 需要专门接口、测试反馈和环境隔离”的学习边界；但不能证明某个当前模型、框架或 agent 在用户本地仓库中稳定可靠。

## 可能的问题

- README、docs banner 和站点弹窗当前推荐 mini-SWE-agent，且站点写明 SWE-agent is now in maintenance-only mode；原 SWE-agent 的工程入口不应作为初学者默认试跑路径。
- 论文中的 benchmark 数字来自当时版本、任务集和模型环境，不应写成当前能力事实。
- README 和 docs index 中的 SWE-bench / EnIGMA / open-source SOTA / performance claim 属于项目宣传或论文/leaderboard 时点信息；本手册不能把它们写成当前模型、当前本地安装或当前 GitHub issue 修复效果。
- 软件工程 Agent 涉及写文件、运行命令、安装依赖和可能访问敏感代码，真实试跑必须有 sandbox、只读/写权限分离、成本限制和回滚策略。
- `hello_world` 示例默认使用 Docker sandbox，但也提到可直接在本机运行；正文不能把“使用 SWE-agent”写成天然安全隔离，仍要明确 deployment、sandbox、API key、trajectory 和 patch 回滚边界。
- SWE-agent / mini-SWE-agent 能帮助学习 repo issue 工作流，但不能替代本手册中对权限、trace、eval 和人工确认的要求。

## 初学者阅读建议

- 先读本手册第 04、08、09 和 11 章，理解架构、eval、安全和实践路线。
- 阅读 SWE-agent 摘要时重点看 ACI 为什么重要：文件编辑、仓库导航、测试执行都是工具接口，不只是自然语言能力。
- 不建议初学者直接在重要仓库上运行软件工程 Agent；应先用 toy repo、只读任务或隔离 sandbox。

## 可复现实验

- 本手册已完成标准库 workflow / hybrid / ReAct-like 对比、planner/executor 对比和 trace-aware eval 实验，可作为 repo issue 任务实验设计的起点。
- Real Repo Issue Agent Toy 已完成固定 workflow baseline 和确定性 workflow-agent hybrid baseline：临时 toy repo 初始 `pytest` 失败，修复实现后通过，并记录 implementation-only diff、trajectory、人工审批和风险命令拒绝。后续真实实验应优先增加真实模型驱动 hybrid 和 mini-SWE-agent confirm-mode；若试跑 SWE-agent，应把它作为 maintenance-mode / historical tool 对照，记录 deployment、Docker/remote/local execution、文件读写、测试执行、失败原因、token、latency、cost、权限确认、patch 回滚和 trajectory 脱敏。
