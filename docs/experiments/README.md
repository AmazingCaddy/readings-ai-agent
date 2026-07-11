# 实验与复现

实验用于验证工程结论，而不是展示 demo。

## 统一运行入口

真实 / 准真实验证 harness 可以通过统一 runner 执行：

```bash
uv run python docs/experiments/validation-harness-runner/run_validation_harnesses.py
```

没有 `OPENAI_API_KEY` 时，依赖真实 API 的 harness 应返回 `skipped`；本地 MCP stdio harness 应返回 `completed`；官方 MCP SDK harness 在没有 `mcp` Python package 时应返回 `skipped`；LlamaIndex harness 在没有 `llama-index-core` 时应返回 `skipped`；AutoGen/CrewAI harness 在没有对应包时应返回 `skipped`；Repo Issue Agent toy harness 在没有 `pytest` 时应返回 `skipped`；mini-SWE-agent CLI harness 在没有 `mini-swe-agent` 时应返回 `skipped`。部分框架 harness 可以用 `uv run --with ...` 临时依赖运行。runner 只汇总 harness 状态，不代表真实 API / 框架结论已经完成。

当前 runner 状态见 [Validation Harness Runner 结果](validation-harness-runner/results-2026-07-12.md)：2026-07-12 运行覆盖 19 个入口，真实 API harness 因缺少 `OPENAI_API_KEY` 保守跳过，LlamaIndex harness 通过临时依赖完成本地 `VectorStoreIndex` / retriever / source-node metadata run，Playwright harness 通过临时依赖和本地 Chromium headless shell 完成固定 demo page workflow，LangGraph interrupt recovery harness 通过临时依赖完成 `MemorySaver` 最小 run 和 `SqliteSaver` 本地 SQLite 同进程 graph 重建恢复 case、双本地 Python 进程 prepare/resume case 和双本地 Python 进程并发 resume case，LangGraph memory store harness 完成本地 `InMemoryStore` namespace / put / get / search / delete run，Real Framework Same-Task Comparison 在标准 full runner 中完成 OpenAI Agents SDK / LangGraph / LlamaIndex adapter，本地 MCP stdio harness 和官方 MCP Python SDK stdio harness 完成。Semantic Kernel plugin harness、same-task comparison 的 Semantic Kernel adapter、Real Multi-Agent Framework Validation、Real Repo Issue Agent Toy 和 Real mini-SWE-agent CLI Surface Validation 均已有单独 completed run；在标准 full runner 中因未安装对应依赖而保守 skipped。

## 实验清单与状态

下面的条目混合了三类状态：

- `标准库模拟已完成`：可支撑流程、trace 字段和失败模式的窄结论，但不能证明真实模型或真实框架表现。
- `真实 harness 已准备`：脚本入口已存在；无 API key 或未接入真实框架时只能说明入口可运行或会保守跳过。
- `真实实验待跑`：需要真实 API、真实框架、真实数据、成本/延迟记录或人工复核后，才能升级更宽的工程结论。

1. Tool calling 参数错误恢复
   - 目标：观察模型生成错误参数时，schema 校验和重试策略是否有效。
   - 状态：已完成标准库模拟实验，见 [Tool Calling 参数校验与重试实验](tool-calling-validation/README.md) 和 [2026-07-11 结果](tool-calling-validation/results-2026-07-11.md)；真实 API harness 已准备，见 [Real Tool Calling 参数校验与重试实验](real-tool-calling-validation/README.md) 和 [2026-07-11 结果](real-tool-calling-validation/results-2026-07-11.md)。当前无 API key，运行结果为 `skipped`；仍需配置 API key 后记录真实模型 / API 结果。

