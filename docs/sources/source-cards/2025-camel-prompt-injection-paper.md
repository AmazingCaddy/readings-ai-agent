# Defeating Prompt Injections by Design

- 来源链接：https://arxiv.org/abs/2503.18813；https://github.com/google-research/camel-prompt-injection
- 作者 / 机构：Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Andreas Terzis, Florian Tramer / Google, Google DeepMind, ETH Zurich
- 发布时间：2025-03-24；arXiv v2 updated 2025-06-24
- 最后复核日期：2026-07-12
- 类型：论文 / Source / Security Architecture
- 主题：Prompt Injection Defense / Tool-agent Security / Capability-based Isolation
- 适合阶段：进阶 / Production 安全 / 评测
- 可信度等级：A
- 是否已验证：arXiv 页面、arXiv API metadata、GitHub repo metadata、README 和关键源码入口已于 2026-07-12 复核；支撑“prompt injection 防护应把可信控制流和非可信数据流分开，并在工具调用时用 capability / security policy 约束数据外流”的安全架构边界；真实模型表现、生产防护有效性、代码安全性、成本和延迟仍部分验证

## 一句话总结

CaMeL 是一篇 prompt injection 防护架构论文和研究代码：它把可信用户请求中的控制流 / 数据流抽取出来，让非可信工具数据不能改变程序流，并在工具调用时用 capability policy 限制未授权数据流。

## 核心结论

- 论文的问题设定是 agentic systems 会和 untrusted environment 交互，LLM agent 在处理非可信数据时容易受到 prompt injection。
- CaMeL 的核心防护思路不是“写更强 system prompt”，而是在 LLM 外围创建 protective system layer。
- 摘要明确说 CaMeL 从 trusted query 中显式抽取 control 和 data flows，因此 LLM 后续检索到的 untrusted data 不能影响 program flow。
- CaMeL 还引入 capability 概念，在工具调用时执行 security policies，防止 private data 通过 unauthorized data flows 外泄。
- 论文摘要报告在 AgentDojo 上用 provable security 完成 77% 任务，对比 undefended system 84%；这个数字只能作为论文设置下的 utility/security tradeoff，不应写成当前模型或生产系统的通用表现。
- GitHub README 明确代码是 research artifact，用于复现论文结果；interpreter implementation 可能有 bug、可能不 fully secure，不是 Google product，也不计划维护或支持。
- 源码入口 `main.py` 使用 AgentDojo suites，并支持 `--use-original`、`--ad_defense`、`--run-attack`、`--replay-with-policies` 和 `--eval_mode`；`models.py` 中可见 `+camel`、`+camel+secpol`、suite-specific security policy engines 和多 provider model wiring。这支持把它当作安全研究复现代码，而不是通用生产库。

## 支撑证据

