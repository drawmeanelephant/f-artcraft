## songkran-V1R00 — water arcs need a landing, drops need rotation

- Kind: lesson
- Source: issue #985; `work/holidays/draw_songkran.py`;
  `art/holidays/songkran/songkran-V1R00.{vectorcraft,svg}`; proof
  `work/out/songkran-V1R00@2x.png`
- Applies to: holidays / Festival Seals; any splash/fountain motif
- Status: pending

### Evidence

First pass drew thin diagonal water streaks ending in mid-air with a puff —
they read as wires, and the freehand bezier teardrops rendered as arrowhead
flags. Two changes fixed it:

- Parabolic jets that start at the bowl rim, crest, and *land* on the field
  floor (squashed foam burst + flattened rings at the endpoint) read as
  sloshed water immediately. A splash needs somewhere to land.
- Droplets work as small `ellipse` shapes stretched along the flight
  tangent via `rotation=` — no hand-built teardrop path needed.
  (`rotation=` is accepted on `draw_shape`; `rotate` is the rejected key.)

`water_puff` ports the gulal_cloud soft-lobe language to water by swapping
the pigment for aqua/foam radials; `squash` flattens it into a floor burst.

### Proposed change

Candidate for the shared splash notes at consolidation: "arcs land on
geometry or ground, never mid-air" and "droplets = rotated ellipses".
