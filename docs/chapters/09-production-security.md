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

OWASP Agentic Security Initiative 的公开资源还把 Agentic AI 风险扩展到目标劫持、工具误用、身份和权限滥用、记忆污染、多 Agent 通信不安全、级联失败和失控 Agent。这里不能得出“某个缓解方案已经有效”的结论，但可以提醒你：生产安全不只是挡住 prompt injection，还要检查身份、权限、记忆、运行时隔离、schema 校验、停止条件和监控。

MITRE ATLAS 可以作为更具体的攻击技术和案例库。它把 AI / Agentic AI 攻击组织成 tactics、techniques、mitigations 和 case studies，并标注 platform 与 maturity。对初学者来说，它最适合用来扩展安全 regression set：例如 prompt injection、agent tool invocation、tool poisoning、memory poisoning、MCP / remote tool abuse 和 computer-use 破坏性动作；不要把 ATLAS mitigation 条目直接当成“用了就安全”。

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

以 LangGraph 这类 graph runtime 为例，当前文档把 human-in-the-loop 做成 `interrupt()` / resume 机制：流程可以在关键节点暂停，把需要人类判断的数据交给调用方，再用 resume command 继续。这个机制适合解释“审批点应在工作流里显式建模”，但初学者要特别注意它的限制：恢复时 node 可能从头重新执行，`interrupt()` 前的代码会再次运行；有副作用的代码应该放在确认之后，或设计成幂等；恢复还依赖正确的 checkpointer 和同一个 `thread_id`。内存型 checkpointer 只适合教程或进程内实验，不能当成生产持久化。

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

本手册的 Real LangGraph Interrupt Recovery 最小实验进一步把这个边界放到真实 LangGraph runtime 中观察：在 LangGraph 1.2.9、`MemorySaver` 和本地假退款工具下，`interrupt()` / `Command(resume=...)` 跑通了批准、拒绝、参数 hash 不匹配和重复 resume case。批准 case 执行 1 次工具；拒绝和参数篡改 case 不执行工具；重复 resume 没有造成第二次执行；trace 和 interrupt payload 未泄露实验里的示例 secret marker。实验还用 `langgraph-checkpoint-sqlite` 3.1.0 / `SqliteSaver` 跑了三个本地 SQLite checkpoint case：同进程重建 saver / graph 后恢复、prepare / resume 两个本地 Python 进程之间恢复、两个本地 Python resume 进程同时恢复同一暂停审批。并发 case 中两个 resume 都返回 `approved_executed`，但共享副作用日志只有 1 条记录。这个结果仍很窄：SQLite case 只是本机 SQLite 文件和本地 Python 进程；它没有验证部署式服务重启、真实服务并发恢复、真实支付/邮件/数据库副作用、真实审批 UI、状态表、事务幂等或生产审计，也不能说明 LangGraph 默认替你完成参数完整性、幂等和脱敏。

本手册的 Real OpenAI Agents SDK Guardrail Validation 用 `openai-agents==0.18.2` 和 deterministic fake model 补了另一个角度：guardrail 放在哪里会改变它能阻止什么。实验观察到 input guardrail 可以在模型调用前触发，output guardrail 只能在模型产出后触发；function-tool input guardrail 的拒绝内容可以阻止本地函数工具副作用，function-tool output guardrail 则发生在函数已经执行之后，只能替换工具输出，不能撤销副作用。实验也确认 `needs_approval=True` metadata 可观察。2026-07-12 复核的 Agents SDK 文档进一步说明：tool guardrails 只覆盖 `function_tool` 创建的 function tools，不覆盖 hosted tools、built-in execution tools、handoff call 本身或 `Agent.as_tool()` 的直接 tool-guardrail options；hosted-container `ShellTool` 不支持 `needs_approval` / `on_approval`。这个结果只覆盖本地 function tool 和 fake model，不覆盖真实模型安全、guardrail 检测质量、hosted/MCP/Shell/ApplyPatch 工具面、真实 HITL UI、生产 trace、serialized RunState 治理、成本或延迟。

### 记录成本和延迟

Agent 常常多轮调用模型和工具。上线前应该记录每类任务的平均成本、P95 延迟、工具调用次数和失败重试次数。

否则系统可能功能可用，但成本不可控或用户体验不可接受。

