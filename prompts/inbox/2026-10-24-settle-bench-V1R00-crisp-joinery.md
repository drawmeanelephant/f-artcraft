## Settle bench V1R00 — crisp quads for joinery; Catmull-Rom is for cushions

- Kind: lesson
- Source: #1188, `work/furniture/draw_settle_bench.py`, `art/furniture/settle-bench/settle-bench-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates; case goods, paneled work, architecture
- Status: pending

### Evidence

First pass ran every face through `smooth()` (Catmull-Rom): the top rail
became a loaf, fielded panels became blobs, the whole settle read as
bread. Joinery wants `M L L L Z` — a straight polygon `quad()` with a
miter join. Same split as the upholstery lesson going the other way:
soft goods get bowed edge midpoints, case goods get crisp corners.

Fielded panels read with three strokes: a darker inset quad, a light
bevel line on its top edge, a shade line on its bottom. Stiles are just
3pt strokes. The settle's width fights the disc — bottom outer corners
of the wings are the extent culprits, not the top rail; budget the
footprint first (`farthest point` print caught it).

The hearth glow does the "tavern corner": a warm radial wash drawn under
the piece, plus 3pt rim-light strokes up the wall's right edge and the
wing's front edge.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Case goods
and joinery draw as straight `M…Z` polygons — Catmull-Rom smoothing
belongs to upholstery. Fielded panel = inset quad + light top bevel +
dark bottom bevel." A proposal does not override current house rules.
