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
- Source 7：[Evidence Note: Agent Eval 与 Trajectory 边界](agent-eval-trajectory-boundary.md)
- Source 8：[Trace-Aware Eval 最小实验结果](../experiments/trace-aware-eval/results-2026-07-11.md)
- Source 9：[Trace Schema Audit 最小实验结果](../experiments/trace-schema-audit/results-2026-07-11.md)

## 交叉验证结果

- 一致点：AgentBench 和 WebArena 支撑 Agent eval 需要交互环境、长程任务、工具/外部知识和失败原因分析，而不是只看最终文本。
- 一致点：OpenAI Evals repo 支撑 custom/private eval 和 tool-using agents 的回归测试思路，但不直接给出通用 trajectory 自动评分标准。
- 一致点：LangSmith Observability 页面将 observability 定位为从 individual traces 到 production-wide performance metrics 的可见性，并覆盖 view traces、monitor performance、automations 和 feedback。
- 一致点：LangSmith Evaluation concepts 明确将 offline evaluation 用于 pre-deployment testing、benchmarking、regression testing、unit testing、backtesting，将 online evaluation 用于 production monitoring、anomaly detection 和 production feedback。
- 一致点：LangSmith 将 offline eval 目标定义为 dataset/examples，将 online eval 目标定义为 production runs/threads；run 包含 inputs、outputs、intermediate steps、metadata、feedback、latency 等信息。
- 一致点：Phoenix overview 将 trace 定义为可捕获 model calls、retrieval、tool use 和 custom logic，用于 debug behavior 和理解 time spent；Phoenix tutorial 进一步列出 inputs、outputs、latency、token usage。
- 一致点：Phoenix evaluation 支持用 LLM-based evaluators、code-based checks 或 human labels 给 traces/spans 打分；LangSmith 也列出 Human、Code、LLM-as-judge、Pairwise 等 evaluator 类型。
- 一致点：OpenAI Cookbook 的 Agents SDK/Langfuse recipe 支撑 trace、online evaluation、offline evaluation、dataset evaluation 的工程示例，但第三方工具细节需单独复核。
- 边界：LangSmith 和 Phoenix 都是平台/框架文档，支撑工程形态和字段设计，不证明任一平台默认最优。
- 边界：LLM-as-judge 和在线 evaluator 需要抽样人工复核、误判分析、成本控制和隐私边界；不能把模型评审当作可靠真值。
- 本地实验：标准库 trace-aware eval 实验显示，如果 trace 记录 tool call、tool result/error、approval 和 final response，就能用简单规则发现 final-only scoring 漏掉的过程错误；这支持正文中把 trace 作为调试、审计和回归输入，而不只是日志。
- 本地实验：标准库 trace schema audit 显示，`debug_trace` 能支持 debug 但不能支持 audit、regression、cost、RAG 或 privacy；`audit_ready_trace` 支持审计和成本分析但仍缺 dataset/case/retrieval/citation；`eval_rag_trace` 同时覆盖 debug、audit、regression、cost、RAG 和 privacy；`privacy_leaky_trace` 虽能 debug，但因泄露假 secret 和邮箱而隐私失败。这支持“trace 字段要按用途设计”的工程边界。

## 实验验证

- 是否需要实验：是
- 实验设计：实现一个 toy RAG + tool-calling Agent。为 10-20 条任务记录 trace：user input、prompt/config version、model version、retrieved chunks、tool name/args/result/error、intermediate steps、latency、token usage、final output、human feedback、failure category。比较 final-answer-only scoring 与 trace-aware scoring 能发现的错误类型。
- 结果：已完成标准库最小 trace-aware eval 实验和 trace schema audit。前者记录 tool call、tool result/error、approval 和 final response，并比较 final-answer-only scoring 与 trace-aware scoring；后者比较 debug、audit、regression、cost、RAG 和 privacy 用途所需字段。尚未覆盖真实 observability 平台映射、真实 LLM-as-judge 或人工复核。

## 结论状态

- 可入正文：窄结论“对工具型或有副作用的 Agent，trace 是 eval、审计和回归输入，不只是 debug 日志”已完成第一轮交叉验证。论文/benchmark 支撑过程评测的重要性，OpenAI Evals 支撑 custom eval，LangSmith/Phoenix/Cookbook 支撑 trace、runs、spans、datasets、online/offline evaluation 和反馈工作流；标准库 trace-aware eval 支撑 trace 能发现 final-only 漏掉的过程错误。
- 部分验证：完整 trace 字段集合、平台字段覆盖、真实 Agent / RAG traces、自动评分误判分析和人工复核设计仍需真实运行与平台对照。trace schema audit 只能支持“字段要按用途设计”的工程边界，不能定义通用 schema。

## 可进入章节

- 是。可以写成：Agent eval 应同时保存任务、关键 trace、工具调用、检索、错误、成本/延迟和反馈；offline eval 更适合回归和版本对比，online eval 更适合监控生产流量中的异常和质量退化。不能写成“上了 observability 平台就可靠”，也不能把任何 trace 字段清单写成通用标准。
