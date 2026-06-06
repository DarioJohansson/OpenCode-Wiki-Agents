# Wiki Documentation Agent System

This project uses an ensemble of agents to help populate a wiki-style documentation archive.

## Directory Structure
- `wiki/` — The wiki documentation repository (cloned from remote)
- `drafts/` — Sandbox for unprocessed raw data and work-in-progress drafts

## Startup Instruction
**Run `@init-worker` at the start of every session** to verify the project structure.

## Workflow Rules
1. `wiki/` is READ-ONLY unless the publisher agent is explicitly told to write.
2. All raw data and initial drafts go in `drafts/`.
3. Do NOT read or modify `wiki/` without explicit user permission.
4. The contextualizer creates `.cache-*` files in `drafts/` — these are append-only logs.

## Workflow (in order)
1. User populates `drafts/` with raw notes, output, diagrams.
2. (Optional) → `/research <topic>` — researcher searches web, fetches approved sources, saves raw data to `drafts/`.
3. User says "ready" → `/contextualize` — contextualizer asks questions and builds cache.
4. User describes the wiki page they want → `/draft <description>` — scribe produces a draft in `drafts/`.
5. User reviews and approves → `/publish` — publisher copies draft to `wiki/`.
6. User wants to save → `/sync` — git-worker shows diff, asks for commit message, commits and pushes.

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
