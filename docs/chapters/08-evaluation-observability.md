# Evaluation 与 Observability

## 本章适合谁

如果你已经能做一个会调用工具的 Agent，但不知道怎么判断它“真的能用”，这一章适合阅读。

本章不会把评测讲成一堆排行榜，而是从工程角度解释：怎样知道 Agent 做对了，错在哪里，改动有没有让系统变差。

## 你会学到什么

- Eval、benchmark 和 observability 的区别。
- 为什么 Agent 评测不能只看最终答案。
- 什么是 trace、trajectory 和 regression set。
- 如何给 Agent 错误分类。
- 为什么生产前需要小而稳定的回归测试集。

## 先用一句话理解

Evaluation 负责判断 Agent 是否完成任务，Observability 负责让你看见它是怎么完成或怎么失败的。

## 基础概念

### Evaluation

Evaluation 简称 eval，指用一组任务、标准和记录方法来评估系统表现。

对普通问答系统来说，eval 可能主要看答案是否正确。对 Agent 来说，eval 还要看工具调用、步骤顺序、权限控制、错误恢复和最终副作用。

OpenAI 的 Evaluation best practices 把 eval 解释为应对生成式 AI 变动性的 structured tests。初学者可以先记住一个简单顺序：先定义任务目标和成功标准，再收集 dataset，定义评分指标，运行和比较结果，最后把新失败样例持续加入回归集。

需要注意：OpenAI 官方 deprecations 页面已经说明 Evals platform 正在退役：2026-10-31 既有 evals 会变为 read-only，平台计划在 2026-11-30 关闭。Graders 文档也说明 eval workflow 中的 graders 属于这次过渡。因此本手册引用 OpenAI Evals / Graders 时，重点采用 eval 设计原则、trace grading、dataset/eval run 和 grader 风险边界的工程思想，不把旧平台入口写成长期稳定教程。

### Benchmark

Benchmark 是相对标准化的评测集合。它适合回答“在这个公开任务环境下，系统表现如何”。

Benchmark 的价值是可比较和可复现；局限是它不一定代表你的业务场景。一个模型在公开 benchmark 上表现好，不代表它在你的内部工具、数据和权限边界里也稳定。

AgentBench、WebArena 和 τ-bench 这类 benchmark 的价值在于让你看到 Agent 评测需要交互环境、长程任务、工具、用户交互、状态变化和失败原因分析。它们不应该被简单理解成“某个分数等于产品可用”。

### Observability

Observability 是可观测性。它关注系统运行时能不能被理解和诊断。

Agent 的 observability 通常包括：输入、模型输出、工具调用参数、工具结果、状态变化、错误、重试、人工确认和最终输出。

### Trace

Trace 是一次任务执行的完整记录。它像一条时间线，记录 Agent 每一步做了什么。

没有 trace，很多失败只能看到“结果错了”，很难知道是检索错、工具参数错、模型理解错，还是权限设计错。

工程实践里，trace 往往还会记录延迟、token 或成本、版本、metadata、用户反馈和人工标注。LangSmith 和 Phoenix 这类 observability 工具都把 trace/runs/spans、datasets、evaluators、feedback 和 experiments 放在同一条工作流里；这说明 trace 不只是 debug 日志，也是 eval 和回归的输入。

OpenAI Agent evals guide 也把 trace 放在调试 workflow behavior 的起点：一次 trace 应能还原 model calls、tool calls、guardrails 和 handoffs。等你知道什么样的 trace 算“好”，再把样例沉淀成 dataset 和 eval runs，用来比较 prompt、工具、路由或 guardrail 的改动。

### Trajectory

Trajectory 更强调 Agent 从目标到结果的行动轨迹。它不只记录最终答案，还记录推理路径、选择、工具调用和中间状态。

对 Agent 来说，trajectory 往往比最终答案更重要。因为两个结果都正确的任务，可能一个过程安全可控，另一个过程越权、浪费成本或依赖偶然行为。

