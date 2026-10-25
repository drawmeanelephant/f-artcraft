## Belgian V1R00 — draft mass is barrel depth plus leg thickness

- Kind: analysis
- Source: issue #1522; `work/horse-breeds/draw_belgian.py`,
  `art/horse-breeds/belgian/belgian-V1R00.{vectorcraft,svg}`,
  proof `work/out/belgian-V1R00@2x.png`
- Applies to: horse-breeds milestone cards; heavy/draft subjects
- Status: pending

### Evidence

One render-and-critique loop before shipping.

What worked:

- "Gentle giant" is a proportion problem: deepen the barrel to
  y≈655, widen legs to ~50pt columns, keep the neck short and
  crested. A normal-proportioned horse at bigger size still reads
  light horse; the leg-to-body ratio is what sells draft.
- Flaxen mane on sorrel is the breed's colour signature — keep it a
  tidy band on the crest. First pass let it fall to the chest and it
  read as a pale bib, not a mane.
- Small ears on a big plain head: deliberately undersized ears are
  the single fastest Belgian tell.
- "Clean-legged" is a real instruction: no feather at the fetlock —
  resist the draft-horse reflex to add it.
- Straw ticks on the floor give the stable world for ~8 calls.

What failed and got fixed:

- An interior "barrel glow" patch read as a pale saddle stain on the
  sorrel; warm glows on light coats must sit on edges (topline,
  chest), not the barrel face.

### Proposed change

Add to the horse-breeds card note at consolidation: draft = barrel
depth + column legs + small ears + clean fetlocks; flaxen mane stays
a crest band. No grammar divergence.
