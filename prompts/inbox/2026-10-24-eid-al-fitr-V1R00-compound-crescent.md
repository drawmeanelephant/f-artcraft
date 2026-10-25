## eid-al-fitr-V1R00 — crescents via compound paths, foot silhouettes via rim arc

- Kind: lesson
- Source: issue #977, work/holidays/draw_eid_al_fitr.py, art/holidays/eid-al-fitr/eid-al-fitr-V1R00.*
- Applies to: holidays / festival seals
- Status: pending

### Evidence

A crescent draws cleanly as one compound `draw_path`: outer disc as two
arcs wound clockwise plus a smaller offset "bite" disc wound
counter-clockwise. The nonzero fill rule punches a true hole so the disc
field (gradient and all) shows through the bite — no fake background-fill
overlay needed, and the stroke traces the bite edge for free. A second
slightly smaller compound pass at low opacity reads as earthshine.

Foot-of-disc silhouettes (rooftops) use the same chord-plus-rim-arc
closure as the christmas snow floor; endpoints must be computed on the
rim, not eyeballed — x=236 at y=806 leaked 55 px outside r430.

### Proposed change

Add the compound-path crescent idiom and the rim-arc floor idiom to the
shared holidays notes; both are reusable across the wider calendar
(obon, vesak, dia-de-los-muertos all want night fields).
