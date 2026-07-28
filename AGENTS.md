# Wiki Documentation Agent System

This project uses an ensemble of agents to help populate a wiki-style documentation archive.

## Directory Structure
- `wiki/` — The wiki documentation repository (cloned from remote)
- `drafts/` — Sandbox for unprocessed raw data and work-in-progress drafts
- `config/trusted-sources.yaml` — Whitelist of external domains approved as trusted sources

## Source Authority and Verification

OpenCode-Wiki-Agents follows SHLD-Brain source discipline. Repository sources override the model's background, cached, or training-data knowledge.

Source authority order:

1. `wiki/` pages that the user explicitly approved reading by exact path.
2. User-provided material in `drafts/`, including raw notes, uploaded/source files, and generated `.cache-*` files that preserve source mappings.
3. External URLs whose domains are listed in `config/trusted-sources.yaml`.
4. Non-whitelisted external URLs only after explicit user approval.
5. Model/background/cached AI knowledge only as `Needs verification` unless verified by one of the sources above.

Rules:
- Do not present model/background/cached AI knowledge as fact when repository or approved source material is absent.
- If a useful claim is not supported by `wiki/`, `drafts/`, a trusted source, or a user-approved external source, label it `Needs verification`.
- If repository sources conflict with model/background knowledge, repository sources win.
- If approved sources conflict with each other, report the contradiction instead of silently choosing one.
- Online sources outside `config/trusted-sources.yaml` require explicit user approval before being fetched, saved, summarized, or used as evidence.

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
