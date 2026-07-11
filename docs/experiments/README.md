# 实验与复现

实验用于验证工程结论，而不是展示 demo。

## 候选实验

1. Tool calling 参数错误恢复
   - 目标：观察模型生成错误参数时，schema 校验和重试策略是否有效。
   - 状态：已完成标准库模拟实验，见 [Tool Calling 参数校验与重试实验](tool-calling-validation/README.md) 和 [2026-07-11 结果](tool-calling-validation/results-2026-07-11.md)；真实 API harness 已准备，见 [Real Tool Calling 参数校验与重试实验](real-tool-calling-validation/README.md)。仍需配置 API key 后记录真实模型 / API 结果。

2. RAG chunk size 对召回质量的影响
   - 目标：比较不同 chunk size 和 overlap 对答案准确率的影响。
   - 状态：已完成标准库最小 pipeline / citation 模拟实验，见 [RAG 最小 Pipeline 与 Citation 实验](rag-pipeline/README.md) 和 [2026-07-11 结果](rag-pipeline/results-2026-07-11.md)。仍需真实 embedding / vector store / LLM synthesis 和 chunk size 对比实验。

3. Long-term memory 写入守门
   - 目标：验证自动写入记忆是否会引入冲突、过时和脏数据。
   - 状态：已完成标准库长期记忆写入守门模拟实验，见 [长期记忆写入守门与治理实验](memory-governance/README.md) 和 [2026-07-11 结果](memory-governance/results-2026-07-11.md)。仍需真实多会话 Agent / memory framework 实验。

4. ReAct vs 简单 workflow
   - 目标：比较工具搜索任务中 ReAct 和固定 workflow 的成功率、成本和延迟。
   - 状态：已完成标准库 workflow / hybrid / ReAct-like tool loop 模拟实验，见 [Workflow、Hybrid 与 ReAct-like Tool Loop 对比实验](workflow-agent-comparison/README.md) 和 [2026-07-11 结果](workflow-agent-comparison/results-2026-07-11.md)。仍需真实模型 / Agent framework / repo issue 实验。

5. Planner/Executor vs 单 Agent
   - 目标：验证任务拆解是否提高复杂任务完成率，还是增加错误传播。
   - 状态：已完成标准库 Planner / Executor 与单循环对比实验，见 [Planner / Executor 与单循环对比实验](planner-executor-comparison/README.md) 和 [2026-07-11 结果](planner-executor-comparison/results-2026-07-11.md)。仍需真实模型 / Agent framework / repo issue 实验。

6. Prompt injection 基线测试
   - 目标：验证工具型 Agent 在恶意文档或外部输入下是否会越权。
   - 状态：已完成标准库 prompt injection / tool permission 模拟实验，见 [Prompt Injection 与工具权限最小实验](prompt-injection-permission/README.md) 和 [2026-07-11 结果](prompt-injection-permission/results-2026-07-11.md)。仍需真实模型 / 框架 guardrail / HITL approval 实验。

7. MCP 最小 trace 实验
   - 目标：验证 host/client/server、`tools/list`、`tools/call`、`resources/list`、`resources/read`、roots 和 host approval trace 字段。
   - 状态：已完成标准库模拟实验，见 [MCP 最小 Trace 实验](mcp-trace/README.md) 和 [2026-07-11 结果](mcp-trace/results-2026-07-11.md)。仍需真实 MCP SDK / host 实验。

8. Trace-aware eval 最小实验
   - 目标：比较 final-answer-only scoring 和 trace-aware scoring 能发现的错误类型差异。
   - 状态：已完成标准库模拟实验，见 [Trace-Aware Eval 最小实验](trace-aware-eval/README.md) 和 [2026-07-11 结果](trace-aware-eval/results-2026-07-11.md)。仍需真实 Agent trace、LLM-as-judge 误判和人工复核实验。

9. Reflection / Retry 错误反思实验
   - 目标：验证 reflection 是否能帮助补证据，以及未验证反思是否会污染后续尝试。
   - 状态：已完成标准库 Reflection / Retry 模拟实验，见 [Reflection / Retry 与错误反思实验](reflection-retry/README.md) 和 [2026-07-11 结果](reflection-retry/results-2026-07-11.md)。仍需真实模型 / critic / framework / 长期 episodic memory 实验。

10. 多 Agent 与 Flow 控制对比实验
    - 目标：验证多角色协作是否抵消通信、重复读取和冲突处理成本。
    - 状态：已完成标准库多 Agent / Flow 控制模拟实验，见 [多 Agent 与 Flow 控制对比实验](multi-agent-comparison/README.md) 和 [2026-07-11 结果](multi-agent-comparison/results-2026-07-11.md)。仍需真实模型 / AutoGen / CrewAI / LangGraph 横向实验。

11. 上下文治理与结构化输出实验
    - 目标：比较 free text、JSON mode、schema validation 和 naive/governed context 的失败模式。
    - 状态：已完成标准库上下文治理与结构化输出模拟实验，见 [上下文治理与结构化输出实验](context-structured-output/README.md) 和 [2026-07-11 结果](context-structured-output/results-2026-07-11.md)。仍需真实 Responses API / Structured Outputs / 长上下文成本实验。

12. 实践路线 smoke harness
    - 目标：验证初学者实践项目是否能拆成结构化输出、工具校验、RAG 引用、eval cases 和成本闸门等可运行验收单元。
    - 状态：已完成标准库 smoke harness，见 [实践路线 Smoke Harness](practice-roadmap-harness/README.md) 和 [2026-07-11 结果](practice-roadmap-harness/results-2026-07-11.md)。仍需真实 Cookbook / API recipe 本地试跑。

13. 框架选择 rubric smoke test
    - 目标：验证框架比较能否从任务画像、能力标签、missing required 和 cautions 出发，而不是做框架排行榜。
    - 状态：已完成标准库 rubric smoke test，见 [框架选择 Rubric Smoke Test](framework-selection-rubric/README.md) 和 [2026-07-11 结果](framework-selection-rubric/results-2026-07-11.md)。仍需真实同一任务框架横向实验。

14. RAG、短期记忆与长期记忆对比实验
    - 目标：验证外部知识检索、当前 thread state 和跨会话 guarded memory 的适用边界。
    - 状态：已完成标准库对比实验，见 [RAG、短期记忆与长期记忆对比实验](rag-memory-comparison/README.md) 和 [2026-07-11 结果](rag-memory-comparison/results-2026-07-11.md)。仍需真实 RAG / memory framework / 多会话实验。

## 实验记录要求

- 明确假设。
- 明确输入数据。
- 记录模型、框架和版本。
- 保存 trace 或日志。
- 记录成功率、成本、延迟和失败类型。
- 结论必须说明适用边界。
