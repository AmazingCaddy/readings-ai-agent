# Evidence Note: Browser Agent 与网页自动化边界

## 要验证的结论

Browser Agent 是高风险的工具型 Agent：它把模型决策连接到真实网页动作、登录态、表单、文件、购物和第三方站点。Playwright / browser-use 这类工具能提供浏览器动作和 trace，但不能单独证明 Agent 在长程网页任务中可靠、安全或合规。

## 资料来源

- Source 1：[Browser Use and Playwright Browser Automation References](../sources/source-cards/2026-browser-use-playwright.md)
- Source 2：[WebArena: A Realistic Web Environment for Building Autonomous Agents](../sources/source-cards/2023-webarena-paper.md)
- Source 3：[Evidence Note: Agent Eval 与 Trajectory 边界](agent-eval-trajectory-boundary.md)
- Source 4：[Evidence Note: 工具权限、人工确认与审计边界](tool-permission-audit-boundary.md)
- Source 5：[Evidence Note: Observability 与 Trace 工程边界](observability-trace-boundary.md)
- Source 6：[Anthropic Computer Use Tool Documentation](../sources/source-cards/2026-anthropic-computer-use-docs.md)
- Source 7：[Real Browser Use Package Surface Validation 结果](../experiments/real-browser-use-package-validation/results-2026-07-12.md)

## 交叉验证结果

- 一致点：Browser Use README 将浏览器 Agent 的动作面描述为打开页面、点击按钮、输入文本和填表，并展示求职表单、购物和网页搜索类任务。这说明 browser agent 会触达真实网页交互和外部副作用。
- 一致点：Browser Use README / docs 提到 real browser profiles、saved logins、profile sync、persistent browser state、2FA、file/workspace、human-in-the-loop、MCP server 和 production hosting。这支持正文中把浏览器 Agent 视为权限和数据边界更复杂的工具型 Agent。
- 一致点：Real Browser Use Package Surface Validation 验证 `browser-use==0.13.3` 可通过临时依赖安装，并暴露 `browser-use` / `browser` / `bu` 等 console scripts；源码表面包含 `Agent`、`BrowserProfile`、`Tools`、`allowed_domains`、`sensitive` 和 `highlight_elements`。这补强 Browser Use 的本地入口和安全相关配置表面，但不证明 agent task 行为。
- 一致点：Playwright actions docs 支持文本输入、选择、点击、键盘、文件上传、拖拽和滚动等浏览器动作；trace viewer docs 支持按 action 回放 trace、查看页面状态、log、source、network 和 DOM snapshot。这说明浏览器自动化可以提供可复盘的动作轨迹。
- 一致点：WebArena 摘要强调 web agent 任务是 long-horizon、diverse、需要 functional correctness 的端到端环境；这支持“浏览器 Agent 不能只看最终文本，需要看网页状态和过程”的评测边界。
- 一致点：Anthropic computer use 文档把 screenshot、mouse、keyboard 和 desktop automation 作为工具动作面，并说明开发者需要在自己的 computer / container / VM 中执行 tool request，再把 screenshot 或 command output 作为 `tool_result` 回传。这与 Playwright / Browser Use 的“动作层和 trace 层必须由应用治理”的边界一致。
- 一致点：Anthropic computer use security considerations 建议 dedicated VM/container、minimal privileges、避免敏感登录信息、domain allowlist，以及对金融交易、同意条款、接受 cookies 等有现实后果或需要 affirmative consent 的任务做人工确认。这补强了浏览器/桌面 Agent 的权限隔离和确认边界。
- 一致点：Anthropic 文档明确说明网页或图片中的指令可能 override 开发者指令或 cause mistakes，并提到 screenshot prompt injection classifier 会引导模型在继续动作前请求用户确认；但文档同时强调即使有 classifier defense layer，隔离和确认仍然重要，且 classifier 是 Anthropic computer use 文档中的供应商防护层，不是通用浏览器 Agent 默认能力。
- 一致点：Anthropic 文档给出 validate actions before running them 和 log actions for debugging 的应用侧模式，并在 limitations 中列出 latency、computer vision accuracy、tool selection reliability、coordinate / scrolling / spreadsheet limitations 和 vulnerabilities。这支持“真实 browser/computer-use 任务必须看 action log、页面状态、坐标/视觉错误和失败分类”的评测设计。
- 一致点：Anthropic 文档的 data retention 段落把 computer use 定义为 client-side tool：screenshots、mouse actions、keyboard inputs 和 session files 存在开发者环境中；同时 Anthropic 会实时处理 API 请求中的 screenshot images 和 action requests，保留边界按 API data retention 执行。文档还说明功能 eligible for ZDR，但需要组织已有 ZDR arrangement。
- 一致点：Anthropic 文档的 pricing 段落给出 system prompt overhead 466-499 tokens、Claude 4.x tool definition 735 input tokens，并提醒 screenshot images 和 tool execution results 会产生额外 token consumption。这支持把 browser/computer-use 的成本记录纳入 trace，而不是只记录动作是否成功。
- 一致点：Agent eval evidence 和 trace evidence 已确认，对会调用工具或产生外部副作用的 Agent，只看最终答案不足以验证过程安全；关键 trajectory / trace 应进入 eval、审计和回归输入。浏览器 Agent 是这一边界的典型场景。
- 一致点：tool permission evidence 支持高风险动作要使用最小权限、参数校验、人工确认、审批状态恢复和审计 trace。浏览器 Agent 的表单提交、购物、文件上传、登录态操作和删除/发布按钮都应归入高风险动作集合。
- 边界：Browser Use README 中的 benchmark、leaderboard、速度、云服务和 CAPTCHA/stealth 相关 claim 来自项目自身材料，当前没有独立复现；不能用作本手册中真实质量、成本、延迟或生产可靠性的确定性证据。
- 边界：Playwright 是执行和测试工具，不是 Agent runtime；它能支撑 browser action / trace 设计，不能证明模型的网页规划、任务理解或错误恢复能力。
- 边界：Anthropic computer use 是 beta 产品文档；screenshot classifier、模型点击精度、真实桌面任务成功率、真实成本、延迟、ZDR/data-retention 安排和生产可靠性都需要真实试跑或合同/配置层复核，不能自动泛化到其他 browser agent。

