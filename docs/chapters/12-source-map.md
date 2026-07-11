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

先读手册 01 和 04，再看 ReAct、Reflexion、Tree of Thoughts、LangGraph 文档、LangGraph current quickstart 和 Voyager。

阅读重点不是记住所有方法名，而是理解：模型如何在观察、行动、状态和反馈之间循环。
Agent/Workflow 与自治程度窄边界已升级为可入正文，可帮助理解固定 workflow、workflow-agent hybrid 和更开放 tool loop 是控制权连续谱，不是能力等级排行。
ReAct 推理/行动交替和 Tree of Thoughts 搜索式推理路径的机制边界已可入正文；二者适合学习架构思想，但不能写成真实任务默认更优或默认生产编排方案。
Workflow / Hybrid / ReAct-like 标准库对比实验已经完成，可帮助理解固定流程、受控动态查询和 tool loop 在成功率、工具调用数、失败原因和 trace 上的差异；真实模型 / Agent framework / repo issue 仍需后续实验。
LangGraph current docs 已完成第一轮复核：overview / quickstart 可作为 state graph 和 tool loop 学习入口，interrupts / persistence 可作为 pause/resume、checkpointer、`thread_id` 和 side-effect idempotency 的工程边界参考；仓库 `examples/` 已标注归档，只能作为历史架构形态参考。
Voyager 适合放在进阶阅读阶段：它支持 automatic curriculum、executable skill library、environment feedback、execution errors 和 self-verification 组成开放式具身 Agent 学习循环的研究机制；本手册还补了一个标准库 toy environment，帮助初学者先观察 curriculum、技能修正、verified skill library、sandbox rejection 和 trace。它们不能写成 Minecraft 以外默认有效，也不能写成技能库或无人工干预默认适合生产。

### LLM 接口与工具调用

先读手册 02 和 03，再看 Responses API、Function Calling docs、Google Responsible AI、Toolformer 和 MRKL。

阅读重点是区分：模型生成工具调用参数，应用程序执行工具，工具结果再回到模型上下文。
Tool use 连接外部 API、搜索、计算器等工具能力的基础概念已可入正文；MRKL 补充了 LLM 与外部知识源、离散推理模块组合的架构历史线；Function Calling 本身不执行工具的工程边界也已可入正文。Function Calling 2026-07-12 复核补强 namespace / `tool_search`、工具定义 input-token 成本、`tool_choice` / allowed tools、parallel function calling、Responses strict-mode normalization、custom tools / CFG 和 reasoning item 回传边界；Responses API 2026-07-12 复核进一步补强 function/custom/namespace/tool_search/MCP/hosted execution tools、`allowed_callers`、`output_schema`、remote MCP `allowed_tools` / `require_approval` / `authorization` 和 shell/local_shell/apply_patch/computer-use 等高风险工具面边界。跨框架 tool / function / plugin / retriever / flow 术语对照已完成第一轮，可帮助理解不同框架抽象层级；Real Semantic Kernel Plugin Validation 已补 native plugin / kernel function metadata、参数处理和应用层审批 wrapper 的本地 runtime 观察；真实模型参数修正、真实模块路由、OpenAPI/MCP plugin、真实框架默认行为和成本仍需后续实验。
上下文治理与结构化输出标准库实验已经完成，可帮助理解 free text、JSON mode、schema validation、schema-valid semantic error、旧资料冲突和外部文档注入的最小边界；Responses API 2026-07-12 复核补强 `include` 附加数据、conversation / `previous_response_id` state、`instructions` 不自动继承、`text.format`、`json_schema`、JSON mode 和 truncation 默认边界；Structured Outputs 2026-07-12 复核补强 supported models、refusal、mistakes、JSON mode explicit instruction / edge cases 和 schema/type divergence 边界。Real Structured Outputs / JSON Mode harness 已准备并接入统一 runner，当前无 API key 时完成本地 deterministic schema/semantic control，覆盖 parse failure、schema-valid semantic error 和 schema-valid semantic-ok 三类固定样例。真实 Responses API / Structured Outputs、refusal、retry、truncation、长上下文成本和跨模型稳定性仍需后续实验。
Google Responsible AI 适合补充模型限制和生产治理视角：grounding/factuality、数据质量、长度/结构限制、安全测试、过滤、用户反馈和内容监控都属于上下文与生产质量的一部分；它不证明任何具体过滤、grounding 或监控方案的真实效果。
Tool Calling 参数校验与重试的标准库模拟实验已经完成，可帮助理解应用层校验、错误回传、有限重试和 trace 字段；Real Tool Calling harness 已准备并接入统一 runner，当前无 API key 时完成本地 deterministic validation/retry control，覆盖 schema-valid 但业务非法参数、validation error、corrected tool call 和 toy tool execution。真实模型 / API 稳定性仍需后续实验。

### MCP 与工具生态

先读手册 05，再看 MCP official docs、MCP servers repo 和 Anthropic MCP connector / tunnels docs。

阅读重点是 host、client、server、tools、resources、prompts、authorization、roots、elicitation、sampling 和权限边界。尤其要注意：authorization 是 optional transport-level capability，roots 不等于 sandbox，token passthrough 被官方安全最佳实践禁止。
MCP 官方 versioning 文档说明协议版本使用 `YYYY-MM-DD` 标识最近一次向后不兼容变更；当前版本是 `2025-11-25`，但向后兼容更新可能不改变版本号，所以引用时仍要记录复核日期。
Anthropic MCP docs 适合用来学习具体产品集成：Messages API 如何连接 remote MCP tools、如何配置 allowlist/denylist、OAuth bearer token 和 per-tool config，以及 MCP tunnels 如何把私有网络中的 server 连接给 Claude。它不替代 MCP official specification，也不能证明 connector、tunnel 或任意 MCP server 默认安全或生产可靠。
Real MCP SDK Trace 已用官方 MCP Python SDK / FastMCP stdio server 跑通本地 tools/resources/prompts flow，可作为学习 SDK 最小通信和 host policy trace 的参考；它仍不代表真实 host UI、OAuth、URL mode、sampling、connector 或 tunnel 行为。

### RAG 与 Memory

先读手册 06，再看 RAG paper、Self-RAG、LlamaIndex、OpenAI File Search / Retrieval、LangGraph memory、MemGPT、MemoryBank、Generative Agents、Letta 和 Zep。

