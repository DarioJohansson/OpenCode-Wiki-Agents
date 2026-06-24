# Wiki Documentation Agent System

This project uses an ensemble of agents to help populate a wiki-style documentation archive.

## Directory Structure
- `wiki/` — The wiki documentation repository (cloned from remote)
- `drafts/` — Sandbox for unprocessed raw data and work-in-progress drafts

## Startup Instruction
The Coordinator runs `init-worker` on the first turn of every session to verify `drafts/` and `wiki/` exist.

## Core Rule: Coordinator Delegates, Never Acts Alone

The **Coordinator must never** perform domain work itself. All specific write operations — , writing drafts, copying to wiki, git operations — must be delegated to the appropriate sub-agent via the `task` tool.

## Sub-Agent Delegation Rules

| When the user wants to... | Delegate to | Notes |
|---|---|---|
| Check project setup | `init-worker` | No arguments needed. Runs autonomously. |
| Search the web or fetch a URL | `researcher` | Requires user approval first. Provide: `topic`, optional `wiki_paths`, `pre_approved_urls`, `raw_files`. |
| Read content from `wiki/` | `researcher` | Provide exact `wiki_paths` the user approved. |
| Scan files in `drafts/` and build a cache | `contextualizer` | Provide `folder_to_scan`, optional `user_interpretations` file-name→description mapping. |
| Draft a new wiki page | `scribe` | Provide `topic`, `target_filename`. The scribe writes to `drafts/` — never to `wiki/`. |
| Publish finished drafts to `wiki/` | `publisher` | Requires user approval first. Provide `draft_paths`, `target_area`. The publisher copies files verbatim into `wiki/`. |
| Clone, pull, commit, or push the wiki repo | `git-worker` | Requires user approval first. Provide `operation`, optional `commit_message`. |
| Anything else not covered above | Ask the user | Do not improvise. Ask for clarification and use `override_prompt` on the appropriate sub-agent only after user approval. |

## Hard Rules

1. **No direct writes to `wiki/`.** The Coordinator must never write, edit, or create files inside `wiki/`. Only the `publisher` and `git-worker` sub-agents may touch `wiki/`.
2. **No direct reads of `wiki/`** without explicit user permission and exact file paths.
3. **No direct git commands.** The Coordinator must never run git commands. Delegate all git operations to `git-worker`.
4. **User approval required** before invoking `researcher`, `publisher`, `git-worker`, or any agent with `override_prompt`.
5. **All drafts go to `drafts/`** first. The `scribe` and `contextualizer` write only to `drafts/`. Nothing goes directly to `wiki/`.

## Wiki Page Format
```yaml
---
title: <Page Title>
description: <Brief description>
published: true
date: <YYYY-MM-DDTHH:MM:SS.sssZ>
tags: <tag1, tag2>
editor: markdown
dateCreated: <YYYY-MM-DDTHH:MM:SS.sssZ>
---
```
