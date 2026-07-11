# Evidence Note: Observability 与 Trace 工程边界

## 要验证的结论

Agent observability 不是普通日志的同义词。对会检索、调用工具、跨多步状态行动的 Agent，trace 至少要能还原输入、输出、中间步骤、工具调用、检索、错误、延迟、成本或 token usage、人工反馈和版本信息。Trace 可以支撑调试、审计、回归和在线/离线评测，但 trace 平台或 LLM-as-judge 不能自动保证系统正确。

## 资料来源

- Source 1：[AgentBench: Evaluating LLMs as Agents](../sources/source-cards/2023-agentbench-paper.md)
- Source 2：[WebArena: A Realistic Web Environment for Building Autonomous Agents](../sources/source-cards/2023-webarena-paper.md)
- Source 3：[OpenAI Evals Repository](../sources/source-cards/2026-openai-evals-repo.md)
- Source 4：[LangSmith Documentation](../sources/source-cards/2026-langsmith-docs.md)
- Source 5：[Arize Phoenix Documentation](../sources/source-cards/2026-arize-phoenix-docs.md)
- Source 6：[OpenAI Cookbook](../sources/source-cards/2026-openai-cookbook.md)
- Source 7：[OpenAI Evaluation Guides](../sources/source-cards/2026-openai-evaluation-guides.md)
- Source 8：[OpenAI Graders Documentation](../sources/source-cards/2026-openai-graders-docs.md)
- Source 9：[Evidence Note: Agent Eval 与 Trajectory 边界](agent-eval-trajectory-boundary.md)
- Source 10：[Evidence Note: Browser Agent 与网页自动化边界](browser-agent-boundary.md)
- Source 11：[Trace-Aware Eval 最小实验结果](../experiments/trace-aware-eval/results-2026-07-11.md)
- Source 12：[Trace Schema Audit 最小实验结果](../experiments/trace-schema-audit/results-2026-07-11.md)
- Source 13：[Grader Misalignment / Reward Hacking 最小实验结果](../experiments/grader-misalignment/results-2026-07-11.md)

## 交叉验证结果

- 一致点：AgentBench 和 WebArena 支撑 Agent eval 需要交互环境、长程任务、工具/外部知识和失败原因分析，而不是只看最终文本。
- 一致点：OpenAI Evals repo 支撑 custom/private eval 和 tool-using agents 的回归测试思路，但不直接给出通用 trajectory 自动评分标准。
- 一致点：OpenAI Agent evals guide 将 trace 描述为一次运行中 model calls、tool calls、guardrails 和 handoffs 的端到端记录，并建议在调试 workflow behavior 时先用 trace grading 发现 regressions 和 failure modes。
- 一致点：OpenAI Evaluation best practices 强调 log everything、continuous evaluation 和用 human feedback 校准 automated scoring；这补强 trace 与 dataset / eval run / human review 之间的工作流关系。
- 一致点：OpenAI Graders docs 列出 string check、text similarity、score model grader、Python grader 和 multigrader，并说明 tool-call grading 可以基于 `sample.output_tools` 检查工具名称和参数；2026-07-12 复核还确认 multigrader 当前标注为只用于 reinforcement fine-tuning，不能泛化为所有 eval workflow 的默认组合方式。
- 一致点：OpenAI Graders docs 明确提示 grader hacking / reward hacking：模型可能在 model grader eval 上高分，但在人类专家评估中表现差；这直接支撑“自动评分不能当真值”的边界。
- 一致点：LangSmith Observability 页面将 observability 定位为从 individual traces 到 production-wide performance metrics 的可见性，并覆盖 view traces、monitor performance、automations 和 feedback。
- 一致点：LangSmith Evaluation concepts 明确将 offline evaluation 用于 pre-deployment testing、benchmarking、regression testing、unit testing、backtesting，将 online evaluation 用于 production monitoring、anomaly detection 和 production feedback。
- 一致点：LangSmith 将 offline eval 目标定义为 dataset/examples，将 online eval 目标定义为 production runs/threads；run 包含 inputs、outputs、intermediate steps、metadata、feedback、latency 等信息。
- 一致点：Phoenix overview 将 trace 定义为可捕获 model calls、retrieval、tool use 和 custom logic，用于 debug behavior 和理解 time spent；Phoenix tutorial 进一步列出 inputs、outputs、latency、token usage。
- 一致点：Phoenix evaluation 支持用 LLM-based evaluators、code-based checks 或 human labels 给 traces/spans 打分；LangSmith 也列出 Human、Code、LLM-as-judge、Pairwise 等 evaluator 类型。
- 一致点：OpenAI Cookbook 的 Agents SDK/Langfuse recipe 支撑 trace、online evaluation、offline evaluation、dataset evaluation 的工程示例，但第三方工具细节需单独复核。
- 一致点：Browser Agent evidence 和 Playwright trace viewer docs 说明浏览器任务 trace 应能按 action 回放，并查看页面状态、log、source、network 和 DOM snapshot；这补强了“trace 字段按任务用途设计”的边界，尤其适用于 Web/Browser Agent。
- 边界：LangSmith 和 Phoenix 都是平台/框架文档，支撑工程形态和字段设计，不证明任一平台默认最优。
- 边界：LLM-as-judge 和在线 evaluator 需要抽样人工复核、误判分析、成本控制和隐私边界；不能把模型评审当作可靠真值。
- 边界：OpenAI Evaluation guides 和 Graders docs 支撑 trace grading、grader 类型和 eval workflow 的工程形态，但不证明任何 grader、judge model、平台 trace 或指标在具体业务中准确可靠；OpenAI deprecations 页面显示 Evals platform 2026-10-31 read-only、2026-11-30 shutdown，且 eval workflow 的 graders 属于该过渡，因此正文必须区分 eval 方法和具体平台入口。
- 本地实验：标准库 trace-aware eval 实验显示，如果 trace 记录 tool call、tool result/error、approval 和 final response，就能用简单规则发现 final-only scoring 漏掉的过程错误；这支持正文中把 trace 作为调试、审计和回归输入，而不只是日志。
- 本地实验：Real Trace-Aware Eval scorer control 显示，同一类 toy refund trace 中 final-only scorer 4/4 通过，trace-aware scorer 1/4 通过，并用规则发现缺工具调用、缺 tool error trace 和缺 approval rejection。该结果支持“trace 字段要服务于可执行 scorer / audit checks”的窄边界，但不证明真实模型或平台 eval 效果。
- 本地实验：标准库 trace schema audit 显示，`debug_trace` 能支持 debug 但不能支持 audit、regression、cost、RAG 或 privacy；`audit_ready_trace` 支持审计和成本分析但仍缺 dataset/case/retrieval/citation；`eval_rag_trace` 同时覆盖 debug、audit、regression、cost、RAG 和 privacy；`privacy_leaky_trace` 虽能 debug，但因泄露假 secret 和邮箱而隐私失败。这支持“trace 字段要按用途设计”的工程边界。
- 本地实验：标准库 grader misalignment / reward hacking audit 显示，exact string、关键词式 judge、tool-call rule 和 majority multigrader 都可能与人工标签不一致；其中 keyword judge 会被 verbose / reward-hacked 输出骗过，string check 会漏掉语义等价答案并放过过程错误。这支持“自动评分器需要误判统计、edge cases 和人工校准”的工程表述。

