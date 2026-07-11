# Planning、Orchestration 与多 Agent

## 本章适合谁

如果你已经了解 Agent 架构模式，但还不清楚 Planning 和 Orchestration 的区别，也不确定什么时候需要多 Agent，这一章适合阅读。

本章会把“任务怎么拆”和“系统怎么管”分开讲，再讨论多 Agent 为什么不是默认答案。

## 你会学到什么

- Planning 和 Orchestration 的区别。
- Planner / Executor 模式解决什么问题。
- 多 Agent 常见协作模式。
- 为什么多 Agent 会增加成本和调试难度。
- 如何为复杂任务设计人工确认和恢复策略。

## 先用一句话理解

Planning 关注“下一步该做什么”，Orchestration 关注“整个系统如何把步骤、工具、状态、错误和人类确认组织起来”。

## 基础概念

### Planning

Planning 是把目标拆成步骤，并根据反馈调整计划。它可以是模型一次性生成计划，也可以是在执行过程中动态调整。

Planning 的风险是：计划看起来合理，不代表可执行。复杂计划需要检查点和失败恢复。

### Orchestration

Orchestration 是系统层面的编排。它包括任务流、状态转移、工具调用、并发、重试、人工确认、日志和恢复。

Planning 更偏决策，Orchestration 更偏工程控制。

### Planner / Executor

Planner / Executor 是常见拆分方式：planner 负责拆解任务，executor 负责执行具体步骤。

这种模式能让职责更清楚，但也会带来接口问题。planner 生成的步骤必须足够具体，否则 executor 很难执行；executor 的失败也必须能反馈给 planner。

本手册的标准库 Planner / Executor 对比实验显示：一次性计划在 migration 任务中漏掉关键文件时，executor 不会自动补证据；加入 validation feedback 后，系统记录 `validation_failed` 和 `plan_revised`，再补读缺失文件。这个实验不能证明真实模型会稳定重规划，但可以说明 planner/executor 的接口至少需要计划步骤、证据校验、失败反馈和重规划 trace。

### Critic / Reviewer

Critic 或 reviewer 负责检查计划、结果或中间步骤。它可以发现遗漏，但不能保证正确。它本身也可能误判。

Reflection / Retry 实验给了一个最小例子：当 critic 只是根据 required evidence 检查缺失资料时，重试可以补齐证据；当系统把未验证反思当成策略记忆时，retry 会继续跳过关键文件。对初学者来说，critic 的价值不在于“多一个角色”，而在于它检查什么、检查结果是否可验证、错误反馈是否会污染后续状态。

### Human-in-the-loop

Human-in-the-loop 是把人类确认放入流程。涉及高风险操作、模糊判断、写操作或业务责任时，人类确认是控制风险的重要机制。

在工程上，Human-in-the-loop 最好是流程节点，而不是最后加一句“请确认”。LangGraph current docs 的 `interrupt()` / resume 机制给了一个具体参考：graph 可以在 critical action 前暂停，把待确认内容交给人类，再基于保存的 state 恢复。这个例子也提醒我们，编排不是只画流程图，还要处理恢复语义：node 恢复时可能从头执行，确认点前的代码可能重跑，有副作用的动作需要放在确认之后或做成幂等。

## 多 Agent 是什么

多 Agent 是让多个角色化 Agent 协作完成任务。常见角色包括：

- Planner：拆解任务。
- Executor：执行步骤。
- Researcher：查资料。
- Critic：审查结果。
- Summarizer：汇总输出。
- Router：决定任务分配。

多 Agent 的价值在于分工和视角多样性，但它也会增加通信成本、协调复杂度和调试难度。

AutoGen 和 CrewAI 的文档都说明多 Agent 已经是成熟工程生态的一部分；但这些文档主要说明“可以怎么组织”，不等于证明“默认应该这样组织”。尤其是 CrewAI 文档明确建议 production-ready application 先从 Flow 开始，再在需要自治协作的步骤中调用 Crew。

Multiagent Debate 论文展示了另一个研究方向：让多个模型实例分别提出答案和推理过程，再经过多轮辩论形成共同答案。它说明多视角和互相审查可能有价值，但不等于工程系统里角色越多越好。实际采用前仍要看冲突如何合并、谁负责最终结论、成本是否可接受，以及 trace 是否能审计每个角色的贡献。

本手册的多 Agent 标准库实验比较了单流程、无控制多 Agent 和 Flow 控制多 Agent。单流程 checklist 以 6 次工具调用完成 3/3 个任务；无控制多 Agent 只完成 1/3，出现重复读取、漏证据和 unresolved conflict；Flow 控制多 Agent 恢复到 3/3，但产生 9 条 messages。这个实验支持一个保守规则：多 Agent 的关键不是角色数量，而是 Flow / workflow 是否明确证据、角色边界、冲突处理和 review trace。

LangGraph 的历史 examples 覆盖 plan-and-execute、human_in_the_loop 和 multi_agent 等形态，但该目录已经标注为归档，不再更新。它适合作为“这些架构大概如何组织成 state / node / edge”的参考；真实跟练应优先使用当前 LangGraph Docs 和 Quickstart，并重新记录依赖、trace、成本和失败模式。

