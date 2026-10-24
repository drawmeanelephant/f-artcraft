## Peacock chair V1R00 — annulus bands seam under smooth()

- Kind: lesson
- Source: #1211, `work/furniture/draw_wicker_peacock_chair.py`, `art/furniture/wicker-peacock-chair/`
- Applies to: field plates — any ring/torus/band built as outer-arc + reversed inner-arc
- Status: pending

### Evidence

Every "annulus" path (outer ellipse sampled forward + inner ellipse sampled
back, closed) run through the closed Catmull-Rom `smooth()` spawns a ~10px
loop bump at the 3-o'clock seam where the radial jump between the two arcs
is faired into a curl — visible on the fan rim's right edge in the proof.
The same latent seam exists in `draw_papasan_chair.py` (rim band) and any
band built this way. `poly()` makes the join a crisp radial step that reads
as a rim joint instead. Also: arm ribbons that should grow out of a rim
frame only read once the root starts *inside* the rim's inner edge
(u≈inner radius at the take-off angle); starting at mid-band left the flat
cap exposed outside the silhouette. The peacock fan needs its convergence
hidden — a tapered "tail bundle" ribbon + binding wraps between hub and
seat sells the joint.

### Proposed change

Add to Furniture traps in `prompts/series/20-field-plates.md`: closed
Catmull-Rom is for curves without radial jumps — annulus bands (outer+inner
arc) must use `poly()` or the seam curls into a loop at the wrap point.
