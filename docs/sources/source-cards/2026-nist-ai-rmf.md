# NIST AI Risk Management Framework

- 来源链接：https://www.nist.gov/itl/ai-risk-management-framework
- 相关链接：https://airc.nist.gov/airmf-resources/playbook/；https://doi.org/10.6028/NIST.AI.600-1；https://www.nist.gov/programs-projects/concept-note-ai-rmf-profile-trustworthy-ai-critical-infrastructure
- 作者 / 机构：NIST
- 发布时间：AI RMF 1.0 发布于 2023-01-26；页面持续更新，HTTP last-modified 复核为 2026-07-11；页面显示 AI RMF 1.0 is being revised
- 最后复核日期：2026-07-12
- 类型：Standard / Risk Guidance
- 主题：Risk Management / Governance / Production
- 适合阶段：生产化 / 治理
- 可信度等级：A
- 是否已验证：AI RMF 主页面、AIRC / Playbook 和 Critical Infrastructure concept note 已于 2026-07-12 复核；关键概述段落和 Playbook 边界已精读；支撑生产安全风险治理、全生命周期治理和检查清单设计的窄边界；安全 regression set 已完成；GenAI profile 仅由主页面摘要支撑，DOI/PDF 当前取回失败；具体 Agent 控制仍部分验证

## 一句话总结

NIST AI RMF 适合为生产化章节提供风险管理、治理和可信 AI 的宏观框架，但不应被当作 Agent 专用的工具隔离实现指南。

## 核心结论

- NIST AI RMF 面向 AI 风险管理，目标是帮助组织把 trustworthiness considerations 纳入 AI 产品、服务和系统的 design、development、use 和 evaluation。
- AI RMF 明确是 voluntary use，适合作为上线前风险治理框架，而不是强制合规清单或 Agent 框架说明书。
- 主页面显示 `The AI RMF 1.0 is being revised`，因此正文不能把 AI RMF 1.0 写成未来长期稳定、不变的最终版本。
- AIRC Playbook 页面说明 Playbook 提供 suggested actions 以达成 AI RMF outcomes，并按 Govern、Map、Measure、Manage 四个 functions 对齐；同时明确 Playbook is neither a checklist nor set of steps to be followed in its entirety，suggestions are voluntary。
- NIST 主页面说明 `NIST-AI-600-1: Generative Artificial Intelligence Profile` 可帮助组织识别 generative AI unique risks 并提出风险管理行动；但本次 DOI/PDF 获取未成功，当前只可引用主页面摘要，不能写成已精读 profile 全文。
- 2026 年 Critical Infrastructure concept note 支撑“高风险/关键基础设施场景需要更明确的 trustworthiness requirements、生命周期和供应链沟通”的治理边界；它仍是 profile development / community-of-interest 资料，不是 Agent 工具权限实现指南。
- 页面材料支持把生产化章节组织成 Govern、Map、Measure、Manage 或“识别风险、度量风险、管理风险、治理风险”的思路，但不直接给出 prompt injection 的具体工程防护。

## 支撑证据

- 2026-07-12 使用 `curl -L -I https://www.nist.gov/itl/ai-risk-management-framework` 复核 NIST AI RMF 主页面，返回 HTTP 200，`content-type: text/html; charset=UTF-8`，`last-modified: Sat, 11 Jul 2026 09:51:11 GMT`。
- 页面概述写明 AI RMF “is intended for voluntary use”。
- 页面概述写明 AI RMF 用于提升把 trustworthiness considerations 纳入 AI products、services 和 systems 的 design、development、use、evaluation 的能力。
- 页面 callout 写明 `The AI RMF 1.0 is being revised`。
- 页面写明 `NIST-AI-600-1` 可帮助组织 identify unique risks posed by generative AI，并 proposes actions for generative AI risk management；2026-07-12 使用 `curl -L -I https://doi.org/10.6028/NIST.AI.600-1` 观察到 DOI 302 到 `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`，但后者返回 HTTP 404；直接 HEAD `NIST.AI.600-1.pdf` 也返回 404。因此当前未精读 GenAI profile 全文。
- 页面中的 AI RMF 图示 alt 文本包含 `Govern, Measure, Manage, Map` 四个核心功能。
- 2026-07-12 使用 `curl -L -I https://airc.nist.gov/airmf-resources/playbook/` 复核 AIRC Playbook，返回 HTTP 200；页面说明 Playbook provides suggested actions for achieving AI RMF outcomes，suggestions are aligned to Govern, Map, Measure, Manage，并明确 Playbook is neither a checklist nor set of steps to be followed in its entirety。
- 2026-07-12 使用 `curl -L -I https://www.nist.gov/programs-projects/concept-note-ai-rmf-profile-trustworthy-ai-critical-infrastructure` 复核 Critical Infrastructure concept note，返回 HTTP 200，`last-modified: Sat, 11 Jul 2026 10:00:10 GMT`；页面显示 published 2026-04-07，created 2026-04-06，updated 2026-04-08，并说明 profile will guide critical infrastructure operators towards specific risk management practices when engaging AI-enabled capabilities。

## 可能的问题

- AI RMF 是治理框架，不是 Agent 专用工程指南。
- 初学者章节应只抽取和 Agent 上线相关的风险管理思路，避免过早引入合规复杂度。
- 当前 source card 只精读页面概述、Playbook landing page 和 Critical Infrastructure concept note 页面；完整 AI RMF PDF、GenAI profile PDF、Playbook 详细条目和 Critical Infrastructure concept note PDF 仍待后续精读。
- `NIST-AI-600-1` DOI / PDF 当前取回失败，后续应重新复核 DOI 或寻找新的官方 landing page；在此之前不能把 GenAI profile 全文结论写入正文。

## 初学者阅读建议

- 在理解 Agent 工程风险之后再读，用于建立生产化和治理意识。

## 可复现实验

- 不适合直接复现实验；可转化为上线前风险检查清单。
- 已完成标准库安全 regression set、agentic security regression set 和 production safety / data governance checklist，作为把风险治理资料转成可运行 case matrix / checklist 字段的最小示例；它们不证明 NIST 风险治理流程已经完整落地。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 Production / Governance 章节的风险管理框架、AI RMF 1.0 修订状态、Playbook 自愿建议边界和 GenAI / critical-infrastructure 风险意识；与 OWASP、框架安全文档和标准库安全实验共同支撑“安全控制应进入设计、开发、使用和评测流程”的治理边界。具体 Agent 安全控制、GenAI profile 全文结论和真实拦截效果仍需工程文档与实验补充。
