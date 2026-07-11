# OWASP Top 10 for Large Language Model Applications

- 来源链接：https://owasp.org/www-project-top-10-for-large-language-model-applications/
- 作者 / 机构：OWASP
- 发布时间：持续更新项目；页面 last-modified 复核为 2025-12-29
- 最后复核日期：2026-07-11
- 类型：Security Guidance
- 主题：Security / Prompt Injection / LLM Application Risk
- 适合阶段：工程实践 / 生产化
- 可信度等级：A
- 是否已验证：来源链接已复核；关键风险项已精读；“prompt 不是充分安全边界”窄结论已可入正文；安全 regression set 已完成；真实 guardrail 效果仍部分验证

## 一句话总结

OWASP LLM Top 10 是构建 Agent 安全章节的基础安全 reference，适合解释 prompt injection、敏感信息泄露、工具/插件访问控制和过度授权等风险。

## 核心结论

- OWASP 将 `LLM01: Prompt Injection` 列为 LLM 应用风险项，并说明 crafted inputs 可能导致 unauthorized access、data breaches 和 compromised decision-making。
- `LLM06: Sensitive Information Disclosure` 支撑正文中“不要把敏感信息直接塞进上下文，也不要依赖模型承诺不泄露”的风险提醒。
- `LLM07: Insecure Plugin Design` 直接关联 Agent 工具和插件：处理不可信输入且访问控制不足，可能带来严重 exploit 风险。
- `LLM08: Excessive Agency` 支撑“不要给 Agent unchecked autonomy；高风险动作需要权限边界、人工确认和审计”的生产化建议。
- OWASP 是风险分类和安全意识资料，不是某个 Agent 框架的完整安全实现方案。

## 支撑证据

- OWASP 项目页面返回 HTTP 200；HTTP `last-modified` 为 2025-12-29。
- 页面列出 `LLM01: Prompt Injection`，并写明：“Manipulating LLMs via crafted inputs can lead to unauthorized access, data breaches, and compromised decision-making.”
- 页面列出 `LLM06: Sensitive Information Disclosure`，并写明敏感信息泄露可能导致 legal consequences 或 loss of competitive advantage。
- 页面列出 `LLM07: Insecure Plugin Design`，并写明处理 untrusted inputs 且 insufficient access control 的插件可能导致 remote code execution 等严重 exploit。
- 页面列出 `LLM08: Excessive Agency`，并写明 unchecked autonomy to take action 可能 jeopardize reliability, privacy, and trust。

## 可能的问题

- OWASP 是安全风险分类，不是具体框架实现指南。
- 需要和实际工具权限、MCP 安全、部署审计资料结合。
- 当前 source card 只精读了与 Agent 生产安全最相关的风险项，没有覆盖全部 Top 10 条目。

## 初学者阅读建议

- 不需要一次读完所有风险项。先关注 prompt injection、sensitive information disclosure、excessive agency 和 insecure plugin/tool design 相关内容。

## 可复现实验

- 已完成标准库 prompt injection / permission 模拟实验，验证最小权限、写工具阻断和 trace 脱敏流程。
- 已完成标准库安全 regression set，覆盖外部文档注入、跨用户读取、高金额退款、敏感信息外泄、破坏性工具、重复提交和 benign case，并记录误报、漏报和 trace secret 泄漏。
- 已准备真实 Responses API prompt injection / permission harness：无 API key 时跳过，配置后可记录模型是否请求高风险写工具、prompt-only 模拟副作用、policy-enforced 模拟人工拒绝和 trace 脱敏结果；结果待跑，不能提前升级结论。

## 是否进入正文

- 结论：进入；窄边界可入正文
- 原因：可支撑生产安全章节的风险分类、prompt injection、插件/工具访问控制和 excessive agency 边界，并与标准库 prompt injection / permission 实验、安全 regression set 共同支撑“prompt 不是充分安全边界，外部内容和高风险工具必须由系统层权限/审批/审计控制”。具体缓解效果仍需真实模型 / 框架 guardrail 和 HITL 验证。
