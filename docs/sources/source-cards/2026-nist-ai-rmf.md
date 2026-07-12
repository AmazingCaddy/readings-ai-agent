# NIST AI Risk Management Framework

- 来源链接：https://www.nist.gov/itl/ai-risk-management-framework
- 相关链接：https://airc.nist.gov/airmf-resources/playbook/；https://airc.nist.gov/docs/playbook.json；https://airc.nist.gov/docs/playbook.csv；https://airc.nist.gov/docs/AI_RMF_Playbook.pdf；https://doi.org/10.6028/NIST.AI.600-1；https://www.nist.gov/programs-projects/concept-note-ai-rmf-profile-trustworthy-ai-critical-infrastructure
- 作者 / 机构：NIST
- 发布时间：AI RMF 1.0 发布于 2023-01-26；页面持续更新，HTTP last-modified 复核为 2026-07-11；页面显示 AI RMF 1.0 is being revised
- 最后复核日期：2026-07-12
- 类型：Standard / Risk Guidance
- 主题：Risk Management / Governance / Production
- 适合阶段：生产化 / 治理
- 可信度等级：A
- 是否已验证：AI RMF 主页面、AIRC Playbook landing、Playbook JSON/CSV/PDF 下载端点和 Critical Infrastructure concept note 已于 2026-07-12 复核；关键概述段落、Playbook 自愿建议边界和 JSON/CSV 字段样例已精读；支撑生产安全风险治理、全生命周期治理和检查清单字段设计的窄边界；安全 regression set 已完成；AI RMF 1.0 和 GenAI profile 的 DOI/PDF 当前均取回失败，因此 PDF 全文不能算已精读；具体 Agent 控制仍部分验证

## 一句话总结

NIST AI RMF 适合为生产化章节提供风险管理、治理和可信 AI 的宏观框架，但不应被当作 Agent 专用的工具隔离实现指南。

## 核心结论

- NIST AI RMF 面向 AI 风险管理，目标是帮助组织把 trustworthiness considerations 纳入 AI 产品、服务和系统的 design、development、use 和 evaluation。
- AI RMF 明确是 voluntary use，适合作为上线前风险治理框架，而不是强制合规清单或 Agent 框架说明书。
- 主页面显示 `The AI RMF 1.0 is being revised`，因此正文不能把 AI RMF 1.0 写成未来长期稳定、不变的最终版本。
- AI RMF 主页面仍可支撑上述概述；但 2026-07-12 复核时 AI RMF 1.0 的 DOI 和 PDF 直链也返回 404，因此本卡不能声称已精读 AI RMF 1.0 PDF 全文。
- AIRC Playbook 页面说明 Playbook 提供 suggested actions 以达成 AI RMF outcomes，并按 Govern、Map、Measure、Manage 四个 functions 对齐；同时明确 Playbook is neither a checklist nor set of steps to be followed in its entirety，suggestions are voluntary。
- AIRC Playbook JSON/CSV/PDF 下载端点可访问；JSON/CSV 结构化条目包含 `type`、`title`、`category`、`description`、`section_actions`、`section_doc`、`AI Actors`、`Topic` 等字段，可支撑把 governance checklist 拆成职责、主题、证据文档和动作项字段。
- Playbook 条目样例可支撑生产安全 / 数据治理 checklist 的字段设计：`GOVERN 1.2` 覆盖把 trustworthy AI characteristics 纳入 policies/processes/procedures、data governance、testing/validation、monitoring/auditing/review、incident response 和 third-party systems；`GOVERN 1.6` 支撑 AI system inventory；`GOVERN 1.7` 支撑 decommissioning；`MEASURE 4.2` / `MEASURE 4.3` 支撑 end-user / AI actor feedback、field data 和改进/退化记录。
- NIST 主页面说明 `NIST-AI-600-1: Generative Artificial Intelligence Profile` 可帮助组织识别 generative AI unique risks 并提出风险管理行动；但本次 DOI/PDF 获取未成功，当前只可引用主页面摘要，不能写成已精读 profile 全文。
- 2026 年 Critical Infrastructure concept note 支撑“高风险/关键基础设施场景需要更明确的 trustworthiness requirements、生命周期和供应链沟通”的治理边界；它仍是 profile development / community-of-interest 资料，不是 Agent 工具权限实现指南。
- 页面材料支持把生产化章节组织成 Govern、Map、Measure、Manage 或“识别风险、度量风险、管理风险、治理风险”的思路，但不直接给出 prompt injection 的具体工程防护。

## 支撑证据

