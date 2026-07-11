# Real mini-SWE-agent Runtime Surface Validation 实验

## 目标

用 mini-SWE-agent 自带的 deterministic test model，在临时 toy repo 上验证真实 mini-SWE-agent agent / local environment / trajectory runtime surface。

本实验会创建临时 toy repo、运行 mini-SWE-agent `InteractiveAgent`、执行固定命令序列、修改 `discount.py`、跑 `pytest`，并写出 trajectory。它不调用真实模型，不进入人工 confirm 交互，不运行 SWE-bench，也不证明 repo issue 修复质量。

## 运行方式

```bash
uv run --with mini-swe-agent --with pytest python docs/experiments/real-mini-swe-agent-runtime-validation/real_mini_swe_agent_runtime_validation.py
```

缺少 `mini-swe-agent` 或 `pytest` 时，脚本返回 `skipped`。

## 检查项

- 临时 toy repo 初始测试失败。
- mini-SWE-agent `InteractiveAgent` + `LocalEnvironment` + `DeterministicModel` 能执行 5 个固定 action。
- action sequence 读取 issue / implementation、复现失败测试、只 patch `discount.py`、复跑测试并提交。
- 最终 `pytest` 通过，`git diff --name-only` 只包含 `discount.py`。
- trajectory 写出，格式为 `mini-swe-agent-1.1`，记录 `mini_version`、API calls 和 instance cost。
- 示例 env marker 会出现在 trajectory 中，因为 `LocalEnvironment` 会序列化配置的 env 值。

## 支撑边界

可支撑：mini-SWE-agent 的真实 runtime surface 可以在本地临时依赖环境中跑通 toy repo 命令执行、实现文件修改、测试反馈、trajectory 写出、模型调用计数和实例 cost 记录。也可支撑一个重要安全边界：不要把真实 secret 放进 `LocalEnvironment` env 配置或 trajectory 可见字段。

不可支撑：真实模型规划能力、confirm 模式人工确认负担、sandbox 隔离、成本准确性、SWE-bench、真实 repo issue 成功率、mini-SWE-agent 相对固定 workflow / hybrid / SWE-agent 的优劣。

## 后续

下一步应在同一 toy repo 上运行真实模型驱动的 mini-SWE-agent confirm-mode，并记录人工确认次数、拒绝/恢复、diff/rollback、测试反馈、trajectory、token、成本、延迟和失败原因。
