# OWASP Top 10 for Large Language Model Applications

- 来源链接：https://owasp.org/www-project-top-10-for-large-language-model-applications/
- 相关链接：https://genai.owasp.org/llm-top-10/；https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
- 作者 / 机构：OWASP
- 发布时间：持续更新项目；OWASP 项目页 last-modified 复核为 2025-12-29；GenAI LLM Top 10 archive 页面 last-modified 复核为 2026-07-10
- 最后复核日期：2026-07-12
- 类型：Security Guidance
- 主题：Security / Prompt Injection / LLM Application Risk
- 适合阶段：工程实践 / 生产化
- 可信度等级：A
- 是否已验证：OWASP 项目页和 GenAI LLM Top 10 2025 archive 页面已于 2026-07-12 复核；2025 risk archive 与 LLM01/02/05/06/08 条目页已抽样精读；“prompt 不是充分安全边界”“LLM output 也要当作不可信输入处理”“高风险工具/agent agency 需要最小权限和人工确认”窄结论已可入正文；安全 regression set 已完成；真实 guardrail / detector / HITL 效果仍部分验证

## 一句话总结

OWASP LLM Top 10 是构建 Agent 安全章节的基础安全 reference，适合解释 prompt injection、敏感信息泄露、LLM 输出处理、工具/插件访问控制、过度授权和 RAG/vector store 风险。

## 核心结论

- OWASP GenAI 站点当前提供 `LLM TOP 10 FOR 2025`；旧 OWASP 项目页仍保留 version 1.1 摘要，并把 latest Top 10 指向 `https://genai.owasp.org/llm-top-10/`。
- 2025 版 `LLM01: Prompt Injection` 说明 direct / indirect prompt injection，且明确 RAG 和 fine-tuning 不能完全缓解 prompt injection；缓解建议包括 least privilege、human approval for high-risk actions、segregate external content 和 penetration testing。
- 2025 版 `LLM02: Sensitive Information Disclosure` 支撑“不要把敏感信息直接塞进上下文，也不要依赖模型承诺不泄露”的风险提醒；页面建议 robust input validation、least privilege、tokenization/redaction 和用户教育。
- 2025 版 `LLM05: Improper Output Handling` 说明 LLM output 在进入下游组件前需要 validation、sanitization 和 context-aware output encoding；否则可能导致 XSS、CSRF、SSRF、privilege escalation、RCE、SQL injection 或 path traversal。
- 2025 版 `LLM06: Excessive Agency` 直接关联 Agent 工具和插件：应 minimize extensions、minimize extension functionality / permissions、avoid open-ended extensions、execute extensions in user's context、require user approval，并在 downstream systems 做 authorization。
- 2025 版 `LLM08: Vector and Embedding Weaknesses` 支撑 RAG/vector store 的 access control、multi-tenant leakage、embedding inversion、data poisoning、permission-aware vector stores、knowledge-source validation 和 retrieval audit 边界。
- OWASP 是风险分类和安全意识资料，不是某个 Agent 框架的完整安全实现方案。

## 支撑证据

