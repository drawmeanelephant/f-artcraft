## Orangutan V1R00 — decor under the subject is dead geometry; vines start on the disc

- Kind: lesson
- Source: issue #1067, `work/animals/draw_orangutan.py`,
  `art/animals/orangutan/orangutan-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — composition ordering
- Status: pending

### Evidence

Drafted a split durian on the litter floor *before* drawing the mane — but
the flanged male's mane closes on the disc arc at y800 and covers the whole
bottom crescent. The proof's `@2x.png` came out byte-identical with the
fruit removed: five objects of pure dead geometry. Rule: any floor decor
drawn before an arc-closed subject must land outside that subject's
footprint, or be drawn after it and read as resting on top.

Second near-miss: lianas drafted from y40 exit the disc sideways — at
x300/690 the disc's top edge is y≈85–91, so a vine "from the top" that
starts at the canvas top-left corner of the plate rect leaks onto the
backdrop. Vines must root at the *disc* edge, not the bounding square.

### Proposed change

Fold both into the field-plate trap list: *before drawing, check each decor
piece's layer order against the subject silhouette — fully occluded shapes
are dead weight; and decor "from the top of the plate" roots on the arc,
not on the plate's bounding square.* Destination:
`prompts/series/20-field-plates.md`.
