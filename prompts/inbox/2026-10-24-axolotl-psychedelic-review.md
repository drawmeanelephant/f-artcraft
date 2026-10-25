## axolotl-V3R00 — psychedelic poster idiom; envelope warp destroys type, letter-by-letter arc works

- Kind: lesson / analysis
- Source: issue #1359, driver `work/animals/draw_axolotl_v3r00.py`,
  native/proof `work/out/axolotl-V3R00.{vectorcraft,svg,pdf,@2x.png}`
- Applies to: rendition work in the psychedelic idiom; warped lettering anywhere
- Status: pending

### Evidence

First pass applied `object.envelope.makeWithWarp` (arc, bend 42) to a whole
"AXOLOTL" text object in Party LET. The envelope crushed the word into two
spiral scrolls — decorative, illegible, a clear miss against "legible warped
type". Rebuilt letter-by-letter: each glyph as its own point text on a
baseline circle (tangent rotation via `object.rotate` about the glyph's own
origin), plus a cyan ghost copy offset +5,+5 for the overprint vibrato. That
reads cleanly at @2x and still feels liquid. Colour-wave bands are wavy
closed strokes (sinusoidal radius, 8 lobes) — cheap, controllable, and they
stay inside the 60pt margin when max r + wobble + stroke/2 ≤ 440. Gill
feathering reads as barbs when filaments are perpendicular to the stalk;
sweeping them ~40° toward the tip (normal·0.72 + tangent·0.62) restores the
axolotl softness.

### Proposed change

New inbox note candidate for a future `prompts/themes/` psychedelic-rendition
entry: for warped display type, prefer letter-by-letter arc placement over
envelope warps; reserve `makeWithWarp` for mild bends (<25) on single short
words, and always re-proof at @2x for legibility.
