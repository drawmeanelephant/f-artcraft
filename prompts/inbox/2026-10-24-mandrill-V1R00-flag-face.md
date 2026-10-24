## Mandrill V1R00 — build the flag as three zones, not a pattern

- Kind: lesson
- Source: issue #1097; `work/animals/draw_mandrill.py`,
  `art/animals/mandrill/mandrill-V1R00.*`
- Applies to: animals field plates; saturated facial colour zones
- Status: pending

### Evidence

Proof `work/out/mandrill-V1R00@2x.png`. The muzzle was built as three
separate filled zones in strict z-order: violet-blue ridged swellings
(each a slim closed `smooth()` lobe with two darker groove strokes and an
outer highlight), then the vermillion nose stripe drawn over them down
the centre, then the red nose tip and dark nostril wings. The colour
stays saturated because each zone is its own gradient — no translucent
colour layered over colour. Three groove strokes at 55% opacity inside
each lobe are enough to read as the mandrill's corrugation.

Two things nearly failed: a chin badge sized like a real marking (wider
than the mouth) read as a tongue sticking out — shrinking it to a narrow
lip-width mark fixed it. And fronds in the upper corners: the first
angles pointed up-right, outside the disc; a paired frond needs its lean
angle recomputed per side (35°/55° left, 145°/125° right), checked with
`on_disc` asserts on base/mid/tip, since `smooth`/`Q` control points can
exceed the rim even when endpoints sit inside.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: mirrored
directional decor (fronds, tails, horns) — store the lean as an angle per
side and assert all generated vertices, not just anchors, stay inside
the disc. And for any chin/lip colour accent on a portrait: keep it
narrower than the mouth line or it reads as a protruding tongue.
