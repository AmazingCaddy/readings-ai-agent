# Microsoft Semantic Kernel Documentation

- 来源链接：https://learn.microsoft.com/en-us/semantic-kernel/overview/
- 作者 / 机构：Microsoft
- 发布时间：持续更新文档；overview 页面 last-modified 复核为 2025-08-27，plugins / task automation 页面 last-modified 复核为 2026-05-26
- 最后复核日期：2026-07-12
- 类型：框架文档
- 主题：Agent Framework / Orchestration / Enterprise Integration
- 适合阶段：进阶 / 工程实践
- 可信度等级：A
- 是否已验证：overview、Agent Framework、Plugins、task automation、Process Framework、experimental attribute 和 TOC 已于 2026-07-12 复核；框架生态边界和跨框架术语对照已完成第一轮交叉验证；高风险工具权限窄边界可入正文；审批状态恢复实验已完成标准库模拟；Semantic Kernel native plugin runtime 窄观察已完成；真实模型 / OpenAPI / MCP plugin / HITL UI / Process Framework 行为仍部分验证

## 一句话总结

Semantic Kernel 是理解企业应用中模型、插件、工具和编排集成的 Microsoft 官方框架 reference。

## 核心结论

- Overview 页面将 Semantic Kernel 定义为 lightweight, open-source development kit，用于构建 AI agents，并把最新 AI models 集成到 C#、Python 或 Java codebase 中；它被定位为 enterprise-grade solutions 的 middleware。
- Overview 页面强调企业场景中的 modular、observable、telemetry support、hooks and filters，以及通过 plugins 把 existing APIs 暴露给 AI models。
- Agent Framework 页面定义 AI agent 是能 autonomously 或 semi-autonomously 接收输入、处理信息并采取行动达成目标的软件实体；agent 可结合 models、tools、human inputs 和其他组件生成响应。
- Agent Framework 页面强调 modular components、multi-agent collaboration、human-agent collaboration 和 process orchestration。
- Plugins 页面说明 plugins 可封装 existing APIs，让 AI 通过 function calling 请求函数；Semantic Kernel 将请求 marshals 到应用代码并把结果返回给 LLM。
- Plugins 页面说明可通过 native code、OpenAPI specification 或 MCP Server 导入 plugins，并建议入门优先使用 native code plugins。
- Plugins 页面区分 retrieval functions 和 task automation functions；后者通常需要 human-in-the-loop approval processes。
- Task automation 页面明确写明 agent 执行动作前应请求用户同意，尤其涉及敏感数据或金融交易时；示例使用 function invocation filter 在函数调用前拦截 `create_order` 并把拒绝结果返回给 agent。
- Process Framework 当前入口是 `frameworks/process/process-framework`；页面说明其用于 automating complex workflows，步骤通过 user-defined Kernel Functions 执行，并用 event-driven model 管理 workflow execution；该 package 当前 experimental，仍可能变化。
- Experimental attribute 页面说明 experimental features 尚不稳定，可能被修改、弃用或删除，支持和文档可能有限；这强化了 Process Framework 只能作为方向性参考的边界。

## 支撑证据

