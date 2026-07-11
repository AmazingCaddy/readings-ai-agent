# Evidence Note: Agent Eval 与 Trajectory 边界

## 要验证的结论

Agent eval 不能只看最终答案。对会调用工具、跨多步环境行动或产生外部副作用的 Agent，评测至少要覆盖任务完成、交互过程、工具调用、失败原因、权限边界和可复现 trace；trajectory 自动评分则需要单独设计和验证。

## 资料来源

- Source 1：[AgentBench: Evaluating LLMs as Agents](../sources/source-cards/2023-agentbench-paper.md)
- Source 2：[WebArena: A Realistic Web Environment for Building Autonomous Agents](../sources/source-cards/2023-webarena-paper.md)
- Source 3：[τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](../sources/source-cards/2024-tau-bench-paper.md)
- Source 4：[OpenAI Evals Repository](../sources/source-cards/2026-openai-evals-repo.md)
- Source 5：[OpenAI Evaluation Guides](../sources/source-cards/2026-openai-evaluation-guides.md)
- Source 6：[Evidence Note: Browser Agent 与网页自动化边界](browser-agent-boundary.md)
- Source 7：[Trace-Aware Eval 最小实验结果](../experiments/trace-aware-eval/results-2026-07-11.md)
- Source 8：[Grader Misalignment / Reward Hacking 最小实验结果](../experiments/grader-misalignment/results-2026-07-11.md)

## 交叉验证结果

- 一致点：AgentBench 摘要强调需要在 challenging tasks in interactive environments 中定量评估 LLM-as-Agent，并用 8 个环境评估 reasoning 和 decision-making abilities。
- 一致点：AgentBench 摘要把失败原因归到 long-term reasoning、decision-making 和 instruction following 等过程性能力，这支持正文中把错误分类和过程诊断作为 eval 的重点。
- 一致点：WebArena 摘要强调真实、可复现的 Web 环境，包含工具和外部知识库，任务 diverse、long-horizon，并关注 task completions 的 functional correctness。
- 一致点：τ-bench 摘要强调动态用户交互、domain-specific API tools、policy guidelines、conversation 结束后的 database state 和 annotated goal state 对比，以及用 `pass^k` 衡量多次试验一致性。
- 一致点：Browser Agent evidence 显示浏览器 Agent 的过程包含导航、点击、输入、上传、滚动、登录态和表单/购物等外部动作；这进一步支持 Web/Browser Agent 必须评估 trajectory、页面状态、权限和外部副作用，而不是只看最终文本。
- 一致点：OpenAI Evals README 将 eval 定义为评估 LLM 或 LLM-based systems 的 framework，并支持 custom/private evals 和 tool-using agents 的高级用例。
- 一致点：OpenAI Evaluation best practices 将 eval 定义为 structured tests，用来处理 AI output variability；它强调 task-specific evals、log everything、automated scoring、continuous evaluation 和用 human feedback 校准自动评分。
- 一致点：OpenAI Evaluation best practices 将 single-agent 的 tool selection / data precision 和 multi-agent 的 handoff accuracy 列为需要评估的 nondeterminism 来源；这直接补强工具型和多 Agent 不能只看最终答案的边界。
- 一致点：OpenAI Agent evals guide 建议调试 workflow behavior 时先从 traces 开始，因为 trace 捕获 model calls、tool calls、guardrails 和 handoffs；知道“good”是什么之后，再迁移到 datasets 和 eval runs 来做 repeatable comparison。
- 分歧点：WebArena 更强调端到端 Web 任务完成正确性，τ-bench 更强调工具 Agent 与模拟用户和数据库状态的交互评测，OpenAI Evals 更强调 eval 框架和自定义用例；它们都不直接给出通用 trajectory 自动评分标准。
- 可能原因：Agent eval 同时有 benchmark、工程回归和线上观测三个层面。公开 benchmark 更适合比较环境，工程 eval 更适合诊断业务系统。
- 本地实验：标准库 trace-aware eval 模拟中，3 条 toy refund runs 的 final-answer-only scorer 全部通过，但 trace-aware scorer 只通过 1 条；它额外发现了无审批执行 `issue_refund` 和工具错误未恢复。这支持“最终答案正确不等于 Agent 过程正确”的工程边界。
- 本地实验：Real Trace-Aware Eval harness 在无 API key 时运行 deterministic scorer control。4 条 trace fixture 中 final-only scorer 4/4 通过，trace-aware scorer 1/4 通过；3 个 score delta 分别来自缺少 `get_order` / `check_refund_policy`、最终文本声称 not found 但无 `tool_error` trace、以及 `issue_refund` side-effect tool 缺少 approval rejection trace。该结果补强最小规则 scorer 的失败样例，但不调用真实模型。
- 本地实验：标准库 grader misalignment / reward hacking audit 中，`string_check` 匹配人工标签 3/6，`keyword_judge` 2/6，`tool_call_rule` 4/6，`multigrader_majority` 3/6；它覆盖 format variant 漏报、verbose wrong answer 误报、reward-hacked answer 误报、未审批副作用和错误 tool arguments。这支持“trajectory 自动评分需要 edge cases、误判统计和人工校准”的工程边界。

