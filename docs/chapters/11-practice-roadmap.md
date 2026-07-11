# 实践项目路线

## 本章适合谁

如果你已经读完前面的概念章节，但不知道如何动手练习，这一章适合阅读。

本章把学习拆成一组逐步升级的小项目。每个项目都应该能独立完成、独立验证，并且对应前面章节的概念。

## 你会学到什么

- 如何从最小 LLM 应用逐步走到 Agent。
- 每个阶段应该练习什么能力。
- 如何给练习项目设置验收标准。
- 为什么实践项目也要记录 references、trace 和失败样例。
- 如何避免一开始就做过大的“全能 Agent”。

## 先用一句话理解

学习 Agent 最稳的路线是：先做小而可测的工具调用，再逐步加入 RAG、memory、编排、eval 和生产化边界。

本手册的实践路线 smoke harness 把部分项目验收标准转成了 6 条可运行 eval cases：结构化输出、refusal 记录、工具参数校验、RAG 引用、资料不足拒答和成本预算阻断。它不调用真实模型，也不能替代 Cookbook/API 试跑，但可以作为初学者理解“项目要可测、可复盘、可失败分类”的起点。

## 项目 1：最小问答应用

### 学习目标

理解模型输入、输出、system instruction、用户消息和结构化输出。

### 任务描述

构建一个简单问答程序：用户输入问题，模型返回简洁回答，并用固定 JSON 格式输出答案和置信说明。

### 验收标准

- 能运行最小请求。
- 能记录输入和输出。
- 输出格式稳定，失败时能被检测。
- 至少准备 5 条测试问题。

### 关联章节

- [LLM 基础与上下文工程](02-llm-context.md)

### 可参考 recipe

- OpenAI Cookbook 的 `Introduction to Structured Outputs`，尤其是 math tutor、summarization、entity extraction 和 refusal 小节。

## 项目 2：最小 Tool Calling Agent

### 学习目标

理解工具 schema、参数生成、应用层执行工具和工具结果回传。

### 任务描述

给模型提供一个计算器或天气查询 mock 工具。模型需要决定是否调用工具，并用工具结果回答问题。

### 验收标准

- 工具参数有 schema。
- 应用层负责执行工具，模型本身不直接执行。
- 参数错误时能返回错误并重试或失败退出。
- 记录每次工具调用的参数和结果。

### 关联章节

- [Tool Use、Function Calling 与 Structured Output](03-tool-use.md)

### 可参考资料

- OpenAI Function Calling / Tool Calling docs。
- OpenAI Cookbook 的 `Introduction to Structured Outputs` 中 function call usage 和 entity extraction 示例。

## 项目 3：带来源的 RAG 问答

### 学习目标

理解 document、chunk、embedding、retrieval、reranking、provenance 和引用。

### 任务描述

准备一小批 Markdown 文档，让系统根据文档回答问题，并输出引用来源。

### 验收标准

- 能说明 chunking 规则。
- 能看到检索到的 top-k 文档片段。
- 答案必须带来源。
- 如果资料不足，系统应该说不知道，而不是编造。
- 准备 10 条检索测试问题，并记录失败原因。

### 关联章节

- [RAG、Memory 与知识库治理](06-rag-memory.md)

### 可参考 recipe

- OpenAI Cookbook 的 `Doing RAG on PDFs using File Search in the Responses API`。它适合作为 PDF/RAG 入门练习参考，也包含 retrieval evaluation 的例子。

## 项目 4：短期状态与长期记忆

### 学习目标

区分 conversation state、short-term memory、long-term memory 和知识库。

### 任务描述

做一个学习助手。它能记住当前会话目标，也能在用户明确确认后写入长期偏好。

### 验收标准

- 当前会话状态和长期记忆分开存储。
- 长期记忆写入需要明确触发或确认。
- 用户能查看和删除记忆。
- 过时或冲突记忆有处理规则。

### 关联章节

- [RAG、Memory 与知识库治理](06-rag-memory.md)

## 项目 5：可恢复的多步骤 Workflow

### 学习目标

理解任务拆解、状态、重试、人工确认和失败恢复。

