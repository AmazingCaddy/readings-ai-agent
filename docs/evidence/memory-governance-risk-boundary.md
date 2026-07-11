# Evidence Note: 长期记忆治理与风险边界

## 要验证的结论

长期记忆可能提升持续交互、个性化和跨会话任务体验，但它不是默认增益。长期记忆一旦写入错误、过时、冲突或敏感信息，就可能污染后续任务；因此工程上需要写入守门、可检查/可编辑、版本或历史、冲突处理、过期/失效标记和隐私边界。

## 资料来源

- Source 1：[MemoryBank: Enhancing Large Language Models with Long-Term Memory](../sources/source-cards/2023-memorybank-paper.md)
- Source 2：[MemGPT: Towards LLMs as Operating Systems](../sources/source-cards/2023-memgpt-paper.md)
- Source 3：[Generative Agents: Interactive Simulacra of Human Behavior](../sources/source-cards/2023-generative-agents-paper.md)
- Source 4：[Letta Documentation](../sources/source-cards/2026-letta-docs.md)
- Source 5：[Zep Documentation](../sources/source-cards/2026-zep-docs.md)
- Source 6：[OWASP LLM Top 10](../sources/source-cards/2026-owasp-llm-top-10.md)
- Source 7：[NIST AI Risk Management Framework](../sources/source-cards/2026-nist-ai-rmf.md)
- Source 8：[长期记忆写入守门与治理实验结果](../experiments/memory-governance/results-2026-07-11.md)
- Source 9：[长期记忆生命周期与权限审计实验结果](../experiments/memory-lifecycle-audit/results-2026-07-11.md)

## 交叉验证结果

- 一致点：MemoryBank 摘要支持长期记忆在持续交互、用户画像适应和 companion / counseling 类场景中的潜在价值，并明确包含记忆更新、遗忘和强化机制。
- 一致点：MemGPT 摘要支持“上下文窗口之外需要显式 memory management”的研究方向，并把多会话聊天列为评估场景之一。
- 一致点：Generative Agents 摘要支持“记录经验、生成反思、动态检索记忆并用于规划”这类 memory-reflection-planning 架构，但其目标是 believable behavior，不等同于生产可靠性。
- 一致点：Letta 文档把长期运行的 agent memory 工程化为 persisted state/database、core memory blocks、agent/tool/API 可编辑 memory blocks、messages/conversations、`/remember`、`/doctor`、git-backed MemFS、version history、conflict resolution 和 direct inspection/editing 的体系。这支持“长期记忆需要治理机制、层次划分和可检查/可编辑路径，而不只是自动写入”的正文表述。
- 一致点：Zep 文档把 agent memory 建模为 temporal Context Graph，并说明过时 fact 会被 invalidated，Context Block 可以包含 fact 生效/失效日期；`thread.get_user_context()` 会用给定 thread 的最新消息检索整个 User Graph，可能返回同一 user 其他 threads 的 context；ingestion 可能需要几分钟，因此仍建议把最近 4-6 条 thread messages 作为 raw short-term context 提供。这支持“长期记忆需要处理过时、冲突、时间有效性、跨 thread 边界和短期上下文分层”的正文表述。
- 一致点：OWASP GenAI LLM Top 10 2025 archive 中的 `LLM02: Sensitive Information Disclosure` 和 `LLM08: Vector and Embedding Weaknesses` 支持长期记忆系统需要隐私、访问控制、跨用户隔离和检索/嵌入泄露边界；`LLM06: Excessive Agency` 也支持不要让带记忆访问能力的 Agent 获得过宽工具权限。
- 一致点：NIST AI RMF 支持把 AI 风险放到 design、development、use 和 evaluation 的治理流程中处理，而不是把 memory 风险视为单点 prompt 问题。
- 边界：论文主要支撑“长期记忆可能有价值”和“需要记忆管理机制”；产品文档主要支撑具体工程治理模式；安全资料支撑隐私和权限风险。三类资料互补，但不能单独证明“长期记忆一定提升 Agent 表现”，也不能证明 Letta/Zep 的真实实现默认安全、默认低延迟、默认低成本、默认删除一致或默认适合生产。
- 本地实验：标准库 memory governance 模拟中，`auto_write` 持久化了假 secret 和低置信模型推断，并在 trace 中泄露假 secret；`guarded_write` 拒绝敏感信息、低置信推断和助手猜测，保留用户明确偏好/纠正事实，并在偏好变化时 invalidates 旧版本。这支持“长期记忆需要写入守门、失效历史和 trace 脱敏”的工程建议。
- 本地实验：标准库 memory lifecycle audit 中，`naive_memory` 只通过 1/6 个操作，暴露了跨用户 inspect / recall、编辑无历史、删除不生效、删除后仍召回和 trace 泄露等失败模式；`governed_memory` 通过 6/6 个操作，覆盖跨用户阻断、旧版本 invalidated、敏感记录 deleted、删除后不召回和 trace 脱敏。这支持“长期记忆需要用户可查看/可编辑/可删除、权限隔离和删除语义”的工程建议。

## 实验验证

- 是否需要实验：是
- 实验设计：设计一个多会话学习助手任务，比较三个 baseline：无长期记忆、用户显式确认写入的长期记忆、模型自动写入的长期记忆。测试偏好变化、错误事实写入、旧偏好过期、敏感信息误写入、用户查看/编辑/删除、跨用户访问和后续任务污染。
- 指标：个性化命中率、错误记忆写入率、过时记忆使用率、用户可纠错性、删除后召回率、跨用户泄露率、敏感信息进入上下文次数、最终任务质量。
- 结果：已完成标准库最小写入守门模拟实验和生命周期权限审计实验。实验覆盖自动写入、显式写入守门、敏感信息拒绝、低置信推断拒绝、用户偏好变化、事实纠正、失效历史、inspect/edit/delete/recall 权限、跨用户阻断和 trace 脱敏。尚未覆盖真实多会话 Agent、真实 memory framework、收益指标或长期污染评测。

## 结论状态

- 可入正文：窄结论“长期记忆可能适合持续交互、个性化和跨会话任务，但必须配套写入守门、冲突/失效处理、用户可检查/可编辑/可删除、跨用户权限隔离、短期/长期上下文分层和敏感 trace 脱敏；不能默认自动写入或默认提升表现”已完成第一轮交叉验证。论文支撑长期记忆和显式 memory management 的潜在价值，Letta/Zep 支撑检查、编辑、版本/失效、temporal fact、cross-thread retrieval 和 ingestion delay 等工程模式，OWASP 2025 LLM02/08 和 NIST 支撑隐私、检索/嵌入泄露、访问控制和风险治理边界，标准库实验复现了自动写入敏感信息、低置信推断、跨用户访问、删除后召回和 trace 泄露等失败模式。
- 部分验证：真实多会话 Agent 和 memory framework 的质量收益、污染率、用户控制体验、持久化、权限 UI、删除一致性、成本、延迟和隐私控制仍缺真实实验；不能写成“长期记忆一定提升表现”或“某个 memory framework 默认安全”。

## 可进入章节

- 是。可以确定写成：长期记忆可能适合持续交互、个性化和跨会话任务，但它会引入错误写入、过时、冲突、权限、短期/长期上下文混用和隐私风险。初学者不应默认加长期记忆，应先设计写入守门、用户可检查/可编辑/可删除、跨用户隔离、过期/冲突处理、短期原始上下文保留、trace 脱敏和评测。
