# AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents

- 来源链接：https://arxiv.org/abs/2406.13352；https://github.com/ethz-spylab/agentdojo；https://agentdojo.spylab.ai/；https://agentdojo.spylab.ai/results/
- DOI：https://doi.org/10.48550/arXiv.2406.13352
- 作者 / 机构：Edoardo Debenedetti, Jie Zhang, Mislav Balunovic, Luca Beurer-Kellner, Marc Fischer, Florian Tramer / ETH Zurich and collaborators
- 发布时间：2024-06-19；arXiv v3 updated 2024-11-24
- 最后复核日期：2026-07-12
- 类型：论文 / Benchmark / Source
- 主题：Prompt Injection / Tool-agent Security / Agent Evaluation
- 适合阶段：工程实践 / 生产化 / 评测
- 可信度等级：A
- 是否已验证：arXiv 页面、arXiv API 元数据、PDF 页数、GitHub repo metadata、README、项目站点和 results 页面可达性已于 2026-07-12 复核；支撑“工具型 Agent 的 prompt injection 评测应覆盖动态工具调用、非可信工具结果、状态变化、utility/security 双指标和自适应攻击边界”的窄结论；不验证当前模型表现、生产 guardrail / detector / HITL 有效性、成本、延迟或任意框架默认安全

## 一句话总结

AgentDojo 是一个面向工具调用 Agent 的 prompt injection 安全评测环境：它把用户任务、攻击者目标、注入位置、工具调用和环境状态放进同一个动态 benchmark，而不是只看最终回答是否正常。

## 核心结论

- 论文把风险设定为：Agent 需要调用工具处理外部或第三方数据，而这些工具返回的数据可能包含间接 prompt injection。
- AgentDojo 评测的是 stateful adversarial environments：工具可读写环境状态，utility 和 security 检查基于环境状态，而不是只靠 LLM 自评或最终文本答案。
- 论文报告的 benchmark 包含 4 个环境 / suite：Workspace、Slack、Travel、Banking；表 1 合计 70 个工具、97 个用户任务和 27 个注入目标，并在全文中评测 629 个 security test cases。
- 论文和 data card 说明 AgentDojo 适合测试 tool-calling agents 在 prompt injection 下的 utility 和 robustness，也适合测试攻击和防御；不适合只用默认攻击而不做自适应攻击和充分安全评估。
- 防御结论必须保守引用：论文显示 detector、重复用户 prompt、tool filtering 等方法在其设置中有不同 utility / attack-success tradeoff；但这些结果不能写成某个防御在生产中充分有效。
- Tool filtering 在论文设置中可以降低部分攻击成功率，但论文也列出失败条件：当所需工具无法提前规划、任务所需工具也足以完成攻击，或注入等待后续任务可用工具时，过滤策略会失效。

## 支撑证据

