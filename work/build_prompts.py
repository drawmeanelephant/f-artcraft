#!/usr/bin/env python3
"""Compile the prompt workshop into a periodic reading copy. Stdlib only.

Default: stdout. Only a consolidation task should use --output PROMPTS.md.
Snapshot freshness is deliberately not a per-art-branch requirement.
"""
import argparse
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
GROUPS = ("core", "banks", "series", "analysis", "themes", "inbox")
LINK = re.compile(r"(!?\[[^\]\n]*\]\()([^\s)]+)(\))")


def rebase_links(body, parent):
    """Rebase simple inline Markdown links from a fragment to the repo root."""
    def replace(match):
        prefix, target, suffix = match.groups()
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
            return match.group(0)
        path = posixpath.normpath((parent / url.path).as_posix())
        return prefix + urlunsplit(("", "", path, url.query, url.fragment)) + suffix

    return LINK.sub(replace, body)


def build(root=ROOT):
    source = root / "prompts"
    chunks = [
        "# Art Loop — Prompts & Rounds",
        "<!-- Built by work/build_prompts.py. Edit prompts/, not this snapshot. -->\n\n"
        "This is a periodically compiled reading copy. The editable sources and\n"
        "newer pending notes live in [prompts/](prompts/README.md). Art branches\n"
        "do not rebuild this file; see the [consolidation brief](prompts/CONSOLIDATE.md).",
    ]
    for group in GROUPS:
        files = sorted((source / group).rglob("*.md"))
        if group in ("core", "banks", "series", "analysis") and not files:
            raise ValueError(f"Missing prompt sources: prompts/{group}/")
        if group == "inbox" and files:
            chunks.append(
                "## Pending task notes\n\n"
                "These are unconsolidated evidence and proposals, not adopted rules."
            )
        for path in files:
            body = path.read_text(encoding="utf-8").strip()
            if body.startswith("# "):
                body = "#" + body
            if not body.startswith("## "):
                raise ValueError(f"{path.relative_to(root)} must start with a ## heading")
            relative = path.relative_to(root)
            body = rebase_links(body, relative.parent)
            chunks.append(f"<!-- Source: {relative.as_posix()} -->\n\n{body}")
    return "\n\n---\n\n".join(chunks) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a reading copy instead of stdout")
    args = parser.parse_args()
    try:
        result = build()
    except ValueError as error:
        parser.error(str(error))
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
