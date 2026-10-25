## canada-day V1R00 — recovered draft finished; underlay stem-poke fix

- Kind: lesson / analysis
- Source: #990; `work/holidays/draw_canada_day.py`;
  `art/holidays/canada-day/canada-day-V1R00.{vectorcraft,svg}`;
  proof `work/out/canada-day-V1R00@2x.png`
- Applies to: holidays / Festival Seals; any emblem built from stacked
  offset underlays of the same polygon
- Status: pending

### Evidence

The piece was recovered as a finished V1R00 draft from a dead worker's
worktree (t3/1c3b203b): scarlet eleven-point maple leaf on a cream field,
red/amber firework bursts, maple-key samaras, drawn-leaf chop. Two real
defects and one gap showed in the proof:

- Shadow/edge underlays were the leaf polygon offset and enlarged — both
  poked a visible cream/grey tab below the leaf stem (the stem is inside
  the polygon, so every underlay gains a stem too). Fix shipped: a second
  outline `LEAF_NS = LEAF[:12] + LEAF[16:]` chords the stem shut and is
  used for shadow + edge; the body keeps the stem. Nothing pokes.
- The same 11-point leaf shape drawn small (s<~0.5 of the hero) reads as a
  starburst/splat, not a leaf — the lobe hierarchy compresses to uniform
  spikes. Dropped; the lower field fills with a gingham picnic-blanket
  arc + six samaras instead.
- The finished seal survives critique: clean rim (`check_rim` pass),
  no flag echo (no bars/rectangle — leaf is a shaded object on a round
  field), bilingual date line "JULY 1 · FÊTE DU CANADA" in Source Sans 3.

### Proposed change

For `prompts/core/` or a festival-kit note: when an emblem outline embeds
an appendage (stem, tail, cord) inside its polygon, generate a chorded
`*_NS` variant for every underlay (shadow/edge/halo-adjacent path fills);
the appendage only belongs in the top body fill. And: reuse-silhouette-at-
small-scale needs a proof check — an emblem that reads at 300px can
collapse to a starburst at 100px.
