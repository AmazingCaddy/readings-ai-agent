# Anthropic Jailbreak and Prompt Injection Mitigation Documentation

- 来源链接：https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks.md
- 页面链接：https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks
- 作者 / 机构：Anthropic
- 发布时间：文档持续更新；页面未给出稳定发布日期
- 最后复核日期：2026-07-12
- 类型：Official Docs / Security Engineering
- 主题：Jailbreaks / Prompt Injection / Guardrails / Tool Result Security
- 适合阶段：进阶 / Production 安全
- 可信度等级：A
- 是否已验证：官方 Markdown 和 HTML 页面于 2026-07-12 复核仍为 HTTP 200，标题、摘要和关键正文段落已复核；支撑直接 jailbreak / direct prompt injection 与 indirect prompt injection 的威胁模型区分、input screening、system prompt policy、untrusted tool content、JSON encoding、least privilege、tool output screening、red-team 和 continuous monitoring 的工程边界；不证明任何模型、classifier、prompt、guardrail 或产品配置的真实拦截率、误报率、漏报率、成本、延迟或生产安全充分性

## 一句话总结

Anthropic 这页文档适合补强 prompt injection 防护的工程做法：直接攻击和间接攻击要分开建模，第三方内容和工具结果要当作不可信数据处理，并把筛查、权限、确认、red-team 和监控放进系统流程；但这些建议不能替代真实攻击样例和误报/漏报实验。

## 核心结论

- 文档把攻击分成两类：jailbreaks / direct prompt injection 与 indirect prompt injection。前者把应用用户当作 adversary；后者把网页、邮件、文档、tool results 等第三方内容当作潜在攻击载体。
- 对直接攻击，文档建议使用 harmlessness screens、input validation、强调边界和拒绝策略的 system prompts，并对 repeat offenders 做响应、限流或封禁。
- 对间接攻击，文档建议把第三方内容放在 `tool_result` blocks 中，而不是放进 system prompt 或普通 user text；同时明确说明内容来源和可信度。
- 文档建议在 system prompt 中声明：tools、documents、search results 返回的内容是不可信数据，不能覆盖 system prompt 或用户原始请求。
- 文档建议在可能时用 JSON object 包装第三方字符串，让不可信 payload 和周围结构有明确分隔。
- 文档提醒不要把开发者自己的指令放进 tool results，因为 Claude 会把 tool-result content 当作 untrusted data。
- 文档建议使用最小权限：不要给 Claude 访问不必要的 secrets，用 sandboxed environments 运行工具，并尽量缩小权限范围。
- 文档建议在 Claude 处理 tool output 前先筛查 tool raw output；如果疑似 injection，则返回 error 或 stripped summary，而不是 raw content。
- 文档建议 red-team 自己的 agent，用包含 injection attempts 的 documents、emails 和 tool outputs 测试 workflow，并检查 screening 和 confirmation steps。
- 文档还建议持续监控输出中的 successful injection 迹象，并迭代 prompts、validation 和 filtering strategies。

## 支撑证据

- 2026-07-12 使用 `curl -L -I` 复核官方 Markdown URL，返回 HTTP 200，`content-type: text/markdown; charset=utf-8`，`cache-control: private, no-store`；HTML 页面也返回 HTTP 200。随后使用 `curl -L` 抓取 Markdown 正文，页面标题为 `Mitigate jailbreaks and prompt injections`。
- 页面摘要写明：Defend your application against jailbreaks and prompt injection with input screening, hardened system prompts, and safe handling of untrusted tool content。
- 正文说明 jailbreaks and prompt injection are attempts to make Claude ignore its guidelines or your instructions，并把 attacks 分为 direct 与 indirect 两类。
- Direct threat model 段落列出 harmlessness screens、input validation、prompt engineering 和 respond to repeat offenders；harmlessness screen 示例使用 Claude Haiku 4.5 和 structured outputs。
- Indirect threat model 段落说明 Claude 可能代表用户处理 inbound email、fetched web page、OCR output、uploaded file 或 tool call result；攻击者可在这些内容里嵌入 redirect Claude 的指令。
- Indirect mitigation 列表包含 put untrusted content only in tool results、tell Claude what the content is and where it came from、state the policy in your system prompt、JSON-encode untrusted content、do not put your own instructions in tool results、limit Claude's access to sensitive data and actions、screen tool outputs before Claude acts on them、red-team your own agent；文档还提示 Claude Opus 4.8+ 可使用 mid-conversation system message 承载开发者指令。
- Tool output screening 示例要求 classifier 判断 tool output 是否包含 redirect assistant、override system prompt 或 make it take actions the user did not request 的指令，并使用 structured outputs 返回 `injection_suspected`。
- Continuous monitoring 段落建议定期分析 outputs 中的 successful injection 迹象，并据此改进 prompts、validation 和 filtering strategies。
- Computer use note 说明 Anthropic 对 computer use screenshots 运行 additional classifiers 并引导 Claude 在行动前请求用户确认；该信息适合放入待验证实验，不应写成通用 browser/computer-use 安全保证。

## 可能的问题

- 这是供应商官方工程文档，不是独立安全评测；不能证明任何 guardrail、classifier、prompt 或 model 默认能防住 jailbreak / prompt injection。
- 文档建议使用 Claude Haiku 4.5 做 lightweight screening，但本手册未实测该 classifier 的误报、漏报、成本或延迟。
- 文档中的 `tool_result`、mid-conversation system message 和 computer-use classifier 是 Anthropic 产品语境下的实现细节；跨供应商正文应抽取通用边界，不应把字段名泛化到所有 API。
- JSON encoding、system prompt policy 和 screening 都是降低风险的工程层，不能替代最小权限、写工具审批、审计 trace、回归测试和真实 red-team。

## 初学者阅读建议

- 先读本手册第 09 章，理解 prompt injection 为什么不是“提示词写好一点”就能解决。
- 重点读开头的两个 threat model：直接攻击是用户主动攻击；间接攻击是网页、邮件、文档、工具结果里藏了指令。
- 再读 indirect prompt injection 的列表，尤其是 untrusted content、tool results、least privilege、tool output screening 和 red-team。
- 对初学者最重要的 takeaway 是：外部内容只是数据，不是命令；工具权限和写操作必须由系统流程控制。

## 可复现实验

- 扩展本手册 Real Prompt Injection / Permission harness，加入 raw tool output screening、JSON-encoded tool result、policy-enforced tool result 和 HITL confirmation 对照。
- 设计直接 jailbreak、外部网页注入、邮件正文注入、OCR 文本注入、tool result 注入和 benign request case，记录 false positive、false negative、成本、延迟、审批负担和 trace 脱敏。
- 对 browser/computer-use 练习加入 screenshot / DOM / tool output injection case，检查系统是否要求用户确认以及是否限制写操作。

## 是否进入正文

- 结论：部分进入
- 原因：可作为第 09/12 章中“prompt injection 防护需要区分直接/间接威胁、把工具结果和第三方内容当作不可信数据、结合筛查/权限/确认/red-team/监控”的官方工程资料；不能支撑“Anthropic guardrails、classifier、prompt 或 computer-use 机制能可靠防住攻击”这类效果结论。