阅读重点是区分外部知识检索、短期状态、长期记忆、写入守门和隐私风险。
RAG 的外部知识访问、知识更新和 provenance 基础动机已可入正文；真实 RAG stack 的质量、成本和延迟仍需后续实验。
Self-RAG 适合放在进阶阅读阶段：它支持“不要盲目固定检索 top-k，检索必要性、passage relevance、answer faithfulness 和 citation accuracy 都需要评估”的边界，但不能写成现代工程 RAG 默认应采用 Self-RAG。
RAG / Memory 对比标准库实验已经完成，可帮助理解外部知识问题应走 RAG 和 citation，当前任务连续性应走 thread state，跨会话偏好/纠正事实应走 guarded long-term memory，敏感且无安全来源的问题应拒答。
RAG 最小 pipeline / citation 标准库模拟实验已经完成，可帮助理解 chunk metadata、retrieval trace、chunk-level citations 和无证据拒答；该实验现已补 deterministic retrieval strategy audit，覆盖 top-k 过小、metadata filter 错配、细 chunk + rerank terms 仍可能漏召回的固定失败样例；窄结论“RAG 是可观察工程 pipeline，不是单个 prompt 技巧”已可入正文。Real RAG Citation Synthesis harness 已完成本地 deterministic citation verifier control，覆盖 citation id、quote matching、grounded/ungrounded citation 和 unsupported grounded claim 的失败样例；Real LlamaIndex RAG Source-Node Validation 已用本地 `llama-index-core` / `VectorStoreIndex` / retriever 跑通 source-node metadata、trust filter、citation metadata 和无证据 `grounded=false` 的最小观察；真实 embedding / vector store / LLM synthesis、citation correctness、成本和延迟仍需后续实验。
LlamaIndex examples repo 已完成第一轮复核，可作为 RAG workflow、citation/source nodes、BM25、hybrid retrieval 和 agent/query engine 示例的代码参考；本地 LlamaIndex source-node run 可以补强真实框架结构观察，但不证明这些示例生产可用，也不证明某个检索或 rerank 策略默认最优。
OpenAI File Search / Retrieval docs 已于 2026-07-12 复核，可作为托管 RAG / vector store 实践参考：`file_search_call`、file citations、included search results、metadata filtering、query rewriting、ranking options、chunking、batch ingestion、rate limits、expiration、pricing、ZDR/data residency 和成本都应进入 trace / eval；它不证明 File Search 默认引用正确、默认低成本或默认生产可靠。
长期记忆写入守门标准库模拟实验已经完成，可帮助理解显式写入、敏感信息拒绝、低置信推断拒绝、用户纠正、失效历史和 trace 脱敏；Real LangGraph Memory Store Validation 已补真实框架 `InMemoryStore` 的 namespace、put/get/search/delete、删除后不召回、应用层 invalidated history wrapper 和 trace 脱敏观察。它同时提醒：过宽 prefix search 可看到多个 user namespace，跨用户授权不能假设由 store 自动完成。真实多会话 Agent / memory framework 的收益、污染、权限 UI、持久化和用户编辑流程仍需后续实验。

### Planning、Orchestration 与多 Agent

先读手册 07，再看 Tree of Thoughts、Reflexion、Multiagent Debate、AutoGen、CrewAI 和 LangGraph current docs。

阅读重点是任务拆解、状态管理、反馈、重规划、角色协作和成本。
Planner / Executor 标准库对比实验已经完成，可帮助理解一次性计划遗漏、missing evidence 校验、反馈重规划和 trace 字段；真实模型 / Agent framework / repo issue 仍需后续实验。
Reflection / Retry 标准库实验已经完成，可帮助理解 verified feedback、missing evidence retry、错误反思污染和 reflection trace；窄结论“Reflection 必须绑定可校验反馈、范围控制和 trace，未验证反思不应直接进入长期记忆或后续策略”已可入正文。真实模型、长期 episodic memory、人工评审和成本评估仍需后续实验。
多 Agent / Flow 控制标准库实验已经完成，可帮助理解角色协作、Flow 控制、重复读取、冲突和消息开销；Real Multi-Agent Framework Validation 已补 AutoGen AgentChat / CrewAI 的本地 fake-model researcher/reviewer runtime surface，也补了 LangGraph deterministic `StateGraph` researcher/reviewer state trace；“多 Agent 不是复杂任务默认升级路径”窄边界已可入正文。真实模型、token/latency/cost、冲突合并质量和人工评审负担仍需后续实验。
LangGraph current docs 的 interrupts / persistence 页面可帮助理解 `interrupt()`、checkpointer、`thread_id`、`Command(resume=...)`、node restart 和副作用幂等限制；Real LangGraph Interrupt Recovery harness 已完成 LangGraph 1.2.9 / `MemorySaver` 最小 run，并用 `langgraph-checkpoint-sqlite` 3.1.0 / `SqliteSaver` 完成本地 SQLite 同进程 graph 重建恢复 case、双本地 Python 进程 prepare/resume case 和双本地 Python 进程并发 resume case，覆盖批准、拒绝、参数 hash、重复恢复不重复执行、trace 脱敏和本地 SQLite 同进程/双进程恢复和并发 resume 观察；历史 plan-and-execute 和 human-in-the-loop notebooks 只能作为 planner / agent / replan 形态参考，不能证明当前 API、真实任务表现或生产审批安全。
Multiagent Debate 适合放在进阶阅读阶段：它支持多个模型实例多轮提出、辩论并汇总答案的研究机制，但不能写成工程多 Agent 默认减少幻觉或默认适合复杂任务。

### Evaluation 与 Observability

先读手册 08，再看 AgentBench、WebArena、τ-bench、OpenAI Evaluation guides、OpenAI Graders docs、OpenAI Evals repo、LangSmith、Phoenix、Browser Use 和 Playwright。

阅读重点是任务环境、trajectory、trace、offline/online eval、regression set、datasets、feedback 和错误分类。
公开 benchmark 不能直接代表真实业务 Agent 质量的窄边界已可入正文：AgentBench 和 WebArena 适合学习交互环境、长程任务、functional correctness 和失败分类，τ-bench 适合学习动态用户交互、领域 API tools、policy guidelines、数据库状态评测和多次试验一致性，OpenAI Evaluation guides、OpenAI Graders docs 和 OpenAI Evals repo 适合学习 task-specific / custom eval、trace grading、grader 类型、tool-call grading、datasets / eval runs、LLM-as-judge 校准和 reward hacking 风险；业务系统仍需自己的任务集、trace、权限检查和回归集。
OpenAI Evals platform 正在退役，所以阅读 OpenAI eval 资料时要区分“eval 方法”和“具体平台入口”。2026-07-12 复核确认 deprecations 页面写明 Evals platform 将在 2026-10-31 对既有 evals 变为 read-only，并计划 2026-11-30 shutdown；eval workflow 的 graders 也属于这次过渡。OpenAI Graders docs 仍可支撑 grader 类型、`sample.output_tools` tool-call grading、Python grader 约束、multigrader 的 RFT-only 边界和 reward hacking 风险，但本手册不把旧平台路径写成长期稳定教程。
τ-bench 原始 repo 已提示任务不是最新版，后续真实试跑应优先看 τ³-bench；本手册当前只把它作为评测设计 reference，不把旧 leaderboard 数字写成当前模型能力结论。
Trace-aware eval 标准库模拟实验已经完成，可帮助理解为什么 final-answer-only scoring 会漏掉无审批副作用工具和工具错误未恢复；Real Trace-Aware Eval harness 已完成本地 deterministic scorer control，进一步验证 final-only 会漏掉缺工具调用、缺 tool error trace 和缺 approval rejection；grader misalignment / reward hacking 标准库实验已经完成，可帮助理解 exact string、关键词式 judge、tool-call rule 和 majority multigrader 的不同误判；OpenAI Agent evals guide 补强了先看代表性 traces、再沉淀 datasets/eval runs 的流程边界；OpenAI Graders docs 补强了自动 grader、tool-call grading、Python grader 执行约束、multigrader RFT-only 和 reward hacking 风险边界。真实 Agent trace、真实 LLM-as-judge 和人工复核仍需后续实验。
Browser Use / Playwright source card 已完成第一轮复核：它支持浏览器 Agent 的动作层、profile/auth 风险、custom tools 和 trace viewer 边界；Anthropic Computer Use source card 补强 screenshot/mouse/keyboard control、VM/container 隔离、domain allowlist、human confirmation、screenshot prompt injection classifier、action validation/logging、limitations、data retention 和 token overhead。Real Browser Use Package Surface Validation 已完成 `browser-use==0.13.3` package metadata、console scripts 和 Agent / BrowserProfile / Tools 源码表面检查。Browser action trace 标准库 audit 已补 action trace、DOM/screenshot state、side-effect approval、profile isolation、file upload policy、external content boundary、trace redaction 和 failure classification 字段模板；Real Browser Playwright Validation 已完成固定本地 demo page workflow 和 deterministic computer-use-style loop，记录 8 条 action record、DOM/screenshot hash、coordinate validation、redacted invoice 文件上传、submit order 审批阻断、destructive action 阻断和 trace.zip metadata。真实 Browser Use agent / 模型驱动 computer-use agent、模型任务成功率、点击精度、classifier 行为、CAPTCHA/stealth、成本、延迟、合规和生产可靠性仍待实验。