### 任务描述

构建一个“资料整理助手”：输入主题，系统生成搜索计划、读取资料卡片、输出摘要草稿，并在进入正文前要求确认。

### 验收标准

- 每一步有明确输入和输出。
- 中断后可以从状态恢复。
- 高风险结论需要标记为待验证。
- 工具失败时不会编造结果。

### 关联章节

- [Agent 架构模式](04-agent-architecture.md)
- [Planning、Orchestration 与多 Agent](07-planning-orchestration.md)

## 项目 6：MCP 工具接入实验

### 学习目标

理解 MCP server、client、host、tools、resources 和权限边界。

### 任务描述

接入一个简单 MCP server，例如只读文件或 mock 数据查询工具，让 Agent 通过 MCP 获取上下文或调用工具。

### 验收标准

- 能说明 host、client、server 的职责。
- 工具权限是最小化的。
- 只读和写操作分开。
- trace 中能看到 MCP 工具调用。

### 关联章节

- [MCP 与工具生态](05-mcp.md)

## 项目 7：小型 Agent Eval

### 学习目标

理解 regression set、trace、trajectory、错误分类和版本对比。

### 任务描述

为前面的 tool-calling 或 RAG Agent 建立 20 条测试任务。每条任务记录预期行为、实际 trace、是否成功和失败分类。

### 验收标准

- 至少 20 条任务。
- 每条任务有成功标准。
- 能区分需求理解、检索、工具参数、权限、恢复和输出错误。
- 每次改 prompt、工具或模型后能重新运行测试。

### 关联章节

- [Evaluation 与 Observability](08-evaluation-observability.md)

### 可参考 recipe

- OpenAI Cookbook 的 `Getting Started with OpenAI Evals`。
- OpenAI Cookbook 的 `Evaluating Agents with Langfuse`，用于理解 trace、online evaluation、offline evaluation 和 dataset evaluation 的工程形态。

## 项目 8：生产化前检查

### 学习目标

理解权限、审计、成本、延迟、降级和回滚。

### 任务描述

选择一个前面项目，加入生产化前检查：只读模式、写操作确认、成本记录、错误日志、禁用工具开关和回滚方案。

### 验收标准

- 高风险工具默认关闭或需要确认。
- trace 脱敏后可用于调试。
- 成本和延迟有记录。
- 有降级路径和人工接管方式。
- 有安全类 regression cases。

安全 regression cases 不应只写“有一个 prompt injection 测试”。更实用的最小集合应同时包含：外部文档注入、跨用户数据访问、高金额写操作、敏感字段外泄、破坏性工具、重复提交和一个正常请求。每条 case 都应记录预期行为、实际行为、是否误报、是否漏报和 trace 是否泄露敏感字段。

### 关联章节

- [Production：安全、权限、成本与部署](09-production-security.md)

### 可参考 recipe

- OpenAI Cookbook 的 `How to use the Usage API and Cost API to monitor your OpenAI usage`。
- OpenAI Cookbook 的 `How to handle rate limits`。

## 进阶项目：Repo Issue Agent

### 学习目标

理解软件工程 Agent 为什么需要仓库导航、文件编辑、测试执行、sandbox、回滚和更严格的 trace。

### 任务描述

准备一个 toy repo，放入一个带测试的简单 bug。让 Agent 读取 issue、定位相关文件、提出 patch、运行测试，并输出改动说明。

### 验收标准

- 在隔离目录或 sandbox 中运行，不直接操作重要仓库。
- 读文件、写文件和执行命令的权限分开记录。
- 每次文件修改都能 diff 和回滚。
- 测试失败时不能编造通过结果。
- 记录 token、耗时、命令、测试输出和人工确认点。

### 可参考资料

- SWE-agent 论文和 README。它适合理解 agent-computer interface、仓库导航、代码编辑和测试执行；但 README 已提示当前推荐 mini-SWE-agent，因此真实试跑前需要复核当前文档。

## 进阶项目：Browser / Computer Use Agent

### 学习目标

理解网页和桌面动作为什么需要隔离环境、动作 trace、权限确认和失败分类。