更具体地说，生产化前至少要记录：输入 token、输出 token、请求数、使用的模型、rate-limit headers、重试次数、平均延迟、P95 延迟、预算阈值、超预算后的行为，以及是否有降级路径。OpenAI 的生产、成本、延迟、限流和 token counting 文档能支撑这些字段进入工程检查清单：usage dashboard / billing limits 用于用量治理，rate-limit headers 用于观测剩余请求和 token 限额，exponential backoff with jitter 用于限流错误恢复，token counting 用于请求前估算。

这些资料不证明某个应用会便宜或快。减少输出 token、设置更贴近期望输出的 `max_tokens`、选择更小模型、streaming、batching、Batch API、flex processing 或 prompt caching 都是需要用真实任务 eval 复核的取舍，而不是默认优化。尤其要注意：Batch 适合不需要即时响应的离线任务；Flex 适合能接受慢响应和偶发资源不可用的低优先级任务；Prompt Caching 要记录 `cached_tokens` 和 `cache_write_tokens`，不能只假设有缓存收益。

OpenAI Cookbook 的 Usage/Cost recipe 可以作为字段化练习参考：它示例了用 `start_time`、`end_time`、`bucket_width`、`group_by`、`project_id`、`line_item`、`amount.value` 和 `amount.currency` 拉取并聚合 usage/cost 数据。Rate limits recipe 可以作为限流练习参考：它覆盖 429 / `RateLimitError`、exponential backoff、最大重试、失败请求消耗预算、主动节流、RPM/RPD/TPM、`max_tokens` 估算影响、batching 和 fallback model 风险。它们适合帮你设计记录表，不证明你的账户、任务和模型下会得到同样的成本、延迟、吞吐或 fallback 质量。

本手册的 production cost / latency / rate-limit 标准库 audit 把这些边界拆成 9 个检查项：usage / token accounting、rate-limit headers、bounded retry、latency distribution、budget gate、model/output controls、Batch workload boundary、Flex fallback 和 Prompt Caching observability。`naive_run` 9 项全部失败，`governed_run` 9 项全部通过。Real Production Cost / Latency / Rate-Limit harness 在无 API key 时补了本地 deterministic accounting control，复用字段解析逻辑检查 usage/cache 字段、rate-limit headers、平均 / P95 latency、fixture cost estimate 和 budget action。这个结果只说明字段设计、检查表和本地汇总逻辑可以被自动审计；它不证明真实 API 更便宜、更快、更稳定，也不证明 Batch、Flex 或 Prompt Caching 在你的任务里一定有收益。

### 为事故准备开关

生产系统需要 kill switch、只读模式、禁用高风险工具、回滚到上一版本、切换到人工处理等机制。

这些机制应该在上线前测试，而不是事故发生后才临时设计。

### 控制 trace 中的敏感数据

Trace 对调试和审计很重要，但 trace 本身也可能包含敏感输入、工具参数、工具输出或音频数据。生产系统应明确哪些字段进入 trace、哪些字段脱敏、谁能访问、保留多久、如何删除。

如果框架默认记录模型输入输出或工具输入输出，应显式检查是否能关闭敏感数据捕获，或在写入 trace 前做脱敏。

还要区分“不会用于训练”和“不会被保留”。OpenAI Data controls 文档说明 API 数据默认不用于训练或改进模型，除非显式 opt in；但 API 使用仍可能产生 abuse monitoring logs 或 application state。不同 endpoint、`store` 设置、Zero Data Retention / Modified Abuse Monitoring、prompt caching、hosted containers、files、vector stores、batches 和 tools 的数据保留边界并不一样。例如 `/v1/moderations` 当前 retention matrix 显示不保留 abuse monitoring logs 或 application state，但 Responses 的 `store`、background mode、hosted containers、prompt caching、files/vector stores 和第三方工具传输都有单独边界。初学者做生产化练习时，至少要写清楚：哪些对象会被服务端保存，保存多久，是否需要显式删除，哪些 trace 字段会进入日志，第三方工具会看到什么数据。

如果应用有用户交互，还应考虑 privacy-preserving `safety_identifier`。它不是用户画像功能，而是帮助滥用监控和问题追踪的稳定标识；应避免直接发送 email、姓名等可识别信息。

