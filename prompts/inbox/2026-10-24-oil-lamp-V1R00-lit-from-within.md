## Oil lamp V1R00 — a lit subject carries its own plate lighting

- Kind: lesson
- Source: #1177, `work/furniture/draw_oil_lamp.py`, `art/furniture/oil-lamp/oil-lamp-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates (lamps, stoves, anything self-luminous)
- Status: pending

### Evidence

The lamp is turned ware, so it was built as lathe-profile outlines mirrored
about the axis plus section ellipses at each rim — the pedestal-table
approach, not the prism rig (a faceted glass chimney would read wrong). Three
moves did most of the work: the flame is drawn as three nested smoothed
teardrops seated directly on the wick (any gap reads as floating); the font
sells "reservoir" through one horizontal oil-surface ellipse over a darker
inset pool, not through glass shading alone; and the plate's whole lighting
scheme is sourced from the subject — a warm radial bloom behind the lamp and
a warm pool on the floor chord, over a cool dark disc. The open chimney mouth
is one ellipse ring seen from slightly above; it is what makes the glass read
hollow instead of solid.

### Proposed change

For self-luminous subjects, cool the disc and let the subject own every warm
pixel: bloom behind, light pool on the floor, and seat the flame geometry on
its wick. Candidate line for the furniture spec on next consolidation. A
proposal does not override current house rules.
