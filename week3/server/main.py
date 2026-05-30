from __future__ import annotations

import logging
import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("github_mcp_server")

mcp = FastMCP("github-repo-helper")

GITHUB_API_BASE = "https://api.github.com"
DEFAULT_TIMEOUT = 15.0


def _headers() -> dict[str, str]:
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "week3-github-mcp-server",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


async def _get_json(path: str, params: dict[str, Any] | None = None) -> Any:
    url = f"{GITHUB_API_BASE}{path}"
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT, headers=_headers()) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_repo_summary(owner: str, repo: str) -> dict[str, Any]:
    """Return high-level metadata for a public GitHub repository."""
    data = await _get_json(f"/repos/{owner}/{repo}")
    return {
        "full_name": data["full_name"],
        "description": data["description"],
        "default_branch": data["default_branch"],
        "language": data["language"],
        "stargazers_count": data["stargazers_count"],
        "open_issues_count": data["open_issues_count"],
        "html_url": data["html_url"],
    }


@mcp.tool()
async def list_open_issues(owner: str, repo: str, limit: int = 5) -> list[dict[str, Any]]:
    """Return the newest open issues for a repository, excluding pull requests."""
    if limit < 1 or limit > 20:
        raise ValueError("limit must be between 1 and 20")
    data = await _get_json(
        f"/repos/{owner}/{repo}/issues",
        params={"state": "open", "per_page": limit, "sort": "created", "direction": "desc"},
    )
    issues: list[dict[str, Any]] = []
    for item in data:
        if "pull_request" in item:
            continue
        issues.append(
            {
                "number": item["number"],
                "title": item["title"],
                "user": item["user"]["login"],
                "created_at": item["created_at"],
                "html_url": item["html_url"],
            }
        )
    return issues


def main() -> None:
    logger.info("Starting GitHub MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
