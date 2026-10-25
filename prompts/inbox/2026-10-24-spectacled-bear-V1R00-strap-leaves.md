# Spectacled bear V1R00 — plants want leaf shapes, not leaf strokes

- Kind: lesson
- Source: issue #1130; `work/animals/draw_spectacled_bear.py`,
  `art/animals/spectacled-bear/spectacled-bear-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: animals field plates; habitat props (bromeliad, rosettes)
- Status: pending

### Evidence

Proof `work/out/spectacled-bear-V1R00@2x.png`. First bromeliad pass used
single cubic outlines pinched at both ends — rendered as grass blades
with a floating red ball. Replaced with `strap_leaf()`: each leaf a
closed quad-strip (base point → widened mid → pointed tip) fanning from
one rosette base, so the five leaves share an origin and read as one
plant.

Paw-on-log: claws drawn from the paw's lower edge hanging to y+8 read as
little legs under the log. Shortening them to 6pt hooks ending against
the log's front face fixed the contact.

Also: a translucent mist ellipse whose corner crossed r420 was the only
rim leak — ellipse corners, not edge midpoints, are what escape the disc.

### Proposed change

For `prompts/series/20-field-plates.md`: note that habitat flora is
built from closed leaf shapes sharing a base point; and when checking
rim containment, evaluate ellipse corners, not just centers/edges.
