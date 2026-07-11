# Letta Documentation

- 来源链接：https://docs.letta.com/letta-agent/memory
- 作者 / 机构：Letta
- 发布时间：持续更新文档；页面 last-modified 复核为 2026-07-11
- 最后复核日期：2026-07-12
- 类型：框架文档
- 主题：Agent Memory / Stateful Agents / MemGPT Ecosystem
- 适合阶段：工程实践
- 可信度等级：B
- 是否已验证：stateful agents 与 Letta Agent memory 页面已复核；旧 memory guide URL 跳转已记录；长期记忆治理窄边界可入正文；生命周期权限审计已完成标准库模拟；真实 Letta 行为仍部分验证

## 一句话总结

Letta 是 MemGPT 相关生态的工程化文档，可用于观察长期记忆 agent 在框架层如何建模。

## 核心结论

- 文档描述 Letta Agent 可跨 sessions、days 或 months 使用同一个 agent，并记住历史交互、学习偏好和自编辑 memory。
- Stateful agents 页面说明 Letta 会把 state、memories、user messages、reasoning 和 tool calls 持久化到 database，core memories 会进入 context window，agent 可通过 tools 修改自身 memories。
- Memory blocks 可由 agent memory tools 编辑，也可由 developer API 直接编辑；attached blocks 会进入 context，blocks 可以 attach/detach 并被多个 agents 共享。
- `/init` 用于初始化或刷新 memory；`/doctor` 用于审计 memory placement 和 token usage；`/remember` 支持用户显式指示写入记忆。
- dream subagents 可回顾近期对话并写入 lessons；memory defragmentation 会备份当前 memory、拆分大文件、合并重复内容并重构层级。
- MemFS 是 git-backed memory filesystem，提供 version history、conflict resolution、direct inspection/editing；本地 backend 需要备份以避免数据丢失。
- `system/` 中的 memory 总是进入 system prompt，其他文件按相关性加载；这支持“长期记忆需要分层和召回控制”的工程表述。
- 同一个 agent 可以有多个 conversation；旧 messages 在 compaction / eviction 后仍可由 API 或 retrieval tools 取回。这个边界支撑“conversation thread、agent state 和长期记忆不是同一层”的正文解释。

## 支撑证据

- 2026-07-12 复核：`https://docs.letta.com/guides/agents/memory` 返回 HTTP 308，并跳转到 `https://docs.letta.com/guides/core-concepts/stateful-agents`；最终页面 HTTP 200，`last-modified: Sat, 11 Jul 2026 02:30:05 GMT`。旧 URL 不能继续当作独立 memory guide 内容引用。
- 2026-07-12 复核：`https://docs.letta.com/letta-agent/memory` 返回 HTTP 200，`last-modified: Sat, 11 Jul 2026 01:02:45 GMT`。
- 2026-07-12 抓取 `https://docs.letta.com/guides/core-concepts/stateful-agents.md` 成功；页面包含 persistent state/database、core memories、memory blocks、tools、messages、runs/steps 和 conversations 等关键内容。
- 2026-07-12 抓取 `https://docs.letta.com/letta-agent/memory.md` 成功；页面包含 `/init`、`/doctor`、`/remember`、dream subagents、memory defragmentation、MemFS、version history、conflict resolution、direct inspection/editing、`system/` always-loaded memory 和 git synchronization 等关键内容。
- `https://docs.letta.com/llms.txt` 也确认 Letta 把 persistent memory 分为 in-context blocks 与 archival/RAG，并提供 REST API / Python / TypeScript SDK、agent blocks、passages、conversations 和 memory docs 入口。
- 已与 MemoryBank、MemGPT、Generative Agents、Zep、OWASP、NIST 和标准库 memory governance / lifecycle audit 实验交叉验证长期记忆治理边界；可支撑显式写入、审计、版本历史、冲突处理和可检查/可编辑等工程模式。
- 标准库 lifecycle audit 已把 direct inspection/editing、版本历史、删除语义、权限隔离和 trace 脱敏转化为最小验收项；该实验不验证 Letta 的真实实现行为。

## 可能的问题

- 这是产品/框架文档，可信度按 B 级处理；可用于工程模式参考，不可单独作为效果收益证明。
- 文档中的具体命令和 MemFS 设计属于 Letta 实现，不应写成所有 Agent 框架必须采用的通用方案。
- 文档可证明 Letta 的文档化设计面，不证明当前本地环境真实部署行为、memory 写入质量、权限默认安全、删除一致性、成本、延迟或生产可靠性。

## 初学者阅读建议

- 先读 MemGPT 论文卡片，再把 Letta 当作工程化实现参考。

## 可复现实验

- 构建一个最小 stateful agent，记录 memory 写入、查看、编辑、删除、召回、权限阻断和更新路径。

## 是否进入正文

- 结论：作为工程资料进入
- 原因：Memory 章节需要工程治理案例，包括显式写入、审计、版本历史、冲突处理、可检查/可编辑和备份；不能把 Letta 的真实实现效果或安全性提前写成已验证。
