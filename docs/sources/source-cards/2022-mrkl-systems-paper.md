# MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning

- 来源链接：https://arxiv.org/abs/2205.00445
- DOI：https://doi.org/10.48550/arXiv.2205.00445
- 作者 / 机构：Ehud Karpas, Omri Abend, Yonatan Belinkov, Barak Lenz, Opher Lieber, Nir Ratner, Yoav Shoham, Hofit Bata, Yoav Levine, Kevin Leyton-Brown, Dor Muhlgay, Noam Rozen, Erez Schwartz, Gal Shachaf, Shai Shalev-Shwartz, Amnon Shashua, Moshe Tenenholtz
- 发布时间：2022-05-01
- 最后复核日期：2026-07-12
- 类型：论文 / Modular tool reasoning
- 主题：MRKL / Modular Reasoning / Tool Use / Neuro-symbolic architecture
- 适合阶段：入门后 / 架构历史
- 可信度等级：A
- 是否已验证：来源链接、HTTP metadata、arXiv API 元数据和摘要已于 2026-07-12 复核；支撑“把 LLM 与外部知识、离散推理模块组合成系统架构”的窄边界；真实工具路由质量、现代 function calling 行为、成本、延迟和框架表现仍部分验证

## 一句话总结

MRKL 适合用来理解早期模块化 Agent / 工具系统思想：LLM 可以作为系统中的语言组件之一，再和外部知识源、离散推理模块组合，而不是把所有知识和推理都压进同一个模型输出里。

## 核心结论

- 摘要指出大型语言模型虽然重要，但 inherent limitations 需要用 systems approach 处理。
- 摘要把问题定义为不仅包含 linguistic processing，还包含 knowledge 和 reasoning。
- 论文提出一种 flexible architecture：multiple neural models complemented by discrete knowledge and reasoning modules。
- 该架构被命名为 Modular Reasoning, Knowledge and Language system，简称 MRKL。
- 对本手册而言，稳妥结论是：工具使用和模块路由有一条系统架构历史线；现代 function calling / tool calling 可以借鉴“把语言模型和外部能力组合”的思想，但二者不是同一个 API 机制。

## 支撑证据

- 2026-07-12 抓取 arXiv 页面返回 HTTP 200；响应头 `last-modified: Tue, 03 May 2022 00:24:18 GMT`。
- arXiv API 返回有效条目：`2205.00445v1`，published / updated `2022-05-01T11:01:28Z`，primary category `cs.CL`。
- API 摘要写明 LMs are inherently limited in a number of ways，并讨论 adopting a systems approach。
- API 摘要写明 MRKL conceptualizes the challenge as one that involves knowledge and reasoning in addition to linguistic processing。
- API 摘要写明 architecture uses multiple neural models, complemented by discrete knowledge and reasoning modules，并描述 Jurassic-X as AI21 Labs' MRKL system implementation。
- arXiv 页面列出 DOI：`https://doi.org/10.48550/arXiv.2205.00445`。

## 是否进入正文

- 结论：进入；作为 Tool Use / Agent 架构历史和模块化外部能力组合的窄边界 reference。
- 原因：它与 Toolformer、ReAct、OpenAI Function Calling / Responses API 共同支撑“模型可以通过系统设计连接外部能力”的学习路径，但不能支撑现代 API 行为、工具执行可靠性或框架优劣。

## 可能的问题

- 论文是 2022 年的架构论文，不是现代 function calling API 规范。
- 摘要级证据只能支撑模块化系统思想，不能支撑具体 router 算法、工具选择准确率或生产可靠性。
- Jurassic-X 是论文中的实现案例，不等同于当前主流框架或 OpenAI / LangGraph / LlamaIndex 的工程接口。
- 正文不应写成“MRKL 证明工具路由可靠”或“MRKL 等于 Function Calling”。

## 初学者阅读建议

- 先读本手册第 03 章，理解 Tool Use 和 Function Calling 的执行边界。
- 再读 MRKL 摘要，把重点放在“为什么需要把 LLM 和外部知识 / 推理模块组合”。
- 阅读时要和现代 API 分开：MRKL 是架构思想，Function Calling 是 API 交互机制。

## 可复现实验

- 本手册已完成标准库 Tool Calling 参数校验与重试实验，验证应用层校验、错误回传、有限重试和 trace 设计。
- 本手册已完成 workflow / hybrid / ReAct-like 对比实验，验证固定 workflow、受控动态查询和 tool loop 在最小任务中的差异。
- 仍需真实模型 / API / 框架实验，比较 router、tool selection、参数修正、权限审批、成本、延迟和 trace 可读性。