2. RAG chunk size 对召回质量的影响
   - 目标：比较不同 chunk size 和 overlap 对答案准确率的影响。
   - 状态：已完成标准库最小 pipeline / citation 模拟实验，见 [RAG 最小 Pipeline 与 Citation 实验](rag-pipeline/README.md) 和 [2026-07-11 结果](rag-pipeline/results-2026-07-11.md)；真实 LLM citation synthesis harness 已准备，见 [Real RAG Citation Synthesis 实验](real-rag-citation-validation/README.md) 和 [2026-07-11 结果](real-rag-citation-validation/results-2026-07-11.md)，当前无 API key，运行结果为 `skipped`；已完成本地 LlamaIndex `VectorStoreIndex` / retriever / source-node metadata run，见 [Real LlamaIndex RAG Source-Node Validation](real-llamaindex-rag-validation/README.md) 和 [2026-07-11 结果](real-llamaindex-rag-validation/results-2026-07-11.md)。仍需真实 LLM synthesis completed run、真实 embedding / vector store / rerank 和 chunk size 对比实验。

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
   - 状态：已完成标准库 prompt injection / tool permission 模拟实验，见 [Prompt Injection 与工具权限最小实验](prompt-injection-permission/README.md) 和 [2026-07-11 结果](prompt-injection-permission/results-2026-07-11.md)；已完成标准库安全 regression set 最小实验，见 [安全 Regression Set 最小实验](security-regression-set/README.md) 和 [2026-07-11 结果](security-regression-set/results-2026-07-11.md)；已完成标准库审批状态恢复与幂等性实验，见 [审批状态恢复与幂等性实验](approval-state-recovery/README.md) 和 [2026-07-11 结果](approval-state-recovery/results-2026-07-11.md)；已完成 Real LangGraph Interrupt Recovery `MemorySaver` 最小 run 和 `SqliteSaver` 本地 SQLite 同进程 graph 重建恢复 case、双本地 Python 进程 prepare/resume case 和双本地 Python 进程并发 resume case；真实 API harness 已准备，见 [Real Prompt Injection 与工具权限实验](real-prompt-injection-permission/README.md) 和 [2026-07-11 结果](real-prompt-injection-permission/results-2026-07-11.md)。当前无 API key，真实 prompt-injection API 运行结果为 `skipped`；仍需配置 API key 后记录真实模型 / 框架 guardrail / 部署式 HITL approval 结果。

7. MCP 最小 trace 实验
   - 目标：验证 host/client/server、`tools/list`、`tools/call`、`resources/list`、`resources/read`、roots 和 host approval trace 字段。
   - 状态：已完成标准库模拟实验，见 [MCP 最小 Trace 实验](mcp-trace/README.md) 和 [2026-07-11 结果](mcp-trace/results-2026-07-11.md)；本地 stdio JSON-RPC harness 已完成，见 [Real MCP Stdio Trace 实验](real-mcp-stdio-trace/README.md) 和 [2026-07-11 结果](real-mcp-stdio-trace/results-2026-07-11.md)；官方 MCP Python SDK stdio harness 已完成，见 [Real MCP SDK Trace 实验](real-mcp-sdk-trace/README.md) 和 [2026-07-11 结果](real-mcp-sdk-trace/results-2026-07-11.md)。本地结果支撑进程边界、JSON-RPC / SDK 消息流、tools/resources/prompts、host approval/resource review 和 trace 脱敏的窄结论；仍需真实 host UI / OAuth / URL mode / sampling / tunnel 实验。

8. Trace-aware eval 最小实验
   - 目标：比较 final-answer-only scoring 和 trace-aware scoring 能发现的错误类型差异。
   - 状态：已完成标准库模拟实验，见 [Trace-Aware Eval 最小实验](trace-aware-eval/README.md) 和 [2026-07-11 结果](trace-aware-eval/results-2026-07-11.md)；已完成标准库 trace schema audit，见 [Trace Schema Audit 最小实验](trace-schema-audit/README.md) 和 [2026-07-11 结果](trace-schema-audit/results-2026-07-11.md)；已完成标准库 grader misalignment / reward hacking audit，见 [Grader Misalignment / Reward Hacking 最小实验](grader-misalignment/README.md) 和 [2026-07-11 结果](grader-misalignment/results-2026-07-11.md)；真实模型 trace-aware eval harness 已准备，见 [Real Trace-Aware Eval 实验](real-trace-aware-eval/README.md) 和 [2026-07-11 结果](real-trace-aware-eval/results-2026-07-11.md)。当前无 API key，运行结果为 `skipped`；仍需配置 API key 后记录真实 Agent trace、真实 LLM-as-judge、平台 grader 和人工复核结果。

9. Reflection / Retry 错误反思实验
   - 目标：验证 reflection 是否能帮助补证据，以及未验证反思是否会污染后续尝试。
   - 状态：已完成标准库 Reflection / Retry 模拟实验，见 [Reflection / Retry 与错误反思实验](reflection-retry/README.md) 和 [2026-07-11 结果](reflection-retry/results-2026-07-11.md)。仍需真实模型 / critic / framework / 长期 episodic memory 实验。