这不表示每个中间步骤都必须人工逐字评分。更实际的做法是先记录关键过程：用了哪些工具、传了什么参数、是否触发权限检查、是否发生重试、是否请求人工确认、最终有没有产生外部副作用。

### Regression Set

Regression set 是回归测试集。它是一组固定任务，用来检查修改后系统是否退化。

初学者不需要一开始做很大的 eval。先做 10-30 条高质量、常见且容易复现的任务，比追求大而泛的测试集更有价值。

### Offline Eval 与 Online Eval

Offline eval 更适合上线前或改动前后做版本对比。它通常基于固定 dataset，有预期输出或人工标注，适合做 regression testing、benchmarking、unit testing 和 prompt/model/tool schema 对比。

Online eval 更适合上线后监控真实流量。它通常基于 production traces、runs 或 conversation threads，不一定有标准答案，适合发现异常、质量退化、安全问题和用户反馈中的失败模式。

两者应该配合使用：online eval 发现的问题，可以整理成新的 offline regression case；offline eval 验证修复后，再继续用 online eval 观察真实环境是否改善。

## 通俗例子

假设你做了一个“帮我查订单并生成退款建议”的客服 Agent。

只看最终答案，可能看到它写了一段很像样的回复。

但 eval 和 observability 还要问这些问题：

- 它查的是不是正确订单？
- 工具参数有没有用错用户 ID？
- 它是否在没有授权时查看了敏感字段？
- 它是否把政策文档里的恶意指令当成系统指令？
- 它是否在工具失败后编造了查询结果？
- 它是否把需要人工确认的退款操作直接执行了？

这些问题只看最终文本很难发现，必须看 trace 和 trajectory。

## 工作原理

一个实用的 Agent eval 通常分成五层。

### 任务是否完成

最基础的问题是：用户目标有没有完成。

这可以用人工打分、规则判断、单元测试、对比标准答案或业务系统状态检查完成。不同任务适合不同方法。

### 中间步骤是否合理

Agent 可能最终答对，但过程有问题。例如查询了不必要的敏感数据，调用了高成本工具，或者在不该执行写操作时执行了写操作。

所以 Agent eval 应该检查关键步骤，而不只检查最终答案。

初学者可以先把关键步骤做成检查点：是否调用了正确工具、是否访问了允许的数据、是否在写操作前等待确认、是否在工具失败后停止编造。等这些检查点稳定后，再考虑更复杂的 trajectory 自动评分。

本手册的 trace-aware eval 最小实验验证了这个差异：3 条 toy refund runs 的最终答案关键词评分全部通过，但 trace-aware scoring 只通过 1 条。它额外发现了无审批执行 `issue_refund` 和工具错误未恢复。这个实验不证明自动评分器可靠，但说明只看最终文本会漏掉关键过程风险。

### 工具调用是否正确

工具型 Agent 的常见错误包括：工具选错、参数错、漏掉必填字段、重复调用、忽略工具错误、把工具返回误读为最终事实。

工具调用 eval 应该记录参数、返回值、错误码和重试策略。

Browser Agent 还要记录网页动作和页面状态。比如打开了哪个 URL、点击了哪个元素、输入了哪些字段、是否上传文件、是否提交表单、提交后 DOM 或业务状态是否正确。Playwright 的 trace viewer 可以按 action 回放浏览器状态、log、source、network 和 DOM snapshot；这说明网页任务的 trace 不应只保存最终回答。

τ-bench 还提醒一个容易忽略的点：客服类工具 Agent 不能只看回答文字，还要看对话结束后的数据库状态是否达到目标，以及同一个任务多次运行是否稳定。它的原始 repo 已提示任务不是最新版，所以正文只采用这个评测思想，不采用旧 leaderboard 数字作为当前能力结论。

### 失败是否可恢复

真实环境里，工具会超时，检索会失败，外部 API 会返回不完整数据。Agent 不应该在失败后直接编造。

好的 eval 会检查系统是否能识别失败、重试、降级、请求用户补充信息，或者把任务转给人工处理。

### 风险是否受控

