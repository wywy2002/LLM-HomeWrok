# Week 2 行动项提取器

本周项目是在原始 FastAPI + SQLite 笔记处理器基础上扩展出的双路径提取器：

- 一个基于规则的行动项提取器，支持项目符号、复选框和祈使句
- 一个基于 Ollama 的 LLM 提取器，返回结构化行动项列表

## 环境准备

1. 创建并激活 Python 环境。
2. 在仓库根目录安装依赖。
3. 如果要使用 LLM 提取接口，需要单独安装并启动 Ollama，并确保本地已有可用模型，例如 `llama3.1:8b`。

## 运行项目

在仓库根目录执行：

```powershell
.venv\Scripts\python.exe -m uvicorn week2.app.main:app --reload
```

然后打开 `http://127.0.0.1:8000`。

## API 接口

- `POST /notes`
  - 通过 `{ "content": "..." }` 创建一条笔记
- `GET /notes`
  - 返回所有已保存笔记
- `GET /notes/{note_id}`
  - 返回单条笔记
- `POST /action-items/extract`
  - 通过 `{ "text": "...", "save_note": true }` 进行规则提取
- `POST /action-items/extract-llm`
  - 通过 `{ "text": "...", "save_note": true }` 进行 Ollama 提取
- `GET /action-items`
  - 返回行动项列表，可按 `note_id` 过滤
- `POST /action-items/{id}/done`
  - 通过 `{ "done": true }` 更新完成状态

## 测试

在仓库根目录执行：

```powershell
.venv\Scripts\python.exe -m pytest week2/tests -q
```

## 说明

- 前端已经加入规则提取、LLM 提取和列出笔记三个按钮。
- LLM 路径采用延迟导入，因此即使 Ollama 没启动，应用和测试也能正常加载。