### 任务描述

准备一个本地 demo page，让 Agent 完成只读信息提取、表单填写但不提交、需要确认后提交和文件上传。先用固定 Playwright workflow 实现，再对比 Browser Use 或 computer-use-style action loop。

### 验收标准

- 使用测试账号、隔离 profile 或 VM/container，不接触真实重要账号。
- 每个 click、type、upload、submit 都有 action log 或 trace。
- 提交、购物、付款、同意条款、删除、发送消息等动作必须人工确认。
- 外部网页文本、截图/OCR 文本和工具结果都按不可信数据处理。
- 记录 DOM/screenshot state、失败原因、成本、延迟和敏感字段脱敏。

### 可参考资料

- Browser Use / Playwright source card 用于理解浏览器动作和 trace。
- Anthropic Computer Use source card 用于理解 screenshot/mouse/keyboard control、VM/container 隔离、domain allowlist、action validation/logging 和 beta limitation。

## 进阶项目：Browser Agent

### 学习目标

理解浏览器 Agent 为什么比普通只读问答风险更高：它会触达网页动作、页面状态、登录态、profile、表单、文件上传、提交按钮和第三方站点边界。

### 任务描述

先做一个本地 demo website，包含只读信息页、普通表单、文件上传控件、需要确认的提交按钮和一个 destructive button。然后用两种方式完成同一任务：固定 Playwright workflow，以及 Browser Use 或同类 browser agent 的自然语言任务。

### 验收标准

- 只能使用测试账号、隔离 browser profile 或本地 demo site，不使用真实购物、付款、投递或重要账号。
- 记录访问 URL、点击元素、输入字段、上传文件、提交动作、页面状态和失败原因。
- 表单提交、购物、支付、发送消息、文件上传和 destructive button 都必须有人工确认点。
- 对比固定 Playwright workflow 和 browser agent 的成功率、步骤数、失败原因、成本、延迟和 trace 可读性。
- 不把 CAPTCHA / stealth / 网站 ToS / 账号风控 / 生产可靠性写成已验证结论，除非后续真实实验覆盖这些问题。

### 可参考资料

- Browser Use README 和 docs。它适合理解 browser agent 的任务形态、custom tools、profile/auth 和 human-in-the-loop 等产品能力边界。
- Playwright actions 和 trace viewer 文档。它适合理解浏览器动作层和按 action 回放 trace 的工程基础。

## 推荐学习顺序

1. 先完成项目 1 和 2，理解模型调用和工具调用。
2. 再完成项目 3，建立 RAG 和引用意识。
3. 然后完成项目 4 和 5，学习状态、记忆和编排。
4. 如果需要工具生态，再做项目 6。
5. 最后做项目 7 和 8，把质量和生产化边界补上。
6. 如果你想练软件工程 Agent，再做 Repo Issue Agent；它比前面项目风险更高，必须先用 toy repo 和隔离环境。
7. 如果你想练 Browser Agent，把它放在 Repo Issue Agent 之后或同级进阶阶段，只用 demo site、测试账号、隔离 profile 和人工确认来练习。

## 常见误区

- 误区一：第一个项目就做全能 Agent。范围越大，越难知道哪里错了。
- 误区二：只看 demo，不写测试。Agent 的失败往往出现在边界情况。
- 误区三：练习时不记录 trace。没有 trace 就无法复盘。
- 误区四：先接很多工具。工具越多，权限和错误处理越复杂。
- 误区五：只追求功能，不做 eval。没有 eval 的功能很难持续改进。

## 已验证结论

