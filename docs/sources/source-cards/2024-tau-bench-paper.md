# τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains

- 来源链接：https://arxiv.org/abs/2406.12045
- DOI：https://doi.org/10.48550/arXiv.2406.12045
- 作者 / 机构：Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan
- 发布时间：2024-06-17
- 最后复核日期：2026-07-11
- 类型：论文 / Benchmark / Tool-agent evaluation
- 主题：Tool-agent eval / User simulation / Domain rules / State-based evaluation
- 适合阶段：进阶 / Evaluation
- 可信度等级：A
- 是否已验证：来源链接、HTTP metadata、arXiv 元数据、摘要和 GitHub README 已复核；支撑“工具 Agent 评测需要覆盖动态用户交互、领域规则、API tools、数据库状态和多次试验一致性”的窄边界；原 `tau-bench` repo 已提示任务过期，实际试跑应优先参考 `tau2-bench` / τ³-bench；真实模型表现、leaderboard 数字和最新任务质量仍部分验证

## 一句话总结

τ-bench 适合用来理解工具型 Agent 的评测为什么不能只看最终回答：客服类任务里，Agent 要和模拟用户多轮对话、调用领域 API、遵守 policy，最后还要看数据库状态是否达到目标。

## 核心结论

- 摘要指出 existing benchmarks 不测试 language agents 与 human users 的交互，也不测试 follow domain-specific rules 的能力。
- τ-bench 用 LLM 模拟用户，与提供 domain-specific API tools 和 policy guidelines 的 language agent 进行动态对话。
- 评测流程比较 conversation 结束后的 database state 和 annotated goal state。
- 论文提出 `pass^k`，用多次试验衡量 agent behavior 的可靠性和一致性。
- 摘要报告当时 state-of-the-art function calling agents 在任务上成功率有限且不稳定；这只能作为当时 benchmark 观察，不能泛化为当前模型能力。

## 支撑证据

- arXiv 页面返回 HTTP 200；HTTP `last-modified` 为 2024-06-19。
- arXiv 元数据显示 submitted on 2024-06-17，当前版本 v1。
- 摘要写明 benchmark emulates dynamic conversations between a user simulated by language models and a language agent provided with domain-specific API tools and policy guidelines。
- 摘要写明 evaluation process compares database state at the end of a conversation with annotated goal state。
- 摘要写明 `pass^k` evaluates reliability of agent behavior over multiple trials。
- 原 GitHub repo `sierra-research/tau-bench` README 明确警告：tasks in this repo are not updated，并建议使用 `tau2-bench` / τ³-bench。
- `sierra-research/tau2-bench` README 说明 τ³-bench 是 customer service agents 的 simulation framework，支持 text half-duplex、voice full-duplex、多个 domains、policies、tools、tasks、user simulator，并记录 results。

## 是否进入正文

- 结论：进入；作为 Evaluation / Observability 和 Tool-use eval 的 benchmark reference。
- 原因：它直接支撑“工具 Agent 评测应覆盖用户交互、工具调用、领域规则、状态变化和多次试验一致性”的窄结论；同时 repo 过期警告也能提醒读者不要把 leaderboard 数字当成当前生产能力证明。

## 可能的问题

- 原始 τ-bench repo 已提示 airline / retail tasks 不是最新版本，不能直接作为当前最可靠任务集。
- README leaderboard 数字会随模型、任务修复、运行策略和版本变化，不应写进正文作为稳定事实。
- 使用 LLM user simulator 和自动错误定位会引入额外不确定性，README 也提醒 auto error identification 可能不准确。
- 真实业务 Agent 仍需要自己的数据、权限边界、人工复核和回归集；公开 benchmark 不能替代业务 eval。

## 初学者阅读建议

- 先读本手册第 08 章，理解 eval、benchmark、trace 和 trajectory。
- 阅读 τ-bench 摘要时重点看三件事：用户模拟、工具/API、数据库状态评测。
- 不建议初学者一上来试跑完整 benchmark；可以先学习它的任务结构和状态评测思想，再做小型自定义 regression set。

## 可复现实验

- 本手册已完成标准库 trace-aware eval 实验，显示 final-answer-only scoring 会漏掉无审批副作用工具和工具错误未恢复。
- 本手册已完成 trace schema audit，说明工具、权限、错误、成本、RAG 和 privacy 需要不同 trace 字段。
- 后续真实实验可选择 τ³-bench 的小任务子集试跑，记录安装阻塞、API key、成本、延迟、失败分类、用户模拟误差和人工复核样例。
