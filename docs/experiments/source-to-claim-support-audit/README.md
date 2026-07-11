# Source To Claim Support Audit

## 目标

检查 01-11 内容章节直接引用的 source cards 是否也出现在 claim ledger 的 `支撑资料` 列中，避免章节正文引用资料但台账没有把它纳入结论证据链。

这个 harness 不验证外部资料事实，也不替代人工精读；它只把 source card 到 claim ledger 的可追溯关系做成可运行检查：

- 只扫描 01-11 内容章节，不把第 12 章 source map 的全量资料列表当成正文引用。
- 每个章节 source-card 链接必须能解析到实际文件。
- 每个章节直接引用的 source card 必须能用标题、文件名派生别名或少量显式别名，在 claim ledger `支撑资料` 列中找到。

## 运行方式

```bash
uv run python docs/experiments/source-to-claim-support-audit/source_to_claim_support_audit.py
```

## 结果解释

- `all_passed=true`：没有发现内容章节 source card 缺 claim ledger 支撑资料落点。
- `real_fact_validation=false`：该检查只验证本地文本可追溯关系，不验证 source 内容、claim 事实或章节解释正确性。
- `missing_support`：列出章节引用但没有在 claim ledger 支撑列中命中的 source card。

## 当前结论

当前结果见 [2026-07-12 结果](results-2026-07-12.md)。

该 audit 可支撑“内容章节 source cards 与 claim ledger 支撑资料之间有机器可检查的追溯关系”这一窄结论；不能支撑任何真实模型质量、API 行为、框架可靠性、安全效果、成本、延迟或生产效果结论。
