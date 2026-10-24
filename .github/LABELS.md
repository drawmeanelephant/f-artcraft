# Task labels, not model rankings

Three independent questions:

- **Who owns it?** `claimed` plus its verified worker/token comment. Never
  remove a claim as part of classification.
- **What gets delivered?** One `type:*` label.
- **What kind of work is requested?** One explicit `work:*` label on a leaf
  task once the brief is clear. Do not infer intent from “V1R00.”

## Type

| Label | Deliverable |
| --- | --- |
| `type:illustration` | Plates, animals, furniture, mascots, wallpaper, brand or spot art |
| `type:icons` | Icon/cursor family, with size and consistency constraints |
| `type:ui` | Interface component, screen, layout or interaction |
| `type:design-system` | Shared tokens, styles, component library or design contract |
| `type:motion` | Animation or sprite sequence |
| `type:workflow` | Tooling, documentation or production process |
| `type:tracking` | Index/umbrella, not an independently claimable task |

## Work intent

| Label | Brief must identify |
| --- | --- |
| `work:original` | The new design/composition and its acceptance bar |
| `work:variation` | Approved base revision, permitted changes and invariants |
| `work:refinement` | Newest native of the same design and concrete defects to fix |
| `work:review` | A standalone critique/proof task and evidence to inspect |

These are not lifecycle states: opening a PR does not turn an original
task into `work:review`. They are not difficulty scores or promises that
any particular model can do the work.

A mixed deliverable may contain both a fidelity pass and new scenes.
Do not silently choose one intent, split active work, or add several
conflicting labels. Leave it unclassified until its owner/maintainer
chooses a dominant intent or independently landable scopes.

## Creating, finding and claiming

Set type and intent when filing an issue, using `gh issue create --label`
or GitHub's labels sidebar. The art-plate form defaults only its type;
its intent field is not automatic label assignment.

```sh
gh issue edit 1126 --repo drawmeanelephant/f-artcraft --add-label type:illustration --add-label work:original
python3 work/issue_claim.py ready --type illustration --work variation --limit 20
python3 work/issue_claim.py claim 1126 --owner t3/YOUR-THREAD-ID --type illustration --work original
```

Claim-time flags are optional for already-running workers. They add only
missing explicit metadata, reject an existing conflicting family, and do
not replace labels or assignees. Correct misclassification deliberately
after reading the brief, not with a bulk replacement.

The additive metadata operation is separate from ownership. If adding
metadata fails after a claim was acquired, inspect `status` before
retrying or handing back. The reservation may already exist.

## Conservative backfill

```sh
python3 work/task_labels.py catalogue
python3 work/task_labels.py plan
```

Both commands are read-only. The plan recognizes established title
conventions, preserves any existing `type:*` label, and lists unfamiliar
titles for review. It never assigns work intent, changes issue text,
posts comments, claims issues or removes labels. Applying a reviewed plan
is a separate, additive operation. Re-read current metadata first.

No `cheap`, `easy` or model-name labels. Route from demonstrated
task-family strengths using the [model trial guidance](MODEL-ROUTING.md),
then narrow the candidate queue by type/intent. No model is qualified yet
just because these labels exist.