## 实验验证

- 是否需要实验：是
- 实验设计：为一个 toy refund Agent 建立 10 条任务，分别只评分最终答案、同时评分工具调用/权限/失败恢复/成本。比较两种评分能发现的错误类型差异，并保存 trace 字段清单。
- 结果：已完成标准库 trace-aware eval 最小实验、Real Trace-Aware Eval deterministic scorer control 和 grader misalignment / reward hacking audit。标准库实验中 final-answer-only scoring 通过 3/3，trace-aware scoring 通过 1/3；Real Trace-Aware Eval scorer control 中 final-only 4/4 通过，trace-aware 1/4 通过；过程评分发现 side-effect tool 无审批执行、tool error 未恢复、缺工具调用、缺 error trace 和缺 approval rejection。grader audit 进一步显示 exact string、关键词 judge、tool-call rule 和 majority multigrader 都有不同误报/漏报。实验未覆盖真实模型、真实工具、RAG trace、真实 LLM-as-judge 或真实人工复核流程。

## 结论状态

- 可入正文：窄结论“公开 benchmark 可以帮助学习评测环境、任务设计和失败分类，但不能直接代表真实业务 Agent 质量或产品可用性”已完成第一轮交叉验证。AgentBench、WebArena 和 τ-bench 支撑交互环境、长程任务、工具/外部知识、用户交互、状态评测、functional correctness 和失败原因分析的重要性；OpenAI Evals repo 和 Evaluation guides 支撑为具体 use case 写 task-specific / custom eval，并用 datasets 和持续评估做回归；这共同说明公开 benchmark 更适合学习评测思想和做有限比较，业务系统仍需要自己的任务集、trace、权限和回归评测。
- 可入正文：窄结论“对会调用工具或产生外部副作用的 Agent，只看最终答案不足以验证过程安全；关键 trajectory / trace 应作为 eval、审计和回归输入”已完成第一轮交叉验证。AgentBench 和 WebArena 支撑交互环境、长程任务、工具/外部知识和失败原因分析的重要性；τ-bench 支撑工具 Agent 需要评估动态对话、API tools、policy guidelines、数据库状态和多次试验一致性；Browser Agent evidence 补强网页动作、浏览器状态和表单/购物/登录态等外部副作用边界；OpenAI Evaluation guides 补强 trace grading、tool selection、data precision、handoff accuracy、instruction/safety policy violation 和 dataset/eval run 的工程流程；标准库实验和 Real Trace-Aware Eval scorer control 复现了 final-only scoring 漏掉无审批副作用工具、工具错误未恢复、缺工具调用、缺 error trace 和缺 approval rejection 等过程错误。
- 部分验证：τ-bench 原始任务已被仓库标注为过期；OpenAI Evals platform 正在退役；Real Trace-Aware Eval scorer control 只验证本地规则 scorer，不验证真实模型、真实平台或 LLM-as-judge；标准库 grader audit 只验证误判结构，不验证真实 LLM-as-judge 可靠性；真实 Agent trace 字段覆盖、真实业务质量与公开 benchmark 的相关性仍待真实模型、平台映射、τ³-bench 小样本试跑和人工复核实验。

## 可进入章节

- 是。可以确定写成：公开 benchmark 适合学习评测思想和有限比较，但不能替代业务 eval；对会调用工具或产生外部副作用的 Agent，只看最终文本不足以验证过程安全，关键 trajectory / trace 应进入 eval、审计和回归输入；调试阶段可先看代表性 traces，稳定后再沉淀为 dataset / eval runs；自动 grader 需要 edge cases、误判统计和人工校准。仍需保守写明：公开 benchmark 分数不能直接推出产品可用性，真实 LLM-as-judge 和真实平台字段覆盖必须按任务单独验证。
