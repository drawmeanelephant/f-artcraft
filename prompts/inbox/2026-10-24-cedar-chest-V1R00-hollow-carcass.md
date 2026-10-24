## Cedar chest V1R00 — a hollow carcass needs slab walls, and contents must crest the rim

- Kind: lesson
- Source: #1168, `work/furniture/draw_cedar_chest.py`, `art/furniture/cedar-chest/cedar-chest-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates (any open box, drawer, trunk or crate)
- Status: pending

### Evidence

The chest is modelled as five thin slabs (floor, back, left, right, front
walls) rather than one solid prism, so the existing `normal · TO_VIEWER`
culling opens a real cavity: the pale interior faces of the back and left
walls face the viewer while the right wall's interior is correctly culled.
An open lid is an ordinary 8-corner prism whose corners are rotated about
the hinge axis before projection — its underside lands facing the viewer
at ~105° and takes the pale interior gradient.

Two proof failures taught the contents rule: folded linens stacked below
rim height render as an empty box (the front wall hides them), and a long
rolled blanket laid along the rim read as a white cigar, not bedding. What
worked: fill the cavity to ~2in below the rim, then place one folded
blanket cresting ~1.5in over the front rim, drawn *before* the front wall
slab so the rim occludes its lower edge — the crest sells "full chest" in
one glance. A draped quilt over the front lip needs its fold lines stopped
~1in above its hem or they render as drips.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Open
containers: build the carcass from five slabs so face-culling reveals the
cavity; contents must crest the front rim or the box reads empty. A lid is
a prism rotated about its hinge line — its underside faces the viewer past
~95°." A proposal does not override current house rules.
