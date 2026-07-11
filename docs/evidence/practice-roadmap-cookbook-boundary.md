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
- Source 8：[实践路线 Smoke Harness 结果](../experiments/practice-roadmap-harness/results-2026-07-11.md)
- Source 9：[SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](../sources/source-cards/2024-swe-agent-paper.md)
- Source 10：[mini-SWE-agent Documentation and Source](../sources/source-cards/2026-mini-swe-agent-docs.md)
- Source 11：[Real Repo Issue Agent Toy 结果](../experiments/real-repo-issue-agent-toy/results-2026-07-12.md)
- Source 12：[Real mini-SWE-agent CLI Surface Validation 结果](../experiments/real-mini-swe-agent-cli-validation/results-2026-07-12.md)

## 交叉验证结果

- 一致点：Cookbook 首页定位为 notebook examples；这支持把它作为学习项目模板，而不是规范来源。
- 一致点：`Introduction to Structured Outputs` 包含 response format usage、function call usage、math tutor、summarization、entity extraction 和 refusal 小节；这能支撑项目 1 的结构化输出练习，也能连接第 02/03 章的 schema 与 refusal 边界。
- 一致点：`Doing RAG on PDFs using File Search in the Responses API` 包含 vector store、file search、LLM 整合、retrieval evaluation、Recall / Precision / MRR / MAP 等内容；这能支撑项目 3 的 RAG 练习和项目 7 的检索评测入门。
- 一致点：`Getting Started with OpenAI Evals` 包含 eval setup、dataset、running evaluation 和 eval logs；这能支撑小型 regression set 的实践路线。同时页面提示已有 hosted evals product/API，说明旧框架材料需要按当前 API 复核。
- 一致点：`Evaluating Agents with Langfuse` 明确围绕 OpenAI Agents SDK 内部步骤 trace、online evaluation、offline evaluation、dataset evaluation 和生产指标；这能支撑“trace 不只是日志，而是 eval/observability 的输入”这一练习方向。
- 一致点：`Usage API / Cost API` recipe 覆盖自定义 usage/cost monitoring 的最小流程，示例字段包括 `start_time`、`end_time`、`bucket_width`、`group_by`、`project_id`、`line_item`、`amount.value` 和 `amount.currency`，并示例按日、按 line item 聚合以及第三方 dashboard 集成；这能支撑项目 8 的成本记录表字段。
- 一致点：`How to handle rate limits` recipe 覆盖 429 / `RateLimitError`、exponential backoff、最大重试约束、失败请求消耗预算、主动节流、RPM/RPD/TPM 区分、`max_tokens` 估算影响、batching、fallback model 和并发请求脚本入口；这能支撑项目 8 的限流、重试、降级和批处理练习字段。
- 一致点：SWE-agent 摘要和 README 支撑软件工程 Agent 进阶练习需要 agent-computer interface、仓库导航、文件编辑、测试执行和程序执行；mini-SWE-agent README、docs 和源码补强当前轻量 coding agent 入口、bash-only 最小控制流、confirm/yolo/human 模式、trajectory、cost/call limit 和 sandbox 配置边界；Real mini-SWE-agent CLI Surface Validation 进一步确认 `mini-swe-agent==2.4.5` 的本地 CLI 入口、关键 options、默认 `mode: confirm` 和 `cost_limit:` 可用。
- 边界：Cookbook recipe 往往以演示为主，权限、审计、数据隔离、成本上限、部署和回滚常被简化；不能把 recipe 直接写成生产最佳实践。
- 边界：Usage/Cost 和 rate limit recipe 只能支撑“应记录哪些字段、可如何组织练习”的工程参考；没有真实 API key、真实账户用量、真实 429、真实 dashboard 或真实 fallback 对照时，不能推出成本更低、延迟更稳、吞吐更高、限流处理更可靠或 fallback 质量足够的结论。
- 边界：SWE-agent / mini-SWE-agent 这类 coding agent 涉及真实文件写入和命令执行，不适合作为初学者第一项目；应先用 toy repo、sandbox、diff/rollback、测试输出和人工确认控制风险。
- 边界：Practice roadmap 的“先结构化输出、再工具/RAG、再 eval/生产化”有资料支撑为学习顺序，但仍不是唯一正确顺序；项目难度和技术栈需要本地试跑后再细化。
- 本地实验：标准库 smoke harness 将结构化输出、refusal、工具参数校验、RAG 引用、unsupported question 拒答和成本预算阻断组织成 6 条 eval cases，全部通过。这支持“实践项目要有验收标准、trace、失败分类和可重复运行命令”的教学边界。
- 本地实验：Real Repo Issue Agent Toy 已完成固定 workflow baseline 和确定性 workflow-agent hybrid baseline。脚本创建临时 Python toy repo，初始 `pytest` 为 3 failed / 2 passed；两个 baseline 都只修改 `discount.py`，复跑后 5 tests passed，并记录 diff、trajectory、是否修改测试和 secret 脱敏。hybrid baseline 额外记录建议、人工审批、拒绝不必要环境变量 dump、scoped diff 和复跑测试。这支持“Repo Issue Agent 练习应先建立可复现对照组和审批边界”的教学边界，但不证明 mini-SWE-agent、SWE-agent、真实模型或自主 coding agent 表现。
- 本地实验：Real mini-SWE-agent CLI Surface Validation 已完成临时依赖 run。它验证 `mini-swe-agent --help`、`--model`、`--task`、`--yolo`、`--cost-limit`、`--config`、`--output` 等关键选项和包内默认 `mini.yaml` 中的 `mode: confirm` / `cost_limit:`。这支持“进阶练习可以先检查工具入口和默认安全相关配置”的教学边界，但不证明 mini-SWE-agent 能修复 issue。

