# Mem0 Documentation and Paper

- 来源链接：https://docs.mem0.ai/
  - https://docs.mem0.ai/llms.txt
  - https://github.com/mem0ai/mem0
  - https://arxiv.org/abs/2504.19413
- 作者 / 机构：Mem0
- 发布时间：持续更新文档；论文 arXiv v1 发布于 2025-04-28
- 最后复核日期：2026-07-12
- 类型：框架文档 / Source / Paper metadata
- 主题：Agent Memory / Long-term Memory / Memory Operations
- 适合阶段：工程实践
- 可信度等级：B
- 是否已验证：docs、`llms.txt`、GitHub repo metadata、README 和 arXiv metadata 已复核；可作为 memory CRUD、entity scope、expiration/history/export/events 和 OSS/Platform 边界的工程资料；真实 Mem0 API/SDK 行为和效果收益仍部分验证

## 一句话总结

Mem0 是一个长期记忆框架 / 平台资料，可用于观察现代 memory system 如何暴露增删查改、实体范围、过期、历史和导出等治理接口。

## 核心结论

- Mem0 文档把自身定位为 LLM agent 的 memory layer，Platform managed service 和 OSS/self-hosted 共享 add/search/get/update/delete 等基本 mental model。
- Platform Python `MemoryClient` 和 OSS Python `Memory` 均提供 `add`、`search`、`get_all`、`get`、`update`、`delete`、`delete_all` 等操作；这可作为长期记忆 lifecycle 操作面的工程参考。
- Platform REST `add memories` 要求至少提供一种 entity id，例如 `user_id`、`agent_id`、`app_id` 或 `run_id`；search/get 也通过 filters 绑定实体范围。这支持“长期记忆必须明确归属范围”的正文表述。
- 文档说明 `expiration_date` 会让过期记忆默认不出现在 search/get-all 中，但过期记忆仍存储，除非显式删除。这提醒初学者不要把“过期”误解成“删除”。
- 文档列出 memory history、feedback、export、events、webhooks、entity delete、organization/project access control 等接口面，可作为 inspect/edit/delete/audit/export 设计 checklist 的参考。
- README 同时区分 Platform、OSS library、self-hosted server 和 cloud platform；self-hosted auth 默认开启，`AUTH_DISABLED=true` 仅适合本地开发。
- README 和论文中的 LOCOMO 质量、延迟、token 改善数字只能作为 Mem0 作者/产品语境下的 claim，不能写成通用长期记忆收益，也不能外推到 OSS 默认表现。

## 支撑证据

- 2026-07-12 复核：`https://docs.mem0.ai/` 返回 308 到 `/introduction` 后 HTTP 200，响应头包含 `llms.txt`、`llms-full.txt`、OpenAPI、MCP 和 agent card 入口。
- 2026-07-12 抓取 `https://docs.mem0.ai/llms.txt` 成功；内容列出 Platform `MemoryClient` 和 OSS `Memory` 的 add/search/get_all/get/update/delete/delete_all 操作，并列出 entity-scoped memory、graph memory、temporal reasoning、memory decay、import/export、expiration、webhooks、feedback、history 和 organization/project access control 等文档入口。
- 2026-07-12 抽样复核 `llms-full.txt`：REST API 使用 `Authorization: Token <api-key>`；add memories 为 async operation 并返回 `event_id`；至少需要 `user_id`、`agent_id`、`app_id`、`run_id` 之一；search 支持 hybrid semantic + BM25 + entity matching、filters、`top_k`、threshold 和 rerank；expired memories 默认隐藏但可通过 `show_expired` 查询。
- 2026-07-12 复核 GitHub repo `mem0ai/mem0`：public、Apache-2.0、default branch `main`、archived false，topics 包含 `agents`、`ai-agents`、`long-term-memory`、`memory-management`、`rag` 和 `state-management`。
- 2026-07-12 抓取 raw README 成功；README 提供 `Memory()`、`memory.search(... filters={"user_id": user_id})`、`memory.add(... user_id=user_id)` 的基本示例，并说明 managed platform benchmark 使用 proprietary optimizations，OSS users should expect directionally similar gains but not identical numbers。
- 2026-07-12 复核 arXiv `2504.19413`：API 返回 `2504.19413v1`，标题为 `Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory`，published / updated 为 `2025-04-28T01:46:35Z`，primary category `cs.CL`，also `cs.AI`。摘要支持动态抽取、整合、检索 salient information 和 graph variant 的研究/产品设计语境，但 benchmark 数字未在本项目复现。
- 已与 MemoryBank、MemGPT、Generative Agents、LangGraph memory docs、Letta、Zep、OWASP、NIST 和本地 memory governance / lifecycle / LangGraph store harness 交叉验证长期记忆治理边界；Mem0 主要补充实际框架/平台 API surface，不单独提升真实效果结论状态。

## 可能的问题

- 这是产品文档、产品 README 和作者论文组合，可信度按 B 级处理；可用于接口和治理模式参考，不可单独作为独立效果证明。
- 文档和 README 中的 benchmark、latency、token、quality、production-ready 等 claim 未在本项目环境复现，不能写成正文确定性结论。
- Platform features、OSS library、self-hosted server 和 Cloud Platform 不能混用；managed platform 的 proprietary optimizations 不应外推到 OSS。
- 本项目没有实际运行 Mem0 API/SDK，也没有验证默认权限隔离、删除一致性、导出完整性、组织权限、隐私控制、成本、延迟或生产可靠性。
- 过期默认隐藏不等于物理删除；正文引用时应明确 expiration、delete、history/export/audit 是不同语义。

## 初学者阅读建议

- 先把它当作 memory lifecycle API checklist 阅读：add/search/update/delete、user/agent/run scope、expiration、history、export、events、access control。不要从 benchmark 数字直接推导“加长期记忆一定更好”。

## 可复现实验

- 用同一组多会话偏好、事实纠正、敏感信息和删除请求，对比 Mem0 OSS、LangGraph store、Letta/Zep 或标准库 governed memory 的写入守门、查看、编辑、删除、过期、历史、跨用户隔离、trace 脱敏、成本和延迟。

## 是否进入正文

- 结论：作为工程资料进入
- 原因：Memory 章节需要真实框架/平台的 lifecycle API 和实体范围案例；Mem0 可补充 CRUD、entity-scoped filters、expiration/history/export/events、OSS/Platform split 和 auth 边界。它不能证明长期记忆默认提升质量、默认安全、默认低延迟或默认生产可靠。