10. 多 Agent 与 Flow 控制对比实验
    - 目标：验证多角色协作是否抵消通信、重复读取和冲突处理成本。
    - 状态：已完成标准库多 Agent / Flow 控制模拟实验，见 [多 Agent 与 Flow 控制对比实验](multi-agent-comparison/README.md) 和 [2026-07-11 结果](multi-agent-comparison/results-2026-07-11.md)；已完成 AutoGen AgentChat / CrewAI 的本地 fake-model runtime run，见 [Real Multi-Agent Framework Validation](real-multi-agent-framework-validation/README.md) 和 [2026-07-12 结果](real-multi-agent-framework-validation/results-2026-07-12.md)。当前结果只支撑 researcher/reviewer team / crew 编排表面和 trace 输出形状；仍需真实模型、多轮冲突合并、LangGraph multi-agent、token/latency/cost 和人工评审负担实验。

11. 上下文治理与结构化输出实验
    - 目标：比较 free text、JSON mode、schema validation 和 naive/governed context 的失败模式。
    - 状态：已完成标准库上下文治理与结构化输出模拟实验，见 [上下文治理与结构化输出实验](context-structured-output/README.md) 和 [2026-07-11 结果](context-structured-output/results-2026-07-11.md)；已完成标准库上下文策略对比实验，见 [上下文策略对比实验](context-strategy-comparison/README.md) 和 [2026-07-11 结果](context-strategy-comparison/results-2026-07-11.md)；真实 API harness 已准备，见 [Real Structured Outputs / JSON Mode 对比实验](real-structured-output-validation/README.md) 和 [2026-07-11 结果](real-structured-output-validation/results-2026-07-11.md)。当前无 API key，运行结果为 `skipped`；仍需配置 API key 后记录真实 Responses API / Structured Outputs / refusal / retry / 长上下文成本结果。

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
    - 状态：固定 workflow baseline 和确定性 workflow-agent hybrid baseline 已完成，见 [Real Repo Issue Agent Toy 实验](real-repo-issue-agent-toy/README.md) 和 [2026-07-12 结果](real-repo-issue-agent-toy/results-2026-07-12.md)。本次创建临时 toy repo，初始 3 failed / 2 passed，修复后 5 passed，只修改实现文件并记录 diff/trajectory；hybrid baseline 记录建议、人工审批、拒绝不必要环境读取、scoped diff 和复跑测试。尚未运行 mini-SWE-agent、SWE-agent 或真实模型，不能证明任何 coding agent 默认可靠。

16. Real mini-SWE-agent CLI surface validation 实验
    - 目标：验证 mini-SWE-agent 是否能作为临时依赖安装，并暴露本地 CLI、confirm/yolo/cost/config/output 等关键选项和默认配置表面。
    - 状态：真实 harness 已完成 CLI surface run，见 [Real mini-SWE-agent CLI Surface Validation](real-mini-swe-agent-cli-validation/README.md) 和 [2026-07-12 结果](real-mini-swe-agent-cli-validation/results-2026-07-12.md)。本次用 `mini-swe-agent==2.4.5` 验证 `mini-swe-agent --help`、关键 options、默认 `mode: confirm` 和 `cost_limit:`；没有运行 repo issue 任务、模型调用、sandbox、trajectory browser、成本或延迟实验。

17. LangGraph interrupt recovery 实验
    - 目标：验证 LangGraph `interrupt()`、checkpointer、`thread_id` 和 `Command(resume=...)` 在高风险工具审批流程中的恢复、幂等和审计边界。
    - 状态：真实 harness 已完成 `MemorySaver` 最小 run 和 `SqliteSaver` 本地 SQLite 同进程 graph 重建恢复 case、双本地 Python 进程 prepare/resume case 和双本地 Python 进程并发 resume case，见 [Real LangGraph Interrupt Recovery 实验](real-langgraph-interrupt-recovery/README.md) 和 [2026-07-11 结果](real-langgraph-interrupt-recovery/results-2026-07-11.md)。它覆盖批准、拒绝、参数 hash、重复恢复不重复执行、trace 脱敏和本地 SQLite 同进程/双进程恢复和并发 resume 观察；不能证明 LangGraph interrupt、checkpointer 或任何 HITL 框架默认生产安全，部署式服务重启、真实服务并发恢复和真实副作用仍待验证。