Agent 评测还要覆盖安全、隐私、权限、成本和延迟。尤其是会执行外部动作的 Agent，评测应该包含越权、误操作和注入类样例。

## 错误分类方法

做 eval 时，最有价值的不是得到一个分数，而是知道错误主要来自哪里。

可以先用下面这组分类：

- 需求理解错误：没有理解用户真正目标或约束。
- 上下文错误：遗漏关键上下文、使用过期信息或被无关信息干扰。
- 检索错误：RAG 没取到正确资料，或取到了但没有正确使用。
- 工具选择错误：选错工具，或没有在需要时调用工具。
- 工具参数错误：字段、格式、ID、时间范围或单位错误。
- 工具结果解释错误：把工具输出误读、过度推断或忽略错误。
- 规划错误：步骤顺序不合理，或没有处理依赖关系。
- 权限错误：执行了不该执行的操作，或访问了不该访问的数据。
- 恢复错误：失败后编造、死循环、重复调用或没有请求帮助。
- 输出错误：结果格式、语气、引用或可执行建议不符合要求。

错误分类能帮助你判断下一步改什么。比如工具参数错误多，应该改 schema、参数校验和示例；检索错误多，应该改 chunk、索引和 reranking；权限错误多，应该改系统边界，而不是继续调 prompt。

## 工程实践

### 从业务任务开始

不要先问“用哪个 benchmark”。先列出用户真实会做的 10 个任务，再写清楚每个任务的成功标准。

公开 benchmark 可以帮助学习评测思想，但不能替代业务 eval。

### 保存完整 trace

至少保存这些信息：用户输入、系统配置版本、模型版本、工具 schema 版本、工具调用参数、工具结果、错误、重试、人工确认和最终输出。

如果系统包含 RAG，还应保存检索 query、top-k 片段、来源 metadata、过滤或 rerank 结果。如果系统会调用工具，还应保存工具名称、参数、返回值摘要、错误码、重试次数和是否触发人工确认。如果要做成本和性能分析，还应保存延迟、token usage、费用估算和模型版本。

如果涉及隐私或敏感数据，trace 需要脱敏、访问控制和保留期限。

本手册的 trace schema audit 最小实验比较了 5 种 trace 形态：`minimal_log` 无法支持任何完整用途；`debug_trace` 足够排查工具错误，但不够审计、回归、成本或隐私治理；`audit_ready_trace` 支持审批、副作用和成本分析，但缺 dataset/case/retrieval/citation；`eval_rag_trace` 同时覆盖 debug、audit、regression、cost、RAG 和 privacy；`privacy_leaky_trace` 虽能 debug，但因为写入假 secret 和邮箱而隐私失败。这个实验不定义通用 schema，但说明 trace 字段必须按用途设计。

最小 trace-aware eval 可以先从规则开始：例如检查是否调用了必需工具、是否执行了禁止工具、工具错误后是否 retry / ask_user / handoff_to_human、写操作前是否有 approval。规则评分不等于完整质量评分，但能快速覆盖一批高风险失败模式。

Real Trace-Aware Eval harness 已把这个思路补成一个本地 scorer control：4 条 deterministic trace fixture 中，final-only scorer 因只看最终文本关键词而 4/4 通过；trace-aware scorer 只让过程完整的 1 条通过，并额外识别缺少工具调用、声称工具错误但没有 error trace、写工具缺少审批拒绝记录这 3 类过程错误。这个结果仍不是平台 eval 或真实模型效果，只说明最小规则 scorer 能覆盖这些高风险 trace failure。

### 先做小型回归集

初始阶段可以从 10-30 条任务开始。每条任务都应该可复现、有预期结果、有失败分类。

当你修复一个 bug，就把对应案例加入 regression set。这样系统会逐渐积累真实保护网。

### 评估改动而不是只评估模型

Agent 的表现不只由模型决定，还由 prompt、工具 schema、RAG、权限、状态管理和编排决定。

每次改动都应该记录版本，否则你很难知道性能变化来自哪里。

### 把人工评审用在高价值样例上

