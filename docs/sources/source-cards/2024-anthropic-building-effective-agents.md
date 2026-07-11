# Building effective agents

- 来源链接：https://www.anthropic.com/engineering/building-effective-agents
- 作者 / 机构：Erik S. and Barry Zhang / Anthropic
- 发布时间：2024-12-19
- 最后复核日期：2026-07-12
- 类型：Engineering Guide / Official Blog
- 主题：Agentic Systems / Workflows / Agent Patterns / Framework Boundaries
- 适合阶段：入门 / 架构模式 / 框架选型
- 可信度等级：A
- 是否已验证：页面 HTTP 200、HTML metadata、发布日期、摘要和关键正文段落已于 2026-07-12 复核；支撑 workflow / agent 区分、简单优先、常见 agentic workflow patterns、framework abstraction caveat、agent loop / tool feedback / human checkpoint / stop condition 边界；不能验证任意模型、框架或生产系统的真实效果、成本、延迟或可靠性

## 一句话总结

Anthropic 这篇工程文章把 agentic systems 分成 workflows 和 agents：workflows 由预定义代码路径编排 LLM 和工具，agents 则让 LLM 动态决定流程和工具使用；文章反复强调先用简单、可组合模式，只有在需要灵活决策时再提高自治程度。

## 核心结论

- Anthropic 把 workflows 和 agents 都归入 agentic systems，但明确区分二者：workflow 是 predefined code paths，agent 是 LLM dynamically direct its own process and tool usage。
- 构建 LLM 应用时应先找最简单可行方案，必要时再增加复杂度；很多应用只优化单次 LLM call、retrieval 和 in-context examples 就足够。
- Agentic systems 通常用 latency 和 cost 换取更好的任务表现；是否值得必须按任务判断，不能把“更像 Agent”当作默认升级。
- 框架能简化调用模型、定义/解析工具和串联调用，但也可能遮蔽底层 prompts / responses，增加调试难度，并诱导不必要复杂度。
- 常见构件从 augmented LLM 开始，再到 prompt chaining、routing、parallelization、orchestrator-workers、evaluator-optimizer，最后才是更开放的 agent loop。
- Agents 适合难以预先写死步骤数、需要灵活决策和多轮工具反馈的开放任务；执行中需要从环境取得 ground truth，必要时在 checkpoint 或 blocker 处暂停给人类反馈。
- Agents 的自治会带来更高成本和 compounding errors；文章建议 extensive testing in sandboxed environments 和 appropriate guardrails，并设置 stopping conditions。

## 支撑证据

- 2026-07-12 复核 `https://www.anthropic.com/engineering/building-effective-agents` HEAD 返回 HTTP 200，`content-type: text/html; charset=utf-8`。
- HTML metadata 包含标题 `Building Effective AI Agents \ Anthropic`，canonical URL 为 `https://www.anthropic.com/engineering/building-effective-agents`。
- 页面 hero 显示 `Published Dec 19, 2024`，摘要写明 Anthropic 与多个行业团队合作构建 LLM agents，成功实现通常使用 simple, composable patterns rather than complex frameworks。
- 关键正文 `What are agents?` 段落明确说明 agent 可以有多种定义；Anthropic 将这些变体称为 agentic systems，但区分 workflows 和 agents。
- 正文定义 workflows 为 `systems where LLMs and tools are orchestrated through predefined code paths`，agents 为 `systems where LLMs dynamically direct their own processes and tool usage`。
- `When (and when not) to use agents` 段落明确建议先找 simplest solution possible，并且 only increasing complexity when needed；还说明 agentic systems often trade latency and cost for better task performance。
- 同段说明 workflows 对 well-defined tasks 更 predictable / consistent，agents 更适合 flexibility 和 model-driven decision-making needed at scale；很多应用优化 single LLM calls with retrieval and in-context examples 就足够。
- `When and how to use frameworks` 段落说明框架简化低层任务，但可能创建 extra layers of abstraction，遮蔽 underlying prompts and responses，增加调试难度，并诱导增加复杂度。
- `Building blocks, workflows, and agents` 段落列出 augmented LLM 作为基础构件，并逐步增加复杂度。
- 抽样复核的 workflow sections 覆盖 prompt chaining、routing、parallelization、orchestrator-workers 和 evaluator-optimizer，并给出各自适用条件。
- `Agents` 段落说明成熟 agent 会理解复杂输入、reasoning/planning、可靠使用工具和从错误恢复；执行时应从 tool call results 或 code execution 获取 ground truth，并可在 checkpoint / blocker 暂停给人类反馈。
- `When to use agents` 段落说明 agents 适合难以预测步骤数、无法 hardcode fixed path、需要多轮运行且能信任模型决策的开放问题；同时提醒 autonomy 带来 higher costs 和 compounding errors，需要 sandbox testing 和 guardrails。

## 可能的问题

- 这是一篇 Anthropic 工程博客，不是 peer-reviewed paper，也不是标准规范；它能支撑工程经验和架构边界，不能支撑严谨的性能或可靠性结论。
- 文章提到与客户和 Anthropic 自身实现的经验，但没有提供可复现实验数据、benchmark、样本分布或成本/延迟表；不能写成“简单模式一定优于复杂框架”。
- 文章列出的框架和模型名称会随时间变化；本 source card 只引用 workflow/agent 区分、复杂度递进和框架抽象风险这些相对稳定的工程边界。
- 它不验证 Claude、Claude Agent SDK、任意第三方框架、coding agents 或 customer support agents 的真实表现。

## 初学者阅读建议

- 先看 `What are agents?`：把 workflow 和 agent 的控制权差异弄清楚。
- 再看 `When (and when not) to use agents`：记住“简单优先”，不要把所有 LLM 应用都做成 agent。
- 最后按顺序读五个 workflow pattern：prompt chaining、routing、parallelization、orchestrator-workers、evaluator-optimizer。理解这些以后，再读真正的 agents 段落会更容易。

## 可复现实验

- 用同一个小任务实现 single-call、prompt chaining、routing、orchestrator-workers 和 agent loop 五个版本，记录成功率、错误类型、工具调用数、token、延迟、成本和 trace 可读性。
- 在现有 Workflow / Hybrid / ReAct-like 对比实验中加入 Anthropic pattern labels，把每个实现标成 predefined code path、dynamic orchestration 或 LLM-controlled loop。

## 是否进入正文

- 结论：进入正文；架构和学习路线边界可入正文
- 原因：它与 OpenAI Practical Guide to Building Agents、LangGraph docs、ReAct/Reflection/ToT 论文和本地 workflow-agent 对比实验共同支撑“Agent/Workflow 是控制权和编排方式的连续谱，复杂度应按任务需要逐步增加，框架抽象需要能被调试和理解”的窄结论。它不能支撑真实模型、真实框架、真实 customer support / coding agent 的性能、成本、延迟、安全或生产可靠性。
