## obon-V1R00 — water as a disc cap; chochin silhouette

- Kind: lesson
- Source: issue #984; `work/holidays/draw_obon.py`;
  `art/holidays/obon/obon-V1R00.{vectorcraft,svg}`; proof
  `work/out/obon-V1R00@2x.png`
- Applies to: holidays / Festival Seals; any plate with a horizon or water
- Status: pending

### Evidence

A full-width water rectangle would poke square corners past the disc rim.
Clip it instead with a chord path: `M87.7,540 A420,420 1 0 1 912.3,540 Z`
(lower cap of the r420 disc at a y=540 horizon). The un-stroked top chord
reads as the horizon; one short line object at opacity ~40 reinforces it.

The chochin body wanted near-straight sides: a path that curves out through
`±a` all the way down reads as a beehive. Straighter sides with the dome
compressed into the top ~40% of the height fixes the silhouette; the dark
wooden float base must overlap the paper's bottom edge or it reads as a
detached hole.

Lanterns meant to float must keep their bases below the horizon y — a
distant lantern with its foot above the horizon reads as airborne.

### Proposed change

Add "water/horizon cap" + "floating chochin" notes to the shared festival
motif list at consolidation; `ripple()` + `reflection()` in this driver are
reusable for dragon-boat-style water scenes.
