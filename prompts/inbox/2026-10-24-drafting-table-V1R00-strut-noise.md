## Drafting table V1R00 — mechanism clutter reads as breakage

- Kind: lesson
- Source: issue #1162, `work/furniture/draw_drafting_table.py`, `art/furniture/drafting-table/drafting-table-V1R00.*`
- Applies to: field plates — furniture
- Status: pending

### Evidence

First render added two tilt-lock struts from the rear legs up to the
board's underside. At plate scale they crossed the A-frame legs at similar
stroke weight and read as a snapped strut, not a mechanism. Removed them;
the pivot discs at the trestle apexes carry the "adjustable" story alone.
The rest holds: trapezoid board (near edge wide, far edge short) reads as
tilt; vellum sheet inset by lerping corners toward the centroid keeps the
perspective honest; the T-square's maple head overhanging the board's left
edge is the instant tool read.

### Proposed change

On machine-adjacent furniture, one clear joint beats two fuzzy linkages —
pivot disc + axle reads, a second crossing diagonal does not. Parametrize
inset panels (paper, leather, upholstery) by lerping toward the parent's
centroid so perspective survives later resizes.
