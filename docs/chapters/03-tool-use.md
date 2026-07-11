# Tool Use、Function Calling 与 Structured Output

## 本章适合谁

如果你已经理解模型输入输出和上下文工程，但还不清楚模型如何“调用工具”、Function Calling 到底执行了什么、Structured Output 和 Tool Use 有什么关系，这一章适合阅读。

本章重点是工程边界：模型生成工具调用请求，应用程序负责校验、授权、执行和回传结果。

## 你会学到什么

- Tool Use、Function Calling、Structured Output 的区别。
- 工具调用在 Agent 系统中的基本流程。
- 为什么 schema、参数校验和权限边界很重要。
- 工具调用常见失败模式。
- 什么时候不该让模型直接调用工具。

## 先用一句话理解

Tool Use 是让模型使用外部能力；Function Calling 是常见 API 机制；Structured Output 是让模型输出可被程序解析和校验的结构。

## 基础概念

### Tool Use

Tool Use 指模型基于上下文选择工具、生成参数、接收工具结果，并把结果纳入后续推理或回答的机制。工具可以是搜索、计算器、数据库查询、文件读取、代码执行、邮件发送、日历操作或业务 API。

Tool Use 的核心不是“模型会执行代码”，而是模型能提出一个工具调用意图。

### Function Calling

Function Calling 通常指开发者向模型提供函数或工具 schema，模型根据 schema 生成调用请求。应用程序拿到请求后，决定是否执行工具，并把执行结果返回给模型。

因此，Function Calling 本身不应该被理解为“模型执行函数”。更准确地说，它是模型和应用程序之间的结构化协作接口。

### Structured Output

Structured Output 是更广的概念。它指模型输出符合某种结构，例如 JSON、枚举、字段对象或工具参数。

Function Calling 通常依赖结构化输出，但结构化输出不一定是工具调用。比如让模型输出：

```json
{
  "priority": "high",
  "category": "security",
  "needs_human_review": true
}
```

这只是分类和路由，不一定触发工具。

## Tool Use 的基本流程

OpenAI Function Calling 文档把工具调用描述为一个多步流程：应用程序把工具提供给模型，模型返回工具调用，应用程序执行代码，再把工具输出交回模型，模型继续生成最终响应或更多工具调用。

为了便于工程实现，本章把这个流程展开成七步。

1. 开发者定义工具：名称、用途、参数 schema、权限和失败处理。
2. 应用程序把工具说明放进模型上下文。
3. 模型根据任务决定是否需要工具。
4. 模型生成工具调用请求和参数。
5. 应用程序校验参数和权限。
6. 应用程序执行工具，并把结果返回给模型。
7. 模型基于工具结果继续推理、调用下一个工具或生成最终回答。

关键点在第 5 步。真正可靠的系统不会因为模型生成了调用请求就直接执行。它需要检查参数是否完整、类型是否正确、权限是否允许、是否需要用户确认，以及工具结果是否可信。

## 通俗例子

假设用户说：“帮我看看这个 repo 最新 release 有没有 breaking changes。”

模型可能生成工具调用：

```json
{
  "tool": "get_latest_release",
  "arguments": {
    "repository": "owner/project"
  }
}
```

应用程序检查：

- `repository` 是否存在。
- 这个工具是否只读。
- 是否需要联网权限。
- 返回结果是否为空。

如果工具返回 release notes，模型再总结 breaking changes。如果工具失败，系统可能重试、换工具、请求用户提供 repo 名称，或直接说明无法确认。

这个过程里，模型负责选择和组织调用意图，应用程序负责执行和安全边界。

## 工作原理

工具调用之所以比自然语言指令更适合工程系统，是因为它把“想做什么”转换成了可检查的数据结构。

一个工具 schema 通常需要说明：

- 工具名称。
- 工具用途。
- 参数字段。
- 参数类型。
- 必填字段。
- 枚举值或范围限制。
- 工具是否有副作用。
- 权限和确认要求。

schema 写得越清楚，应用程序越容易判断模型输出是否可执行。schema 写得模糊，模型更容易生成看似合理但无法执行的参数。

## 工程实践

### 把工具分成只读和有副作用

只读工具如搜索、读取文件、查询数据库。有副作用工具如发送邮件、写数据库、删除文件、创建订单、部署服务。

有副作用工具应该默认需要更严格的权限控制、确认机制和审计日志。

### 参数必须校验

不要相信模型生成的参数天然正确。应用程序应该做类型校验、必填校验、范围校验和业务规则校验。

如果校验失败，可以把错误返回给模型，让它修正参数；但重试次数应有限制。

本手册的最小 tool-calling 模拟实验验证了这个控制循环：fake model 第一轮生成 `unit=kelvin`，应用层拒绝执行并返回 `unit must be one of: celsius, fahrenheit`，第二轮 fake model 改成 `unit=celsius` 后应用层才执行工具。这个实验只能支撑流程设计，不证明真实模型总能稳定修正参数；真实 Responses API harness 已准备，后续需要配置 API key 后记录实际模型行为。

