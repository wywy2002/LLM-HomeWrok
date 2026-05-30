import re


TAG_PATTERN = re.compile(r"#([A-Za-z0-9_-]+)")


def extract_action_items(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    results: list[str] = []
    seen: set[str] = set()
    for line in lines:
        cleaned = line.lstrip("-* ").strip()
        if cleaned.startswith("[ ]"):
            cleaned = cleaned.removeprefix("[ ]").strip()
        normalized = cleaned.lower()
        if (
            normalized.startswith("todo:")
            or normalized.startswith("action:")
            or cleaned.endswith("!")
            or "[ ]" in line
        ):
            if cleaned.lower() not in seen:
                seen.add(cleaned.lower())
                results.append(cleaned)
    return results


def extract_tags(text: str) -> list[str]:
    seen: set[str] = set()
    tags: list[str] = []
    for match in TAG_PATTERN.findall(text):
        lowered = match.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        tags.append(lowered)
    return tags


