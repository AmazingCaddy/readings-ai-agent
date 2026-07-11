# 待验证问题清单

这些问题后续需要通过 references 交叉验证或最小实验确认。未完成验证前，不应写成确定性结论。

## 概念边界

- Agent 和 Workflow 的边界如何定义才准确？已完成第一轮 OpenAI Agents SDK、LangGraph、ReAct 交叉验证和标准库 workflow / hybrid / ReAct-like 对比实验；仍需真实模型 / Agent framework / repo issue 实验。
- “自治程度”是否可以作为分类维度？已完成第一轮边界验证：它可以作为控制权和风险面的连续谱维度，但不能写成能力等级；仍需真实模型 / 框架 / 成本 / 权限实验。
- RAG 和 Memory 的边界如何解释给初学者？已完成第一轮验证、标准库 RAG / short-term / long-term memory 对比实验和最小 RAG pipeline / citation 模拟；仍需真实 RAG / memory framework / 多会话质量实验。

## 真实验证执行队列

这些任务优先补“标准库模拟无法证明”的部分。每个任务完成后，应同步更新 source card、claim ledger、coverage matrix 和相关章节的“已验证结论 / 待验证问题”。

| 优先级 | 验证任务 | 主要验证对象 | 最小产出物 | 仍需保守的边界 |
| --- | --- | --- | --- | --- |
| P0 | 真实 tool-calling 参数校验与有限重试 | OpenAI Responses / Function Calling API | 可复现实验脚本、失败样例、trace、成本/延迟记录；harness 已准备，结果待跑 | 只能验证所选模型和 schema，不代表所有模型稳定修正 |
| P0 | 真实 Structured Outputs / JSON mode / refusal 对比 | OpenAI Structured Outputs / Responses API | schema valid、semantic valid、refusal、retry 结果表；harness 已准备，结果待跑 | schema 通过不等于事实正确或业务正确 |
| P0 | 真实 prompt injection + tool permission / HITL | OpenAI Responses API 或一个轻量 tool agent | 攻击样例、阻断/漏报/误报、审批和 trace 脱敏结果；harness 已准备，结果待跑 | 不证明 guardrail 完全安全，只能记录覆盖范围 |
| P1 | 真实 RAG citation correctness | 轻量本地检索 + LLM synthesis；后续扩展到 LlamaIndex / vector store | chunk 配置、top-k、citation correctness、faithfulness、成本/延迟；LLM synthesis harness 已准备，结果待跑 | 不证明某个 chunk/rerank 策略默认最优 |
| P1 | 真实 Agent trace-aware eval | Responses API toy agent trace；后续扩展到 OpenAI Evals / LangSmith / Phoenix | runs/traces、final-only vs trace-aware 对比、人工复核样例；真实模型 trace harness 已准备，结果待跑 | 自动评分不能当真值，需保留人工抽样 |
| P1 | 真实 MCP host/client/server trace | 本地 stdio JSON-RPC harness；后续扩展到 MCP SDK / host | tools/resources/prompts 调用 trace、approval/resource review、token/resource 泄露检查；stdio harness 已完成 | 不同 host 实现差异可能很大 |
| P2 | 真实 memory framework 多会话对比 | LangGraph memory / Letta / Zep 中至少一种 | 写入、查看、编辑、删除、失效历史、污染样例 | 不写成长期记忆一定提升质量 |
| P2 | 同一任务框架横向对比 | OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen/CrewAI、Semantic Kernel | 相同任务实现、LOC、trace、权限、错误恢复、成本/延迟 | 不得推出“某框架默认最好” |
| P2 | Cookbook 初学者项目试跑 | Structured Outputs、File Search/RAG、Eval、Cost/Rate limit recipes | 环境步骤、阻塞点、费用、失败样例、可跟练教程草稿 | Cookbook 是练习入口，不是生产保证 |

统一运行入口：`uv run python docs/experiments/validation-harness-runner/run_validation_harnesses.py`。无 API key 时，API 类 harness 应返回 `skipped`；本地 stdio / 标准库 harness 应返回 `completed`。runner 结果只说明入口可运行，不代表真实验证完成。

## 架构模式

