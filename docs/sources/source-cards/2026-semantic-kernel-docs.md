# Microsoft Semantic Kernel Documentation

- 来源链接：https://learn.microsoft.com/en-us/semantic-kernel/overview/
- 作者 / 机构：Microsoft
- 发布时间：持续更新文档；页面 last-modified 复核为 2025-08-27
- 最后复核日期：2026-07-11
- 类型：框架文档
- 主题：Agent Framework / Orchestration / Enterprise Integration
- 适合阶段：进阶 / 工程实践
- 可信度等级：A
- 是否已验证：overview、Agent Framework、Plugins 和 Process Framework 页面已复核；框架生态边界已完成第一轮交叉验证

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
- Process Framework 页面说明其用于 automating complex workflows，步骤通过 user-defined Kernel Functions 执行，并用 event-driven model 管理 workflow execution；该 package 当前 experimental，仍可能变化。

## 支撑证据

- Microsoft Learn 页面返回 HTTP 200。
- 2026-07-11 抓取 `https://learn.microsoft.com/en-us/semantic-kernel/overview/?accept=text/markdown` 成功；页面包含 middleware、enterprise-grade、telemetry、hooks/filters、plugins 和 OpenAPI 等关键内容。
- 2026-07-11 抓取 Agent Framework、Plugins 和 Process Framework Markdown 成功；页面包含 agents、human input、multi-agent collaboration、process orchestration、function calling、native/OpenAPI/MCP plugins、human-in-the-loop approval 和 experimental Process Framework 等关键内容。
- 已与 OpenAI Agents SDK、LangGraph、AutoGen、CrewAI、MCP、Tool Calling 和 Multi-agent evidence 完成第一轮交叉验证。

## 可能的问题

- 它的术语和抽象受 Microsoft 生态影响，需要和其他框架对照。
- 初学者正文应避免过早引入企业集成复杂度。
- Process Framework 文档明确标注当前 package experimental，因此正文只能把它作为方向性参考，不能写成稳定通用能力。
- Plugins 文档包含产品定位和企业生态表述，应重点引用 function calling、native/OpenAPI/MCP plugins、human-in-the-loop approval 等工程边界，不引用“更快/更强”等营销式表述。

## 初学者阅读建议

- 把它放在框架比较章节阅读，重点看它如何组织工具、插件和 agent 抽象。

## 可复现实验

- 构建一个简单工具插件，并比较它和 OpenAI Agents SDK / LangGraph 的工具定义差异。

## 是否进入正文

- 结论：进入
- 原因：框架生态章节需要覆盖 Microsoft 官方 Agent/AI app framework；可支撑 enterprise integration、plugins/functions、agent framework、process orchestration 和 MCP/OpenAPI 集成边界。
