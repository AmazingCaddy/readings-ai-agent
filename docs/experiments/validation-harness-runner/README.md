# Validation Harness Runner

## 目标

统一运行当前手册中的真实 / 准真实验证 harness，生成一个小型状态摘要，避免后续长时间验证时漏跑某个入口。

## 运行方式

```bash
uv run python docs/experiments/validation-harness-runner/run_validation_harnesses.py
```

没有 `OPENAI_API_KEY` 时，依赖真实 API 的 harness 应返回 `skipped` 或运行明确标记的本地 deterministic control。Real Tool Calling 会改跑本地 validation/retry fixtures，Real Structured Outputs / JSON Mode 会改跑本地 schema/semantic fixtures，Real Prompt Injection / Permission 会改跑本地 tool-permission fixtures，Real RAG Citation Synthesis 会改跑本地 deterministic citation verifier control、Real Trace-Aware Eval 会改跑本地 deterministic scorer control、Real Production Cost / Latency / Rate-Limit 会改跑本地 deterministic accounting control、Real Batch / Flex / Prompt Caching 会改跑本地 cache/flex/batch metadata fixtures、Real Moderation Safety 会改跑本地 deterministic policy-signal control，并分别标记 `real_model_validated=false` 或 `real_api_validated=false`；没有 OpenAI Agents SDK 时，Real OpenAI Agents SDK Guardrail Validation 应返回 `skipped`；没有 Playwright 时，真实浏览器 harness 应返回 `skipped`；没有 Browser Use 时，Real Browser Use Package Surface Validation 应返回 `skipped`；没有 LangGraph 时，真实 LangGraph harness 应返回 `skipped`；没有 `mcp` Python package 时，官方 MCP SDK harness 应返回 `skipped`；没有 `llama-index-core` 时，真实 LlamaIndex RAG harness 应返回 `skipped`；没有 `semantic-kernel` 时，真实 Semantic Kernel plugin harness 和 same-task comparison 的 Semantic Kernel adapter 应返回 `skipped`；没有 `autogen-agentchat` / `crewai` 时，Real Multi-Agent Framework Validation 应跳过对应 adapter，但有 LangGraph 时可完成 LangGraph adapter；没有 `pytest` 时，Real Repo Issue Agent Toy 应保守 `skipped`；没有 `mini-swe-agent` 时，Real mini-SWE-agent CLI Surface Validation 应保守 `skipped`；没有 `mini-swe-agent` 或 `pytest` 时，Real mini-SWE-agent Runtime Surface Validation 应保守 `skipped`；Batch 提交必须显式 opt-in；不依赖 API 的本地 stdio MCP harness 应返回 `completed`。

若要在不修改项目依赖的情况下运行 OpenAI Agents SDK、LangGraph、Playwright 和官方 MCP SDK harness，可使用临时依赖：

```bash
uv run --with openai-agents==0.18.2 --with playwright --with mcp --with llama-index-core --with langgraph --with langchain-core --with langgraph-checkpoint-sqlite python docs/experiments/validation-harness-runner/run_validation_harnesses.py
```

Semantic Kernel harness 建议单独运行：

```bash
uv run --with semantic-kernel python docs/experiments/real-semantic-kernel-plugin-validation/real_semantic_kernel_plugin_validation.py
```

原因是 `semantic-kernel` 与当前 full runner 的临时依赖集合可能触发独立 dependency resolution / import 组合问题；full runner 中该入口可以保守 `skipped`，不影响单独 completed result 的证据状态。

Semantic Kernel adapter 的 same-task comparison 建议单独运行：

```bash
uv run --with langgraph --with llama-index-core --with semantic-kernel python docs/experiments/real-framework-same-task-comparison/real_framework_same_task_comparison.py
```

full runner 的标准临时依赖集合未包含 `semantic-kernel`，因此 same-task comparison 在 full runner 中通常完成 OpenAI Agents SDK / LangGraph / LlamaIndex adapter，并保守跳过 Semantic Kernel adapter。`openai-agents==0.18.2` 与 `semantic-kernel==1.36.0` 在同一临时环境中会触发 pydantic import 组合问题，因此该实验结果页使用两组命令覆盖 4 个 adapter。

AutoGen / CrewAI / LangGraph multi-agent harness 建议单独运行：

```bash
uv run --with autogen-agentchat --with crewai --with langgraph python docs/experiments/real-multi-agent-framework-validation/real_multi_agent_framework_validation.py
```

