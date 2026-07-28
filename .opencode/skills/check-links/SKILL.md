---
name: check-links
description: >-
  Use ONLY when the user wants to check for broken markdown links in the wiki,
  or when the publisher agent auto-fixes broken links after publishing drafts.
  Scans all .md files under wiki/ and reports links pointing to non-existent
  .md pages. Do NOT use for link checking outside the wiki directory.
---

# Broken Link Checker — Wiki

Checks all markdown files under `wiki/` for `[...](...)` links that point to
markdown pages that do not exist on disk. Run from the project root.

## Usage

```bash
python3 helper-scripts/check-links.py
```

The script exits with code 0 if all links are valid, or code 1 and prints
every broken link (file, line, link text, target) otherwise.

## Auto-fix workflow

After publishing new content, run the checker. For any broken link found:

1. Identify the correct target filename under `wiki/`
2. Edit the offending file to replace the broken link target
3. Re-run the checker to confirm all links are valid