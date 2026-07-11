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
- Source 13：[Real mini-SWE-agent Runtime Surface Validation 结果](../experiments/real-mini-swe-agent-runtime-validation/results-2026-07-12.md)
- Source 14：[Hugging Face Agents Course](../sources/source-cards/2026-huggingface-agents-course.md)
- Source 15：[Hugging Face smolagents Documentation and Source](../sources/source-cards/2026-smolagents-docs.md)

## 交叉验证结果

- 一致点：Cookbook 首页定位为 notebook examples；这支持把它作为学习项目模板，而不是规范来源。
- 一致点：`Introduction to Structured Outputs` 包含 response format usage、function call usage、math tutor、summarization、entity extraction 和 refusal 小节；这能支撑项目 1 的结构化输出练习，也能连接第 02/03 章的 schema 与 refusal 边界。
- 一致点：`Doing RAG on PDFs using File Search in the Responses API` 包含 vector store、file search、LLM 整合、retrieval evaluation、Recall / Precision / MRR / MAP 等内容；这能支撑项目 3 的 RAG 练习和项目 7 的检索评测入门。
- 一致点：`Getting Started with OpenAI Evals` 包含 eval setup、dataset、running evaluation 和 eval logs；这能支撑小型 regression set 的实践路线。同时页面提示已有 hosted evals product/API，说明旧框架材料需要按当前 API 复核。
- 一致点：`Evaluating Agents with Langfuse` 明确围绕 OpenAI Agents SDK 内部步骤 trace、online evaluation、offline evaluation、dataset evaluation 和生产指标；这能支撑“trace 不只是日志，而是 eval/observability 的输入”这一练习方向。
- 一致点：`Usage API / Cost API` recipe 覆盖自定义 usage/cost monitoring 的最小流程，示例字段包括 `start_time`、`end_time`、`bucket_width`、`group_by`、`project_id`、`line_item`、`amount.value` 和 `amount.currency`，并示例按日、按 line item 聚合以及第三方 dashboard 集成；这能支撑项目 8 的成本记录表字段。
- 一致点：`How to handle rate limits` recipe 覆盖 429 / `RateLimitError`、exponential backoff、最大重试约束、失败请求消耗预算、主动节流、RPM/RPD/TPM 区分、`max_tokens` 估算影响、batching、fallback model 和并发请求脚本入口；这能支撑项目 8 的限流、重试、降级和批处理练习字段。
- 一致点：2026-07-12 复核确认 Cookbook 首页和 6 个具体 recipe 均返回 HTTP 200：Structured Outputs、File Search Responses、Getting Started with OpenAI Evals、Agents SDK evaluate agents、Usage/Cost API、Rate limits；Rate limits 页最新 `last-modified` 为 `Sat, 11 Jul 2026 19:02:32 GMT`，比旧记录更新，应以 source card 当前 metadata 为准。
- 一致点：SWE-agent arXiv API、GitHub API / README、docs index / hello_world / architecture Markdown 已于 2026-07-12 复核。SWE-agent 摘要和 docs 支撑软件工程 Agent 进阶练习需要 agent-computer interface、仓库导航、文件编辑、测试执行、程序执行、deployment、sandbox 和 trajectory；hello_world 说明 `sweagent run` 会经历 deployment、tools、prompts、main loop、submission 并保存 trajectory，architecture 说明 `SWEEnv` 通过 SWE-ReX Deployment 启动本地 Docker container 或远程执行环境并把 Agent action 交给 shell session 执行。
- 一致点：SWE-agent README、docs index warning 和站点弹窗均提示当前推荐 mini-swe-agent；站点弹窗写明 SWE-agent is now in maintenance-only mode。因此实践路线中 SWE-agent 更适合作为 ACI / repo-issue agent 的论文和历史 reference，真实练习入口应优先考虑 mini-SWE-agent。
- 一致点：mini-SWE-agent README、docs 和源码补强当前轻量 coding agent 入口、bash-only 最小控制流、confirm/yolo/human 模式、trajectory、cost/call limit 和 sandbox 配置边界；Real mini-SWE-agent CLI Surface Validation 进一步确认 `mini-swe-agent==2.4.5` 的本地 CLI 入口、关键 options、默认 `mode: confirm` 和 `cost_limit:` 可用；Real mini-SWE-agent Runtime Surface Validation 进一步确认 `InteractiveAgent` / `LocalEnvironment` / deterministic fake model 可以在 toy repo 上执行固定命令、修改实现、复跑测试并写出 trajectory。
- 一致点：Hugging Face Agents Course 2026-07-12 复核补强初学者外部跟学地图：Unit 0 说明 basic Python / basic LLM prerequisites、beginner-to-expert 课程结构和每周 3-4 小时节奏；Unit 1 支撑 Agent、reasoning、planning、actions/tools、agency spectrum 和 LLM 只生成文本而由应用/Agent 执行工具的教学边界；Unit 2 支撑简单 prompt chain 不一定需要 agentic framework、复杂 tool calling / multi-agent / memory / logging / retry 才更需要框架抽象；bonus observability/evaluation 单元支撑 token/cost、latency、error traces、user feedback、LLM-as-judge 和 offline benchmark datasets 这些练习主题。
- 一致点：smolagents docs 2026-07-12 复核补强一个可选框架练习：用同一只读 mock task 对比 `CodeAgent` 的 Python code snippets 和 `ToolCallingAgent` 的 JSON/text tool calls，记录 tool metadata、参数校验、trace、sandbox、Hub/MCP tool trust 和 `trust_remote_code`。Real smolagents validation 已完成这个方向的本地 fake-model 最小 run：`CodeAgent` 和 `ToolCallingAgent` 都调用同一组 toy tools，`output_schema` 声明不触发 runtime output validation，默认 local executor 阻断未授权 import。Secure Code Execution 和 README 明确 `LocalPythonExecutor` 不是 security boundary。
- 边界：Cookbook recipe 往往以演示为主，权限、审计、数据隔离、成本上限、部署和回滚常被简化；不能把 recipe 直接写成生产最佳实践。
- 边界：Usage/Cost 和 rate limit recipe 只能支撑“应记录哪些字段、可如何组织练习”的工程参考；没有真实 API key、真实账户用量、真实 429、真实 dashboard 或真实 fallback 对照时，不能推出成本更低、延迟更稳、吞吐更高、限流处理更可靠或 fallback 质量足够的结论。
- 边界：Cookbook notebook 页面可能包含示例输出、第三方库代码和 dashboard 原型；除非本 repo 单独运行并记录结果，否则这些输出不能写成本地复现证据，也不能替代 API reference、账户设置或生产 runbook。
- 边界：SWE-agent / mini-SWE-agent 这类 coding agent 涉及真实文件写入和命令执行，不适合作为初学者第一项目；应先用 toy repo、sandbox、diff/rollback、测试输出和人工确认控制风险。
- 边界：SWE-agent docs 中的 Docker sandbox、SWE-ReX deployment、remote execution 和 trajectory 说明只能证明文档化机制存在；不能证明用户本地默认安全、sandbox 隔离充分、真实 API key 不会进入日志、patch 总是正确或回滚总是可靠。
- 边界：SWE-agent README / docs 中的 SWE-bench、EnIGMA、SOTA、performance claim 和 mini-SWE-agent 65% news 不能作为本手册正文中的当前能力结论；这些需要独立 benchmark 复核、真实模型成本和同题实验。
- 边界：Hugging Face Agents Course 是课程资料，不是 API spec、benchmark 或生产指南；它不能证明课程 examples / Spaces / final assignment / leaderboard 可复现，也不能证明 smolagents、LlamaIndex、LangGraph 或任何模型在真实任务中更可靠、更便宜或更适合生产。
- 边界：smolagents 官方文档可以支撑 agent 类型、工具 metadata、代码执行和 sandbox/trust boundary，但不能证明 code agents 默认更好、真实 sandbox 隔离充分、Hub/MCP tool 安全、benchmark claim 有代表性、成本更低或生产可靠。
- 边界：Practice roadmap 的“先结构化输出、再工具/RAG、再 eval/生产化”有资料支撑为学习顺序，但仍不是唯一正确顺序；项目难度和技术栈需要本地试跑后再细化。
- 本地实验：标准库 smoke harness 将结构化输出、refusal、工具参数校验、RAG 引用、unsupported question 拒答和成本预算阻断组织成 6 条 eval cases，全部通过。扩展后的 readiness audit 还检查了 6 个跟练项目卡片，要求每个卡片包含 prerequisites、setup/run commands、acceptance checks、trace fields、failure examples、references 和 boundaries，并至少有一个可重复 `uv run ...` 命令和本地 control 边界说明，6/6 通过。这支持“实践项目要有验收标准、trace、失败分类、可重复命令、references 和适用边界”的教学边界。
- 本地实验：Real Repo Issue Agent Toy 已完成固定 workflow baseline 和确定性 workflow-agent hybrid baseline。脚本创建临时 Python toy repo，初始 `pytest` 为 3 failed / 2 passed；两个 baseline 都只修改 `discount.py`，复跑后 5 tests passed，并记录 diff、trajectory、是否修改测试和 secret 脱敏。hybrid baseline 额外记录建议、人工审批、拒绝不必要环境变量 dump、scoped diff 和复跑测试。这支持“Repo Issue Agent 练习应先建立可复现对照组和审批边界”的教学边界，但不证明 mini-SWE-agent、SWE-agent、真实模型或自主 coding agent 表现。
- 本地实验：Real mini-SWE-agent CLI Surface Validation 已完成临时依赖 run。它验证 `mini-swe-agent --help`、`--model`、`--task`、`--yolo`、`--cost-limit`、`--config`、`--output` 等关键选项和包内默认 `mini.yaml` 中的 `mode: confirm` / `cost_limit:`。这支持“进阶练习可以先检查工具入口和默认安全相关配置”的教学边界，但不证明 mini-SWE-agent 能修复 issue。
- 本地实验：Real mini-SWE-agent Runtime Surface Validation 已完成 deterministic fake-model runtime run。它用 mini-SWE-agent `InteractiveAgent`、`LocalEnvironment` 和 `DeterministicModel` 在临时 toy repo 上执行 5 个固定 action：读取 issue/实现、复现失败测试、patch `discount.py`、复跑测试通过并提交；trajectory 写出 `mini-swe-agent-1.1`，记录 fake API calls / fake cost，并观察到 configured env marker 会进入 trajectory。这支持“进阶练习需要检查 trajectory 和 env 脱敏”的教学边界，但不证明真实模型规划、confirm 人工负担、sandbox 隔离或真实成本。