- arXiv 页面 2026-07-12 返回 HTTP 200；响应头 `last-modified: Tue, 26 Nov 2024 02:02:12 GMT`。
- arXiv API 2026-07-12 返回 entry `2406.13352v3`，published `2024-06-19T08:55:56Z`，updated `2024-11-24T22:04:23Z`，primary category `cs.CR`，并列 `cs.LG`；comment 说明 v3 修复 Llama implementation bug 并更新 travel suite。
- PDF 已于 2026-07-12 下载并用 `pypdf` 确认 26 页。
- 摘要写明 AI agents combine text reasoning with external tool calls，且会受到 prompt injection attacks，其中 external tools 返回的数据可能 hijack the agent。
- 摘要写明 AgentDojo evaluates agents executing tools over untrusted data，并是 extensible environment for tasks, defenses, and adaptive attacks。
- 摘要写明 benchmark populated with 97 realistic tasks, 629 security test cases, attacks and defenses from the literature。
- 论文第 2 页说明 AgentDojo requires dynamic multi-tool calling in stateful adversarial environments，utility checks computed over environment state 而不是 LLM simulator。
- 论文第 3 页说明 untrusted data returned by tools is an effective vector for indirect prompt injection，并指出 current techniques are not foolproof。
- 论文表 1 列出 Workspace / Slack / Travel / Banking 四个环境，合计 70 tools、97 user tasks 和 27 injection targets；表格数字优先于正文中出现的 74 tools 表述。
- 论文第 7 页说明评测 full suite of 629 security test cases over 97 user tasks，并使用 official provider APIs except Llama 3 custom prompt。
- 论文第 9 页说明 prompt injection detector false positives degraded utility，repeating user prompt after tool call unlikely to withstand adaptive attacks，tool filtering 在其 suite 中降低攻击成功率但有明确失败条件。
- Data card 页列出 dataset name AgentDojo、dataset link GitHub、DOI `10.5281/zenodo.12528188`、release date 06/2024、current version v1.0、regularly updated，并说明 synthetic data 不含有意或无意收集的敏感数据。
- GitHub repo 2026-07-12 通过 API 复核：`ethz-spylab/agentdojo`，public，MIT license，default branch `main`，language Python，archived false，topics 包含 `benchmark`、`large-language-models`、`prompt-injection`、`security`。
- README 2026-07-12 复核：描述 AgentDojo is a dynamic environment to evaluate attacks and defenses for LLM agents，quickstart 为 `pip install agentdojo`，并提示 package API still under development and might change。
- 项目站点 `https://agentdojo.spylab.ai/` 和 results 页面 `https://agentdojo.spylab.ai/results/` 于 2026-07-12 均返回 HTTP 200。

## 是否进入正文

- 结论：部分进入；安全评测 / regression set 设计边界可入正文
- 原因：可与 Indirect Prompt Injection paper、OWASP LLM Top 10、OWASP Agentic AI resources、MITRE ATLAS、Microsoft Prompt Shields、Anthropic mitigation docs、本手册 prompt injection / permission 实验和 agentic security regression set 交叉支撑“工具型 Agent 安全评测不能只看最终回答，要覆盖非可信工具结果、状态变化、用户目标、攻击者目标、注入端点、utility/security checks 和自适应攻击”的窄结论。它不能支撑某个 detector、tool filtering、guardrail、HITL、sandbox 或框架在生产中充分安全。

## 可能的问题

- 论文数据反映 2024 年及其 v3 设置，不能外推为当前模型、当前 API 或当前框架的攻击成功率。
- 论文中的攻击成功率和防御效果必须写成“在 AgentDojo suite / 论文设置中”，不能写成通用安全事实。
- Data card 的 dataset snapshot 写 124 tasks，而论文主文表格和摘要强调 97 user tasks / 629 security test cases；正文引用任务规模时应说明取自论文主文 benchmark，避免混用 snapshot 数字。
- GitHub README 明确 package API still under development，不能把当前包接口写成稳定教程。
- AgentDojo 是 benchmark / evaluation environment，不是生产防护方案；它不证明 detector、prompt rewriting、tool filtering、HITL 或 sandbox 的充分性。
- 本卡没有运行 AgentDojo benchmark，也没有复现任何模型攻击或防御结果。

## 初学者阅读建议

- 先读摘要和表 1，理解为什么工具型 Agent 的安全测试要同时看“用户任务是否完成”和“攻击者目标是否得逞”。
- 不要先记攻击成功率数字；先学习 case 设计：用户目标、攻击者目标、注入位置、可用工具、环境状态和通过/失败判定。
- 读第 9 页防御讨论时重点看 tradeoff 和失败条件，避免把某个检测器或工具过滤策略当成万能方案。

## 可复现实验

- 本手册已有标准库 prompt injection / permission、security regression set 和 agentic security regression set，可把 AgentDojo 的 case 设计思想继续扩展为 stateful tool-agent benchmark。
- 后续真实实验可选择 AgentDojo 的一个小 suite，记录模型、工具调用轨迹、utility pass/fail、security pass/fail、攻击类型、防御策略、误报/漏报、成本和延迟。
- 真实运行前应明确：是否使用官方 benchmark、是否使用当前 package API、是否做自适应攻击、是否只测试默认攻击，以及结果是否只适用于所选模型 / suite / 防御配置。
