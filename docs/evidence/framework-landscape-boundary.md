# Evidence Note: 框架生态定位边界

## 要验证的结论

Agent 框架应按任务核心难点来比较，而不是按流行度排名。OpenAI Agents SDK 更偏轻量 agent runtime、tool loop、guardrails、handoffs、sessions 和 tracing；smolagents 适合观察 code action、structured tool calling、local code execution、sandbox 和 Hub/MCP tool trust boundary；LangGraph 更偏低层 orchestration runtime、状态图、durable execution 和 human-in-the-loop；LlamaIndex 更偏数据接入、RAG、index/retriever/query engine；AutoGen 和 CrewAI 更偏多 Agent 协作和团队抽象；Semantic Kernel 更偏企业应用中的模型、插件、函数、OpenAPI/MCP 集成、agent framework 和业务流程编排。框架文档能支撑能力边界，但不能证明某个框架默认最优。

## 资料来源

- Source 1：[OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)
- Source 2：[LangGraph Documentation](../sources/source-cards/2026-langgraph-docs.md)
- Source 3：[LlamaIndex Documentation](../sources/source-cards/2026-llamaindex-docs.md)
- Source 4：[Microsoft AutoGen Documentation](../sources/source-cards/2026-autogen-docs.md)
- Source 5：[CrewAI Documentation](../sources/source-cards/2026-crewai-docs.md)
- Source 6：[Microsoft Semantic Kernel Documentation](../sources/source-cards/2026-semantic-kernel-docs.md)
- Source 7：[Hugging Face smolagents Documentation and Source](../sources/source-cards/2026-smolagents-docs.md)
- Source 8：[Evidence Note: Agent 与 Workflow 边界](agent-workflow-boundary.md)
- Source 9：[Evidence Note: 多 Agent 不是默认更好](multi-agent-default-boundary.md)
- Source 10：[框架选择 Rubric Smoke Test 结果](../experiments/framework-selection-rubric/results-2026-07-11.md)
- Source 11：[Evidence Note: 框架能力交叉表与选择边界](framework-capability-crosswalk.md)
- Source 12：[Building effective agents](../sources/source-cards/2024-anthropic-building-effective-agents.md)

## 交叉验证结果

