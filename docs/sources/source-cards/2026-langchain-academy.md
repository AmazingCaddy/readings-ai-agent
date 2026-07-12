# LangChain Academy Repository

- 来源链接：https://github.com/langchain-ai/langchain-academy；https://raw.githubusercontent.com/langchain-ai/langchain-academy/main/README.md；https://academy.langchain.com/
- 作者 / 机构：LangChain / LangChain AI
- 发布时间：GitHub repo 创建于 2024-07-23；README 未给出单独发布日期
- 最后复核日期：2026-07-12
- 类型：Course / Open Source Educational Material / Notebook Repository
- 主题：LangGraph 入门 / Agent workflow / Memory / Human feedback / Deployment / Practice Roadmap
- 适合阶段：入门 / 实践路线 / 框架初体验
- 可信度等级：B+
- 是否已验证：GitHub repo metadata、raw README、requirements、root directory、module 1-6 directory listings 和 `module-1/simple-graph.ipynb` 抽样已于 2026-07-12 复核；可支撑 LangGraph 跟练路线、环境依赖、notebook / Studio / deployment 练习边界；公开 academy 站点当前返回 Cloudflare challenge / HTTP 403，未作为已读网页证据；没有本地运行 notebooks、真实模型、LangSmith Studio、Tavily 或部署流程，真实成本、延迟、可复现性和生产可靠性仍未验证

## 一句话总结

LangChain Academy 的开源仓库是一套以 LangGraph 为主线的 notebook 课程材料，适合把本手册第 11 章的 workflow、state、memory、human feedback 和 deployment 练习落成可跟练项目，但不能替代 LangGraph 官方文档或本地试跑。

## 核心结论

- README 把课程定位为 `Introduction to LangGraph`，Module 0 是 basic setup，Modules 1-5 逐步构建 LangGraph，Module 6 处理部署 agents。
- README 要求 Python 3.11 / 3.12 / 3.13、clone repo、创建 venv、安装 `requirements.txt`、运行 Jupyter notebook，并设置 `OPENAI_API_KEY`、`LANGSMITH_API_KEY` / tracing project 和部分课程用到的 `TAVILY_API_KEY`。
- README 说明每个 module folder 包含 notebooks，notebook 顶部有 LangChain Academy lesson 链接；module 1-5 还有 `studio` 子目录，用于配合 LangGraph API 和 Studio。
- root directory 包含 `module-0` 到 `module-6`、`requirements.txt` 和 `LICENSE`，适合作为分阶段跟练路线，而不是单篇教程。
- module 1 覆盖 simple graph、router、chain、agent、agent memory 和 deployment；抽样的 `simple-graph.ipynb` 展示 `StateGraph`、`START` / `END`、node function、conditional edge、compile、Mermaid visualization 和 `invoke`。
- module 2 覆盖 state schema、state reducers、multiple schemas、trim/filter messages、chatbot summarization 和 external memory。
- module 3 覆盖 breakpoints、dynamic breakpoints、edit state / human feedback、streaming interruption 和 time travel，适合和本手册 HITL / interrupt / resume 边界一起读。
- module 4 覆盖 map-reduce、parallelization、sub-graph 和 research assistant，适合作为编排结构练习；本次没有运行任何 web research 或 Tavily 相关代码。
- module 5 覆盖 memory store、memory schema profile / collection 和 memory agent，适合补充长期记忆练习的工程入口，但不证明 memory 质量提升或治理充分。
- module 6 覆盖 assistant、creating、connecting、double texting 和 deployment 目录，适合作为部署主题入口；本次没有验证真实部署、并发恢复、double texting 策略或 LangSmith Studio 行为。

## 支撑证据

