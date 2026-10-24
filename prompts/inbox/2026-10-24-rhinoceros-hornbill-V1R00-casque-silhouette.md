## Rhinoceros hornbill V1R00 — the casque is a wedge, not a crest

- Kind: lesson
- Source: issue #1077; `work/animals/draw_rhinoceros_hornbill.py`,
  `art/animals/rhinoceros-hornbill/rhinoceros-hornbill-V1R00.*`
- Applies to: field plates, hornbills and other bill-casque birds
- Status: pending

### Evidence

First pass drew the casque as a tall lobe rising over the crown — on the
proof it read as a crest/mohawk, not a casque, because its top edge peaked
above the head and its front face merged into the face silhouette. The fix:
the casque is a long low wedge riding the mandible, roughly parallel to the
culmen, with only the front-top corner kicking up into the horn. Two seams
sold it: a casque-foot line where the wedge lands on the bill
(`M313,352 C340,362 375,368 420,372`) and the tomium along the under-edge.
Drawing the head as a strokeless fill inside the body's own crown contour
removed the "bean" seam a stroked head blob made against the nape.
The red eye with three short lash strokes carries the male at plate scale;
keep it just inside the bill's face edge, not on the bare skin blob alone.

### Proposed change

For bill-casque plates: draw bill+casque as one silhouette, then colour-zone
the casque with a translucent darker flush and mark the casque/mandible
seam — separate outlined shapes read as a hat. Destination: a line in the
animals section of the shared field-plate rules.
