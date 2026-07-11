# 长期记忆写入守门与治理实验

## 目标

验证第 06 章中的长期记忆边界：长期记忆不是默认增益。自动写入会把推断、过时、冲突或敏感信息带入后续上下文；更稳妥的设计需要写入守门、冲突失效、版本历史和敏感字段脱敏。

## 实验边界

这是一个确定性的标准库实验，不调用模型、不接入真实 memory framework。脚本比较两种策略：

- `auto_write`：所有候选记忆直接写入。
- `guarded_write`：只接受用户明确表达、非敏感、高置信度的候选；拒绝模型推断、敏感信息和低置信事实。

本实验不能证明长期记忆会提升任务质量，也不能证明 Letta、Zep 或 LangGraph 的真实行为。它只验证写入策略、冲突处理、失效历史、污染标记和 trace 脱敏字段设计。

## 输入数据

候选记忆包括：

- 用户明确偏好：`language_preference=Chinese`。
- 模型低置信推断：`skill_level=beginner`。
- 敏感信息：`api_key=sk-example-secret`。
- 用户偏好变化：`language_preference=English`。
- 助手低置信猜测：`project_framework=LangChain`。
- 用户纠正事实：`project_framework=MkDocs`。

## 运行方式

```bash
uv run python docs/experiments/memory-governance/memory_governance.py
```

## 观察点

- `auto_write` 是否持久化敏感信息和低置信推断。
- `guarded_write` 是否拒绝敏感信息、模型推断和低置信事实。
- 偏好变化时是否 invalidates 旧版本。
- Trace 是否记录候选审查、写入、失效和拒绝原因。
- Guarded trace 是否避免泄露假 secret。

## 结论状态

- 支撑：可以把“长期记忆需要写入守门、冲突/失效处理、用户可纠错和敏感信息过滤”写入第 06 章。
- 仍缺：真实多会话 Agent、真实用户任务、真实 memory framework、收益指标、隐私权限和长期污染评测。