## 实验验证

- 是否需要实验：是
- 已完成：标准库 [Browser Action Trace Audit](../experiments/browser-action-trace-audit/README.md)。该 audit 比较 `naive_trace` 和 `governed_trace`：`naive_trace` 0/8 通过，`governed_trace` 8/8 通过，覆盖 action trace、page state、side-effect approval、profile isolation、file upload control、external content untrusted boundary、sensitive trace redaction 和 failure classification。
- 支撑范围：该结果支撑“浏览器 Agent 练习和评测需要记录哪些字段”的窄结论。
- 已完成：真实 [Real Browser Playwright Validation](../experiments/real-browser-playwright-validation/README.md) harness。2026-07-11 completed run 使用本地 demo page 和 Playwright Chromium headless，生成 8 条 action record 和 trace.zip；覆盖固定 workflow 的读价格、填表不提交、上传 redacted invoice、submit order 被策略阻断，也覆盖 deterministic computer-use-style loop 的 screenshot/DOM observe、坐标点击前 `elementFromPoint` 校验、坐标填写 name、submit 坐标动作审批阻断和 delete-account destructive action 阻断；记录 DOM/screenshot hash、临时 context、`127.0.0.1` allowlist、外部页面指令作为 untrusted data 和 trace 脱敏字段。
- 已完成：真实 [Real Browser Use Package Surface Validation](../experiments/real-browser-use-package-validation/README.md) harness。2026-07-12 completed run 使用临时 `browser-use` 依赖，记录 package metadata、console scripts 和源码表面；它不导入 `browser_use`，不启动浏览器，不调用模型，也不打开网站。
- 仍需实验：在同一本地 demo website 上把 Browser Use browser agent 和真实模型驱动 computer-use-style action loop 与已完成的固定 Playwright workflow / deterministic loop 对照。任务包括只读信息提取、表单填写但不提交、需要确认后提交、文件上传、错误元素、外部页面/截图注入和登录态 profile。记录 browser action trace、DOM / screenshot state、tool decisions、action validation、approval、cost、latency、失败分类和敏感字段脱敏。
- 结果边界：已完成 Browser Use package surface run 和真实 Playwright 固定 workflow / deterministic computer-use-style loop run，但尚未完成真实模型 / Browser Use agent / Anthropic computer-use completed run。当前标准库 audit 不启动浏览器；Browser Use package harness 不运行 agent；真实 Playwright harness 只验证本地 demo page、固定脚本和 deterministic loop，不验证模型规划、Browser Use task、Anthropic computer use、真实网站、登录态、classifier、成本或延迟。这些结果都不能证明任意浏览器 Agent 的真实成功率、点击精度、classifier 行为、成本、CAPTCHA/stealth、合规或生产可靠性。

## 结论状态

- 可入正文：窄结论“浏览器 Agent 的执行层包括导航、点击、输入、选择、上传、滚动等网页动作；这些动作应被记录为可复盘 trace，并进入 eval、审计和回归测试”由 Browser Use / Playwright 文档、WebArena 和现有 eval/trace evidence 支撑。
- 可入正文：窄结论“浏览器 / computer-use Agent 不能只用最终文本或 demo 成功判断可靠性；登录态、cookies、文件、表单提交、购物/支付、第三方站点 ToS、CAPTCHA/风控、网页/截图 prompt injection 和 destructive button 都需要权限、人工确认、隔离 profile / VM / container、测试账号和 trace 脱敏”由 Browser Use、Anthropic computer use 文档和工具权限 evidence 支撑。
- 部分验证：Browser Use 的本地 package / source surface 已完成临时依赖验证，固定 Playwright workflow 和 deterministic computer-use-style loop 的动作记录、坐标校验、策略阻断和 trace.zip 生成已完成本地真实浏览器验证；Browser Use benchmark / leaderboard / hosted model claims、Browser Use agent task 行为、Anthropic screenshot classifier 行为、真实网页/桌面任务成功率、点击精度、CAPTCHA/stealth、成本、延迟、合规、跨站点稳定性和生产可靠性仍需真实实验与独立评测。

## 可进入章节

- 是。可以写成：Browser Agent 是工具型 Agent 的高风险实践方向。Playwright/browser-use 能提供动作层和 trace，但可靠性必须通过任务级 eval、浏览器状态检查、权限确认、测试账号、隔离 profile、审计和人工复核来验证。不能写成“用了 browser-use / Playwright 就能可靠自动完成网页任务”。