- 一致点：OpenAI Agents SDK 文档支持 managed agent loop、tool execution、guardrails、handoffs、sessions 和 tracing；它适合作为理解轻量 SDK runtime 的入口。2026-07-12 复核补强了 guardrail / approval / tracing 覆盖边界：tool guardrails 只覆盖 `function_tool`，hosted shell approval 和 serialized RunState 治理需要单独处理。
- 一致点：LangGraph 文档把自己定位为 low-level orchestration framework and runtime，支持 long-running, stateful workflow or agent、durable execution、persistence、human-in-the-loop 和 trace/debug。
- 一致点：LlamaIndex 文档支持 context augmentation、RAG 五阶段、Documents / Nodes、Indexes、Retrievers 和 Query Engines；它适合作为 data/RAG framework 参考。
- 一致点：AutoGen 文档支持 AgentChat、Teams、Selector Group Chat、Swarm、GraphFlow、logging/tracing 等多 Agent 协调抽象。
- 一致点：CrewAI 文档支持 Flows / Crews 的组合：Flow 管理状态和执行控制，Crew 在 Flow 内协作完成特定复杂任务。
- 一致点：Semantic Kernel 文档支持企业集成定位：lightweight open-source development kit、middleware、plugins/functions、native/OpenAPI/MCP plugin 导入、task automation function invocation filter、agent framework、human-agent collaboration 和 process orchestration。
- 一致点：smolagents 文档支持 `CodeAgent` / `ToolCallingAgent` 的范式对照：code action 提高组合表达能力但扩大本地代码执行风险；structured tool calling 更接近 JSON/text tool-call 范式但表达能力受限。其 Secure Code Execution / README 明确 `LocalPythonExecutor` 不是完整安全边界，Hub/MCP tools 和 `trust_remote_code=True` 是信任边界。
- 一致点：Anthropic `Building effective agents` 指出 frameworks 可以简化 LLM 调用、tool definition 和 chain 编排，但也可能遮蔽 prompts / responses、增加 debugging 难度，并诱导不必要复杂度。这补强“框架是任务和调试边界的选择，不是默认升级路径”的正文表述。
- 边界：Semantic Kernel Process Framework 当前入口是 `frameworks/process/process-framework`，旧 `frameworks/process/` 路径已返回 404；Process Framework 仍标注 experimental，只能作方向性参考。CrewAI source card 可信度为 B；smolagents API reference 明确 experimental and subject to change；框架文档通常强调能力和产品定位，不等于严格对照实验。
- 边界：Anthropic 文章是工程博客，不是框架横向评测；它能支撑 abstraction caveat 和 simple-first 原则，不能证明裸 API、轻框架或复杂框架在真实任务中更可靠。
- 交叉结论：框架选择应从控制流、状态、工具、RAG/memory、多 Agent、observability、权限/审批和部署治理等维度比较，而不是直接给出“最佳框架”。
- 交叉结论：框架能力交叉表把 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI 和 Semantic Kernel 映射到不同主轴，并明确每个框架“不应误读为”的边界；这支持正文中使用定位表，而不是排行榜。
- 本地实验：标准库 rubric smoke test 用 5 个任务画像比较 required、nice-to-have、avoid、missing required 和 cautions。结果分别把最小 tool agent、RAG QA、审批 workflow、多角色 review 和企业插件集成映射到不同框架方向，并且所有任务都保留 `needs_real_experiment=true`。这支持“rubric 可用于学习和预筛选，但不能替代真实横向实验”。

## 实验验证

- 是否需要实验：是
- 实验设计：先用标准库 rubric smoke test 验证任务画像和能力标签；再用同一个“检索资料、调用只读工具、生成带来源答案、必要时请求人工确认”的小任务分别用 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen/CrewAI 和 Semantic Kernel 实现。比较实现时间、工具 schema、状态恢复、trace 可读性、人工确认、错误处理、成本和依赖复杂度。
- 结果：已完成标准库 rubric smoke test；真实框架横向实验待执行。

## 结论状态

- 可入正文：窄结论“Agent 框架应按任务难点和能力边界比较，不应写成某个框架默认最好”已完成第一轮交叉验证。OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen、CrewAI 和 Semantic Kernel 文档分别支撑轻量 runtime、状态编排、RAG/data、多 Agent 协作和企业集成等不同主轴；Anthropic `Building effective agents` 补强框架抽象会简化调用/编排但也可能遮蔽 prompts / responses、增加调试难度和诱导复杂度的 caveat；框架能力交叉表和标准库 rubric smoke test 支撑 required / nice-to-have / avoid / missing required / cautions 的任务画像式比较方法。OpenAI Agents SDK 2026-07-12 复核进一步说明，即使同一框架内也要区分 function-tool guardrail、hosted/built-in 工具、HITL approval、trace sensitive-data 和 serialized state 的覆盖边界；Semantic Kernel 2026-07-12 复核进一步说明，即使同一框架内也要区分 plugins/functions、task automation filters、Agent Framework 和 experimental Process Framework。
- 部分验证：同一任务的真实框架横向实验、更细的 observability / permission / HITL / RAG citation / tool error recovery / sandbox isolation / Hub-MCP trust review 对比、实现成本、维护成本、latency 和 token cost 仍待实测；不能写成任何框架真实更快、更便宜、更可靠或默认适合初学者。

## 可进入章节

- 是。可以确定写成：初学者不要先问“哪个框架最好”，而要先判断任务主要难点是 tool loop、状态编排、RAG、multi-agent 协作还是企业集成。框架定位和选型维度可以进入正文；框架优劣排序、真实成本和可靠性必须等待同任务实验。
