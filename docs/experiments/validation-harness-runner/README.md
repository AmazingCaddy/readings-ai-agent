# Validation Harness Runner

## 目标

统一运行当前手册中的真实 / 准真实验证 harness，生成一个小型状态摘要，避免后续长时间验证时漏跑某个入口。

## 运行方式

```bash
uv run python docs/experiments/validation-harness-runner/run_validation_harnesses.py
```

没有 `OPENAI_API_KEY` 时，依赖真实 API 的 harness 应返回 `skipped`；没有 Playwright 时，真实浏览器 harness 应返回 `skipped`；没有 LangGraph 时，真实 LangGraph harness 应返回 `skipped`；Batch 提交必须显式 opt-in；不依赖 API 的本地 stdio MCP harness 应返回 `completed`。

若要在不修改项目依赖的情况下运行 LangGraph harness，可使用临时依赖：

```bash
uv run --with langgraph --with langchain-core python docs/experiments/validation-harness-runner/run_validation_harnesses.py
```

最新记录：见 [2026-07-11 结果](results-2026-07-11.md)。本次运行验证了统一入口、API harness 的 skip 分支、LangGraph `MemorySaver` 最小 run、`SqliteSaver` 同进程本地 SQLite graph 重建恢复 case、`SqliteSaver` 双本地 Python 进程 prepare/resume case 和本地 MCP stdio harness；没有完成真实 API 行为验证。

## 覆盖范围

- Real Tool Calling 参数校验与重试
- Real Structured Outputs / JSON Mode 对比
- Real Prompt Injection 与工具权限
- Real RAG Citation Synthesis
- Real Trace-Aware Eval
- Real Production Cost / Latency / Rate-Limit Validation
- Real Browser Playwright Validation
- Real Batch / Flex / Prompt Caching Validation
- Real LangGraph Interrupt Recovery
- Real Moderation Safety Validation
- Real MCP Stdio Trace

## 结论状态

runner 只证明 harness 可以被统一调用，并不证明真实 API / 框架结论已经完成。只有在对应 harness 实际返回可审计结果后，才能同步 source card、claim ledger、coverage matrix 和章节正文。
