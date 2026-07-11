# Evidence Note: 框架生态定位边界

## 要验证的结论

Agent 框架应按任务核心难点来比较，而不是按流行度排名。OpenAI Agents SDK 更偏轻量 agent runtime、tool loop、guardrails、handoffs、sessions 和 tracing；LangGraph 更偏低层 orchestration runtime、状态图、durable execution 和 human-in-the-loop；LlamaIndex 更偏数据接入、RAG、index/retriever/query engine；AutoGen 和 CrewAI 更偏多 Agent 协作和团队抽象；Semantic Kernel 更偏企业应用中的模型、插件、函数、OpenAPI/MCP 集成、agent framework 和业务流程编排。框架文档能支撑能力边界，但不能证明某个框架默认最优。

## 资料来源

- Source 1：[OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- Source 2：[LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- Source 3：[LlamaIndex Documentation](../sources/source-cards/2026-llamaindex-docs.md)
- Source 4：[Microsoft AutoGen Documentation](../sources/source-cards/2026-autogen-docs.md)
- Source 5：[CrewAI Documentation](../sources/source-cards/2026-crewai-docs.md)
- Source 6：[Microsoft Semantic Kernel Documentation](../sources/source-cards/2026-semantic-kernel-docs.md)
- Source 7：[Evidence Note: Agent 与 Workflow 边界](agent-workflow-boundary.md)
- Source 8：[Evidence Note: 多 Agent 不是默认更好](multi-agent-default-boundary.md)

## 交叉验证结果

- 一致点：OpenAI Agents SDK 文档支持 managed agent loop、tool execution、guardrails、handoffs、sessions 和 tracing；它适合作为理解轻量 SDK runtime 的入口。
- 一致点：LangGraph 文档把自己定位为 low-level orchestration framework and runtime，支持 long-running, stateful workflow or agent、durable execution、persistence、human-in-the-loop 和 trace/debug。
- 一致点：LlamaIndex 文档支持 context augmentation、RAG 五阶段、Documents / Nodes、Indexes、Retrievers 和 Query Engines；它适合作为 data/RAG framework 参考。
- 一致点：AutoGen 文档支持 AgentChat、Teams、Selector Group Chat、Swarm、GraphFlow、logging/tracing 等多 Agent 协调抽象。
- 一致点：CrewAI 文档支持 Flows / Crews 的组合：Flow 管理状态和执行控制，Crew 在 Flow 内协作完成特定复杂任务。
- 一致点：Semantic Kernel 文档支持企业集成定位：lightweight open-source development kit、middleware、plugins/functions、native/OpenAPI/MCP plugin 导入、agent framework、human-agent collaboration 和 process orchestration。
- 边界：Semantic Kernel Process Framework 当前标注 experimental；CrewAI source card 可信度为 B；框架文档通常强调能力和产品定位，不等于严格对照实验。
- 交叉结论：框架选择应从控制流、状态、工具、RAG/memory、多 Agent、observability、权限/审批和部署治理等维度比较，而不是直接给出“最佳框架”。

## 实验验证

- 是否需要实验：是
- 实验设计：用同一个“检索资料、调用只读工具、生成带来源答案、必要时请求人工确认”的小任务分别用 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen/CrewAI 和 Semantic Kernel 实现。比较实现时间、工具 schema、状态恢复、trace 可读性、人工确认、错误处理、成本和依赖复杂度。
- 结果：待执行

## 结论状态

- 部分验证：各框架官方文档或框架文档已支撑各自定位和能力边界；仍缺同一任务的横向实验和更细的 observability / permission 对比。

## 可进入章节

- 是。可以写成：初学者不要先问“哪个框架最好”，而要先判断任务主要难点是 tool loop、状态编排、RAG、multi-agent 协作还是企业集成。框架定位可以进入正文，但框架优劣排序必须等待同任务实验。
