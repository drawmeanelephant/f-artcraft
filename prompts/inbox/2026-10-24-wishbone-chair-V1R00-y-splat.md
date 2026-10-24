## Wishbone chair V1R00 — a flat Y splat inside a swept rail

- Kind: lesson
- Source: #1185, `work/furniture/draw_wishbone_chair.py`, `art/furniture/wishbone-chair/wishbone-chair-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates; chairs with bent rails or flat splats
- Status: pending

### Evidence

The CH24-style arm rail is one smooth 3D centerline (a horseshoe in plan,
height falling toward the arm tips) drawn as a screen-space ribbon —
outer/inner edges offset along the curve normal, same idiom as the Windsor
hoop. Two failures cost iterations: the splat tips kept nicking above the
rail's top edge (Catmull-Rom overshoot at the sharp tips — cap tip height
~0.5in under the rail surface, not at it), and the front leg tops poked
through the rail ends until they were dropped ~0.8in below the rail
centerline. The splat's stem has to run *below* the seat top and hide
behind the back rail's face or it reads as a vase parked on the seat.

The +z half of the chair (splat, rail apex, back posts) shifts right under
positive yaw — at 30° the composition visibly leaned; 27° rebalanced it.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Members that
must *meet* a rail should stop ~0.5–0.8in inside it — Catmull-Rom
overshoot at tapered tips escapes ribbons. A flat back splat needs its
stem planted below seat level behind a rail face, or it floats." A
proposal does not override current house rules.
