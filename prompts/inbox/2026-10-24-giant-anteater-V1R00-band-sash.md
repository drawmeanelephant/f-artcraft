## Giant anteater V1R00 — the shoulder band is a sash, not a stripe

- Kind: lesson
- Source: issue #1129; `work/animals/draw_giant_anteater.py`,
  `art/animals/giant-anteater/giant-anteater-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: animals field plates; diagonal body markings
- Status: pending

### Evidence

Proof `work/out/giant-anteater-V1R00@2x.png`. First pass drew the marking
as a narrow wedge converging to a point on the back, edged once in cream —
at plate scale it read as a single pale scratch across the neck, not the
anteater's band. Fixed by drawing a broad dark sash (~90pt between cream
borders) with the front edge from chest to mid-back and the rear edge
running parallel ~90pt behind it, each border stroked 6pt cream at 85%.
That reads as *Myrmecophaga*'s band immediately.

Knuckle-walk: a rounded pale fist plus three dark claws stroked 6pt
sweeping *back* along the ground from the fist's top front, tips landing
rearward — reads as folded foreclaws, not as fingers or a normal paw.

### Proposed change

For `prompts/series/20-field-plates.md` animal notes (or a future
anteater/marking prompt): bilateral body bands should be drawn as filled
quads between two edge strokes, not as one stroked diagonal. A single
stroke can only ever read as a line.
