# Letta Documentation

- 来源链接：https://docs.letta.com/letta-agent/memory
- 作者 / 机构：Letta
- 发布时间：持续更新文档；页面 last-modified 复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：框架文档
- 主题：Agent Memory / Stateful Agents / MemGPT Ecosystem
- 适合阶段：工程实践
- 可信度等级：B
- 是否已验证：memory 页面已复核；长期记忆治理边界已完成第一轮交叉验证

## 一句话总结

Letta 是 MemGPT 相关生态的工程化文档，可用于观察长期记忆 agent 在框架层如何建模。

## 核心结论

- 文档描述 Letta Agent 可跨 sessions、days 或 months 使用同一个 agent，并记住历史交互、学习偏好和自编辑 memory。
- `/init` 用于初始化或刷新 memory；`/doctor` 用于审计 memory placement 和 token usage；`/remember` 支持用户显式指示写入记忆。
- dream subagents 可回顾近期对话并写入 lessons；memory defragmentation 会备份当前 memory、拆分大文件、合并重复内容并重构层级。
- MemFS 是 git-backed memory filesystem，提供 version history、conflict resolution、direct inspection/editing；本地 backend 需要备份以避免数据丢失。
- `system/` 中的 memory 总是进入 system prompt，其他文件按相关性加载；这支持“长期记忆需要分层和召回控制”的工程表述。

## 支撑证据

- 官方文档入口返回 HTTP 200。
- 2026-07-11 抓取 `https://docs.letta.com/letta-agent/memory.md` 成功；页面包含 `/init`、`/doctor`、`/remember`、dream subagents、memory defragmentation、MemFS、version history、conflict resolution 和 direct inspection/editing 等关键内容。
- 已与 MemoryBank、MemGPT、Generative Agents、Zep、OWASP 和 NIST 交叉验证长期记忆治理边界。

## 可能的问题

- 这是产品/框架文档，可信度按 B 级处理；可用于工程模式参考，不可单独作为效果收益证明。
- 文档中的具体命令和 MemFS 设计属于 Letta 实现，不应写成所有 Agent 框架必须采用的通用方案。

## 初学者阅读建议

- 先读 MemGPT 论文卡片，再把 Letta 当作工程化实现参考。

## 可复现实验

- 构建一个最小 stateful agent，记录 memory 写入、召回和更新路径。

## 是否进入正文

- 结论：作为工程资料进入
- 原因：Memory 章节需要工程治理案例，包括显式写入、审计、版本历史、冲突处理、可检查/可编辑和备份。
