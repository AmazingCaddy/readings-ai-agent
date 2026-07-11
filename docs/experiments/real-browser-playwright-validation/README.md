# Real Browser Playwright Validation

## 目标

把 Browser Action Trace Audit 的字段模板推进到真实浏览器固定 workflow：在本地 demo page 上用 Playwright 记录真实 action、DOM hash、screenshot hash、文件上传、提交审批、外部页面指令边界、trace.zip 和失败分类。

当前 harness 只覆盖固定 Playwright workflow，不运行 Browser Use，不调用 Anthropic computer use，也不调用任何模型。

## 当前状态

- Harness 已准备：`real_browser_playwright_validation.py`
- 当前本地运行状态：`completed`。2026-07-11 使用临时 Playwright 依赖和本地 Chromium headless shell 跑通固定 demo page workflow，生成 4 条 action record 和 trace.zip。
- 结果页：[2026-07-11 结果](results-2026-07-11.md)

## 运行方式

```bash
uv run --with playwright python docs/experiments/real-browser-playwright-validation/real_browser_playwright_validation.py
```

如果 Playwright browser binaries 尚未安装，先执行：

```bash
uv run --with playwright playwright install chromium
```

依赖齐全后，脚本会：

1. 创建临时本地 demo page。
2. 启动本地 HTTP server。
3. 用 Chromium 打开页面。
4. 读取商品价格。
5. 填写表单但不提交。
6. 上传一个临时 redacted invoice 文件。
7. 阻断 submit order 动作，记录 `pending` approval。
8. 生成 Playwright trace.zip，并记录 action records。

## 记录字段

- action trace：URL、action type、selector、action result、timestamp
- page state：DOM hash、screenshot hash、before/after state
- side-effect approval：risk level、approval required/status、side effect
- profile isolation：temporary Playwright context、test account、cookie scope、domain allowlist
- file upload control：file name、file type policy、upload approval
- external content boundary：页面注入文本作为 untrusted data，记录 ignored instruction
- redaction：敏感输入、cookie、文件内容不写入 trace records
- failure classification：expected/actual outcome、failure type、recovery action

## 结论边界

- 可支撑：真实 Playwright 固定 workflow 可以作为 browser agent 对照组入口；本次 completed run 收集了真实 browser action trace、DOM/screenshot hash、文件上传、审批阻断和 trace.zip metadata。
- 当前不能支撑：本次只验证固定 demo page 和固定 Playwright workflow；不能证明 Browser Use、Anthropic computer use、任意模型、真实网站、CAPTCHA/2FA/stealth、classifier、防护层、成本、延迟、合规或生产可靠性。

## 下一步

1. 在同一 demo page 上增加 Browser Use browser agent 对照。
2. 可选增加 computer-use-style action loop，对比 screenshot/coordinate action、approval burden、trace readability、成本和延迟。
3. 增加错误元素、登录态 profile、下载/删除类按钮和截图注入 case。