- “OpenAI Cookbook 的具体 recipe 可以作为初学者实践项目参考，但不能替代 API 文档、生产安全指南或本地实验”已升级为可入正文。正文应引用具体 recipe，而不是笼统引用整个站点；Cookbook 是示例集合，不是 API 规范或生产保证。
- 当前已复核的 Cookbook recipe 可以支撑以下练习方向：Structured Outputs、File Search RAG、OpenAI Evals、Agents SDK trace/eval、Usage/Cost 和 Rate limits。
- OpenAI Function Calling docs 和 Responses API docs 可支撑最小工具调用和 API 结构练习；具体 API 细节需要按当前文档复核。
- MCP servers repo 可作为 MCP 工具生态示例来源，但具体 server 的权限和安全假设需要逐个检查。
- OpenAI Evals repo 可作为小型回归测试和 eval 结构参考；Agent eval 仍应结合 trace 和业务任务。
- SWE-agent 论文和 README 可作为 repo issue / coding agent 进阶练习参考：它支撑 agent-computer interface、仓库导航、文件编辑和测试执行的重要性；README 已提示当前推荐 mini-SWE-agent，真实试跑仍需复核当前文档、sandbox、权限和成本。
- Browser Use / Playwright / Anthropic Computer Use source cards 可作为 Browser / Computer Use Agent 进阶练习参考：它们支撑浏览器动作、profile/auth 风险、custom tools、screenshot/mouse/keyboard control、VM/container 隔离、action validation/logging 和 trace viewer 的工程边界；真实 browser/computer-use agent 任务成功率、点击精度、classifier 行为、成本、延迟、CAPTCHA/stealth、合规和生产可靠性仍待实验。
- 实践路线 smoke harness 已完成标准库试跑，支持“每个项目都要有验收标准、trace、失败分类和可重复运行命令”的学习建议；仍不能替代真实 Structured Outputs、File Search/RAG、OpenAI Evals、Agents SDK trace/eval、Usage/Cost 和 Rate limits 试跑。
- 安全 regression set 最小实验已完成标准库试跑，支持“生产化练习需要覆盖多类安全 case，并记录误报、漏报和 trace 泄漏”的学习建议；仍不能替代真实模型 / 框架 guardrail / HITL approval 试跑。

## 待验证问题

- 这些 Cookbook recipe 真实本地试跑时的依赖、成本、失败样例和初学者阻塞点是什么？
- 每个项目应使用哪个最小技术栈，才能降低环境成本？
- 如何为项目 7 设计可自动运行的 eval harness？
- MCP 实验应选择哪个只读 server 作为最小示例？
- 如何把这些项目逐步发布成 GitHub Pages 的可跟练教程？
- 如何把安全 regression set 迁移到真实 tool-calling / Agents SDK / MCP 工具练习？
- Repo Issue Agent 应优先用 SWE-agent、mini-SWE-agent、OpenAI Agents SDK、LangGraph 还是固定 workflow 做最小对比？成本、sandbox、回滚和测试反馈如何记录？
- 固定 Playwright workflow 与 Browser Use / browser agent 在同一 demo site 上的成功率、步骤数、失败原因、成本、延迟、trace 可读性和审批负担有什么差异？

## 本章小结

- 实践路线应该由小到大，由可测到复杂。
- 最小工具调用、RAG、memory、workflow、MCP、eval 和生产化检查应逐步加入。
- 每个项目都要有验收标准、trace 和失败分类。
- 初学者不要一开始追求全能 Agent，先建立可复现的学习闭环。

## References

### Official Docs, Examples and Practice Sources

- [OpenAI Responses API Reference](../sources/source-cards/2026-openai-responses-api-docs.md)
- [OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- [OpenAI Cookbook](../sources/source-cards/2026-openai-cookbook.md)
- [MCP servers repo](../sources/source-cards/2026-mcp-servers-repo.md)
- [OpenAI Evals Repository](../sources/source-cards/2026-openai-evals-repo.md)
- [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](../sources/source-cards/2024-swe-agent-paper.md)
- [Browser Use and Playwright Browser Automation References](../sources/source-cards/2026-browser-use-playwright.md)
- [Evidence Note: 实践路线与 Cookbook 示例边界](../evidence/practice-roadmap-cookbook-boundary.md)
- [Evidence Note: Browser Agent 与网页自动化边界](../evidence/browser-agent-boundary.md)
- [实践路线 Smoke Harness 结果](../experiments/practice-roadmap-harness/results-2026-07-11.md)

### Governance

- [结论证据台账](../evidence/claim-ledger.md)
- [实验说明](../experiments/README.md)
