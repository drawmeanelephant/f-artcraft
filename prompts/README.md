# Prompt workshop

The editable prompt bank lives here. [`PROMPTS.md`](../PROMPTS.md) is a
compiled reading copy, refreshed in occasional consolidation batches, not
on every art branch. A stale reading copy is expected; read the sources and
pending notes when starting work.

## Where things go

| Path | Purpose |
| --- | --- |
| `core/` | The art loop and house rules |
| `banks/` | The original round-robin briefs |
| `series/` | Established formats and historical rosters |
| `themes/` | New theme lists, one independent file per theme |
| `issues/` | Issue-ready drafts, one file per task, not posted automatically |
| `inbox/` | New lessons, analyses and proposed changes, one file per task/topic |
| `archive/` | Resolved inbox notes, retained as evidence |
| `templates/` | Copyable task-note and issue templates |

The builder discovers Markdown files in `core`, `banks`, `series`, `analysis`,
`themes` and `inbox`, in that order, sorted by path within each directory.
There is no shared manifest to update. Templates, issue drafts, this guide
and archived notes are not compiled.

Source fragments start with a `##` heading. Use ordinary inline Markdown
links relative to the fragment; the builder rebases them for the root-level
reading copy.

## On an art branch

1. Read the core rules, relevant series/theme and pending inbox notes.
2. Check the current `art/` tree and GitHub issues, open **and closed**, before
   proposing or claiming a subject. Historical roster prose is not inventory.
   Check open PRs too. For an existing task, acquire a confirmed per-worker
   claim before drawing; follow [the claim lifecycle](../.github/CLAIMS.md).
   Keep it through review; release with handoff notes if stopping.
3. Draw, export and inspect proofs under the revision rules in
   [AGENTS.md](../AGENTS.md). Record an in-house critique, or an appreciative
   account for guest work, in a new task-local note.
4. Copy `templates/note.md` to
   `inbox/<date>-<subject>-<topic>.md`. Include the revision, evidence and a
   concrete proposed lesson. Use a unique suffix if that path is taken.
5. Commit the note with the art. **Do not edit `PROMPTS.md`, shared rosters or
   common rules just to report one piece.** New themes and issue drafts also
   get their own files; do not append to a shared queue.

Pending notes are evidence and proposals, not new house rules. The current
core rules still apply until consolidation resolves a proposal.

## New lists and issue drafts

Start with the six independent lists in `themes/`. Each has eight candidates
and a linked starter issue in `issues/`. They are proposals, not reserved
subjects or claims that work has shipped.

An issue draft should stand on its own when copied to GitHub: include the
concept, composition, caption, exact paths and acceptance checks. Use
`templates/issue.md`. Do not invent archive IDs or poetry attributed to the
existing cast. Posting issues needs the user's go-ahead; a file here is not
a GitHub issue.

## Consolidation

Run the [consolidation brief](CONSOLIDATE.md) after roughly ten inbox notes,
at a round boundary, or whenever requested. This is a suggested manual
trigger, not an installed timer or automation.

Preview the complete bank without changing the snapshot:

```sh
python3 work/build_prompts.py
```

Only the consolidation branch refreshes the committed reading copy:

```sh
python3 work/build_prompts.py --output PROMPTS.md
```

CI validates the source and builder, not snapshot freshness. Requiring every
branch to rebuild the snapshot would recreate the merge hotspot.