人工评审成本高，但对复杂 Agent 很重要。可以把人工评审集中在高风险任务、失败样例和自动评分不可靠的任务上。

LLM-as-judge 可以降低评审成本，但不能直接当真值。OpenAI 的评估指南明确提醒它可能有 position bias 和 verbosity bias。更稳的做法是先用清晰 rubric、pass/fail 或 pairwise comparison 做小规模评分，再和人工标签对齐，确认误判类型后才扩大使用。

OpenAI Graders 文档还提供了更具体的评分器类型：string check、text similarity、score model grader、Python grader 和 multigrader。它也说明工具调用可以用 `sample.output_tools` 检查 tool name 和 arguments。这里要保守一点：multigrader 在当前文档中标注为 currently only used for reinforcement fine-tuning，不能直接当作所有 eval workflow 的默认组合机制。对初学者来说，这些是设计 eval harness 的参考，不是自动正确性的保证。尤其要注意 reward hacking：系统可能学会迎合 grader 拿高分，但在人类专家看来质量更差。

## 常见误区

- 误区一：有 benchmark 分数就等于产品可用。公开 benchmark 不能覆盖你的业务边界。
- 误区二：最终答案正确就代表 Agent 正确。过程可能越权、浪费成本或不可复现。
- 误区三：eval 只需要上线前做一次。Agent 系统会随模型、工具、数据和 prompt 变化而退化。
- 误区四：用另一个模型打分就完全可靠。模型评审也需要校验和抽样人工检查。
- 误区五：trace 只用于调试。trace 也是审计、回归和安全分析的基础。

## 什么时候不该追求复杂 eval 平台

如果你还没有稳定任务、稳定工具和清晰成功标准，先不要急着上复杂平台。

更合适的第一步是：记录任务、保存 trace、人工标注失败原因、建立小型 regression set。

复杂平台适合在任务规模变大、团队协作变多、版本迭代频繁时引入。

即使用了平台，也不能把平台分数当成真值。LLM-as-judge、自动化规则和在线 evaluator 都需要抽样人工复核，特别是涉及安全、权限、事实正确性和用户影响的任务。

## 已验证结论

