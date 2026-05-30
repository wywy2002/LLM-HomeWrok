import re


def extract_action_items(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    items: list[str] = []
    seen: set[str] = set()
    for line in lines:
        cleaned = line.lstrip("-* ").strip()
        if cleaned.startswith("[ ]"):
            cleaned = cleaned.removeprefix("[ ]").strip()
        normalized = cleaned.lower()
        if normalized.startswith("todo:") or normalized.startswith("action:") or cleaned.endswith("!") or "[ ]" in line:
            if normalized not in seen:
                seen.add(normalized)
                items.append(cleaned)
    return items


def extract_tags(text: str) -> list[str]:
    seen: set[str] = set()
    tags: list[str] = []
    for match in re.findall(r"#([A-Za-z0-9_-]+)", text):
        lowered = match.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        tags.append(lowered)
    return tags
