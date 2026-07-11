# Production Safety / Data Governance Checklist

## 目标

把 OpenAI Moderation、Safety Best Practices 和 Data Controls 文档中的生产安全与数据治理边界，整理成一个可审计的项目检查表。这个实验不是为了证明检测层、HITL、数据驻留或合规配置有效，而是为了验证：上线前应记录哪些字段，哪些数据面需要分开审查，哪些地方不能只写“已接入安全 API”。

## 实验边界

当前实验是 Python 标准库 deterministic audit。它不会调用 OpenAI API，不会读取真实组织 / project 配置，不会测试真实 moderation false positive / false negative，也不会验证任何企业数据控制能力是否已经开通。

## 资料来源

- [OpenAI Moderation Documentation](../../sources/source-cards/2026-openai-moderation-docs.md)
- [OpenAI Safety Best Practices and Data Controls Documentation](../../sources/source-cards/2026-openai-safety-data-controls-docs.md)
- [Anthropic MCP Connector and Tunnels Documentation](../../sources/source-cards/2026-anthropic-mcp-docs.md)

## 检查项

| item id | 重点 | 必查字段 |
| --- | --- | --- |
| `moderation_policy_signals` | moderation 是 policy signal，不是自动安全保证。 | moderation stage、policy action、human review queue、failure fallback |
| `tool_calling_moderation_coverage` | tool arguments / outputs 与 tool name / schema 覆盖边界不同。 | tool arguments checked、tool outputs checked、tool schema reviewed |
| `streaming_moderation_timing` | streaming scores 在完整输出后到达。 | partial delta policy、final score gate、pre-action buffer |
| `safety_identifier_logging` | abuse monitoring 需要隐私保护的用户标识和日志 join key。 | safety identifier、privacy-preserving hash、log join key |
| `api_key_revoke_runbook` | API key 泄露需要撤销、替换和影响面审计流程。 | owner、detection signal、revoke step、replacement step、impact review |
| `abuse_logs_application_state_split` | abuse logs 与 application state 是不同数据面。 | abuse log fields、application state objects、retention owner、delete path |
| `remote_mcp_third_party_data_flow` | remote MCP server 是第三方数据流。 | remote server、data sent、third-party retention、allowlist、user disclosure |
| `hosted_tool_application_state` | hosted tool 可能产生临时 application state。 | hosted tool、container state、expiration/delete、sensitive data policy |
| `data_residency_boundary` | data residency 是 project / endpoint 边界，不覆盖所有 system data。 | project region、endpoint supported、system data exclusion、unsupported feature note |
| `red_team_and_user_report_loop` | red-team 和用户举报要回流到 regression set。 | red-team cases、user report channel、response owner、regression update |

## 运行方式

```bash
uv run python docs/experiments/production-safety-data-governance/production_safety_data_governance.py
```

当前标准库结果见 [2026-07-11 结果](results-2026-07-11.md)。

## 对照组

- `naive_project`：只记录少量 moderation、remote MCP、hosted tool 和 region 信息，缺少人工复核、失败降级、schema review、API key revoke、application state、删除和数据驻留边界。
- `governed_project`：记录完整检查项，包括 policy routing、人工复核、streaming gate、隐私保护 safety identifier、API key revoke、abuse logs / application state 分离、remote MCP 第三方保留、hosted tool cleanup、data residency 限制和 red-team 回归更新。

## 结论状态

- 当前状态：标准库 checklist audit 已完成；真实项目 / 账户配置验证待跑。
- 可支撑：章节和实践路线可以写成“生产安全与数据治理检查表应覆盖 moderation 信号、tool-calling 覆盖边界、streaming 时机、safety identifier、API key revoke、abuse logs vs application state、remote MCP 数据流、hosted tool state、data residency 和 red-team / 用户举报回流”。
- 不能支撑：不能证明真实 moderation、HITL、guardrail、data retention、data residency、ZDR/MAM、API key revoke 或第三方工具数据治理充分有效。

## 下一步

1. 在真实项目中填同一 checklist，记录哪些字段可从平台配置直接确认，哪些需要应用日志或 runbook 证明。
2. 在真实 prompt injection / tool permission harness 中加入 moderation-only、policy-enforced 和 HITL 对照，记录误报、漏报、成本、延迟和人工复核负担。
3. 对 remote MCP、hosted tools、file/vector store、prompt caching 和 data residency 做对象级数据流与删除路径检查。
