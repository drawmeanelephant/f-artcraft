# Agent rules — f-artcraft

Vector art drawn in VectorCraft over its MCP server. The editable loop, prompt
bank and house style live in [prompts/](prompts/README.md); [PROMPTS.md](PROMPTS.md)
is a periodically compiled reading copy. Read the core rules, relevant
series/theme and pending `prompts/inbox/` notes before starting a piece.
Baseline critique lives in `ANALYSIS-ROUND-*.md`.

## Issue claims and throughput

Before starting a leaf art issue, check existing art/issues/open PRs, then
run `python3 work/issue_claim.py claim ISSUE --owner UNIQUE-WORKER-ID`.
Use a unique thread/task identity, not the shared GitHub username. Start
only after the helper confirms your token. `claimed` is the visible label;
the issue's append-only claim log decides ownership. If busy or uncertain,
pick another issue, not a duplicate drawing. One active art task per worker.

Keep the claim through proofing and PR review. Heartbeat at milestones
(roughly hourly on long tasks). Use `Closes #ISSUE` in the PR. On handoff,
blockage or abandonment, stop editing, preserve partial work, and release
with the token and a useful note. Never clear another worker's claim
without an authorized recovery. Six-hour stale flags are not permission
to steal a task. See [.github/CLAIMS.md](.github/CLAIMS.md) for commands,
close-cleanup and safe adoption by already-running workers.

## Task types and model routing

Use one `type:*` label for the deliverable and one explicit `work:*`
intent when the leaf brief is clear. Preserve `claimed` and existing
metadata; never infer work intent from a filename or overwrite another
worker's labels. Mixed or uncertain work stays unclassified until reviewed.
See [.github/LABELS.md](.github/LABELS.md) for the vocabulary and optional
`ready`/`claim` filters.

Route models by demonstrated task-family strengths, not price labels.
Variations require an approved base, bounded changes and proof inspection;
native-file editability is not evidence of visual quality. Model trials
are budgeted and capped, with independent review and escalation rather
than endless retries. See [.github/MODEL-ROUTING.md](.github/MODEL-ROUTING.md).
Do not launch paid comparisons or claim a model is qualified without
approved budget and observed results.

## Prompt contributions (merge-friendly)

Art tasks add one uniquely named `prompts/inbox/<date>-<subject>-<topic>.md`
for their critique, lesson or proposed prompt, using `prompts/templates/note.md`.
New theme lists go in separate `prompts/themes/` files; issue-ready drafts go
in separate `prompts/issues/` files. Check current artwork and open/closed
issues for duplicates first. Do not edit shared rosters, common rules or
`PROMPTS.md` just to report an art task.

Only a consolidation task folds verified notes into the shared sources and
rebuilds `PROMPTS.md`; follow [prompts/CONSOLIDATE.md](prompts/CONSOLIDATE.md).
Pending proposals do not override house rules. Snapshot freshness is not
required on art branches.

## Revision rule (mandatory)

**Never overwrite an existing piece.** Every piece is versioned
`<slug>-V<V>R<RR>` — e.g. `ember-dusk-V1R01`. `V` is the interpretation
(the original artist's take is `V1`, another artist's riff is `V2`), `R`
is the revision inside it, counting from `00`. When improving a drawing:

- Start from the newest revision of the piece.
- Save the improved result as the next revision: bump `R` (`V1R01` → `V1R02`)
  for refinements of the same design; bump `V` and reset `R` (`V1R02` → `V2R00`)
  for a redesign or new direction.
- The suffix applies to every output of that revision: `.vectorcraft`, `.svg`,
  `.pdf`, `@2x.png`, and the driving script where it is revision-specific.
- First pass of a brand-new piece starts at `V1R00`. Work received from
  elsewhere is registered as `V1R00` (or consecutive `R`s when the dump
  itself holds revisions, e.g. `bunny-avatar` → `V1R00`/`V1R01`).
- Previous revision files are read-only. If a revision is bad, the next
  revision fixes it — nothing is edited in place or deleted.

## Driving VectorCraft

`vectorcraft-cli mcp` runs the MCP server on stdio (newline-delimited
JSON-RPC). `work/mcp_client.py` is the shared client; `work/vc.py` the shared
drawing helper.

- Connected mode: launch the app with `vectorcraft --control 7979`, then the
  MCP attaches to the live window (`ui_screenshot`, `pointer_gesture`, …).
- Headless mode: pass `--automation-read-root DIR` and
  `--automation-write-root DIR` — without a write root, no file can be saved.
- Draw with `draw_shape` / `draw_path`, paint with `set_paint`, check with
  `render_preview`, batch atomic edits with `command_batch`. Coordinates are
  points, y down, origin at the first artboard's top-left.

## Deliverables

Per `prompts/core/00-art-loop.md`: every revision ships `.vectorcraft` + `.svg` + `.pdf` +
`@2x.png`. Committed to git: the `.vectorcraft` native (JSON — SVG is not
an editable format), the `.svg`, the `@2x.png` and the driving script.
PDF proofs and scratch renders in `work/out/` stay local.

## The site

`docs/` generated output (data JSONs, site HTML, media copies) is a
build artifact — never committed. The deploy job rebuilds on latest
main, so nothing needs regen-by-hand: new pieces and new
`art/<category>/` dirs are discovered automatically (unknown
categories land on the plates page). The `docs-build` check only
verifies the scan + render still runs clean:

    python3 docs/gen_data.py   # scans art/ -> docs/data/*.json + docs/site/media/
    DOGBED=<dogbed binary> sh docs/build.sh   # -> docs/site/*.html
