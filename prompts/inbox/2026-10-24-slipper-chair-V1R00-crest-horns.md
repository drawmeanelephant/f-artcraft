## Slipper chair V1R00 — closed splines sprout horns at crest corners

- Kind: lesson
- Source: issue #1181, `work/furniture/draw_slipper_chair.py`, `art/furniture/slipper-chair/slipper-chair-V1R00.*`
- Applies to: field plates — furniture
- Status: pending

### Evidence

First render of the chair back used the usual smooth() closed spline over a
boundary of just two polylines: crest left→right, then seat line
right→left. The closing edge (seat-end back up to crest-start, ~340pt of
side) fed the Catmull-Rom tangent at the crest corners, and each top corner
overshot into a ~15pt spike — twin horns on the proof. Fix: sample the side
edges in the boundary loop (four intermediate points per side) so every
spline neighbour stays local. Crest band also went to fill-only with its
ends tucked at u=0.03..0.97, and the welt cord carries the edge. Second
render is clean; tufting, cushion overhang and caster legs all read at @2x.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: a closed smooth() ring
must never contain a long jump between its last and first samples — pad the
loop with points along every real edge, or the spline corners overshoot
into spikes. Padding costs nothing; the rim clearance assert already sees
the loop.
