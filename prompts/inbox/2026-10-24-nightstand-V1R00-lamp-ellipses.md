## Nightstand V1R00 — horizontal circles project to ellipses; a prop lamp carries a night plate

- Kind: lesson
- Source: #1169, `work/furniture/draw_nightstand.py`, `art/furniture/nightstand/nightstand-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates; any turned/cylindrical detail or glowing prop
- Status: pending

### Evidence

A horizontal circle of radius r at model height y projects to an ellipse
with semi-axes `r·S` by `r·S·sin(pitch)` — the `ell()` helper returns centre
+ radii, so lamp feet, glass rims and waterlines are exact, not eyeballed.
The glass of water is one translucent body quad (10→30% opacity ramp), a
waterline ellipse and a rim ellipse — three strokes and it reads at @2x.

The 3 a.m. mood is carried almost entirely by the lamp: a big soft radial
wash on the plate (26%→0%) plus a small hot core, both drawn *before* the
furniture so the stand sits inside the light. The shade itself is a plain
trapezoid whose bottom-rim arc (dark amber, ~3.5pt) sells the cone; the
brightest stop sits at the bottom of the shade where the bulb would be.

Face-framing the cubby worked like the cedar chest's slab carcass: stiles
+ rails + interior floor/back/left-wall quads, darkest stop at the ceiling
line. Two muted clothbound books inside keep the poem's "one drawer"
without emptying the piece.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Cylindrical
details (feet, stems, rims, glassware) project as ellipses: rx=r·S,
ry=r·S·sin(pitch). A lit prop reads when its glow is drawn under the
subject, its brightest gradient stop at the bulb position." A proposal
does not override current house rules.
