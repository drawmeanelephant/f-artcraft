## guy-fawkes-night V1R00 — a bonfire needs visible wood, not hidden structure

- Kind: lesson
- Source: issue #988, `work/holidays/draw_guy_fawkes_night.py`,
  `art/holidays/guy-fawkes-night/guy-fawkes-night-V1R00.vectorcraft`,
  `work/out/guy-fawkes-night-V1R00@2x.png`
- Applies to: holidays / Festival Seals; any fire motif
- Status: pending

### Evidence

First pass drew a classic teepee of leaning logs converging behind
`festival_kit.flame`. The layered flame (opacity ~96 gradient) swallowed
every log top; what survived was a wishbone of two front legs with a
floating char dot — unreadable. Second pass stacked a horizontal pyre but
left a dark gap between flame base and log, so the fire floated. What
worked: two long logs in a shallow X with ends protruding past the coal
bed, a glowing `Coal bed` ellipse (orange radial) tucked on the crossing,
the flame base overlapping the coals by a few px, then a short front log +
`cut_face` sawn ends (pale wood disc + growth ring) to sell "wood".
Smoke wisps from `flame()`'s smoke param read well against the night field;
the seeded `spark_shower` of bowed falling streaks under the top burst is a
reusable Guy-Fawkes/generic ember-rain motif.

### Proposed change

Rule of thumb for fire scenes: flame gradients are nearly opaque — never
rely on structure drawn behind a flame to read; give the pyre protruding
ends, a coal bed, and cut faces, and overlap the flame base onto the fuel
by ~5px so nothing floats. Candidate helper for `festival_kit.py`:
`pyre(d, cx, cy, w)` bundling crossed logs + coal bed + cut faces.
Destination: `prompts/series/` holidays notes on next consolidation.
