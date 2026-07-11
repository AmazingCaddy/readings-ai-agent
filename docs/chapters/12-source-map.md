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
Agent/Workflow 与自治程度窄边界已升级为可入正文，可帮助理解固定 workflow、workflow-agent hybrid 和更开放 tool loop 是控制权连续谱，不是能力等级排行。
Workflow / Hybrid / ReAct-like 标准库对比实验已经完成，可帮助理解固定流程、受控动态查询和 tool loop 在成功率、工具调用数、失败原因和 trace 上的差异；真实模型 / Agent framework / repo issue 仍需后续实验。

### LLM 接口与工具调用

先读手册 02 和 03，再看 Responses API、Function Calling docs 和 Toolformer。

阅读重点是区分：模型生成工具调用参数，应用程序执行工具，工具结果再回到模型上下文。
上下文治理与结构化输出标准库实验已经完成，可帮助理解 free text、JSON mode、schema validation、schema-valid semantic error、旧资料冲突和外部文档注入的最小边界；真实 Responses API / Structured Outputs、refusal、长上下文成本和跨模型稳定性仍需后续实验。
Tool Calling 参数校验与重试的标准库模拟实验已经完成，可帮助理解应用层校验、错误回传、有限重试和 trace 字段；真实模型 / API 稳定性仍需后续实验。

### MCP 与工具生态

先读手册 05，再看 MCP official docs 和 MCP servers repo。

阅读重点是 host、client、server、tools、resources、prompts、authorization、roots、elicitation、sampling 和权限边界。尤其要注意：authorization 是 optional transport-level capability，roots 不等于 sandbox，token passthrough 被官方安全最佳实践禁止。

### RAG 与 Memory

先读手册 06，再看 RAG paper、LlamaIndex、LangGraph memory、MemGPT、MemoryBank、Generative Agents、Letta 和 Zep。

阅读重点是区分外部知识检索、短期状态、长期记忆、写入守门和隐私风险。
RAG / Memory 对比标准库实验已经完成，可帮助理解外部知识问题应走 RAG 和 citation，当前任务连续性应走 thread state，跨会话偏好/纠正事实应走 guarded long-term memory，敏感且无安全来源的问题应拒答。
RAG 最小 pipeline / citation 标准库模拟实验已经完成，可帮助理解 chunk metadata、retrieval trace、chunk-level citations 和无证据拒答；真实 embedding / vector store / LLM synthesis 仍需后续实验。
长期记忆写入守门标准库模拟实验已经完成，可帮助理解显式写入、敏感信息拒绝、低置信推断拒绝、用户纠正、失效历史和 trace 脱敏；真实多会话 Agent / memory framework 的收益、污染、权限和用户编辑流程仍需后续实验。

### Planning、Orchestration 与多 Agent

先读手册 07，再看 Tree of Thoughts、Reflexion、AutoGen、CrewAI 和 LangGraph。

阅读重点是任务拆解、状态管理、反馈、重规划、角色协作和成本。
Planner / Executor 标准库对比实验已经完成，可帮助理解一次性计划遗漏、missing evidence 校验、反馈重规划和 trace 字段；真实模型 / Agent framework / repo issue 仍需后续实验。
Reflection / Retry 标准库实验已经完成，可帮助理解 verified feedback、missing evidence retry、错误反思污染和 reflection trace；真实模型、长期 episodic memory、人工评审和成本评估仍需后续实验。
多 Agent / Flow 控制标准库实验已经完成，可帮助理解角色协作、Flow 控制、重复读取、冲突和消息开销；“多 Agent 不是复杂任务默认升级路径”窄边界已可入正文。真实 AutoGen / CrewAI / LangGraph 对比仍需后续实验。

### Evaluation 与 Observability

先读手册 08，再看 AgentBench、WebArena、OpenAI Evals、LangSmith 和 Phoenix。

阅读重点是任务环境、trajectory、trace、offline/online eval、regression set、datasets、feedback 和错误分类。
Trace-aware eval 标准库模拟实验已经完成，可帮助理解为什么 final-answer-only scoring 会漏掉无审批副作用工具和工具错误未恢复；真实 Agent trace、LLM-as-judge 误判和人工复核仍需后续实验。

