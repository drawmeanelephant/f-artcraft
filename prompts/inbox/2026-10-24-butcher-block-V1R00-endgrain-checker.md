## Butcher block island V1R00 — the end-grain top is a checkerboard, and a stuck cleaver reads instantly

- Kind: lesson
- Source: issue #1220, `work/furniture/draw_butcher_block_island.py`,
  `art/furniture/butcher-block-island/butcher-block-island-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — furniture (surfaces, props)
- Status: pending

### Evidence

The signature surface sells with cheap geometry: a 9×6 grid of projected
quads on the top plane, alternating four close maple tones with a faint
0.55pt seam stroke, reads unmistakably as end-grain butcher block at plate
scale. The tones must stay close (±10% brightness) — stronger contrast
would read as a chess board, not wood.

Props that carry the "prep" reading: a cleaver *struck into* the block
(four-point blade quad in a vertical plane tilted ~7°, bevel line, spine
line, corner hole, raised handle) reads instantly; a halved onion works
as concentric `flat_ellipse` rings for the cut face plus a radial-gradient
dome with meridian strokes; rosemary is one stem stroke with eight pairs
of needle strokes. A linen towel draped over the near edge is two quads —
one on the top plane, one hanging past it — with a woven stripe line on
each half.

Caption check: a 20-character name needs `nsize` ~46 to clear the width
assert; the helper now takes `nsize`/`ntrack`.

### Proposed change

Furniture note candidate: "Worktops read by their surface treatment —
end-grain = checkerboard of near-tone cells, scrubbed pine = plank seams
+ pale scrub strokes. A blade struck *into* the surface is stronger than
one laid on it; give it a cast shadow on the plane and a small bite
below the top." Pending until consolidated.
