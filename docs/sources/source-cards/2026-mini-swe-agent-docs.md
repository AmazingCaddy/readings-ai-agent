# mini-SWE-agent Documentation and Source

- 来源链接：https://github.com/SWE-agent/mini-swe-agent
- 文档链接：https://mini-swe-agent.com/latest/
- README raw：https://raw.githubusercontent.com/SWE-agent/mini-swe-agent/main/README.md
- 关键文档 raw：`docs/quickstart.md`、`docs/usage/mini.md`、`docs/faq.md`、`docs/advanced/global_configuration.md`
- 关键源码 raw：`src/minisweagent/agents/default.py`、`src/minisweagent/agents/interactive.py`、`src/minisweagent/environments/local.py`、`src/minisweagent/config/mini.yaml`
- 最后复核日期：2026-07-12
- 类型：Source / Engineering Docs / Software engineering agent
- 主题：coding agent / repo issue agent / bash-only agent / trajectory / sandbox
- 适合阶段：进阶 / 实践扩展
- 可信度等级：A/B
- 是否已验证：GitHub 页面、raw README、官方文档 Markdown、默认 agent / interactive agent / local environment / config 源码已抽样复核；Real mini-SWE-agent CLI Surface Validation 已完成本地临时依赖 run，验证 `mini-swe-agent==2.4.5` 可导入、`mini-swe-agent --help` 暴露关键选项、默认配置包含 `mode: confirm` 和 `cost_limit:`；支撑 mini-SWE-agent 是当前 SWE-agent 系列中更推荐的轻量 coding agent 入口，并支撑 bash-only、线性 history、confirm / yolo / human 模式、trajectory、call/cost limit 和本地 / container sandbox 相关工程边界；Real Repo Issue Agent Toy 已完成固定 workflow baseline 和确定性 workflow-agent hybrid baseline，但尚未运行 mini-SWE-agent 修复 toy repo；真实 repo issue 成功率、benchmark claim、模型表现、成本、延迟和安全隔离效果仍部分验证

## 一句话总结

mini-SWE-agent 适合放在进阶实践路线里作为 repo issue / coding agent 的当前工具入口和最小基线：它故意把 agent scaffold 做得很薄，默认主要依赖 bash、线性 history、逐步命令执行和 trajectory，而不是复杂工具接口。

## 核心结论

- README 明确称 mini-SWE-agent 是 SWE-agent 团队当前更推荐的轻量实现，并在 “Should I use SWE-agent or mini-SWE-agent?” 中把 `mini-swe-agent` 作为默认选择。
- README 和 FAQ 都说明默认 mini 不使用除 bash 之外的工具，也不依赖 LLM tool-calling interface；这使它适合作为初学者理解 coding agent 最小控制流的参考。
- README、FAQ 和 `local.py` 源码共同支撑：默认动作通过 `subprocess.run` / `subprocess.Popen` 风格的独立命令执行，而不是维持一个长期 shell session；因此 `cd` 和环境变量不会跨 action 持久化。
- `usage/mini.md` 和 `interactive.py` 说明 `mini` 有 `confirm`、`yolo` 和 `human` 三种模式；默认配置为 `confirm`，`yolo` 会立即执行模型命令，风险更高。
- `default.py`、`global_configuration.md` 和 `mini.yaml` 支撑 step/cost/global call/cost limit、trajectory 保存和默认 cost limit 等工程边界。
- README、quickstart 和 FAQ 支撑它可通过 `uvx`、`pipx`、`pip` 或源码安装，可接 LiteLLM / OpenRouter 支持的模型，也可使用本地模型；但这些入口仍需本地试跑确认依赖和成本。

## 支撑证据

