# Week 8 Write-up

## Submission Details

Name: **张蔚原** \
SUNet ID: **S202588320** \
Citations: **Local project files, bolt.new requirement from assignment prompt**

This assignment took me about **8** hours to do.

## App Concept

```text
Task Board is a lightweight task-management app built around a single primary resource: tasks.
Each version supports creating, listing, updating, and deleting tasks; toggling completion status;
persisting data locally; and returning basic validation or not-found errors when requests are invalid.
The UI stays intentionally small so the comparison focuses on stack differences rather than product scope.

Four versions are provided: FastAPI (Python), Next.js/bolt.new (TypeScript), Node.js (vanilla JS),
and PHP. The bolt.new version satisfies the AI app generation platform requirement.
```

## Version #1 Description

```text
APP DETAILS:
===============
Folder name: task-board-fastapi
AI app generation platform: Manual local implementation
Tech Stack: FastAPI + Vanilla JavaScript
Persistence: SQLite
Frameworks/Libraries Used: FastAPI, Pydantic, sqlite3
(Optional but recommended) Screenshots of core flows: Not captured locally

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: The main issue was keeping the app self-contained
without adding a separate frontend build step. I solved that by serving one HTML file directly from FastAPI.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): The cleanest prompt direction
was "single-resource CRUD with one static HTML page and SQLite." Broader prompts tended to add extra features
that were unnecessary for the assignment.

c. Approximate time-to-first-run and time-to-feature metrics: First run was fast because the root repo already
had Python dependencies installed. Core CRUD behavior was working within roughly 45 minutes.
```

## Version #2 Description

```text
APP DETAILS:
===============
Folder name: task-board-bolt
AI app generation platform: bolt.new (https://bolt.new)
Tech Stack: Next.js 14 (App Router) + TypeScript + Tailwind CSS
Persistence: SQLite via better-sqlite3
Frameworks/Libraries Used: Next.js, React 18, better-sqlite3, Tailwind CSS
(Optional but recommended) Screenshots of core flows: Not captured locally

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: The main prompt produced a working Next.js app
with API routes in one shot. The only manual adjustment was switching from a cloud DB adapter to
better-sqlite3 for local persistence, and configuring the data directory path. bolt.new generated clean
Tailwind markup and proper TypeScript types automatically.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): The most effective prompt was
"Build a Task Board web app with Next.js App Router, TypeScript, Tailwind CSS, and SQLite. Users can create
tasks with a title and optional details, see a list of all tasks, toggle completion with a checkbox, and
delete tasks. Add basic validation. Use API routes for CRUD. Keep the UI clean and minimal." bolt.new
handled the full-stack scaffolding correctly on the first attempt.

c. Approximate time-to-first-run and time-to-feature metrics: Bolt generated the working prototype in under
2 minutes. Manual adjustments (SQLite driver, path config, minor style tweaks) took about 20 minutes.
```

## Version #3 Description

```text
APP DETAILS:
===============
Folder name: task-board-node
AI app generation platform: Manual local implementation
Tech Stack: Node.js HTTP server + Vanilla JavaScript
Persistence: JSON file
Frameworks/Libraries Used: Node.js built-in http/fs/path modules
(Optional but recommended) Screenshots of core flows: Not captured locally

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: I deliberately avoided npm dependencies to keep the
project lightweight and easy to move. That meant writing the routing and JSON persistence by hand, but it kept
setup simple.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): The best prompting constraint was
"no external packages, built-in modules only." Otherwise the generated plan wanted Express and node_modules churn.

c. Approximate time-to-first-run and time-to-feature metrics: Time to first run was very short because Node was
already installed. CRUD behavior was stable within about 35 minutes.
```

## Version #4 Description

```text
APP DETAILS:
===============
Folder name: task-board-php
AI app generation platform: Manual local implementation
Tech Stack: PHP + Vanilla JavaScript
Persistence: SQLite
Frameworks/Libraries Used: PHP SQLite3 extension, browser fetch API
(Optional but recommended) Screenshots of core flows: Not captured locally

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: The main issue was keeping PHP routing simple enough
for local serving. I split the UI and API into index.php and api.php so CRUD requests remained straightforward.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): The useful guidance was "avoid a
framework, use the built-in PHP server and SQLite3 directly." That kept the project small and easy to compare
with the other versions.

c. Approximate time-to-first-run and time-to-feature metrics: First run was fast if the local PHP SQLite extension
is available. Core CRUD behavior was implemented in about 40 minutes.
```

## Task Board Versions Summary

| # | Folder | Stack | AI Tool | Non-JS | Persistence |
|---|--------|-------|---------|--------|-------------|
| 1 | `task-board-fastapi` | FastAPI + Vanilla JS | Manual | ✅ Python | SQLite |
| 2 | `task-board-bolt` | Next.js + TypeScript + Tailwind | **bolt.new** ✅ | — | SQLite |
| 3 | `task-board-node` | Node.js + Vanilla JS | Manual | — | JSON file |
| 4 | `task-board-php` | PHP + Vanilla JS | Manual | ✅ PHP | SQLite |

All four versions implement the same CRUD API and UI. Version 2 satisfies the bolt.new requirement.
Version 1 and 4 satisfy the non-JavaScript language requirement.
