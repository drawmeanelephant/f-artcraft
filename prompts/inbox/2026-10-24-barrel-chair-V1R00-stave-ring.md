## Barrel chair V1R00 — a tub is a ring of rotated prisms, and an opening is a height change

- Kind: lesson
- Source: #1180, `work/furniture/draw_barrel_chair.py`, `art/furniture/barrel-chair/barrel-chair-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates (cylindrical or stave-built pieces)
- Status: pending

### Evidence

The tub is 41 staves — rotated 8-corner prisms set on a circle (`rbox` rotates
the local plan rectangle about y before projection) — so the stock
face-culling sorts inner faces, outer faces and the cut ends on its own. Two
findings on the proofs:

- The "opening" of a barrel chair is not missing wall — it is staves cut to
  seat height all the way around front. First framing (tall arc + a separate
  flat front rail) read as a wall with a hole; the full ring of staves at two
  heights reads as a cut-down barrel, and the low front staves get a proper
  iron hoop across them.
- A free-standing cushion kept reading as an egg until it got three anchors:
  wider than tall, an up-vector tilted back onto the wall, and a contact
  shadow where it meets the seat.
- (lam + bias) ** 0.8 throws on negative bases — clamp before fractional
  powers when jittering per-part brightness.

### Proposed change

For the furniture spec on next consolidation: "cylindrical furniture is a
ring of rotated prisms; cut openings are height changes, not holes — painter-
sort the ring by view depth and let face culling do the rest." A proposal
does not override current house rules.