- GitHub repo 页面返回 HTTP 200；raw README 返回 HTTP 200，`content-type: text/plain; charset=utf-8`，`content-length: 11106`。
- 官方文档首页返回 HTTP 200，`last-modified: Mon, 06 Jul 2026 16:11:42 GMT`。
- README 写明 `mini` 是 minimal，agent class 约百行，并链接 default agent、environment、model 和 run script 源码。
- README 的动机段落写明默认不使用 bash 以外的工具、线性 history、每个 action 通过 `subprocess.run` 独立执行。
- FAQ 写明 mini-SWE-agent should work on any system with bash shell or container runtime，并再次说明默认没有 bash 以外工具、每个 action independent。
- `docs/usage/mini.md` 写明 `mini` 是本地环境 REPL-style interactive CLI，并定义 `confirm` / `yolo` / `human` 三种模式；默认从 `confirm` 开始。
- `src/minisweagent/agents/interactive.py` 的 `InteractiveAgentConfig` 默认 `mode="confirm"`，并在 `_ask_confirmation_or_interrupt` 中对非白名单命令请求确认。
- `src/minisweagent/environments/local.py` 写明 LocalEnvironment executes bash commands directly on the local machine，`_run` 使用 `subprocess.Popen(..., shell=True, cwd=..., env=..., timeout=...)`，超时会杀掉进程组。
- `src/minisweagent/config/mini.yaml` 提醒目录和环境变量变化不持久，每个 action 在新 subshell 中执行，并设置默认 `mode: confirm`、`cost_limit: 3.`。
- `docs/advanced/global_configuration.md` 记录 `MSWEA_GLOBAL_CALL_LIMIT`、`MSWEA_GLOBAL_COST_LIMIT` 和模型重试等配置项。
- Real mini-SWE-agent CLI Surface Validation 使用 `uv run --with mini-swe-agent ...` 完成本地临时依赖 run：package version `2.4.5`，CLI command `mini-swe-agent`，`--help` 返回 0，关键 options 包括 `--model`、`--task`、`--yolo`、`--cost-limit`、`--config`、`--output`、`--agent-class`、`--environment-class`，默认 config 中 `mode: confirm` 和 `cost_limit:` 存在，示例 secret marker 未出现在输出中。

## 是否进入正文

- 结论：进入；作为第 11 章 Repo Issue Agent 进阶项目和第 12 章 Software Engineering Agents 阅读路线的当前工具入口。
- 原因：它能补齐旧 SWE-agent 卡片的当前实现入口，并让实践路线更具体：先用 toy repo、确认模式、成本限制、trajectory 和 sandbox 练习 coding agent，而不是直接在重要仓库中运行全自动修复。

## 可能的问题

- README 中关于性能、采用方和 benchmark 的宣传性说法不能直接入正文；本次只把项目定位、控制流、模式、限制和源码可见的执行边界纳入证据。
- `yolo` 模式会跳过确认，初学者不应在真实仓库、真实凭据或重要文件上使用。
- 默认 LocalEnvironment 会在本机直接执行 bash 命令；如果没有 Docker、bubblewrap、contree、singularity/apptainer 或其他 sandbox 配置，不能假设它已经隔离。
- API key 可以写入全局 `.env`，这对长期使用方便，但学习材料应提示不要把真实 key 写入项目仓库或 trace。
- 本次只安装并验证了 mini-SWE-agent 的 CLI / 默认配置表面，没有运行 mini-SWE-agent 修复 toy repo，也没有验证真实模型、真实 repo issue、SWE-bench 得分、cost tracking、sandbox 实现或 trajectory browser 行为。Real Repo Issue Agent Toy 已完成固定 workflow baseline 和确定性 workflow-agent hybrid baseline：临时 toy repo 初始测试失败、实现修复后测试通过、记录 diff、trajectory、人工审批和风险命令拒绝；它是后续 mini-SWE-agent 对照组，不代表 mini-SWE-agent 表现。

## 初学者阅读建议

- 先读本手册第 03、08、09 和 11 章，理解工具执行、trace、安全和实践路线。
- 阅读 mini-SWE-agent 时优先看 Quick start、`mini` CLI、FAQ 和默认配置；先理解 confirm / yolo / human 的区别。
- 练习时用 toy repo、测试任务、`confirm` 模式、低 step/cost limit 和 git diff 回滚；不要用重要仓库或真实生产凭据做第一次实验。

## 可复现实验

- Real Repo Issue Agent Toy 已创建并运行固定 workflow baseline 和确定性 workflow-agent hybrid baseline；后续应在同一 toy repo 任务上增加真实模型驱动 hybrid、mini-SWE-agent confirm 和可选 SWE-agent 做同题对比。
- Real mini-SWE-agent CLI Surface Validation 已完成安装 / CLI / 默认配置表面检查；后续应继续升级到同一 toy repo 的 confirm-mode run。
- 最小记录项：安装方式、模型、API key 放置方式、sandbox、任务描述、文件读写、命令执行、测试输出、trajectory、人工确认次数、拒绝/恢复、diff、回滚、token、成本、延迟和失败原因。