- 2026-07-12 复核 GitHub HTML `https://github.com/langchain-ai/langchain-academy` 返回 HTTP 200；GitHub API 返回 repo public、owner `langchain-ai`、default branch `main`、archived `false`、language `Jupyter Notebook`、license `MIT`、created `2024-07-23T23:57:41Z`、updated `2026-07-11T13:11:17Z`、pushed `2026-06-15T16:01:24Z`。
- Raw README 返回 HTTP 200；README 写明课程是 `Welcome to LangChain Academy, Introduction to LangGraph!`，Module 0 是 setup，Modules 1-5 聚焦 LangGraph，Module 6 addresses deploying your agents。
- README 的 setup 要求 Python 3.11 / 3.12 / 3.13，clone repo，创建 venv，`pip install -r requirements.txt`，运行 Jupyter notebook。
- README 明确需要设置 `OPENAI_API_KEY`；如使用 LangSmith，还需 `LANGSMITH_API_KEY`、`LANGSMITH_TRACING_V2="true"` 和 `LANGSMITH_PROJECT="langchain-academy"`；Module 4 部分课程使用 Tavily，需要 `TAVILY_API_KEY`。
- README 的 Studio 小节说明 module 1-5 的 `studio` 文件夹可用 `langgraph dev` 启动本地 server，并给出 API、Studio UI 和 API Docs 的本地 URL 示例。
- `requirements.txt` 包含 `langgraph`、`langgraph-prebuilt`、`langgraph-sdk`、`langgraph-checkpoint-sqlite`、`langsmith>=0.7.31`、`langchain-community`、`langchain-core>=1.2.28`、`langchain-openai>=1.1.14`、`langchain-tavily`、`notebook`、`trustcall` 和 `langgraph-cli[inmem]` 等依赖。
- GitHub contents API root 返回 `.devcontainer`、`README.md`、`LICENSE`、`requirements.txt` 和 `module-0` 到 `module-6`。
- GitHub contents API `module-1` 返回 `simple-graph.ipynb`、`router.ipynb`、`chain.ipynb`、`agent.ipynb`、`agent-memory.ipynb`、`deployment.ipynb` 和 `studio/`。
- 抽样 `module-1/simple-graph.ipynb` raw 内容：notebook 顶部包含 Colab 和 LangChain Academy lesson 链接；正文标题为 `The Simplest Graph`，构建 3 个 nodes 和 1 个 conditional edge；代码使用 `TypedDict` state、`StateGraph`、`START`、`END`、node functions、conditional edge、`compile()`、Mermaid visualization 和 `graph.invoke(...)`。
- GitHub contents API `module-2` 返回 `state-schema.ipynb`、`state-reducers.ipynb`、`multiple-schemas.ipynb`、`trim-filter-messages.ipynb`、`chatbot-summarization.ipynb`、`chatbot-external-memory.ipynb`、`state_db/` 和 `studio/`。
- GitHub contents API `module-3` 返回 `breakpoints.ipynb`、`dynamic-breakpoints.ipynb`、`edit-state-human-feedback.ipynb`、`streaming-interruption.ipynb`、`time-travel.ipynb` 和 `studio/`。
- GitHub contents API `module-4` 返回 `map-reduce.ipynb`、`parallelization.ipynb`、`sub-graph.ipynb`、`research-assistant.ipynb` 和 `studio/`。
- GitHub contents API `module-5` 返回 `memory_store.ipynb`、`memoryschema_profile.ipynb`、`memoryschema_collection.ipynb`、`memory_agent.ipynb` 和 `studio/`。
- GitHub contents API `module-6` 返回 `assistant.ipynb`、`creating.ipynb`、`connecting.ipynb`、`double-texting.ipynb` 和 `deployment/`。
- 公开站点 `https://academy.langchain.com/` 于 2026-07-12 返回 Cloudflare challenge / HTTP 403；因此本卡只引用 GitHub repo、raw README、requirements、contents API 和 notebook raw 抽样，不把 academy 网站课程页面当成已读证据。

## 可能的问题