## 实验验证

- 是否需要实验：是
- 实验设计：先用标准库 smoke harness 验证项目验收结构，再选择 3 个真实最小项目：Structured Outputs 问答、File Search/RAG 问答、小型 eval harness。Repo Issue Agent 进阶项目先建立 fixed workflow baseline 和 workflow-agent hybrid 审批 baseline，检查 mini-SWE-agent CLI / 默认配置表面，再扩展 mini-SWE-agent confirm-mode。每个项目记录依赖、运行成本、输入输出样例、trace、失败样例、初学者阻塞点和可复现命令。
- 结果：已完成标准库 smoke harness。Usage/Cost 与 rate limit recipe 已完成字段级复核；Real Repo Issue Agent Toy 已完成固定 workflow baseline 和确定性 workflow-agent hybrid baseline；Real mini-SWE-agent CLI Surface Validation 已完成安装 / CLI / 默认配置表面检查；尚未执行真实 Cookbook / API recipe，也尚未运行 mini-SWE-agent repo issue / SWE-agent / 真实模型。

## 结论状态

- 可入正文：窄结论“Cookbook 的具体 recipe 可以作为初学者实践项目参考，但不能替代 API 文档、生产安全指南或本地实验”已完成第一轮交叉验证。Cookbook 具体 recipe 支撑 Structured Outputs、File Search RAG、Evals、Agents trace/eval、Usage/Cost 和 Rate limits 等练习方向；Usage/Cost 与 rate limit recipe 可支撑项目 8 的 usage/cost/rate-limit/retry/fallback/batching 字段设计；OpenAI Function Calling / Responses API / Evals source cards 提供对应 API 或 eval 背景；标准库 smoke harness 支撑把项目组织成验收标准、trace、失败分类和可重复运行命令；mini-SWE-agent docs/source 和 CLI surface validation 支撑把 Repo Issue Agent 设计成 toy repo、确认模式、trajectory、成本限制、CLI 配置和 sandbox 检查的进阶练习；Real Repo Issue Agent Toy 固定 workflow 和确定性 workflow-agent hybrid baseline 支撑 toy repo / failing tests / diff / trajectory 对照组以及建议-审批-执行控制边界的可复现形状。
- 部分验证：真实 Cookbook / API 本地运行、真实 Usage/Cost API 账户数据、真实 429 / retry / throttle / batching / fallback 行为、SWE-agent / mini-SWE-agent repo issue / 真实模型驱动 workflow-agent hybrid toy repo 试跑、最小技术栈选择、成本估算、真实模型 refusal / RAG citation / trace 结果和初学者跟练体验仍需实测；不能写成照着 Cookbook 或 coding-agent demo 就能得到生产级 Agent，也不能断言当前项目顺序唯一最优。

## 可进入章节

- 是。可以确定写成：实践路线应引用具体 recipe 作为项目参考，例如 Structured Outputs、File Search RAG、Evals、Agent trace/eval、Usage/Cost 和 Rate limits。Usage/Cost 与 Rate limits recipe 可支撑成本、用量、限流、重试、fallback 和 batching 的练习记录字段。不能写成“照着 Cookbook 就能得到生产级 Agent”，也不能把 Cookbook 示例替代 API 文档、安全治理资料、本地验收、真实成本记录和真实限流实验。