full runner 的标准临时依赖集合包含 `langgraph`，但未包含 `autogen-agentchat` 或 `crewai`，因此该入口在 full runner 中通常完成 LangGraph adapter，并保守跳过 AutoGen/CrewAI adapter；单独 completed run 见对应结果页。

Repo Issue Agent toy harness 建议单独运行：

```bash
uv run --with pytest python docs/experiments/real-repo-issue-agent-toy/real_repo_issue_agent_toy.py
```

full runner 的标准临时依赖集合未包含 `pytest`，因此该入口在 full runner 中通常保守跳过；单独 completed run 见对应结果页。

mini-SWE-agent CLI surface harness 建议单独运行：

```bash
uv run --with mini-swe-agent python docs/experiments/real-mini-swe-agent-cli-validation/real_mini_swe_agent_cli_validation.py
```

full runner 的标准临时依赖集合未包含 `mini-swe-agent`，因此该入口在 full runner 中通常保守跳过；单独 completed run 只验证 CLI / 默认配置表面，不运行 repo issue 或模型任务。

mini-SWE-agent runtime surface harness 建议单独运行：

```bash
uv run --with mini-swe-agent --with pytest python docs/experiments/real-mini-swe-agent-runtime-validation/real_mini_swe_agent_runtime_validation.py
```

full runner 的标准临时依赖集合未包含 `mini-swe-agent` 和 `pytest`，因此该入口在 full runner 中通常保守跳过；单独 completed run 只验证 deterministic fake-model runtime、LocalEnvironment、toy repo mutation、pytest feedback 和 trajectory shape，不调用真实模型或验证 confirm-mode。

Browser Use package surface harness 建议单独运行：

```bash
uv run --with browser-use python docs/experiments/real-browser-use-package-validation/real_browser_use_package_validation.py
```

full runner 的标准临时依赖集合未包含 `browser-use`，因此该入口在 full runner 中通常保守跳过；单独 completed run 只验证 package metadata、console scripts 和源码表面，不启动浏览器或模型任务。

