## VirelaiOS virelai/ area — layout and naming conventions

- Kind: rule proposal
- Source: issue #1261; `virelai/README.md`, `virelai/notes/style-bible.md`,
  `virelai/design/README.md`, `art/virelai/README.md`, `work/virelai/vkit.py`
- Applies to: the virelai series — #1248–#1251, #1253–#1255, #1257 (assets),
  #1262–#1264 (figcraft sheets)
- Status: pending

### Evidence

Setting up the area surfaced three pipeline facts the conventions are built
on. `docs/gen_data.py`'s `collect_versioned` reads exactly two levels —
`art/<series>/<slug>/<slug>-V*R*` — so the downstream issues' proposed
`art/virelaios/<family>/<slug>/` nesting would be invisible to the site; the
family moves into the slug prefix (`icon-gofiles`) and the series is `virelai`.
Natives under `virelai/design/` needed `.gitignore` exceptions
(`*.vectorcraft`/`*.designcraft`/`*.figcraft` are repo-wide ignored outside
`art/` and `test/`). The OS-side fixtures give real colors: WALLPAPER.QOI's
field is `#1E1E2E` (93% of pixels), the mascot's body is `#FDB845` family and
its warm-dark outline is `#634B48`–`#7B5E5A` — never pure black, matching the
house ink habit.

### Proposed change

The conventions land as the committed docs above (destination `virelai/` +
`art/virelai/` + `work/virelai/`): flat `<family>-<slug>` naming, transparent
backgrounds for chrome-painted assets, the read-at-size proof gate, 8.3 names
recorded as adoption-side notes, per-wave contact sheets as their own
`sheet-*` pieces, and Virelai Sans's missing digits covered by Source Sans 3.
The style bible seeds from the shipped tokens and sampled fixtures; each wave
should append what it learns (stroke survival at 16 px, mono-mask reductions)
to `virelai/notes/`, not to shared rosters.
