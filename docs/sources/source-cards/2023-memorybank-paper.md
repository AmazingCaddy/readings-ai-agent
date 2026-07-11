# MemoryBank: Enhancing Large Language Models with Long-Term Memory

- 来源链接：https://arxiv.org/abs/2305.10250
- 作者 / 机构：Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, Yanlin Wang
- 发布时间：2023-05-17；arXiv v3 updated 2023-05-21
- 最后复核日期：2026-07-11
- 类型：论文
- 主题：Long-term Memory / Personalization / Conversational Agents
- 适合阶段：进阶
- 可信度等级：A
- 是否已验证：arXiv 元数据和摘要已复核；长期记忆价值与治理边界已完成第一轮交叉验证

## 一句话总结

MemoryBank 研究 LLM 长期记忆机制，适合用于讨论个人化、持续交互和记忆更新策略。

## 核心结论

- 摘要描述 MemoryBank 允许模型召回相关记忆、持续更新记忆，并通过历史交互理解用户画像。
- 摘要称其引入受 Ebbinghaus Forgetting Curve 启发的记忆更新机制，用于遗忘和强化记忆。
- 论文场景偏长期 AI companion / counseling-style interaction，可支撑“持续交互中长期记忆可能有价值”的保守表述。

## 支撑证据

- arXiv API 返回有效条目：`2305.10250v3`。
- 2026-07-11 抓取 arXiv 页面成功；摘要包含 relevant memories、continuous memory updates、user personality、forgetting curve、forget/reinforce memory 等关键表述。
- 已与 MemGPT、Generative Agents、Letta、Zep、OWASP 和 NIST 交叉验证长期记忆治理边界。

## 可能的问题

- 论文强调 companion / counseling 等持续交互场景，不应泛化到所有 Agent 任务。
- 需要额外关注隐私、用户画像、错误记忆、过时记忆和自动写入带来的风险。

## 初学者阅读建议

- 先理解 RAG 和 memory 的区别，再读这类长期个人化记忆论文。

## 可复现实验

- 模拟多轮用户偏好变化，测试长期记忆是否能更新、遗忘并避免旧偏好污染。

## 是否进入正文

- 结论：作为进阶资料进入
- 原因：长期记忆章节需要有具体机制论文支撑；正文必须保守表达为“可能有价值，但需要治理”。
