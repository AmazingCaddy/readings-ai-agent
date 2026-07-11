# Browser Use and Playwright Browser Automation References

- 来源链接：https://github.com/browser-use/browser-use
- 相关链接：https://docs.browser-use.com；https://playwright.dev/python/docs/intro；https://playwright.dev/python/docs/input；https://playwright.dev/python/docs/trace-viewer-intro
- 作者 / 机构：Browser Use project；Microsoft Playwright project
- 发布时间：Browser Use repo created 2024-10-31；Playwright documentation 持续更新
- 最后复核日期：2026-07-11
- 类型：Source / Engineering docs
- 主题：Browser Agent / Browser Automation / Web Agent / Trace
- 适合阶段：进阶 / 实践扩展
- 可信度等级：B
- 是否已验证：Browser Use GitHub metadata、README、docs `llms.txt`、Playwright Python installation/actions/trace viewer 页面已复核；标准库 Browser Action Trace Audit 已完成字段审计；真实 Playwright harness 已准备但当前因未安装 Playwright 只验证 skip 分支；支撑浏览器 Agent 的动作层、浏览器 profile/auth、custom tools、云端托管、trace、审批、文件上传策略、外部内容边界、脱敏和失败分类边界；README benchmark / leaderboard / hosted model claims 未独立复现，真实任务成功率、成本、延迟、CAPTCHA/stealth、合规和安全仍部分验证

## 一句话总结

Browser Use 和 Playwright 适合说明浏览器 Agent 的工程执行层：Agent 可以打开网页、点击、输入、填表、上传文件并记录 trace，但这些能力不等于网页任务默认可靠或安全。

## 核心结论

- Browser Use README 将项目定位为让 AI agent 像人一样使用 web browser：打开页面、点击按钮、输入文本和填表。
- Browser Use 提供 Python library 入口：开发者定义 natural-language task，传入 LLM，运行 `Agent(...).run()`。
- Browser Use README 展示了求职表单、购物、PC 配件搜索等网页任务示例；这些例子说明浏览器 Agent 的任务面包含表单填写、购物车、比较搜索和个人助理式网页操作。
- Browser Use 支持 custom tools，开发者可以把额外动作注册给 Agent；这意味着浏览器动作和普通工具权限需要统一治理。
- Browser Use README 区分 CLI 和 Python library：一次性任务可通过已有 agent / CLI 使用，重复自动化和产品集成更适合 Python library。
- Browser Use README 讨论 authentication：可复用真实 Chrome profile、同步 auth profile、处理临时账号和 inbox。这说明 browser agent 往往会接触登录态、cookies、localStorage 和用户账号边界。
- Browser Use docs `llms.txt` 描述 Cloud SDK 是 managed API for AI browser automation，并列出 live preview / recording、persistent browser state、2FA、MCP server、webhooks、human-in-the-loop、structured output 和 deterministic rerun 等能力。
- Browser Use README 的 benchmark、leaderboard、速度和 hosted model claims 来自项目自身材料，当前只能作为候选工程资料；本手册不把这些数字写成独立验证结论。
- Playwright Python docs 提供浏览器自动化和测试基础：安装 Playwright / pytest plugin、安装 browsers、用 `page.goto`、`get_by_role(...).click()`、断言页面标题和 heading。
- Playwright actions docs 支持常见浏览器动作：文本输入、checkbox/radio、select、mouse click、keyboard、upload files、focus、drag and drop、scrolling。
- Playwright trace viewer docs 支持记录浏览器执行 trace，并可按 action 回放页面状态、查看 log、source、network 和 DOM snapshot。
- 本地标准库 Browser Action Trace Audit 显示，最小浏览器 Agent 评测字段应覆盖 action trace、DOM/screenshot state、side-effect approval、profile isolation、file upload control、external content untrusted boundary、sensitive trace redaction 和 failure classification。
- 对本手册而言，稳妥结论是：浏览器 Agent 需要把 browser state、auth、cookies、file upload/download、表单提交、支付/购物、外部网站条款、trace、人工确认和回滚纳入设计；不能只用“能点击网页”证明任务可靠。

## 支撑证据

