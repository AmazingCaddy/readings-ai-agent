# 实验与复现

实验用于验证工程结论，而不是展示 demo。

## 候选实验

1. Tool calling 参数错误恢复
   - 目标：观察模型生成错误参数时，schema 校验和重试策略是否有效。
   - 状态：已完成标准库模拟实验，见 [Tool Calling 参数校验与重试实验](tool-calling-validation/README.md) 和 [2026-07-11 结果](tool-calling-validation/results-2026-07-11.md)。仍需真实模型 / API 实验。

2. RAG chunk size 对召回质量的影响
   - 目标：比较不同 chunk size 和 overlap 对答案准确率的影响。
   - 状态：已完成标准库最小 pipeline / citation 模拟实验，见 [RAG 最小 Pipeline 与 Citation 实验](rag-pipeline/README.md) 和 [2026-07-11 结果](rag-pipeline/results-2026-07-11.md)。仍需真实 embedding / vector store / LLM synthesis 和 chunk size 对比实验。

3. Long-term memory 写入守门
   - 目标：验证自动写入记忆是否会引入冲突、过时和脏数据。

4. ReAct vs 简单 workflow
   - 目标：比较工具搜索任务中 ReAct 和固定 workflow 的成功率、成本和延迟。

5. Planner/Executor vs 单 Agent
   - 目标：验证任务拆解是否提高复杂任务完成率，还是增加错误传播。

6. Prompt injection 基线测试
   - 目标：验证工具型 Agent 在恶意文档或外部输入下是否会越权。
   - 状态：已完成标准库 prompt injection / tool permission 模拟实验，见 [Prompt Injection 与工具权限最小实验](prompt-injection-permission/README.md) 和 [2026-07-11 结果](prompt-injection-permission/results-2026-07-11.md)。仍需真实模型 / 框架 guardrail / HITL approval 实验。

7. MCP 最小 trace 实验
   - 目标：验证 host/client/server、`tools/list`、`tools/call`、`resources/list`、`resources/read`、roots 和 host approval trace 字段。
   - 状态：已完成标准库模拟实验，见 [MCP 最小 Trace 实验](mcp-trace/README.md) 和 [2026-07-11 结果](mcp-trace/results-2026-07-11.md)。仍需真实 MCP SDK / host 实验。

8. Trace-aware eval 最小实验
   - 目标：比较 final-answer-only scoring 和 trace-aware scoring 能发现的错误类型差异。
   - 状态：已完成标准库模拟实验，见 [Trace-Aware Eval 最小实验](trace-aware-eval/README.md) 和 [2026-07-11 结果](trace-aware-eval/results-2026-07-11.md)。仍需真实 Agent trace、LLM-as-judge 误判和人工复核实验。

## 实验记录要求

- 明确假设。
- 明确输入数据。
- 记录模型、框架和版本。
- 保存 trace 或日志。
- 记录成功率、成本、延迟和失败类型。
- 结论必须说明适用边界。
