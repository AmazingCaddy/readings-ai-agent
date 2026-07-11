# Real mini-SWE-agent CLI Surface Validation 实验

## 目标

验证 mini-SWE-agent 是否能作为临时依赖安装并暴露预期的本地 CLI / 默认配置表面，为第 11 章 Repo Issue Agent 进阶项目提供更稳的工具入口证据。

本实验只检查 import、`mini-swe-agent --help` 和包内 `mini.yaml`。它不运行 repo issue 修复任务，不调用模型，不读取真实仓库，不验证 benchmark、成本、延迟或 sandbox 隔离效果。

## 运行方式

```bash
uv run --with mini-swe-agent python docs/experiments/real-mini-swe-agent-cli-validation/real_mini_swe_agent_cli_validation.py
```

没有 `mini-swe-agent` 包时，脚本返回 `skipped`。

## 检查项

- 包版本可通过 `importlib.metadata` 读取。
- `mini-swe-agent --help` 返回成功。
- CLI help 暴露 `--model`、`--task`、`--yolo`、`--cost-limit`、`--config`、`--output`、`--agent-class`、`--environment-class` 等选项。
- 包内默认配置包含 `mode: confirm` 和 `cost_limit:`。
- 运行 help 时使用临时 `HOME` / `XDG_CONFIG_HOME` / `XDG_DATA_HOME`，避免依赖用户真实配置目录。
- trace / help 输出不泄露示例 secret marker。

## 支撑边界

可支撑：mini-SWE-agent 的本地 CLI 入口、confirm/yolo/cost/config/output 等配置表面和默认配置可以在本机临时依赖环境中复现。

不可支撑：mini-SWE-agent 能修复 toy repo issue、真实模型能稳定选择命令、confirm 模式的人工负担、sandbox 隔离、trajectory browser、token/cost/latency、SWE-bench 或真实 repo issue 成功率。

## 后续

下一步应在 Real Repo Issue Agent Toy 的同一 toy repo 上运行 mini-SWE-agent confirm-mode，记录模型、API key 配置方式、sandbox、人工确认次数、命令、diff、测试输出、trajectory、成本、延迟和失败原因。
