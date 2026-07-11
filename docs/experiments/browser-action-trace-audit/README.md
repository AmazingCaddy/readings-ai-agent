# Browser Action Trace Audit

## 目标

把 Browser Use、Playwright、Anthropic Computer Use 和本手册权限 / observability evidence 中的浏览器 Agent 边界，整理成一个可运行的 action trace 字段审计。

这个实验不是为了证明 Browser Use、Playwright、computer-use-style agent 或任何模型能稳定完成网页任务，而是为了验证：浏览器 Agent 练习和评测至少应该记录哪些动作、页面状态、权限、审批、文件上传、外部内容和脱敏字段。

## 实验边界

当前实验是 Python 标准库 deterministic audit。它不会启动浏览器，不调用 Playwright，不运行 Browser Use，不调用 Anthropic API，不读取真实 DOM / screenshot，也不测真实点击精度、CAPTCHA、2FA、stealth、成本、延迟或合规。

## 资料来源

- [Browser Use and Playwright Browser Automation References](../../sources/source-cards/2026-browser-use-playwright.md)
- [Anthropic Computer Use Tool Documentation](../../sources/source-cards/2026-anthropic-computer-use-docs.md)
- [Evidence Note: Browser Agent 与网页自动化边界](../../evidence/browser-agent-boundary.md)
- [Evidence Note: Agent Eval 与 Trajectory 边界](../../evidence/agent-eval-trajectory-boundary.md)
- [Evidence Note: 工具权限、人工确认与审计边界](../../evidence/tool-permission-audit-boundary.md)

## 检查项

| rule id | 重点 | 必查字段 |
| --- | --- | --- |
| `action_trace` | 浏览器任务要能按动作复盘。 | url、action type、selector/coordinates、action result、timestamp |
| `page_state` | 评测不能只看最终文本。 | DOM snapshot hash、screenshot hash、before/after state |
| `approval_for_side_effects` | 提交、上传、付款、删除等动作需要审批状态。 | risk level、approval required/status、side effect |
| `profile_isolation` | 真实 profile 和登录态不能随便暴露。 | profile type、test account、cookie scope、domain allowlist |
| `file_upload_control` | 文件上传需要独立策略。 | file upload、file name、file type allowed、upload approved |
| `external_content_untrusted` | 网页和截图文字是数据，不是系统指令。 | external content、injection detected、tool result boundary、ignored external instruction |
| `sensitive_trace_redaction` | trace 本身可能泄密。 | sensitive inputs redacted、cookie redacted、secret leaked、retention note |
| `failure_classification` | 失败要能分类和恢复。 | expected/actual outcome、failure type、recovery action |

## 运行方式

```bash
uv run python docs/experiments/browser-action-trace-audit/browser_action_trace_audit.py
```

当前标准库结果见 [2026-07-11 结果](results-2026-07-11.md)。

## 对照组

- `naive_trace`：只记录少量 URL、action type、selector 和 final text；缺少页面状态、审批、profile 隔离、文件上传策略、外部注入处理、trace 脱敏和失败分类。
- `governed_trace`：记录 URL、selector、DOM/screenshot hash、before/after state、approval、profile isolation、file upload policy、external content boundary、redaction 和 failure classification。

## 结论状态

- 当前状态：标准库 audit 已完成；真实 browser / computer-use 练习待跑。
- 可支撑：章节和实践路线可以写成“浏览器 Agent 评测至少应记录 action trace、页面状态、审批、profile 隔离、文件上传策略、外部内容不可信边界、敏感字段脱敏和失败分类”。
- 不能支撑：不能证明 Browser Use、Playwright、Anthropic computer use 或任何模型在真实网站任务中的成功率、点击精度、classifier 效果、CAPTCHA/2FA/stealth 处理、成本、延迟、合规或生产可靠性。

## 下一步

1. 准备本地 demo site，覆盖只读、表单填写但不提交、需要确认后提交、文件上传和 destructive button。
2. 用固定 Playwright workflow 记录真实 trace.zip、DOM/screenshot state 和失败分类。
3. 再对比 Browser Use 或 computer-use-style action loop，记录成功率、步骤数、审批负担、成本、延迟和敏感字段脱敏。
