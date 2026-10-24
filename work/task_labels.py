#!/usr/bin/env python3
"""Print the label catalogue or a conservative type-only backfill plan.

Read-only: no labels, issue bodies, claims or comments are changed here.
Work intent is deliberately never inferred from a title or filename.
"""
import argparse
import json
import re
import sys

from issue_claim import ClaimError, REPO, TASK_TYPES, WORK_KINDS, gh, label_names


def catalogue():
    return [
        {"name": prefix + name, "description": description, "color": color}
        for prefix, choices, color in (
            ("type:", TASK_TYPES, "1D76DB"), ("work:", WORK_KINDS, "7057FF"))
        for name, description in choices.items()
    ]


def infer_type(title):
    title = title.casefold().strip()
    if re.search(r"field plates,\s*wave", title):
        return "tracking"
    if re.match(r"^(animal|furniture|insect|watercraft)\s*[—–-]\s*field plate:", title):
        return "illustration"
    if re.match(
        r"^(field plate|holiday seal|mascot portrait|poetry graphic|haiku graphic|"
        r"limerick graphic|aphorism graphic|commemorative plate|necropolis plate|"
        r"lorelog graphic|site equity):", title,
    ):
        return "illustration"
    if title.startswith("virelaios — "):
        if title.startswith("virelaios — figcraft sheet: design tokens + primitives"):
            return "design-system"
        if title.startswith("virelaios — figcraft sheet:"):
            return "ui"
        if re.match(r"^virelaios — (app-icon set|file-type icon family|cursor set)\b", title):
            return "icons"
        if title.startswith("virelaios — spinner sprite"):
            return "motion"
        if re.match(r"^virelaios — (brand plate|empty-state spot art|wallpaper set|sexiburger mascot pose set)\b", title):
            return "illustration"
    return None


def backfill_plan(issues):
    result = {"add": [], "preserved": [], "unclassified": []}
    for issue in issues:
        existing = sorted(label for label in label_names(issue) if label.startswith("type:"))
        if existing:
            result["preserved"].append({"number": issue["number"], "labels": existing})
            continue
        kind = infer_type(issue["title"])
        if kind:
            result["add"].append({
                "number": issue["number"], "title": issue["title"], "label": "type:" + kind,
            })
        else:
            result["unclassified"].append({"number": issue["number"], "title": issue["title"]})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("catalogue", "plan"))
    parser.add_argument("--repo", default=REPO)
    args = parser.parse_args()
    try:
        if args.command == "catalogue":
            result = catalogue()
        else:
            issues = gh("issue", "list", "--repo", args.repo, "--state", "open",
                        "--limit", "1000", "--json", "number,title,labels")
            if len(issues) >= 1000:
                raise ClaimError("Scan limit reached; do not apply an incomplete backfill")
            result = backfill_plan(issues)
        print(json.dumps(result, indent=2))
    except (ClaimError, OSError, ValueError) as error:
        print(f"Label plan error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
