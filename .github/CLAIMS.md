# Keep the art queue moving

Use **`claimed`** on the individual issue being worked. A unique worker ID
and token in an append-only issue comment distinguish agents that share
the same GitHub account. Assignees alone cannot do that.

The comment log decides ownership; the label is its visible queue index.
The helper verifies the first accepted request before allowing work. A
losing concurrent request is discarded, not queued for later. This is a
cooperative protocol, not an atomic GitHub lock or a security boundary.
All workers must use it; raw label edits are not sufficient.

## Pick, claim, work, ship

From the repository root, with authenticated `gh`:

```sh
python3 work/issue_claim.py ready --limit 20
python3 work/issue_claim.py claim 1126 --owner t3/YOUR-UNIQUE-THREAD-ID --branch plate/keel-billed-toucan
```

1. Pick one **leaf issue**, not an entire wave. Check current art,
   open/closed issues and existing PRs first. An unlabeled issue is only a
   candidate: old workers may already be drawing it without this protocol.
2. Start only after `claim` exits successfully and returns your active
   owner/token. Keep that token for this task. If denied or uncertain,
   inspect `status`, then pick a different task rather than waiting or
   starting a second copy. Never clear someone else's claim to obtain work.
3. One active drawing task per worker. Draw, export all deliverables,
   inspect proofs and add a task-local critique. Do not edit shared prompt
   rosters or rebuild the master bank.
4. Heartbeat at meaningful milestones, roughly hourly for long work.
   There is no heartbeat polling loop or need for minute-by-minute comments.
5. Keep the claim through PR review. Use `Closes #1126` in the PR. Renew
   with the PR URL in the note when handing the PR to review.
6. Merge/issue closure removes the visible claim label via the cleanup
   workflow once that workflow is on the default branch. Do not release
   merely because a PR was opened: that would offer unfinished work again.
7. On abandonment, blockage or explicit handoff, preserve partial work,
   stop editing, then release with a useful note. A new worker claims
   separately; do not pass an ambiguous shared token around.

```sh
python3 work/issue_claim.py status 1126
python3 work/issue_claim.py heartbeat 1126 --token YOUR-TOKEN --note "Proof checked; PR https://github.com/drawmeanelephant/f-artcraft/pull/123 awaits review."
python3 work/issue_claim.py release 1126 --token YOUR-TOKEN --note "Handed back. Partial native/driver are on plate/keel-billed-toucan; missing PDF proof. No open PR."
```

Release changes only `claimed`, not other labels, assignees, issue text,
branches or artwork. A stale token cannot remove a replacement worker's
claim. Never edit/delete the machine-readable claim comments; they are the
ownership history. After a network error, run `status` before retrying:
the write may already have succeeded.

## Quiet or stuck workers

```sh
python3 work/issue_claim.py stale
```

Six hours without a heartbeat is **a review flag, not automatic expiry**.
An active PR or long proof run is not abandoned work. Pick other ready
tasks while an operator checks stale claims. For an authorized recovery:

- Confirm the old worker stopped, inspect its branch/worktree and open PRs.
- Preserve and explain any partial work.
- Release using the recorded token and an explicit recovery note, then
  acquire a fresh claim. Never take over solely because time passed.

A bare `claimed` label without a trusted log record is treated as a manual
reservation, not automatically erased. Public comments from non-collaborators
cannot acquire/release claims through this helper. Reopened issues do not
inherit claims from before their last closure.

## Rollout while other agents are busy

- Do not bulk-claim the backlog, infer ownership from issue age, or clear
  existing workers' reservations.
- Existing workers adopt their own issue at their next safe checkpoint.
  New workers use the protocol before starting.
- The label can exist immediately. The helper, instructions, issue form
  and close-cleanup workflow need to reach main before other checkouts and
  GitHub automatically use them.
- No new scheduler, central queue file, mandatory prompt rebuild, or
  drawing-quality gate is added. If a task is busy or blocked, take another.