Moderation 可以作为检测层，但不要把它写成自动安全闸门。OpenAI Moderation 文档说明，moderation scores 应作为应用 policy 的 signals，用来过滤、路由人工复核、记录审计或干预账户。对 tool-calling 请求，它覆盖 conversation content 中的 tool-call arguments 和 tool outputs，但不覆盖 tool names、tool descriptions、tool schemas 或 response-format schemas；这些仍要人工和应用层审查。流式输出时，moderation scores 会在完整输出可用后才到达，因此不能假设 partial deltas 已经被最终分数保护。本手册的 Real Moderation Safety harness 在无 API key 时补了本地 deterministic policy-signal control，覆盖 `flagged`、categories、category scores、`category_applied_input_types`、expected mismatch 和 allow / block-review / false-positive-review / false-negative-fallback policy decision 分支；它支撑记录模板和应用层分支检查，不支撑真实 API 误报、漏报、阈值或生产安全效果结论。

### 审查远程工具连接

Remote MCP tools 和第三方 tool servers 也属于生产权限面。接入前要确认 server 由谁运营、需要什么授权、会看到哪些用户数据、数据保留政策是什么、是否支持最小 scope，以及是否能按工具做 allowlist 或 denylist。

OpenAI Data controls 文档也明确：通过 remote MCP server tool 发送给 MCP server 的数据受第三方服务的数据保留政策影响；发送到第三方服务的网络数据也受第三方 retention policies 约束。因此 remote MCP、web search、hosted shell、code interpreter、hosted skills、files/vector stores、prompt caching、browser/computer-use 这类工具和对象都要进入数据流审查，而不是只看 OpenAI API 本身的数据保留说明。

以 Anthropic MCP connector 为例，文档支持 `mcp_servers`、`mcp_toolset`、OAuth bearer token、allowlist、denylist 和 per-tool configuration，也说明 MCP connector 不适用于 Zero Data Retention。它还明确第三方 remote MCP servers 不由 Anthropic 拥有、运营或背书。因此，remote MCP server 不能因为“能被模型调用”就被当成可信后端。

MCP tunnels 可以让 Claude 访问私有网络里的 MCP servers，而不必打开 inbound firewall ports 或把服务暴露到公网。但 tunnels 不是安全设计的终点：文档要求每个上游 MCP server 使用 OAuth，限制 `upstream.allowed_ips`，保护 tunnel token 和 TLS private key，轮换凭据，限制网络可达范围，并监控日志。Tunnels 还是 research preview，不能用来支撑生产可靠性或可用性承诺。

### 隔离浏览器 Agent

Browser Agent 是另一类高风险工具连接。它可能复用真实浏览器 profile、读取 cookies/localStorage、上传文件、提交表单、修改购物车、点击付款或发布按钮。Browser Use 和 Playwright 这类工具能提供浏览器动作能力和 trace，但不能替代权限模型。

生产前至少要使用测试账号或隔离 profile，把只读浏览和写操作分开，表单提交、购物、付款、发送消息、文件上传等动作默认要求人工确认，并记录 action trace、页面状态、审批和失败原因。涉及 CAPTCHA、反自动化、网站 ToS、代理/stealth 或真实用户账号时，还需要合规审查；不能把 demo 成功当成可上线证据。

### 处理 API key 泄露

API key 泄露不是 prompt 层问题。生产系统应把 key 放在后端或 secret manager 中，避免进入前端、公开仓库、日志和 trace。如果怀疑 key 暴露或被误用，应及时 revoke 并替换，同时检查使用记录、预算阈值和受影响服务。

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

