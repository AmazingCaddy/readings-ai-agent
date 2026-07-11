# tau2-bench / tau3-bench Current Repository and Documentation

- 来源链接：https://github.com/sierra-research/tau2-bench
- 论文链接：https://arxiv.org/abs/2506.07982
- 相关论文：https://arxiv.org/abs/2603.04370
- Leaderboard / 项目入口：https://taubench.com
- 相关说明：https://sierra.ai/blog/benchmarking-agents-in-collaborative-real-world-scenarios
- 作者 / 机构：Sierra Research / Princeton NLP authorship as listed in arXiv metadata and repository materials
- 发布时间：tau2-bench repo created 2025-06-09；tau2 paper published 2025-06-09；tau-Knowledge paper published 2026-03-04
- 最后复核日期：2026-07-12
- 类型：Benchmark repository / Papers / Documentation
- 主题：Tool-agent eval / Dual-control user interaction / Knowledge-aware eval / Voice eval / State-based reward
- 适合阶段：进阶 / Evaluation / Observability
- 可信度等级：A/B
- 是否已验证：GitHub repo metadata、README、Getting Started、Evaluation docs、arXiv API metadata for `2506.07982` and `2603.04370`、`taubench.com` HEAD 和 Sierra blog HEAD 已于 2026-07-12 复核；支撑 current benchmark entry point、domain/task/evaluation design 和 reward/action 边界；未本地安装或运行，不能支撑 leaderboard 数字、真实模型能力、voice provider 行为、真实业务相关性、成本、延迟或生产可用性

## 一句话总结

tau2-bench 是当前 tau-bench 系列的主要工程入口：它把工具 Agent 评测扩展到 dual-control 用户交互、知识检索和语音场景，但本手册只把它作为评测设计和试跑入口 reference，不把 README、论文或 leaderboard 数字写成当前模型能力证明。

## 核心结论

- `sierra-research/tau2-bench` 是本次复核采用的当前 canonical repository；搜索到的 `saksornr/tau3-bench` 是 fork，不应作为主要证据入口。
- README 说明 tau3-bench 已加入 `banking_knowledge` knowledge-retrieval domain、voice full-duplex、75+ task fixes 和 updated leaderboard。
- README 把框架定位为 customer-service agents simulation framework，支持 text half-duplex 和 voice full-duplex；domain 包含 policy、tools、tasks 和可选 user tools。
- tau2 paper 摘要说明 benchmark 引入 Telecom dual-control domain，agent 和 user 都能在 shared dynamic environment 中使用 tools，并把问题建模为 Dec-POMDP。
- tau-Knowledge paper 摘要说明 knowledge-intensive setting 需要在 live user interaction 中检索并应用 unstructured corpus；tau-Banking 约含 700 个互相关联知识文档和 tool-mediated account updates。
- Evaluation docs 明确 `evaluation_criteria.actions` 是 one reference trajectory，不是默认唯一正确动作路径；除非 `RewardType.ACTION` 进入 `reward_basis`，否则 agent 不必复现这条动作轨迹。
- Evaluation docs 说明 airline / retail / telecom 默认 `reward_basis` 是 `DB` + `COMMUNICATE`；`ACTION` 只用于少量 `banking_knowledge` tasks。Leaderboard score 使用 task `reward_basis`，diagnostic partial action reward 不是 correctness。

## 支撑证据

