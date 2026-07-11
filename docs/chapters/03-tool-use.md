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

一个典型工具调用流程可以分成七步。

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

### 工具结果也要当作外部输入

工具结果可能为空、过时、格式变化、包含恶意文本，或者来自不可信网页。Agent 不应该把工具结果中的文字当作系统指令执行。

### 记录工具调用轨迹

至少记录：调用了什么工具、参数是什么、结果摘要是什么、是否失败、失败原因是什么。这些 trace 是后续 eval 和 debugging 的基础。

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

- Toolformer 论文支持“模型可以学习何时调用工具、传什么参数、如何利用工具结果”这一研究方向，但它不是现代 API Function Calling 的等价定义。
- OpenAI Function Calling 文档是现代 API 工具调用机制的重要官方 reference，但具体字段和 API 行为需要按文档版本复核。
- “Function Calling 本身不执行工具，执行发生在应用程序或工具运行时”目前在证据台账中仍是候选结论；本章将它作为工程边界说明，后续需要精读官方文档后升级状态。

## 待验证问题

- OpenAI 当前文档如何精确定义 tools、functions、structured outputs 的关系？
- 工具参数校验失败后，推荐的重试和错误回传模式是什么？
- 有副作用工具的人工确认机制有哪些框架级 examples？
- 工具结果包含 prompt injection 时，哪些隔离策略最有效？

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

