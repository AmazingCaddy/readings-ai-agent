# Chapter Evidence Alignment Audit

## 目标

检查 01-11 章的正文证据控制是否和 claim ledger / coverage matrix 保持对齐。

这个 harness 不验证外部事实，也不判断章节解释是否完全正确；它只检查章节层面的证据结构、待验证问题、控制文件引用和边界文字是否没有明显回退。

## 检查项

- 每个内容章节都包含非空的 `已验证结论` section。
- 每个内容章节都包含非空的 `待验证问题` section。
- 每个内容章节都从 References 链接到 claim ledger。
- 每个内容章节都从 References 链接到 coverage matrix。
- `已验证结论` 中提到 `可入正文` 的 bullet 必须保留边界词。
- `已验证结论` 中提到真实系统、生产、成本、延迟、可靠性或默认行为的 bullet 必须保留边界词。

## 运行方式

```bash
uv run python docs/experiments/chapter-evidence-alignment-audit/chapter_evidence_alignment_audit.py
```

## 当前结果

当前结果见 [2026-07-12 结果](results-2026-07-12.md)。

该 audit 可支撑“章节正文的证据控制入口和边界文字具备基本一致性”的窄结论；不能证明外部资料事实正确、章节解释正确、真实模型 / API / 框架行为、成本、延迟、安全或生产可靠性。
