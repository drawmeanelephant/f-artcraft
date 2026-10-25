## cuban-trogon-V1R00 — colour-blocked bird needs overlapping zones, not islands

- Kind: lesson
- Source: issue #1135, `work/animals/draw_cuban_trogon.py`,
  `art/animals/cuban-trogon/cuban-trogon-V1R00.{vectorcraft,svg}`,
  proof `work/out/cuban-trogon-V1R00@2x.png`
- Applies to: field plates, multi-colour birds and patched plumage
- Status: pending

### Evidence

First proof put the grey bib, teal flank and red belly on as three
non-overlapping patches: a teal sliver survived between bib and belly and
the red read as a bean glued to the bird. Fix was to let the zones run
under each other — bib drawn over the upper front with a curved hem, red
patch drawn after and wide enough to span the whole lower abdomen so the
base colour never shows between them. That ordering, not the paths'
edges, is what made the plumage read as a bird.

Tail: the tocororo's flat blade wants three nearly parallel feathers,
not a fan. First pass spread the tips over ~115pt and the white tip
bands were cut wider than the feather ends — they read as dangling
tags. Pulling the tips to ~w-8pt and keeping the blades parallel fixed
the silhouette; the checkered white-on-dark underside survived.

### Proposed change

Add to `prompts/series/20-field-plates.md` animal notes: "Plumage colour
zones are overlapping regions, not tiling patches — draw each zone a
little too big and let the next one cover its edge. A gap of base colour
between zones reads as a stickered-on island."
