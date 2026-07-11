# Voyager-style Toy Embodied Agent 实验

## 目标

验证第 04 章中 Voyager-style embodied lifelong agent 的工程边界：automatic curriculum、executable skill library、environment feedback、execution error、自我验证、skill reuse、sandbox 和 stop condition 应该如何进入 trace 和验收，而不是只写成“Agent 会自己学习”。

## 实验边界

这是一个确定性的 Python 标准库实验，不调用模型、不运行 Voyager 原仓库、不启动 Minecraft。它只用一个小型 toy environment 复现“任务 -> 动作 -> 环境反馈 -> 错误修正 -> 自我验证 -> 技能库写入/复用”的最小形状。

本实验不能证明 Voyager 论文结果、Minecraft 复现、真实 LLM 代码生成能力、开放式探索能力、技能迁移能力或生产可靠性。

## 输入数据

三个 curriculum task 按顺序执行：

- `TASK-1`：在森林中收集 wood。
- `TASK-2`：用已有资源制作 pickaxe。
- `TASK-3`：进入洞穴并用 pickaxe 挖 stone。

脚本比较三种策略：

- `no_skill_library`：没有技能库，只执行固定动作。
- `unverified_skill_library`：使用技能库，但失败技能也可能继续保留，暴露 skill pollution 风险。
- `governed_curriculum_skill_library`：使用 curriculum、环境反馈、错误修正、自我验证、只保存 verified skill，并在 unsafe action 被 sandbox 拒绝后修正技能。

## 运行方式

```bash
uv run python docs/experiments/voyager-style-toy-agent/voyager_style_toy_agent.py
```

## 观察点

- Trace 是否记录 `curriculum_task_started`、`skill_selected`、`action`、`environment_feedback`、`execution_error`、`skill_revised`、`self_verification`、`skill_stored` 和 `stop_condition`。
- 环境错误是否能触发技能修正。
- 只有自我验证通过的技能是否进入 verified skill library。
- unsafe action 是否被 sandbox 拒绝。
- step budget 是否作为停止条件进入 trace。

## 结论状态

- 支撑：可以把 Voyager-style Agent 解释为需要环境接口、动作执行、环境反馈、错误处理、自我验证、技能库治理、sandbox 和停止条件的长期循环。
- 支撑：技能库不是自动可靠资产；失败技能或 unsafe skill 必须经过验证、修正或拒绝，否则会污染后续任务。
- 仍缺：真实 Voyager / Minecraft 复现、真实模型生成/修正技能、真实成本/延迟、开放式探索质量、跨环境 skill transfer、长期 skill library 污染率和生产隔离验证。
