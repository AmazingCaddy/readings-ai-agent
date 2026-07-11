# Source Card Evidence Quality Audit

## 目标

检查进入正文的 source cards 是否保留可追溯证据、风险段落和边界措辞，防止把“进入正文”简化成没有证据或没有限制条件的确定性结论。

这个 harness 不联网，也不验证资料事实本身；它只检查 source card 的证据结构和边界文字是否足够明确。

## 检查项

- 标记为进入正文的 source cards 必须包含 `支撑证据` section。
- `支撑证据` section 至少包含一个 bullet，并出现可观察证据标记，例如 HTTP、抓取、复核、运行、README、arXiv 或官方文档。
- 标记为进入正文的 source cards 必须包含 `可能的问题` section。
- 标记为进入正文的 source cards 必须在进入正文、风险或后续验证段落中保留限制措辞。
- `是否已验证` 行如果提到真实系统，必须保留明确边界词。

## 运行方式

```bash
uv run python docs/experiments/source-card-evidence-quality-audit/source_card_evidence_quality_audit.py
```

## 当前结果

当前结果见 [2026-07-12 结果](results-2026-07-12.md)。

该 audit 可支撑“进入正文的 source cards 具备基本证据结构和边界文字”的窄结论；不能证明外部资料事实正确、章节解释正确、真实模型 / API / 框架行为、成本、延迟、安全或生产可靠性。
