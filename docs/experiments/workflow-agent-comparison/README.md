# Workflow、Hybrid 与 ReAct-like Tool Loop 对比实验

## 目标

验证第 01 章和第 04 章中的架构边界：Agent 和 Workflow 不是高低级替代关系，而是控制权、状态和决策方式不同。固定 workflow 更便宜、更可控；动态 tool loop 更适合需要根据中间证据继续行动的任务，但会增加工具调用、停止条件和 trace 要求。

## 实验边界

这是一个确定性的标准库实验，不调用模型、不接入真实 Agent framework。脚本比较三种策略：

- `fixed_workflow`：读取 issue 后按固定规则分类并输出建议，不额外查询 repo 文件。
- `workflow_agent_hybrid`：先用固定 workflow 分类，只在 bug 类任务进入受控的证据查询分支。
- `react_like_loop`：使用 ReAct-like 的“读 issue -> 决策 -> 搜索/读文件 -> 停止”循环；这里的决策是确定性规则，不是模型推理。

本实验不能证明 ReAct、LangGraph、OpenAI Agents SDK 或任何真实框架的表现。它只验证最小 trace、工具调用次数、失败类型和 workflow-agent hybrid 的工程边界说明。

## 输入数据

三类假 issue：

- 文档拼写问题：只读 issue 即可修复 README 命令。
- 登录超时 bug：需要读取 log、服务配置和部署环境才能定位 cache port mismatch。
- CSV 导出需求：属于 feature triage，不需要工程排障。

## 运行方式

```bash
uv run python docs/experiments/workflow-agent-comparison/workflow_agent_comparison.py
```

## 观察点

- 固定 workflow 在简单任务上是否足够。
- 固定 workflow 是否会漏掉需要中间证据的 bug root cause。
- Hybrid 是否能用固定路由限制动态查询范围。
- ReAct-like loop 是否能完成动态查询，但付出更多工具调用。
- Trace 是否记录 tool call、tool result、decision 和 stop reason。

## 结论状态

- 支撑：可以把“先从固定 workflow 或 workflow-agent hybrid 起步，再按任务需要引入 Agent loop”写入第 01/04 章。
- 支撑：比较架构时不应只看最终答案，还要看工具调用次数、失败类型、trace 可读性和停止条件。
- 仍缺：真实模型、真实 Agent framework、真实代码库、token/latency/cost、权限确认、错误恢复和人工评审实验。