### Production、安全与治理

先读手册 09，再看 OWASP LLM Top 10、OWASP Agentic AI Security resources、MITRE ATLAS、NIST AI RMF、Microsoft Prompt Shields、Anthropic jailbreak / prompt injection mitigation、Google Responsible AI、OpenAI Moderation、OpenAI Safety / Data Controls 文档、OpenAI Production / Cost / Latency / Rate Limit 文档、OpenAI Batch / Flex / Prompt Caching 文档、OpenAI Agents SDK guardrails / human-in-the-loop / tracing 文档，以及 Semantic Kernel Plugins 文档。

阅读重点是 prompt injection、权限、工具审批、guardrails 的执行位置、agentic-specific 风险、数据边界、审计、人工确认、降级、敏感 trace 控制和风险管理。
Prompt injection / tool permission 标准库模拟实验已经完成，可帮助理解 prompt-only 风险、只读/写工具分离、写工具审批拒绝和 trace 脱敏；Microsoft Prompt Shields 补强 user prompt attack / document attack 分类、生成前检测 API 和误报/漏报边界；Anthropic mitigation docs 补强 direct / indirect threat model、untrusted tool result handling、JSON encoding、tool output screening、least privilege、red-team 和 monitoring；Real Prompt Injection / Permission harness 已完成 no-key 本地 deterministic tool-permission control，覆盖固定 tool calls、危险写工具请求计数、prompt-only toy side effects、policy-enforced 写工具拒绝和 trace 脱敏，但真实模型 / API 行为仍未验证；Real LangGraph Interrupt Recovery harness 已补真实框架 HITL 恢复 completed run，覆盖 `MemorySaver` 最小 graph 和 `SqliteSaver` 本地 SQLite 同进程 graph 重建恢复 case、双本地 Python 进程 prepare/resume case 和双本地 Python 进程并发 resume case；真实模型、框架 guardrail、检测层、tool-output screening、部署式 HITL approval 和生产副作用仍需后续实验。
OWASP Agentic AI Security resources 的公开页面和 WP JSON 摘要已在 2026-07-12 复核，补强了 goal hijacking、tool misuse、identity / privilege abuse、memory poisoning、insecure inter-agent communication、cascading failures、rogue agents、runtime containment、architectural monitoring 和 schema controls 等风险分类；但白皮书全文未精读，所以它只能支撑保守风险边界和 regression set 设计，不能支撑具体 mitigation 有效性。
MITRE ATLAS 的主页、manifest、latest v6 YAML、term catalog 和关键 Agentic AI 条目已在 2026-07-12 复核；它适合学习 AI / Agentic AI attack techniques、platform、maturity 和 case-study-derived regression cases，例如 LLM Prompt Injection、AI Agent Tool Invocation、AI Agent Tool Poisoning、memory poisoning、MCP / remote tool abuse 和 computer-use destructive action。它不证明 ATLAS mitigation 条目在真实系统中有效。
Real Agentic Security Regression Set 已经把这些来源整理成 case matrix、记录字段、对照组和通过标准，并完成标准库 toy runtime；它适合后续迁移到真实模型 / 框架实验，但当前结果只验证 case 覆盖、字段设计、误报/漏报统计和 HITL 与 sandbox/runtime containment 的边界，不是真实防护效果。
Google Responsible AI 补强另一个生产边界：即使有内置 safety filters，应用仍需要按用例做 security risk assessment、safety testing、必要时配置 filters、收集用户反馈并监控内容。
OpenAI Moderation 文档 2026-07-12 复核补充检测信号边界：moderation scores 应作为应用 policy signals，而不是自动阻断决定；tool-calling moderation 覆盖 conversation content 中的 tool-call arguments 和 tool outputs，但不覆盖 tool names、descriptions、schemas 或 response-format schemas；streaming scores 要等完整输出后才有；`/v1/moderations` retention matrix 边界也已记录。OpenAI Safety / Data Controls 文档补充数据治理边界：red-team、HITL、用户举报、`safety_identifier`、API key revoke、abuse monitoring logs、application state、ZDR/MAM、endpoint retention、prompt caching application state、remote MCP third-party retention、third-party network transmission、hosted container state 和 data residency。Production safety / data governance checklist 标准库实验已把这些边界以及 remote MCP、hosted execution、file/vector store、prompt caching、browser/computer-use 对象级 data-flow 字段拆成可审计字段；Real Moderation Safety harness 已完成本地 deterministic policy-signal control，覆盖 result fields、误报/漏报分支和应用层 policy decision；真实 Moderation API completed run 仍待做。阅读时要区分“API 数据默认不用于训练”和“不会保留任何数据”，二者不是同一件事。
OpenAI Production / Cost / Latency / Rate Limit 文档适合学习生产质量的数字化记录：usage dashboard、billing / usage limits、staging / production project 隔离、organization/project 级 rate limits、standard/project token rate-limit headers、exponential backoff、token counting、`max_tokens` / `max_output_tokens`、streaming、batching、模型选择和预算阈值。2026-07-12 复核还确认 token counting 文档提醒 reported output/completion tokens 可能包含不可见的格式、channel、tool-call 或消息结构 token，练习记录不应只数可见输出。OpenAI Cookbook 的 Usage/Cost 和 Rate limits recipe 适合把这些边界转成初学者练习字段：`start_time`、`end_time`、`bucket_width`、`group_by`、`project_id`、`line_item`、`amount.value`、`amount.currency`、429 / `RateLimitError`、retry、主动节流、RPM/RPD/TPM、fallback 和 batching。OpenAI Batch / Flex / Prompt Caching 文档适合学习更具体的优化边界：Batch 用于不需要即时响应的离线任务，Flex 用于可容忍慢响应和资源不可用的低优先级任务，Prompt Caching 需要稳定长前缀和 `cached_tokens` / `cache_write_tokens` 观测。Production cost / latency / rate-limit 标准库 audit 已把这些资料拆成 usage/token accounting、rate-limit headers、bounded retry、latency distribution、budget gate、model/output controls、Batch boundary、Flex fallback 和 Prompt Caching observability 字段；Real Production Cost / Latency / Rate-Limit harness 已完成本地 deterministic accounting control，验证 usage/cache 字段提取、rate-limit header 解析、平均/P95 latency、fixture cost estimate 和 budget action 汇总逻辑；Real Batch / Flex / Prompt Caching harness 已完成 no-key 本地 deterministic cache/flex/batch metadata control，验证 cache usage 字段聚合、Flex fallback 记录、Batch JSONL metadata、`custom_id` 唯一性和 required result fields；Batch 提交默认 opt-in。它们支撑“成本、延迟和限流要进入生产检查清单”，但不证明任何具体应用的真实成本、P95 延迟、吞吐、fallback 质量、缓存命中率或优化收益。