- 这是课程仓库和 notebook 材料，不是 LangGraph API specification；API 语义、版本兼容和生产部署边界仍应以 LangGraph / LangSmith 官方文档和本地实验为准。
- 本卡没有运行任何 notebook，也没有安装 repo requirements；不能证明依赖组合、API key 设置、LangSmith Studio、Tavily search、deployment 或 double-texting 示例在本机可复现。
- 多数练习依赖真实 OpenAI / LangSmith / Tavily key 或本地 Studio；本手册当前没有这些真实 run 的成本、延迟、trace、失败样例或初学者阻塞点。
- 课程 notebook 的输出、图示和示例状态只能作为学习材料，不应写成 LangGraph 在真实任务中默认更可靠、更便宜或更适合生产。
- 公开 academy 站点当前被 Cloudflare challenge 阻断，不能把网页课程正文、视频、测验或登录后内容当作已验证资料。

## 和其他资料的对比

- 与 LangGraph docs 一致：都适合学习 state graph、nodes、edges、conditional routing、persistence / memory 和 human-in-the-loop 相关概念；LangChain Academy 更偏 notebook 跟练，LangGraph docs 更适合作为 API / 行为边界依据。
- 与 Hugging Face Agents Course 一致：二者都可作为初学者外部课程地图；Hugging Face 覆盖 Agent/tool/framework/eval 的更宽路线，LangChain Academy 更集中在 LangGraph notebook 实作。
- 与本手册 Real LangGraph Interrupt Recovery / Memory Store harness 的关系：课程可作为后续真实跟练入口，但当前本地 harness 才能支撑本手册已验证的最小 runtime surface；课程本身不证明 interrupt recovery、memory governance 或 deployment safety。
- 与 OpenAI Practical Guide / Cookbook 的关系：LangChain Academy 可补 workflow/state/memory/HITL notebook 练习，但不能替代 use-case 判断、tool risk rating、guardrails、cost/latency 和安全治理资料。

## 初学者阅读建议

- 先读 README 的 setup、API key 和 Studio 小节，确认自己是否准备好 OpenAI、LangSmith 和 Tavily 依赖。
- 如果只想理解 LangGraph 概念，先看 module 1 的 `simple-graph.ipynb`、`router.ipynb` 和 `agent.ipynb`，把 nodes、edges、state、conditional routing 和 `invoke` 跑通或手动读懂。
- 学到 memory 时，先对照本手册第 06 章的写入守门、权限和删除边界，再读 module 2 / module 5，避免把 memory 示例写成默认质量收益。
- 学到 human feedback / interrupt 时，先对照本手册第 09 章审批状态恢复和 Real LangGraph Interrupt Recovery 的边界，再读 module 3，不要把 notebook 里的暂停/恢复当成生产幂等或审计已完成。
- 学到 deployment 时，把 module 6 当成练习入口；真实部署仍需要记录 state storage、并发、审批 UI、trace 脱敏、成本、延迟和回滚策略。

## 可复现实验

- 最小练习：只运行 `module-1/simple-graph.ipynb`，记录 Python version、依赖版本、`StateGraph` 定义、nodes/edges、conditional routing、compiled graph、`invoke` 输出和是否需要网络/API key。
- 进阶练习：运行 module 3 的 human feedback / interruption notebook，并与本手册 Real LangGraph Interrupt Recovery 字段对齐：approval payload、resume command、重复 resume、参数完整性、trace 脱敏和副作用幂等。
- Memory 练习：运行 module 5 的 memory store / memory agent notebook，并记录 namespace、写入触发、查看/删除、跨用户隔离、过时事实处理、成本和延迟；这一步不能替代真实 memory governance 实验。
- Deployment 练习：运行 module 6 / Studio 相关材料时，记录 `langgraph dev`、本地 API / Studio URL、环境变量、状态存储、并发、失败恢复、trace、成本和初学者阻塞点。

## 是否进入正文

- 结论：部分进入
- 原因：可作为第 10/11/12 章中 LangGraph 外部跟练路线和 notebook 课程参考，支撑 state graph、routing、memory、human feedback、Studio 和 deployment 练习主题；不能用于证明 LangGraph 真实模型行为、部署可靠性、memory 质量、HITL 幂等、LangSmith Studio 行为、Tavily search 质量、成本、延迟或生产表现。
