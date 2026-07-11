# NIST AI Risk Management Framework

- 来源链接：https://www.nist.gov/itl/ai-risk-management-framework
- 作者 / 机构：NIST
- 发布时间：AI RMF 1.0 发布于 2023-01-26；页面持续更新，HTTP last-modified 复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：Standard / Risk Guidance
- 主题：Risk Management / Governance / Production
- 适合阶段：生产化 / 治理
- 可信度等级：A
- 是否已验证：来源链接已复核；关键概述段落已精读；结论已部分交叉验证；安全 regression set 已完成

## 一句话总结

NIST AI RMF 适合为生产化章节提供风险管理、治理和可信 AI 的宏观框架，但不应被当作 Agent 专用的工具隔离实现指南。

## 核心结论

- NIST AI RMF 面向 AI 风险管理，目标是帮助组织把 trustworthiness considerations 纳入 AI 产品、服务和系统的 design、development、use 和 evaluation。
- AI RMF 明确是 voluntary use，适合作为上线前风险治理框架，而不是强制合规清单或 Agent 框架说明书。
- NIST 发布的 `NIST-AI-600-1: Generative Artificial Intelligence Profile` 专门帮助组织识别 generative AI 的 unique risks，并提出与组织目标和优先级一致的风险管理行动。
- 页面材料支持把生产化章节组织成“识别风险、度量风险、管理风险、治理风险”的思路，但不直接给出 prompt injection 的具体工程防护。

## 支撑证据

- NIST 页面返回 HTTP 200；HTTP `last-modified` 为 2026-07-11；页面 metadata 显示 `article:modified_time` 为 2026-06-10。
- 页面概述写明 AI RMF “is intended for voluntary use”。
- 页面概述写明 AI RMF 用于提升把 trustworthiness considerations 纳入 AI products、services 和 systems 的 design、development、use、evaluation 的能力。
- 页面写明 `NIST-AI-600-1` 可帮助组织 identify unique risks posed by generative AI，并 proposes actions for generative AI risk management。
- 页面中的 AI RMF 图示 alt 文本包含 `Govern, Measure, Manage, Map` 四个核心功能。

## 可能的问题

- AI RMF 是治理框架，不是 Agent 专用工程指南。
- 初学者章节应只抽取和 Agent 上线相关的风险管理思路，避免过早引入合规复杂度。
- 当前 source card 只精读页面概述和 GenAI profile 入口；完整 AI RMF PDF 和 Playbook 仍待后续精读。

## 初学者阅读建议

- 在理解 Agent 工程风险之后再读，用于建立生产化和治理意识。

## 可复现实验

- 不适合直接复现实验；可转化为上线前风险检查清单。
- 已完成标准库安全 regression set，作为把风险清单转成可运行 case matrix 的最小示例；它不证明 NIST 风险治理流程已经完整落地。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 Production / Governance 章节的风险管理框架和 GenAI 风险意识；具体 Agent 安全控制仍需 OWASP、框架安全文档和实验补充。
