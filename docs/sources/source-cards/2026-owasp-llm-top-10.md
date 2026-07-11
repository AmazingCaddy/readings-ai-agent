# OWASP Top 10 for Large Language Model Applications

- 来源链接：https://owasp.org/www-project-top-10-for-large-language-model-applications/
- 作者 / 机构：OWASP
- 发布时间：持续更新项目；页面 last-modified 复核为 2025-12-29
- 最后复核日期：2026-07-11
- 类型：Security Guidance
- 主题：Security / Prompt Injection / LLM Application Risk
- 适合阶段：工程实践 / 生产化
- 可信度等级：A
- 是否已验证：来源链接已复核；内容待精读；结论待交叉验证

## 一句话总结

OWASP LLM Top 10 是构建 Agent 安全章节的基础安全 reference，适合解释 prompt injection、数据泄露、供应链和过度授权等风险。

## 核心结论

- 待精读后提取。

## 支撑证据

- OWASP 项目页面返回 HTTP 200。

## 可能的问题

- OWASP 是安全风险分类，不是具体框架实现指南。
- 需要和实际工具权限、MCP 安全、部署审计资料结合。

## 初学者阅读建议

- 不需要一次读完所有风险项。先关注 prompt injection、sensitive information disclosure、excessive agency 和 insecure plugin/tool design 相关内容。

## 可复现实验

- 构造一个包含恶意指令的外部文档，测试工具型 Agent 是否会越权执行。

## 是否进入正文

- 结论：进入
- 原因：Production / Security 章节必须有独立安全 reference。

