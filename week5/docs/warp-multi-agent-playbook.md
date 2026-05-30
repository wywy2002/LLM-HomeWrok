# Warp 多 Agent 协作手册

这个手册把 week 5 的任务拆到多个独立 Warp 标签页中。

## Agent 分工

- Agent 1：notes 搜索、分页和 CRUD
- Agent 2：action item 过滤和 bulk complete
- Agent 3：前端接线与基本交互检查

## 协作方式

1. 每个 agent 只在 `week5/` 内工作
2. 编辑前先说明自己要改哪些文件
3. 与后端相关的 agent 在完成后执行 `pytest backend/tests -q`
4. 最终整合 agent 负责合并结果并重新跑共享测试集

## 风险

- 多个 agent 同时修改 schema 时容易冲突
- 如果不先声明接口结构，前端和后端可能出现 payload 漂移
- 保持一份简短共享检查表，通常就能避免大多数冲突
