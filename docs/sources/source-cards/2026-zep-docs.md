# Zep Documentation

- 来源链接：https://help.getzep.com/overview
- 作者 / 机构：Zep
- 发布时间：持续更新文档
- 最后复核日期：2026-07-12
- 类型：框架文档 / Memory Platform
- 主题：Agent Memory / Knowledge Graph / Long-term Memory
- 适合阶段：工程实践
- 可信度等级：B
- 是否已验证：overview、concepts、retrieving context 和 facts 页面已复核；长期记忆治理窄边界可入正文；生命周期权限审计已完成标准库模拟；真实 Zep 行为仍部分验证

## 一句话总结

Zep 是 Agent memory 工程生态中的常见资料，可用于比较长期记忆、知识图谱和会话记忆实现方式。

## 核心结论

- Zep 文档把 agent memory 描述为从 chat、business data、documents、JSON 等来源构建 temporal knowledge graph / Context Graph。
- Context Graph 的节点是 entities，边是 facts/relationships；新数据到来时图会动态更新，并 invalidating outdated facts while preserving history。
- Context Block 可包含 user summary、相关 facts，以及 facts became valid / invalid 的日期。
- Context types 包括 facts、entities、episodes、thread summaries、observations 和 user summary。
- 默认情况下，添加到某个 user 任意 thread 的 messages 会被 ingested into that user's graph；这提醒初学者关注自动写入边界。
- `thread.get_user_context()` 虽然只需要 thread ID，但会用该 thread 的最新消息检索整个 User Graph，因此返回内容可能来自同一 user 的其他 threads；这提醒初学者把“同一用户跨 thread 记忆”和“当前 thread 短期上下文”分开治理。
- Zep 文档建议调用 LLM 时仍提供最近 4-6 条 thread messages，因为 ingestion 可能需要几分钟，Context Block 可能不包含最近消息；这支持“长期记忆不能替代短期原始上下文”的工程边界。
- Facts 存在 graph edges 上，包含 `created_at`、`valid_at`、`invalid_at` 和 `expired_at`；删除 facts 通过删除对应 graph data / edge 完成。
- Debug mode 可捕获 per-episode workflow logs；enterprise 还可捕获 selected ingestion steps 的 LLM reflection traces。

## 支撑证据

- 2026-07-12 复核：`https://help.getzep.com/` 返回 HTTP 307 并重定向到 `/overview`，最终 HTTP 200；`https://help.getzep.com/concepts` 返回 HTTP 200。
- 2026-07-12 抓取 `https://help.getzep.com/overview.md`、`https://help.getzep.com/concepts.md`、`https://help.getzep.com/retrieving-context.md` 和 `https://help.getzep.com/facts.md` 成功；concepts 页面包含 Context Graph、Fact Invalidation、Context Block、Context Types、Threads 和 Debug mode 等关键内容。
- `retrieving-context.md` 明确 `thread.get_user_context()` 使用给定 thread 的最新消息检索整个 User Graph，并说明 Context Block 可能来自该 user 的任意 thread；同页还说明 ingestion 可能需要几分钟，建议把最近 4-6 条 thread messages 作为 raw short-term context 一并提供。
- `facts.md` 明确 facts 是 Context Graph edges 上的精确、time-stamped relationships，包含 `valid_at` / `invalid_at`，新数据可能 invalidate 旧 fact 并创建新 facts，Context Block 会包含 date ranges。
- 已与 MemoryBank、MemGPT、Generative Agents、Letta、OWASP、NIST 和标准库 memory governance / lifecycle audit 实验交叉验证长期记忆治理边界；可支撑 temporal validity、fact invalidation、history 和 debug trace 等工程治理模式。
- 标准库 lifecycle audit 已把 fact invalidation、history、删除后召回、跨用户隔离和 trace 脱敏转化为最小验收项；该实验不验证 Zep 的真实实现行为。

## 可能的问题

- 产品文档可能有营销倾向，可信度按 B 级处理；可用来说明时间有效性、失效标记和 debug trace 等工程模式，不直接采信“减少幻觉/提升准确率”等效果宣传。
- 文档中的 sub-200ms、减少幻觉、提升准确率等性能/质量宣传未在本项目环境验证，不能写成正文确定性结论。
- 默认 ingest 用户 thread messages 的行为需要在正文中转化为“自动写入需要边界和用户控制”的风险提醒。
- 文档可证明 Zep 的文档化设计面，不证明真实 Zep API 行为、默认权限隔离、删除一致性、隐私控制、成本、延迟或生产可靠性。

## 初学者阅读建议

- 作为工程生态资料阅读，不作为 memory 概念定义来源。

## 可复现实验

- 设计一个用户事实更新和删除实验，观察 memory 系统如何处理冲突、过时信息、权限隔离和删除后召回。

## 是否进入正文

- 结论：作为补充进入
- 原因：Memory 工程生态需要覆盖；Zep 可支撑 temporal validity、fact invalidation、history 和 debug trace 等治理模式；不能把 Zep 的真实质量收益或默认安全性提前写成已验证。
