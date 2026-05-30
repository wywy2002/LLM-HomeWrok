# Warp Drive 自动化 A：搜索与 CRUD 工作流

目标：自动化 notes 搜索、分页、CRUD 编辑以及回归测试这一组高频后端循环。

建议的 Warp prompt：

```text
In week5/, implement or update note search pagination and CRUD.
Then run backend/tests and summarize changed routes, validation behavior, and any failing tests.
```

输入：
- `docs/TASKS.md` 中的可选任务目标
- 可选的后端测试路径

输出：
- 更新后的后端文件
- 测试结果摘要
- 接口变化清单

步骤：
1. 先检查 `backend/app/routers/notes.py` 及其相关 schema / tests
2. 实现所需接口变更
3. 执行 `pytest backend/tests -q`
4. 报告修改点和仍需人工检查的部分
