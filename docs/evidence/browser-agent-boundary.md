# Evidence Note: Browser Agent 与网页自动化边界

## 要验证的结论

Browser Agent 是高风险的工具型 Agent：它把模型决策连接到真实网页动作、登录态、表单、文件、购物和第三方站点。Playwright / browser-use 这类工具能提供浏览器动作和 trace，但不能单独证明 Agent 在长程网页任务中可靠、安全或合规。

## 资料来源

- Source 1：[Browser Use and Playwright Browser Automation References](../sources/source-cards/2026-browser-use-playwright.md)
- Source 2：[WebArena: A Realistic Web Environment for Building Autonomous Agents](../sources/source-cards/2023-webarena-paper.md)
- Source 3：[Evidence Note: Agent Eval 与 Trajectory 边界](agent-eval-trajectory-boundary.md)
- Source 4：[Evidence Note: 工具权限、人工确认与审计边界](tool-permission-audit-boundary.md)
- Source 5：[Evidence Note: Observability 与 Trace 工程边界](observability-trace-boundary.md)

## 交叉验证结果

- 一致点：Browser Use README 将浏览器 Agent 的动作面描述为打开页面、点击按钮、输入文本和填表，并展示求职表单、购物和网页搜索类任务。这说明 browser agent 会触达真实网页交互和外部副作用。
- 一致点：Browser Use README / docs 提到 real browser profiles、saved logins、profile sync、persistent browser state、2FA、file/workspace、human-in-the-loop、MCP server 和 production hosting。这支持正文中把浏览器 Agent 视为权限和数据边界更复杂的工具型 Agent。
- 一致点：Playwright actions docs 支持文本输入、选择、点击、键盘、文件上传、拖拽和滚动等浏览器动作；trace viewer docs 支持按 action 回放 trace、查看页面状态、log、source、network 和 DOM snapshot。这说明浏览器自动化可以提供可复盘的动作轨迹。
- 一致点：WebArena 摘要强调 web agent 任务是 long-horizon、diverse、需要 functional correctness 的端到端环境；这支持“浏览器 Agent 不能只看最终文本，需要看网页状态和过程”的评测边界。
- 一致点：Agent eval evidence 和 trace evidence 已确认，对会调用工具或产生外部副作用的 Agent，只看最终答案不足以验证过程安全；关键 trajectory / trace 应进入 eval、审计和回归输入。浏览器 Agent 是这一边界的典型场景。
- 一致点：tool permission evidence 支持高风险动作要使用最小权限、参数校验、人工确认、审批状态恢复和审计 trace。浏览器 Agent 的表单提交、购物、文件上传、登录态操作和删除/发布按钮都应归入高风险动作集合。
- 边界：Browser Use README 中的 benchmark、leaderboard、速度、云服务和 CAPTCHA/stealth 相关 claim 来自项目自身材料，当前没有独立复现；不能用作本手册中真实质量、成本、延迟或生产可靠性的确定性证据。
- 边界：Playwright 是执行和测试工具，不是 Agent runtime；它能支撑 browser action / trace 设计，不能证明模型的网页规划、任务理解或错误恢复能力。

## 实验验证

- 是否需要实验：是
- 实验设计：在本地 demo website 上实现同一任务的两个版本：固定 Playwright workflow 和 Browser Use browser agent。任务包括只读信息提取、表单填写但不提交、需要确认后提交、文件上传、错误元素、外部页面注入和登录态 profile。记录 browser action trace、DOM state、tool decisions、approval、cost、latency、失败分类和敏感字段脱敏。
- 结果：尚未完成真实实验。当前只有文档和 source card 交叉验证，不能证明 Browser Use 或任意浏览器 Agent 的真实成功率、稳定性、成本、CAPTCHA/stealth 或生产可靠性。

## 结论状态

- 可入正文：窄结论“浏览器 Agent 的执行层包括导航、点击、输入、选择、上传、滚动等网页动作；这些动作应被记录为可复盘 trace，并进入 eval、审计和回归测试”由 Browser Use / Playwright 文档、WebArena 和现有 eval/trace evidence 支撑。
- 可入正文：窄结论“浏览器 Agent 不能只用最终文本或 demo 成功判断可靠性；登录态、cookies、文件、表单提交、购物/支付、第三方站点 ToS、CAPTCHA/风控和 destructive button 都需要权限、人工确认、隔离 profile、测试账号和 trace 脱敏”由 Browser Use 文档和工具权限 evidence 支撑。
- 部分验证：Browser Use benchmark / leaderboard / hosted model claims、真实网页任务成功率、CAPTCHA/stealth、成本、延迟、合规、跨站点稳定性和生产可靠性仍需真实实验与独立评测。

## 可进入章节

- 是。可以写成：Browser Agent 是工具型 Agent 的高风险实践方向。Playwright/browser-use 能提供动作层和 trace，但可靠性必须通过任务级 eval、浏览器状态检查、权限确认、测试账号、隔离 profile、审计和人工复核来验证。不能写成“用了 browser-use / Playwright 就能可靠自动完成网页任务”。
