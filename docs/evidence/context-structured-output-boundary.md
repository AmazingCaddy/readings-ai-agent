# Evidence Note: 上下文工程与结构化输出边界

## 要验证的结论

LLM 应用不能把模型调用理解成“输入一段 prompt，取回一段文本”这么简单。工程系统需要区分输入来源、指令优先级、输出 item 类型、结构化输出 schema、工具调用结果和上下文窗口限制。结构化输出能提升解析和 schema 校验可靠性，但不能单独保证事实正确；长上下文能容纳更多信息，但不能替代检索、摘要、状态管理、权限隔离和评测。

## 资料来源

- Source 1：[OpenAI Text Generation Documentation](../sources/source-cards/2026-openai-text-generation-docs.md)
- Source 2：[OpenAI Structured Outputs Documentation](../sources/source-cards/2026-openai-structured-outputs-docs.md)
- Source 3：[OpenAI Responses API Reference](../sources/source-cards/2026-openai-responses-api-docs.md)
- Source 4：[OpenAI Function Calling / Tool Calling Documentation](../sources/source-cards/2026-openai-function-calling-docs.md)
- Source 5：[Evidence Note: Tool Use 与 Function Calling 边界](tool-use-function-calling-boundary.md)
- Source 6：[Evidence Note: RAG 与 Memory 边界](rag-memory-boundary.md)
- Source 7：[Evidence Note: Prompt Injection 与权限边界](prompt-injection-permission-boundary.md)
- Source 8：[上下文治理与结构化输出实验结果](../experiments/context-structured-output/results-2026-07-11.md)
- Source 9：[上下文策略对比实验结果](../experiments/context-strategy-comparison/results-2026-07-11.md)

## 交叉验证结果

- 一致点：OpenAI Text Generation 文档说明 Responses 的 `output` array 经常不止一个 item，可能包含 tool calls、reasoning tokens 等，因此不能假设文本总在 `output[0].content[0].text`。
- 一致点：Responses API reference 把 `input` 定义为文本、图像或文件输入，并把 message role、content item、output message、tool call、refusal 等建模为结构化对象；这支持“模型输入输出是应用协议的一部分，而不只是字符串”的正文表述。
- 一致点：Text Generation 文档和 Responses API reference 都说明 `instructions` / `developer` / `system` 层级高于 `user` 输入；这支持第 02 章关于指令层次的基础解释。
- 一致点：Structured Outputs 文档说明 schema 约束可以减少遗漏 required key 或无效 enum，并明确 JSON mode 只保证 valid JSON，不保证 schema adherence。
- 一致点：Function Calling 文档和 Structured Outputs 文档都把工具调用描述为模型与应用系统之间的结构化协作接口；结构化输出也可用于非工具调用场景，例如分类、路由和 UI 数据。
- 一致点：Structured Outputs 文档明确 structured output 仍可能包含 mistakes；这支持“结构化输出提升可解析性，不等于保证事实正确”的边界。
- 一致点：Text Generation 文档说明 context window 是模型一次请求可处理的数据上限；Responses API reference 提供 `context_management` 和 `truncation` 参数。这支持“上下文窗口是限制和治理对象，不是可靠性保证”的表述。
- 关联点：RAG/Memory evidence 说明外部知识检索、状态和长期记忆治理各有边界；Prompt Injection evidence 说明外部内容不能只靠 prompt 处理。这些资料共同支持“长上下文不能替代检索、摘要、状态、权限和评测”。
- 本地实验：标准库输出解析实验中，`free_text` 只有 1/3 语义有效，`json_mode` 有 2/3 schema valid 但只有 1/3 semantic valid，`schema_validated` 全部 schema valid 但仍有 1 个语义错误。这支持“结构化输出提升解析和 schema adherence，不等于业务正确”。
- 本地实验：标准库上下文治理实验中，`naive_long_context` 同时使用旧政策和外部注入，输出自动退款和导出 token；`governed_context` 选择最新可信政策并隔离外部 attachment。这支持“长上下文不能替代来源、时效、信任和权限治理”。
- 本地实验：标准库上下文策略对比实验中，`full_context`、`recency_only`、`lossy_summary` 和 `keyword_rag` 分别暴露旧政策/外部注入、最新但不可信材料、source id 丢失和基础检索召回不可信文档等失败模式；`governed_context` 保留可信 citation、隔离外部 attachment 并维护 human gate。这支持“长上下文、摘要和 RAG 都需要治理”的边界。

## 实验验证

- 是否需要实验：是
- 实验设计：用同一批输入构建三个最小实验：自由文本输出、JSON mode、Structured Outputs；再构建一个包含长历史、冲突资料和外部文档注入的上下文实验。记录解析失败、schema 不匹配、refusal、语义错误、过时信息使用、外部指令误遵循和 token 成本。
- 结果：已完成标准库最小实验。实验覆盖 free text、JSON-mode-like valid JSON、schema validation、schema-valid semantic error、旧资料使用和外部文档注入隔离。尚未覆盖真实 Responses API / Structured Outputs、refusal、token/latency/cost、跨模型差异或真实外部攻击样本。

## 结论状态

- 可入正文：窄结论“LLM 应用的输入输出不只是字符串；Responses 等 API 会把 message roles、content items、tool calls、refusals、structured outputs 和 context management 建模为结构化对象”由 OpenAI Text Generation 文档和 Responses API reference 直接支撑，并被 Tool Calling / Structured Outputs 资料交叉支撑。
- 可入正文：窄结论“Structured Outputs / schema validation 提升可解析性和 schema adherence，但不保证事实正确、权限正确或业务正确”由 OpenAI Structured Outputs 文档直接支撑，并被 Responses API / Function Calling source cards 和标准库 schema-valid semantic error 实验交叉支撑。
- 可入正文：窄结论“长上下文不能替代上下文治理；系统仍需要处理来源、时效、信任级别、引用、状态、权限隔离和评测”已完成第一轮交叉验证。OpenAI 文档支撑 context window、context management 和 truncation 是工程限制，RAG/Memory 与 Prompt Injection evidence 支撑检索、状态和权限隔离的必要性，两组标准库实验复现了旧资料、外部注入、摘要丢失 provenance 和基础 RAG 召回不可信文档的失败模式。
- 部分验证：真实 Responses API / Structured Outputs 的 refusal、retry、跨模型稳定性、真实长上下文成本和真实外部攻击样本仍待验证；其他供应商和框架可能有不同字段名；真实长上下文 / RAG / 摘要策略的质量、成本和延迟对比仍需实验。

## 可进入章节

- 是。可以写成：现代 LLM 应用不是简单的字符串输入输出函数；系统需要按 API 结构处理角色、内容项、工具调用、拒绝、结构化输出和上下文管理。结构化输出让系统更容易解析、校验和执行模型结果，但它不是事实正确性的保证；长上下文能容纳更多信息，但系统仍需要选择、压缩、标注、检索、状态管理、权限隔离和评测。