18. LangGraph memory store 实验
    - 目标：验证 LangGraph `InMemoryStore` 的 namespace、`put` / `get` / `search` / `delete`、应用层编辑历史和 trace 脱敏边界。
    - 状态：真实 harness 已完成本地 `InMemoryStore` run，见 [Real LangGraph Memory Store Validation](real-langgraph-memory-store-validation/README.md) 和 [2026-07-12 结果](real-langgraph-memory-store-validation/results-2026-07-12.md)。它支撑 store 原语和应用层治理包装的窄观察；同时显示 broad prefix search 可看到多个 user namespace，跨用户授权不能假设由 store 自动完成。真实多会话质量、模型使用记忆、持久化、UI、合规删除、成本和延迟仍待验证。

19. Agentic security regression set 实验
    - 目标：把 MITRE ATLAS 和 OWASP Agentic AI resources 中的 agentic-specific 风险整理成可迁移到真实模型 / 框架的安全 case matrix。
    - 状态：已完成标准库 toy runtime，见 [Real Agentic Security Regression Set 实验](real-agentic-security-regression-set/README.md) 和 [2026-07-11 结果](real-agentic-security-regression-set/results-2026-07-11.md)。尚未运行真实模型或真实框架；不能证明任何 mitigation、detector、guardrail、HITL、sandbox、runtime containment 或 monitoring 有效。

20. Production safety / data governance checklist 实验
    - 目标：把 Moderation、Safety Best Practices 和 Data Controls 文档中的生产安全与数据治理边界整理成可审计 checklist。
    - 状态：已完成标准库 checklist audit，见 [Production Safety / Data Governance Checklist](production-safety-data-governance/README.md) 和 [2026-07-11 结果](production-safety-data-governance/results-2026-07-11.md)。尚未读取真实 project / account 配置；不能证明任何 moderation、HITL、数据保留、data residency 或合规方案有效。

21. Production cost / latency / rate-limit audit 实验
    - 目标：把 Production、Cost、Latency、Rate Limits、Token Counting、Batch、Flex 和 Prompt Caching 文档中的生产质量边界整理成可审计字段表。
    - 状态：已完成标准库 field audit，见 [Production Cost / Latency / Rate-Limit Audit](production-cost-latency-rate-limit/README.md) 和 [2026-07-11 结果](production-cost-latency-rate-limit/results-2026-07-11.md)；真实 API harness 已准备，见 [Real Production Cost / Latency / Rate-Limit Validation](real-production-cost-latency-validation/README.md)、[2026-07-11 结果](real-production-cost-latency-validation/results-2026-07-11.md)、[Real Batch / Flex / Prompt Caching Validation](real-batch-flex-caching-validation/README.md) 和 [2026-07-11 结果](real-batch-flex-caching-validation/results-2026-07-11.md)。当前无 API key，真实 harness 只验证 skip 分支；尚未调用真实 API、读取真实 rate-limit headers、提交 Batch job、使用 Flex 或触发 Prompt Caching；不能证明任何真实成本、P95 latency、吞吐、缓存命中率、优化收益或生产可靠性。

22. Browser action trace audit 实验
    - 目标：把 Browser Use、Playwright、Anthropic Computer Use 和权限 / observability evidence 中的 browser agent 边界整理成可审计 action trace 字段表。
    - 状态：已完成标准库 field audit，见 [Browser Action Trace Audit](browser-action-trace-audit/README.md) 和 [2026-07-11 结果](browser-action-trace-audit/results-2026-07-11.md)。标准库 audit 不启动真实浏览器；真实浏览器固定 workflow 已由下一项 Playwright harness 覆盖。该 audit 不能证明真实网页任务成功率、点击精度、classifier 效果、CAPTCHA/2FA/stealth、成本、延迟、合规或生产可靠性。

