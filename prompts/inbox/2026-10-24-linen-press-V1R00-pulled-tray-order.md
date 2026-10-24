## Linen press V1R00 — a pulled tray must paint over the frame, and a swung door needs ≤40°

- Kind: lesson
- Source: #1199, `work/furniture/draw_linen_press.py`, `art/furniture/linen-press/linen-press-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates (open doors, pulled trays/drawers)
- Status: pending

### Evidence

Two draw-order facts for full-width sliding trays: the tray physically
crosses in front of the face frame and the closed door when pulled out, so
the pulled tray, its linen piles and its garnish must be painted *after*
the frame and the closed door (but before the swung-open leaf, whose tip
is nearer the viewer). Kept inside the interior block it gets a stile bar
painted across its front board — reads broken.

Swing angle is legibility, not just realism: at 52° of swing a ~115-unit
leaf projects ~20px — a sliver, not a door. At 36° the same leaf lands
~50px with its inner face visible; the armoire's 46° worked because its
leaf is wider. Rough rule: screen width ≈ leaf·(cosA·cosTH − sinA·sinTH).

Folded linens are parallelogram bands with one low-opacity fold seam each
and a darker ramp per fold — a stack of 3–4 reads as cloth instantly. A
lavender sprig survives as two stems + lozenge buds; ticks under ~3.5pt
vanish.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Pulled
elements paint after the face frame they cross; swung doors need ≥35px of
projected leaf or they vanish — solve the swing angle for that, not the
mechanism." A proposal does not override current house rules.