### Production、安全与治理

先读手册 09，再看 OWASP LLM Top 10、NIST AI RMF、OpenAI Agents SDK guardrails / human-in-the-loop / tracing 文档，以及 Semantic Kernel Plugins 文档。

阅读重点是 prompt injection、权限、工具审批、guardrails 的执行位置、数据边界、审计、人工确认、降级、敏感 trace 控制和风险管理。
Prompt injection / tool permission 标准库模拟实验已经完成，可帮助理解 prompt-only 风险、只读/写工具分离、写工具审批拒绝和 trace 脱敏；真实模型、框架 guardrail 和 HITL approval 仍需后续实验。

### 框架生态与实践

先读手册 10 和 11，再横向阅读 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI、Semantic Kernel 和 OpenAI Cookbook 的具体 recipe。

阅读重点是选择维度、可迁移概念和可复现练习，而不是追随单一框架或照搬复杂 demo。
框架选择 rubric smoke test 已经完成，可帮助理解如何把框架比较拆成 required、nice-to-have、avoid、missing required 和 cautions；真实同一任务框架横向实验仍需后续试跑。
实践路线 smoke harness 已经完成，可帮助理解如何把结构化输出、工具参数、RAG 引用、eval cases 和成本闸门组织成可运行验收流程；真实 Cookbook / API recipe 的依赖、成本和初学者阻塞点仍需后续试跑。

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

核心 source cards 已经完成多轮链接、元数据和关键段落复核，能支撑章节中的学习方向、术语边界和部分验证结论。主索引已同步这些状态：论文、官方文档、框架文档和安全资料会标注“关键段落已精读 / 部分验证 / 下一步真实实验”。OpenAI Cookbook 已完成 Structured Outputs、File Search RAG、OpenAI Evals、Agents SDK trace/eval、Usage/Cost 和 Rate limits 等具体 recipe 的第一轮复核，可支撑实践项目参考。仍处于候选或只完成链接复核的资料，不能支撑过强的工程断言。

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
- Coverage matrix 显示 Agent/Workflow、LLM / Context、Evaluation / Observability、Production / Security 和 Memory / 知识库治理都已补标准库模拟实验；这些实验支撑流程和 trace 设计，但仍需要真实模型、真实框架和真实多会话实验来升级结论强度。
- Agent / Workflow 和自治程度边界已补标准库 workflow / hybrid / ReAct-like 对比实验，窄结论“Agent 和 Workflow 是控制权与编排方式的连续谱，自治程度不是能力等级”已可入正文；仍缺真实模型 / Agent framework / repo issue、token/latency/cost、权限确认和工具错误恢复实验。
- Agent 架构模式边界已补论文 / 框架资料和多组标准库对比实验，窄结论“复杂 Agent 架构不是默认更可靠，需要用 trace、成本、失败原因、权限和实验结果比较”已可入正文；仍缺真实模型 / 框架任务中的收益、成本、延迟和错误恢复实验。
- Planner / Executor 已补标准库对比实验，窄结论“计划需要可执行，执行结果需要证据校验，失败需要反馈给 planner 并记录重规划 trace”已可入正文；Reflection / Retry 已补标准库错误反思实验，可支撑 verified feedback 与 unverified reflection memory 的边界；仍缺真实模型 / 框架 / repo issue、token/latency/cost、长期记忆和人工评审实验。
- 多 Agent 已补标准库单流程 / 无控制多 Agent / Flow 控制多 Agent 对比实验，窄结论“多 Agent 不是复杂任务默认升级路径；引入前应明确角色边界、证据分配、冲突处理、review trace 和成本预算”已可入正文；仍缺真实模型、真实框架、token/latency/cost 和复杂任务实验。
- MCP official docs 已补 2025-11-25 tools/resources/prompts/authorization/roots/elicitation/sampling spec 和 Security Best Practices 第一轮精读；MCP 最小 trace 标准库模拟实验已完成，可支撑最小审计字段和职责流设计；仍缺真实 MCP SDK / host trace、权限确认、URL mode / OAuth、恶意 resource/prompt 和 host 实现差异实验。
- Tool Use / Function Calling 已补标准库参数校验/重试模拟实验，可支撑“应用层校验、错误回传、有限重试”的流程说明；仍缺真实 Function Calling / Responses API 实验和其他框架术语对照。
- LLM / Context 已补官方文档精读、标准库输出解析 / 上下文治理模拟实验和上下文策略对比实验，窄结论“LLM 应用输入输出不只是字符串”“schema validation 不等于语义正确”和“长上下文不能替代来源、时效、权限治理”已可入正文；仍缺真实 Responses API / Structured Outputs、refusal、semantic validator、retry loop、长上下文 token/latency/cost 和跨模型稳定性实验。
- RAG / Memory 已补标准库对比实验，可支撑外部知识、thread state、guarded long-term memory 和无安全来源拒答的分层边界；仍缺真实 RAG / memory framework / 多会话质量实验。
- RAG 已补标准库最小 pipeline / citation 模拟实验，可支撑 chunk metadata、retrieval trace、chunk-level citations 和 `grounded=false` 拒答流程；仍缺真实 embedding / vector store / LLM synthesis、chunk size/top-k/rerank 对比、citation correctness 和成本/延迟实验。
- Memory / 知识库治理已补标准库写入守门模拟实验，可支撑显式写入、敏感信息拒绝、低置信推断拒绝、用户纠正、失效历史和 trace 脱敏流程；仍缺真实多会话 Agent / memory framework 的收益、污染、权限、隐私和用户查看/编辑/删除实验。
- Evaluation / Observability 已补标准库 trace-aware eval 模拟实验，可支撑 final-answer-only 与 trace-aware scoring 的差异说明；仍缺真实 Agent trace、LLM-as-judge 误判分析、人工复核和回归集工程案例。
- Production / Security 已补标准库 prompt injection / tool permission 模拟实验，可支撑 prompt-only 风险、写工具阻断和 trace 脱敏流程；仍缺真实模型 / 框架 guardrail / HITL approval 实验、跨框架权限对比和审计脱敏策略。
- Framework landscape 已补标准库框架选择 rubric smoke test，可支撑任务画像、能力标签、missing required 和 cautions 的比较方法；仍缺真实同一任务框架横向实验。
- Cookbook 的具体 recipe 已能支撑实践项目路线，标准库 smoke harness 已支撑项目验收结构和 trace / 失败分类设计；仍需要真实本地试跑来确认依赖、成本、失败样例和初学者阻塞点。
- Claim ledger 规定只有状态为“可入正文”的结论，才能写成确定性表述；其他结论需要保守表达。