- Indirect Prompt Injection paper 和 OWASP LLM Top 10 的关键风险项已完成第一轮精读，可支撑外部内容模糊数据/指令边界、prompt injection、敏感信息泄露、工具/插件访问控制和 excessive agency 的保守风险表述。
- OWASP Agentic AI Security Resources 的公开资源页、HTTP metadata 和 WP JSON 摘要已在 2026-07-12 复核，可支撑 goal hijacking、tool misuse、identity / privilege abuse、memory poisoning、insecure inter-agent communication、cascading failures、rogue agents、runtime containment、architectural monitoring 和 schema controls 等 agentic-specific 风险边界。白皮书全文未精读，因此不能支撑完整缓解清单或具体控制效果。
- MITRE ATLAS 的主页、manifest、latest v6 YAML、HTTP metadata、term catalog 和关键 Agentic AI 条目已在 2026-07-12 复核，可支撑 LLM Prompt Injection、AI Agent Tool Invocation、AI Agent Tool Poisoning、memory / MCP / computer-use case-study-derived regression set、Agentic AI platform 和 maturity 的保守边界。它不能支撑任意 mitigation、guardrail、detector、HITL 或监控方案的真实效果。
- Real Agentic Security Regression Set 已完成标准库 toy runtime，可作为把 MITRE ATLAS / OWASP 风险转成 case matrix 的模板；它定义并运行了 prompt injection、tool invocation、tool poisoning、memory poisoning、MCP / remote tool abuse、computer-use destructive action、runaway loop 和 inter-agent message 等 case，以及 expected decision、approval state、trace redaction、false positive / false negative 等记录字段。该结果只支撑 case 覆盖和记录字段设计，不能支撑真实防护效果。
- NIST AI RMF 的概述段落已完成第一轮精读，可支撑生产化章节的风险管理和治理视角；它不是 Agent 专用工程指南。
- “Prompt injection 不能只靠 prompt 解决；外部内容应被当作不可信数据，工具权限和写操作审批必须由应用/系统层控制”已升级为可入正文。Indirect Prompt Injection paper 支撑外部检索数据中的恶意 prompt 可影响应用行为和 API 调用的风险边界；OWASP 支撑风险分类，NIST 支撑全生命周期风险治理，Microsoft Prompt Shields 支撑 user prompt attack / document attack 分类、生成前检测接口和误报/漏报边界，OpenAI 工具调用文档支撑应用侧执行和控制边界。
- Microsoft Prompt Shields 文档已于 2026-07-12 复核检测层工程资料：`shieldPrompt` API 可以分析 `userPrompt` 和 `documents`，返回 `attackDetected` 字段；但文档也明确提示可能出现 false positives / negatives，并建议 additional validation layers。因此它只能支撑“检测层应纳入安全 workflow”，不能支撑“接入检测后就安全”。
- Anthropic jailbreak / prompt injection mitigation 文档已于 2026-07-12 复核另一组官方工程资料：直接 jailbreak / prompt injection 和 indirect prompt injection 是不同 threat model；网页、邮件、文档、OCR 输出和 tool results 等第三方内容应作为不可信数据处理；工程上可结合 `tool_result` 边界、来源说明、JSON encoding、tool output screening、最小权限、red-team 和持续监控。它支撑这些防护层应进入系统设计，但不证明任意 classifier、prompt、JSON encoding 或 computer-use 机制的真实拦截率。
- OpenAI Agents SDK 和 Semantic Kernel 文档已补充第一轮工程资料，可支撑 guardrails、human approval、tool approval、sensitive trace 控制和 task automation approval 的保守表述；标准库 prompt injection / tool permission 实验、安全 regression set 和审批状态恢复实验已覆盖最小权限、trace 脱敏、误报/漏报字段、多类风险 case、审批恢复、参数快照和幂等执行。“高风险工具应使用最小权限、参数校验、guardrails、人工确认、审批状态恢复和审计 trace 的组合”已升级为可入正文。Real OpenAI Agents SDK Guardrail Validation 已完成本地 fake-model SDK run，支撑 input/output/tool guardrail 运行位置和本地函数工具副作用前后边界；Agents SDK 2026-07-12 复核进一步支撑 tool guardrails 只覆盖 `function_tool`、hosted shell 不支持 `needs_approval/on_approval`、trace 默认可捕获敏感数据、serialized RunState 应按持久化敏感数据治理的边界；Real LangGraph Interrupt Recovery 已完成 `MemorySaver` 最小 run 和 `SqliteSaver` 本地 SQLite 同进程 graph 重建恢复 case、双本地 Python 进程 prepare/resume case 和双本地 Python 进程并发 resume case，支撑一个真实框架 pause/resume 观察和本地 SQLite 同进程/双进程恢复和并发 resume 观察；Real Prompt Injection / Permission harness 已完成本地 deterministic tool-permission control，支撑固定 tool calls 下的危险工具计数、prompt-only toy side effects、policy-enforced 写工具拒绝和 trace 脱敏逻辑。仍需真实模型 / 框架 guardrail、hosted/MCP/Shell/ApplyPatch 工具覆盖、部署式 HITL 与检测层实验验证误报、漏报和覆盖范围。
- LangGraph current docs 已补充 HITL interrupt / persistence 的框架机制证据：`interrupt()` 可暂停 graph execution，`Command(resume=...)` 可恢复，checkpointer 按 `thread_id` 保存 graph state snapshots，approval workflow、review/edit state 和 tool 内中断可放在 critical actions 前；但文档也明确 resume 会重新执行 node、`interrupt()` 前代码会重跑、interrupt 顺序不能随意变化、side effects 需要幂等或放在确认之后，内存型 checkpointer 不适合生产持久化。这支撑“审批要进入可恢复状态机”的窄边界，不证明真实 LangGraph 生产审批流程默认安全。
- Real LangGraph Interrupt Recovery completed run 覆盖 approved once、duplicate resume、rejected resume、tampered args、side-effect-before-interrupt、trace redaction，以及 `SqliteSaver` 本地 SQLite 同进程恢复、双本地 Python 进程 prepare/resume 和双本地 Python 进程并发 resume 的最小检查；它支撑 `MemorySaver` 下的最小真实框架观察和本地 SQLite 同进程/双进程恢复及并发 resume 观察，但不支撑部署式服务重启、真实审批 UI、真实副作用、真实服务并发恢复或生产安全结论。
- Anthropic MCP connector / tunnels 文档已补充 remote MCP tools 和私有网络 MCP server 的产品集成证据：allowlist/denylist、per-tool config、OAuth bearer token、third-party server trust review、data retention、outbound-only tunnel、inner TLS、allowed IPs、凭据保护和 shared responsibility。它们支撑“远程工具连接也要纳入权限、数据保留和审计设计”的窄边界，但不证明 connector、tunnel 或任意 MCP server 默认安全或生产可靠。
- Real MCP SDK Trace completed run 使用官方 MCP Python SDK / FastMCP stdio server 完成 tools/resources/prompts 的本地 SDK flow，记录写工具未转发、恶意 resource review 和 trace 脱敏。这支撑“SDK 接入后 host 仍需实现审批、resource review 和审计脱敏”的窄边界，但不证明真实 host UI、OAuth、URL mode、sampling、connector、tunnel 或跨 host 默认安全。
- MCP 标准化了工具、资源、提示、授权、roots、elicitation 和 sampling 等协议能力，但安全不是协议接入后自动完成；remote MCP、私有 MCP server、resources/prompts 和 sampling 仍需要最小权限、授权审查、用户确认、sandbox/runtime containment、数据保留审查和审计 trace。真实 host UI、OAuth、URL mode、sampling 和 connector/tunnel 行为仍需实验。
- 长上下文不能替代上下文治理，也不能替代生产数据边界；把更多外部内容、历史记忆或工具结果塞进上下文，会扩大 prompt injection、过时信息、隐私暴露和 trace 泄露风险，仍需来源标注、可信度过滤、最小必要字段和脱敏策略。
- 长期记忆可能提升持续交互体验，但也会引入错误写入、过时、权限和隐私风险；生产系统不能默认自动写入或默认提升表现，必须把写入守门、跨用户隔离、inspect/edit/delete、失效历史和敏感 trace 脱敏纳入权限模型。
- 对会调用工具或产生外部副作用的 Agent，只看最终答案不足以验证过程安全；生产审计需要把关键 trajectory / trace 作为 eval、审计和回归输入，尤其要记录工具参数、审批状态、错误恢复、外部内容来源、成本和敏感字段处理；真实平台字段覆盖、成本记录完整性和人工复核流程仍需验证。
- Agent trace 应记录输入、输出、中间步骤、工具调用、检索、错误、延迟/成本、反馈和版本信息，才能支撑调试、审计、回归和在线/离线评测；但 trace 本身也有隐私和数据保留边界，真实平台字段覆盖和脱敏效果仍需验证。
- Browser Use / Playwright / Anthropic Computer Use 资料已补充 browser agent 和 computer-use agent 的工程边界：浏览器动作、登录态 profile、截图、鼠标键盘控制、文件上传、表单提交、custom tools、human-in-the-loop、VM/container 隔离、domain allowlist、action validation/logging 和 Playwright action trace 都需要纳入权限、审计和脱敏设计。Anthropic 文档还提示网页或图片中的指令可能造成 prompt injection，并提供 screenshot classifier 作为一层确认机制；这些资料不能证明真实网站任务、点击精度、classifier 效果、CAPTCHA/stealth、合规或生产可靠性。
- 本地标准库 browser action trace audit 显示，browser/computer-use 工具的生产前检查应把 action trace、DOM/screenshot state、side-effect approval、profile isolation、file upload control、外部内容不可信边界、trace 脱敏和 failure classification 拆成可审计字段。Real Browser Playwright Validation completed run 进一步在固定本地 demo page 上记录 8 条真实浏览器 action record、DOM/screenshot hash、coordinate validation、redacted invoice 文件上传、submit order 审批阻断、destructive action 阻断和 trace.zip metadata。它们支撑权限和审计字段设计、固定执行层观察和 deterministic coordinate-loop 观察，但不证明真实 browser agent、防护层、screenshot classifier 或 sandbox 有效。
- 本地标准库 prompt injection / tool permission 实验显示，prompt-only 模式会产生退款副作用并泄露假 secret 到 trace；应用层权限策略可以阻断写工具、记录拒绝原因并脱敏敏感字段。该实验支撑最小权限、写工具审批和 trace 脱敏的流程设计；Real Prompt Injection / Permission harness 的 no-key 分支已完成本地 deterministic tool-permission control，但仍需真实模型和框架 guardrail completed run。
- 本地标准库安全 regression set 显示，回归测试应同时覆盖 prompt injection、授权、数据边界、金额阈值、敏感信息、破坏性工具、幂等性和 benign case；该实验支撑安全测试矩阵设计，但不证明真实 guardrail 拦截率。
- 本地标准库 agentic security regression set 显示，agentic-specific 安全回归还应覆盖 tool poisoning、memory poisoning、MCP / remote tool 外传、computer-use destructive action、runaway loop 和 inter-agent message 边界；toy runtime 中 `policy_enforced_hitl` 仍未阻断 computer-use destructive action，说明 HITL 不能替代 sandbox / runtime containment。该结果不证明真实 sandbox、detector、guardrail 或 HITL 有效。
- 本地标准库审批状态恢复实验显示，HITL approval 需要保存审批状态、参数快照和执行状态；重复恢复应返回已执行，拒绝后恢复应阻断，参数被篡改后恢复应阻断，trace 应脱敏。该实验支撑审批恢复和幂等性设计，但不证明真实框架的 HITL 行为。
- OpenAI Production / Cost / Latency / Rate Limit 文档已于 2026-07-12 复核生产成本和性能治理资料，可支撑“成本、延迟和限流是生产质量的一部分”的工程边界：上线前应记录 token/usage、organization/project 级 request/token rate limits、standard/project token rate-limit headers、重试、平均/P95 延迟、模型选择、预算阈值和降级策略。Token counting 文档还提醒 reported output/completion tokens 可能包含不可见的格式、channel、tool-call 或消息结构 token，因此预算和 `max_output_tokens` / `max_completion_tokens` 不能只按可见文本估算。真实 API / 应用中的成本、延迟、吞吐、质量取舍和具体优化效果仍需实验。
- OpenAI Batch / Flex / Prompt Caching 文档已补充异步批处理、低优先级处理和缓存前缀资料，可支撑“优化手段需要按 workload 选择并记录观测字段”的边界：Batch 应记录 status、error file、`custom_id` 映射和过期；Flex 应记录 timeout、`429 Resource Unavailable` 和 fallback；Prompt Caching 应记录 `cached_tokens`、`cache_write_tokens` 和 cache miss 原因。
- 本地标准库 production cost / latency / rate-limit audit 显示，生产成本、延迟和限流检查表应把 usage/token accounting、rate-limit headers、bounded retry、latency distribution、budget gate、model/output controls、Batch status / `custom_id` / expiration、Flex fallback 和 Prompt Caching read/write 拆成可审计字段。Real Production Cost / Latency / Rate-Limit harness 的本地 accounting control 进一步验证 usage/cache/latency/cost/budget 汇总逻辑。它们支撑字段设计和本地汇总检查，但不证明真实 API 成本、P95 latency、吞吐、缓存命中率、优化收益或生产可靠性。
- Real Batch / Flex / Prompt Caching harness 已完成 no-key 本地 deterministic cache/flex/batch metadata control，验证 cache usage 字段聚合、Flex fallback 记录、Batch JSONL metadata、`custom_id` 唯一性和 required result fields；Prompt Caching / Flex 仍需要真实 API key 才能观测真实 usage、cache read/write、resource unavailable 或 fallback，Batch job 提交默认 opt-in。该入口不证明任何真实收益或成本/延迟改善。
- OpenAI Moderation 和 Safety / Data Controls 文档已补充安全和数据治理资料，2026-07-12 复核仍可支撑 moderation signals、generated/input/output moderation、tool-calling moderation 覆盖限制、streaming moderation 限制、red-team、HITL、输入/输出约束、用户举报、`safety_identifier`、API key revoke、abuse monitoring logs、application state、ZDR/MAM、endpoint retention、prompt caching application state、remote MCP third-party retention、hosted container state、third-party network transmission 和 data residency 的工程边界。它们不证明任意检测层、数据控制配置或合规方案充分有效。
- 本地标准库 production safety / data governance checklist + object-level data-flow audit 显示，生产安全检查表应把 moderation policy signal、tool-calling 覆盖边界、streaming score 时机、`safety_identifier`、API key revoke、abuse logs / application state、remote MCP 第三方数据流、hosted execution state、file/vector store 对象、prompt caching prefix、browser/computer-use 数据面、data residency 和 red-team / 用户举报回流拆成可审计字段。Real Moderation Safety harness 已完成本地 policy-signal control，记录 `flagged`、categories、scores、latency、expected mismatch 和 policy decision，并覆盖误报 / 漏报分支。它们支撑 checklist、记录入口和应用层分支设计，但不证明真实 moderation、HITL、数据保留、对象删除、trace 脱敏、data residency 或合规方案有效。
- Tool use、MCP、Memory 和 Eval 章节中的风险边界都与生产化相关，生产章节应作为前面章节的收束，而不是独立安全清单。