## 实验验证

- 是否需要实验：是
- 实验设计：实现一个 toy RAG + tool-calling Agent。为 10-20 条任务记录 trace：user input、prompt/config version、model version、retrieved chunks、tool name/args/result/error、intermediate steps、latency、token usage、final output、human feedback、failure category。比较 final-answer-only scoring 与 trace-aware scoring 能发现的错误类型。
- 结果：已完成标准库最小 trace-aware eval 实验、Real Trace-Aware Eval deterministic scorer control、trace schema audit 和 grader misalignment / reward hacking audit。trace-aware eval 记录 tool call、tool result/error、approval 和 final response，并比较 final-answer-only scoring 与 trace-aware scoring；Real scorer control 进一步验证规则 scorer 能识别缺工具调用、缺 error trace 和缺 approval rejection；trace schema audit 比较 debug、audit、regression、cost、RAG 和 privacy 用途所需字段；grader audit 比较 exact string、关键词式 judge、tool-call rule 和 majority multigrader 的误报/漏报。尚未覆盖真实 observability 平台映射、真实 LLM-as-judge 或真实人工复核。

## 结论状态

- 可入正文：窄结论“对工具型或有副作用的 Agent，trace 是 eval、审计和回归输入，不只是 debug 日志”已完成第一轮交叉验证。论文/benchmark 支撑过程评测的重要性，OpenAI Evals repo / Evaluation guides / Graders docs 支撑 custom eval、trace grading、tool-call grading、datasets/eval runs、continuous evaluation、人工校准和 reward hacking 风险，LangSmith/Phoenix/Cookbook 支撑 trace、runs、spans、datasets、online/offline evaluation 和反馈工作流；标准库 trace-aware eval 和 Real Trace-Aware Eval scorer control 支撑 trace 能发现 final-only 漏掉的过程错误，grader audit 支撑自动评分器需要 edge cases、误判统计和人工校准。
- 可入正文：窄结论“trace 不能只保存最终输入输出；字段应按用途覆盖关键工具调用、检索、浏览器动作、页面状态、错误、审批/副作用、版本、延迟/token/成本、dataset/case、citation、隐私脱敏、访问范围和保留策略等信息”已完成第一轮验证。trace schema audit 显示 minimal log 无法支撑 debug/audit/regression/cost/RAG/privacy，debug trace 不等于 audit trace，audit trace 不等于 regression trace，字段够多但未脱敏仍可能隐私失败；Playwright trace viewer 补强了浏览器动作回放、DOM snapshot、log/source/network 等 Web Agent trace 维度。
- 部分验证：完整通用 trace schema、平台字段覆盖、真实 Agent / RAG traces、真实 LLM-as-judge 误判分析和人工复核设计仍需真实运行与平台对照；不能写成任何平台默认覆盖这些字段，也不能把这份字段清单写成所有 Agent 系统的唯一标准。OpenAI Evals / graders platform 退役不影响 eval 方法本身，但会影响具体平台教程、工具入口和旧 API 路线。

## 可进入章节

- 是。可以写成：Agent eval 应同时保存任务、关键 trace、工具调用、检索、错误、审批/副作用、成本/延迟、版本和反馈；trace 字段要按 debug、audit、regression、cost、RAG 和 privacy 等用途设计。offline eval 更适合回归和版本对比，online eval 更适合监控生产流量中的异常和质量退化。不能写成“上了 observability 平台就可靠”，也不能把任何 trace 字段清单写成通用标准。
