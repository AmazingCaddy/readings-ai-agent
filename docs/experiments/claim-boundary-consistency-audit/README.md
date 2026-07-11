# Claim Boundary Consistency Audit

## 目标

检查证据控制文档是否继续区分窄口径 `可入正文` 结论和真实模型 / API / 框架表现的待验证边界。

这个 harness 不证明资料事实正确，也不替代人工精读；它只把容易回归的文字边界做成可运行检查：

- Claim ledger 中每条 `可入正文` 结论的正文写法必须包含限制条件或待验证边界。
- Coverage matrix 中每个主题必须保留非空缺口。
- Coverage matrix 的 `可入正文` 状态摘要必须保留部分验证 / 待验证 / 不证明等边界措辞。
- 已知过期短语不能重新出现，例如把已完成 no-key local control 的 harness 写成“入口已准备但 completed run 待做”。

## 运行方式

```bash
uv run python docs/experiments/claim-boundary-consistency-audit/claim_boundary_consistency_audit.py
```

## 结果解释

- `all_passed=true`：文本结构没有发现上述边界回归。
- `real_fact_validation=false`：该检查不验证外部资料事实、不调用真实模型、不验证真实 API 行为。
- `failed_checks`：列出需要人工修正或调整规则的检查项。

## 当前结论

当前结果见 [2026-07-12 结果](results-2026-07-12.md)。

该 audit 可支撑“手册有机器可检查的证据边界防回归”这一窄结论；不能支撑任何真实模型质量、API 行为、框架可靠性或生产效果结论。
