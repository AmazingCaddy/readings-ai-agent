# Source URL Availability Audit

## 目标

对 source cards 元数据中的主来源 URL 做一次活网络可达性快照，确认当前环境能访问这些原始资料入口。

这个 audit 会联网，因此结果受本地网络、目标站点限流、重定向和临时故障影响。它报告需要关注的 URL，但不把单次网络失败当成资料事实错误，也不放入默认 validation runner，避免外部网络波动影响常规验证。

## 检查项

- 从每张 source card 的 `来源链接` 元数据中抽取主 URL。
- 对每个 URL 先发起 `HEAD` 请求；如果目标返回不支持 `HEAD`，再使用 `GET` fallback。
- 记录 HTTP status、最终 URL、错误类型和需要关注的项目。
- 记录缺少主 URL 的 source cards。

## 运行方式

```bash
uv run python docs/experiments/source-url-availability-audit/source_url_availability_audit.py
```

## 当前结果

当前结果见 [2026-07-12 结果](results-2026-07-12.md)。

该 audit 可支撑“source-card 主来源链接在本次网络环境下可访问”的窄结论；不能证明资料内容正确、章节解释正确、外部页面未来仍可访问、真实模型 / API / 框架行为、成本、延迟、安全或生产可靠性。
