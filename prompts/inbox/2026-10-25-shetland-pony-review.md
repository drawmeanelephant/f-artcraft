## Shetland pony V1R00 — pony reads through proportion, not size

- Kind: analysis
- Source: issue #1521; `work/horse-breeds/draw_shetland_pony.py`,
  `art/horse-breeds/shetland-pony/shetland-pony-V1R00.{vectorcraft,svg}`,
  proof `work/out/shetland-pony-V1R00@2x.png`
- Applies to: horse-breeds milestone cards; pony/stocky subjects
- Status: pending

### Evidence

One render-and-critique loop before shipping (eye buried under the
forelock; moved to peek out at its hem — the intended breed look).

What worked:

- Pony proportion at plate scale: barrel drawn nearly circular and
  deep (belly ~y650), legs SHORT and thick with only ~140pt of leg
  below the barrel. A horse-shaped body with short thick legs reads
  "pony" instantly; a small horse-shaped everything reads "foal".
- Wind told three ways and all cheap: mane/forelock/tail all combed
  in one direction, thin wind strokes across the disc, head carried
  low into it.
- Forelock as a heavy curtain over the brow with the eye peeking at
  the hem reads more Shetland than any tidy parting would.
- Shaggy coat = ragged belly-edge ticks at 60% opacity, not a furry
  outline. Fur on the silhouette edge would muddy it.

Watch for:

- On a dark-coated animal under a dark mane, place the eye at the
  mane's boundary — half-shadowed — rather than fully inside or fully
  outside; inside it disappears, outside it floats in empty face.
- Short legs mean hooves cluster: keep near/far pairs a few px apart
  or they merge into one boot.

### Proposed change

Add to the horse-breeds card note at consolidation: pony = deep
barrel + short thick legs + low head; forelock curtains the face with
the eye at its hem. No structural divergence from the card grammar.
