## Grandfather clock V1R00 — shared gradient ramps must span the element's own extent

- Kind: lesson
- Source: #1178, `work/furniture/draw_grandfather_clock.py`, `art/furniture/grandfather-clock/grandfather-clock-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates (any piece mixing many small metal parts)
- Status: pending

### Evidence

The clock mixes prism-shaded mahogany with small brass parts (weights,
pendulum bob, bezel, finials, caps). First proof: every brass part filled
through one shared linear ramp keyed to canvas y 0–60 — all of them sat past
its end stop and rendered flat dark. The weights inside the glazed trunk
nearly vanished. Fix: a `brass(pts)` helper that builds the ramp over each
element's own projected y-extent (the same pattern the prism helper uses for
its faces). Second proof: bezel, bob and finials all lit correctly, and the
weights read through the door glass. A related find: the glazed trunk works
best as an open front — side cheeks + rails only — with interior contents
drawn before the case and the glass laid over them.

### Proposed change

For the furniture spec on next consolidation: "reused gradient constants must
span the drawing, not the palette — a ramp keyed to one corner of the canvas
goes flat everywhere else; build metal ramps per element from its own
projected extent." A proposal does not override current house rules.
