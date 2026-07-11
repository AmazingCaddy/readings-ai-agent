# Evidence Note: Prompt Injection 与权限边界

## 要验证的结论

Prompt injection 不能只靠 prompt 解决。对会调用工具、读取外部内容或执行写操作的 Agent，安全边界需要由权限控制、工具隔离、参数校验、人工确认、审计日志和安全回归测试共同承担。

## 资料来源

- Source 1：[OWASP Top 10 for Large Language Model Applications](../sources/source-cards/2026-owasp-llm-top-10.md)
- Source 2：[NIST AI Risk Management Framework](../sources/source-cards/2026-nist-ai-rmf.md)
- Source 3：[OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)

## 交叉验证结果

- 一致点：OWASP 将 prompt injection 列为 LLM 应用风险项，并明确 crafted inputs 可能导致 unauthorized access、data breaches 和 compromised decision-making。
- 一致点：OWASP 的 insecure plugin design 风险强调 untrusted inputs 和 insufficient access control 的组合风险；这直接支持“工具/插件权限不能只交给 prompt 控制”。
- 一致点：OWASP 的 excessive agency 风险强调 unchecked autonomy to take action 会影响 reliability、privacy 和 trust；这支持高风险动作需要权限边界和人工确认。
- 一致点：NIST AI RMF 把可信性考虑放进 design、development、use 和 evaluation 全生命周期；这支持把 prompt injection 防护放进系统设计和评测，而不是只放在提示词里。
- 一致点：OpenAI Function Calling docs 已在 tool-use evidence note 中确认工具执行发生在应用侧；这意味着应用侧有责任做参数校验、权限检查和审计。
- 分歧点：OWASP 和 NIST 是风险/治理资料，不是 Agent 框架实现文档；它们不能单独证明某个具体隔离方案有效。
- 可能原因：安全分类和风险管理框架关注“应该控制什么风险”，而工程文档和实验才验证“具体怎么控制”。

## 实验验证

- 是否需要实验：是
- 实验设计：构建一个最小工具型 Agent，工具包含只读查询和写操作；输入外部文档中嵌入恶意指令，要求 Agent 越权读取或执行写操作。分别测试仅提示词防护、工具权限分离、参数校验、人工确认和审计日志的效果。
- 结果：待执行

## 结论状态

- 部分验证：OWASP 直接支撑 prompt injection、工具/插件访问控制和 excessive agency 风险；NIST 支撑全生命周期风险治理；OpenAI 工具调用文档支撑应用侧控制边界。仍缺最小实验和具体框架安全文档。

## 可进入章节

- 是，但应保守表达：prompt 有帮助，但不是充分安全边界。生产化 Agent 需要把外部内容当作不可信数据，并通过权限、隔离、校验、确认、审计和测试共同降低风险。