## 实验验证

- 是否需要实验：是
- 实验设计：先用标准库 smoke harness 验证项目验收结构和 project readiness card 结构，再选择 3 个真实最小项目：Structured Outputs 问答、File Search/RAG 问答、小型 eval harness。Repo Issue Agent 进阶项目先建立 fixed workflow baseline 和 workflow-agent hybrid 审批 baseline，检查 mini-SWE-agent CLI / 默认配置表面和 fake-model runtime surface，再扩展 mini-SWE-agent confirm-mode。每个项目记录依赖、运行成本、输入输出样例、trace、失败样例、初学者阻塞点和可复现命令。
- 结果：已完成标准库 smoke harness，包含 6/6 eval cases 和 6/6 project readiness cards。Usage/Cost 与 Rate limits recipe 已完成字段级和 HTTP metadata 复核；SWE-agent 2026-07-12 复核已把 ACI、SWE-ReX deployment、Docker/remote/local execution、trajectory 和 maintenance-only / mini-first 边界补清楚；Real Repo Issue Agent Toy 已完成固定 workflow baseline 和确定性 workflow-agent hybrid baseline；Real mini-SWE-agent CLI Surface Validation 已完成安装 / CLI / 默认配置表面检查；Real mini-SWE-agent Runtime Surface Validation 已完成 deterministic fake-model toy repo runtime / trajectory / env marker 观察；尚未执行真实 Cookbook / API recipe，也尚未运行真实模型 mini-SWE-agent confirm-mode / SWE-agent / 真实模型驱动 hybrid。

