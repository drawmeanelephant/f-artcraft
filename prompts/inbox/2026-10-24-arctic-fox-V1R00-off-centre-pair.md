## arctic-fox V1R00 — pair()/mirror() only works on centre-line subjects

- Kind: lesson
- Source: #1064, work/animals/draw_arctic_fox.py, art/animals/arctic-fox/arctic-fox-V1R00.*
- Applies to: animals field plates; non-portrait poses (curled, seated 3/4, walking)
- Status: pending

### Evidence

The curled "white comma" pose puts the head at x≈592, not on the plate's
x=500 axis — first draft reused the portrait mirror() helper for eyes and
brows and would have thrown the right eye 90px off the face onto the body.
Fix: hand-mirror about the head's own centre line and say so in a comment.
Second catch: drift-contour strokes drawn *on* the arc-closed snowfield
still leaked — an open q-stroke at (230,800) has endpoints past r=420 even
though the floor beneath it is sealed; contour lines need their endpoints
checked, same as scatter decor.

### Proposed change

For `prompts/series/20-field-plates.md`: when the subject is off-axis,
mirror() its features about the subject's centre, not the canvas — and
check_rim treats open contour strokes like any other shape.