## 通俗例子

假设任务是“为一个新功能写技术方案”。

单 Agent 可能自己读需求、查代码、写方案、检查遗漏。

Planner / Executor 可能先生成计划：读需求、查现有模块、识别风险、写方案。然后 executor 按步骤执行。

多 Agent 可能让 researcher 查资料，让 architect 写方案，让 critic 审查风险，让 summarizer 输出最终文档。

听起来多 Agent 更完整，但也更复杂：谁决定最终结论？意见冲突怎么办？critic 错了怎么办？每个 Agent 都调用工具，成本怎么控制？

## 工作原理

一个复杂任务编排通常需要这些机制。

### 任务分解

把大目标拆成可执行任务。每个任务应该有输入、输出、成功标准和失败处理。

### 状态持久化

保存任务列表、执行状态、工具结果、错误和人工决策。没有状态持久化，任务中断后很难恢复。

如果流程需要暂停后恢复，还要明确“用什么持久化”。LangGraph persistence 文档把 checkpointer 用于保存 thread 的 graph state snapshots，把 store 用于跨 thread 的应用数据。对初学者来说，最重要的不是记住这些 API 名字，而是理解：审批恢复依赖可恢复的状态、稳定的 thread 标识和持久化存储；内存型保存器只适合教程或本地实验。

### 调度和依赖

有些步骤可以并行，有些必须串行。调度器需要知道依赖关系，避免重复劳动或顺序错误。

### 反馈和重规划

工具失败、资料不足、结果冲突时，系统需要决定重试、换工具、修改计划还是请求用户。

### 人工确认

涉及外部副作用、业务判断或高风险结论时，需要把确认点放进流程，而不是最后才让人检查一大段输出。

## 工程实践

### 先定义任务边界

不要先问“要不要多 Agent”。先问：任务的输入是什么，输出是什么，成功标准是什么，失败代价是什么。

### 用 checklist 替代过度自治

很多任务不需要 planner。一个清晰 checklist 加上固定 workflow 就足够。只有当步骤依赖动态观察时，才需要模型参与规划。

### 控制任务粒度

任务太大，Agent 容易泛化和遗漏。任务太小，调度开销会变大。好的任务粒度应该能被独立执行、独立验证。

### 为冲突设计规则

多 Agent 之间意见不一致时，需要明确谁有最终决定权，或者什么时候请求人类判断。

### 记录成本和延迟

多 Agent 常常增加模型调用次数。没有成本和延迟记录，就无法判断架构收益是否值得。

## 常见误区

- 误区一：复杂任务一定需要多 Agent。很多复杂任务更适合 workflow + 少量模型判断。
- 误区二：Planner 写出计划就代表任务可执行。计划必须被校验和更新。
- 误区三：Critic 能保证质量。Critic 也会出错。
- 误区四：多角色就等于专业分工。角色 prompt 不等于真实能力边界。
- 误区五：并行越多越快。并行会增加合并、冲突和重复成本。

## 什么时候不该用多 Agent

以下情况不建议优先使用多 Agent：

- 单 Agent 或 workflow 已经能稳定完成任务。
- 没有明确的角色边界。
- 没有冲突处理策略。
- 没有成本预算和 trace。
- 任务成功标准不清楚。

多 Agent 更适合这些场景：任务天然有多个专业视角，步骤可以相对独立，结果需要审查，且系统能记录和评估每个角色贡献。

## 已验证结论

