## Club chair V1R00 — small props need painter order too

- Kind: lesson
- Source: #1151, `work/furniture/draw_club_chair.py`, `art/furniture/club-chair/club-chair-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates
- Status: pending

### Evidence

The prism helper sorts faces inside one volume, but separate volumes still
draw in script order. First render painted a rear bun foot on top of the
carcass's front apron — a floating dot in the middle of the chair. Splitting
the feet by depth (rear feet before the carcass, front feet after) fixed it
with no other change. Upholstered volumes read soft enough from face
gradients + swept bolster tubes alone; no corner-rounding paths were needed.

### Proposed change

For multi-volume pieces, group draw calls by depth band (behind carcass /
between / in front), not by part type. Candidate note for the furniture spec
on next consolidation. A proposal does not override current house rules.
