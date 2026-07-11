# Validation Harness Runner

## 目标

统一运行当前手册中的真实 / 准真实验证 harness，生成一个小型状态摘要，避免后续长时间验证时漏跑某个入口。

## 运行方式

```bash
uv run python docs/experiments/validation-harness-runner/run_validation_harnesses.py
```

没有 `OPENAI_API_KEY` 时，依赖真实 API 的 harness 应返回 `skipped`；没有 Playwright 时，真实浏览器 harness 应返回 `skipped`；没有 LangGraph 时，真实 LangGraph harness 应返回 `skipped`；没有 `mcp` Python package 时，官方 MCP SDK harness 应返回 `skipped`；没有 `llama-index-core` 时，真实 LlamaIndex RAG harness 应返回 `skipped`；没有 `semantic-kernel` 时，真实 Semantic Kernel plugin harness 和 same-task comparison 的 Semantic Kernel adapter 应返回 `skipped`；没有 `autogen-agentchat` / `crewai` 时，Real Multi-Agent Framework Validation 应保守 `skipped`；Batch 提交必须显式 opt-in；不依赖 API 的本地 stdio MCP harness 应返回 `completed`。

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

AutoGen / CrewAI multi-agent harness 建议单独运行：

```bash
uv run --with autogen-agentchat --with crewai python docs/experiments/real-multi-agent-framework-validation/real_multi_agent_framework_validation.py
```

full runner 的标准临时依赖集合未包含 `autogen-agentchat` 或 `crewai`，因此该入口在 full runner 中通常保守跳过；单独 completed run 见对应结果页。

最新记录：见 [2026-07-12 结果](results-2026-07-12.md)。本次运行验证了统一入口、API harness 的 skip 分支、Real LlamaIndex RAG Source-Node completed run、Real Browser Playwright 固定 demo page completed run、LangGraph `MemorySaver` 最小 run、`SqliteSaver` 同进程本地 SQLite graph 重建恢复 case、`SqliteSaver` 双本地 Python 进程 prepare/resume case、`SqliteSaver` 双本地 Python 进程并发 resume case、Real LangGraph Memory Store completed run、Real Framework Same-Task Comparison 的 OpenAI Agents SDK / LangGraph / LlamaIndex adapter、本地 MCP stdio harness 和官方 MCP Python SDK stdio harness；Semantic Kernel plugin harness 和 Real Multi-Agent Framework Validation 在 full runner 中保守 skipped，但都有单独 completed run；same-task comparison 已用第二组命令完成 Semantic Kernel adapter；没有完成真实 API 行为验证。

## 覆盖范围

- Real Tool Calling 参数校验与重试
- Real Structured Outputs / JSON Mode 对比
- Real Prompt Injection 与工具权限
- Real RAG Citation Synthesis
- Real LlamaIndex RAG Source-Node Validation
- Real Trace-Aware Eval
- Real Production Cost / Latency / Rate-Limit Validation
- Real Browser Playwright Validation
- Real Batch / Flex / Prompt Caching Validation
- Real LangGraph Interrupt Recovery
- Real LangGraph Memory Store Validation
- Real Semantic Kernel Plugin Validation
- Real Framework Same-Task Comparison
- Real Multi-Agent Framework Validation
- Real Moderation Safety Validation
- Real MCP Stdio Trace
- Real MCP SDK Trace

## 结论状态

runner 只证明 harness 可以被统一调用，并不证明真实 API / 框架结论已经完成。只有在对应 harness 实际返回可审计结果后，才能同步 source card、claim ledger、coverage matrix 和章节正文。
