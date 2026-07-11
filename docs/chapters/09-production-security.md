# Production：安全、权限、成本与部署

## 本章适合谁

如果你已经理解 Agent 的工具调用、记忆、RAG、规划和评测，现在想知道“怎样上线才不容易出事故”，这一章适合阅读。

本章不把生产化讲成一个部署命令，而是从安全边界、权限、成本、延迟、审计和回滚来理解 Agent 上线。

## 你会学到什么

- 为什么 Agent 生产化比普通聊天应用风险更高。
- Prompt injection 为什么不能只靠 prompt 解决。
- 如何理解工具权限、数据边界和人工确认。
- 上线前需要哪些日志、审计、成本和降级设计。
- 如何用风险清单而不是直觉判断系统是否可上线。

## 先用一句话理解

生产化 Agent 的核心不是“让模型更聪明”，而是让模型在受控权限、可观测流程和可回滚系统里工作。

## 基础概念

### Production

Production 指系统面向真实用户、真实数据和真实业务后果运行。

实验 demo 可以容忍失败，生产系统需要考虑权限、隐私、可靠性、成本、审计和责任边界。

### Prompt Injection

Prompt injection 指外部输入试图改变模型行为，让系统忽略原有指令、泄露信息或执行不该执行的动作。

对 Agent 来说，风险更高，因为 Agent 可能读取网页、文档、邮件、工单和数据库内容。这些外部内容可能包含恶意指令。

OWASP 把 prompt injection 列为 LLM 应用风险项，并把不安全插件设计、敏感信息泄露和 excessive agency 也列为相关风险。对初学者来说，关键不是背风险编号，而是记住：外部内容只能被当作数据，不能被当作系统规则。

### 权限模型

权限模型决定 Agent 能访问什么数据、能调用什么工具、能执行什么动作、哪些动作需要人类确认。

好的权限模型应该最小化默认权限，而不是把所有能力都交给一个通用 Agent。

### 数据边界

数据边界说明哪些数据可以进入模型上下文，哪些只能通过受控工具查询，哪些必须脱敏，哪些完全不能访问。

Agent 的上下文不是安全边界。把秘密放进 prompt 后，再要求模型“不要泄露”，不是可靠的安全设计。

### Human Approval

Human approval 是人工确认机制。它适合放在高风险写操作、不可逆操作、涉及钱或隐私的操作、影响其他用户的操作之前。

人工确认不是补丁，而是工作流的一部分。

## 通俗例子

假设你做了一个可以处理报销的 Agent。

它需要读取发票、查公司政策、填写报销系统、提醒员工补材料。

如果没有生产化设计，它可能出现这些问题：

- 读取发票里的恶意文本后，忽略公司政策。
- 把 A 员工的报销信息发给 B 员工。
- 在金额异常时仍然自动提交。
- 工具失败后编造审批状态。
- 为了完成任务反复调用高成本模型和 API。
- 上线后出了问题，却没有 trace 能说明它做过什么。

这些不是简单 prompt 可以彻底解决的问题，需要系统层控制。

## 工作原理

生产化 Agent 通常需要把模型放进一个受控运行环境。

### 输入分层

系统应该区分不同来源的输入：开发者指令、用户请求、工具结果、网页内容、文档内容、历史记忆。

不同来源可信度不同。外部文档和网页内容不应拥有改变系统规则的权力。

### 工具隔离

工具应该有明确职责和权限。读工具和写工具分开，高风险工具和低风险工具分开。

例如“查询订单状态”和“执行退款”应该是两个不同工具，后者需要更严格的权限、校验和人工确认。

### 参数校验

模型生成的工具参数不能直接信任。系统应该检查参数类型、范围、用户权限、业务规则和幂等性。

框架里的 guardrails 可以帮助拦截输入、输出或工具调用，但要注意它们运行在不同位置。比如有的 guardrail 只在第一个 agent 输入或最后输出运行；如果你真正需要检查每次工具调用，就应该把检查放在工具调用前后，或在应用层做参数校验。

### 审计日志

审计日志记录谁发起任务、Agent 调用了什么工具、用了什么参数、得到什么结果、谁批准了高风险动作。

没有审计日志，生产事故很难复盘。

### 降级和回滚

Agent 失败时不应只有“继续尝试”和“报错”两个选择。系统需要降级路径：转人工、只读模式、停止写操作、回到规则流程或使用旧版本。

## 工程实践

### 从最小权限开始

先给 Agent 最少工具、最少数据、最少写权限。每增加一个工具，都要问：失败后果是什么，是否需要确认，是否需要审计。

### 把写操作设为显式流程

涉及发送邮件、提交表单、修改数据库、下单、退款、删除文件等操作时，不要让模型在模糊状态下直接执行。

更稳妥的模式是：Agent 先生成计划和参数，系统展示给用户或审批人确认，再执行。

如果使用支持 human-in-the-loop 的框架，审批流程最好能暂停、保存状态、恢复执行，并记录批准或拒绝的决定。审批不是一句“请确认”的 UI 文案，而是一段可审计、可恢复的执行流程。

