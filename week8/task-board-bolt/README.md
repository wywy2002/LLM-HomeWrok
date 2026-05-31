# Task Board — Bolt.new Edition (Next.js + SQLite)

This version was generated using **[bolt.new](https://bolt.new)**, an AI app generation platform. It implements the same Task Board CRUD functionality as the other versions using a modern full-stack JavaScript framework.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Frontend**: React 18 + Tailwind CSS 3
- **Backend**: Next.js API Routes
- **Persistence**: SQLite via `better-sqlite3`
- **Styling**: Tailwind CSS (utility-first)

## Prerequisites

- **Node.js** >= 18
- **npm** >= 9

## Quick Start

```bash
# Install dependencies
npm install

# Run the dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create a task (`{ title, details }`) |
| PUT | `/api/tasks/:id` | Update a task (`{ title, details, completed }`) |
| DELETE | `/api/tasks/:id` | Delete a task |

## Bolt.new Generation Notes

This app was created by providing the following prompt to bolt.new:

> "Build a Task Board web app with Next.js App Router, TypeScript, Tailwind CSS, and SQLite. Users can create tasks with a title and optional details, see a list of all tasks, toggle completion with a checkbox, and delete tasks. Add basic validation: title is required (max 120 chars), details max 500 chars. Use API routes for CRUD. Keep the UI clean and minimal."

### Manual Adjustments After Generation

- Added `better-sqlite3` as the SQLite driver (bolt.new defaulted to a different DB adapter).
- Configured `data/` directory for persistent local storage.
- Minor style refinements for consistency with other Task Board versions.

## Deviations & Known Issues

- SQLite requires a native module compile step; if `npm install` fails, ensure your system has build tools installed (Python, C++ compiler on Windows, or Xcode Command Line Tools on macOS).
- No authentication — same scope as the other versions.
