# Week 3 GitHub 仓库 MCP Server

这是一个本地 STDIO MCP server，封装了 GitHub 公共 REST API。

## 提供的工具

- `get_repo_summary(owner, repo)`
  - 返回仓库基础信息，例如描述、主要语言、star 数和 open issue 数
- `list_open_issues(owner, repo, limit=5)`
  - 返回仓库最新的 open issue，并过滤掉 pull request

## 为什么选 GitHub API

GitHub API 稳定、文档清晰，而且很适合作为 MCP 场景中的仓库检索与仓库梳理工具。

## 前置要求

- 已安装仓库根目录里的 Python 依赖
- 可选：设置 `GITHUB_TOKEN`，用于提高 rate limit

## 本地运行

在仓库根目录执行：

```powershell
.venv\Scripts\python.exe week3\server\main.py
```

这个命令会以 STDIO 方式启动服务。

## Claude Desktop 配置示例

本地 MCP server 条目可以写成：

```json
{
  "command": "E:\\GitCode\\LLM-HomeWork\\modern-software-dev-assignments\\.venv\\Scripts\\python.exe",
  "args": ["E:\\GitCode\\LLM-HomeWork\\modern-software-dev-assignments\\week3\\server\\main.py"]
}
```

## 示例调用

- “用 `get_repo_summary` 查看 `microsoft/vscode`”
- “列出 `pallets/flask` 的 3 个 open issue”

## 可靠性说明

- 使用了 `httpx` timeout
- 上游 HTTP 失败会直接抛出明确错误
- 支持可选 `GITHUB_TOKEN`，避免太快触发限流