- ReAct 在哪些任务中确实优于单次提示或简单 workflow？已完成论文摘要第一轮验证和标准库 ReAct-like tool loop 对比；仍需真实模型、真实工具和真实任务实验。
- Plan-and-Execute 的收益是否足以抵消额外成本和错误传播？已完成相关架构模式第一轮验证、标准库 planner/executor 对比实验和 reflection retry 对照；仍需真实模型 / Agent framework / repo issue 实验。
- Reflection / Critic 模式在真实任务中是否稳定提升质量？Reflexion 已完成论文摘要第一轮验证，标准库 reflection/retry 实验已验证 verified feedback 可补证据、unverified reflection 会重复错误；仍需结合真实模型、长期 episodic memory、成本和人工评审实验。
- 多 Agent 的收益是否足以抵消通信成本、协调复杂度和调试难度？已完成 AutoGen/CrewAI 第一轮资料验证和标准库单流程 / 无控制多 Agent / Flow 控制多 Agent 对比；仍需真实模型、真实框架、token/latency/cost 和复杂多视角任务实验。

## 工具调用

- Function calling、tool use、structured output 在不同框架中的术语差异是什么？OpenAI API 层和 Structured Outputs 边界已完成第一轮验证，仍需补其他框架术语对照。
- 工具参数校验和重试的最佳实践有哪些官方或工程 references？已完成标准库模拟实验，支持“应用层校验、错误回传、有限重试”的流程；真实 Responses API harness 已准备，仍需配置 API key 后记录真实 API / SDK 行为和框架默认行为对照。
- 工具调用权限应该如何设计确认边界？
- 真实 tool-calling 实验中，参数校验失败后模型能否稳定修正？标准库 fake model 已复现流程，真实 API harness 已准备，但不能证明真实模型稳定性，仍需实际运行结果。

## MCP

- MCP 相比传统 API wrapper 的核心价值是什么？
- MCP tools、resources、prompts 的边界如何准确解释？已完成官方 server concepts 和 2025-11-25 spec 第一轮验证：tools 是 model-controlled，resources 是 application-driven，prompts 是 user-controlled；标准库模拟实验和本地 stdio JSON-RPC harness 已验证最小 trace 字段，仍需真实 host 呈现方式对比。
- MCP 安全模型和权限边界有哪些官方建议？已完成第一轮验证：authorization 是 optional transport-level capability；HTTP transport 支持授权时遵循 OAuth 2.1 相关规范；STDIO transport 应从环境取得凭据；token passthrough 被禁止；roots 不等于 sandbox；elicitation/sampling 需要用户可见和可拒绝的交互边界；标准库模拟实验和本地 stdio JSON-RPC harness 已验证 tool approval 和 resource review trace，仍需真实 SDK / host 实验验证实现差异。
- 如何用真实 MCP SDK / host 复现 host/client/server、`tools/list`、`tools/call`、`resources/list`、`resources/read` 和 trace？本地 stdio JSON-RPC harness 已覆盖进程边界和最小消息流，仍需官方 SDK / host 对照。
- 如何把标准库模拟中的最小恶意 resource/prompt 与模拟写工具迁移到真实 host，验证 host 是否展示 tool inputs、允许用户拒绝、记录审计、避免敏感 token/resource 泄露？

## RAG 与 Memory

- 长期记忆是否一定提升 Agent 表现？已完成第一轮验证和标准库写入守门模拟：不能写成“一定提升”；仍需真实多会话 Agent / memory framework 实验验证哪些任务有收益、哪些任务会被污染。
- Chunk size、embedding model、reranking 对结果的影响如何验证？LlamaIndex 已完成第一轮工程流程验证，标准库最小 pipeline 已验证 trace/citation 字段；真实 LLM citation synthesis harness 已准备但仍使用本地关键词检索，仍需真实 embedding / vector store / rerank 对比实验。
- RAG 答案如何稳定带 source citation / source nodes？标准库模拟实验已验证 chunk-level citation 字段设计；真实 LLM citation synthesis harness 已准备；仍需实际运行验证 citation correctness / faithfulness，并扩展到真实 RAG stack。
- Memory 写入守门有哪些可复用设计？Letta/Zep 已提供第一轮工程模式参考，标准库模拟已验证显式写入、敏感信息拒绝、低置信推断拒绝、用户纠正和失效历史的最小流程；仍需真实 framework 的查看、编辑、删除、权限和隐私边界实验。
- RAG paper 中的 non-parametric memory 与 Agent long-term memory 如何避免术语混淆？已完成第一轮边界解释和标准库 RAG / Memory 分流实验；后续仍需真实教程示例避免术语误用。