- 2026-07-12 复核 arXiv 页面 `https://arxiv.org/abs/2503.18813` 返回 HTTP 200，`last-modified: Wed, 25 Jun 2025 00:30:46 GMT`。
- 2026-07-12 复核 arXiv API：entry `2503.18813v2`，标题 `Defeating Prompt Injections by Design`，published `2025-03-24T15:54:10Z`，updated `2025-06-24T08:05:33Z`，primary category `cs.CR`，also `cs.AI`，comment 为 `Updated version with newer models and link to the code`。
- arXiv 摘要明确写明 LLM agents interact with an untrusted environment，handling untrusted data makes them vulnerable to prompt injection attacks。
- arXiv 摘要明确写明 CaMeL creates a protective system layer around the LLM，extracts control and data flows from the trusted query，使 untrusted data retrieved by the LLM can never impact the program flow。
- arXiv 摘要明确写明 CaMeL uses a notion of capability to prevent exfiltration of private data over unauthorized data flows by enforcing security policies when tools are called。
- arXiv 摘要报告 CaMeL 在 AgentDojo 中 solves 77% of tasks with provable security compared to 84% with an undefended system；正文引用时应保留“paper / AgentDojo setting”限定。
- 2026-07-12 复核 GitHub 页面 `https://github.com/google-research/camel-prompt-injection` 返回 HTTP 200。
- 2026-07-12 复核 GitHub API：`google-research/camel-prompt-injection` 为 public、Apache-2.0、default branch `main`、archived false、created `2025-05-13T13:29:24Z`、updated `2026-07-08T23:05:09Z`、pushed `2025-06-20T13:59:30Z`。
- 2026-07-12 抓取 raw README 成功；README 说明这是 paper `Defeating Prompt Injections by Design` 的代码，并给出 AgentDojo 运行命令 `uv run --env-file .env main.py MODEL_NAME ...`。
- README warning 明确说明该代码是用于复现论文结果的 research artifact，interpreter implementation likely contains bugs，implementation might not be fully secure，不是 Google product，也不计划支持或维护。
- 2026-07-12 抽样复核 repository contents：根目录包含 `main.py`、`src`、`tests`、`uv.lock`、`analysis.ipynb` 和 `pyproject.toml`。
- 2026-07-12 抽样复核 `main.py`：代码使用 AgentDojo `benchmark_suite_with_injections` / `benchmark_suite_without_injections`，默认 suites 包含 `workspace`、`banking`、`travel`、`slack`，并输出 utility / security 结果。
- 2026-07-12 抽样复核 `src/camel/models.py`：代码包含 `+camel`、`+camel+secpol`、`+camel+secpol+strict` model suffixes，suite-specific `WorkspaceSecurityPolicyEngine` / `TravelSecurityPolicyEngine` / `BankingSecurityPolicyEngine` / `SlackSecurityPolicyEngine`，以及 original / replay-with-policies / CaMeL pipeline 分支。
- 已与 Indirect Prompt Injection paper、AgentDojo、OWASP LLM Top 10、MITRE ATLAS、Microsoft Prompt Shields、Anthropic mitigation docs 和本手册 prompt injection / permission harness 交叉验证；CaMeL 主要补强“从架构上分离可信控制流和非可信数据流”的设计边界，不替代真实防护实验。

## 可能的问题

- 论文和代码来自研究团队，可信度高，但效果数字只属于论文和 AgentDojo 设置，不能外推为当前模型、当前 API 或生产环境安全性。
- GitHub README 明确代码可能有 bug、可能不 fully secure，并且不是受支持产品；不能把它写成生产可用的 Google 安全框架。
- 本项目没有运行 CaMeL，也没有复现 77% / 84% 数字、provable security 条件、utility tradeoff、成本、延迟或模型覆盖。
- CaMeL 的 capability / security policy 设计可作为架构参考，但实际系统仍需要权限模型、审计、HITL、sandbox、数据保留治理和 red-team regression set。

## 初学者阅读建议

- 先读摘要，抓住一个核心：外部内容不应该有机会改变程序流程。
- 再把 CaMeL 和 AgentDojo 一起读：AgentDojo 提供安全评测形状，CaMeL 提供一种研究型架构防护思路。
- 不要先记论文分数；更重要的是理解 control flow、data flow、capability 和 policy enforcement 这些词对应的工程问题。

## 可复现实验

- 选择 AgentDojo 的一个小 suite，对比 original、prompt-only defense、tool filtering、CaMeL / policy replay，并记录 utility、security、false positives、false negatives、tool trace、成本和延迟。
- 在本手册 Real Prompt Injection / Permission harness 中增加一个 deterministic capability-flow fixture：非可信 tool output 只能作为数据进入后续计算，不能改变写工具调用；private data 只能流向授权工具。

## 是否进入正文

- 结论：部分进入；安全架构边界可入正文
- 原因：它可与 AgentDojo、Indirect Prompt Injection、OWASP、MITRE、Microsoft Prompt Shields、Anthropic mitigation docs 和本地实验共同支撑“prompt injection 防护不能只靠 prompt，应把可信控制流、非可信数据流、工具能力和安全策略分开建模”的窄结论。它不能支撑 CaMeL 代码或任意 capability-based 方案在生产中默认安全、默认低成本、默认低延迟或默认优于其他防护。
