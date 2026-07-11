# Evidence Notes 索引

本页把手册中的 evidence notes 按主题集中列出。它不是新的结论来源，而是帮助读者从章节正文追溯到 claim ledger、source cards 和实验结果。

阅读顺序建议：先看[结论证据台账](claim-ledger.md)，再按主题打开对应 evidence note；如果某条结论涉及真实模型、真实框架、成本或稳定性，继续看[待验证问题清单](validation-backlog.md)。

## Agent 基础与架构

- [Agent 与 Workflow 边界](agent-workflow-boundary.md)
- [Agent 自治程度边界](autonomy-level-boundary.md)
- [Agent 架构模式边界](agent-architecture-pattern-boundary.md)
- [多 Agent 不是默认更好](multi-agent-default-boundary.md)

## LLM、上下文与工具

- [上下文工程与结构化输出边界](context-structured-output-boundary.md)
- [Tool Use 与 Function Calling 边界](tool-use-function-calling-boundary.md)
- [Tool / Function / Plugin 术语对照边界](tool-terminology-crosswalk.md)
- [工具权限、人工确认与审计边界](tool-permission-audit-boundary.md)

## MCP、RAG 与 Memory

- [MCP Host / Client / Server 职责边界](mcp-role-boundary.md)
- [MCP 安全、授权与权限边界](mcp-security-permission-boundary.md)
- [RAG 与 Memory 边界](rag-memory-boundary.md)
- [RAG 工程流程边界](rag-engineering-boundary.md)
- [长期记忆治理与风险边界](memory-governance-risk-boundary.md)

## Evaluation、Observability 与 Production

- [Agent Eval 与 Trajectory 边界](agent-eval-trajectory-boundary.md)
- [Observability 与 Trace 工程边界](observability-trace-boundary.md)
- [Prompt Injection 与权限边界](prompt-injection-permission-boundary.md)

## 框架生态与实践

- [框架生态定位边界](framework-landscape-boundary.md)
- [框架能力交叉表与选择边界](framework-capability-crosswalk.md)
- [实践路线与 Cookbook 示例边界](practice-roadmap-cookbook-boundary.md)

## 状态说明

- `可入正文`：窄口径概念、协议或工程边界已经有 references / 标准库实验支撑。
- `部分验证`：真实模型、真实 API、真实框架、成本、延迟、稳定性或生产效果仍需实验。
- `待验证`：只能作为问题或下一步，不应写成确定性正文。