- GitHub API 于 2026-07-12 返回 `sierra-research/tau2-bench` 为 public、`fork: false`、MIT license、Python、default branch `main`、`archived: false`、homepage `https://www.taubench.com`。
- GitHub repo metadata 显示 created `2025-06-09T23:46:17Z`、updated `2026-07-11T12:34:54Z`、pushed `2026-07-02T00:09:34Z`。
- README 于 2026-07-12 可达，写明 Python 3.12+、arXiv `2506.07982`、blog、leaderboard、`uv sync`、`tau2 run --domain airline --agent-llm gpt-4.1 --user-llm gpt-4.1 --num-trials 1 --num-tasks 5`，并说明 results saved to `data/simulations/`。
- README 的 tau3-bench section 写明新增 `banking_knowledge` domain、configurable RAG pipelines、document search、embeddings、agentic shell-based search、voice full-duplex with realtime providers、75+ task fixes 和 updated leaderboard。
- Getting Started docs 于 2026-07-12 可达，写明 prerequisite 是 uv 和 Python 3.12+，可选 extras 包括 `voice`、`knowledge`、`gym`、`dev`、`experiments` 和 `all-extras`，并说明 API keys 通过 `.env` / LiteLLM 配置。
- Getting Started docs 说明 voice mode 需要 ElevenLabs / Deepgram 和 custom voices；output 包括 text monolithic JSON 或 voice artifacts / audio / logs / `llm_debug` 目录，可用 `tau2 view` 查看。
- Evaluation docs 于 2026-07-12 可达，说明 final reward 是 `evaluation_criteria.reward_basis` components 的 product；`actions` replayed on fresh gold env to derive target DB end state，而不是默认要求 agent 走同一路径。
- arXiv API for `2506.07982` 于 2026-07-12 返回 title `$tau^2$-Bench: Evaluating Conversational Agents in a Dual-Control Environment`，published / updated `2025-06-09T17:52:18Z`，摘要支撑 dual-control、shared dynamic environment、user tools、task generator、user simulator 和 reasoning vs communication/coordination error 分析。
- arXiv API for `2603.04370` 于 2026-07-12 返回 title `$tau$-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge`，published / updated `2026-03-04T18:34:47Z`，摘要支撑 unstructured knowledge、tau-Banking、约 700 个 knowledge docs 和 tool-mediated account updates 的研究设置。
- `https://taubench.com` 于 2026-07-12 HEAD 返回 HTTP 200，`last-modified: Thu, 02 Jul 2026 00:10:16 GMT`；该可达性只证明入口存在，不证明 leaderboard 内容正确或稳定。

## 是否进入正文

- 结论：进入；作为第 08 章 Evaluation / Observability 和第 12 章 Source Map 的当前 benchmark 入口与评测边界 reference。
- 可支撑：工具 Agent 评测需要关注用户也能行动的 dual-control 场景、知识检索、语音交互、DB / communication / action reward basis、reference trajectory 和真实试跑入口。
- 不可支撑：当前模型能力、leaderboard 数字、真实业务 Agent 质量、用户模拟可靠性、voice provider 行为、RAG pipeline 质量、成本、延迟、生产可用性或安全性。

## 可能的问题

- 本手册未本地安装或运行 tau2-bench / tau3-bench；依赖、API key、provider、数据、任务修复和结果查看流程仍待真实试跑验证。
- Leaderboard 和论文数字随模型、任务修复、provider、prompt、运行配置和评测代码变化，不能写成稳定事实。
- LLM user simulator、LLM judge / NL assertions、auto error identification 和 voice providers 都可能引入评测噪声，需要人工抽样复核。
- `evaluation_criteria.actions` 容易被误读为唯一正确动作序列；实际应先看 `reward_basis`，区分 DB / COMMUNICATE / ACTION。
- voice full-duplex 和 knowledge retrieval 模式需要额外 provider / RAG 配置；不能把 README 的可用模式等同于本地已验证能力。
- Fork 或第三方镜像可能出现在搜索结果中；本卡使用 `sierra-research/tau2-bench` 作为当前主入口。

## 初学者阅读建议

- 先读本手册第 08 章，理解 benchmark、trace、trajectory 和 regression set。
- 再读本卡的 Evaluation docs 结论：重点理解“状态评测”和“reference trajectory 不等于唯一正确路径”。
- 不建议初学者直接跑完整 benchmark；可以先学习它如何定义 domain、policy、tools、tasks、user simulator、reward basis 和 output artifacts。

## 可复现实验

- 后续可做小样本试跑：选择 text half-duplex 的 1 个 domain、少量任务、固定 agent/user model、保存 simulation JSON、trace、成本、延迟、失败分类和人工 spot review。
- 知识检索实验应单独记录 document search / embedding / RAG config、citation / retrieval trace、DB state、communication result 和 NL assertion / action reward 误判。
- voice full-duplex 实验应单独记录 provider、voice setup、audio artifacts、latency、turn-taking failure、transcription / synthesis error 和成本。
