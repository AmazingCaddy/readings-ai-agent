# Zep Documentation

- 来源链接：https://help.getzep.com/overview
- 作者 / 机构：Zep
- 发布时间：持续更新文档
- 最后复核日期：2026-07-11
- 类型：框架文档 / Memory Platform
- 主题：Agent Memory / Knowledge Graph / Long-term Memory
- 适合阶段：工程实践
- 可信度等级：B
- 是否已验证：overview 和 concepts 页面已复核；长期记忆治理边界已完成第一轮交叉验证；生命周期权限审计已完成标准库模拟

## 一句话总结

Zep 是 Agent memory 工程生态中的常见资料，可用于比较长期记忆、知识图谱和会话记忆实现方式。

## 核心结论

- Zep 文档把 agent memory 描述为从 chat、business data、documents、JSON 等来源构建 temporal knowledge graph / Context Graph。
- Context Graph 的节点是 entities，边是 facts/relationships；新数据到来时图会动态更新，并 invalidating outdated facts while preserving history。
- Context Block 可包含 user summary、相关 facts，以及 facts became valid / invalid 的日期。
- Context types 包括 facts、entities、episodes、thread summaries、observations 和 user summary。
- 默认情况下，添加到某个 user 任意 thread 的 messages 会被 ingested into that user's graph；这提醒初学者关注自动写入边界。
- Debug mode 可捕获 per-episode workflow logs；enterprise 还可捕获 selected ingestion steps 的 LLM reflection traces。

## 支撑证据

- `https://help.getzep.com/` 重定向到 `/overview` 并返回 HTTP 200。
- 2026-07-11 抓取 `https://help.getzep.com/overview.md` 和 `https://help.getzep.com/concepts.md` 成功；concepts 页面包含 Context Graph、Fact Invalidation、Context Block、Context Types、Threads 和 Debug mode 等关键内容。
- 已与 MemoryBank、MemGPT、Generative Agents、Letta、OWASP 和 NIST 交叉验证长期记忆治理边界。
- 标准库 lifecycle audit 已把 fact invalidation、history、删除后召回、跨用户隔离和 trace 脱敏转化为最小验收项；该实验不验证 Zep 的真实实现行为。

## 可能的问题

- 产品文档可能有营销倾向，可信度按 B 级处理；可用来说明时间有效性、失效标记和 debug trace 等工程模式，不直接采信“减少幻觉/提升准确率”等效果宣传。
- 默认 ingest 用户 thread messages 的行为需要在正文中转化为“自动写入需要边界和用户控制”的风险提醒。

## 初学者阅读建议

- 作为工程生态资料阅读，不作为 memory 概念定义来源。

## 可复现实验

- 设计一个用户事实更新和删除实验，观察 memory 系统如何处理冲突、过时信息、权限隔离和删除后召回。

## 是否进入正文

- 结论：作为补充进入
- 原因：Memory 工程生态需要覆盖；Zep 可支撑 temporal validity、fact invalidation、history 和 debug trace 等治理模式。