23. Real Browser Playwright validation 实验
    - 目标：在本地 demo page 上用固定 Playwright workflow 收集真实 browser action trace、DOM/screenshot state、文件上传、提交审批和失败分类，作为 Browser Use / computer-use-style action loop 的后续对照组。
    - 状态：真实 harness 已完成固定本地 demo page run，见 [Real Browser Playwright Validation](real-browser-playwright-validation/README.md) 和 [2026-07-11 结果](real-browser-playwright-validation/results-2026-07-11.md)。本次记录 4 条 action record、DOM/screenshot hash、redacted invoice 文件上传、submit order 审批阻断和 trace.zip metadata；它只证明固定 Playwright workflow 的动作/trace 记录入口，不证明 Browser Use、Anthropic computer use、任何模型、真实网站或生产网页任务表现。

24. Real Batch / Flex / Prompt Caching validation 实验
    - 目标：为 Batch API、Flex processing 和 Prompt Caching 准备真实 API 观测入口，记录 `custom_id` / batch status、Flex fallback、`cached_tokens` / `cache_write_tokens`、latency 和 rate-limit headers。
    - 状态：真实 harness 已准备，见 [Real Batch / Flex / Prompt Caching Validation](real-batch-flex-caching-validation/README.md) 和 [2026-07-11 结果](real-batch-flex-caching-validation/results-2026-07-11.md)。当前无 API key，运行结果为 `skipped`；Batch job 提交默认 opt-in，尚未产生真实 completed run，不能证明 Batch / Flex / Prompt Caching 的收益、命中率、成本、延迟、质量取舍或生产可靠性。

25. Real Moderation safety validation 实验
    - 目标：为 OpenAI Moderation API 准备真实安全信号观测入口，记录 `flagged`、categories、scores、latency、expected mismatch、tool arguments / tool output 覆盖和 policy decision。
    - 状态：真实 harness 已准备，见 [Real Moderation Safety Validation](real-moderation-safety-validation/README.md) 和 [2026-07-11 结果](real-moderation-safety-validation/results-2026-07-11.md)。当前无 API key，运行结果为 `skipped`；尚未产生真实 moderation completed run，不能证明误报、漏报、阈值策略、人工复核流程或生产安全效果。

26. Real Semantic Kernel plugin validation 实验
    - 目标：用 Semantic Kernel Python native plugin 验证 plugin/function metadata、参数 required/type 处理、应用层写工具审批和 side-effect trace。
    - 状态：真实 harness 已完成单独本地 run，见 [Real Semantic Kernel Plugin Validation](real-semantic-kernel-plugin-validation/README.md) 和 [2026-07-12 结果](real-semantic-kernel-plugin-validation/results-2026-07-12.md)。它支撑 native plugin runtime 的窄观察：metadata 暴露、缺参/不可解析类型拒绝、可解析字符串数值执行、未审批写工具不转发、已审批写工具产生 side effect。它不证明真实模型 tool selection、OpenAPI/MCP plugin、Agent Framework、Process Framework、HITL UI、参数快照、幂等恢复、成本、延迟或生产安全。

27. Real Framework Same-Task Comparison 实验
    - 目标：用同一个本地退款政策检索 + 审批退款任务，对比 OpenAI Agents SDK、LangGraph、LlamaIndex 和 Semantic Kernel 的真实 runtime surface，并拆分 framework-owned 与 application-owned capabilities。
    - 状态：真实 harness 已完成 4 adapter 本地 run，见 [Real Framework Same-Task Comparison](real-framework-same-task-comparison/README.md) 和 [2026-07-12 结果](real-framework-same-task-comparison/results-2026-07-12.md)。本次记录 OpenAI Agents SDK `FunctionTool` schema / `needs_approval` / direct `ToolContext` invocation / fake-model `Runner` approval-resume loop、LangGraph `StateGraph` / conditional edge、LlamaIndex `VectorStoreIndex` / retriever source nodes、Semantic Kernel plugin metadata / `Kernel.invoke()`；四个 adapter 均阻断未审批退款、执行一次已审批退款且 trace 未泄露示例 secret。由于 `openai-agents==0.18.2` 与 `semantic-kernel==1.36.0` 在同一临时环境中存在 pydantic import 组合问题，结果使用两组命令覆盖 4 个 adapter。它不证明真实模型行为、成本、延迟、hosted tracing、真实 HITL UI、部署恢复、OpenAPI/MCP plugin 或生产安全，也不能推出框架排名。

## 实验记录要求

- 明确假设。
- 明确输入数据。
- 记录模型、框架和版本。
- 保存 trace 或日志。
- 记录成功率、成本、延迟和失败类型。
- 结论必须说明适用边界。
