# Wiki Documentation Agent System

An ensemble of opencode agents that helps populate a wiki-style documentation archive.

## Project Structure

```
├── opencode.json           # Agent definitions and custom commands
├── AGENTS.md               # Project rules (injected into every session)
├── wiki/                   # Wiki repository (cloned from remote)
├── drafts/                 # Sandbox for raw data and work-in-progress drafts
└── .opencode/prompts/      # System prompt files for each agent
```

## Quick Start

```bash
opencode
```

The **init-worker** runs automatically on start and verifies that `wiki/` and `drafts/` exist.

## Workflow

| Step | User Action | Agent | What Happens |
|---|---|---|---|---|
| 1 | Paste raw notes, command output, diagrams into **`drafts/`** | — | Unprocessed source data lands in the sandbox |
| 2 | `/research <topic>` | **researcher** | Searches the web, groups results semantically, asks which URLs to fetch, saves raw data to `drafts/` (also reads specific wiki pages if user specifies a path) |
| 3 | `/contextualize` | **contextualizer** | Scans `drafts/`, asks you to describe each file, builds an information cache (`.cache-*.md`) |
| 4 | `/draft create a page about <topic>` | **scribe** | Reads the cache + relevant raw files, produces a formatted markdown page with frontmatter, saves to `drafts/` |
| 5 | Review the draft in `drafts/` | — | Make any edits you want |
| 6 | `/publish` | **publisher** | Lists finalized drafts, asks which to copy into `wiki/`, handles adds/replacements/deletes |
| 7 | `/sync` | **git-worker** | Shows git diff, asks for a commit message and your confirmation, then commits and pushes |

## Agents

| Agent | Command | Responsibility |
|---|---|---|
| **init-worker** | runs automatically | Verifies `wiki/` is a valid git repo and `drafts/` exists |
| **researcher** | `/research` | Searches the web, groups URLs semantically, fetches with user approval, saves raw data to `drafts/` |
| **contextualizer** | `/contextualize` | Interprets raw files by asking you questions, creates append-only cache |
| **scribe** | `/draft <description>` | Produces wiki-formatted markdown drafts with YAML frontmatter |
| **publisher** | `/publish` | Writes confirmed drafts from `drafts/` into `wiki/` |
| **git-worker** | `/sync` | Stages, commits, and pushes with user confirmation at each step |

## Important Rules

- **`wiki/` is read-only** — agents never read or write it without your explicit permission.
- **`drafts/` is the sandbox** — all raw data and drafts go here.
- **Confirm every step** — the publisher and git-worker always ask before making changes.