### 框架生态与实践

先读手册 10 和 11，再横向阅读 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI、Semantic Kernel、OpenAI Cookbook 的具体 recipe，以及 SWE-agent / mini-SWE-agent 这类软件工程 Agent 资料。

阅读重点是选择维度、可迁移概念和可复现练习，而不是追随单一框架或照搬复杂 demo。
框架选择 rubric smoke test 已经完成，可帮助理解如何把框架比较拆成 required、nice-to-have、avoid、missing required 和 cautions；窄结论“框架应按任务难点和能力边界比较，不能写成某个框架默认最好”已可入正文。Real Framework Same-Task Comparison 已补一个本地同任务 run：同一退款政策检索 + 审批退款任务分别用 OpenAI Agents SDK `FunctionTool` schema / `needs_approval` / direct `ToolContext` invocation / fake-model `Runner` approval-resume loop、LangGraph `StateGraph` / conditional edge、LlamaIndex `VectorStoreIndex` / retriever source nodes 和 Semantic Kernel plugin metadata / `Kernel.invoke()` 跑通，并明确哪些能力来自框架、哪些来自应用层 policy / side effect / redaction。OpenAI Agents SDK 2026-07-12 复核进一步补强 function-tool-only guardrail、hosted/built-in tool 不走同一 tool-guardrail pipeline、hosted shell approval 限制、trace 默认敏感数据捕获和 serialized RunState 治理边界。Real Multi-Agent Framework Validation 进一步补 AutoGen AgentChat / CrewAI / LangGraph 的本地 fake-model / deterministic-node multi-agent runtime surface。`openai-agents==0.18.2` 与 `semantic-kernel==1.36.0` 当前需要分两组临时依赖运行；这属于依赖组合边界，不是框架能力排名。这些实验适合学习比较方法，但不证明真实模型、真实 HITL UI、hosted tracing、serialized state 存储治理、成本、延迟、多 Agent 协作质量或生产可靠性。模型 tool selection 和完整生产面横向实验仍需后续试跑。
实践路线 smoke harness 已经完成，可帮助理解如何把结构化输出、工具参数、RAG 引用、eval cases 和成本闸门组织成可运行验收流程；readiness audit 进一步检查 6 个跟练项目卡片是否包含 prerequisites、setup/run commands、acceptance checks、trace fields、failure examples、references 和 boundaries。窄结论“Cookbook 具体 recipe 可作为实践项目参考，但不能替代 API 文档、生产安全指南或本地实验”已可入正文。Usage/Cost 和 Rate limits recipe 已补字段级复核，可作为项目 8 的 usage/cost/rate-limit/retry/fallback/batching 表格参考。真实 Cookbook / API recipe 的依赖、真实 usage/cost、真实限流行为、成本和初学者阻塞点仍需后续试跑。
SWE-agent 适合放在进阶实践阶段：它支持 agent-computer interface、仓库导航、文件编辑和测试执行的重要性；mini-SWE-agent 则补强当前轻量 coding agent 入口、bash-only 最小控制流、confirm/yolo/human 模式、trajectory、cost/call limit、CLI options、默认配置和 runtime/trajectory 边界。Real mini-SWE-agent CLI Surface Validation 已验证 `mini-swe-agent==2.4.5` 的本地 CLI 和默认 `mode: confirm` / `cost_limit:` 表面。Real mini-SWE-agent Runtime Surface Validation 已用 deterministic fake model 跑通 `InteractiveAgent` / `LocalEnvironment` toy repo run，记录失败测试、实现 patch、最终测试通过、trajectory、fake API call/cost，并观察到 configured env marker 会进入 trajectory。Real Repo Issue Agent Toy 已补固定 workflow baseline 和确定性 workflow-agent hybrid baseline：临时 toy repo 初始测试失败、实现修复后测试通过、diff、trajectory、建议、人工审批和风险命令拒绝可记录。真实 repo issue / coding agent 练习仍必须用 toy repo、sandbox、diff/rollback、权限确认、测试 trace 和 trajectory 脱敏，不应直接在重要仓库上运行。
Browser Use、Playwright 和 Anthropic Computer Use 适合放在 Browser / Computer Use Agent 进阶实践阶段：它们支持理解网页动作、页面/截图状态、文件上传、表单提交、登录态/profile、VM/container 隔离、action validation/logging 和 action trace；但练习必须先用 demo site、测试账号、隔离 profile 或 VM/container、人工确认和 trace 脱敏，不应直接操作真实购物、付款、投递或重要账号。

## 当前 Source Card 状态

当前资料库已经覆盖这些大类：

- Agent 架构：ReAct、Reflexion、Tree of Thoughts、Voyager、LangGraph docs、LangGraph examples repo。
- Tool Use：Toolformer、MRKL Systems、OpenAI Function Calling docs、Responses API docs。
- MCP：MCP official docs、MCP servers repo、Anthropic MCP connector / tunnels docs。
- RAG：RAG paper、Self-RAG、LlamaIndex docs、LlamaIndex examples repo。
- Memory：MemGPT、MemoryBank、Generative Agents、LangGraph memory、Letta、Zep。
- Eval / Observability：AgentBench、WebArena、τ-bench、OpenAI Evaluation guides、OpenAI Graders docs、OpenAI Evals repo、LangSmith、Phoenix、Browser Use / Playwright、Anthropic Computer Use。
- Security / Production：Indirect Prompt Injection paper、OWASP LLM Top 10、OWASP Agentic AI Security resources、MITRE ATLAS、NIST AI RMF、Microsoft Prompt Shields、Anthropic jailbreak mitigation、Google Responsible AI、OpenAI Moderation docs、OpenAI Safety / Data Controls docs、OpenAI Production / Cost / Latency docs、OpenAI Batch / Flex / Prompt Caching docs、OpenAI Agents SDK、Semantic Kernel。
- Frameworks / Multi-agent：OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI、Semantic Kernel、Multiagent Debate。
- Practice：OpenAI Cookbook、MCP servers repo、OpenAI Evaluation guides、OpenAI Evals repo、Browser Use / Playwright、Anthropic Computer Use。
- Software Engineering Agents：SWE-agent、mini-SWE-agent。

