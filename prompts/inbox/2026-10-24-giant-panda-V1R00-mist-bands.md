# Giant panda V1R00 — mist as wide soft strokes, canes end inside the rim

- Kind: lesson
- Source: issue #1066, `work/animals/draw_giant_panda.py`,
  `art/animals/giant-panda/giant-panda-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — atmospheric decor
- Status: pending

### Evidence

Mist on a mountain plate works as 4 fat stroked cubic ribbons
(`strokeWidth` 70–110, opacity 14–20, round caps) rather than filled
ellipses: the stroke edge feathers where a filled shape would silhouette.
Ordering matters — mist goes down before the subject and before the bamboo
so the canes read *in* the weather, not under it.

The near-miss: flanking bamboo canes drafted to y770–780 at x≈196/806 leak
past the rim — at that depth the disc is only ~283pt half-wide. Vertical
decor near the rim needs its endpoints computed on the disc, not guessed;
ending the canes ~y740 kept everything inside. The panda's black shoulder
cape uses the bust-closes-on-arc pattern from the wild dog plate (same
issue wave): intercepts at y796, `A420,420` bottom.

### Proposed change

Field-plate trap list, second bullet family: *vertical decor (canes,
trunks, stems) near the disc edge needs endpoints solved on the disc —
`x = CX ± sqrt(R² − (y−CY)²)` — the floor arc does not rescue a stalk that
exits the rim sideways.* Destination: `prompts/series/20-field-plates.md`.