## 结论状态

- 可入正文：窄结论“Cookbook 的具体 recipe 可以作为初学者实践项目参考，但不能替代 API 文档、生产安全指南或本地实验”已完成第一轮交叉验证。Cookbook 具体 recipe 支撑 Structured Outputs、File Search RAG、Evals、Agents trace/eval、Usage/Cost 和 Rate limits 等练习方向；Usage/Cost 与 rate limit recipe 可支撑项目 8 的 usage/cost/rate-limit/retry/fallback/batching 字段设计；OpenAI Function Calling / Responses API / Evals source cards 提供对应 API 或 eval 背景；标准库 smoke harness 支撑把项目组织成验收标准、trace、失败分类和可重复运行命令，readiness audit 进一步支撑每个跟练项目应写清 prerequisites、setup/run commands、acceptance checks、trace fields、failure examples、references 和 boundaries；SWE-agent 支撑 repo issue / coding agent 的 ACI、deployment、Docker/remote/local execution、SWE-ReX shell session 和 trajectory 学习边界，但因官方已推荐 mini-SWE-agent 且站点提示 maintenance-only，正文应把 SWE-agent 写成论文/历史 reference 而不是默认实践入口；mini-SWE-agent docs/source、CLI surface validation 和 runtime surface validation 支撑把 Repo Issue Agent 设计成 toy repo、确认模式、trajectory、成本限制、CLI 配置、runtime/trajectory 和 sandbox 检查的进阶练习；Real Repo Issue Agent Toy 固定 workflow 和确定性 workflow-agent hybrid baseline 支撑 toy repo / failing tests / diff / trajectory 对照组以及建议-审批-执行控制边界的可复现形状。
- 部分验证：真实 Cookbook / API 本地运行、真实 Hugging Face course exercise、真实 smolagents 模型驱动 `CodeAgent` / `ToolCallingAgent` / sandbox / MCP tool 对照、真实 Usage/Cost API 账户数据、真实 429 / retry / throttle / batching / fallback 行为、真实模型 mini-SWE-agent confirm-mode / SWE-agent maintenance-mode 对照 / 真实模型驱动 workflow-agent hybrid toy repo 试跑、最小技术栈选择、成本估算、真实模型 refusal / RAG citation / trace 结果和初学者跟练体验仍需实测；readiness card 和 smolagents fake-model run 只验证教程结构或本地 runtime surface，不证明依赖一定顺利、费用一定可控、模型行为可靠或初学者不会卡住。不能写成照着 Cookbook、Hugging Face course、smolagents demo 或 coding-agent demo 就能得到生产级 Agent，也不能断言当前项目顺序唯一最优。

## 可进入章节

- 是。可以确定写成：实践路线应引用具体 recipe、课程单元和框架文档作为项目参考，例如 Structured Outputs、File Search RAG、Evals、Agent trace/eval、Usage/Cost、Rate limits、Hugging Face Agents Course 的 prerequisites / Agent-tool / frameworks / observability-evaluation 学习单元，以及 smolagents 的 `CodeAgent` / `ToolCallingAgent` 对照练习。每个跟练项目应写清 prerequisites、可重复命令、验收标准、trace 字段、失败样例、references 和适用边界。Usage/Cost 与 Rate limits recipe 可支撑成本、用量、限流、重试、fallback 和 batching 的练习记录字段。不能写成“照着 Cookbook、Hugging Face course 或 smolagents demo 就能得到生产级 Agent”，也不能把 Cookbook 示例、课程单元或框架文档替代 API 文档、安全治理资料、本地验收、真实成本记录和真实限流实验。
