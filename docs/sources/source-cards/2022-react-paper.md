# ReAct: Synergizing Reasoning and Acting in Language Models

- 来源链接：https://arxiv.org/abs/2210.03629
- 作者 / 机构：Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- 发布时间：2022-10-06；arXiv v3 updated 2023-03-10；ICLR camera-ready version
- 最后复核日期：2026-07-11
- 类型：论文
- 主题：Agent 架构 / Tool Use / Reasoning
- 适合阶段：进阶 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接、arXiv 元数据和摘要已复核；Agent/Workflow 控制权连续谱和复杂架构不是默认更可靠的窄边界可入正文；ReAct 效果仍部分验证

## 一句话总结

ReAct 是理解“推理步骤”和“行动步骤”交替执行的核心论文，适合作为 Agent 架构章节的重要 reference。

## 核心结论

- 论文提出让 LLM 交替生成 reasoning traces 和 task-specific actions。
- 摘要声称 reasoning traces 可帮助模型诱导、跟踪、更新行动计划并处理异常，actions 让模型连接知识库或外部环境以获取信息。
- 论文在问答、事实验证和交互式决策任务上评估 ReAct，并报告相对部分 baseline 有效果提升。
- 摘要中的具体任务包括 HotpotQA、Fever、ALFWorld 和 WebShop；这些任务可支撑“ReAct 适用于部分知识检索和交互式决策实验”的保守表述。

## 支撑证据

- arXiv API 返回有效条目：`2210.03629v3`。
- arXiv comment 标注 v3 为 ICLR camera-ready version，并给出项目站点 `https://react-lm.github.io`。
- 2026-07-11 抓取 arXiv 页面成功；摘要包含 interleaved reasoning traces and task-specific actions、update action plans、handle exceptions、interface with external sources 等关键表述。
- 已与 Reflexion、Tree of Thoughts、OpenAI Agents SDK、LangGraph 和多 Agent evidence 交叉验证架构模式边界。

## 可能的问题

- 论文实验环境和当前模型能力可能存在差异，需要结合现代框架文档复核。
- 摘要中的效果提升来自特定任务和 baseline，不能泛化成“ReAct 总是优于 workflow”。

## 和其他资料的对比

- 已与 LangGraph / OpenAI Agents SDK / Reflexion / Tree of Thoughts 完成第一轮交叉验证；标准库 workflow / hybrid / ReAct-like 对比实验已覆盖最小控制流差异，并支撑“Agent/Workflow 是控制权连续谱”和“复杂架构不是默认更可靠”的窄边界。仍需真实模型和框架任务验证 ReAct 稳定性、成本、延迟和失败恢复。

## 初学者阅读建议

- 先读章节中的通俗解释，再读论文摘要和方法部分。

## 可复现实验

- 比较 ReAct 风格工具循环和固定 workflow 在检索任务中的成功率、成本和延迟。

## 是否进入正文

- 结论：进入
- 原因：Agent 架构基础论文；可支撑“推理和行动交替”的模式解释，并与工程文档/标准库实验共同支撑 Agent/Workflow 控制权连续谱和复杂架构默认可靠性边界；但不能支撑默认采用 ReAct。
