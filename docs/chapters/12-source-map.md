# 论文、文档与资料地图

## 本章适合谁

如果你想继续深入学习 AI Agent，但不想被资料海淹没，这一章适合阅读。

本章把当前资料库按主题整理，并说明每类资料适合什么时候读、应该怎样读、哪些结论仍需验证。

## 你会学到什么

- 如何区分论文、官方文档、框架文档、源码和安全指南。
- 初学者应该按什么顺序读资料。
- 当前手册的 source cards 覆盖了哪些主题。
- 哪些资料已可支撑正文，哪些还只是候选。
- 如何继续扩展资料库而不降低正确性。

## 先用一句话理解

资料地图不是链接收藏夹，而是把资料按主题、可信度、学习阶段和验证状态组织起来。

## 资料类型

### 论文

论文适合理解一个想法的来源、实验设置和研究边界。

但论文不等于工程最佳实践。很多论文使用的模型、环境和 API 已经过时，不能直接搬到生产系统。

### 官方 API 文档

官方 API 文档适合理解当前接口、参数、限制和推荐用法。

它通常最接近实际开发，但可能不解释完整背景。初学者应先读手册概念，再把 API 文档当查询资料。

### 框架文档

框架文档适合理解工程抽象和实践路径。

但框架文档会带有产品定位，也会随版本变化。引用时要记录复核日期，并避免把框架术语当成行业通用定义。

### 源码和示例

源码和示例适合学习可运行结构、目录组织、错误处理和测试方式。

但示例往往简化了权限、部署、成本和安全边界，不能直接代表生产方案。

### 安全和治理指南

安全和治理指南适合建立风险意识、检查清单和上线前审查方法。

它们通常不是 Agent 专用教程，需要和具体工具、数据流、权限模型结合。

## 按主题阅读

### Agent 基础与架构

先读手册 01 和 04，再看 ReAct、Reflexion、Tree of Thoughts 和 LangGraph 文档。

阅读重点不是记住所有方法名，而是理解：模型如何在观察、行动、状态和反馈之间循环。

### LLM 接口与工具调用

先读手册 02 和 03，再看 Responses API、Function Calling docs 和 Toolformer。

阅读重点是区分：模型生成工具调用参数，应用程序执行工具，工具结果再回到模型上下文。
Tool Calling 参数校验与重试的标准库模拟实验已经完成，可帮助理解应用层校验、错误回传、有限重试和 trace 字段；真实模型 / API 稳定性仍需后续实验。

### MCP 与工具生态

先读手册 05，再看 MCP official docs 和 MCP servers repo。

阅读重点是 host、client、server、tools、resources、prompts、authorization、roots、elicitation、sampling 和权限边界。尤其要注意：authorization 是 optional transport-level capability，roots 不等于 sandbox，token passthrough 被官方安全最佳实践禁止。

### RAG 与 Memory

先读手册 06，再看 RAG paper、LlamaIndex、LangGraph memory、MemGPT、MemoryBank、Generative Agents、Letta 和 Zep。

阅读重点是区分外部知识检索、短期状态、长期记忆、写入守门和隐私风险。
RAG 最小 pipeline / citation 标准库模拟实验已经完成，可帮助理解 chunk metadata、retrieval trace、chunk-level citations 和无证据拒答；真实 embedding / vector store / LLM synthesis 仍需后续实验。

### Planning、Orchestration 与多 Agent

先读手册 07，再看 Tree of Thoughts、Reflexion、AutoGen、CrewAI 和 LangGraph。

阅读重点是任务拆解、状态管理、反馈、重规划、角色协作和成本。

### Evaluation 与 Observability

先读手册 08，再看 AgentBench、WebArena、OpenAI Evals、LangSmith 和 Phoenix。

阅读重点是任务环境、trajectory、trace、offline/online eval、regression set、datasets、feedback 和错误分类。

### Production、安全与治理

先读手册 09，再看 OWASP LLM Top 10、NIST AI RMF、OpenAI Agents SDK guardrails / human-in-the-loop / tracing 文档，以及 Semantic Kernel Plugins 文档。

阅读重点是 prompt injection、权限、工具审批、guardrails 的执行位置、数据边界、审计、人工确认、降级、敏感 trace 控制和风险管理。

### 框架生态与实践

先读手册 10 和 11，再横向阅读 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI、Semantic Kernel 和 OpenAI Cookbook 的具体 recipe。

阅读重点是选择维度、可迁移概念和可复现练习，而不是追随单一框架或照搬复杂 demo。

## 当前 Source Card 状态

当前资料库已经覆盖这些大类：

- Agent 架构：ReAct、Reflexion、Tree of Thoughts、LangGraph。
- Tool Use：Toolformer、OpenAI Function Calling docs、Responses API docs。
- MCP：MCP official docs、MCP servers repo。
- RAG：RAG paper、LlamaIndex。
- Memory：MemGPT、MemoryBank、Generative Agents、LangGraph memory、Letta、Zep。
- Eval / Observability：AgentBench、WebArena、OpenAI Evals repo、LangSmith、Phoenix。
- Security / Production：OWASP LLM Top 10、NIST AI RMF、OpenAI Agents SDK、Semantic Kernel。
- Frameworks：OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI、Semantic Kernel。
- Practice：OpenAI Cookbook、MCP servers repo、OpenAI Evals repo。