核心 source cards 已经完成多轮链接、元数据和关键段落复核，能支撑章节中的学习方向、术语边界和部分验证结论。主索引已同步这些状态：论文、官方文档、框架文档和安全资料会标注“关键段落已精读 / 部分验证 / 下一步真实实验”。Claim Boundary Consistency Audit 已补 claim ledger、coverage matrix 和若干章节待验证措辞的本地文本边界检查，防止把窄口径 `可入正文` 或 no-key local control 误写成真实系统表现已验证；Chapter Evidence Alignment Audit 已补 01-11 章 `已验证结论`、`待验证问题`、claim ledger / coverage matrix 控制链接和章节结论边界措辞检查；Source Reference Integrity Audit 已补 source-card index、source card 元数据/段落、章节 References 和本地 Markdown links 的结构完整性检查，防止漏索引和本地断链；Source URL Availability Audit 已补联网快照，本次 56 张 source cards 的 73 个主 URL 均可访问；Source Card Evidence Quality Audit 已补进入正文 source cards 的支撑证据、风险段落和边界措辞检查。这些 audit 仍不能替代人工精读、资料内容事实校验、章节解释复核或真实实验。OpenAI Cookbook 已完成 Structured Outputs、File Search RAG、OpenAI Evals、Agents SDK trace/eval、Usage/Cost 和 Rate limits 等具体 recipe 的第一轮复核；其中 Usage/Cost 和 Rate limits 已补字段级证据，但仍不是生产效果证明；实践路线 smoke harness + readiness audit 已补跟练项目结构验证，但仍不是 API recipe 真实试跑。OpenAI Evaluation guides 已补 eval-driven development、trace grading、dataset/eval run、LLM-as-judge caveats 和平台退役边界；OpenAI Graders docs 已于 2026-07-12 复核，补强 grader 类型、tool-call grading、Python grader 约束、multigrader RFT-only、reward hacking 风险和 Evals/graders 退役时间线，标准库 grader audit 已补误判结构；OpenAI Agents SDK docs 已于 2026-07-12 复核，补强 function-tool-only guardrail、hosted shell approval 限制、trace 默认敏感数据捕获、serialized RunState 治理和 Codex tool experimental 边界；OpenAI Function Calling docs 已于 2026-07-12 复核，补强官方 tool-calling flow、应用侧执行、namespace / `tool_search`、工具定义 input-token 成本、`tool_choice` / allowed tools、parallel function calling、Responses strict-mode normalization、custom tools / CFG 和 reasoning item 回传边界，Real Tool Calling harness 已补本地 deterministic validation/retry control；OpenAI Text Generation docs 已于 2026-07-12 复核，补强 SDK `output_text` shortcut、Responses API recommendation、prompt-in-code guidance 和 reusable prompt objects deprecation 边界；OpenAI Responses API docs 已于 2026-07-12 复核，补强 `include`、conversation / `previous_response_id`、instructions、`text.format` / `json_schema`、tool choice、remote MCP permission fields、hosted execution tools 和 truncation 默认边界；OpenAI Structured Outputs docs 已于 2026-07-12 复核，补强 supported models、schema adherence、JSON mode explicit instruction / edge cases、refusal、mistakes 和 schema/type divergence 边界，Real Structured Outputs / JSON Mode harness 已准备并接入统一 runner，且无 API key 时已完成本地 deterministic schema/semantic control；OpenAI File Search / Retrieval docs 已于 2026-07-12 复核，补强 hosted `file_search`、vector stores、included search results、metadata filtering、query rewriting、ranking/chunking、batch ingestion、rate limits、pricing/ZDR/data residency、expiration 和 deletion consistency 边界；OpenAI Moderation docs 已补 moderation signals、result fields、tool-calling coverage 和 streaming 限制，Real Moderation Safety harness 已补本地 deterministic policy-signal control；OpenAI Safety / Data Controls docs 已补 red-team、HITL、safety identifier、API key revoke、abuse logs、application state、ZDR/MAM、remote MCP third-party retention 和 data residency 边界；production safety / data governance checklist 已补 object-level data-flow audit，覆盖 remote MCP、hosted execution、file/vector store、prompt caching 和 browser/computer-use 字段模板；OpenAI Production / Cost / Latency docs 已补 usage dashboard、organization/project 级 rate limits、standard/project token rate-limit headers、exponential backoff、token counting、非可见 output token 计数 caveat、latency/cost optimization 和 project isolation 边界；OpenAI Batch / Flex / Prompt Caching docs 已补异步批处理、低优先级处理和缓存读写观测边界；production cost / latency / rate-limit 标准库 audit 已补字段审计结构；Real Production Cost / Latency / Rate-Limit harness 已补本地 deterministic accounting control；Real LangGraph Interrupt Recovery 已完成 `MemorySaver` 最小 run 和 `SqliteSaver` 本地 SQLite 同进程 graph 重建恢复 case、双本地 Python 进程 prepare/resume case 和双本地 Python 进程并发 resume case；Real Tool Calling harness 和 Real Structured Outputs / JSON Mode harness 已完成本地 control，Real Batch / Flex / Prompt Caching harness 已完成本地 deterministic metadata control；Real Moderation Safety harness 已完成本地 policy-signal control；Real Production Cost / Latency / Rate-Limit harness 已完成本地 accounting control，真实 API run 仍待做。仍处于候选或只完成链接复核的资料，不能支撑过强的工程断言。

Claim To Chapter Landing Audit 已补 29 条 `可入正文` 结论到 50 个声明章节落点的文本对齐检查，防止台账结论没有真正进入目标章节；它仍只验证文本落点，不验证外部事实、章节解释正确或真实系统表现。

Source To Claim Support Audit 已补 01-11 内容章节直接引用的 55 张 source cards 到 claim ledger `支撑资料` 列的文本追溯检查，防止章节引用资料但台账没有纳入证据链；它不扫描第 12 章 source map 的全量资料索引，也不验证外部事实、章节解释正确或真实系统表现。