- 2026-07-12 使用 `curl -L -I https://www.nist.gov/itl/ai-risk-management-framework` 复核 NIST AI RMF 主页面，返回 HTTP 200，`content-type: text/html; charset=UTF-8`，`last-modified: Sat, 11 Jul 2026 09:51:11 GMT`。
- 主页面 Quick Links 中仍包含 `Download the AI RMF 1.0`，目标为 `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf`；2026-07-12 使用 `curl -L -I https://doi.org/10.6028/NIST.AI.100-1` 观察到 DOI 跳转到该 PDF 后返回 HTTP 404；直接 HEAD `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf` 也返回 HTTP 404。因此当前未精读 AI RMF 1.0 PDF 全文。
- 页面概述写明 AI RMF “is intended for voluntary use”。
- 页面概述写明 AI RMF 用于提升把 trustworthiness considerations 纳入 AI products、services 和 systems 的 design、development、use、evaluation 的能力。
- 页面 callout 写明 `The AI RMF 1.0 is being revised`。
- 页面写明 `NIST-AI-600-1` 可帮助组织 identify unique risks posed by generative AI，并 proposes actions for generative AI risk management；2026-07-12 使用 `curl -L -I https://doi.org/10.6028/NIST.AI.600-1` 观察到 DOI 302 到 `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`，但后者返回 HTTP 404；直接 HEAD `NIST.AI.600-1.pdf` 也返回 404。因此当前未精读 GenAI profile 全文。
- 页面中的 AI RMF 图示 alt 文本包含 `Govern, Measure, Manage, Map` 四个核心功能。
- 2026-07-12 使用 `curl -L -I https://airc.nist.gov/airmf-resources/playbook/` 复核 AIRC Playbook，返回 HTTP 200；页面说明 Playbook provides suggested actions for achieving AI RMF outcomes，suggestions are aligned to Govern, Map, Measure, Manage，并明确 Playbook is neither a checklist nor set of steps to be followed in its entirety；页面还提示 `The AI RMF 1.0 is being updated. The Playbook will be updated after the AI RMF is revised.`
- Playbook landing 暴露 `AI_RMF_Playbook.pdf`、`playbook.csv`、`playbook.xlsx`、`playbook.json` 下载入口。2026-07-12 使用 `curl -L -I` 复核 `https://airc.nist.gov/docs/playbook.json`，返回 HTTP 200，`content-type: application/json`，`content-length: 413720`，`last-modified: Thu, 11 Jun 2026 19:18:21 GMT`；`https://airc.nist.gov/docs/playbook.csv` 返回 HTTP 200，`content-length: 356966`，`last-modified: Thu, 11 Jun 2026 19:08:50 GMT`；`https://airc.nist.gov/docs/AI_RMF_Playbook.pdf` 返回 HTTP 200，`content-type: application/pdf`，`content-length: 2882270`，`last-modified: Mon, 16 Sep 2024 16:19:06 GMT`。
- `playbook.json` 抽样确认是结构化数组，条目字段包括 `type`、`title`、`category`、`description`、`section_about`、`section_actions`、`section_doc`、`section_ref`、`AI Actors`、`Topic`。已抽样复核 `GOVERN 1.1`、`GOVERN 1.2`、`GOVERN 1.3`、`GOVERN 1.4`，并在 JSON/CSV 中观察到 `GOVERN 1.5`、`GOVERN 1.6`、`GOVERN 1.7`、`GOVERN 5.1`、`MAP`、`MEASURE 4.2`、`MEASURE 4.3` 等 governance、inventory、monitoring、incident response、stakeholder feedback、third-party risk、decommissioning 相关条目。
- 2026-07-12 使用 `curl -L -I https://www.nist.gov/programs-projects/concept-note-ai-rmf-profile-trustworthy-ai-critical-infrastructure` 复核 Critical Infrastructure concept note，返回 HTTP 200，`last-modified: Sat, 11 Jul 2026 10:00:10 GMT`；页面显示 published 2026-04-07，created 2026-04-06，updated 2026-04-08，并说明 profile will guide critical infrastructure operators towards specific risk management practices when engaging AI-enabled capabilities。

## 可能的问题

- AI RMF 是治理框架，不是 Agent 专用工程指南。
- 初学者章节应只抽取和 Agent 上线相关的风险管理思路，避免过早引入合规复杂度。
- 当前 source card 已精读页面概述、Playbook landing page、Playbook JSON/CSV/PDF 可访问性和 JSON/CSV 代表性字段样例；完整 AI RMF PDF、GenAI profile PDF、Playbook 全量逐条分析和 Critical Infrastructure concept note PDF 仍待后续精读。
- `NIST.AI.100-1` 和 `NIST.AI.600-1` DOI / PDF 当前取回失败，后续应重新复核 DOI 或寻找新的官方 landing page；在此之前不能把 AI RMF 1.0 PDF 或 GenAI profile 全文结论写入正文。

## 初学者阅读建议

- 在理解 Agent 工程风险之后再读，用于建立生产化和治理意识。

## 可复现实验

- 不适合直接复现实验；可转化为上线前风险检查清单。
- 已完成标准库安全 regression set、agentic security regression set 和 production safety / data governance checklist，作为把风险治理资料转成可运行 case matrix / checklist 字段的最小示例；它们不证明 NIST 风险治理流程已经完整落地。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 Production / Governance 章节的风险管理框架、AI RMF 1.0 修订状态、Playbook 自愿建议边界、Playbook 结构化 governance checklist 字段设计和 GenAI / critical-infrastructure 风险意识；与 OWASP、框架安全文档和标准库安全实验共同支撑“安全控制应进入设计、开发、使用和评测流程”的治理边界。具体 Agent 安全控制、AI RMF PDF / GenAI profile 全文结论、真实项目合规状态和真实拦截效果仍需工程文档与实验补充。
