# OpenAI Evals Repository

- 来源链接：https://github.com/openai/evals
- 作者 / 机构：OpenAI
- 发布时间：持续更新 repository
- 最后复核日期：2026-07-12
- 类型：Source Code / Evaluation
- 主题：Evaluation / Benchmark / Regression
- 适合阶段：工程实践
- 可信度等级：A
- 是否已验证：GitHub repo metadata、README、`docs/build-eval.md`、`docs/completion-fns.md` 和目录 API 已于 2026-07-12 复核；custom/private eval、dataset + eval class、registry/YAML、completion function 和 model-graded eval human-label/meta-eval 的窄边界可入正文；trace schema audit、grader misalignment / reward hacking audit 和 Real Trace-Aware Eval 本地 scorer control 已完成；真实 eval harness、旧 Evals platform / dashboard 路线和自动评分可靠性仍部分验证

## 一句话总结

OpenAI Evals repository 是理解 eval 结构、评测数据和回归测试思路的源码 reference。

## 核心结论

- README 将 Evals 定义为评估 LLM 或基于 LLM 构建的系统的 framework。
- README 明确支持 existing registry，也支持为具体 use case 写 custom evals，或用私有数据建立 private evals。
- README 顶部仍指向 OpenAI Dashboard 配置和运行 Evals；但官方 deprecations 页面已经记录 Evals platform 退役时间线，因此本手册只把 repo / dashboard 入口当作迁移前现状和方法参考，不写成长期稳定教程。
- README 指出没有 eval 时，很难理解不同模型版本如何影响具体 use case。
- README 提到对于 prompt chains 或 tool-using agents 等高级用例，可以使用 Completion Function Protocol。
- README 同时提醒运行 eval 有 API 成本、registry data 使用 Git LFS，贡献数据也涉及数据权利和使用政策。
- `build-eval.md` 把构建 eval 拆成 dataset、注册 eval、运行 eval，并提示命名需要 split/version；model-graded eval 建议用 human-provided choice labels 做 meta-eval。
- `completion-fns.md` 将 completion function 描述为模型 completion 的泛化，可把浏览器等 under-the-hood 操作包装成标准输入输出接口。

## 支撑证据

- 2026-07-12 使用 `curl -L -I https://github.com/openai/evals` 复核，GitHub repository 页面返回 HTTP 200。
- 2026-07-12 使用 GitHub API 复核 `openai/evals` metadata：`default_branch=main`，`archived=false`，`language=Python`，`updated_at=2026-07-11T17:09:40Z`，`pushed_at=2026-04-14T15:29:57Z`。
- 2026-07-12 使用 `curl -L -I https://raw.githubusercontent.com/openai/evals/main/README.md` 复核 raw README，返回 HTTP 200，`content-type: text/plain; charset=utf-8`，`content-length: 6463`。
- GitHub contents API 显示仓库根目录包含 `docs`、`evals`、`examples`、`scripts`、`tests` 和 `pyproject.toml`；`evals` 目录包含 `cli`、`completion_fns`、`elsuite`、`registry`、`record.py`、`metrics.py` 等源码/registry 入口。
- README 写明：“Evals provide a framework for evaluating large language models (LLMs) or systems built using LLMs.”
- README 写明可以 write your own custom evals for use cases you care about，也可以 build private evals。
- README 写明 advanced use cases like prompt chains or tool-using agents 可以使用 Completion Function Protocol。
- README 写明 good eval requires careful thought and rigorous experimentation。
- `build-eval.md` 写明构建 eval 是 dataset and a choice of eval class，并覆盖 JSONL data、`evals/registry/evals/<eval_name>.yaml`、`oaieval`、model-graded evals、human-provided choice labels 和 meta-eval。
- `completion-fns.md` 写明 completion function 标准化输入为 text string 或 chat conversation，输出为 text string list，并可通过 `--registry_path` 在外部项目注册。

## 可能的问题

- eval 工具和推荐实践可能随时间演进；README 已提示可以直接在 OpenAI Dashboard 配置和运行 Evals，但官方 deprecations 页面已写明旧 Evals platform 在 2026-10-31 read-only、2026-11-30 shutdown。本手册不能把 dashboard/API/CLI 路线写成长期稳定教程。
- OpenAI Evals README 和 completion function docs 支撑“可为工具链或 Agent-like 系统设计 eval”，但不直接定义通用 trajectory 自动评分标准，也不证明工具执行、trace capture、LLM-as-judge 或平台字段在真实业务中可靠。
- README / build-eval 还涉及贡献数据权利、API 成本、Git LFS 数据和 custom code contribution 限制；初学者练习时应优先做小型私有 harness，不要直接上传敏感或无授权数据。

## 初学者阅读建议

- 先理解“为什么需要 eval”，再看 repository 结构和示例。

## 可复现实验

- 已完成标准库 trace-aware eval 模拟实验，比较 final-only 与 trace-aware scoring 能发现的错误类型。
- 已完成标准库 trace schema audit，验证 regression 需要 dataset、case、expected/actual、failure category、model/prompt/tool schema version 等字段；该结果支撑 trace 字段按用途设计的窄边界，后续仍需映射到真实 eval harness。
- 已完成标准库 grader misalignment / reward hacking audit，验证自动评分器需要 edge cases、误判统计和人工校准；后续仍需真实 judge / platform grader 对照。
- Real Trace-Aware Eval harness 已完成本地 deterministic scorer control：通过 toy traces 记录 tool call、tool result/error、approval rejection 和 final response，并输出 final-only / trace-aware 两套评分；当前无 API key，真实模型 trace 未运行，不能提前升级真实模型 trace 或 grader 效果结论。

## 是否进入正文

- 结论：进入；custom/private eval、dataset + registry/YAML、completion function 和 trace-aware eval 的窄边界可入正文。
- 原因：可支撑 custom eval、private eval、model-graded eval human-label calibration 和 tool/prompt-chain completion function 的工程思路；结合 AgentBench / WebArena，可支撑“公开 benchmark 不能替代业务 eval”的窄边界。标准库 trace-aware eval、Real Trace-Aware Eval scorer control、trace schema audit 和 grader misalignment audit 已覆盖最小评分/回归字段、过程评分和自动评分误判结构，并将“工具/副作用 Agent 不能只看最终答案”“trace 字段要按用途设计”和“自动 grader 需要人工校准”的窄结论升级为可入正文。真实模型 trace、Dashboard/API/CLI 具体入口、Completion Function Protocol 真实运行、真实 LLM-as-judge 和人工复核实验仍待验证；旧 Evals platform / dashboard / API 路线不能写成长期稳定教程。
