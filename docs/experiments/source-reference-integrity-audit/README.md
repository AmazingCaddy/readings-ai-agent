# Source Reference Integrity Audit

## 目标

检查 source cards、source-card index、source-card 目录页、MkDocs Source Cards 导航、章节 references 和本地 Markdown 链接的结构完整性。

这个 harness 不联网，也不验证外部资料本身是否仍正确；它只验证本手册内部的 references 是否可追溯、是否没有明显断链或漏索引。

## 检查项

- Source-card index 中的每个 `source-cards/*.md` 链接都指向存在的文件。
- `docs/sources/source-cards/` 下的每张资料卡片都被 source-card index 收录，排除目录页 `index.md`。
- `docs/sources/source-cards/index.md` 列出每张资料卡片，排除目录页自身。
- `mkdocs.yml` 的 Source Cards 导航列出每张资料卡片，避免 GitHub Pages 导航漏挂。
- 每张 source card 都包含基础元数据：来源链接、最后复核日期、类型、主题、可信度等级、是否已验证。
- 每张 source card 都包含 `一句话总结`、`核心结论` 和 `是否进入正文` 三个结构段落。
- 每张 source card 至少包含一个外部 URL，以便追溯原始资料。
- 每个编号章节都有 `References` section；01-11 章至少链接一张 source card。
- Source cards、source-card index 和章节中的本地 Markdown 链接都能解析到存在的本地文件。

## 运行方式

```bash
uv run python docs/experiments/source-reference-integrity-audit/source_reference_integrity_audit.py
```

## 当前结果

当前结果见 [2026-07-12 结果](results-2026-07-12.md)。

该 audit 可支撑“手册 references 结构具备本地可追溯性，且 source cards 在目录页和 MkDocs 导航中可发现”的窄结论；不能证明外部 URL 当前可访问、资料内容正确、章节解释正确、真实模型 / API / 框架行为、成本、延迟或生产可靠性。
