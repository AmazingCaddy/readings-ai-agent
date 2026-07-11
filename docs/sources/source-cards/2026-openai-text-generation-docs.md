# OpenAI Text Generation Documentation

- 来源链接：https://developers.openai.com/api/docs/guides/text
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；Markdown 页面 last-modified 复核为 2026-07-11 07:34:29 GMT
- 最后复核日期：2026-07-12
- 类型：官方文档
- 主题：Text Generation / Prompt Engineering / Message Roles / Prompt Versioning
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：text generation HTML 与 Markdown 页面均于 2026-07-12 返回 HTTP 200；关键段落已复核；输入输出不是简单字符串、长上下文不能替代治理的窄边界可入正文；上下文治理与结构化输出标准库实验、上下文策略对比实验已完成；真实运行行为仍部分验证

## 一句话总结

OpenAI Text Generation 文档适合解释模型输入、输出数组、message roles、instructions 参数、Responses API 选择和 prompt 版本管理的基础工程边界。

## 核心结论

- 文档说明 Responses API 返回的 `output` array 经常不止一个 item，可能包含 tool calls、reasoning tokens 等，不应假设文本一定在 `output[0].content[0].text`。
- 文档说明官方 SDK 可能提供 `output_text` convenience property，把 text outputs 聚合成单个字符串；这只是读取文本的快捷入口，不改变 `output` array 仍可能包含多类 item 的事实。
- 文档说明模型也可以返回 structured JSON data，并链接到 Structured Outputs。
- 文档把 prompt engineering 描述为编写有效指令以让模型更稳定满足需求，并建议复杂应用 pin model snapshots、建立 tests 和 evaluation suites。
- 文档建议新的 text generation 应用使用 Responses API；reasoning models 尤其适合迁移到 Responses。正文仍不应把某个模型名或示例 snapshot 写成长期学习结论。
- 文档说明 `instructions` 参数会优先于 `input` 中的 prompt；`developer` messages 优先于 `user` messages。
- 文档提醒 `instructions` 只适用于当前 response generation request；使用 `previous_response_id` 管理会话状态时，上一轮的 instructions 不会自动出现在上下文中。
- 文档建议把 production prompts 放在应用代码中，通过 typed inputs、code review、tests 和部署流程管理 prompt 变化；reusable prompt objects 正在退役，`v1/prompts` 计划于 2026-11-30 shutdown。

## 支撑证据

- `https://developers.openai.com/api/docs/guides/text` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 06:08:20 GMT`；`content-type: text/html; charset=utf-8`。
- `https://developers.openai.com/api/docs/guides/text.md` 返回 HTTP 200；`last-modified: Sat, 11 Jul 2026 07:34:29 GMT`；`content-type: text/markdown; charset=utf-8`。
- 2026-07-12 抓取 `https://developers.openai.com/api/docs/guides/text.md` 成功；页面包含 output array、SDK `output_text` convenience property、Structured Outputs、Responses API recommendation、message roles、instructions、developer/user priority、tests/evals、prompt-in-code guidance 和 reusable prompt objects deprecation 等关键段落。
- 已与 Responses API reference、Structured Outputs docs、Tool Calling docs、RAG/Memory evidence 和 Prompt Injection evidence 交叉验证上下文工程边界；output array、message roles、instructions、structured outputs 和 prompt-in-code guidance 支撑“LLM 应用输入输出不只是字符串”的窄结论。长上下文治理边界仍由 Responses / context management 资料、Google Responsible AI、RAG/Memory evidence 和标准库失败模式共同支撑，而不是只靠本页。

## 可能的问题

- 文档中具体模型名称和推荐会随时间变化；手册正文不应把某个模型名写成长期学习结论。
- 文档解释 OpenAI API 语义，其他供应商或框架可能使用不同字段名。
- Message role 优先级有助于组织上下文，但不是安全边界，外部内容仍需权限隔离和校验。
- `output_text` 是 SDK convenience shortcut，不适合替代结构化 `output` item 解析；涉及工具调用、reasoning、refusal 或结构化输出时仍应按 API 对象处理。
- Reusable prompt objects 的退役时间线是当前产品状态；教程应优先写 code-managed prompt builders，不应把旧 prompt object 入口写成长期稳定路径。

## 初学者阅读建议

- 先读第 02 章理解输入、输出、上下文窗口和结构化输出，再把该文档当作 OpenAI API 细节查询资料。

## 可复现实验

- 已完成标准库上下文治理与结构化输出实验，验证输出解析和长上下文治理的最小失败模式。
- 已完成标准库上下文策略对比实验，比较 full stuffing、recency-only、lossy summary、keyword RAG 和 governed context，验证 source id、trust/freshness 和 human gate trace 的最小边界。
- 后续仍需真实 Responses API 请求，记录纯文本输出、tool call 输出、structured output、refusal 和长上下文 / RAG / 摘要成本。

## 是否进入正文

- 结论：进入
- 原因：第 02 章需要官方文档支撑模型输入输出、角色优先级、Responses API 选择、prompt 版本管理和测试/eval 边界；可与 Responses API reference、RAG/Memory evidence、Prompt Injection evidence 和标准库实验共同支撑“输入输出不是简单字符串函数”和“长上下文不能替代治理”的确定性工程边界。
