## Papasan chair V1R00 — a bowl needs its rim to read

- Kind: lesson
- Source: #1210, `work/furniture/draw_papasan_chair.py`, `art/furniture/papasan-chair/`
- Applies to: field plates — furniture (any vessel-like piece)
- Status: pending

### Evidence

First pass put the cushion disc wider than the rim (`overhang 0.13`, `CR 17`
vs rim 17.6) and the render read as a balloon on a wastebasket: the paraboloid
shell band and belly disc all projected *inside* the cushion silhouette, so no
rattan survived. The fix that made it a chair: cushion nests *inside* the rim
(`CR 15.4`, puff lift +2.2 along the bowl axis instead of radius overhang),
which exposes the rim torus band and the shell crescent under the front lip.
A thin "interior wall" band (k 0.74–0.94, far half) gives the inside of the
bowl a shadow edge behind the cushion. Two more traps: a band path run
through the closed Catmull-Rom `smooth()` spikes at its corner joints —
use `poly()` where arc ends meet at real corners; and the base drum only
reads as "nested" once its plan centre sits under the bowl belly (z≈11),
not under the rim's front lip.

### Proposed change

For dish/bowl/hood furniture in `prompts/series/20-field-plates.md`
(Furniture traps): the occupant of a vessel (cushion, hood interior) must
stay *inside* the rim's projected ellipse; depth sells through the rim band
plus an interior-wall crescent, not through silhouette overhang.