- “Tree of Thoughts 支持搜索式推理路径，但不等同于生产 Agent 编排框架”已升级为可入正文：它适合解释多个中间 thought、不同推理路径、自我评估、前瞻和回溯等搜索式规划思路，但不等同于生产编排框架。
- “Reflection / Reflexion 可以利用任务反馈和文字反思改进后续尝试，但不保证稳定提升”已升级为可入正文的机制边界：带 verifier 的反馈可帮助补证据，未验证反思会让错误重复。该模式必须绑定可校验反馈、范围控制和 trace；真实收益仍需要结合反馈质量、成本、人工评审和错误记忆风险保守使用。
- Agent 架构模式边界已升级为可入正文：搜索式推理、反思、状态图、workflow-agent hybrid 和多 Agent 是不同层级的模式；复杂 Agent 架构不是默认更可靠，必须用 trace、成本、失败原因、权限和实验结果比较。
- Planner / Executor 边界已升级为可入正文：Planner / Executor 需要可执行计划、证据校验、失败反馈和重规划 trace；一次性计划可能遗漏关键证据，带校验反馈的重规划可以补齐缺失步骤。真实模型、真实框架和真实任务收益仍待验证。
- Critic / Reflection 对比实验已完成标准库模拟：verified reflection retry 可以补齐 missing evidence，但 unverified reflection memory 会污染 retry；仍需真实 critic、长期 episodic memory 和人工评审实验。
- AutoGen 文档已完成第一轮精读，可支撑 AgentChat、Teams、Selector Group Chat、Swarm、GraphFlow、logging 等多 Agent 协调抽象。
- CrewAI 文档已完成第一轮精读，可支撑 Flows / Crews 的组合：Flow 管理状态和控制执行，Crew 在 Flow 内协作完成特定复杂任务。
- Multiagent Debate 论文摘要已完成第一轮精读，可支撑“多个模型实例多轮提出、辩论并汇总答案”这一研究机制边界；它不能证明工程多 Agent 在真实任务中默认更可靠。
- “多 Agent 是一种编排选择，不是复杂任务的默认升级路径；引入前应明确角色边界、证据分配、冲突处理、review trace 和成本预算”已升级为可入正文。框架文档支撑多 Agent 能力存在，CrewAI 支撑先用 Flow 控制的保守路线，Agent eval 资料支撑需要用 trace、成本和失败原因评估是否值得；标准库多 Agent 对比实验验证了无控制角色协作的重复读取、缺证据和冲突风险。真实模型、真实框架、token/latency/cost 和复杂多视角任务收益仍待验证。
- LangGraph 文档可作为状态图和编排工程参考，但其抽象属于具体框架。
- LangGraph current docs 的 interrupts / persistence 页面可支撑 pause/resume、approval workflow、review/edit state、tool 内中断、checkpointer 和 `thread_id` 的编排边界；同时也明确 node restart、interrupt 顺序、JSON-serializable payload 和 side-effect idempotency 等限制。
- LangGraph examples repo 可作为 planner/replan、interrupt/resume 和 multi-agent 形态参考；但 `examples/` 目录已归档，不能作为最新用法或生产可靠性的证据。

## 待验证问题

- Planner / Executor 在真实工程任务中如何定义接口最稳定？标准库实验已验证最小证据校验和重规划 trace，仍需真实模型 / 框架 / repo issue 实验。
- 哪些任务适合多 Agent，哪些任务只需要 workflow？标准库实验显示清晰写作任务用单流程也能完成，仍需真实模型 / 框架实验覆盖更复杂多视角任务。
- 多 Agent 的成功率提升是否能抵消成本、延迟和协调复杂度？标准库实验已记录 messages、conflicts 和 duplicate reads，仍需真实 token/latency/cost 数据。
- Critic / Reviewer 的错误率如何评估？标准库实验已覆盖错误反思污染 retry 的最小场景，仍需真实模型、长期记忆和人工评审实验。
- Human-in-the-loop 应该放在流程中哪些位置？LangGraph current docs 已给出 critical actions 前中断、review/edit state 和 tool 内中断的机制参考；Real LangGraph Interrupt Recovery completed run 已在 `MemorySaver` 最小 graph 中验证批准执行一次、拒绝不执行、参数 hash 不匹配阻断、重复 resume 不重复执行和 trace 未泄露示例 secret marker，也用 `SqliteSaver` 在本地 SQLite checkpoint 上验证了同进程重建 saver / graph 后恢复，以及 prepare / resume 两个本地 Python 进程之间用同一 `thread_id` 恢复一次暂停审批。真实业务仍需部署式服务重启、并发恢复、真实副作用事务、审批 UI、状态表和生产审计验证。

## 本章小结

- Planning 负责拆解和调整任务，Orchestration 负责组织系统执行。
- Planner / Executor 可以让职责更清楚，但需要反馈和重规划。
- 多 Agent 是一种编排方式，不是默认升级路径。
- 成本、延迟、冲突和 trace 是多 Agent 设计的核心问题。
- 初学者应先掌握 workflow-agent hybrid，再尝试多 Agent。

## References

### Papers

- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](../sources/source-cards/2023-tree-of-thoughts-paper.md)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](../sources/source-cards/2023-reflexion-paper.md)
- [ReAct: Synergizing Reasoning and Acting in Language Models](../sources/source-cards/2022-react-paper.md)
- [Improving Factuality and Reasoning in Language Models through Multiagent Debate](../sources/source-cards/2023-multiagent-debate-paper.md)

### Framework Docs

- [LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- [LangGraph Examples Repository](../sources/source-cards/2026-langgraph-examples-repo.md)
- [Real LangGraph Interrupt Recovery](../experiments/real-langgraph-interrupt-recovery/README.md)
- [Microsoft AutoGen Documentation](../sources/source-cards/2026-autogen-docs.md)
- [CrewAI Documentation](../sources/source-cards/2026-crewai-docs.md)

### Governance

- [术语边界表](../glossary.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [Evidence Note: Agent 架构模式边界](../evidence/agent-architecture-pattern-boundary.md)
- [Evidence Note: 多 Agent 不是默认更好](../evidence/multi-agent-default-boundary.md)
- [Planner / Executor 与单循环对比实验结果](../experiments/planner-executor-comparison/results-2026-07-11.md)
- [Reflection / Retry 与错误反思实验结果](../experiments/reflection-retry/results-2026-07-11.md)
- [多 Agent 与 Flow 控制对比实验结果](../experiments/multi-agent-comparison/results-2026-07-11.md)