- Microsoft Learn overview 页面于 2026-07-12 返回 HTTP 200；响应头 `last-modified: Wed, 27 Aug 2025 22:32:16 GMT`。
- 2026-07-12 抓取 `https://learn.microsoft.com/en-us/semantic-kernel/overview/?accept=text/markdown` 成功；frontmatter `updated_at=2024-06-24T22:09:00Z`，页面包含 middleware、enterprise-grade、telemetry、hooks/filters、plugins 和 OpenAPI 等关键内容。
- 2026-07-12 抓取 `https://learn.microsoft.com/en-us/semantic-kernel/toc.json` 成功；TOC 记录 Plugins、Text Search、Agent Framework、Agent Orchestration、Process Framework、Security 和 API Reference 等入口，并显示当前 Process Framework overview 路径是 `frameworks/process/process-framework`。
- 2026-07-12 抓取 Plugins Markdown 成功；响应头 `last-modified: Tue, 26 May 2026 13:05:38 GMT`，frontmatter `updated_at=2026-05-26T13:05:00Z`；页面包含 function calling、native/OpenAPI/MCP plugins、retrieval functions、task automation functions、import only necessary plugins、token/latency tradeoff、local state 和 return type schema 等建议。
- 2026-07-12 抓取 Agent Framework Markdown 成功；响应头 `last-modified: Wed, 27 Aug 2025 22:32:16 GMT`，frontmatter `updated_at=2025-05-23T04:36:00Z`；页面包含 autonomously / semi-autonomously、models/tools/human inputs、多 agent collaboration、human-agent collaboration、process orchestration 和 supported agent packages。
- 2026-07-12 抓取 Task Automation Markdown 成功；frontmatter `updated_at=2026-05-26T13:05:00Z`；页面说明 agent 执行动作前应请求用户同意，尤其涉及 sensitive data 或 financial transactions，并展示 function invocation filter 拦截 / 拒绝函数调用。
- 旧路径 `https://learn.microsoft.com/en-us/semantic-kernel/frameworks/process/` 于 2026-07-12 返回 HTTP 404；当前 `https://learn.microsoft.com/en-us/semantic-kernel/frameworks/process/process-framework` 返回 HTTP 200，响应头 `last-modified: Fri, 08 Nov 2024 23:10:37 GMT`，Markdown 写明 Process Framework package currently experimental and is subject to change until preview / GA。
- 2026-07-12 抓取 Experimental Attribute Markdown 成功；frontmatter `updated_at=2026-05-26T13:05:00Z`；页面说明 experimental features may be modified, deprecated, or removed，可能有 breaking changes、limited support、stability concerns 和 incomplete documentation。
- 已与 OpenAI Agents SDK、LangGraph、AutoGen、CrewAI、MCP、Tool Calling 和 Multi-agent evidence 完成第一轮交叉验证。
- 2026-07-12 运行 Real Semantic Kernel Plugin Validation：使用 Semantic Kernel Python 1.36.0、native plugin 和 `@kernel_function` 跑通 plugin/function metadata、required/type 参数处理、应用层写工具审批 wrapper、side-effect trace 和 trace 脱敏；结果 `all_passed=true`、`missing_required_rejected=true`、`invalid_type_rejected=true`、`coercible_argument_invoked=true`、`rejected_write_forwarded=false`。

## 可能的问题

- 它的术语和抽象受 Microsoft 生态影响，需要和其他框架对照。
- 初学者正文应避免过早引入企业集成复杂度。
- Process Framework 文档明确标注当前 package experimental，且旧 overview 路径已经 404；正文只能把它作为方向性参考，不能写成稳定通用能力或长期稳定入口。
- Plugins 文档包含产品定位和企业生态表述，应重点引用 function calling、native/OpenAPI/MCP plugins、human-in-the-loop approval 等工程边界，不引用“更快/更强”等营销式表述。
- 本地 native plugin run 不覆盖真实模型 tool selection、OpenAPI plugin、MCP plugin、Agent Framework、Process Framework 或 HITL UI；task automation 文档和本地 run 都支持“可实现审批拦截”这一窄边界，但高风险写操作审批仍需应用层 filter / wrapper / 状态机设计，不能写成框架默认自动保证。

## 初学者阅读建议

- 把它放在框架比较章节阅读，重点看它如何组织工具、插件和 agent 抽象。

## 可复现实验

- 已完成一个简单 native plugin runtime harness；后续仍需比较它和 OpenAI Agents SDK / LangGraph 的同任务工具定义差异。
- 将审批状态恢复与幂等性实验迁移到 Semantic Kernel plugin / process flow，观察 task automation approval、参数快照、重复恢复和拒绝恢复如何实现。
- 已纳入框架能力交叉表，用于支撑“enterprise middleware / plugins / OpenAPI / MCP / HITL / process orchestration”的保守定位；与其他框架卡片和 rubric smoke test 共同支撑“框架应按任务难点比较，不能写成某个框架默认最好”的窄边界；Process Framework experimental 边界仍保留。
- 已纳入 Tool / Function / Plugin 术语对照 evidence，用于说明 Semantic Kernel 的 plugins/functions、native/OpenAPI/MCP plugins、task automation functions 和 Process Framework 属于企业集成 / 业务流程语境，不能直接等同于 OpenAI API function tool 或其他框架的 tool 抽象。
- 已完成 Real Semantic Kernel Plugin Validation，用于补强 native plugin / kernel function metadata 和 runtime 参数处理的窄观察。

## 是否进入正文

- 结论：进入
- 原因：框架生态章节需要覆盖 Microsoft 官方 Agent/AI app framework；可支撑 enterprise integration、plugins/functions、agent framework、process orchestration、MCP/OpenAPI 集成、task automation approval 和跨框架术语区分边界。Native plugin runtime 已有本地 completed run；真实模型 function calling、OpenAPI/MCP plugin、HITL UI、参数快照和幂等恢复仍需实测。
