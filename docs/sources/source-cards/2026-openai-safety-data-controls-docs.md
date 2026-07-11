# OpenAI Safety Best Practices and Data Controls Documentation

- 来源链接：
  - https://developers.openai.com/api/docs/guides/safety-best-practices.md
  - https://developers.openai.com/api/docs/guides/your-data.md
- 作者 / 机构：OpenAI
- 发布时间：持续更新 documentation
- 最后复核日期：2026-07-11
- 类型：Official Docs / Safety / Data Governance
- 主题：Safety / Abuse Monitoring / Data Retention / Data Residency / API Key Compromise
- 适合阶段：工程实践 / 生产化前检查
- 可信度等级：A
- 是否已验证：两个官方 Markdown 页面均返回 HTTP 200；关键段落已精读；可支撑 moderation、red-teaming、HITL、用户举报、safety identifiers、API key revoke、abuse monitoring logs、application state、Zero Data Retention / Modified Abuse Monitoring、endpoint retention、data residency 和第三方工具数据边界；真实 moderation 效果、合规适配、数据驻留配置和误用检测效果仍部分验证

## 一句话总结

OpenAI Safety Best Practices 和 Data Controls 文档适合用来补齐 Agent 生产化的安全和数据治理边界：上线前不只要看 prompt injection，还要设计内容过滤、红队测试、人工复核、用户举报、滥用追踪、API key 处置、数据保留、应用状态和第三方工具数据流。

## 核心结论

- Safety best practices 建议使用 Moderation API 或自建内容过滤系统来降低 unsafe content 频率；这只能支撑“应有检测层”，不能证明过滤一定有效。
- 文档建议对应用做 adversarial testing / red-teaming，覆盖代表性输入和试图破坏系统的输入，包括 prompt injection。
- 文档建议在高风险场景、代码生成等场景使用 human-in-the-loop，并让人类能访问验证输出所需的原始资料。
- 文档建议约束用户输入、限制输出 tokens、使用 validated dropdown fields 或从后端 validated materials 返回内容，以缩小误用空间。
- 文档建议提供用户举报渠道，并由人类监控和响应。
- 文档建议理解并沟通模型限制，评估 API 在广泛输入上的表现，校准用户预期。
- 文档建议在用户交互型产品中发送 privacy-preserving `safety_identifier`，帮助滥用监控和问题追踪；标识符不会在 API 或 session 之间自动继承。
- 文档说明如果 API key 暴露、误用或疑似泄露，应及时 revoke 并替换。
- Data controls 文档说明 API 数据默认不用于训练或改进模型，除非显式 opt in。
- Data controls 文档区分 abuse monitoring logs 和 application state：abuse logs 默认可能包含 customer content、prompts/responses 和 classifier outputs，并默认保留至多 30 天；application state 是部分 API 功能为完成任务而持久化的数据。
- Zero Data Retention 和 Modified Abuse Monitoring 需要 OpenAI 预先批准，并不等于所有 endpoint / capability 都不存 application state；ZDR 下 `/v1/responses` 和 `/v1/chat/completions` 的 `store` 会被视为 `false`，但不符合 ZDR 条件的 endpoint / capability 仍可能保留 application state。
- Data controls 文档明确 remote MCP server 是第三方服务，发送给 MCP server 的数据受第三方数据保留政策影响；这补强“远程工具连接必须单独审查数据流”的边界。
- Data controls 文档说明 hosted shell / code interpreter / hosted skills 可能在容器活动期间写入临时 application state，容器过期或删除后清理。
- Data controls 文档说明 data residency 是 project configuration，且不适用于 system data；某些地区、endpoint、模型和特性有额外限制。

## 支撑证据

- `safety-best-practices.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 12:59:52 GMT`；`content-type: text/markdown; charset=utf-8`。
- `your-data.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:30:30 GMT`；`content-type: text/markdown; charset=utf-8`。
- Safety best practices 页面包含 Moderation API、adversarial testing、HITL、prompt engineering、KYC、constrained input/output、用户举报、limitations、`safety_identifier` 和 revoke compromised API keys。
- Data controls 页面包含 data not used for training by default、abuse monitoring logs、application state、Modified Abuse Monitoring、Zero Data Retention、organization/project data retention controls、endpoint retention matrix、remote MCP third-party retention、hosted container state、data residency controls 和 limitation sections。
- Help Center `https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety` 在当前 CLI 环境返回 HTTP 403 / Cloudflare challenge；未作为已精读来源。

## 可能的问题

- Safety best practices 可以支撑安全流程和检查项；Moderation API 的接口和覆盖边界已另建 source card。两者都不证明 Moderation API、red team、HITL 或 `safety_identifier` 在具体应用中足够有效。
- Data controls 文档涉及大量 endpoint、模型、地区和企业功能，变化风险高；正文应引用边界，不应复制完整表格或写死具体型号/地区支持。
- Zero Data Retention、Modified Abuse Monitoring、Eyes Off、Safety Retention、data residency 和 EKM 等能力通常需要审批、项目配置或企业条件；不能写成默认可用。
- 第三方工具、remote MCP server、web search、hosted containers 和 prompt caching 都可能有额外数据处理边界，需要按功能单独审查。

## 初学者阅读建议

- 先读 Safety best practices，把它当成生产安全 checklist：过滤、红队、人工复核、输入/输出约束、举报渠道、用户追踪和 API key 处置。
- 再读 Data controls，重点理解 abuse monitoring logs 与 application state 的区别，不要把“API 默认不训练”误解成“不保留任何数据”。
- 如果接入 remote MCP、web search、hosted shell/code interpreter、file/vector store 或 prompt caching，要单独查对应 endpoint / capability 的数据保留说明。

## 可复现实验

- 后续真实 prompt injection / permission harness 应加入 moderation / detector / HITL 对照，并记录 false positive、false negative、审批负担、trace 脱敏和 `safety_identifier` 是否进入日志。
- 后续真实 MCP / hosted tool 实验应记录哪些数据发给第三方 server、哪些数据进入 application state、哪些对象需要显式删除、是否有 project-level data retention 或 data residency 配置。
- 后续实践项目应加入 API key 泄露演练清单：检测、撤销、替换、审计影响范围和阻止旧 key 继续使用。

## 是否进入正文

- 结论：进入；安全和数据治理检查项的窄边界可入正文。
- 原因：官方文档直接支撑 moderation / red-team / HITL / safety identifier / API key revoke 和 data retention / application state / ZDR / MAM / remote MCP third-party retention / data residency 等工程边界。仍需保守写明：这些资料不证明具体检测层、防护层、合规配置或数据驻留方案在真实业务中充分有效。
