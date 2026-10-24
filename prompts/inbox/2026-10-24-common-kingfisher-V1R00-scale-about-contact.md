## Common kingfisher V1R00 — scale the bird block about the perch contact

- Kind: lesson
- Source: issue #1080; `work/animals/draw_common_kingfisher.py`,
  `art/animals/common-kingfisher/common-kingfisher-V1R00.*`
- Applies to: field plates, small perched birds
- Status: pending

### Evidence

A ~320pt bird on a tall snag over water left the upper half of the disc
empty — the peregrine scale problem again. Rather than re-hand-placing every
coordinate, the script scales the whole bird block 1.3x in code: `P(x,y)`
for shape positions and `T(dstr)` regexing each path's number pairs about
the perch contact point (530,636), stroke widths included. The feet stay on
the snag seat for free because the pivot IS the grip point. Two smaller
reads also needed the proof: a white "throat" patch placed under the chin
rendered as a hanging tooth — the kingfisher's white belongs at the side of
the neck — and the chestnut ear patch had to cover the whole lower face,
not just a sliver. The underwater fish inside its own ellipse ripple rings
carried "fish-flash" at low opacity without competing with the bird.

### Proposed change

When a plate subject reads small at proof, scale its whole block about the
contact point (perch grip, wheel contact, foot pressure) rather than
redrawing — one pivot keeps every attachment honest. Destination: animals
section of the field-plate rules.