- 2026-07-12 使用 `curl -L -I https://owasp.org/www-project-top-10-for-large-language-model-applications/` 复核 OWASP 项目页，返回 HTTP 200，`content-type: text/html; charset=utf-8`，`last-modified: Mon, 29 Dec 2025 17:43:20 GMT`。页面说明该项目已发展为 OWASP GenAI Security Project，并把 latest Top 10 for LLM 指向 `https://genai.owasp.org/llm-top-10/`；页面仍保留 version 1.1 的十项摘要。
- 2026-07-12 使用 `curl -L -I https://genai.owasp.org/llm-top-10/` 复核 GenAI LLM Top 10 archive，返回 HTTP 200，`content-type: text/html; charset=UTF-8`，`last-modified: Fri, 10 Jul 2026 02:19:21 GMT`。页面导航和标题显示 `LLM TOP 10 FOR 2025` / `2025 Top 10 Risk & Mitigations for LLMs and Gen AI Apps`。
- 2026-07-12 抓取 GenAI archive 成功；页面列出 2025 十项：`LLM01 Prompt Injection`、`LLM02 Sensitive Information Disclosure`、`LLM03 Supply Chain`、`LLM04 Data and Model Poisoning`、`LLM05 Improper Output Handling`、`LLM06 Excessive Agency`、`LLM07 System Prompt Leakage`、`LLM08 Vector and Embedding Weaknesses`、`LLM09 Misinformation`、`LLM10 Unbounded Consumption`。
- 2026-07-12 抓取 `LLM01:2025 Prompt Injection` 成功；页面包含 direct / indirect prompt injection、RAG / fine-tuning 不能完全缓解 prompt injection、least privilege、human approval、external content segregation、penetration testing 和 RAG document injection scenarios。
- 2026-07-12 抓取 `LLM02:2025 Sensitive Information Disclosure` 成功；页面包含 PII、financial、health、confidential business data、security credentials、legal documents、proprietary model information、input validation、least privilege、redaction 和 tokenization。
- 2026-07-12 抓取 `LLM05:2025 Improper Output Handling` 成功；页面包含 validation、sanitization、context-aware output encoding、parameterized queries、CSP、logging/monitoring，以及 XSS、CSRF、SSRF、privilege escalation、RCE、SQL injection、path traversal scenarios。
- 2026-07-12 抓取 `LLM06:2025 Excessive Agency` 成功；页面包含 function / extension / tools / skills / plugins terminology, minimize extensions/functionality/permissions, avoid open-ended extensions, execute in user's context, require user approval, downstream authorization, logging and rate limiting。
- 2026-07-12 抓取 `LLM08:2025 Vector and Embedding Weaknesses` 成功；页面包含 RAG / vector / embedding risk、unauthorized access、multi-tenant leakage、embedding inversion、data poisoning、permission-aware vector stores、source validation 和 immutable retrieval logs。

## 可能的问题

- OWASP 是安全风险分类，不是具体框架实现指南。
- 需要和实际工具权限、MCP 安全、部署审计资料结合。
- 当前 source card 精读了与 Agent / RAG / 生产安全最相关的 2025 条目，未逐段精读全部十项和完整 PDF。
- 旧 version 1.1 页面编号和 2025 archive 编号不同；正文引用时应优先写 2025 编号，避免把旧 `LLM07 Insecure Plugin Design` / `LLM08 Excessive Agency` 当作当前编号。

## 初学者阅读建议

- 不需要一次读完所有风险项。先关注 2025 版 `LLM01 Prompt Injection`、`LLM02 Sensitive Information Disclosure`、`LLM05 Improper Output Handling`、`LLM06 Excessive Agency` 和 `LLM08 Vector and Embedding Weaknesses`。

## 可复现实验

- 已完成标准库 prompt injection / permission 模拟实验，验证最小权限、写工具阻断和 trace 脱敏流程。
- 已完成标准库安全 regression set，覆盖外部文档注入、跨用户读取、高金额退款、敏感信息外泄、破坏性工具、重复提交和 benign case，并记录误报、漏报和 trace secret 泄漏。
- 已准备真实 Responses API prompt injection / permission harness：当前无 API key 时已完成本地 deterministic tool-permission control，覆盖固定 tool calls、危险写工具请求计数、prompt-only toy side effects、policy-enforced 写工具拒绝和 trace 脱敏，并标记未验证真实模型或真实 API；配置后可记录模型是否请求高风险写工具、prompt-only 模拟副作用、policy-enforced 模拟人工拒绝和 trace 脱敏结果。真实 API completed run 仍待跑，不能提前升级结论。

## 是否进入正文

- 结论：进入；窄边界可入正文
- 原因：可支撑生产安全章节的风险分类、prompt injection、敏感信息、LLM output validation、工具/插件访问控制、excessive agency 和 RAG/vector store 边界，并与标准库 prompt injection / permission 实验、安全 regression set 共同支撑“prompt 不是充分安全边界，外部内容、模型输出、检索内容和高风险工具必须由系统层权限/审批/审计控制”。具体缓解效果仍需真实模型 / 框架 guardrail / detector / HITL 验证。
