# Week 4 开发控制中心说明

## 仓库工作流

- 在 `week4/` 目录运行应用：`make run`
- 运行后端测试：`make test`
- 运行格式化和 lint：`make format`、`make lint`

## 关键入口

- FastAPI 应用：`backend/app/main.py`
- Notes 路由：`backend/app/routers/notes.py`
- Action items 路由：`backend/app/routers/action_items.py`
- 提取逻辑：`backend/app/services/extract.py`
- 测试目录：`backend/tests/`
- 种子数据：`data/seed.sql`

## 推荐自动化流程

1. 先为行为变更补测试或更新测试
2. 再实现后端或前端改动
3. 重新运行 `make test`
4. 再运行 `make format` 和 `make lint`
5. 最后总结接口变化和 UI 影响

## 安全边界

- 不要使用破坏性的 git 命令
- 改动尽量限制在 `week4/` 内
- 除非任务明确要求，否则不要改动种子数据
