## Recliner V1R00 — puffed quads for overstuffed work; a footrest reads by its front band

- Kind: lesson
- Source: #1187, `work/furniture/draw_recliner.py`, `art/furniture/recliner/recliner-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates; upholstered/overstuffed pieces
- Status: pending

### Evidence

Overstuffed volume came from `puff()`: four 3D corners projected, then each
edge midpoint bowed outward along the screen-space edge normal (9–15pt) —
one helper turns any slab into a cushion. Welts are stroked edge lines,
channel seams are strokes across the reclined slab.

The recline only read once the slab got a visible right side face and a
top cap leaning back (+z, −y); a front face alone reads vertical no matter
the rake. The flipped-up footrest reads by its **front band** — the
leading edge toward the viewer — not its top face, which is nearly
edge-on at a 16° pitch. First pass drew the top and produced a floating
plank. Yaw matters doubly: at 28° the forward-thrown pad (−z) exits the
disc lower-left; 20° keeps it under the seat.

Scissor linkage is best *hinted*: two thin X bars per side, partially
hidden by the base. Fully drawn it looks like scaffolding.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Upholstery:
project the corner quad, bow each edge midpoint outward ~10–15pt for
puff. A reclined slab needs its side + top cap drawn or it reads upright;
a footrest pad reads by its front band, not its deck." A proposal does
not override current house rules.
