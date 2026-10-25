# Vicuna V1R00 — accented caps reach higher than the name baseline

- Kind: lesson
- Source: issue #1131; `work/animals/draw_vicuna.py`,
  `art/animals/vicuna/vicuna-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates; any name with accented capitals (Ñ, É, Í…)
- Status: pending

### Evidence

Proof `work/out/vicuna-V1R00@2x.png`. `VICUÑA` at y=932 put the Ñ's
tilde at y≈886 — above ordinary cap height, inside `check_rim.py`'s
art zone (y<890), and it was the only flagged "leak": 89px of pale
glyph, not artwork. Virelai Sans does carry Ñ (proof shows it
correctly), but the diacritic box is ~8pt taller than the caps.

Fixed by moving the name to y=942 @58pt; the disc still reads against
it and the checker is clean.

### Proposed change

For `prompts/series/20-field-plates.md` or the typography note:
accented capitals overhang normal cap height; budget ~8–10pt above
the cap line when placing names near the disc rim, or keep name tops
below y895 regardless of the nominal baseline.
