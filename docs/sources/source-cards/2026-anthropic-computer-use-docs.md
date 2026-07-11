# Anthropic Computer Use Tool Documentation

- 来源链接：https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool.md
- 页面链接：https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- 作者 / 机构：Anthropic
- 发布时间：文档持续更新；computer use beta header 包含 `computer-use-2025-11-24` 和旧版 `computer-use-2025-01-24`
- 最后复核日期：2026-07-11
- 类型：Official Docs / Tool Use / Browser and Desktop Automation
- 主题：Computer Use / Browser Agent / Desktop Automation / Security / Trace
- 适合阶段：进阶 / Browser Agent 与 Production 安全
- 可信度等级：A
- 是否已验证：官方 Markdown 页面和 HTTP metadata 已复核；标准库 Browser Action Trace Audit 已完成字段审计；支撑 computer use beta、screenshot / mouse / keyboard action model、client-side tool execution、container / VM isolation、minimal privileges、sensitive data avoidance、domain allowlist、human confirmation、screenshot prompt injection classifiers、action validation、action logging、latency / vision / coordinate / reliability limitations、data retention、token overhead、trace 脱敏和失败分类边界；不证明真实网页/桌面任务成功率、点击精度、classifier 拦截率、成本、延迟、合规或生产可靠性

## 一句话总结

Anthropic computer use 文档适合说明“让模型看屏幕并操作鼠标键盘”是高风险工具能力：执行仍在开发者控制的 VM/container 中完成，必须限制权限、隔离敏感数据、确认现实后果动作、记录动作日志，并把网页/图片里的 prompt injection 当作真实风险。

## 核心结论

- Computer use 是 beta 功能，向 Claude 暴露 screenshot capture、mouse control、keyboard input 和 desktop automation 能力。
- 文档说明 computer use 可以与 bash、text editor 等工具组合，但 computer use 专指看见并控制 desktop environments 的工具能力。
- Security considerations 明确指出 computer use 有不同于标准 API 的独特风险，联网时风险更高。
- 文档建议使用 dedicated virtual machine 或 container，并配置 minimal privileges，以降低直接系统攻击或事故风险。
- 文档建议避免给模型访问敏感数据，例如账号登录信息，以降低 information theft 风险。
- 文档建议把 internet access 限制到 domain allowlist，以减少暴露在 malicious content 下的概率。
- 对可能产生 meaningful real-world consequences 或需要 affirmative consent 的任务，例如接受 cookies、完成金融交易、同意服务条款，文档建议要求人工确认。
- 文档明确说明 Claude 在某些情况下会跟随网页或图片中的指令，即使这些指令与开发者指令冲突；这直接支撑 browser/computer-use 场景中的 prompt injection 风险。
- Anthropic 为 computer use 增加了 screenshot prompt injection classifier，检测到潜在注入时会引导模型在下一步动作前请求用户确认；但文档同时强调即使有 classifier defense layer，上述防护仍然重要。
- How computer use works 说明 API 返回 `tool_use`，开发者需要在自己的 computer/container/VM 中执行工具请求，再把 screenshot 或 command output 作为 `tool_result` 回传。
- Implementation best practices 包括验证 action 是否安全有效、记录 action type / params / result、处理截图尺寸和坐标缩放、控制截图历史以管理上下文和缓存。
- Limitations 明确包括 latency、computer vision accuracy、tool selection reliability、scrolling reliability、spreadsheet interaction、账号创建/社交平台内容限制、vulnerabilities、illegal actions 等。
- Data retention 段落说明 computer use 是 client-side tool，screenshots、mouse actions、keyboard inputs 和 session files 存储在开发者环境中；Anthropic 按 API data retention 处理 API 请求。
- Pricing 段落说明 computer use beta 会增加 system prompt overhead，tool definition 也有 token 开销，截图和 tool execution results 会产生额外 token 消耗。
- 本地标准库 Browser Action Trace Audit 把上述安全和 logging 边界拆成 action trace、DOM/screenshot state、side-effect approval、profile isolation、file upload control、external content untrusted boundary、sensitive trace redaction 和 failure classification 字段模板。

## 支撑证据

