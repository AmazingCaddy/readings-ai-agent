# Evidence Note: Agent Eval 与 Trajectory 边界

## 要验证的结论

Agent eval 不能只看最终答案。对会调用工具、跨多步环境行动或产生外部副作用的 Agent，评测至少要覆盖任务完成、交互过程、工具调用、失败原因、权限边界和可复现 trace；trajectory 自动评分则需要单独设计和验证。

## 资料来源

- Source 1：[AgentBench: Evaluating LLMs as Agents](../sources/source-cards/2023-agentbench-paper.md)
- Source 2：[WebArena: A Realistic Web Environment for Building Autonomous Agents](../sources/source-cards/2023-webarena-paper.md)
- Source 3：[OpenAI Evals Repository](../sources/source-cards/2026-openai-evals-repo.md)
- Source 4：[Trace-Aware Eval 最小实验结果](../experiments/trace-aware-eval/results-2026-07-11.md)

## 交叉验证结果

- 一致点：AgentBench 摘要强调需要在 challenging tasks in interactive environments 中定量评估 LLM-as-Agent，并用 8 个环境评估 reasoning 和 decision-making abilities。
- 一致点：AgentBench 摘要把失败原因归到 long-term reasoning、decision-making 和 instruction following 等过程性能力，这支持正文中把错误分类和过程诊断作为 eval 的重点。
- 一致点：WebArena 摘要强调真实、可复现的 Web 环境，包含工具和外部知识库，任务 diverse、long-horizon，并关注 task completions 的 functional correctness。
- 一致点：OpenAI Evals README 将 eval 定义为评估 LLM 或 LLM-based systems 的 framework，并支持 custom/private evals 和 tool-using agents 的高级用例。
- 分歧点：WebArena 更强调端到端任务完成正确性，OpenAI Evals 更强调 eval 框架和自定义用例；二者都不直接给出通用 trajectory 自动评分标准。
- 可能原因：Agent eval 同时有 benchmark、工程回归和线上观测三个层面。公开 benchmark 更适合比较环境，工程 eval 更适合诊断业务系统。
- 本地实验：标准库 trace-aware eval 模拟中，3 条 toy refund runs 的 final-answer-only scorer 全部通过，但 trace-aware scorer 只通过 1 条；它额外发现了无审批执行 `issue_refund` 和工具错误未恢复。这支持“最终答案正确不等于 Agent 过程正确”的工程边界。

## 实验验证

- 是否需要实验：是
- 实验设计：为一个 toy refund Agent 建立 10 条任务，分别只评分最终答案、同时评分工具调用/权限/失败恢复/成本。比较两种评分能发现的错误类型差异，并保存 trace 字段清单。
- 结果：已完成标准库最小实验。final-answer-only scoring 通过 3/3，trace-aware scoring 通过 1/3；过程评分发现 side-effect tool 无审批执行和 tool error 未恢复。实验未覆盖真实模型、真实工具、RAG trace、LLM-as-judge 或人工复核。

## 结论状态

- 部分验证：AgentBench 和 WebArena 支撑交互环境、长程任务、工具/外部知识和失败原因分析的重要性；OpenAI Evals 支撑为具体 LLM 系统和 tool-using agents 设计 custom eval；标准库实验支撑 final-only 与 trace-aware scoring 的错误发现差异。仍缺真实 Agent trace、LLM-as-judge 误判分析和人工复核实验。

## 可进入章节

- 是，但应保守表达：Agent eval 不应只看最终文本，还应记录并检查关键过程。trajectory/trace 是诊断、安全审计和回归测试的重要输入，但自动评分方法需要按任务单独验证。