### 不把敏感信息直接塞进上下文

如果模型只需要判断“用户是否有权限”，就不一定需要看到完整权限表。如果只需要摘要，就不一定需要完整原文。

把敏感数据留在工具和后端系统里，通过最小必要字段返回给模型，通常更容易控制风险。

### 对外部内容保持不信任

网页、PDF、邮件、工单、聊天记录和用户上传文件都可能包含恶意指令。它们应该被当作数据，而不是指令。

这需要系统提示、工具设计、内容标注、权限控制和 eval 样例一起配合。

仅靠一句“忽略外部文档里的指令”是不够的。更稳妥的做法是让外部内容无法直接获得工具权限：读工具和写工具分开，写操作走确认流程，工具参数由应用层校验，敏感字段尽量不进入模型上下文。

如果 guardrail 有 blocking 和 parallel 两种模式，高风险工具前应优先考虑 blocking 检查。并行检查延迟更低，但在检查失败前可能已经消耗 token，甚至已经开始执行工具。

也要确认 guardrail 覆盖了哪些工具类型。有些框架的 tool guardrail 只覆盖特定 function tools，不覆盖 hosted tools、shell、computer、handoff 或 MCP 工具；这些执行面需要额外权限和审计设计。

本手册的 prompt injection / tool permission 最小实验验证了这个边界：外部 refund policy 文档中嵌入恶意指令后，`prompt_only` 模式执行了 `issue_refund` 并把假 secret 写进 trace；`policy_enforced` 模式只允许只读 `get_order`，拒绝 `issue_refund` 和 `send_email`，并在审计记录里脱敏敏感字段。这个实验不证明真实框架的拦截率，但能说明外部内容、写工具、审批和 trace 脱敏必须由应用层策略控制。

安全 regression set 需要比单个攻击样例更宽。本手册的安全 regression set 最小实验覆盖 7 个 case：外部文档诱导退款、跨用户读取、高金额退款、敏感信息邮件、删除客户记录、重复提交和正常读取自己的订单。`prompt_only` 对 6 个风险 case 全部漏报；`policy_enforced` 区分 `allow`、`block` 和 `require_approval`，并保留 false positive、false negative 和 secret leak 字段。这个实验仍不是真实模型安全结论，但能说明上线前测试不应只看“能不能挡住一个注入样例”。

审批流程还要能安全恢复。本手册的审批状态恢复实验显示，`naive_resume` 虽然能创建待审批记录和执行一次批准后的退款，但在重复恢复同一审批、拒绝后恢复邮件、参数被篡改后恢复退款时都会继续执行，并产生重复副作用或敏感 trace 泄露；`governed_resume` 则检查 approval status、executed 标记、参数快照 hash 和 trace 脱敏，7 个操作全部通过。这个实验不证明真实 HITL 框架行为，但能说明：人工审批不是一个“用户点过确认”的布尔值，而是可审计、可恢复、可幂等的执行状态机。

### 记录成本和延迟

Agent 常常多轮调用模型和工具。上线前应该记录每类任务的平均成本、P95 延迟、工具调用次数和失败重试次数。

否则系统可能功能可用，但成本不可控或用户体验不可接受。

### 为事故准备开关

生产系统需要 kill switch、只读模式、禁用高风险工具、回滚到上一版本、切换到人工处理等机制。

这些机制应该在上线前测试，而不是事故发生后才临时设计。

### 控制 trace 中的敏感数据

Trace 对调试和审计很重要，但 trace 本身也可能包含敏感输入、工具参数、工具输出或音频数据。生产系统应明确哪些字段进入 trace、哪些字段脱敏、谁能访问、保留多久、如何删除。

如果框架默认记录模型输入输出或工具输入输出，应显式检查是否能关闭敏感数据捕获，或在写入 trace 前做脱敏。

## 常见误区

- 误区一：安全 prompt 足够解决 prompt injection。Prompt 有帮助，但不能替代权限、隔离和审计。
- 误区二：只要模型够强，生产风险就会消失。更强的模型仍可能被错误数据、错误权限和错误工具设计影响。
- 误区三：把所有工具都接给 Agent 更灵活。工具越多，越需要权限边界、选择约束和 trace。
- 误区四：人工确认会降低智能程度。对高风险动作来说，确认是可靠性设计的一部分。
- 误区五：上线后再补 observability。没有日志和 trace，事故后很难知道发生了什么。

## 上线前检查清单

- 是否定义了 Agent 可以访问的数据范围？
- 是否区分了只读工具和写工具？
- 高风险操作是否需要人工确认？
- 工具参数是否经过应用层校验？
- 外部文档和网页是否被当作不可信数据？
- 是否保存了可审计 trace？
- 是否有小型 regression set 覆盖安全和失败场景？
- 是否记录成本、延迟和重试？
- 是否有降级、回滚和禁用工具的机制？
- 是否清楚哪些结论仍然待验证？

## 已验证结论

