# 质量标准

## 广度

覆盖 AI Agent 学习所需的主要主题，不遗漏初学者建立完整认知所需的基础概念、工程组件和生态工具。

必须覆盖：

- AI Agent 基本定义、边界与发展脉络
- LLM 基础与上下文工程
- Tool use、function calling、structured output
- Agent 架构模式：ReAct、Plan-and-Execute、workflow-agent hybrid、状态机
- MCP 与工具生态
- RAG、长期记忆、短期记忆和知识库治理
- Planning、orchestration、多 Agent 协作
- Evaluation、observability、trace、benchmark
- Production：权限、安全、成本、延迟、部署、审计
- Prompt injection、数据边界和工具权限风险
- 主流框架和生态
- 实践项目路线

## 深度

每个核心主题至少包含：

- 基础直觉
- 工作原理
- 适用场景
- 失败模式
- 工程取舍
- 代表框架或实现
- 关键论文、官方文档或源码 references
- 可复现实验或验证建议

## 精度

必须准确区分这些概念：

- Agent vs Workflow
- Agent vs Chatbot
- Tool Use vs Function Calling
- RAG vs Memory
- Short-term Memory vs Long-term Memory
- Planning vs Orchestration
- MCP Server vs MCP Client
- Eval vs Benchmark vs Observability
- Autonomy vs Automation

避免使用“Agent 就是会自己思考的 AI”这类泛化说法。更准确的表达是：Agent 是围绕模型推理、工具调用、状态管理和目标执行构建的系统形态，自治程度取决于控制循环和权限设计。

## 正确性

重要结论必须有 references 支撑。优先采用：

- 官方文档
- 学术论文
- 标准或协议文档
- 开源项目源码和示例
- 主流框架文档
- 有真实上下文的一线工程实践

观点类资料必须标注可信度和适用边界。营销文、无来源断言、过时内容不能直接进入正文。

## 可学习性

读者假设为初学者。章节必须由浅入深：

1. 先讲直觉：这是什么，为什么重要。
2. 再讲概念：核心术语和边界。
3. 再讲机制：它如何工作。
4. 再讲工程：什么时候用，怎么用，哪里容易失败。
5. 最后给进阶资料和 references。

## 可追溯性

GitHub Pages 最终正文中的关键概念、结论、图表、最佳实践和争议点都要附 references 超链接。

