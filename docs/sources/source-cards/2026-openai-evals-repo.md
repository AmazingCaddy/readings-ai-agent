# OpenAI Evals Repository

- 来源链接：https://github.com/openai/evals
- 作者 / 机构：OpenAI
- 发布时间：持续更新 repository
- 最后复核日期：2026-07-11
- 类型：Source Code / Evaluation
- 主题：Evaluation / Benchmark / Regression
- 适合阶段：工程实践
- 可信度等级：A
- 是否已验证：来源链接已复核；README 关键段落已精读；benchmark 不能替代业务 eval、工具/副作用 Agent 的 trace-aware eval 和 trace 字段用途设计窄边界可入正文；trace schema audit 和 grader misalignment / reward hacking audit 已完成；真实 eval harness 和自动评分仍部分验证

## 一句话总结

OpenAI Evals repository 是理解 eval 结构、评测数据和回归测试思路的源码 reference。

## 核心结论

- README 将 Evals 定义为评估 LLM 或基于 LLM 构建的系统的 framework。
- README 明确支持 existing registry，也支持为具体 use case 写 custom evals，或用私有数据建立 private evals。
- README 指出没有 eval 时，很难理解不同模型版本如何影响具体 use case。
- README 提到对于 prompt chains 或 tool-using agents 等高级用例，可以使用 Completion Function Protocol。
- README 同时提醒运行 eval 有 API 成本，贡献数据也涉及数据权利和使用政策。

## 支撑证据

- GitHub repository 页面返回 HTTP 200；raw README 返回 HTTP 200。
- README 写明：“Evals provide a framework for evaluating large language models (LLMs) or systems built using LLMs.”
- README 写明可以 write your own custom evals for use cases you care about，也可以 build private evals。
- README 写明 advanced use cases like prompt chains or tool-using agents 可以使用 Completion Function Protocol。
- README 写明 good eval requires careful thought and rigorous experimentation。

## 可能的问题

- eval 工具和推荐实践可能随时间演进；README 已提示可以直接在 OpenAI Dashboard 配置和运行 Evals。
- OpenAI Evals README 支撑“可为工具型 Agent 设计 eval”，但不直接定义 trajectory 自动评分标准。

## 初学者阅读建议

- 先理解“为什么需要 eval”，再看 repository 结构和示例。

## 可复现实验

- 已完成标准库 trace-aware eval 模拟实验，比较 final-only 与 trace-aware scoring 能发现的错误类型。
- 已完成标准库 trace schema audit，验证 regression 需要 dataset、case、expected/actual、failure category、model/prompt/tool schema version 等字段；该结果支撑 trace 字段按用途设计的窄边界，后续仍需映射到真实 eval harness。
- 已完成标准库 grader misalignment / reward hacking audit，验证自动评分器需要 edge cases、误判统计和人工校准；后续仍需真实 judge / platform grader 对照。
- Real Trace-Aware Eval harness 已完成本地 deterministic scorer control：通过 toy traces 记录 tool call、tool result/error、approval rejection 和 final response，并输出 final-only / trace-aware 两套评分；当前无 API key，真实模型 trace 未运行，不能提前升级真实模型 trace 或 grader 效果结论。

## 是否进入正文

- 结论：进入；custom/private eval 和 trace-aware eval 窄边界可入正文
- 原因：可支撑 custom eval、private eval 和 tool-using agent eval 的工程思路；结合 AgentBench / WebArena，可支撑“公开 benchmark 不能替代业务 eval”的窄边界。标准库 trace-aware eval、Real Trace-Aware Eval scorer control、trace schema audit 和 grader misalignment audit 已覆盖最小评分/回归字段、过程评分和自动评分误判结构，并将“工具/副作用 Agent 不能只看最终答案”“trace 字段要按用途设计”和“自动 grader 需要人工校准”的窄结论升级为可入正文。真实模型 trace、Dashboard / Completion Function Protocol 具体入口、真实 LLM-as-judge 和人工复核实验仍待验证。
