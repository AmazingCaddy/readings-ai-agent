# Real LangGraph Memory Store Validation

## 目标

用真实 LangGraph `InMemoryStore` 跑一个最小长期记忆 store 行为检查，验证 namespace、`put` / `get` / `search` / `delete`、应用层编辑历史和 trace 脱敏的本地可观察流程。

## 实验边界

本实验不调用模型，也不验证 LangGraph agent graph 的记忆收益。它只验证 LangGraph memory store 的本地存储原语和应用层治理包装方式。

重要边界：`InMemoryStore` 提供 namespace 和 store 操作，但跨用户授权、敏感记忆过滤、编辑历史、删除策略和 trace 脱敏仍需要应用层设计；不能写成框架默认自动保证。

## 运行方式

```bash
uv run --with langgraph --with langchain-core python docs/experiments/real-langgraph-memory-store-validation/real_langgraph_memory_store_validation.py
```

没有 LangGraph 时，脚本会返回 `skipped`，不会把真实框架行为写成已验证结论。

## 观察点

- user-specific namespace search 是否只返回该 user namespace 下的 memory。
- 过宽的 namespace prefix search 是否可能看到多个 user namespace。
- 应用层 edit wrapper 是否能在覆盖 active memory 前写入 invalidated history。
- `delete` 后 active memory 是否从 `get` / `search` 中消失。
- trace 是否避免泄露合成 secret marker。

## 结论状态

- 当前状态：已完成本地 LangGraph `InMemoryStore` run。
- 可支撑：真实框架 store 层的 namespace、put/get/search/delete、应用层历史包装和 trace 脱敏的最小观察。
- 不能支撑：长期记忆提升任务质量、真实模型正确使用记忆、真实持久化数据库、真实鉴权/UI、组织权限、合规删除、跨进程持久化、成本、延迟或生产 memory framework 默认安全。
