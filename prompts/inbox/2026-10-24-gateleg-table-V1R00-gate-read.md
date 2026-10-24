## Gateleg table V1R00 — the gate is a silhouette problem, not a label

- Kind: lesson
- Source: issue #1160, `work/furniture/draw_gateleg_table.py`, `art/furniture/gateleg-table/gateleg-table-V1R00.*`
- Applies to: field plates — furniture
- Status: pending

### Evidence

First render read as a generic oval-top table: the leaf seams were 3.5pt
at 65% and vanished, and two detached "leaf underside" quads floated past
the top silhouette as stray bars. Fixed by (a) moving underside shadow
onto the edge band itself as 12pt arcs hugging the lower rim inside the
leaf thirds, (b) doubling the seams to 4.5pt plus a 2pt light hinge line,
(c) lifting the apron so the drawer face shows below the band. The swung
gates read through their angled top/bottom rails converging back to pivot
dots at the frame edge; the gate legs alone do not sell it.

### Proposed change

Furniture with moving parts (drop leaves, fold-downs, tilts): draw the
mechanism's signature as a *relationship* (rail-to-pivot, leaf-to-seam),
not a silhouette part — a lone extra leg reads as just another leg. Keep
under-top shading on the top's own rim arc; quads hanging below an
ellipse edge always look detached.
