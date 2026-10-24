# <Series>: <subject>

Status: draft, not posted.

## Concept

<One visual idea, pose, palette and the specific thing the drawing must show.>

## Composition and lettering

<Canvas, frame/disc, margins, title, second line and any justified exceptions.>

Use gradients and translucent shading, warm dark ink, Virelai Sans lettering
and Virelai Mascots ornaments where appropriate. Inspect the actual proof,
not only the drawing commands.

## Files

- Subject: `art/<category>/<slug>/`
- Revision: `<slug>-V1R00`, only if this is genuinely a new piece.
- Commit: `.vectorcraft`, `.svg`, `@2x.png` and the revision-specific driver
  `work/<category>/<slug>-V1R00.py`.
- Local proof: `work/out/<slug>-V1R00.pdf`, not committed.

For existing work, start from the newest revision and follow `AGENTS.md`;
never overwrite earlier files.

## Acceptance

- [ ] Check current artwork and open/closed issues for duplicates.
- [ ] Check open PRs and claim this leaf issue with
      `python3 work/issue_claim.py claim ISSUE --owner UNIQUE-WORKER-ID`.
      Start only after ownership is confirmed; see `.github/CLAIMS.md`.
- [ ] Draw in VectorCraft through its MCP server.
- [ ] Inspect the PDF/PNG proof for clipping, overset, rim leaks and legibility.
- [ ] Check series-specific anatomy, material and thin-geometry constraints.
- [ ] Save all deliverables and a written task-local analysis in
      `prompts/inbox/<date>-<slug>-review.md`.
- [ ] Do not edit `PROMPTS.md`, common rules or shared rosters on this art task.
- [ ] Keep the claim through PR review; close on merge, or stop and release
      with a note pointing to preserved partial work.
