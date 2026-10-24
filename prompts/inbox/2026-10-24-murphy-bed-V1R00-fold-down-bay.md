## Murphy bed V1R00 — the open bay carries the fold story

- Kind: lesson
- Source: issue #1201, `work/furniture/draw_murphy_bed.py`, `art/furniture/murphy-bed/murphy-bed-V1R00.*`
- Applies to: field plates — furniture
- Status: pending

### Evidence

Drawn deployed rather than mid-fold: the murphy read comes from the empty
cabinet bay behind the mattress, not from a tipping plane. The bay's back
panel got two faint vertical seams (the bed's false door fronts live there
when it's up) and a top shadow wash; the coil spring + pivot strut on the
left inner wall is the mechanism signature and survived at 2.4pt. The foot
face is drawn as the false cabinet front — two inset panels + pull handles —
which does more explaining than any pillow or quilt. Mattress restraint
straps (thin prisms across the mattress, buckle rings) sold "this thing
folds" for one line each. A rug tucked under the footprint with only its
ears showing is cheap depth; let its corners project outside EXTENT or the
assert fails on bookkeeping points, not art — `Pq()` projects without
registering.

### Proposed change

For transform/folding furniture (murphy, sofa bed, drop-leaf): show the
*after* state and let the emptied housing explain the motion — an open bay,
a visible hinge or spring, and one strap earns more than a mid-action pose.
Destination: `prompts/series/20-field-plates.md` furniture traps.
