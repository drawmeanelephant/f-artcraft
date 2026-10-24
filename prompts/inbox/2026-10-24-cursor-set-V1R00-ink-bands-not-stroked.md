## cursor set V1R00 — mask-safe shapes are *filled* silhouettes, not stroked ones

- Kind: lesson / analysis
- Source: #1249 · `work/virelai/cursors.py` + `draw_cursor_*.py` ·
  `art/virelai/cursor-*/` · `art/virelai/HOTSPOTS.md`
- Applies to: virelai chrome-register assets (cursors, later icon/spot
  work that must survive 2-color mask or 16 px reads)
- Status: pending

### Evidence

Ten cursors (arrow refresh + 9 context shapes) shipped at the 32×48
master, proofed down to 16×24 on split navy/light fields and through a
coverage+ink mask simulation (`work/tools/proof_size.py`).

What worked: composing hand/grab/grabbing from overlapping white-filled,
ink-stroked primitives — the stroke seams survive the mask as finger
creases, which is exactly what a glove hand wants at 16 px. A single
closed path per cursor was only needed for the truly iconic silhouettes
(arrow, ibeam, double arrows, hourglass). The hourglass's amber sand is
the one color accent in the set and reads on both fields.

What failed and got fixed in-R00: the first `not-allowed` drew the slash
as a *white band with an ink stroke* across a stroked ring — at 16 px
the two stroke edges + ring edge striped into hatching, reading as a
grater, not a prohibition sign. The fix is the mask-first rule: build
the mark from solid ink masses (ink donut + solid ink bar tucked into
the ring), let white be *interior* paper, and give the outer edge a thin
white halo so the shape survives dark chrome. Stroked details subdivide
the silhouette; filled masses merge with it.

Also learned: `draw_path` accepts `join="round"` (verified, no warning) —
rounded joins on closed cursor paths are what keep the cartoon weight
the issue asks for.

### Proposed change

Add to `virelai/notes/style-bible.md` under Geometry and strokes:
*chrome-register marks are built from filled masses, never stroked
bands — a stroke's two edges stripe at mask size. If a band must read as
one mark, fill it with ink and tuck its ends into the enclosing
silhouette.* Destination: style bible next consolidation.