Coverage matrix 的“入门资料”列现在优先使用本手册章节和已精读的核心 docs / papers，目的是给初学者提供阅读入口；它不等同于把真实模型、真实框架或真实生产效果升级为已验证结论。

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
- Coverage matrix 显示 Agent/Workflow、LLM / Context、Evaluation / Observability、Production / Security 和 Memory / 知识库治理都已补标准库模拟实验；RAG、Browser、LangGraph interrupt、LangGraph memory store 和 MCP 已补若干本地真实框架 / 工具 harness。这些实验支撑流程、trace 和窄口径框架原语观察，但仍需要真实模型、真实框架端到端任务和真实多会话实验来升级质量结论强度。
- Agent / Workflow 和自治程度边界已补标准库 workflow / hybrid / ReAct-like 对比实验，窄结论“Agent 和 Workflow 是控制权与编排方式的连续谱，自治程度不是能力等级”已可入正文；仍缺真实模型 / Agent framework / repo issue、token/latency/cost、权限确认和工具错误恢复实验。
- Agent 架构模式边界已补论文 / 框架资料、Voyager embodied lifelong agent 资料、LangGraph current quickstart / interrupts / persistence / historical examples 和多组标准库对比实验，窄结论“ReAct 是推理/行动交替模式”“Tree of Thoughts 是搜索式推理路径而非生产编排框架”“Voyager-style automatic curriculum / skill library / environment feedback 是开放式具身 Agent 的研究机制”“复杂 Agent 架构不是默认更可靠，需要用 trace、成本、失败原因、权限和实验结果比较”已可入正文；Voyager-style toy environment 已覆盖 curriculum task、技能修正、verified skill library、sandbox rejection 和 stop condition 的最小 trace 形状；仍缺真实模型 / 框架 / Voyager / Minecraft 或其他环境任务中的收益、成本、延迟和错误恢复实验。
- Planner / Executor 已补标准库对比实验，窄结论“计划需要可执行，执行结果需要证据校验，失败需要反馈给 planner 并记录重规划 trace”已可入正文；Reflection / Retry 已补标准库错误反思实验，窄结论“Reflection 需要可校验反馈、范围控制和 trace，未验证反思可能污染后续尝试”已可入正文；仍缺真实模型 / 框架 / repo issue、token/latency/cost、长期记忆和人工评审实验。
- 多 Agent 已补 Multiagent Debate 论文、AutoGen/CrewAI/LangGraph 框架资料、标准库单流程 / 无控制多 Agent / Flow 控制多 Agent 对比实验，以及 AutoGen AgentChat / CrewAI / LangGraph 本地 fake-model / deterministic-node runtime run。窄结论“多 Agent 是一种协作/编排选择，不是复杂任务默认升级路径；引入前应明确角色边界、证据分配、冲突处理、review trace 和成本预算”已可入正文；仍缺真实模型、token/latency/cost、复杂任务、冲突合并质量和人工评审负担实验。
- MCP official docs 已补 versioning、2025-11-25 changelog、tools/resources/prompts/authorization/roots/elicitation/sampling spec 和 Security Best Practices 第一轮精读；Anthropic MCP connector / tunnels docs 已补 remote MCP tool 接入、allowlist/denylist、OAuth bearer token、data retention、私有网络 tunnel 和 shared responsibility 产品集成边界；MCP 最小 trace 标准库模拟实验、本地 stdio JSON-RPC harness 和官方 MCP Python SDK / FastMCP stdio harness 已完成，窄结论“authorization 是 optional，roots 不等于 sandbox，token passthrough 被禁止，高风险能力仍需权限/隔离/审计/trace 脱敏”已可入正文；仍缺真实 host UI、Anthropic MCP connector / tunnels 试跑、权限确认、URL mode / OAuth、sampling、恶意 resource/prompt 和 host 实现差异实验。
- Tool Use / Function Calling 已补 Toolformer、MRKL Systems、OpenAI Function Calling / Responses API、标准库参数校验/重试模拟实验、跨框架术语对照和 Real Semantic Kernel Plugin Validation，窄结论“tool use 可以连接外部工具能力”“LLM 可与外部知识源 / 离散推理模块组合”“应用层校验、错误回传、有限重试”和“不同框架术语不能直接互换”已可入正文；Function Calling 2026-07-12 复核补强 namespace / `tool_search`、工具定义 input-token 成本、`tool_choice` / allowed tools、parallel function calling、Responses strict-mode normalization、custom tools / CFG 和 reasoning item 回传边界；Responses API 2026-07-12 复核补强更广的 tool surface、remote MCP permission fields、hosted execution tools 和 forced tool choice 边界；Real Semantic Kernel run 支撑 native plugin/function metadata、required/type 参数处理、应用层写工具审批 wrapper 和 side-effect trace 的窄观察；Real Tool Calling harness 已补本地 deterministic validation/retry control，支撑 parser、validator、错误反馈和 toy tool execution 的固定样例边界；仍缺真实 Function Calling / Responses API completed run、真实模块路由、OpenAPI/MCP plugin、HITL UI、大工具面选择质量、hosted/MCP/Shell/ApplyPatch/computer-use guardrail 覆盖和真实框架同任务对照。
- LLM / Context 已补官方文档精读、Google Responsible AI、标准库输出解析 / 上下文治理模拟实验和上下文策略对比实验，窄结论“LLM 应用输入输出不只是字符串”“schema validation 不等于语义正确”和“长上下文不能替代来源、时效、权限治理”已可入正文；Text Generation 2026-07-12 复核补强 SDK `output_text` shortcut、Responses API recommendation、prompt-in-code guidance 和 reusable prompt objects deprecation 边界；Responses API 2026-07-12 复核补强 `include`、conversation / `previous_response_id` state、instructions、`text.format` / `json_schema`、JSON mode 和 truncation 默认边界；Structured Outputs 2026-07-12 复核补强 supported models、refusal、mistakes、JSON mode explicit instruction / edge cases 和 schema/type divergence 边界；Google Responsible AI 补强 grounding/factuality、数据质量、安全测试和监控边界；Real Structured Outputs / JSON Mode harness 已准备并接入统一 runner，当前无 API key 时完成本地 deterministic schema/semantic control；仍缺真实 Responses API / Structured Outputs、refusal、semantic validator、retry loop、prompt builder 迁移、truncation、长上下文 token/latency/cost 和跨模型稳定性实验。
- RAG / Memory 已补标准库对比实验，可支撑外部知识、thread state、guarded long-term memory 和无安全来源拒答的分层边界；RAG 已补 LlamaIndex source-node harness，Memory 已补 LangGraph `InMemoryStore` harness；仍缺真实 RAG / memory framework / 多会话质量实验。
- RAG 已补 RAG paper、Self-RAG、LlamaIndex 工程流程资料、LlamaIndex examples repo、OpenAI File Search / Retrieval docs、标准库最小 pipeline / citation / retrieval strategy 模拟实验、Real RAG Citation Synthesis verifier control 和 Real LlamaIndex RAG Source-Node Validation，窄结论“RAG 的动机包括外部知识访问、知识更新和 provenance”“工程 RAG 是 loading、indexing、storing、querying/retrieval、response synthesis 和 evaluation 等阶段组成的可观察 pipeline，不是单个 prompt 技巧；最小可治理 RAG 需要 chunk metadata、retrieval trace、citation/source 绑定、citation verifier、检索必要性/相关性评估和无证据拒答或 `grounded=false` 标记”已可入正文；LlamaIndex examples 补强了 citation/source node、RAG workflow、BM25 和 hybrid retrieval 的示例证据，标准库 strategy audit 补强了 top-k、filter、chunking、rerank 都必须被 eval 记录验证的本地失败样例，Real RAG Citation control 补强了 citation id、quote matching、groundedness 和 unsupported grounded claim 的校验器失败样例，Real LlamaIndex run 补强了真实框架 `VectorStoreIndex` / retriever source-node metadata 的窄观察；OpenAI docs 2026-07-12 复核补强 hosted File Search / vector store、included results、metadata filtering、query rewriting、ranking/chunking、batch ingestion、rate limits、pricing/ZDR/data residency、expiration 和成本边界；仍缺真实 embedding / vector store / File Search / LLM synthesis completed run、chunk size/top-k/rerank 对比、citation correctness、batch/rate-limit behavior 和成本/延迟实验。
- Memory / 知识库治理已补标准库写入守门模拟实验、生命周期权限审计和 Real LangGraph Memory Store Validation，窄结论“长期记忆不能默认自动写入或默认提升表现，必须配套写入守门、生命周期权限、跨用户隔离和 trace 脱敏”已可入正文；LangGraph `InMemoryStore` run 支撑 namespace、put/get/search/delete 和应用层历史包装的窄观察，并显示 broad prefix search 可跨 user namespace；仍缺真实多会话 Agent / memory framework 的收益、污染、权限、隐私、持久化和用户查看/编辑/删除 UI 实验。
- Evaluation / Observability 已补 AgentBench、WebArena、τ-bench、OpenAI Evals、Browser Use / Playwright、Anthropic Computer Use、标准库 trace-aware eval 模拟实验、Real Trace-Aware Eval scorer control、trace schema audit、grader misalignment / reward hacking audit、browser action trace audit、Real Browser Use package surface validation 和 Real Browser Playwright fixed-workflow completed run，窄结论“公开 benchmark 不能直接代表真实业务 Agent 质量”“工具/副作用 Agent 不能只看最终答案”“工具 Agent 评测需要关注用户交互、API tools、状态变化和多次试验一致性”“Browser / computer-use Agent 需要把网页动作、DOM/page/screenshot state、profile/auth、权限和 trace 纳入 eval / 审计”“trace 字段要按 debug/audit/regression/cost/RAG/privacy 用途设计”和“自动 grader 需要 edge cases、误判统计和人工校准”已可入正文；Real Trace-Aware Eval scorer control 已覆盖 final-only vs trace-aware 的本地规则差异，但仍不证明真实模型或平台 eval 效果；仍缺真实 Agent trace completed run、真实 Browser Use / computer-use Agent 对比实验、τ³-bench 小样本、真实 LLM-as-judge 误判分析、人工复核、平台字段映射和回归集工程案例。
- Production / Security 已补 Indirect Prompt Injection paper、OWASP LLM Top 10、OWASP Agentic AI Security resources、MITRE ATLAS、NIST 风险资料、Microsoft Prompt Shields 检测层资料、Google Responsible AI 生产治理资料、OpenAI Moderation、OpenAI Safety / Data Controls、OpenAI Production / Cost / Latency / Rate Limit 文档、OpenAI Batch / Flex / Prompt Caching 文档、LangGraph interrupt / persistence docs、标准库 prompt injection / tool permission 模拟实验、Real Agentic Security Regression Set 标准库 toy runtime、Production Safety / Data Governance Checklist 标准库实验、Production Cost / Latency / Rate-Limit 标准库 audit、Real Prompt Injection / Permission harness、Real Production Cost / Latency / Rate-Limit harness、Real Batch / Flex / Prompt Caching harness、Real LangGraph Interrupt Recovery harness 和 Real Moderation Safety harness，可支撑外部内容模糊数据/指令边界、user prompt / document attack 分类、agentic-specific 风险分类、attack-technique / case-study-derived regression set、prompt-only 风险、写工具阻断、安全测试/监控、trace 脱敏、HITL 与 sandbox/runtime containment 的不同边界、moderation signals、tool-calling moderation 覆盖限制、streaming moderation 限制、red-team、HITL、`safety_identifier`、API key revoke、abuse logs、application state、remote MCP third-party retention、hosted tool state、data residency、token/usage 记录、organization/project 级 rate limits、standard/project token rate-limit headers、retry、平均/P95 latency、预算阈值、reported output token 与可见输出差异、model/output controls、Batch status、Flex fallback、Prompt Caching read/write 和降级策略；Real LangGraph Interrupt Recovery 已完成 `MemorySaver` 最小 run 和 `SqliteSaver` 本地 SQLite 同进程 graph 重建恢复 case、双本地 Python 进程 prepare/resume case 和双本地 Python 进程并发 resume case，支撑批准、拒绝、参数 hash、重复恢复不重复执行、trace 脱敏和本地 SQLite 同进程/双进程恢复和并发 resume 的窄观察；Real Prompt Injection / Permission 已完成 no-key 本地 deterministic tool-permission control，支撑固定 tool calls 下的危险工具计数、prompt-only toy side effects、policy-enforced 写工具拒绝和 trace 脱敏逻辑，但真实模型 / API 行为仍未验证；Real Moderation Safety 已完成本地 deterministic policy-signal control，但真实 Moderation API 仍未验证；Real Production Cost / Latency / Rate-Limit 已完成本地 deterministic accounting control，但真实 API 成本/延迟/限流仍未验证；Real Batch / Flex / Prompt Caching 已完成本地 deterministic metadata control，但真实 API 行为仍未验证。仍缺真实模型 / 框架 guardrail / 检测层 / safety filter / 部署式 HITL approval 实验、真实 prompt injection / moderation completed run、agentic-specific regression cases 的真实试跑、跨框架权限对比、真实项目审计脱敏策略、真实 safety/data governance checklist 复核和真实成本/延迟/吞吐 completed run。
- Framework landscape 已补主要框架文档、框架能力交叉表和标准库框架选择 rubric smoke test，窄结论“框架应按任务难点和能力边界比较，不能写成某个框架默认最好”已可入正文；仍缺真实同一任务框架横向实验。
- Cookbook 的具体 recipe 已能支撑实践项目路线，Usage/Cost 和 Rate limits recipe 已能支撑项目 8 的 usage/cost/rate-limit/retry/fallback/batching 字段设计；SWE-agent 和 mini-SWE-agent 已能支撑 repo issue / coding agent 进阶练习的接口、轻量控制流、确认模式、trajectory、成本限制、CLI options、runtime/trajectory 和 sandbox 配置边界；Real mini-SWE-agent CLI Surface Validation 已完成安装 / CLI / 默认配置表面检查；Real mini-SWE-agent Runtime Surface Validation 已完成 deterministic fake-model toy repo run，支撑 `InteractiveAgent` / `LocalEnvironment` / pytest feedback / trajectory 的窄观察，并显示 configured env marker 会进入 trajectory；Real Repo Issue Agent Toy 已完成固定 workflow 和确定性 workflow-agent hybrid baseline，支撑 toy repo、failing tests、implementation-only diff、trajectory 对照组以及建议-审批-执行控制边界；Browser Use / Playwright / Anthropic Computer Use 已能支撑 Browser / Computer Use Agent 的动作层、trace、profile/auth、VM/container 和截图注入风险边界，Real Browser Use Package Surface Validation 已完成 package / source surface 检查，标准库 smoke harness 已支撑项目验收结构和 trace / 失败分类设计，readiness audit 已支撑 prerequisites / commands / references / failure examples / boundaries 的跟练卡片结构，窄结论“Cookbook 示例不是 API 规范或生产保证”已可入正文；仍需要真实本地试跑来确认依赖、真实 usage/cost、真实 rate-limit/retry/fallback 行为、成本、失败样例、真实模型驱动 hybrid、真实模型 mini-SWE-agent confirm-mode、SWE-agent toy repo 行为、Browser / computer-use Agent 同任务对比和初学者阻塞点。
- Claim ledger 规定只有状态为“可入正文”的结论，才能写成确定性表述；其他结论需要保守表达。

