## Bar cart V1R00 — turned bottles need their own axis, not P() points

- Kind: lesson
- Source: #1234, `work/furniture/draw_bar_cart.py`,
  `art/furniture/bar-cart/bar-cart-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — furniture (any plate with bottles, glasses or
  other lathed dressing)
- Status: pending

### Evidence

The trolley (culled prisms + `rbox` rails) read on the first pass, but every
lathed object needed a second iteration:

- A "glint" streak keyed to the profile's absolute y values ran the full
  model height — thin antennae sticking out of every bottle into empty
  plate. Glints must key to the profile's own `y0..y1` range, not to raw
  profile coordinates.
- `lin((0,0),(0,1), ...)` placeholders on the ice bucket and jigger produced
  near-flat dark blobs. Every gradient must be keyed to real projected
  extents (the axis anchor ± the silhouette radius), exactly like the prism
  shading does.
- A surface of revolution about a vertical axis needs no 3D sampling: the
  silhouette edge projects at `xr ± r` at each profile height, so
  `axis2d()` + `S*r` + `S*CP*y` gives the whole outline from one
  `(r, y)` list.
- Opaque contents (shaker, ice bucket) should skip the glass-envelope
  helper entirely and take a metal ramp — the translucent glass wrapper
  over an opaque fill read as a pale milk bottle.
- Survives critique on pass 2: trolley read is immediate, stock order is
  far→near, casters dim with depth, extent 339 of 396.

### Proposed change

Add a short note to `prompts/series/20-field-plates.md` under Furniture:
"bottles, glasses and other lathed dressing draw as silhouette envelopes
from `(r, y)` profiles — key every gradient to the projected axis anchor,
and key glints to the profile's own height range."
