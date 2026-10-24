# Raccoon V1R00 — the ringed tail wants a sampled ribbon, not stroked arcs

- Kind: lesson
- Source: issue #1102; `work/animals/draw_raccoon.py`,
  `art/animals/raccoon/raccoon-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: animals field plates; banded/ringed tails (raccoon, lemur,
  coatimundi, genet)
- Status: pending

### Evidence

Proof `work/out/raccoon-V1R00@2x.png`. Three findings from the pass:

1. The tail was built as a sampled quadratic spine with per-station
   normals: one outer path from the ±halfwidth points, then ring quads
   spanning station pairs, then a dark tip quad. Taper (92→30 pt) and
   ring placement come free from the station list, and every ring edge
   stays perpendicular to the spine — much cleaner than stacking stroked
   arcs and hoping the bands land on the band.
2. Forepaws over the loot first shipped with finger strokes crossing the
   apple — they read as scribbles on the fruit. Moving the mitts out to
   cup the apple's flanks (x ≈ ±42) and keeping finger marks inside the
   mitt fixed it: the red has to show between the hands or the prop
   disappears.
3. Ear v1 was a tall triangle on top of the head — read as lagomorph.
   Shortening to a rounded shell tucked into the head corner (base
   overlapping the crown line) fixed the species read. Raccoon ears are
   small and sit ON the silhouette, not above it.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: *banded tails are a
sampled ribbon problem — build the spine, offset it into one outer path,
then lay ring quads between stations; never stroke arcs and overlay
bands. Prop-in-paws: the prop must remain visible between the mitts —
hands cup the flanks, not the front.*