核心 source cards 已经完成多轮链接、元数据和关键段落复核，能支撑章节中的学习方向、术语边界和部分验证结论。OpenAI Cookbook 已完成 Structured Outputs、File Search RAG、OpenAI Evals、Agents SDK trace/eval、Usage/Cost 和 Rate limits 等具体 recipe 的第一轮复核，可支撑实践项目参考。仍处于候选或只完成链接复核的资料，不能支撑过强的工程断言。

## 如何继续扩展资料库

新增资料时，先问五个问题：

1. 资料来自谁？官方、论文、源码、框架团队、个人博客还是营销材料？
2. 它解决哪个主题？是否补齐当前覆盖矩阵缺口？
3. 链接和元数据是否可验证？
4. 核心结论是否能被另一个独立来源或实验支撑？
5. 初学者是否应该现在读，还是放到进阶资料？

只有通过这些问题的资料，才适合进入 source cards。只有完成精读和交叉验证的结论，才适合迁移到正文。

## 常见误区

- 误区一：资料越多越好。没有验证状态的资料会增加噪声。
- 误区二：论文结论可以直接当工程建议。研究环境和生产环境不同。
- 误区三：官方文档永远完整。官方文档可能偏 API 细节，缺少学习路径。
- 误区四：框架示例就是生产方案。示例通常省略权限、审计和回滚。
- 误区五：只看最新资料。经典论文和协议文档仍然能提供概念源头。

## 已验证结论

- 当前手册已经建立 source card index、coverage matrix 和 claim ledger，用于控制资料进入正文的门槛。
- Source card index 明确记录了每张卡片的可信度、验证状态和下一步。
- Coverage matrix 显示 Evaluation / Observability 已补 LangSmith 和 Phoenix 第一轮工程资料，但仍缺本地 trace-aware eval 实验；Production / Security 已补 OpenAI Agents SDK 和 Semantic Kernel 第一轮工程资料，但仍需要最小 prompt injection / tool permission 实验、跨框架权限对比和审计脱敏策略。
- MCP official docs 已补 2025-11-25 tools/resources/prompts/authorization/roots/elicitation/sampling spec 和 Security Best Practices 第一轮精读；MCP 最小 trace 标准库模拟实验已完成，可支撑最小审计字段和职责流设计；仍缺真实 MCP SDK / host trace、权限确认、URL mode / OAuth、恶意 resource/prompt 和 host 实现差异实验。
- Tool Use / Function Calling 已补标准库参数校验/重试模拟实验，可支撑“应用层校验、错误回传、有限重试”的流程说明；仍缺真实 Function Calling / Responses API 实验和其他框架术语对照。
- RAG 已补标准库最小 pipeline / citation 模拟实验，可支撑 chunk metadata、retrieval trace、chunk-level citations 和 `grounded=false` 拒答流程；仍缺真实 embedding / vector store / LLM synthesis、chunk size/top-k/rerank 对比、citation correctness 和成本/延迟实验。
- Cookbook 的具体 recipe 已能支撑实践项目路线，但仍需要本地试跑来确认依赖、成本、失败样例和初学者阻塞点。
- Claim ledger 规定只有状态为“可入正文”的结论，才能写成确定性表述；其他结论需要保守表达。

## 待验证问题

- prompt injection / tool permission 的最小攻击实验应该如何覆盖 guardrails、HITL approval、敏感 trace 和审计字段？
- 真实 MCP SDK / host trace 实验应如何覆盖 `tools/list`、`tools/call`、`resources/list`、`resources/read`、用户拒绝、roots、URL mode elicitation 和敏感日志脱敏？
- 真实 Function Calling / Responses API 实验中，模型能否稳定根据 tool validation error 修正参数？不同框架如何表示 tool execution error？
- 真实 RAG stack 中，chunk size、top-k、rerank/filter 和 LLM synthesis 如何影响 citation correctness、faithfulness、latency 和 token cost？
- trace-aware eval 的本地实验应如何设计，才能比较最终答案评分和过程评分的差异？
- 是否需要为每个框架增加最小示例 source card？
- 是否需要补充面向初学者的视频课程或书籍？
- 哪些论文结论已经被现代框架吸收，哪些仍主要是研究方向？

## 本章小结

- 资料地图的目标是组织可信学习路径，不是堆链接。
- 论文、官方文档、框架文档、源码示例和治理指南各有用途。
- Source cards、coverage matrix 和 claim ledger 是控制正确性的核心机制。
- 大部分资料仍需精读和交叉验证，正文应保持保守表述。
- 后续扩展资料库时，应优先补当前矩阵中的缺口。

## References

### Indexes

- [Source Card 索引](../sources/source-card-index.md)
- [References 覆盖矩阵](../references/coverage-matrix.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [待验证问题](../evidence/validation-backlog.md)

### Templates

- [资料卡片模板](../governance/templates/source-card.md)
- [Evidence Note 模板](../governance/templates/evidence-note.md)