## 待验证问题

- prompt injection / tool permission 的最小攻击实验应该如何覆盖 guardrails、HITL approval、敏感 trace 和审计字段？Real Prompt Injection / Permission harness 已完成 no-key 本地 deterministic tool-permission control；真实模型 / API completed run 和 detector / HITL / guardrail 对照仍待做。
- 真实 MCP host UI 实验应如何覆盖 `tools/list`、`tools/call`、`resources/list`、`resources/read`、`prompts/get`、用户拒绝、roots、URL mode elicitation、sampling 和敏感日志脱敏？本地 SDK flow 已完成，真实 host 呈现仍待做。
- 真实 Anthropic MCP connector / tunnels 实验应如何覆盖 `mcp_tool_use` / `mcp_tool_result`、allowlist/denylist、OAuth token、data retention、third-party server trust review、allowed IPs、credential rotation 和 tunnel shared responsibility？
- 真实 Function Calling / Responses API 实验中，模型能否稳定根据 tool validation error 修正参数？namespace / `tool_search`、allowed tools、strict mode、custom tools / CFG 和 parallel tool-call 设置如何影响真实选择质量、token 成本、延迟和错误恢复？不同框架如何表示 tool execution error？Real Tool Calling harness 已完成 no-key 本地 deterministic validation/retry control；真实 API completed run 仍待做。Semantic Kernel native plugin 已补本地参数处理和应用层审批 wrapper 观察，但还没有真实模型 tool selection、OpenAPI/MCP plugin 或 HITL UI 结果。
- 真实 Agent/Workflow 对比实验中，固定 workflow、workflow-agent hybrid、ReAct tool loop、planner/executor 和 reflection retry 如何影响成功率、工具调用数、成本、延迟、失败原因、权限确认和 trace 可读性？
- Voyager-style embodied lifelong agent 是否能在真实模型、Voyager / Minecraft 或其他环境中稳定复用技能库？toy environment 已完成最小对照组；仍需验证环境依赖、成本、skill library 污染、停止条件、sandbox、跨环境迁移和 trace。
- 真实 RAG stack 中，chunk size、top-k、rerank/filter 和 LLM synthesis 如何影响 citation correctness、faithfulness、latency 和 token cost？
- 真实多会话 Agent / memory framework 中，guarded memory、auto memory 和 no memory 如何影响任务质量、错误写入、过时记忆使用、敏感信息进入上下文和用户纠错成本？
- 真实 Agent trace 中，规则评分、LLM-as-judge 和人工评审如何组合，才能发现过程错误并控制误判率？标准库 grader audit 已覆盖最小误判结构，真实 judge / 平台对照仍待做。
- 真实 Agent trace-aware eval 应如何覆盖 RAG、工具调用、权限确认、成本/延迟和人工反馈？
- 真实模型 / 框架 guardrail / moderation 下，prompt injection 防护如何测量误报、漏报、审批负担、延迟和敏感 trace 泄露？Real Moderation Safety harness 已完成 no-key 本地 deterministic policy-signal control；真实 Moderation API completed run、真实 guardrail / detector 对照和人工复核仍待做。
- agentic-specific regression set 如何从 MITRE ATLAS / OWASP resources 抽样覆盖 goal hijacking、tool misuse、tool poisoning、identity / privilege abuse、memory poisoning、MCP / remote tool abuse、computer-use destructive action、insecure inter-agent communication、cascading failures 和 rogue agent / runaway loop 停止条件？
- 真实 API / Cookbook 练习中，token/usage、organization/project 级 rate-limit headers、retry、平均/P95 latency、cost estimate、budget threshold、reported output token 与可见输出差异、Batch status、Flex fallback、cache read/write 和降级策略如何记录成可复用模板？标准库 production cost / latency / rate-limit audit 已完成字段模板，Real Production Cost / Latency / Rate-Limit harness 已补本地 accounting control，Batch/Flex/Caching harness 已补本地 metadata control；真实 API、真实 rate-limit headers、Batch/Flex/Prompt Caching 行为和质量取舍仍待验证。
- OpenAI API、remote MCP、hosted tools、files/vector stores、prompt caching 和 browser/computer-use 工具的数据保留边界如何落到项目 checklist？
- 是否需要为每个框架增加最小示例 source card？
- 真实框架横向实验应先选哪 2-3 个框架做最小实现，避免一次性引入过多依赖和 API 成本？
- SWE-agent / mini-SWE-agent 是否适合作为初学者 repo issue 进阶项目？固定 workflow baseline、确定性 workflow-agent hybrid baseline、mini-SWE-agent CLI surface validation 和 deterministic fake-model runtime surface validation 已完成；仍需验证真实模型驱动 hybrid、mini-SWE-agent confirm-mode repo issue run、sandbox、权限、回滚、测试反馈、trajectory 脱敏、成本上限和人工确认负担。
- Browser Use / browser agent 与固定 Playwright workflow 在同一 demo site 上的表现如何？应如何记录 action trace、DOM/page state、profile/auth、文件上传、表单提交、人工确认、成本、延迟和失败分类？标准库 browser action trace audit 已完成字段模板，Browser Use package surface、固定 Playwright demo run 和 deterministic coordinate-loop 已完成；Browser Use agent / 模型驱动 computer-use-style 对照仍待做。
- 是否需要补充面向初学者的视频课程或书籍？
- 哪些论文结论已经被现代框架吸收，哪些仍主要是研究方向？

## 本章小结

- 资料地图的目标是组织可信学习路径，不是堆链接。
- 论文、官方文档、框架文档、源码示例和治理指南各有用途。
- Source cards、coverage matrix 和 claim ledger 是控制正确性的核心机制。
- 当前台账中的窄口径概念、协议和工程边界多已可入正文；真实质量、成本、延迟、稳定性和框架优劣仍需保守表述。
- 后续扩展资料库时，应优先补当前矩阵中的缺口。

## References

### Indexes

- [Source Card 索引](../sources/source-card-index.md)
- [References 覆盖矩阵](../references/coverage-matrix.md)
- [Evidence Notes 索引](../evidence/README.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [待验证问题](../evidence/validation-backlog.md)
- [实验与复现](../experiments/README.md)

### Templates

- [资料卡片模板](../governance/templates/source-card.md)
- [Evidence Note 模板](../governance/templates/evidence-note.md)
