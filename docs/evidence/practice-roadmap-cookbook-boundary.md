# Evidence Note: 实践路线与 Cookbook 示例边界

## 要验证的结论

OpenAI Cookbook 可以支撑初学者的实践项目路线，但只能作为具体 recipe 级别的练习参考。它能帮助把结构化输出、RAG、eval、trace、成本和限流拆成可动手的小项目；它不能单独证明某个项目顺序最优，也不能替代 API 文档、生产安全指南或本地实验。

## 资料来源

- Source 1：[OpenAI Cookbook](../sources/source-cards/2026-openai-cookbook.md)
- Source 2：[OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- Source 3：[OpenAI Responses API Documentation](../sources/source-cards/2026-openai-responses-api-docs.md)
- Source 4：[OpenAI Evals Repository](../sources/source-cards/2026-openai-evals-repo.md)
- Source 5：[Evidence Note: 上下文工程与结构化输出边界](context-structured-output-boundary.md)
- Source 6：[Evidence Note: RAG 工程流程边界](rag-engineering-boundary.md)
- Source 7：[Evidence Note: Agent Eval 与 Trajectory 边界](agent-eval-trajectory-boundary.md)

## 交叉验证结果

- 一致点：Cookbook 首页定位为 notebook examples；这支持把它作为学习项目模板，而不是规范来源。
- 一致点：`Introduction to Structured Outputs` 包含 response format usage、function call usage、math tutor、summarization、entity extraction 和 refusal 小节；这能支撑项目 1 的结构化输出练习，也能连接第 02/03 章的 schema 与 refusal 边界。
- 一致点：`Doing RAG on PDFs using File Search in the Responses API` 包含 vector store、file search、LLM 整合、retrieval evaluation、Recall / Precision / MRR / MAP 等内容；这能支撑项目 3 的 RAG 练习和项目 7 的检索评测入门。
- 一致点：`Getting Started with OpenAI Evals` 包含 eval setup、dataset、running evaluation 和 eval logs；这能支撑小型 regression set 的实践路线。同时页面提示已有 hosted evals product/API，说明旧框架材料需要按当前 API 复核。
- 一致点：`Evaluating Agents with Langfuse` 明确围绕 OpenAI Agents SDK 内部步骤 trace、online evaluation、offline evaluation、dataset evaluation 和生产指标；这能支撑“trace 不只是日志，而是 eval/observability 的输入”这一练习方向。
- 一致点：`Usage API / Cost API` 和 `How to handle rate limits` 分别覆盖用量/成本监控、429/RateLimitError、exponential backoff、batching 等内容；这能支撑项目 8 的成本、限流和降级练习。
- 边界：Cookbook recipe 往往以演示为主，权限、审计、数据隔离、成本上限、部署和回滚常被简化；不能把 recipe 直接写成生产最佳实践。
- 边界：Practice roadmap 的“先结构化输出、再工具/RAG、再 eval/生产化”有资料支撑为学习顺序，但仍不是唯一正确顺序；项目难度和技术栈需要本地试跑后再细化。

## 实验验证

- 是否需要实验：是
- 实验设计：选择 3 个最小项目：Structured Outputs 问答、File Search/RAG 问答、小型 eval harness。每个项目记录依赖、运行成本、输入输出样例、trace、失败样例、初学者阻塞点和可复现命令。
- 结果：待执行

## 结论状态

- 部分验证：Cookbook 的具体 recipe 已经能支撑实践路线中的若干项目模板；仍缺本地运行、最小技术栈选择、成本估算和初学者跟练体验验证。

## 可进入章节

- 是。可以写成：实践路线应引用具体 recipe 作为项目参考，例如 Structured Outputs、File Search RAG、Evals、Agent trace/eval、Usage/Cost 和 Rate limits。不能写成“照着 Cookbook 就能得到生产级 Agent”，也不能把 Cookbook 示例替代 API 文档和安全治理资料。
