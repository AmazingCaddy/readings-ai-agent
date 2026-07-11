# Microsoft Prompt Shields Documentation

- 来源链接：https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection
- 相关链接：https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-jailbreak
- 作者 / 机构：Microsoft Learn / Azure AI Content Safety
- 发布时间：concept page `ms.date` 2025-11-21；quickstart `ms.date` 2026-01-30
- 最后复核日期：2026-07-12
- 类型：Official Docs / Security Engineering
- 主题：Prompt Injection / Prompt Shields / Content Safety / Guardrails
- 适合阶段：进阶 / Production 安全
- 可信度等级：A
- 是否已验证：Microsoft Learn concept page 和 quickstart 于 2026-07-12 复核仍为 HTTP 200；页面元数据、Prompt Shields concept page 和 quickstart 关键段落已复核；支撑 user prompt attack、document attack、`shieldPrompt` API、`attackDetected` 返回字段和 false positive / false negative 边界；不证明真实攻击拦截率、误报率、漏报率、跨模型效果或生产安全充分性

## 一句话总结

Microsoft Prompt Shields 文档适合说明 prompt injection 可以被放进系统层检测和工作流控制中：系统可以在生成前分析 user prompt 和 documents，并返回 attack flag；但这种检测不是充分安全边界，仍需要权限、审批、审计和回归测试。

## 核心结论

- Prompt Shields 是 Azure AI Content Safety 中的统一 API，用于检测和阻断针对 LLM 的 adversarial user input attacks，并在生成内容之前分析 prompts 和 documents。
- 文档把输入攻击分成两类：User Prompt attacks 和 Document attacks。
- User Prompt attacks 指用户主动利用系统弱点诱导 LLM 产生未授权行为，例如改变系统规则、伪造对话上下文、替换系统 persona 或要求编码输出。
- Document attacks 指攻击者把隐藏指令嵌入外部文档、邮件等第三方内容中，以试图获得 LLM session 的未授权控制。
- Document attack 示例包括在 grounding document 中嵌入发布博客、数据外泄、删除数据、阻断系统能力、欺诈、代码执行或感染其他系统等恶意指令。
- Quickstart 展示了 `contentsafety/text:shieldPrompt?api-version=2024-09-01` API，请求体包含 `userPrompt` 和 `documents`，响应包含 `userPromptAnalysis.attackDetected` 和 `documentsAnalysis[].attackDetected`。
- Quickstart 明确说明 `attackDetected=true` 表示检测到威胁，建议 review and action。
- Concept page 的 troubleshooting 明确提示 false positives / negatives：Prompt Shields may not catch all attack vectors or may flag legitimate prompts，并建议实现 additional validation layers。
- 对本手册而言，稳妥结论是：prompt injection 防护可以引入专门检测层，但仍不能把检测服务、guardrail 或 prompt 本身当成充分安全边界。

## 支撑证据

- 2026-07-12 使用 `curl -L -I` 复核 concept page，返回 HTTP 200；`last-modified: Fri, 05 Jun 2026 22:13:21 GMT`；页面标题为 `Prompt Shields in Azure AI Content Safety - Azure AI services`。
- Concept page 元数据包含 `ms.date=2025-11-21T00:00:00Z`、`updated_at=2026-06-05T22:11:00Z`，并提供 canonical URL。
- Concept page 描述写明：Learn about User Prompt injection attacks and document attacks and how to prevent them with the Prompt Shields feature。
- Concept page 正文写明 Prompt Shields detects and blocks adversarial user input attacks on LLMs，并在 content generated 之前分析 prompts and documents。
- Concept page 的 `Types of input attacks` 表格列出 User Prompt attacks 和 Document attacks，分别对应 user prompts 与 third-party content such as documents/emails。
- Concept page 的 User Prompt attacks 段落说明该能力此前称为 Jailbreak risk detection，并针对用户故意利用系统漏洞诱导 LLM 未授权行为。
- Concept page 的 Document attacks 段落说明外部 documents 中可嵌入 hidden instructions，以获取 LLM session 的 unauthorized control。
- Concept page troubleshooting 写明 Prompt Shields may not catch all attack vectors or may flag legitimate prompts，并建议 additional validation layers。
- 2026-07-12 使用 `curl -L -I` 复核 quickstart，返回 HTTP 200；`last-modified: Fri, 05 Jun 2026 22:11:00 GMT`；页面标题为 `Quickstart: Detect prompt attacks with Prompt Shields - Azure AI services`。
- Quickstart 元数据包含 `ms.date=2026-01-30T00:00:00Z`、`updated_at=2026-06-05T22:11:00Z`。
- Quickstart 展示 `shieldPrompt` REST 调用和 expected response，其中 `userPromptAnalysis.attackDetected=true`，`documentsAnalysis[].attackDetected` 表示 prompt 或 document attack 检测结果。

## 可能的问题

- Microsoft Learn 是官方产品文档，适合支撑功能存在、攻击分类和 API shape；不能作为独立安全评测。
- `attackDetected` 是检测服务的输出字段，不等于攻击一定被完整阻断，也不等于系统已经安全。
- false positives / negatives 已由文档明确提示；生产系统仍需要额外 validation layers、权限隔离、人工确认、审计、trace 脱敏和安全 regression set。
- 文档没有给出本手册可复用的真实拦截率、成本、延迟、跨模型表现或 adversarial benchmark 结果。

## 初学者阅读建议

- 先读本手册第 09 章，理解为什么外部内容只能当作不可信数据。
- 再读 Prompt Shields concept page 的 Types of input attacks、User Prompt attacks、Document attacks 和 troubleshooting 小节。
- Quickstart 只用来理解检测接口和响应字段；不要把它当成“接入后就安全”的证明。

## 可复现实验

- 把本手册现有 Real Prompt Injection / Permission harness 接入 Prompt Shields 或同类检测层，对比 prompt-only、detector-only 和 policy-enforced 三种模式。
- 记录 user prompt attack、document attack、benign request、高风险写工具、敏感字段和 destructive tool cases 的 allow/block/review 决策。
- 统计 false positive、false negative、审批负担、延迟、成本和 trace 中是否泄露敏感字段。

## 是否进入正文

- 结论：部分进入
- 原因：可作为第 09 章中“prompt injection 防护需要系统层检测、权限、审批、审计和 regression set”的官方工程资料；不能支撑“Prompt Shields 或任意 guardrail 能完全防住 prompt injection”这类结论。
