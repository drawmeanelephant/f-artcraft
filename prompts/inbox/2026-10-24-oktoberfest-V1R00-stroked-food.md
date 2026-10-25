## Oktoberfest V1R00 — fat stroked paths make legible food icons at seal scale

- Kind: lesson
- Source: #994, `work/holidays/draw_oktoberfest.py`,
  `art/holidays/oktoberfest/` native and proof
- Applies to: holiday seals / any twisted-dough or rope motif
- Status: pending

### Evidence

The pretzel was drawn as three stroked paths, not a filled silhouette:
a closed smooth loop for the ring plus two open arms crossing the middle,
each stroked three times (crust `#5E2E0C` at w+7, dough `#C88434` at w,
highlight at w*0.34) with round caps. Self-intersection is free with
strokes — the over/under twist reads automatically, and the same
three-layer stack gives a baked edge with no outline pass. Salt grains
are tiny rotated ellipses scattered on the dough only. First pass held
up; the only iteration was nudging the pretzel's centre ~12px toward the
stein so the two props touch and the lean reads.

The mini pretzel in the vermilion chop uses the same trick smaller:
one stroked ring + two crossing arm lines, all cream.

### Proposed change

Add to the holiday-seal notes in `prompts/`: for twisted or braided
foods (pretzels, knots, ropes, bread), stroke the medial axis at
crust/dough/highlight widths rather than modelling the silhouette —
self-crossing strokes carry the twist for free.