## 待验证问题

- 针对具体 Agent 框架，guardrails、approval、sensitive trace、serialized state 和 tool permission 覆盖范围有哪些差异？已完成 OpenAI Agents SDK、LangGraph 和 Semantic Kernel 第一轮文档验证；Real OpenAI Agents SDK Guardrail Validation 已完成 input/output/tool guardrail 本地 runtime surface；Agents SDK 当前文档已明确 function-tool-only guardrail、hosted shell approval 限制、trace 默认敏感数据捕获和 RunState 持久化数据风险；Real LangGraph Interrupt Recovery 已完成 `MemorySaver` 最小 run；仍需横向比较真实 pause/resume、持久化审批状态序列化、参数快照、真实服务并发恢复、幂等执行、hosted/MCP/Shell/ApplyPatch 工具面和 trace 脱敏。
- MCP 工具生态中的安全边界应该如何落到 host、client 和 server 实现？
- Anthropic MCP connector / tunnels 的 allowlist/denylist、OAuth token、data retention、shared responsibility 和 tunnel credential rotation 在真实试跑中如何记录到 trace 和安全检查清单？
- Browser Agent 如何在真实或仿真网站中隔离 profile、限制登录态、确认表单/购物/上传等写操作，并记录可审计 action trace？Browser Use package surface、标准库 browser action trace audit 字段模板、固定 Playwright demo page workflow 和 deterministic coordinate-loop 已完成；Browser Use agent / 真实模型驱动 computer-use 对照仍待做。
- 真实模型 / 框架 guardrail / Prompt Shields 或同类检测层下，prompt injection 防护的误报、漏报、成本、延迟和人工审批负担如何测量？Real Prompt Injection / Permission harness 已完成 no-key 本地 tool-permission control；仍需配置 API key 后实际运行并比较 prompt-only、detector-only、policy-enforced 和 HITL 对照。
- agentic-specific 安全 regression set 应如何覆盖 goal hijacking、tool misuse、identity / privilege abuse、memory poisoning、insecure inter-agent communication、cascading failures 和 rogue agent / runaway loop 停止条件？
- 哪些日志字段既能支持审计，又不会引入新的隐私风险？已完成 observability/trace 第一轮验证，仍需脱敏和访问控制实验。
- 成本和延迟应该如何纳入 Agent eval？已补 OpenAI 官方 production / rate limit / cost / latency / token counting / Batch / Flex / Prompt Caching 边界，标准库字段 audit、真实 cost-latency 本地 accounting control 和 Batch/Flex/Caching 本地 metadata control 已完成；仍需真实 API / Cookbook 练习记录 token、usage、rate-limit headers、retry、平均/P95 latency、cost estimate、budget threshold、cache read/write 和失败样例。
- OpenAI API、remote MCP、hosted tools、files/vector stores、prompt caching 和 browser/computer-use 工具的数据保留边界如何落到项目 checklist？已补 OpenAI Safety / Data Controls 官方边界，并补标准库 object-level data-flow 字段模板；仍需真实项目按 endpoint、对象删除、third-party server、trace 字段和 project data controls 复核。
- Moderation-only、policy-enforced 和 HITL 组合在真实 prompt injection / tool calling 场景中的误报、漏报、延迟和人工复核负担如何测量？已补 OpenAI Moderation 官方边界和 Real Moderation Safety 本地 policy-signal control；当前仍需 API key completed run 与对照实验。
- Safety / data governance checklist 在真实 project 中哪些字段能从平台配置直接确认，哪些需要应用日志、runbook 或人工审计证明？标准库 checklist + object-level data-flow audit 已完成，仍需真实账户 / 项目验证。

