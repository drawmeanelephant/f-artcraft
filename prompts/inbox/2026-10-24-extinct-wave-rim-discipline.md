## Extinct wave (mammoth / rex / dodo / megalodon) — rim leaks and jaw-drop layering

- Kind: lesson
- Source: issues #1023–#1026; `work/animals/draw_woolly_mammoth.py`,
  `draw_tyrannosaurus_rex.py`, `draw_dodo.py`, `draw_megalodon.py`;
  proofs `work/out/*-V1R00@2x.png`
- Applies to: animal field plates — any decor band, ray or streak near the rim
- Status: pending

### Evidence

All four extinct-animal plates shipped V1R00 after one critique round each.
Two recurring traps surfaced beyond the documented `A420,420` floor arc:

- **Decor that crosses the rim leaks visibly.** Aurora strokes (mammoth) and
  god-ray polygons (megalodon) both leaked past the disc on the first proof.
  Endpoint asserts against `on_disc(x, y, pad)` caught it for the flakes but
  long strokes need every control point checked, or their top edge seated on
  the disc curve (`y = cy - sqrt(r² - (x-cx)²)`).
- **Horizon/water bands must be lenses, not bars.** A rectangle-ish lagoon
  band (dodo) showed hard vertical seams inside the rim; a pointed lens
  (`M x,y C … C … Z` meeting at both ends) vanishes cleanly.
- **Open jaws want: mouth interior → dropped lower jaw → upper skull →
  teeth.** Teeth drawn last, straddling both jaw edges, read as rooted in
  the mouth (rex, megalodon). Dropping the jaw ~30–40pt at the chin is
  enough for the gape to read; the mouth interior should extend below the
  jaw's top edge everywhere so no plate color shows through the gape.
- Inverting the plate disc (dark abyss gradient top→bottom, megalodon)
  keeps the format but lets the subject read by rim-light + countershade
  instead of fill contrast — worth reusing for deep-sea subjects.

### Proposed change

Append to the field-plates traps in `prompts/series/20-field-plates.md`:
"Long decor (rays, ribbons, streaks) must seat its ends on or inside the
disc curve — assert every endpoint, not just the midpoint; horizon bands
read cleanest as pointed lenses." Consolidation only; no rule change.
