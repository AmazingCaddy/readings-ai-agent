# Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection

- 来源链接：https://arxiv.org/abs/2302.12173
- DOI：https://doi.org/10.48550/arXiv.2302.12173
- 作者 / 机构：Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz
- 发布时间：2023-02-23；arXiv v2 updated 2023-05-05
- 最后复核日期：2026-07-11
- 类型：论文 / Security
- 主题：Prompt Injection / LLM-integrated Applications / Tool Security
- 适合阶段：工程实践 / 生产化
- 可信度等级：A
- 是否已验证：来源链接、HTTP metadata、arXiv 元数据和摘要已复核；支撑“外部内容会模糊数据与指令边界”和“prompt injection 不能只靠 prompt 解决”的安全窄边界；真实 guardrail / HITL / 框架防护效果仍部分验证

## 一句话总结

这篇论文是理解 indirect prompt injection 的核心安全资料：攻击者不一定直接和模型对话，也可以把恶意指令放进会被应用检索、浏览、总结或处理的外部数据里。

## 核心结论

- LLM-integrated applications 会模糊 data 和 instructions 的边界；外部网页、文档、搜索结果、邮件或代码注释中的文字可能被模型当作指令处理。
- Indirect prompt injection 允许攻击者在没有直接访问聊天界面的情况下，把恶意 prompt 注入到目标应用可能检索的数据中。
- 摘要列出的影响包括 data theft、worming、information ecosystem contamination，以及控制应用功能或 API 调用方式等风险。
- 论文把 processing retrieved prompts 类比为 arbitrary code execution 的风险信号；对初学者来说，保守理解应是：外部内容不能直接获得系统指令或工具调用权限。
- 论文声称当时 effective mitigations 仍不足；这支持正文中“不能把某个 guardrail 写成默认充分安全”的保守边界。

## 支撑证据

- arXiv 页面返回 HTTP 200；HTTP `last-modified` 为 2023-05-08。
- arXiv 元数据显示 submitted on 2023-02-23，last revised 2023-05-05，当前版本 v2。
- 摘要写明 Prompt Injection attacks enable attackers to override original instructions and employed controls。
- 摘要写明 LLM-Integrated Applications blur the line between data and instructions。
- 摘要写明 Indirect Prompt Injection 可以通过 injecting prompts into data likely to be retrieved 远程利用 LLM-integrated applications。
- 摘要写明攻击影响包括 data theft、worming、information ecosystem contamination，以及 manipulate application's functionality and control how and if other APIs are called。

## 是否进入正文

- 结论：进入；prompt injection 风险边界可入正文
- 原因：可与 OWASP LLM Top 10、NIST AI RMF、OpenAI tool calling 文档、标准库 prompt injection / permission 实验、安全 regression set 和审批状态恢复实验交叉支撑“外部内容是不可信数据；prompt 不是充分安全边界；工具权限、审批、审计和 regression set 必须由系统层承担”的窄结论。

## 可能的问题

- 论文中的具体真实系统案例反映 2023 年前后的系统和模型环境，不能直接泛化为当前所有模型或产品的拦截率。
- 摘要支撑风险类别和攻击面边界，但不能证明某个防护方案有效。
- 正文不应写成“处理外部文本等同于传统 RCE”，更稳妥的写法是：处理被注入的外部 prompt 可能控制模型后续行为和工具/API 调用，因此需要系统层权限隔离和审计。

## 初学者阅读建议

- 先读摘要，重点理解 indirect prompt injection 和“数据/指令边界被模糊”这两个概念。
- 不需要先读完整攻击 taxonomy；学到生产安全章节时，再结合 OWASP、工具权限和本手册实验一起读。

## 可复现实验

- 本手册已经完成标准库 prompt injection / permission 模拟实验，复现“外部文档注入诱导写工具”的最小失败模式。
- 已完成标准库安全 regression set 和审批状态恢复实验，覆盖外部注入、跨用户读取、高金额审批、敏感字段脱敏、破坏性工具和幂等性。
- 已准备真实 prompt injection / permission harness；无 API key 时跳过，配置后可记录真实模型是否请求高风险写工具、策略层是否阻断以及 trace 是否脱敏。该 harness 仍待真实运行。