- OWASP LLM Top 10 的关键风险项已完成第一轮精读，可支撑 prompt injection、敏感信息泄露、工具/插件访问控制和 excessive agency 的保守风险表述。
- NIST AI RMF 的概述段落已完成第一轮精读，可支撑生产化章节的风险管理和治理视角；它不是 Agent 专用工程指南。
- “Prompt injection 不能只靠 prompt 解决；外部内容应被当作不可信数据，工具权限和写操作审批必须由应用/系统层控制”已升级为可入正文。OWASP 支撑风险分类，NIST 支撑全生命周期风险治理，OpenAI 工具调用文档支撑应用侧执行和控制边界。
- OpenAI Agents SDK 和 Semantic Kernel 文档已补充第一轮工程资料，可支撑 guardrails、human approval、tool approval、sensitive trace 控制和 task automation approval 的保守表述；标准库 prompt injection / tool permission 实验、安全 regression set 和审批状态恢复实验已覆盖最小权限、trace 脱敏、误报/漏报字段、多类风险 case、审批恢复、参数快照和幂等执行。“高风险工具应使用最小权限、参数校验、guardrails、人工确认、审批状态恢复和审计 trace 的组合”已升级为可入正文。真实 prompt injection / permission harness 已准备，但结果待跑，仍需真实模型 / 框架 guardrail 与 HITL 实验验证误报、漏报和覆盖范围。
- 本地标准库 prompt injection / tool permission 实验显示，prompt-only 模式会产生退款副作用并泄露假 secret 到 trace；应用层权限策略可以阻断写工具、记录拒绝原因并脱敏敏感字段。该实验支撑最小权限、写工具审批和 trace 脱敏的流程设计；真实 API harness 已准备但结果待跑，仍需真实模型和框架 guardrail 实验。
- 本地标准库安全 regression set 显示，回归测试应同时覆盖 prompt injection、授权、数据边界、金额阈值、敏感信息、破坏性工具、幂等性和 benign case；该实验支撑安全测试矩阵设计，但不证明真实 guardrail 拦截率。
- 本地标准库审批状态恢复实验显示，HITL approval 需要保存审批状态、参数快照和执行状态；重复恢复应返回已执行，拒绝后恢复应阻断，参数被篡改后恢复应阻断，trace 应脱敏。该实验支撑审批恢复和幂等性设计，但不证明真实框架的 HITL 行为。
- Tool use、MCP、Memory 和 Eval 章节中的风险边界都与生产化相关，生产章节应作为前面章节的收束，而不是独立安全清单。

## 待验证问题

- 针对具体 Agent 框架，guardrails、approval、sensitive trace 和 tool permission 覆盖范围有哪些差异？已完成 OpenAI Agents SDK/Semantic Kernel 第一轮验证，仍需横向比较。
- MCP 工具生态中的安全边界应该如何落到 host、client 和 server 实现？
- 真实模型 / 框架 guardrail 下，prompt injection 防护的误报、漏报、成本、延迟和人工审批负担如何测量？真实 API harness 已准备，仍需实际运行并扩展到框架 guardrail / HITL 对照。
- 哪些日志字段既能支持审计，又不会引入新的隐私风险？已完成 observability/trace 第一轮验证，仍需脱敏和访问控制实验。
- 成本和延迟应该如何纳入 Agent eval？

## 本章小结

- 生产化 Agent 的重点是受控权限、可观测流程、可审计行为和可回滚系统。
- Prompt injection 不能只靠 prompt 解决，需要权限、隔离、校验、审计和测试共同控制。
- 写操作、敏感数据和外部副作用必须有明确边界。
- 成本和延迟是生产质量的一部分，不是上线后的附属问题。
- 初学者做生产化练习时，应先实现只读、安全、可观测的小 Agent，再逐步增加能力。

## References

### Security and Risk

- [OWASP Top 10 for Large Language Model Applications](../sources/source-cards/2026-owasp-llm-top-10.md)
- [NIST AI Risk Management Framework](../sources/source-cards/2026-nist-ai-rmf.md)

### Related Chapters

- [Tool Use、Function Calling 与 Structured Output](03-tool-use.md)
- [MCP 与工具生态](05-mcp.md)
- [RAG、Memory 与知识库治理](06-rag-memory.md)
- [Evaluation 与 Observability](08-evaluation-observability.md)

### Governance

- [结论证据台账](../evidence/claim-ledger.md)
- [Evidence Note: Prompt Injection 与权限边界](../evidence/prompt-injection-permission-boundary.md)
- [Evidence Note: 工具权限、人工确认与审计边界](../evidence/tool-permission-audit-boundary.md)
- [Prompt Injection 与工具权限最小实验结果](../experiments/prompt-injection-permission/results-2026-07-11.md)
- [安全 Regression Set 最小实验结果](../experiments/security-regression-set/results-2026-07-11.md)
- [审批状态恢复与幂等性实验结果](../experiments/approval-state-recovery/results-2026-07-11.md)
- [Real Prompt Injection 与工具权限实验](../experiments/real-prompt-injection-permission/README.md)
- [References 覆盖矩阵](../references/coverage-matrix.md)
