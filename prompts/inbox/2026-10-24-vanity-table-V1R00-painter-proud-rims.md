## Vanity table V1R00 — painter's-order proud rims, and a cylinder helper for small glass

- Kind: lesson
- Source: issue #1219, `work/furniture/draw_vanity_table.py`,
  `art/furniture/vanity-table/vanity-table-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — furniture (projection rig, draw order)
- Status: pending

### Evidence

A gilt edge moulding drawn as a slightly oversized prism *after* the top
slab doesn't read as a thin border: with no z-test, its full top-face
quad overpaints the slab and the whole tabletop turns gilt. Draw the
moulding first so the slab covers all but its proud ring — the fillet
then reads as intended. Same ordering rule as the farmhouse stretcher:
anything meant to sit *behind* or *under* must be emitted earlier, even
when the prism helper would cull it correctly in isolation.

Round smalls (scent cylinders, flacons, powder boxes) wanted a
`cylinder()` helper: side wall as a path joining the two projected
ellipses (`A rx,ry 0 0 1` top front arc, `0 0 0` bottom front arc) plus a
`flat_ellipse` lid. An upright oval (mirror) projects honestly as a
26-gon through `P()` — it picks up the correct yaw skew that an
axis-aligned `draw_shape` ellipse cannot.

### Proposed change

Furniture note candidate: "Painter's algorithm is the whole occlusion
model: proud mouldings and under-parts go before the piece that
overlaps them. Keep a `cylinder()` helper in the furniture kit for
bottles, jars and pots." Pending until consolidated.
