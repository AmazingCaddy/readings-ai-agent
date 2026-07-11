# Trace Schema Audit 最小实验

## 目标

验证第 08/09/11 章中的一个工程边界：trace 不是普通日志。不同用途需要不同字段：debug 需要工具调用和错误，audit 需要审批和副作用，regression 需要 dataset/case/expected/actual，RAG 需要 retrieval/citation，成本分析需要 latency/token/cost，隐私治理需要脱敏、访问范围和保留策略。

## 实验边界

这是一个确定性的标准库实验，不调用模型、不调用真实工具、不使用 LangSmith、Phoenix 或 OpenAI Evals。脚本比较 5 种固定 trace 形态：

- `minimal_log`：只保存输入和最终输出。
- `debug_trace`：足够排查工具错误，但不够做审计、回归或成本分析。
- `audit_ready_trace`：包含审批、副作用、版本、成本和脱敏字段。
- `eval_rag_trace`：包含 dataset、case、expected/actual、retrieval、citation 和失败分类。
- `privacy_leaky_trace`：字段看似可调试，但把假 secret 和邮箱写入 trace。

本实验不能证明任何真实 observability 平台的字段设计，也不能证明某个 trace schema 是通用标准。它只验证字段覆盖和隐私泄漏检查的最小结构。

## 运行方式

```bash
uv run python docs/experiments/trace-schema-audit/trace_schema_audit.py
```

## 观察点

- 最小日志是否无法支持 debug、audit、regression、RAG、成本和隐私用例。
- debug trace 是否仍缺审批、副作用、版本、成本和隐私治理字段。
- audit-ready trace 是否仍缺 dataset/case 和 retrieval/citation 字段。
- eval/RAG trace 是否能同时支持 debug、audit、regression、cost、RAG 和 privacy。
- trace 中是否出现假 secret 或邮箱等敏感值。

## 结论状态

- 支撑：可以把“trace 字段要按用途设计；debug 足够不等于 audit/eval/privacy 足够”写入第 08/09/11 章。
- 支撑：trace 字段至少应考虑 run/case/version、tool/retrieval、approval/side effect、latency/token/cost、failure category、feedback 和 privacy controls。
- 仍缺：真实 Agent traces、真实平台字段映射、LLM-as-judge 误判分析、人工复核和生产访问控制实验。
