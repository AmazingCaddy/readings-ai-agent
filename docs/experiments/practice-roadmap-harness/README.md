# 实践路线 Smoke Harness

## 目标

验证第 11 章的实践路线是否能被拆成可运行、可验收、可记录 trace 的最小练习单元。这个实验覆盖结构化输出、工具参数校验、RAG 引用、unsupported question 拒答和成本预算闸门；同时审计跟练项目卡片是否具备初学者需要的 prerequisites、commands、acceptance checks、trace fields、failure examples、references 和 boundary notes。

## 实验边界

这是一个确定性的 Python 标准库实验，不调用模型、不联网、不接入真实 OpenAI API 或 Cookbook notebook。它不能证明 Cookbook recipe 的真实依赖、成本或稳定性，只能验证本地学习路线可以有明确输入、输出、验收标准、trace、失败样例和边界说明。

## 覆盖项目

- 项目 1：结构化输出和 refusal 记录。
- 项目 2：工具参数错误、应用层校验和修正后执行。
- 项目 3：RAG 答案引用和资料不足拒答。
- 项目 7：把练习组织成可重复运行的 eval cases。
- 项目 8：成本预算检查和拒绝执行。
- 进阶项目：Repo Issue Agent toy 的命令、测试、diff、approval 和 redaction 记录结构。

## 运行方式

```bash
uv run python docs/experiments/practice-roadmap-harness/practice_roadmap_harness.py
```

## 观察点

- 每个练习是否有可机器检查的成功标准。
- 每个跟练项目是否包含 prerequisites、setup/run commands、acceptance checks、trace fields、failure examples、references 和 boundaries。
- 每个跟练项目是否至少有一个可重复运行的 `uv run ...` 命令。
- 每个跟练项目是否明确说明本地 control 不能替代真实 API / 模型 / 框架验证。
- trace 是否能说明失败发生在输出格式、工具参数、检索引用还是预算闸门。
- unsupported question 是否能明确拒答，而不是编造。
- 成本预算是否能在执行前阻断高成本请求。

## 结论状态

- 支撑：第 11 章可以强调“实践项目要有验收标准、trace 和失败分类”。
- 支撑：第 11 章可以强调“初学者跟练项目要写清 prerequisites、命令、references、失败样例和适用边界”，否则很容易把 demo 当成可靠教程。
- 支撑：初学者路线可以先用无模型、无网络的 smoke harness 练习结构和评测，再迁移到真实 API / Cookbook recipe。
- 仍缺：真实 Structured Outputs、File Search/RAG、OpenAI Evals、Agents SDK trace/eval、Usage/Cost 和 Rate limits 的本地试跑。
