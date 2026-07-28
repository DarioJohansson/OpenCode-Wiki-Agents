# Wiki Documentation Agent System

An ensemble of opencode agents that helps populate a wiki-style documentation archive.

## Project Structure

```
├── opencode.json           # Agent definitions and custom commands
├── AGENTS.md               # Project rules (injected into every session)
├── config/trusted-sources.yaml # Trusted external source whitelist
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

1. **Populate `drafts/`** — Paste raw notes, command output, or diagrams into the sandbox.
2. **`/research <topic>`** *(optional)* — Researcher searches the web, fetches approved sources, and saves raw data to `drafts/`.
3. **`/contextualize`** — Contextualizer scans `drafts/`, asks you to describe each file, and builds an information cache.
4. **`/draft <description>`** — Scribe reads the cache and raw files, then produces a formatted wiki page draft in `drafts/`.
5. **Review** — Edit the draft in `drafts/` as needed.
6. **`/publish`** — Publisher lists finalized drafts, asks which to copy into `wiki/`.
7. **`/sync`** — Git-worker shows the diff, asks for a commit message, then commits and pushes.

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

## Source Discipline

The repository source system overrides AI model background or cached knowledge.

Source authority order:

1. `wiki/` pages approved by exact path.
2. User-provided material in `drafts/` and generated `.cache-*` files.
3. External sources listed in `config/trusted-sources.yaml`.
4. Non-whitelisted external sources only after user approval.
5. Model/background/cached AI knowledge only as `Needs verification` unless verified by one of the sources above.

If sources conflict, the agent should report the conflict. If a claim is useful but unsupported, it must be marked `Needs verification` instead of being presented as fact.
