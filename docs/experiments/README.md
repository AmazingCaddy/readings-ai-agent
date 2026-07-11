# 实验与复现

实验用于验证工程结论，而不是展示 demo。

## 统一运行入口

真实 / 准真实验证 harness 可以通过统一 runner 执行：

```bash
uv run python docs/experiments/validation-harness-runner/run_validation_harnesses.py
```

没有 `OPENAI_API_KEY` 时，依赖真实 API 的 harness 应返回 `skipped`；本地 MCP stdio harness 应返回 `completed`。runner 只汇总 harness 状态，不代表真实 API / 框架结论已经完成。

当前 runner 状态见 [Validation Harness Runner 结果](validation-harness-runner/results-2026-07-11.md)：2026-07-11 运行覆盖 6 个入口，5 个真实 API harness 因缺少 `OPENAI_API_KEY` 保守跳过，1 个本地 MCP stdio harness 完成。

## 实验清单与状态

下面的条目混合了三类状态：

- `标准库模拟已完成`：可支撑流程、trace 字段和失败模式的窄结论，但不能证明真实模型或真实框架表现。
- `真实 harness 已准备`：脚本入口已存在；无 API key 或未接入真实框架时只能说明入口可运行或会保守跳过。
- `真实实验待跑`：需要真实 API、真实框架、真实数据、成本/延迟记录或人工复核后，才能升级更宽的工程结论。

1. Tool calling 参数错误恢复
   - 目标：观察模型生成错误参数时，schema 校验和重试策略是否有效。
   - 状态：已完成标准库模拟实验，见 [Tool Calling 参数校验与重试实验](tool-calling-validation/README.md) 和 [2026-07-11 结果](tool-calling-validation/results-2026-07-11.md)；真实 API harness 已准备，见 [Real Tool Calling 参数校验与重试实验](real-tool-calling-validation/README.md)。仍需配置 API key 后记录真实模型 / API 结果。

2. RAG chunk size 对召回质量的影响
   - 目标：比较不同 chunk size 和 overlap 对答案准确率的影响。
   - 状态：已完成标准库最小 pipeline / citation 模拟实验，见 [RAG 最小 Pipeline 与 Citation 实验](rag-pipeline/README.md) 和 [2026-07-11 结果](rag-pipeline/results-2026-07-11.md)；真实 LLM citation synthesis harness 已准备，见 [Real RAG Citation Synthesis 实验](real-rag-citation-validation/README.md)。仍需真实 embedding / vector store / rerank 和 chunk size 对比实验。

3. Long-term memory 写入守门
   - 目标：验证自动写入记忆是否会引入冲突、过时和脏数据。
   - 状态：已完成标准库长期记忆写入守门模拟实验，见 [长期记忆写入守门与治理实验](memory-governance/README.md) 和 [2026-07-11 结果](memory-governance/results-2026-07-11.md)；已完成标准库长期记忆生命周期与权限审计实验，见 [长期记忆生命周期与权限审计实验](memory-lifecycle-audit/README.md) 和 [2026-07-11 结果](memory-lifecycle-audit/results-2026-07-11.md)。仍需真实多会话 Agent / memory framework 实验。

4. ReAct vs 简单 workflow
   - 目标：比较工具搜索任务中 ReAct 和固定 workflow 的成功率、成本和延迟。
   - 状态：已完成标准库 workflow / hybrid / ReAct-like tool loop 模拟实验，见 [Workflow、Hybrid 与 ReAct-like Tool Loop 对比实验](workflow-agent-comparison/README.md) 和 [2026-07-11 结果](workflow-agent-comparison/results-2026-07-11.md)。仍需真实模型 / Agent framework / repo issue 实验。

5. Planner/Executor vs 单 Agent
   - 目标：验证任务拆解是否提高复杂任务完成率，还是增加错误传播。
   - 状态：已完成标准库 Planner / Executor 与单循环对比实验，见 [Planner / Executor 与单循环对比实验](planner-executor-comparison/README.md) 和 [2026-07-11 结果](planner-executor-comparison/results-2026-07-11.md)。仍需真实模型 / Agent framework / repo issue 实验。

6. Prompt injection 基线测试
   - 目标：验证工具型 Agent 在恶意文档或外部输入下是否会越权。
   - 状态：已完成标准库 prompt injection / tool permission 模拟实验，见 [Prompt Injection 与工具权限最小实验](prompt-injection-permission/README.md) 和 [2026-07-11 结果](prompt-injection-permission/results-2026-07-11.md)；已完成标准库安全 regression set 最小实验，见 [安全 Regression Set 最小实验](security-regression-set/README.md) 和 [2026-07-11 结果](security-regression-set/results-2026-07-11.md)；已完成标准库审批状态恢复与幂等性实验，见 [审批状态恢复与幂等性实验](approval-state-recovery/README.md) 和 [2026-07-11 结果](approval-state-recovery/results-2026-07-11.md)；真实 API harness 已准备，见 [Real Prompt Injection 与工具权限实验](real-prompt-injection-permission/README.md)。仍需配置 API key 后记录真实模型 / 框架 guardrail / HITL approval 结果。

7. MCP 最小 trace 实验
   - 目标：验证 host/client/server、`tools/list`、`tools/call`、`resources/list`、`resources/read`、roots 和 host approval trace 字段。
   - 状态：已完成标准库模拟实验，见 [MCP 最小 Trace 实验](mcp-trace/README.md) 和 [2026-07-11 结果](mcp-trace/results-2026-07-11.md)；本地 stdio JSON-RPC harness 已准备，见 [Real MCP Stdio Trace 实验](real-mcp-stdio-trace/README.md)。仍需真实 MCP SDK / host / OAuth / URL mode 实验。

