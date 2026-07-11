# LangGraph Documentation

- 来源链接：https://docs.langchain.com/oss/python/langgraph/overview
- 作者 / 机构：LangChain
- 发布时间：持续更新文档；旧入口 `https://langchain-ai.github.io/langgraph/` 已重定向到 docs.langchain.com
- 最后复核日期：2026-07-11
- 类型：框架文档
- 主题：Agent Architecture / State Graph / Orchestration
- 适合阶段：进阶 / 工程实践
- 可信度等级：A
- 是否已验证：新文档入口和 Markdown 页面已复核；关键段落已精读；Agent/Workflow、自治程度、复杂架构默认可靠性、Planner/Executor trace 和跨框架术语对照窄边界可入正文；真实 LangGraph 行为仍部分验证

## 一句话总结

LangGraph 是理解状态图、可控 workflow-agent hybrid 和复杂任务编排的重要工程 reference。

## 核心结论

- LangGraph 文档将其定位为 low-level orchestration framework and runtime，用于 building、managing、deploying long-running, stateful agents。
- 文档明确 LangGraph focused entirely on agent orchestration，不抽象 prompts 或 architecture。
- 文档把 LangGraph 描述为支持 any long-running, stateful workflow or agent 的低层基础设施。
- 核心能力包括 durable execution、streaming、human-in-the-loop、persistence、memory 和 trace/debug 支持。
- 文档建议刚开始学习或需要更高层抽象时使用 LangChain agents；这支持正文中“不要一开始就追求复杂底层编排”的保守建议。
- 当前 quickstart 展示 Graph API 和 Functional API 两条入门路径；Graph API 通过 `StateGraph`、state、model node、tool node、conditional edge、compile 和 invoke 组织工具循环。

## 支撑证据

- 新文档入口和 `.md` 页面返回 HTTP 200；旧 GitHub Pages 入口返回重定向页面。
- Markdown 页面写明 LangGraph 是 low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents。
- Markdown 页面写明 LangGraph provides low-level supporting infrastructure for any long-running, stateful workflow or agent。
- Markdown 页面写明 LangGraph does not abstract prompts or architecture。
- Markdown 页面列出 persistence、human-in-the-loop、memory、debugging/trace execution paths、state transitions 等核心收益。
- Quickstart Markdown 返回 HTTP 200，并展示 calculator agent 的 tools、`MessagesState`、conditional edge 和 tool node；它可作为当前代码入口。
- LangGraph examples repo 已另建 source card；该 repo 的 `examples/README.md` 明确说明 examples 目录已经归档，不再更新，应优先使用当前 docs。

## 可能的问题

- LangGraph 属于特定框架，不能把它的抽象直接当成所有 Agent 系统的通用定义。
- 需要和 OpenAI Agents SDK、AutoGen、Semantic Kernel 等框架比较。
- LangGraph 更偏底层 orchestration runtime；初学者需要先理解 model、tool、state 和 workflow，再读复杂 API。
- 需要区分当前 docs / quickstart 与归档 examples；旧 notebooks 可帮助理解架构形态，但不能作为最新 API 指南。

## 初学者阅读建议

- 先理解 workflow、state、edge、node 的直觉，再看复杂多 agent 示例。

## 可复现实验

- 构建一个带状态持久化的两步 tool workflow，对比无状态单 Agent 的可调试性。
- 已纳入框架能力交叉表，用于支撑“state graph / durable execution / persistence / HITL / trace”的保守定位；与其他框架卡片和 rubric smoke test 共同支撑“框架应按任务难点比较，不能写成某个框架默认最好”的窄边界；不代表真实横向性能结论。
- 已纳入 Tool / Function / Plugin 术语对照 evidence，用于区分 LangGraph 的 state graph、node、edge、stateful workflow / agent 和 durable execution 抽象与 API 层 function/tool calling、RAG retriever 或多 Agent team 抽象；不代表真实 LangGraph 默认工具错误处理或权限行为。
- Agent/Workflow 和自治程度窄边界已升级为可入正文：LangGraph 文档直接支撑 long-running, stateful workflow or agent、orchestration runtime、state transitions 和 trace/debug execution paths 的工程边界。真实 LangGraph workflow / agent 表现、成本和失败恢复仍需实验。
- 复杂架构默认可靠性窄边界已升级为可入正文：LangGraph 支撑 durable execution、state、trace/debug 等工程控制能力，但这些能力是选择和验证架构的依据，不证明状态图、Agent 或更复杂编排在真实任务中默认更可靠。
- Planner/Executor 窄边界已升级为可入正文：LangGraph 支撑状态、转移、持久化和 trace/debug 的工程编排边界；标准库 planner/executor 实验补充了 validation_failed / plan_revised 的最小流程。真实 LangGraph planner/executor 实现仍需实验。
- 已补 LangGraph examples repo source card：current quickstart 补强 `StateGraph` tool loop 的代码形态，历史 plan-and-execute / human-in-the-loop notebooks 补强 planner/replan 和 interrupt/resume 的架构参考；但 examples 目录已归档，真实试跑应使用当前 docs。

## 是否进入正文

- 结论：部分进入
- 原因：可支撑 stateful workflow/agent、orchestration runtime、persistence、human-in-the-loop、trace 和跨框架术语区分的工程边界，并与 OpenAI Agents SDK/ReAct/标准库实验共同支撑 Agent/Workflow、自治程度、复杂架构默认可靠性和 Planner/Executor trace 窄边界；不能单独证明任何复杂 Agent 架构默认更好。