- AgentBench 的摘要已完成第一轮精读，可支撑“Agent eval 需要交互环境、长期推理、决策和失败原因分析”的保守表述。
- WebArena 的摘要已完成第一轮精读，可支撑“真实 Web Agent 任务需要端到端环境、工具、外部知识和 long-horizon 评测”的保守表述；论文中的旧实验数值不能泛化为当前模型能力。
- Browser Use / Playwright / Anthropic Computer Use 资料已完成第一轮复核，可支撑浏览器 / computer-use Agent 的动作层和 trace 边界：任务可能包含打开页面、点击、输入、填表、上传文件、登录态 profile、screenshot/mouse/keyboard control、custom tools 和 human-in-the-loop；Playwright trace viewer 支持按 action 回放页面状态、log、source、network 和 DOM snapshot；Anthropic computer use docs 补强 VM/container 隔离、domain allowlist、action validation/logging、截图 prompt injection classifier 和 beta limitation 边界。Real Browser Use Package Surface Validation 已完成 `browser-use==0.13.3` package / source surface 检查；Real Browser Playwright Validation 已完成固定本地 demo page workflow 和 deterministic computer-use-style loop，记录 8 条 action record、DOM/screenshot hash、coordinate validation、redacted invoice 文件上传、submit order 审批阻断、destructive action 阻断和 trace.zip metadata。真实 Browser Use agent / Anthropic computer-use agent、模型任务成功率、点击精度、classifier 行为、成本、延迟、CAPTCHA/stealth、合规和生产可靠性仍需实验。
- 本地标准库 browser action trace audit 显示，浏览器 Agent 的最小评测字段应覆盖 action trace、DOM/screenshot state、side-effect approval、profile isolation、file upload control、external content untrusted boundary、trace redaction 和 failure classification。该实验支撑字段设计；Browser Use package harness 支撑本地入口和源码表面观察；真实 Playwright completed run 支撑一个固定浏览器执行层观察和一个 deterministic coordinate-loop 观察；这些结果都不证明 Browser Use、Anthropic computer use 或任何模型的真实网页任务表现。
- τ-bench 的摘要和 README 已完成第一轮复核，可支撑“工具 Agent 评测需要动态用户交互、领域 API tools、policy guidelines、数据库状态评测和多次试验一致性”的保守表述；原始 repo 已提示任务不是最新版，实际试跑应优先看 τ³-bench。
- “公开 benchmark 可以帮助学习评测环境、任务设计、functional correctness、用户交互、状态评测和失败分类，但不能直接代表真实业务 Agent 质量或产品可用性”已升级为可入正文。业务系统仍需要自己的 custom/private eval、trace、权限检查和回归集。
- OpenAI Evals README 已完成第一轮精读，可支撑 custom eval、private eval 和 tool-using agent eval 的工程思路；标准库 trace-aware eval 已覆盖最小评分字段。Real Trace-Aware Eval harness 已完成本地 deterministic scorer control，验证 final-only scoring 会放过缺工具调用、缺 tool error trace 和缺 approval rejection 的过程错误；当前无 API key，真实模型 completed run 仍待做，具体实践仍需结合当前文档、LLM-as-judge 误判和人工复核实验。
- OpenAI Evaluation best practices 和 Agent evals guide 已完成第一轮精读，可支撑 eval-driven development、task-specific eval、trace grading、datasets/eval runs、tool selection、data precision、handoff accuracy、LLM-as-judge caveats 和 Evals platform 退役边界。它们不证明任何 grader、judge model、平台 trace 或指标在真实业务中可靠。
- OpenAI Graders docs 和 deprecations 页面已完成 2026-07-12 复核，可支撑 grader 类型、tool-call grading、Python grader 执行约束、score model grader、multigrader 的 RFT-only 边界、reward hacking 风险，以及 Evals/graders 退役时间线。它不证明 graders / LLM-as-judge 在真实业务中稳定准确，也不能绕过人工校准或旧平台迁移。
- LangSmith 与 Phoenix 文档已完成第一轮精读，可支撑 offline/online eval、datasets、runs/traces/spans、human feedback、LLM-as-judge、code evaluators、experiments 和 sessions 等工程工作流。
- 本地标准库 trace-aware eval 实验显示，final-answer-only scoring 通过 3/3，而 trace-aware scoring 只通过 1/3；过程评分发现了无审批副作用工具和工具错误未恢复。Real Trace-Aware Eval harness 的本地 scorer control 进一步显示，在 4 条 deterministic trace fixture 中 final-only 4/4 通过、trace-aware 1/4 通过，3 个 score delta 分别来自缺工具调用、缺 tool error trace 和缺 approval rejection。它们支撑“Agent eval 不应只看最终答案”的工程建议。真实模型 trace-aware eval completed run 仍未完成，仍需要真实 LLM-as-judge、人工复核和平台对照实验。
- 本地标准库 grader misalignment / reward hacking 实验显示，`string_check` 会漏掉语义等价答案并放过过程错误，关键词式 judge 会被 verbose / reward-hacked 输出骗过，tool-call rule 会放过纯文本错误，majority multigrader 也不能自动消除共享偏差。该实验支撑“自动 grader 需要人工校准、edge cases、误判统计和抽样复核”的流程设计；真实 LLM-as-judge、平台 grader、成本和延迟仍需实验。
- “Agent trace 不能只保存最终输入输出，字段要按 debug、audit、regression、cost/latency、RAG 和 privacy 等用途设计”已升级为可入正文：本地标准库 trace schema audit 显示，debug、audit、regression、cost/latency、RAG 和 privacy 需要不同字段集合；debug 够用不代表 audit/eval/privacy 够用。该实验不证明任何真实平台默认覆盖这些字段，也不能定义所有 Agent 系统的通用 schema。
- “对会调用工具或产生外部副作用的 Agent，只看最终答案不足以验证过程安全；关键 trajectory / trace 应作为 eval、审计和回归输入”已升级为可入正文。trace 字段、grader 类型、reward hacking 风险和 offline/online eval 工作流已有工程资料和标准库实验支撑；真实 LLM-as-judge、平台 grader 和真实平台字段覆盖仍待任务级验证。

