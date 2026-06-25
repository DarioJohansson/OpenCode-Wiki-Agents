# check-links.py — Wiki Link Checker

Scans all `.md` files under `wiki/` for broken internal markdown links.

## Usage

```powershell
# From repo root
python helper-scripts/check-links.py

# From anywhere (script auto-resolves wiki/ path)
python C:\path\to\helper-scripts\check-links.py
```

## What It Checks

Finds links in `[text](path)` format and verifies the target file exists. It appends `.md` automatically if omitted (the wiki convention). **Skips** external URLs (`http://`, `https://`), anchors (`#`), email links (`mailto:`), and image references (`![alt](src)`).

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | `[OK] All links are valid — no broken links found.` |
| `1` | Broken links found — each printed as `file:line  [text](link)` |

## Known Limitation

Does **not** validate external URLs — it only checks local file references.
