import os
import re
import sys
from urllib.parse import urlparse

WIKI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki")
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
ANCHOR_OR_SCHEME = re.compile(r"^(#|mailto:|https?://|ftp://)")


def resolve_target(link: str, source_dir: str) -> str | None:
    parsed = urlparse(link)
    path = parsed.path or link
    anchor = parsed.fragment

    if not path:
        return None

    resolved = os.path.normpath(os.path.join(source_dir, path))
    if os.path.isfile(resolved):
        return resolved

    if not resolved.endswith(".md"):
        candidate = resolved + ".md"
        if os.path.isfile(candidate):
            return candidate

    for ext in ["", ".md"]:
        candidate = resolved + ext
        if os.path.isfile(candidate):
            return candidate

    return None


def check_file(filepath: str) -> list[dict]:
    rel_path = os.path.relpath(filepath, WIKI_DIR)
    source_dir = os.path.dirname(filepath)
    issues = []

    with open(filepath, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            for match in LINK_RE.finditer(line):
                text, raw_link = match.groups()
                link = raw_link.strip()

                if ANCHOR_OR_SCHEME.match(link):
                    continue

                target = resolve_target(link, source_dir)
                if target is None:
                    issues.append({
                        "file": rel_path,
                        "line": lineno,
                        "link": link,
                        "text": text.strip(),
                    })

    return issues


def main():
    if not os.path.isdir(WIKI_DIR):
        print(f"Error: wiki directory not found at {WIKI_DIR}")
        sys.exit(1)

    all_issues = []
    md_files = []
    for root, _, files in os.walk(WIKI_DIR):
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(root, f))

    for f in md_files:
        all_issues.extend(check_file(f))

    if not all_issues:
        print("[OK] All links are valid \u2014 no broken links found.")
        sys.exit(0)

    print(f"[FAIL] Found {len(all_issues)} broken link(s):\n")
    for issue in all_issues:
        print(f"  {issue['file']}:{issue['line']}  [{issue['text']}]({issue['link']})")

    sys.exit(1)


if __name__ == "__main__":
    main()