8. Trace-aware eval 最小实验
   - 目标：比较 final-answer-only scoring 和 trace-aware scoring 能发现的错误类型差异。
   - 状态：已完成标准库模拟实验，见 [Trace-Aware Eval 最小实验](trace-aware-eval/README.md) 和 [2026-07-11 结果](trace-aware-eval/results-2026-07-11.md)；已完成标准库 trace schema audit，见 [Trace Schema Audit 最小实验](trace-schema-audit/README.md) 和 [2026-07-11 结果](trace-schema-audit/results-2026-07-11.md)；真实模型 trace-aware eval harness 已准备，见 [Real Trace-Aware Eval 实验](real-trace-aware-eval/README.md)。仍需配置 API key 后记录真实 Agent trace、LLM-as-judge 误判和人工复核结果。

9. Reflection / Retry 错误反思实验
   - 目标：验证 reflection 是否能帮助补证据，以及未验证反思是否会污染后续尝试。
   - 状态：已完成标准库 Reflection / Retry 模拟实验，见 [Reflection / Retry 与错误反思实验](reflection-retry/README.md) 和 [2026-07-11 结果](reflection-retry/results-2026-07-11.md)。仍需真实模型 / critic / framework / 长期 episodic memory 实验。

10. 多 Agent 与 Flow 控制对比实验
    - 目标：验证多角色协作是否抵消通信、重复读取和冲突处理成本。
    - 状态：已完成标准库多 Agent / Flow 控制模拟实验，见 [多 Agent 与 Flow 控制对比实验](multi-agent-comparison/README.md) 和 [2026-07-11 结果](multi-agent-comparison/results-2026-07-11.md)。仍需真实模型 / AutoGen / CrewAI / LangGraph 横向实验。

11. 上下文治理与结构化输出实验
    - 目标：比较 free text、JSON mode、schema validation 和 naive/governed context 的失败模式。
    - 状态：已完成标准库上下文治理与结构化输出模拟实验，见 [上下文治理与结构化输出实验](context-structured-output/README.md) 和 [2026-07-11 结果](context-structured-output/results-2026-07-11.md)；已完成标准库上下文策略对比实验，见 [上下文策略对比实验](context-strategy-comparison/README.md) 和 [2026-07-11 结果](context-strategy-comparison/results-2026-07-11.md)；真实 API harness 已准备，见 [Real Structured Outputs / JSON Mode 对比实验](real-structured-output-validation/README.md)。仍需配置 API key 后记录真实 Responses API / Structured Outputs / 长上下文成本结果。

12. 实践路线 smoke harness
    - 目标：验证初学者实践项目是否能拆成结构化输出、工具校验、RAG 引用、eval cases 和成本闸门等可运行验收单元。
    - 状态：已完成标准库 smoke harness，见 [实践路线 Smoke Harness](practice-roadmap-harness/README.md) 和 [2026-07-11 结果](practice-roadmap-harness/results-2026-07-11.md)。仍需真实 Cookbook / API recipe 本地试跑。

13. 框架选择 rubric smoke test
    - 目标：验证框架比较能否从任务画像、能力标签、missing required 和 cautions 出发，而不是做框架排行榜。
    - 状态：已完成标准库 rubric smoke test，见 [框架选择 Rubric Smoke Test](framework-selection-rubric/README.md) 和 [2026-07-11 结果](framework-selection-rubric/results-2026-07-11.md)。仍需真实同一任务框架横向实验。

14. RAG、短期记忆与长期记忆对比实验
    - 目标：验证外部知识检索、当前 thread state 和跨会话 guarded memory 的适用边界。
    - 状态：已完成标准库对比实验，见 [RAG、短期记忆与长期记忆对比实验](rag-memory-comparison/README.md) 和 [2026-07-11 结果](rag-memory-comparison/results-2026-07-11.md)。仍需真实 RAG / memory framework / 多会话实验。

15. Repo Issue Agent toy 实验
    - 目标：验证 coding agent 进阶项目是否能用 toy repo、安全 sandbox、确认模式、trajectory、diff/rollback、测试输出和成本/延迟记录来复现。
    - 状态：真实实验设计已准备，见 [Real Repo Issue Agent Toy 实验](real-repo-issue-agent-toy/README.md)。尚未运行 mini-SWE-agent、SWE-agent、真实模型或 toy repo；不能证明任何 coding agent 默认可靠。

16. LangGraph interrupt recovery 实验
    - 目标：验证 LangGraph `interrupt()`、checkpointer、`thread_id` 和 `Command(resume=...)` 在高风险工具审批流程中的恢复、幂等和审计边界。
    - 状态：真实实验设计已准备，见 [Real LangGraph Interrupt Recovery 实验](real-langgraph-interrupt-recovery/README.md)。尚未安装或运行 LangGraph；不能证明 LangGraph interrupt、checkpointer 或任何 HITL 框架默认生产安全。

17. Agentic security regression set 实验
    - 目标：把 MITRE ATLAS 和 OWASP Agentic AI resources 中的 agentic-specific 风险整理成可迁移到真实模型 / 框架的安全 case matrix。
    - 状态：真实实验设计已准备，见 [Real Agentic Security Regression Set 实验](real-agentic-security-regression-set/README.md)。尚未实现脚本、运行真实模型或运行真实框架；不能证明任何 mitigation、detector、guardrail、HITL、sandbox、runtime containment 或 monitoring 有效。

## 实验记录要求

- 明确假设。
- 明确输入数据。
- 记录模型、框架和版本。
- 保存 trace 或日志。
- 记录成功率、成本、延迟和失败类型。
- 结论必须说明适用边界。
