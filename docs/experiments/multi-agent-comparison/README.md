# 多 Agent 与 Flow 控制对比实验

## 目标

验证第 07 章和第 10 章中的多 Agent 边界：多 Agent 是一种编排方式，不是默认升级路径。角色拆分只有在任务边界、证据分配、冲突处理和 trace 可见时才可能有价值；否则会增加通信、重复读取和调试成本。

## 实验边界

这是一个确定性的标准库实验，不调用模型、不接入 AutoGen、CrewAI 或其他真实 Agent framework。脚本比较三种策略：

- `single_checklist`：单流程按 required docs 读取资料并写出结论。
- `ungoverned_multi_agent`：researcher、writer、reviewer 自行读取资料和传话，没有统一 Flow 控制。
- `flow_controlled_multi_agent`：Flow 先定义 required docs 和角色边界，再分配读取、写作和 review。

本实验不能证明真实多 Agent 框架的表现。它只验证最小的角色边界、重复读取、冲突处理、证据覆盖和消息开销。

## 输入数据

三类假写作任务：

- CSV export note：只需要 `spec.md`。
- 外部 CSV export launch note：需要 `spec.md`、`security.md` 和 `cost.md`。
- 初学者 CSV export tutorial note：需要 `spec.md` 和 `feedback.md`。

## 运行方式

```bash
uv run python docs/experiments/multi-agent-comparison/multi_agent_comparison.py
```

## 观察点

- 单流程 checklist 是否足够完成清晰任务。
- 无控制多 Agent 是否出现重复读取、缺证据和冲突。
- Flow 控制是否能保留角色分工，同时减少重复读取和冲突。
- 多 Agent 是否引入额外 messages，即使最终结果正确。

## 结论状态

- 支撑：可以把“多 Agent 不应作为默认起点；先用 Flow / workflow 控制，再在需要角色协作时引入 Agent team”写入第 07/10 章。
- 支撑：比较多 Agent 架构时应记录 success、tool calls、messages、conflicts、duplicate reads 和 missing evidence。
- 仍缺：真实模型驱动的 AutoGen/CrewAI/LangGraph 多角色流程、token/latency/cost、工具错误、人工评审和更复杂冲突处理实验。