## 待验证问题

- prompt injection / tool permission 的最小攻击实验应该如何覆盖 guardrails、HITL approval、敏感 trace 和审计字段？
- 真实 MCP SDK / host trace 实验应如何覆盖 `tools/list`、`tools/call`、`resources/list`、`resources/read`、用户拒绝、roots、URL mode elicitation 和敏感日志脱敏？
- 真实 Function Calling / Responses API 实验中，模型能否稳定根据 tool validation error 修正参数？不同框架如何表示 tool execution error？
- 真实 Agent/Workflow 对比实验中，固定 workflow、workflow-agent hybrid、ReAct tool loop、planner/executor 和 reflection retry 如何影响成功率、工具调用数、成本、延迟、失败原因、权限确认和 trace 可读性？
- 真实 RAG stack 中，chunk size、top-k、rerank/filter 和 LLM synthesis 如何影响 citation correctness、faithfulness、latency 和 token cost？
- 真实多会话 Agent / memory framework 中，guarded memory、auto memory 和 no memory 如何影响任务质量、错误写入、过时记忆使用、敏感信息进入上下文和用户纠错成本？
- 真实 Agent trace 中，规则评分、LLM-as-judge 和人工评审如何组合，才能发现过程错误并控制误判率？
- 真实 Agent trace-aware eval 应如何覆盖 RAG、工具调用、权限确认、成本/延迟和人工反馈？
- 真实模型 / 框架 guardrail 下，prompt injection 防护如何测量误报、漏报、审批负担、延迟和敏感 trace 泄露？
- 是否需要为每个框架增加最小示例 source card？
- 真实框架横向实验应先选哪 2-3 个框架做最小实现，避免一次性引入过多依赖和 API 成本？
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