- 2026-07-11 使用 `curl -L --no-progress-meter` 抓取官方 Markdown URL 成功，页面标题为 `Computer use tool`。
- 2026-07-11 使用 `curl -L -I` 复核页面 URL，返回 HTTP 200。
- 页面开头说明 computer use provides screenshot capabilities and mouse/keyboard control for autonomous desktop interaction。
- Security considerations warning 列出 VM/container、minimal privileges、避免敏感数据、domain allowlist 和 human confirmation。
- Prompt injection 段落说明 webpages 或 images 中的指令可能 override your instructions or cause Claude to make mistakes，并要求隔离敏感数据和动作。
- Classifier 段落说明 computer use tools 会自动运行 classifiers 来标记 screenshots 中潜在 prompt injections，并 steer the model to ask for user confirmation before proceeding。
- How computer use works 说明开发者 extract tool input、evaluate the tool on a computer、return results in a `tool_result` content block。
- Computing environment 段落说明 reference implementation 使用 Docker container，并由应用接收 Claude tool use request、转换为环境动作、捕获 screenshot / command output、回传 Claude。
- Best practices 段落给出 validate actions before running them 和 log actions for debugging 的应用侧代码形态。
- Limitations 段落明确 computer use is in beta，并列出 latency、vision accuracy、tool selection reliability 和 vulnerabilities 等限制。
- Data retention 段落说明 computer use data 由开发者应用控制存储位置和方式，ZDR eligibility 取决于相应安排和 API data retention。
- 2026-07-11 运行 [Browser Action Trace Audit](../../experiments/browser-action-trace-audit/README.md) 成功；`naive_trace` 0/8 通过，`governed_trace` 8/8 通过。该结果只支撑 browser/computer-use action trace 字段设计，不调用 Anthropic API、不启动真实 VM/container，也不验证 screenshot classifier 行为。

## 可能的问题

- 这是 Anthropic 产品文档，不是独立评测；不能证明真实点击精度、任务完成率、跨网站稳定性、classifier 拦截率或生产安全效果。
- Screenshot prompt injection classifier 是供应商实现细节；正文只能写成“可以作为一层防护”，不能写成通用浏览器 Agent 默认能力。
- Browser Action Trace Audit 是标准库字段审计，不是 Anthropic computer use 实测；它不能证明真实点击精度、坐标/滚动可靠性、classifier 拦截率、成本、延迟或生产安全效果。
- Computer use 涉及真实桌面、网页、文件、账号和外部副作用；初学者练习应使用 demo site、测试账号、隔离 profile、最小权限和人工确认。
- 文档给出 token overhead 和 screenshot token 消耗方向，但本手册未实测具体成本、延迟或缓存效果。

## 初学者阅读建议

- 先读本手册第 08/09/11 章，理解 trace、权限和生产安全边界。
- 阅读本页时重点看 Security considerations、How computer use works、The computing environment、Validate actions、Log actions 和 Understand computer use limitations。
- 不要从真实账号、购物、投递、支付或重要文件开始练习；先用本地 demo 页面和容器环境。

## 可复现实验

- 在本地 demo site 上比较固定 Playwright workflow、Browser Use browser agent 和 Anthropic computer-use-style action loop 的 trace 字段、人工确认点和失败分类。
- 加入网页文本注入、截图/OCR 注入、误点击 destructive button、坐标缩放错误、登录态 profile 和文件上传 case，记录 allow/block/confirm、action log、screenshot history、成本、延迟和敏感数据脱敏。
- 如果接入 Anthropic API，必须单独记录 beta header、模型、token overhead、screenshot token usage、classifier 是否要求确认和用户确认后的动作。
- 当前已完成无 API 字段审计；真实 computer-use-style action loop 仍需单独实验记录真实 screenshot/DOM state、动作日志、确认点、成本、延迟和失败样例。

## 是否进入正文

- 结论：部分进入
- 原因：可作为 Browser/Computer-use Agent 的官方工程边界资料，支撑 sandbox / VM / container、最小权限、domain allowlist、人工确认、prompt injection classifier、action validation、action logging、limitations、data retention、token overhead、trace 脱敏和失败分类的保守正文；不能支撑真实任务成功率、点击精度、安全 classifier 效果、成本、延迟或生产可靠性结论。
