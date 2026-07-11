# AI Agent 学习手册

这本手册面向 AI Agent 初学者，目标是从基础概念出发，逐步进入工具调用、记忆、RAG、规划、评测和生产化。

本项目的重点是：资料经过校验，结论可以追溯，学习路径由浅入深。

## 如何阅读

建议按下面顺序学习：

1. 先读主题地图，建立整体认知。
2. 再按章节目录逐章学习。
3. 每章先看通俗解释，再看工作原理和工程实践。
4. 遇到关键结论时检查 references。
5. 对工程结论优先看 evidence 和 experiments。

## 当前状态

当前处于证据升级和真实实验准备阶段。章节正文、source cards、claim ledger、coverage matrix 和多组标准库实验已经建立；`可入正文` 只表示窄口径概念、协议或工程边界可追溯，真实模型、真实 API、真实框架、成本、延迟和稳定性仍需继续实验验证。

## 核心文档

- [项目 Goal](governance/goal.md)
- [质量标准](governance/quality-standard.md)
- [主题地图](topic-map.md)
- [术语边界表](glossary.md)
- [初学者学习路径](learning-path.md)
- [章节目录](chapter-outline.md)
- [00. 序言：如何学习 AI Agent](chapters/00-preface.md)
- [01. AI Agent 是什么](chapters/01-agent-landscape.md)
- [02. LLM 基础与上下文工程](chapters/02-llm-context.md)
- [03. Tool Use、Function Calling 与 Structured Output](chapters/03-tool-use.md)
- [04. Agent 架构模式](chapters/04-agent-architecture.md)
- [05. MCP 与工具生态](chapters/05-mcp.md)
- [06. RAG、Memory 与知识库治理](chapters/06-rag-memory.md)
- [07. Planning、Orchestration 与多 Agent](chapters/07-planning-orchestration.md)
- [08. Evaluation 与 Observability](chapters/08-evaluation-observability.md)
- [09. Production：安全、权限、成本与部署](chapters/09-production-security.md)
- [10. 框架生态比较](chapters/10-framework-landscape.md)
- [11. 实践项目路线](chapters/11-practice-roadmap.md)
- [12. 论文、文档与资料地图](chapters/12-source-map.md)
- [References 覆盖矩阵](references/coverage-matrix.md)
- [候选资料清单](sources/seed-candidates.md)
- [Source Card 索引](sources/source-card-index.md)
- [待验证问题](evidence/validation-backlog.md)
- [Evidence Notes 索引](evidence/README.md)
- [结论证据台账](evidence/claim-ledger.md)
- [实验与复现](experiments/README.md)