结构化输出模拟实验也支持同一个边界：即使输出完全符合 schema，仍可能在 `requires_human`、citation 或权限判断上出错。因此 schema validation 适合做第一层格式和枚举检查，不能替代业务校验、权限控制和人工确认。

### 工具结果也要当作外部输入

工具结果可能为空、过时、格式变化、包含恶意文本，或者来自不可信网页。Agent 不应该把工具结果中的文字当作系统指令执行。

### 记录工具调用轨迹

至少记录：调用了什么工具、参数是什么、结果摘要是什么、是否失败、失败原因是什么。这些 trace 是后续 eval 和 debugging 的基础。

对参数校验和重试来说，trace 至少应记录：模型请求的 tool call、应用层校验失败、错误回传、第二次 tool call、工具执行结果和最终响应。没有这些事件，很难判断失败来自模型参数、schema 设计、业务规则还是工具本身。

### 限制工具数量

不要一开始给模型几十个工具。工具越多，选择错误和上下文混乱的概率越高。初学者项目可以先从 1-3 个工具开始。

## 常见误区

- 误区一：Function Calling 会自动执行函数。实际执行发生在应用程序或工具运行时。
- 误区二：有 schema 就安全。schema 只能约束格式，不能替代权限和业务校验。
- 误区三：工具越多 Agent 越强。工具越多，路由、权限和错误处理越复杂。
- 误区四：工具结果一定可信。工具结果是外部输入，仍可能错误、过时或恶意。
- 误区五：只要模型会调用工具，就已经是完整 Agent。工具调用只是 Agent 的一个组件。

## 什么时候不该用工具调用

以下场景不适合直接引入工具调用：

- 任务只需要固定文本生成或简单分类。
- 工具副作用很高，但还没有权限和确认机制。
- 工具 API 不稳定，错误处理尚未设计。
- 团队无法记录和审计工具调用。
- 用户输入中可能包含高风险外部指令，但系统还没有隔离策略。

可以先用手动确认、只读工具、固定 workflow 或离线处理替代。

## 已验证结论

- Toolformer 论文摘要支持“模型可以学习何时调用工具、传什么参数、如何利用工具结果”这一研究方向，但它不是现代 API Function Calling 的等价定义。
- OpenAI Function Calling 文档明确 function calling 也称 tool calling，并把工具调用描述为模型与应用程序之间的多步交互。
- OpenAI Function Calling 文档明确流程中包含“应用侧执行代码”和“带工具输出再次请求模型”，因此“Function Calling 本身不执行工具”是本章可入正文的确定性工程边界。
- OpenAI Responses API reference 进一步说明 function tool 包含 `name`、`type`、`parameters`、`strict` 等字段，并支持多种工具类型；具体字段和能力仍需按文档版本复核。
- 本地标准库模拟实验复现了参数校验失败、工具错误回传、第二次工具调用、工具执行和最终响应；它支撑“参数校验和有限重试是应用层控制循环”的工程建议。真实 Responses API tool-calling harness 已准备，但结果待跑，仍不能证明真实模型稳定修正参数。

## 待验证问题

- 其他框架如何定义 tools、functions、structured outputs，它们和 OpenAI API 术语有何差异？
- 真实模型和真实 Function Calling API 中，工具参数校验失败后能否稳定根据错误修正参数？harness 已准备，仍需实际运行并记录模型、schema、错误格式、成本和延迟。
- 有副作用工具的人工确认机制有哪些框架级 examples？
- 工具结果包含 prompt injection 时，哪些隔离策略最有效？
- 不同框架对 tool execution errors、protocol errors 和 retry policy 的默认处理有什么差异？

## 本章小结

- Tool Use 是让模型使用外部能力。
- Function Calling 是常见 API 机制，不等于模型自己执行函数。
- Structured Output 是更广的结构化结果机制，可以用于工具调用，也可以用于分类、路由和状态更新。
- 工具调用可靠性取决于 schema、参数校验、权限控制、错误处理和 trace。
- 初学者应先从少量只读工具开始，再逐步增加复杂度。

## References

### Official Docs

- [OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- [OpenAI Responses API Reference](../sources/source-cards/2026-openai-responses-api-docs.md)
- [OpenAI Agents SDK Documentation](../sources/source-cards/2026-openai-agents-sdk-docs.md)

### Papers

- [Toolformer: Language Models Can Teach Themselves to Use Tools](../sources/source-cards/2023-toolformer-paper.md)
- [ReAct: Synergizing Reasoning and Acting in Language Models](../sources/source-cards/2022-react-paper.md)

### Governance

- [术语边界表](../glossary.md)
- [结论证据台账](../evidence/claim-ledger.md)
- [Evidence Note: Tool Use 与 Function Calling 边界](../evidence/tool-use-function-calling-boundary.md)
- [Tool Calling 参数校验与重试实验结果](../experiments/tool-calling-validation/results-2026-07-11.md)
- [Real Tool Calling 参数校验与重试实验](../experiments/real-tool-calling-validation/README.md)
- [上下文治理与结构化输出实验结果](../experiments/context-structured-output/results-2026-07-11.md)
