# Week 2 Write-up

## Submission Details

Name: **张蔚原** \
SUNet ID: **S202588320** \
Citations: **Ollama structured outputs docs, FastAPI docs, local repository code**

This assignment took me about **4.5** hours to do.

## Your Responses

For each exercise, I include the prompt intent and the main local files changed.

### Exercise 1: Scaffold a New Feature
Prompt:
```text
Analyze the existing heuristic extractor in week2/app/services/extract.py and add an
LLM-backed alternative named extract_action_items_llm(). Use Ollama structured JSON output,
lazy-load the client so tests can run without an Ollama server, and normalize duplicate items.
```

Generated Code Snippets:
```text
week2/app/services/extract.py:68-114
week2/app/routers/action_items.py:21-54
week2/app/schemas.py:1-51
```

### Exercise 2: Add Unit Tests
Prompt:
```text
Write unit tests for the new extract_action_items_llm() flow. Mock the Ollama chat call so
the tests do not require a running local model, and cover both populated and empty outputs.
```

Generated Code Snippets:
```text
week2/tests/test_extract.py:19-34
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt:
```text
Refactor the week2 backend for clearer API contracts. Add Pydantic request/response schemas,
centralize note and action item response shapes, expose a note-list endpoint, and remove
import-time side effects that break test collection in proxy-heavy environments.
```

Generated/Modified Code Snippets:
```text
week2/app/schemas.py:1-51
week2/app/db.py:47-104
week2/app/routers/notes.py:12-30
week2/app/routers/action_items.py:21-54
week2/app/main.py:1-24
```

### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt:
```text
Use the new backend endpoints to update the raw HTML frontend. Add an "Extract LLM" button
wired to /action-items/extract-llm and a "List Notes" button wired to GET /notes, while
keeping the original heuristic extraction flow intact.
```

Generated Code Snippets:
```text
week2/frontend/index.html:25-100
week2/app/routers/notes.py:20-22
week2/app/routers/action_items.py:37-45
```

### Exercise 5: Generate a README from the Codebase
Prompt:
```text
Read the current week2 codebase and generate a concise README covering setup, run commands,
available endpoints, and the test command. Mention the Ollama prerequisite only for the LLM
endpoint.
```

Generated Code Snippets:
```text
week2/README.md:1-42
```