- 2026-07-11 使用 GitHub API 抓取 `browser-use/browser-use` repo metadata 成功；repo 为 public、MIT license、Python 项目，topics 包含 `ai-agents`、`browser-automation`、`llm`、`playwright`。
- 2026-07-11 抓取 Browser Use README 成功；README 写明 Browser Use lets an AI agent use a web browser the same way you do，并列出 opens pages、clicks buttons、types、fills in forms。
- Browser Use README 包含 Python library quickstart，示例使用 `Agent(task=..., llm=...)` 和 `await agent.run()`。
- Browser Use README 包含 custom tools 示例，使用 `Tools()` 和 `@tools.action(...)` 注册自定义工具。
- Browser Use README FAQ 说明可使用 real browser profiles 复用 saved logins，并提供 sync auth profile 到 remote browser 的命令方向。
- Browser Use README 的 production FAQ 提到 Chrome 内存消耗和并行运行管理困难，并把 scalable browser infrastructure、proxy rotation、stealth browser fingerprinting、parallel execution 作为 Cloud API 能力。
- Browser Use docs `llms.txt` 返回 HTTP 200，列出 Cloud SDK、Agent、structured output、live messages、human-in-the-loop、persistent browser state、2FA、MCP server、webhooks 等页面。
- `https://docs.browser-use.com/open-source/introduction` 返回 HTTP 200，HTTP header 提供 `llms.txt` 和 `llms-full.txt` 链接。
- Playwright home 和 Python docs 返回 HTTP 200；Python intro 页面包含 install Playwright / browsers、example test、`page.goto`、`get_by_role(...).click()`、assert heading 等示例。
- Playwright actions 页面包含 text input、checkboxes/radio buttons、select options、mouse click、keys/shortcuts、upload files、focus、drag and drop、scrolling 等动作目录。
- Playwright trace viewer 页面说明可用 `--tracing` 或 `context.tracing.start(...)` / `stop(...)` 记录 trace，并用 trace viewer 按 action 回看页面状态、log、source、network 和 DOM snapshot。
- 2026-07-11 运行 [Browser Action Trace Audit](../../experiments/browser-action-trace-audit/README.md) 成功；`naive_trace` 0/8 通过，`governed_trace` 8/8 通过。该结果只支撑字段设计，不启动真实浏览器、不调用 Playwright / Browser Use / Anthropic API，也不读取真实 DOM 或 screenshot。
- 2026-07-11 准备 [Real Browser Playwright Validation](../../experiments/real-browser-playwright-validation/README.md) harness；当前环境未安装 Playwright，结果为 `skipped`。该入口尚未产生真实 browser completed run。

## 可能的问题

- Browser Use README 含有 benchmark、leaderboard、hosted model 和 cloud product claims，这些不是独立评测结果；正文只能作为项目自述，不能当成已验证性能。
- 浏览器 Agent 可能处理登录态、cookies、localStorage、文件上传/下载、购物、表单提交、邮箱、支付和第三方网站数据；权限和合规风险高于普通只读 RAG。
- Playwright 是浏览器自动化和测试框架，不是 Agent runtime。它能支撑动作执行和 trace，但不证明模型能稳定规划网页任务。
- Browser Action Trace Audit 是标准库字段审计，不是 browser agent benchmark。它不能证明 Browser Use、Playwright workflow、computer-use-style action loop 或任意模型的真实网页任务表现。
- CAPTCHA、反自动化、网站 ToS、账号风控和代理/stealth 是真实系统问题；本手册当前没有复现实验。
- 使用真实浏览器 profile 会扩大敏感数据暴露面。初学者练习应使用测试账号、隔离 profile、只读任务和人工确认。

## 初学者阅读建议

- 先读 WebArena source card 和本手册第 08/09 章，理解 Web Agent 评测和安全边界。
- 再读 Browser Use README 的 What can Browser Use do、Python library、FAQ 中 authentication / production 小节。
- Playwright docs 重点看 actions 和 trace viewer；它们帮助理解 browser agent 背后的可执行动作和可复盘 trace。
- 不建议初学者直接让 browser agent 使用真实账号购物、投递、付款或发送表单；先用 demo site、测试账号和只读任务。

## 可复现实验

- 使用 Playwright 在本地 demo page 上实现固定 workflow：打开页面、填写表单、点击提交、记录 trace.zip，并检查 DOM 状态。
- 使用 Browser Use 在同一 demo page 上运行一个自然语言任务，对比固定 Playwright workflow 与 browser agent 的步骤数、失败原因、trace 可读性、成本、延迟和是否需要人工确认。
- 设计安全 case：登录态 profile、文件上传、购物车、表单提交、外部页面 prompt injection、CAPTCHA / 2FA、误点击 destructive button，记录 allow/block/require_approval 和 trace 脱敏。
- 当前已完成无浏览器字段审计，并准备了真实 Playwright harness；下一步仍需要安装 Playwright 后运行 completed case，再扩展真实 demo site 对照实验来记录 trace.zip、真实 DOM/screenshot state、成本、延迟和失败样例。

## 是否进入正文

- 结论：部分进入
- 原因：可作为 Web/Browser Agent 工程执行层、browser automation trace、auth/profile 风险和实践项目的 reference；与 WebArena、Agent eval evidence、tool permission evidence 和 Browser Action Trace Audit 共同支撑“浏览器 Agent 不能只看最终结果，必须看动作 trace、页面状态、权限、外部副作用、脱敏和失败分类”的边界。不能支撑 Browser Use benchmark 数字、云服务能力、真实点击精度、CAPTCHA/stealth 效果、生产可靠性或模型网页任务成功率。
