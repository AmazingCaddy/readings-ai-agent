# OWASP Agentic AI Security Resources

- 来源链接：https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/；https://genai.owasp.org/resource/aiuc-1-crosswalks-owasp-top-10-for-agentic-applications/；https://genai.owasp.org/resource/state-of-agentic-ai-security-and-governance/
- 作者 / 机构：OWASP Gen AI Security Project / OWASP Agentic Security Initiative
- 发布时间：`Agentic AI - Threats and Mitigations` 页面发布时间 2025-02-17，修改时间 2025-04-28；`AIUC-1 Crosswalks OWASP Top 10 For Agentic Applications` 页面发布时间 2026-05-25；`State of Agentic AI Security and Governance 2.01` 页面发布时间 2026-06-02，修改时间 2026-06-08
- 最后复核日期：2026-07-11
- 类型：Security Guidance / Whitepaper metadata
- 主题：Agentic AI Security / Tool Misuse / Privilege Abuse / Memory Poisoning / Governance
- 适合阶段：工程实践 / 生产化
- 可信度等级：A/B
- 是否已验证：公开资源页、HTTP metadata 和 WordPress JSON 摘要已复核；可支撑 agentic AI 风险分类和治理 gap 的保守边界；白皮书下载端点返回 no-access，全文未精读；真实缓解效果仍未验证

## 一句话总结

OWASP Agentic Security Initiative 的公开资源补强了 Agentic AI 特有风险面：目标劫持、工具误用、身份和权限滥用、记忆污染、多 Agent 通信、级联失败、信任利用和失控 Agent。

## 核心结论

- `Agentic AI - Threats and Mitigations` 页面把 agentic AI 描述为 autonomous systems 的发展，并指出 LLM / generative AI 集成扩大了规模、能力和相关风险。
- 该页面说明该文档是 OWASP Agentic Security Initiative 的系列指南之一，目标是提供 threat-model-based reference 并讨论 mitigations。
- `AIUC-1 Crosswalks OWASP Top 10 For Agentic Applications` 页面说明其把 AIUC-1 requirements 与 OWASP Agentic Security Initiative 的 Top 10 risks 做双向映射。
- 公开摘要列出的 agentic 风险包括 agent goal hijacking、tool misuse、identity and privilege abuse、memory poisoning、insecure inter-agent communication、cascading failures、trust exploitation 和 rogue agents。
- 公开摘要还列出治理 gap：agent identity、runtime containment、architectural monitoring、supply chain attestation 和 schema controls 等需要新增或扩展要求的方向。
- `State of Agentic AI Security and Governance 2.01` 页面把报告定位为梳理 autonomous AI systems 的 security / governance landscape、frameworks、governance models 和 global regulatory standards。

## 支撑证据

- `Agentic AI - Threats and Mitigations` 页面返回 HTTP 200；HEAD metadata 显示 `last-modified: Wed, 24 Jun 2026 15:28:58 GMT`；WP JSON 显示 `date: 2025-02-17T11:19:52`、`modified: 2025-04-28T11:35:15`。
- `Agentic AI - Threats and Mitigations` WP JSON 摘要写明：agentic AI predates modern LLMs，但与 generative AI 集成显著扩大 scale、capabilities 和 associated risks；该文档是 OWASP ASI guides 系列第一篇，用于 threat-model-based reference 和 mitigations。
- `AIUC-1 Crosswalks OWASP Top 10 For Agentic Applications` 页面返回 HTTP 200；WP JSON 显示 `date: 2026-05-25T09:37:49`。
- `AIUC-1 Crosswalks` WP JSON 摘要直接列出 agent goal hijacking、tool misuse、identity and privilege abuse、memory poisoning、insecure inter-agent communication、cascading failures、trust exploitation 和 rogue agents。
- `AIUC-1 Crosswalks` WP JSON 摘要列出 gap analysis 的优先方向：agent identity、runtime containment、architectural monitoring、supply chain attestation 和 schema controls。
- `State of Agentic AI Security and Governance 2.01` WP JSON 显示 `date: 2026-06-01T22:48:51`、`modified: 2026-06-08T12:35:04`，摘要说明该报告面向 autonomous AI systems 的安全、治理、frameworks、governance models 和 regulatory standards。
- `Agentic AI - Threats and Mitigations` 下载端点 `https://genai.owasp.org/download/45674/` 当前重定向到 no-access 页面；因此本卡没有把白皮书全文内容当成已精读证据。

## 可能的问题

- 当前可验证内容主要来自公开资源页和 WP JSON 摘要，不是完整白皮书正文。
- OWASP 资源适合支撑风险分类和治理方向，不能单独证明任何 mitigation、tool guardrail、identity system、runtime containment 或 schema control 的真实有效性。
- `AIUC-1 Crosswalks` 是 crosswalk / governance 映射资料，不应被写成某个 Agent 框架的实现建议。
- 需要与 OWASP LLM Top 10、NIST AI RMF、OpenAI / Anthropic / Microsoft 官方工程文档和本地实验交叉使用。

## 初学者阅读建议

- 先把这些风险名当成检查清单，不要试图一次理解所有治理框架。
- 阅读时重点对应本手册第 09 章：工具误用、权限滥用、记忆污染、多 Agent 通信和级联失败都需要系统层 trace、权限、审批和 regression tests。

## 可复现实验

- 安全 regression set 可扩展 agentic-specific cases：goal hijacking、tool misuse、identity / privilege abuse、memory poisoning、insecure inter-agent communication 和 cascading failure。
- Prompt injection / permission harness 可扩展到工具输出污染、长期记忆污染、跨 Agent 消息污染和 rogue agent / runaway loop 停止条件。
- Real LangGraph Interrupt Recovery 实验可覆盖 runtime containment、approval state、duplicate resume、rejected resume 和 trace 脱敏。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑第 09/12 章中“Agentic AI 风险不仅是 prompt injection，还包括工具误用、身份/权限滥用、记忆污染、多 Agent 通信、级联失败、运行时隔离和架构监控”等保守风险边界；不能支撑具体缓解方案默认有效，也不能替代完整白皮书精读或真实框架实验。
