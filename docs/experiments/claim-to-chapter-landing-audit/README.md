# Claim To Chapter Landing Audit

## 目标

检查 claim ledger 中每条 `可入正文` 结论是否真的落到它声明的目标章节，而不是只停留在台账或章节 References 里。

这个 harness 不验证外部资料事实，也不替代人工精读；它只把容易回归的正文落点做成可运行检查：

- 每条 `可入正文` 结论必须在 `正文写法` 中声明目标章节。
- 每个目标章节编号必须能解析到实际章节文件。
- 每条结论必须在每个声明目标章节中有足够具体的短语命中，不能只靠 `Agent`、`MCP`、`trace` 等泛词。

## 运行方式

```bash
uv run python docs/experiments/claim-to-chapter-landing-audit/claim_to_chapter_landing_audit.py
```

## 结果解释

- `all_passed=true`：没有发现 `可入正文` 结论缺目标章节或缺正文落点。
- `real_fact_validation=false`：该检查只验证文本落点，不验证资料事实、章节解释或真实模型/API/框架行为。
- `missing_landings`：列出需要补章节正文或修正 claim ledger 目标章节的结论。

## 当前结论

当前结果见 [2026-07-12 结果](results-2026-07-12.md)。

该 audit 可支撑“claim ledger 与章节正文之间有机器可检查的落点防回归”这一窄结论；不能支撑任何真实模型质量、API 行为、框架可靠性、安全效果、成本、延迟或生产效果结论。
