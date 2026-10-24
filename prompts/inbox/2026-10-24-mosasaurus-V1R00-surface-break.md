## Mosasaurus V1R00 — an arc close above the disc centre flips its flags

- Kind: lesson
- Source: issue #1088; `work/animals/draw_mosasaurus.py`, `art/animals/mosasaurus/mosasaurus-V1R00.*`
- Applies to: animals field plates; any banded plate (waterline, horizon)
- Status: pending

### Evidence

Proof `work/out/mosasaurus-V1R00@2x.png`. A waterline plate wants the sea
to fill from an above-centre chord down around the bottom of the disc.
Every floor in the series uses `A420,420 0 0 1` — but that flag pair only
works for chords *below* the disc centre. For a chord above it (waterline
at y336 vs centre y460), `0 0 1` picks the wrong candidate circle and the
"sea" renders as a lens floating mid-plate. The fix that shipped is
`A420,420 0 1 1` — large-arc on, sweep on: the arc runs the long way
around through the bottom of the disc.

The rest of the surface-break read: submerged shapes at opacity ~88 sell
"under water" without a blue wash layer; a foam collar ellipse on the line
plus four short crown arcs and a handful of droplets is enough for a
breach; the countershade belly (translucent pale path inside the trunk
silhouette) is what keeps the animal a lizard and not a whale.

### Proposed change

For `prompts/series/20-field-plates.md`: the rim-closing arc idiom is
`A R,R 0 0 1` for fills that hug the bottom of the disc, `A R,R 0 1 1`
for fills that span it from an above-centre line. Check any chord drawn
above y=460 before committing — the failure looks like a floating lens,
not a leak past the rim.
