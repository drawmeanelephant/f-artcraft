## Madagascan sunset moth V1R00 — structural colour as broken bands

- Kind: lesson
- Source: issue #1120, `work/insects/madagascan-sunset-moth-V1R00.py`,
  `art/insects/madagascan-sunset-moth/madagascan-sunset-moth-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: insects field plates (iridescent-winged subjects)
- Status: pending

### Evidence

Iridescence on the forewing reads best as short colour-stepped strokes
(green → teal → violet) hugging the outer margin, not a single gradient —
a stroke can't vary hue along its length, so three-to-four 15pt segments
at ~80% opacity fake the shift cleanly. The orange hindwing field wants a
radial warm gradient with a dark margin band laid over it; the pale tail
tips (small cream blobs at each tail point) are what make the scalloped
margin read as *tails* rather than a wavy edge. Eyes must be placed in
transformed space — a first pass put them in raw y and they floated 50pt
above the head.

### Proposed change

For mirror-built insects, run every facial feature through `T()` even when
it sits on the axis — raw/screen mixups are invisible until the proof.
Candidate note for the insects section of
`prompts/series/20-field-plates.md`.
