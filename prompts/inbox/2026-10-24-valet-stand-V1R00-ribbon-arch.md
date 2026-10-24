## Valet stand V1R00 — chained prisms on a shallow curve read as cogs

- Kind: lesson
- Source: #1238, `work/furniture/draw_valet_stand.py`,
  `art/furniture/valet-stand/` native and proof
- Applies to: field plates — furniture (any gently curved timber part)
- Status: pending

### Evidence

First pass built the valet's arched shoulder from ~18 short `beam`
segments end to end. On the proof each segment's ink outline showed as a
cross-cut, so the shoulder read as a cogged track / roller, not bent
mahogany. Replaced it with a single smooth ribbon: offset the arch spine
by its in-plane normal to get top and bottom edges (front face), plus a
narrow front-to-back "crown" band on top for the lit edge. The cogging
disappeared and the crown band still sells the 3D roundness. The
companion trick that survived: a long thin silk ribbon (the draped tie)
built by the same spine-plus-width method reads clearly at plate scale
and needs no prisms at all.

### Proposed change

Add to the furniture notes in `prompts/`: for a timber part whose curve
is gentle and lies near the picture plane (hanger shoulders, bent arms,
bows), draw one offset-edge ribbon with a crown band rather than chained
prisms — chained segments only suit sharp, faceted construction. Keep
the prism rig for straight members.
