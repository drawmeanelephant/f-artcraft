## Remembrance Day V1R00 — drawn chop marks need outlined lobes to read at 60px

- Kind: lesson
- Source: #992, `work/holidays/draw_remembrance_day.py`,
  `art/holidays/remembrance-day/` native and proof
- Applies to: festival seals — the drawn-mark vermilion chop (christmas star,
  easter egg, remembrance poppy)
- Status: pending

### Evidence

First pass stamped the chop poppy at r=16 with unstroked cream petals:
four ellipses overlapped into a single blob, and on the proof the mark
read as a fried-egg dot, not a flower. Enlarging to r=18 and stroking
each petal with the chop's dark vermilion outline (`#4E100E`, 1.4px)
separated the lobes — at seal scale the inter-petal outline is what
carries the read, not the fill silhouette. Matches the christmas/easter
precedent: one bold glyph, strong inner contrast, no fine detail.

Also confirmed: `rim_band()` (disc-arc ground, same family as
golden-week's `rim_hill`) is the right way to put a horizon/ground inside
the seal without tripping `check_rim.py`.

### Proposed change

Add to the holiday-seal notes in `prompts/`: for drawn marks inside the
62px vermilion chop, keep one glyph, push lobes out to ~0.3 of the seal,
and stroke every lobe in the dark seal-outline colour — unstroked
adjacent petals merge into a blob at proof scale.
