# Wiki Documentation Agent System

This project uses an ensemble of agents to help populate a wiki-style documentation archive.

## Directory Structure
- `wiki/` — The wiki documentation repository (cloned from remote)
- `drafts/` — Sandbox for unprocessed raw data and work-in-progress drafts

## Startup Instruction
The Coordinator agent runs the initialization automatically at the start of every session.

## Workflow Rules
1. `wiki/` is READ-ONLY unless the publisher agent is explicitly told to write.
2. All raw data and initial drafts go in `drafts/`.
3. Do NOT read or modify `wiki/` without explicit user permission.
4. The contextualizer creates `.cache-*` files in `drafts/` — these are append-only logs.

## Workflow (Orchestrated Pattern)
1. The user describes what they want to achieve in natural language.
2. The Coordinator interprets the request, segments it into specific tasks, and asks for approval on token-expensive actions.
3. Under the hood, the Coordinator delegates tasks to specialized subagents (e.g. Researcher, Contextualizer, Scribe, Publisher, Git Worker, Archiver) using the task tool.
4. The subagents interact with the user as needed to gather specific information, draft content, copy files, or commit changes.

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
