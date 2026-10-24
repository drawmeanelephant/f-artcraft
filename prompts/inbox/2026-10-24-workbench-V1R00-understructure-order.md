## Workbench V1R00 — draw understructure before legs, and light shafts start inside the rim

- Kind: lesson
- Source: issue #1194, `work/furniture/draw_workbench.py`,
  `art/furniture/workbench/workbench-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — furniture (prism rig, painter-order joins)
- Status: pending

### Evidence

Two proof failures. First, a window-shaft quad and glow ellipse anchored at
the canvas edge leaked past the plate rim — shafts and glows must be placed
so every control point clears r=420, i.e. they start *inside* the disc, not
at a pretend window off-frame. Second, shelf planks spanning the full leg
pitch overpainted the leg faces and read as a slatted ramp running through
the legs; the fix was to end shelf boards ~1in inside the leg inner faces
and draw stretchers/shelf before the legs, so legs overpaint the joint ends
— painter-order joinery, not boolean joinery. What carried the workbench
read: the face-vise jaw + screw barrel + tommy bar cluster, a wide pale
board standing proud of the top (a narrow one read as a flag), the dog-hole
row with one popped dog, and a darker inset wagon block for the tail vise.

### Proposed change

Furniture spec candidates for next consolidation: "Draw a piece's
understructure (stretchers, shelves, dust frames) before its legs and posts
so the supports overpaint the joint ends; terminate infill boards inside
the posts' inner faces." and "Off-frame light sources are staged by cones
that begin inside the disc — never anchored to the canvas edge." Pending.
