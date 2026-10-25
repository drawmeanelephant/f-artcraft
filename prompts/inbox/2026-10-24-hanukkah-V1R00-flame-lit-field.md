## Hanukkah/V1R00 — let the flames be the only light source

- Kind: lesson
- Source: issue #979, `work/holidays/draw_hanukkah.py`,
  `art/holidays/hanukkah/hanukkah-V1R00.*`, proof `work/out/hanukkah-V1R00@2x.png`
- Applies to: holidays (Festival Seal) series
- Status: pending

### Evidence

First wider-calendar seal and the first non-CJK/Devanagari-script chop.
What worked: a straight chanukiah bar (8 cups, shamash cup riding the stem
above centre) reads instantly as Hanukkah without any figure. Drawing the
stem base→bar→shamash as one continuous column, with the bar crossing over
it, keeps the elevated ninth light physically legible. "Flames as the
light source" landed: two stacked radial glows centred on the flame row
plus a small halo per flame, over a cool sapphire disc with a strong
vignette — the gold bar and cups pick up the warm pool believably.
Alternating cream/ice-blue candles keep 8 identical flames from going
monotonous. Gelt coins at the foot add the food-holiday note without a
second scene.

Gotchas exercised: the chop uses `Arial Hebrew` (installed); Hebrew needs
no shaping so the per-glyph vertical stack in `Plate.chop` is safe — Devanagari
or Sinhala chops would need `horizontal=True` instead. The date line uses
`Source Sans 3` because Virelai Sans has no digit glyphs. Backdrop stars
trip `check_rim.py` (85px) — expected; they are deliberate backdrop, same
as lantern-festival.

### Proposed change

A short note in the Festival Seal section: wider-calendar seals stamp the
holiday's own script in the chop when it needs no shaping (Hebrew OK);
use `horizontal=True` for shaping scripts (Devanagari, Sinhala, Thai).
Destination: `prompts/series/40-orient.md`.
