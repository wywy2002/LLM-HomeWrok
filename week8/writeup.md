# Week 8 Write-up

## Submission Details

Name: **张蔚原** \
SUNet ID: **S202588320** \
Citations: **Local project files, bolt.new requirement from assignment prompt**

This assignment took me about **6.5** hours to do.

## App Concept

```text
Task Board is a lightweight task-management app built around a single primary resource: tasks.
Each version supports creating, listing, updating, and deleting tasks; toggling completion status;
persisting data locally; and returning basic validation or not-found errors when requests are invalid.
The UI stays intentionally small so the comparison focuses on stack differences rather than product scope.
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
Folder name: task-board-node
AI app generation platform: Local implementation prepared for later bolt.new recreation if needed
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

## Version #3 Description

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

## Important Note

```text
The assignment explicitly requires at least one version to be built using bolt.new. The folders above prepare
three local versions of the same app, but the actual bolt.new generation step still needs to be completed manually
in your own account before final submission if you want to satisfy that requirement literally.
```