最新记录：见 [2026-07-12 结果](results-2026-07-12.md)。本次运行验证了统一入口、API harness 的 skip / control 分支、Real Tool Calling 本地 deterministic validation/retry control、Real Structured Outputs / JSON Mode 本地 deterministic schema/semantic control、Real Prompt Injection / Permission 本地 deterministic tool-permission control、Real RAG Citation Synthesis 本地 deterministic verifier control、Real Trace-Aware Eval 本地 deterministic scorer control、Real Production Cost / Latency / Rate-Limit 本地 deterministic accounting control、Real Batch / Flex / Prompt Caching 本地 deterministic cache/flex/batch metadata control、Real Moderation Safety 本地 deterministic policy-signal control、Real OpenAI Agents SDK Guardrail completed run、Real LlamaIndex RAG Source-Node completed run、Real Browser Playwright 固定 demo page + deterministic computer-use-style loop completed run、LangGraph `MemorySaver` 最小 run、`SqliteSaver` 同进程本地 SQLite graph 重建恢复 case、`SqliteSaver` 双本地 Python 进程 prepare/resume case、`SqliteSaver` 双本地 Python 进程并发 resume case、Real LangGraph Memory Store completed run、Real Framework Same-Task Comparison 的 OpenAI Agents SDK / LangGraph / LlamaIndex adapter、Real Multi-Agent Framework Validation 的 LangGraph adapter、本地 MCP stdio harness、官方 MCP Python SDK stdio harness、Claim Boundary Consistency Audit、Chapter Evidence Alignment Audit、Claim To Chapter Landing Audit、Source Reference Integrity Audit、Source To Claim Support Audit 和 Source Card Evidence Quality Audit；runner 现在会把 `all_passed=false` 的 harness 计为失败，避免文本 audit 静默回归。Real Tool Calling 现在覆盖 schema-valid 但业务非法参数、错误反馈、修正参数和单次工具执行的本地 fixtures，但仍不覆盖真实 Responses API tool-call generation 或模型修正行为；Real Structured Outputs / JSON Mode 现在覆盖 parse failure、schema-valid semantic error 和 schema-valid semantic-ok 三个本地 fixtures，但仍不覆盖真实 Responses API / JSON mode / Structured Outputs 行为；Real Prompt Injection / Permission 现在覆盖固定 tool calls、危险写工具请求计数、prompt-only toy side effects、policy-enforced 写工具拒绝和 trace 脱敏，但仍不覆盖真实模型 prompt-injection 易感性、真实 detector / guardrail / HITL 效果、hosted tool 行为、成本或延迟；Real RAG Citation Synthesis 现在覆盖 citation id、quote matching、grounded/ungrounded citation 和 unsupported grounded claim 的 verifier 失败样例，但仍不覆盖真实 LLM citation faithfulness；Real Trace-Aware Eval 现在覆盖 final-only vs trace-aware 的本地规则差异，但仍不覆盖真实模型或平台 eval；Real Production Cost / Latency / Rate-Limit 现在覆盖 usage/cache 字段提取、rate-limit header 解析、平均 / P95 latency、成本估算和 budget action 的本地聚合逻辑，但仍不覆盖真实 API 成本、延迟或限流；Real Batch / Flex / Prompt Caching 现在覆盖 cache usage 字段聚合、Flex fallback 记录、Batch JSONL metadata 和 `custom_id` 检查，但仍不覆盖真实 Prompt Caching hit rate、Flex availability、Batch submission/completion、成本收益、延迟、吞吐或质量；Real Moderation Safety 现在覆盖 moderation result fields、category scores、`category_applied_input_types` 和 allow / block-review / false-positive-review / false-negative-fallback policy decision 分支，但仍不覆盖真实 Moderation API 分类质量；Claim Boundary Consistency Audit 覆盖 claim ledger / coverage matrix / selected chapter stale phrase 的本地文本一致性检查；Chapter Evidence Alignment Audit 覆盖章节 `已验证结论` / `待验证问题`、claim ledger / coverage matrix 链接和章节结论边界措辞；Claim To Chapter Landing Audit 覆盖 29 条 `可入正文` 结论和 50 个声明章节落点；Source Reference Integrity Audit 覆盖 62 张 source cards、source-card index、source-card 元数据/段落、章节 references 和 340 个本地 Markdown 链接解析；Source To Claim Support Audit 覆盖 01-11 内容章节直接引用的 61 张 source cards 到 claim ledger `支撑资料` 列的文本追溯；Source Card Evidence Quality Audit 覆盖 39 张进入正文 source cards 的支撑证据、风险段落和边界措辞；这些文本 audit 都不验证外部事实或真实系统表现。LlamaIndex run 覆盖本地 `VectorStoreIndex` / retriever / QueryEngine / `MockLLM` / source-node metadata，但仍不覆盖真实 LLM citation faithfulness；Browser Playwright run 覆盖 8 条 action record、坐标校验和 destructive action 阻断，但仍不覆盖真实模型或 Browser Use agent；Semantic Kernel plugin harness、Real Repo Issue Agent Toy、Real mini-SWE-agent CLI Surface Validation、Real mini-SWE-agent Runtime Surface Validation 和 Real Browser Use Package Surface Validation 在 full runner 中保守 skipped，但都有单独 completed run；Real Multi-Agent Framework Validation 已用单独命令完成 AutoGen/CrewAI/LangGraph 三个 adapter；same-task comparison 已用第二组命令完成 Semantic Kernel adapter；没有完成真实 API 行为验证。

## 覆盖范围

- Real Tool Calling 参数校验与重试
- Real OpenAI Agents SDK Guardrail Validation
- Real Structured Outputs / JSON Mode 对比
- Real Prompt Injection 与工具权限
- Real RAG Citation Synthesis
- Real LlamaIndex RAG Source-Node Validation
- Real Trace-Aware Eval
- Real Production Cost / Latency / Rate-Limit Validation
- Real Browser Playwright Validation
- Real Browser Use Package Surface Validation
- Real Batch / Flex / Prompt Caching Validation
- Real LangGraph Interrupt Recovery
- Real LangGraph Memory Store Validation
- Real Semantic Kernel Plugin Validation
- Real Framework Same-Task Comparison
- Real Multi-Agent Framework Validation
- Real Repo Issue Agent Toy
- Real mini-SWE-agent CLI Surface Validation
- Real mini-SWE-agent Runtime Surface Validation
- Real Moderation Safety Validation
- Real MCP Stdio Trace
- Real MCP SDK Trace
- Claim Boundary Consistency Audit
- Chapter Evidence Alignment Audit
- Claim To Chapter Landing Audit
- Source Reference Integrity Audit
- Source To Claim Support Audit
- Source Card Evidence Quality Audit

## 结论状态

runner 只证明 harness 可以被统一调用，并不证明真实 API / 框架结论已经完成。只有在对应 harness 实际返回可审计结果后，才能同步 source card、claim ledger、coverage matrix 和章节正文。