## Eval 与生产化

- 上下文工程中的输出解析、Structured Outputs、JSON mode 和长上下文失败模式如何设计最小实验？已完成 OpenAI 官方文档第一轮验证、标准库输出解析 / 上下文治理模拟实验和上下文策略对比实验；真实 Structured Outputs / JSON mode harness 已准备；仍需实际运行验证 refusal、semantic validator、retry loop、真实长上下文 / RAG / 摘要 token/latency/cost 和跨模型稳定性。
- Agent eval 应该优先评估最终结果还是完整 trajectory？已确认 AgentBench/WebArena/OpenAI Evals/LangSmith/Phoenix 支撑过程与交互评测的重要性，标准库 trace-aware eval 已验证 final-only 会漏掉无审批副作用工具和工具错误未恢复；真实模型 trace-aware eval harness 已准备，仍需实际运行和平台对照实验。
- 通用 benchmark 对真实业务 agent 的代表性有多强？已确认公开 benchmark 可学习评测思想，但业务系统仍需 custom/private eval。
- Trace 字段如何设计，才能同时支持调试、审计、回归和隐私控制？已完成 LangSmith/Phoenix/Cookbook 第一轮验证，标准库 trace-aware eval 已覆盖 tool call/result/error/approval/final response；真实模型 trace-aware eval harness 已准备；候选字段仍包括输入、输出、中间步骤、工具调用、检索、错误、延迟、token/cost、反馈、版本、metadata；仍需实际运行真实 RAG/tool traces 和隐私脱敏策略。
- LLM-as-judge、online evaluator 和自动化规则的误判率、成本与抽样人工复核比例如何设计？
- Prompt injection 防护有哪些已验证的工程方法？已确认 OWASP/NIST 支撑风险边界，OpenAI Agents SDK/Semantic Kernel/Responses API 支撑 guardrails、approval、require_approval、sensitive trace 控制等工程边界；标准库最小攻击实验已验证 prompt-only 风险和 policy-enforced 写工具阻断/trace 脱敏流程；安全 regression set 已扩展到授权、金额阈值、敏感信息、破坏性工具、幂等性和 benign case；真实 prompt injection / permission harness 已准备；仍需实际运行验证真实模型 / 框架 guardrail 误报漏报。
- 安全 regression set 应该如何覆盖外部文档注入、工具参数越权、敏感信息泄露和 excessive agency？标准库实验已覆盖外部文档注入、写工具越权、跨用户读取、高金额审批、trace 假 secret 泄露、破坏性工具、重复提交和 benign case；仍需迁移到真实工具、真实模型和框架 guardrail。
- Guardrails、HITL approval、tool approval 和 sensitive trace 配置在不同框架中的覆盖范围有什么差异？OpenAI Agents SDK 已确认 tool guardrails 不覆盖所有工具类型，仍需横向比较。

## 实践路线

- 哪些 OpenAI Cookbook 示例最适合初学者作为项目模板？已完成第一轮验证：Structured Outputs、File Search RAG、OpenAI Evals、Agents SDK trace/eval、Usage/Cost、Rate limits 适合作为候选；标准库 smoke harness 已验证无模型验收结构；仍需真实 Cookbook / API 本地试跑确认依赖、成本和阻塞点。
- 每个项目应使用哪个最小技术栈，才能降低环境成本？标准库 smoke harness 可作为无模型入门层；真实技术栈仍需基于本地试跑和 GitHub Pages 教程形态决定。
- 如何为项目 7 设计可自动运行的 eval harness？标准库 smoke harness 已给出最小 eval cases / pass-fail 结构；仍需扩展到真实 OpenAI Evals 或轻量自定义 harness。
- 如何把 Cookbook recipe 改写成初学者可跟练教程，同时保留 references、trace、失败样例和成本记录？

## 框架生态

- 同一任务在 OpenAI Agents SDK、LangGraph、LlamaIndex、AutoGen/CrewAI、Semantic Kernel 下的实现成本、trace、权限和错误处理如何比较？框架定位已完成第一轮验证，标准库 rubric smoke test 已验证任务画像和比较维度；仍需真实框架横向实验。
- Semantic Kernel Process Framework 当前标注 experimental；后续复核时需要确认其稳定性和 API 变化。
