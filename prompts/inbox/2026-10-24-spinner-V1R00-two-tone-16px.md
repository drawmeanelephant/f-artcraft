## spinner set V1R00 — two-tone comet wins the 16 px gate

- Kind: lesson
- Source: #1255 · `work/virelai/spinner.py` (frame machinery) ·
  `work/virelai/draw_spinner_{arc,mascot}.py` ·
  `art/virelai/spinner-{arc,mascot}/…-V1R00.*`
- Applies to: virelai motion assets, anything that must read at 16 px on
  both surfaces
- Status: pending

### Evidence

Two frame sets shipped as the issue invited: `spinner-arc` (required) is a
comet — 280° INK tail + 55° Accent `#3B82F6` head, one 3.8 px stroke,
rounded caps, r=10.5 in a 32 px frame, rigid 30°/frame x 12. At 16 px the
blue head alone carries the spin on dark chrome (the ink tail fades to a
ghost ring, which is the point of the two-tone construction); on light
the full comet reads. `spinner-mascot` (alternative) is a mini bun disc
whose interior seeds sit on an off-center spiral; first pass swirled but
read static at 16 px — fixed by parking one seed ON the rim (r=10.2,
inked) so the silhouette wobbles as it orbits. 45°/frame x 8.

What worked: rigid rotation makes loops trivially seamless (frame N-1 →
frame 0 is just the next step of the same rotation). `spinner.py` splits
the machinery (`arc_path` = tangent-exact quadratic arcs, per-frame PNG
export at 1x+2x, Nx1 sheet doc) from each driver's `motif(d, cx, cy, f)`.
The sheet doc is the canonical `.vectorcraft` — all frames in one native,
diffable like any revision.

Gotchas: `draw_shape` takes `rotation` (degrees) on shapes — used for the
seed tilt. Silhouette change beats interior change at 16 px: interior
swirl dies but a rim bump is a per-frame difference the eye catches.

### Proposed change

Candidate rule for `virelai/notes/style-bible.md`: *at 16 px, motion must
deform the silhouette — interior detail churn is invisible; ride one
element on the outline. Two-tone = the accent carries dark chrome, the
ink tail carries light; never rely on INK alone on navy.* Open sibling
from the issue: `dots-pulse` (3-4 frame "…" for inline waits) — not
built here; `spinner.py`'s machinery already supports it.
