# OpenAI Function Calling / Tool Calling Documentation

- 来源链接：https://developers.openai.com/api/docs/guides/function-calling
- 作者 / 机构：OpenAI
- 发布时间：持续更新文档；页面 last-modified 复核为 2026-07-11
- 最后复核日期：2026-07-11
- 类型：官方文档
- 主题：Tool Use / Function Calling / Structured Output
- 适合阶段：入门 / 工程实践
- 可信度等级：A
- 是否已验证：来源链接已复核；内容待精读；结论待交叉验证

## 一句话总结

这是解释现代 OpenAI API 中工具调用和函数调用机制的首选官方 reference。

## 核心结论

- 待精读后提取。

## 支撑证据

- 旧入口 `https://platform.openai.com/docs/guides/function-calling` 会 301 到 `https://developers.openai.com/api/docs/guides/function-calling`。
- 最终页面返回 HTTP 200。

## 可能的问题

- 官方 API 文档更新频繁，需要记录复核日期。
- 需要和 OpenAI Agents SDK 文档区分：这是 API 层 tool calling，不是完整 Agent SDK 抽象。

## 初学者阅读建议

- 先理解 tool schema、参数生成、工具结果回传，再看 SDK 框架封装。

## 可复现实验

- 设计一个参数校验失败的工具调用，观察模型是否能根据错误信息修正参数。

## 是否进入正文

- 结论：进入
- 原因：Tool Use / Function Calling 章节需要官方 API reference。

