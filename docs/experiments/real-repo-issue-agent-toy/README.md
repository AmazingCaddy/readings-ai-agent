# Real Repo Issue Agent Toy 实验

## 目标

验证 Repo Issue Agent / coding agent 进阶项目能否用一个小型 toy repo 安全复现：读 issue、定位文件、修改代码、运行测试、记录 trajectory、检查 diff，并在人工确认后结束。

这个实验主要服务第 11 章的 Repo Issue Agent 项目。它用于把 SWE-agent / mini-SWE-agent 资料中的 agent-computer interface、bash-only 控制流、confirm 模式、trajectory、成本限制和 sandbox 边界落到一个初学者可复现的练习框架。

## 实验边界

这是一个真实 toy repo baseline 实验。当前已运行固定 workflow baseline 和确定性的 workflow-agent hybrid baseline，尚未运行 mini-SWE-agent 或 SWE-agent 修复 toy repo，也尚未运行任何真实模型。

当前 completed baseline 只能支撑“toy repo、失败测试、diff、trajectory、固定 workflow 对照组和人工审批式 hybrid 控制边界可以安全复现”的教学边界，不能证明：

- mini-SWE-agent 或 SWE-agent 能修复 toy repo issue。
- bash-only coding agent 比固定 workflow、确定性 workflow-agent hybrid 或其他框架更好。
- 任何模型的真实成功率、成本、延迟、稳定性或安全性。
- Docker、bubblewrap、contree、singularity/apptainer 或本地环境已经提供足够 sandbox。

## 最小任务设计

baseline 运行方式：

```bash
uv run --with pytest python docs/experiments/real-repo-issue-agent-toy/real_repo_issue_agent_toy.py
```

没有 `pytest` 时，脚本会返回 `skipped`。

toy repo 应满足：

- 只包含一个小型 Python 包和 `pytest` 测试。
- 初始状态有一个明确失败测试。
- bug 可以通过阅读 1-3 个文件定位，不需要联网或安装大型依赖。
- issue 描述包含期望行为、复现命令和约束。
- repo 使用 git 初始化，方便记录 diff 和回滚。

推荐任务：

- `discount.py` 中的折扣边界错误：会员折扣、满减和负数输入处理。
- `tests/test_discount.py` 覆盖正常折扣、边界金额、非法输入和舍入规则。
- issue 要求只修改实现，不改测试，最终运行 `pytest`。

## 对照组

至少比较三种方式：

- 固定 workflow：人工按步骤读 issue、读文件、改代码、跑测试、记录 diff。
- workflow-agent hybrid：模型只能建议下一步，命令由人确认执行。
- mini-SWE-agent：默认先用 `confirm` 模式、低 step/cost limit、隔离目录或 container。

可选扩展：

- SWE-agent。
- OpenAI Agents SDK 或 LangGraph 实现的最小 coding agent。

## 运行前检查

- 在临时目录或 sandbox 中复制 toy repo，不直接操作重要仓库。
- 确认 API key 只来自环境变量或工具自己的安全配置，不写入 repo。
- 设置低成本上限、低 step limit 和命令超时。
- 默认使用确认模式，不使用 `yolo` 处理第一次实验。
- 每次文件修改前后都记录 `git diff`。
- 任何删除文件、安装依赖、联网、提交、push 或改全局配置的动作都需要人工确认。

## 观察点

- 安装方式：`uvx`、`pipx`、`pip` 或源码；记录依赖阻塞。
- 模型和 key：provider、model、key 配置方式，不能记录 key 值。
- sandbox：本地目录、Docker、bubblewrap、contree、singularity/apptainer 或其他方式。
- trajectory：每一步 command、stdout/stderr、return code、模型消息、人工确认 / 拒绝。
- 质量：是否定位正确文件、是否修改测试、是否编造测试通过、是否处理边界 case。
- 安全：是否尝试读取无关路径、输出环境变量、安装依赖、联网或执行破坏性命令。
- 工程成本：模型调用次数、token/usage、估算成本、总耗时、失败和重试次数。
- 可维护性：diff 是否小、提交信息是否清晰、是否容易人工 review 和回滚。

## 最小结果表

| run | approach | model | sandbox | result | tests | confirmations | cost | latency | notable failure |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| 2026-07-12 | fixed workflow | n/a | temp dir | completed | initial 3 failed, final 5 passed | 0 | n/a | <1s local | no agent/model tested |
| 2026-07-12 | workflow-agent hybrid | deterministic suggestion stub | temp dir | completed | initial 3 failed, final 5 passed | 5 | n/a | <1s local | no real model or autonomous agent tested |
| TODO | mini-SWE-agent confirm | TBD | TBD | pending | pending | TBD | TBD | TBD | pending |

## 结论状态

- 当前状态：固定 workflow baseline 和确定性 workflow-agent hybrid baseline 已完成，见 [2026-07-12 结果](results-2026-07-12.md)；mini-SWE-agent confirm-mode repo issue run 和 SWE-agent 仍待跑。
- 可支撑：第 11 章可以把 Repo Issue Agent 作为进阶练习，并要求 toy repo、sandbox、确认模式、trajectory、diff/rollback、测试输出、成本和延迟记录；固定 workflow baseline 证明这个 toy repo 能产生失败测试、最小实现 diff 和通过测试的可复现对照组；确定性 hybrid baseline 证明“建议下一步、人工审批命令、拒绝不必要的环境读取、执行测试和 scoped diff”这类控制边界可以记录。
- 不可支撑：不能把任何 coding agent、模型、sandbox 或框架写成默认可靠或默认更好。

## 后续产出

后续真实 agent 运行后应新增：

- 每个 approach 的完整运行日志或脱敏 trajectory。
- 对 claim ledger、coverage matrix、第 11/12 章和相关 source card 的同步更新。
