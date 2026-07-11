# Evidence Note: Prompt Injection 与权限边界

## 要验证的结论

Prompt injection 不能只靠 prompt 解决。对会调用工具、读取外部内容或执行写操作的 Agent，安全边界需要由权限控制、工具隔离、参数校验、人工确认、审计日志和安全回归测试共同承担。

## 资料来源

- Source 1：[OWASP Top 10 for Large Language Model Applications](../sources/source-cards/2026-owasp-llm-top-10.md)
- Source 2：[NIST AI Risk Management Framework](../sources/source-cards/2026-nist-ai-rmf.md)
- Source 3：[OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- Source 4：[Prompt Injection 与工具权限最小实验结果](../experiments/prompt-injection-permission/results-2026-07-11.md)
- Source 5：[安全 Regression Set 最小实验结果](../experiments/security-regression-set/results-2026-07-11.md)
- Source 6：[Indirect Prompt Injection paper](../sources/source-cards/2023-indirect-prompt-injection-paper.md)
- Source 7：[Microsoft Prompt Shields Documentation](../sources/source-cards/2026-microsoft-prompt-shields-docs.md)
- Source 8：[Anthropic Jailbreak and Prompt Injection Mitigation Documentation](../sources/source-cards/2026-anthropic-jailbreak-mitigation-docs.md)
- Source 9：[OWASP Agentic AI Security Resources](../sources/source-cards/2026-owasp-agentic-ai-security.md)
- Source 10：[MITRE ATLAS](../sources/source-cards/2026-mitre-atlas.md)
- Source 11：[Real Prompt Injection 与工具权限实验结果](../experiments/real-prompt-injection-permission/results-2026-07-11.md)
- Source 12：[AgentDojo paper](../sources/source-cards/2024-agentdojo-paper.md)
- Source 13：[Defeating Prompt Injections by Design](../sources/source-cards/2025-camel-prompt-injection-paper.md)

## 交叉验证结果

- 一致点：OWASP GenAI LLM Top 10 2025 archive 将 `LLM01: Prompt Injection` 列为 LLM / GenAI 应用风险项，并明确区分 direct / indirect prompt injection；页面还说明 RAG 和 fine-tuning 不能完全缓解 prompt injection，建议 least privilege、human approval for high-risk actions、segregate external content 和 penetration testing。
- 一致点：Indirect Prompt Injection paper 已于 2026-07-12 复核 arXiv HTTP、HTML metadata、API v2 metadata 和摘要；论文明确指出 LLM-integrated applications 会模糊 data 和 instructions 的边界，并展示攻击者可把恶意 prompt 注入到目标应用可能检索的数据中；这直接支撑“外部内容只能当作不可信数据”的章节表述。
- 一致点：Indirect Prompt Injection paper 的摘要把影响范围连接到 data theft、worming、information ecosystem contamination，以及控制应用功能和 API 调用方式；这与 OWASP 2025 的 prompt injection、improper output handling 和 excessive agency 风险方向一致。其 real-world examples 属于 2023 年前后系统案例，不能外推为当前产品表现或防护失效率。
- 一致点：OWASP 2025 `LLM05: Improper Output Handling` 强调 LLM output 在进入下游组件前需要 validation、sanitization 和 context-aware output encoding；这直接支持“模型输出不能直接进入工具、浏览器、数据库或代码执行路径”。
- 一致点：OWASP 2025 `LLM06: Excessive Agency` 强调最小化 extensions、functionality 和 permissions，避免 open-ended extensions，在用户上下文执行工具，并对高风险动作要求 user approval 和 downstream authorization；这支持高风险动作需要权限边界和人工确认。
- 一致点：OWASP 2025 `LLM08: Vector and Embedding Weaknesses` 把 RAG / vector store / embedding 的 unauthorized access、multi-tenant leakage、embedding inversion 和 data poisoning 纳入风险边界；这支持把检索内容和向量库也纳入 prompt injection / 权限 regression set。
- 一致点：OWASP Agentic Security Initiative 的公开资源把 agentic AI 风险扩展到 goal hijacking、tool misuse、identity / privilege abuse、memory poisoning、insecure inter-agent communication、cascading failures、trust exploitation 和 rogue agents；这说明 prompt injection 只是 Agentic AI 安全的一部分，安全 regression set 还应覆盖身份、权限、记忆、多 Agent 通信和级联失败。
- 一致点：OWASP Agentic AI crosswalk 摘要还把 agent identity、runtime containment、architectural monitoring、supply chain attestation 和 schema controls 列为 gap / priority areas；这与本手册对最小权限、运行时隔离、trace、schema 校验和工具边界的工程建议一致。
- 一致点：MITRE ATLAS latest v6 YAML 将 `LLM Prompt Injection`、`AI Agent Tool Invocation`、`AI Agent Tool Poisoning` 和 memory / computer-use / MCP 相关 case studies 放入可版本化的 technique / case-study 数据集中，并用 `Agentic AI` platform 与 `Feasible` / `Demonstrated` / `Realized` maturity 标注攻击技术成熟度；这补强了“安全 regression set 应从真实攻击技术和案例抽样”的边界。
- 一致点：AgentDojo paper 已于 2026-07-12 复核 arXiv v3 metadata、PDF、GitHub repo metadata、README、项目站点和 results 页面；它把工具型 Agent 安全评测设定为 dynamic multi-tool calling in stateful adversarial environments，工具返回的非可信数据可以作为 indirect prompt injection 载体，utility 和 security checks 基于环境状态而不是只看最终回答。
- 一致点：AgentDojo 主文报告 4 个 suite、70 tools、97 user tasks、27 injection targets 和 629 security test cases；这补强了“安全 regression set 应同时记录用户目标、攻击者目标、注入端点、可用工具、环境状态、utility pass/fail 和 security pass/fail”的评测设计边界。
- 边界：AgentDojo 的 defense 结果只能写成论文 suite / setting 下的观察。论文讨论 detector false positives、重复用户 prompt 难以抵抗 adaptive attacks、tool filtering 有失效条件；这支持“检测和工具过滤不能写成充分防护”，但不证明任意 guardrail、detector、HITL、sandbox 或 tool filtering 在生产中有效。
- 一致点：CaMeL / Defeating Prompt Injections by Design 已于 2026-07-12 复核 arXiv v2 metadata、GitHub repo metadata、README 和关键源码入口；摘要明确提出在 LLM 外围创建 protective system layer，从 trusted query 抽取 control / data flows，使后续检索到的 untrusted data 不能影响 program flow，并用 capability 和 security policies 限制 private data 的 unauthorized data flows。
- 一致点：CaMeL 源码入口使用 AgentDojo suites，并区分 original、AgentDojo defense、`+camel`、`+camel+secpol` 和 replay-with-policies 等运行路径；这补强了“prompt injection 防护应把可信控制流、非可信数据流、工具能力和安全策略拆开建模，并用 utility/security eval 评估 tradeoff”的架构边界。
- 边界：CaMeL 的论文数字只能写成 AgentDojo / paper setting 下的结果；GitHub README 明确代码是 research artifact，interpreter 可能有 bug、实现可能不 fully secure，不是 Google product 且不计划支持或维护。因此它不能证明 capability-based 防护在生产中默认安全或默认优于检测层 / HITL / sandbox。
- 一致点：NIST AI RMF 把可信性考虑放进 design、development、use 和 evaluation 全生命周期；这支持把 prompt injection 防护放进系统设计和评测，而不是只放在提示词里。
- 一致点：OpenAI Function Calling docs 已在 tool-use evidence note 中确认工具执行发生在应用侧；这意味着应用侧有责任做参数校验、权限检查和审计。
- 一致点：Microsoft Prompt Shields 文档已于 2026-07-12 复核；它把输入攻击分成 User Prompt attacks 和 Document attacks，并把 document attacks 定义为外部 documents / emails 等第三方内容中嵌入隐藏指令以获得 LLM session 的未授权控制。这与 Indirect Prompt Injection paper 和 OWASP 对外部内容风险的描述一致。
- 一致点：Microsoft Prompt Shields quickstart 已于 2026-07-12 复核；它展示了生成前检测接口 `shieldPrompt`，请求体包含 `userPrompt` 和 `documents`，响应字段包含 `userPromptAnalysis.attackDetected` 和 `documentsAnalysis[].attackDetected`。这支持“prompt injection 防护应进入系统层 workflow / guardrail / review 决策，而不是只写在提示词里”的工程表述。
- 边界：Microsoft 文档明确提示 Prompt Shields may not catch all attack vectors or may flag legitimate prompts，并建议 additional validation layers。这与本手册的保守边界一致：检测层有用，但不能替代权限隔离、人工确认、审计和 regression set。
- 一致点：Anthropic mitigation 文档已于 2026-07-12 复核；它也区分 direct prompt injection / jailbreaks 与 indirect prompt injection，并把网页、邮件、文档、OCR 输出和 tool results 等第三方内容作为间接攻击载体；这与论文和 Microsoft 的 document attack 分类方向一致。
- 一致点：Anthropic 文档建议把第三方内容放在 `tool_result` blocks 中、明确来源和可信度、在 system prompt 中声明工具/文档/搜索结果是不可信数据，并在可能时 JSON-encode untrusted content。这补强了“外部内容是数据，不是系统指令”的工程表达。
- 一致点：Anthropic 文档建议限制 Claude 访问敏感数据和动作、用 sandboxed environments 运行工具、筛查 raw tool output、red-team agent 并持续监控 successful injection 迹象。这与本手册对最小权限、写工具审批、审计 trace、regression set 和真实实验的要求一致。
- 边界：Anthropic 文档是供应商官方工程指南，不能证明 Claude Haiku 4.5 lightweight screens、structured output classifier、JSON encoding、computer-use screenshot classifiers、mid-conversation system message 或 system prompt policy 的真实拦截率；这些仍需真实攻击样例和误报/漏报实验。
- 边界：OWASP Agentic AI Security Resources 当前只复核了公开资源页、WP JSON 摘要和附件 metadata，`Agentic AI - Threats and Mitigations` 下载端点返回 no-access，media API 只公开封面 PNG；因此它只能支撑风险分类和治理 gap 的保守表述，不能支撑完整缓解清单或具体控制效果。
- 边界：MITRE ATLAS 是威胁知识库和 YAML 数据集，mitigation 条目只能作为 checklist 候选；它不能证明任何 guardrail、detector、sandbox、HITL 或监控方案在真实系统中有效。
- 分歧点：OWASP 和 NIST 是风险/治理资料，不是 Agent 框架实现文档；它们不能单独证明某个具体隔离方案有效。
- 可能原因：安全分类和风险管理框架关注“应该控制什么风险”，而工程文档和实验才验证“具体怎么控制”。
- 本地实验：标准库 prompt injection / tool permission 模拟中，`prompt_only` 模式执行了注入诱导的 `issue_refund` 并把假 secret 写入 trace；`policy_enforced` 模式只允许只读工具，拒绝写工具，并对敏感字段脱敏。这支持“prompt 不足以作为工具安全边界”的工程表述。
- 本地实验：标准库安全 regression set 中，`prompt_only` 只有 benign read case 通过，另外 6 个应阻断或审批的 case 全部漏报；`policy_enforced` 在外部注入、跨用户读取、高金额退款、敏感信息外泄、破坏性工具、重复提交和 benign case 上 7/7 通过，且没有假 secret 进入 trace。这支持“安全 regression set 需要覆盖多类失败模式并统计误报/漏报”的工程表述。
- 本地实验：标准库 agentic security regression set 把 MITRE ATLAS / OWASP 线索扩展为 9 个 case，覆盖 prompt injection tool write、越权 tool invocation、tool poisoning、memory poisoning、MCP / remote tool 外传、computer-use destructive action、runaway loop、inter-agent message 和 benign read；`prompt_only` 只通过 benign case，`sandboxed_runtime` 通过 9/9。该结果支持 agentic-specific case matrix 和字段设计，不证明真实防护效果。

## 实验验证

- 是否需要实验：是
- 实验设计：构建一个最小工具型 Agent，工具包含只读查询和写操作；输入外部文档中嵌入恶意指令，要求 Agent 越权读取或执行写操作。分别测试仅提示词防护、工具权限分离、参数校验、人工确认和审计日志的效果。后续从 MITRE ATLAS 和 OWASP Agentic AI resources 抽样扩展 agentic-specific cases：goal hijacking、tool misuse、tool poisoning、identity / privilege abuse、memory poisoning、MCP / remote tool abuse、computer-use destructive action、insecure inter-agent communication、cascading failures 和 rogue agent / runaway loop 停止条件。
- 结果：已完成标准库最小实验、安全 regression set 和 agentic security regression set。`prompt_only` 产生退款副作用并在 trace 中泄露假 secret；扩展 regression set 中 `prompt_only` 对 6 个风险 case 产生漏报；agentic security regression set 中 `prompt_only` 只通过 benign case，`policy_enforced_hitl` 仍未阻断 computer-use destructive action，`sandboxed_runtime` 通过 9/9。AgentDojo 补强了后续真实安全 benchmark 应记录 stateful environment、utility/security checks、injection endpoints 和 adaptive attack 边界；CaMeL 补强了后续实验应记录 control/data flow、capability policy、unauthorized data-flow blocking 和 utility/security tradeoff。Real Prompt Injection / Permission harness 已准备真实模型观测入口；当前无 API key 时完成本地 deterministic tool-permission control，覆盖 3 个固定 tool calls、2 个危险写工具请求、`prompt_only` 2 个 toy side effects、`policy_enforced` 0 个 side effects 和 trace 脱敏，并标记 `real_model_validated=false` / `real_api_validated=false`。实验未覆盖真实模型、真实框架 guardrails、HITL approval、AgentDojo / CaMeL benchmark 试跑、sandbox/runtime containment、成本或延迟。

## 结论状态

- 可入正文：窄结论“Prompt injection 不能只靠 prompt 解决；对会读取外部内容或调用工具的 Agent，外部内容、检索内容和模型输出应被当作不可信数据，工具权限、参数校验、写操作审批、审计和安全 regression set 必须由应用/系统层承担”已完成第一轮交叉验证。Indirect Prompt Injection paper 2026-07-12 复核支撑外部检索数据中的恶意 prompt 可影响应用和 API 调用的风险边界，但不证明当前产品拦截率或某个防护方案效果；AgentDojo 2026-07-12 复核补强 stateful tool-agent security eval、非可信工具结果、utility/security 双指标、injection endpoints 和 adaptive attack 边界；CaMeL 2026-07-12 复核补强 trusted control/data flow extraction、untrusted data 不能影响 program flow、capability-based security policy 和 AgentDojo replay/eval 的架构边界；OWASP GenAI LLM Top 10 2025 archive 直接支撑 `LLM01 Prompt Injection`、`LLM05 Improper Output Handling`、`LLM06 Excessive Agency` 和 `LLM08 Vector and Embedding Weaknesses` 的风险边界；OWASP Agentic AI resources 补强 goal hijacking、tool misuse、identity / privilege abuse、memory poisoning、insecure inter-agent communication、cascading failures、rogue agents、runtime containment 和 schema controls 等 agentic-specific 风险边界；MITRE ATLAS 补强可版本化 attack techniques、maturity 和 case-study-derived regression set 设计；NIST 支撑全生命周期风险治理；Microsoft Prompt Shields 支撑 user prompt / document attack 分类、检测层接口和误报/漏报边界；Anthropic mitigation docs 支撑 direct / indirect threat model、untrusted tool result handling、tool output screening、least privilege、red-team 和 monitoring 的工程边界；OpenAI 工具调用文档支撑应用侧控制边界；标准库实验支撑权限分离、写工具阻断、trace 脱敏、安全 regression set 字段设计和 agentic-specific case matrix。
- 部分验证：真实模型 / 框架 guardrail / HITL approval 的拦截率、误报/漏报、成本、延迟和跨框架覆盖范围仍待实际运行验证；当前真实 API harness 的 no-key 分支只验证本地 policy review、危险工具计数、toy side-effect blocking 和 trace 脱敏逻辑。

## 可进入章节

- 是。可以确定写成：prompt 有帮助，但不是充分安全边界。生产化 Agent 需要把外部内容当作不可信数据，并通过权限、隔离、校验、确认、审计和测试共同降低风险。仍需保守写明：具体 guardrail / HITL / 框架方案的真实拦截效果必须实测。
