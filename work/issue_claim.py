#!/usr/bin/env python3
"""Cooperative issue claims for art workers. Requires authenticated gh; stdlib only.

The append-only comment log decides ownership; `claimed` is its visible index.
No polling, automatic expiry, bulk claiming, or edits to shared queue files.
"""
import argparse
import json
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "drawmeanelephant/f-artcraft"
LABEL = "claimed"
STALE_HOURS = 6
MARKER = re.compile(r"<!-- f-artcraft-claim-v1 (\{[^\n]*\}) -->")
TOKEN = re.compile(r"[0-9a-f]{32}")
OWNER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{0,119}")
TRUSTED = {"OWNER", "MEMBER", "COLLABORATOR"}


class ClaimError(Exception):
    pass


def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def active_claim(comments, closed_at=None):
    """First accepted request wins. Losing requests never become queued claims.

    Comment IDs order concurrent requests, including when timestamps tie.
    Closing an issue ends its old claim, even if the issue is later reopened.
    Public drive-by comments cannot acquire or release a worker's reservation.
    """
    current = None
    for comment in sorted(comments, key=lambda item: item["id"]):
        if comment.get("author_association") not in TRUSTED:
            continue
        matches = MARKER.findall(comment.get("body") or "")
        if len(matches) != 1:
            continue
        try:
            event = json.loads(matches[0])
            created = timestamp(comment["created_at"])
            if closed_at and created <= timestamp(closed_at):
                continue
            if not TOKEN.fullmatch(event.get("token", "")):
                continue
            action = event.get("action")
            if action == "claim" and current is None:
                if not OWNER.fullmatch(event.get("owner", "")):
                    continue
                current = {
                    "token": event["token"], "owner": event["owner"],
                    "branch": event.get("branch", ""),
                    "started_at": comment["created_at"],
                    "heartbeat_at": comment["created_at"],
                    "url": comment.get("html_url", ""),
                }
            elif current and event["token"] == current["token"]:
                if action == "release":
                    current = None
                elif action == "heartbeat":
                    current["heartbeat_at"] = comment["created_at"]
        except (KeyError, TypeError, ValueError):
            continue
    return current