## 本章小结

- 生产化 Agent 的重点是受控权限、可观测流程、可审计行为和可回滚系统。
- Prompt injection 不能只靠 prompt 解决，需要权限、隔离、校验、审计和测试共同控制。
- 写操作、敏感数据和外部副作用必须有明确边界。
- 成本和延迟是生产质量的一部分，不是上线后的附属问题。
- 初学者做生产化练习时，应先实现只读、安全、可观测的小 Agent，再逐步增加能力。

## References

### Security and Risk

- [OWASP Top 10 for Large Language Model Applications](../sources/source-cards/2026-owasp-llm-top-10.md)
- [OWASP Agentic AI Security Resources](../sources/source-cards/2026-owasp-agentic-ai-security.md)
- [MITRE ATLAS](../sources/source-cards/2026-mitre-atlas.md)
- [NIST AI Risk Management Framework](../sources/source-cards/2026-nist-ai-rmf.md)
- [Microsoft Prompt Shields Documentation](../sources/source-cards/2026-microsoft-prompt-shields-docs.md)
- [Anthropic Jailbreak and Prompt Injection Mitigation Documentation](../sources/source-cards/2026-anthropic-jailbreak-mitigation-docs.md)
- [Google Cloud Responsible AI Documentation](../sources/source-cards/2026-google-responsible-ai-docs.md)
- [Anthropic MCP Connector and Tunnels Documentation](../sources/source-cards/2026-anthropic-mcp-docs.md)
- [Browser Use and Playwright Browser Automation References](../sources/source-cards/2026-browser-use-playwright.md)
- [Anthropic Computer Use Tool Documentation](../sources/source-cards/2026-anthropic-computer-use-docs.md)
- [Browser Action Trace Audit](../experiments/browser-action-trace-audit/README.md)
- [OpenAI Production, Cost, Latency and Rate Limit Documentation](../sources/source-cards/2026-openai-production-cost-latency-docs.md)
- [OpenAI Batch, Flex Processing and Prompt Caching Documentation](../sources/source-cards/2026-openai-batch-flex-prompt-caching-docs.md)
- [Real LangGraph Interrupt Recovery](../experiments/real-langgraph-interrupt-recovery/README.md)
- [OpenAI Moderation Documentation](../sources/source-cards/2026-openai-moderation-docs.md)
- [OpenAI Safety Best Practices and Data Controls Documentation](../sources/source-cards/2026-openai-safety-data-controls-docs.md)

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
- [Real Prompt Injection 与工具权限实验结果](../experiments/real-prompt-injection-permission/results-2026-07-11.md)
- [Real Agentic Security Regression Set](../experiments/real-agentic-security-regression-set/README.md)
- [Production Safety / Data Governance Checklist](../experiments/production-safety-data-governance/README.md)
- [Real Moderation Safety Validation](../experiments/real-moderation-safety-validation/README.md)
- [Production Cost / Latency / Rate-Limit Audit](../experiments/production-cost-latency-rate-limit/README.md)
- [References 覆盖矩阵](../references/coverage-matrix.md)
