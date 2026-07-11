# Real Browser Use Package Surface Validation 实验

## 目标

验证 Browser Use 是否能作为临时依赖安装，并暴露可用于 Browser Agent 练习的 Python package / console script / 源码表面。

本实验只检查 package metadata、console scripts 和选定源码文件中的关键类与配置表面。它不导入 `browser_use`，不启动 Playwright / Chromium，不调用模型，不打开网站，也不运行 Browser Use agent 任务。

## 运行方式

```bash
uv run --with browser-use python docs/experiments/real-browser-use-package-validation/real_browser_use_package_validation.py
```

没有 `browser-use` 包时，脚本返回 `skipped`。

## 检查项

- 包版本可通过 `importlib.metadata` 读取。
- console scripts 包含 `browser-use`、`browser`、`browseruse` 和 `bu`。
- `browser_use/agent/service.py` 包含 `class Agent`、`allowed_domains` 和 `sensitive`。
- `browser_use/browser/profile.py` 包含 `class BrowserProfile`、`allowed_domains` 和 `highlight_elements`。
- `browser_use/tools/service.py` 包含 `class Tools` 和 `sensitive`。
- `browser_use/cli.py` 包含 `def main` 和 `browser-use`。
- 输出不泄露示例 secret marker。

## 支撑边界

可支撑：Browser Use 的本地包入口、console script 入口、Agent / BrowserProfile / Tools 源码表面、allowed domains / sensitive data 等安全相关关键词可以在本机临时依赖环境中观察到。

不可支撑：Browser Use 能完成网页任务、模型能正确规划点击、CLI help 稳定可交互、真实网站可用性、登录态/profile 安全、文件上传/下载安全、CAPTCHA/stealth、成本、延迟、合规或生产可靠性。

## 后续

下一步应在 Real Browser Playwright Validation 的同一本地 demo page 上运行 Browser Use browser agent 对照，记录模型、任务、动作 trace、DOM/screenshot state、approval、失败分类、成本、延迟和敏感字段脱敏。