## 待验证问题

- 真实 Agent eval 中 trajectory 应该如何自动评分？
- 真实 Agent trace-aware eval 中，规则评分、LLM-as-judge 和人工评审分别会产生哪些误判？标准库 grader misalignment 实验已给出最小误判结构，Real Trace-Aware Eval 已补本地规则 scorer control；真实模型 trace harness 仍未运行 completed case，仍需实际运行和人工复核样例。
- 模型评审与人工评审如何组合，才能减少误判？
- 不同框架的 observability 能力如何比较？
- AgentBench 和 WebArena 的任务设计对现代业务 Agent 有哪些可迁移经验？
- Browser Use browser agent 和真实模型驱动 computer-use-style action loop 在同一个 demo page 上的 action trace、DOM/screenshot state、权限确认、action validation、成本和失败原因有什么差异？Browser Use package surface、固定 Playwright workflow 和 deterministic coordinate-loop 已完成；模型驱动的 browser/computer-use 对照仍待做。

## 本章小结

- Eval 判断系统是否完成任务，observability 帮你理解过程。
- Agent 评测不能只看最终答案，还要看工具调用、状态、权限和失败恢复。
- Trace 和 trajectory 是 Agent 调试、回归和审计的基础。
- 初学者应先建立小型 regression set，再逐步扩展自动化评测。
- Benchmark 是学习参考，不是业务可用性的直接证明。

## References

### Benchmarks

- [AgentBench: Evaluating LLMs as Agents](../sources/source-cards/2023-agentbench-paper.md)
- [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](../sources/source-cards/2024-tau-bench-paper.md)
- [WebArena: A Realistic Web Environment for Building Autonomous Agents](../sources/source-cards/2023-webarena-paper.md)
- [Browser Use and Playwright Browser Automation References](../sources/source-cards/2026-browser-use-playwright.md)
- [Real Browser Use Package Surface Validation](../experiments/real-browser-use-package-validation/README.md)

### Tools and Source Code

- [OpenAI Evals Repository](../sources/source-cards/2026-openai-evals-repo.md)
- [OpenAI Evaluation Guides](../sources/source-cards/2026-openai-evaluation-guides.md)
- [OpenAI Graders Documentation](../sources/source-cards/2026-openai-graders-docs.md)
- [LangSmith Documentation](../sources/source-cards/2026-langsmith-docs.md)
- [Arize Phoenix Documentation](../sources/source-cards/2026-arize-phoenix-docs.md)
- [OpenAI Cookbook](../sources/source-cards/2026-openai-cookbook.md)

### Governance

- [结论证据台账](../evidence/claim-ledger.md)
- [Evidence Note: Agent Eval 与 Trajectory 边界](../evidence/agent-eval-trajectory-boundary.md)
- [Evidence Note: Observability 与 Trace 工程边界](../evidence/observability-trace-boundary.md)
- [Evidence Note: Browser Agent 与网页自动化边界](../evidence/browser-agent-boundary.md)
- [Browser Action Trace Audit](../experiments/browser-action-trace-audit/README.md)
- [Trace-Aware Eval 最小实验结果](../experiments/trace-aware-eval/results-2026-07-11.md)
- [Trace Schema Audit 最小实验结果](../experiments/trace-schema-audit/results-2026-07-11.md)
- [Grader Misalignment / Reward Hacking 最小实验](../experiments/grader-misalignment/README.md)
- [Real Trace-Aware Eval 实验](../experiments/real-trace-aware-eval/README.md)
- [Real Trace-Aware Eval 结果](../experiments/real-trace-aware-eval/results-2026-07-11.md)
- [References 覆盖矩阵](../references/coverage-matrix.md)
