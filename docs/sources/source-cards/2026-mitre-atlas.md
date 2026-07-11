# MITRE ATLAS

- 来源链接：https://atlas.mitre.org/；https://atlas.mitre.org/atlas-data/dist/manifest.yaml；https://atlas.mitre.org/atlas-data/dist/v6/ATLAS-2026.06.yaml
- 作者 / 机构：MITRE
- 发布时间：collection `created-date: 2020-10-23`；当前复核版本 `2026.06`，manifest `release-date: 2026-06-30`
- 最后复核日期：2026-07-12
- 类型：Threat Knowledge Base / YAML Dataset
- 主题：AI Security / Adversarial Techniques / Agentic AI / Prompt Injection / Tool Misuse / Memory Poisoning
- 适合阶段：工程实践 / 生产化 / 安全测试设计
- 可信度等级：A
- 是否已验证：主页、manifest、最新 v6 YAML 数据、HTTP metadata、term catalog 和关键 Agentic AI 条目 2026-07-12 已复核；可支撑 AI / Agentic AI 攻击技术分类、case study 与安全 regression set 设计；不能证明任意 mitigation、detector、guardrail、sandbox、HITL 或监控方案在真实系统中有效

## 一句话总结

MITRE ATLAS 是面向 AI 系统的 adversarial tactics、techniques、mitigations 和 case studies 知识库，可作为 Agent 安全测试用例和风险分类参考。

## 核心结论

- ATLAS 主页把 ATLAS 描述为 `Adversarial Threat Landscape for Artificial-Intelligence Systems`，是基于 real-world attack observations 和 realistic demonstrations 的 AI 系统 adversary tactics / techniques 知识库。
- 主页说明 ATLAS 是 globally accessible、living knowledge base，适合用作攻击面学习和测试用例来源，而不是某个具体框架的安全保证。
- 最新 manifest 显示 release `2026.06`，`release-date: 2026-06-30`，v6 数据路径为 `v6/ATLAS-2026.06.yaml`。
- 最新 YAML 显示 collection / matrix description 均为 `Adversarial Threat Landscape for AI Systems`，collection version 为 `2026.06`。
- 最新 YAML 抽样计数显示包含 173 个 `object-type: technique`、35 个 `object-type: mitigation`、63 个 `object-type: case-study`。
- term catalog 把 `Agentic AI` platform 定义为 adversary operating against AI components that can autonomously plan, decide, and execute multi-step actions，目标包括 agent logic、planning loops、tool integrations 和 control policies。
- term catalog 把 technique maturity 分为 `Feasible`、`Demonstrated`、`Realized`，可帮助初学者区分研究/控制环境、代表性部署条件和真实事件，但不能替代本地实验。
- 最新 YAML 包含 Agentic AI 相关条目，例如 `LLM Prompt Injection`、`AI Agent Tool Invocation`、`AI Agent Tool Poisoning`，以及 `Data Exfiltration from Slack AI via Indirect Prompt Injection`、`Hacking ChatGPT's Memories with Prompt Injection`、`Data Destruction via Indirect Prompt Injection Targeting Claude Computer-Use` 等 case studies。

## 支撑证据

- 主页返回 HTTP 200；HEAD metadata 显示 `last-modified: Tue, 30 Jun 2026 23:33:41 GMT`，`content-type: text/html; charset=utf-8`。
- 主页 HTML 指向静态资源 `/assets/index-BZkV2o0L.js`，前端 bundle 中的数据加载逻辑指向 `/atlas-data/dist/manifest.yaml` 和 manifest 中的 v6 YAML 路径。
- 2026-07-12 复核：`/atlas-data/dist/manifest.yaml` 返回 HTTP 200；HEAD metadata 显示 `content-type: text/yaml`、`last-modified: Tue, 30 Jun 2026 23:33:41 GMT`。manifest 第一项仍为 release `2026.06`、release-date `2026-06-30`、format-version `6.0.0`、path `v6/ATLAS-2026.06.yaml`。
- `/atlas-data/dist/v6/ATLAS-2026.06.yaml` 返回 HTTP 200；HEAD metadata 显示 `content-type: text/yaml`、`last-modified: Tue, 30 Jun 2026 23:33:41 GMT`、`content-length: 625790`。
- 最新 YAML 开头显示 `format-version: 6.0.0`、collection `name: ATLAS`、description `Adversarial Threat Landscape for AI Systems`、created-date `2020-10-23`、modified-date `2026-05-27`、version `2026.06`。
- 2026-07-12 复核：最新 YAML 包含 tactics、techniques、mitigations、case-studies 和 relationships；`object-type` 计数仍为 173 techniques、35 mitigations、63 case studies。
- term catalog 明确列出 platform values：`Predictive AI`、`Generative AI`、`Agentic AI`、`Enterprise`，并给出 Agentic AI 的 multi-step action / memory / tool use / workflow orchestration 相关定义。
- term catalog 明确列出 maturity values：`Feasible`、`Demonstrated`、`Realized`。
- 2026-07-12 复核：最新 YAML 仍命中 `LLM Prompt Injection`、`AI Agent Tool Invocation`、`AI Agent Tool Poisoning`、`Data Exfiltration from Slack AI via Indirect Prompt Injection`、`Hacking ChatGPT's Memories with Prompt Injection` 和 `Data Destruction via Indirect Prompt Injection Targeting Claude Computer-Use`。

## 可能的问题

- ATLAS 是威胁知识库和数据集，不是 Agent 框架文档，也不是防护产品评测。
- ATLAS 的 mitigations 可作为控制候选和 checklist 来源，但不能直接证明任何 mitigation 在本手册实验环境或读者系统中有效。
- Case study 的真实性、适用范围和复现难度需要逐条看原始 references；不能只凭 case title 推导普遍风险概率。
- 最新数据会随 release 更新，章节中应尽量引用 source card 和版本号，而不是把条目数量写成长期不变事实。

## 初学者阅读建议

- 先从 `LLM Prompt Injection`、`AI Agent Tool Invocation`、`AI Agent Tool Poisoning`、memory 相关条目和 case studies 入手，不必一次读完整矩阵。
- 阅读时重点问三个问题：攻击者需要什么入口？会影响哪些工具/记忆/数据？本地 regression set 需要增加哪一个可复现 case？
- 不要把 `mitigation` 条目当作“照做就安全”。它们适合变成待验证 checklist，再用本地实验验证覆盖范围、误报、漏报、成本和延迟。

## 可复现实验

- 将 ATLAS 中 Agentic AI platform 的 technique 和 case study 抽样转成安全 regression set：prompt injection、tool invocation、tool poisoning、memory poisoning、MCP / remote tool、computer-use data destruction、resource / cost abuse。
- 为每个 case 记录 expected decision、risk tags、required permissions、required trace fields、expected approval state、false positive / false negative 和 secret leak 字段。
- 对 mitigation 条目只做 checklist 候选，必须通过真实模型 / 框架 / 检测层 / HITL / trace 实验后才能升级为效果结论。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑第 09/12 章中“安全 regression set 应覆盖真实攻击技术和 case-study-derived 场景”的保守边界；可补强 prompt injection、tool invocation、tool poisoning、memory poisoning、remote/MCP tool 和 computer-use 风险分类；不能支撑任意防护方案默认有效，也不能替代真实框架实验。