def gh(*args):
    result = subprocess.run(["gh", *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise ClaimError(result.stderr.strip() or result.stdout.strip() or "gh failed")
    return json.loads(result.stdout) if result.stdout.strip() else None


class GitHub:
    def __init__(self, repo):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            raise ClaimError("Repository must be owner/name")
        self.repo = repo

    def pages(self, path):
        pages = gh("api", "--paginate", "--slurp", path + "?per_page=100")
        return [item for page in pages for item in page]

    def snapshot(self, number):
        path = f"repos/{self.repo}/issues/{number}"
        issue = gh("api", path)
        if "pull_request" in issue:
            raise ClaimError("Claim a leaf issue, not a pull request")
        comments = self.pages(path + "/comments")
        closed = [event["created_at"] for event in self.pages(path + "/events")
                  if event.get("event") == "closed"]
        claim = active_claim(comments, max(closed) if closed else None)
        return issue, claim

    def append(self, number, event, note=""):
        owner = event.get("owner", event["token"])
        body = f"Art worker {event['action']}: `{owner}`."
        if event.get("branch"):
            body += f"\n\nBranch: `{event['branch']}`."
        if note:
            body += "\n\n" + note
        body += "\n\n<!-- f-artcraft-claim-v1 " + json.dumps(event, sort_keys=True) + " -->"
        gh("api", f"repos/{self.repo}/issues/{number}/comments", "-f", "body=" + body)

    def label(self, number, present):
        # Modify only our label, never replace unrelated labels or assignees.
        args = ["issue", "edit", str(number), "--repo", self.repo,
                "--add-label" if present else "--remove-label", LABEL]
        result = subprocess.run(["gh", *args], cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            raise ClaimError(result.stderr.strip() or "Could not reconcile claimed label")


def has_label(issue):
    return any(label["name"] == LABEL for label in issue.get("labels", []))


def sync_label(api, number):
    """Re-read after changing the label so a late release can't clear a new claim."""
    for _ in range(3):
        issue, claim = api.snapshot(number)
        wanted = issue["state"].lower() == "open" and claim is not None
        if has_label(issue) != wanted:
            api.label(number, wanted)
        confirmed, latest = api.snapshot(number)
        wanted = confirmed["state"].lower() == "open" and latest is not None
        if has_label(confirmed) == wanted:
            return confirmed, latest
    raise ClaimError("Ownership changed during label sync. Run status before doing any work.")


def status(api, number, now=None):
    issue, claim = api.snapshot(number)
    now = now or datetime.now(timezone.utc)
    is_open = issue["state"].lower() == "open"
    result = {"issue": number, "state": issue["state"], "url": issue["html_url"],
              "claimed_label": has_label(issue), "claim": claim,
              "manual_claim": is_open and has_label(issue) and claim is None}
    result["stale"] = bool(is_open and claim and
                           (now - timestamp(claim["heartbeat_at"])).total_seconds()
                           >= STALE_HOURS * 3600)
    return result


def claim_issue(api, number, owner, branch=""):
    if not OWNER.fullmatch(owner):
        raise ClaimError("Use a unique worker/thread ID: letters, digits, . _ : / -")
    if any(char in branch for char in "\n\r`"):
        raise ClaimError("Branch must be a single line without backticks")
    issue, current = api.snapshot(number)
    if issue["state"].lower() != "open":
        raise ClaimError("Issue is closed; pick another task")
    if current:
        raise ClaimError(f"Already claimed by {current['owner']}; pick another task")
    if has_label(issue):
        raise ClaimError("Manual/legacy claimed label present; do not steal it")
    if issue.get("assignees"):
        raise ClaimError("Issue already has an assignee; check with its owner")
    if re.search(r"field plates,\s*wave", issue["title"], re.I):
        raise ClaimError("Claim an individual art task, not a wave/tracking issue")
    token = uuid.uuid4().hex
    api.append(number, {"action": "claim", "owner": owner, "token": token, "branch": branch})
    _, winner = api.snapshot(number)
    if not winner or winner["token"] != token:
        # Our request remains evidence, not a future reservation.
        if winner:
            sync_label(api, number)
        raise ClaimError("Claim not confirmed or another worker won. Run status; do not start.")
    _, winner = sync_label(api, number)
    if not winner or winner["token"] != token:
        raise ClaimError("Claim changed before confirmation; do not start")
    result = status(api, number)
    if (result["state"].lower() != "open" or not result["claimed_label"]
            or not result["claim"] or result["claim"]["token"] != token):
        raise ClaimError("Claim changed before confirmation; do not start")
    return result


def update_claim(api, number, token, action, note=""):
    if not TOKEN.fullmatch(token):
        raise ClaimError("Use the token returned by claim/status")
    if action not in {"heartbeat", "release"}:
        raise ClaimError("Invalid claim action")
    _, current = api.snapshot(number)
    if not current or current["token"] != token:
        raise ClaimError("Token does not own this issue; no labels were changed")
    api.append(number, {"action": action, "token": token}, note)
    sync_label(api, number)
    result = status(api, number)
    if action == "heartbeat" and (
            result["state"].lower() != "open" or not result["claim"]
            or result["claim"]["token"] != token):
        raise ClaimError("Claim changed during heartbeat; stop and run status")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=REPO)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("status", "claim", "heartbeat", "release"):
        command = commands.add_parser(name)
        command.add_argument("issue", type=int)
        if name == "claim":
            command.add_argument("--owner", required=True, help="Unique worker/thread ID")
            command.add_argument("--branch", default="")
        elif name in {"heartbeat", "release"}:
            command.add_argument("--token", required=True)
            command.add_argument("--note", required=name == "release", default="")
    ready = commands.add_parser("ready")
    ready.add_argument("--limit", type=int, default=20)
    commands.add_parser("stale")
    args = parser.parse_args()
    try:
        api = GitHub(args.repo)
        if args.command in {"ready", "stale"}:
            if args.command == "ready" and not 1 <= args.limit <= 1000:
                raise ClaimError("--limit must be between 1 and 1000")
            issues = gh("issue", "list", "--repo", args.repo, "--state", "open",
                        "--limit", str(args.limit if args.command == "ready" else 1000),
                        "--search", "-label:claimed" if args.command == "ready" else "label:claimed",
                        "--json", "number,title,url,assignees")
            if args.command == "ready":
                # Candidate list only. claim always checks authoritative ownership again.
                result = [issue for issue in issues if not issue["assignees"]
                          and not re.search(r"field plates,\s*wave", issue["title"], re.I)]
            else:
                result = []
                for issue in issues:
                    item = status(api, issue["number"])
                    if item["stale"] or item["manual_claim"]:
                        result.append(item)
        elif args.issue < 1:
            raise ClaimError("Issue number must be positive")
        elif args.command == "claim":
            result = claim_issue(api, args.issue, args.owner, args.branch)
        elif args.command == "status":
            result = status(api, args.issue)
        else:
            if args.command == "release" and not args.note.strip():
                raise ClaimError("Explain completion, handoff or preserved partial work in --note")
            result = update_claim(api, args.issue, args.token, args.command, args.note)
        print(json.dumps(result, indent=2))
    except (ClaimError, OSError, ValueError) as error:
        print(f"Claim error: {error}\nDo not start work on an unconfirmed claim.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
