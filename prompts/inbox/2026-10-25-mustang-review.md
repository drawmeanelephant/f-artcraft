## Mustang V1R00 — the gallop reads on silhouette, not detail

- Kind: analysis
- Source: issue #1519; `work/horse-breeds/draw_mustang.py`,
  `art/horse-breeds/mustang/mustang-V1R00.{vectorcraft,svg}`,
  proof `work/out/mustang-V1R00@2x.png`
- Applies to: the horse-breeds milestone cards (#1519–#1523) and any
  galloping subject on a plate
- Status: pending

### Evidence

First horse-breed card; chassis copied verbatim from
`draw_border_collie.py`. Two render-and-critique loops before shipping.

What worked:

- Suspended-gallop silhouette — all four hooves off the floor, fore
  pair reaching, hind pair trailing — reads instantly. The `leg()`
  helper (two perpendicular-offset segments, one hard joint) gives
  bent limbs without the sausage taper the grammar warns about.
- Dun primitive marks carry the breed on their own: dorsal stripe
  riding the topline, dark points at mane/tail/cannons/hooves.
- Mane as ONE heavy fall draped over the crest plus loose "fly"
  strokes beating past it sells "tangled, not groomed". Four parallel
  ribbons (first attempt) floated off the neck like streamers.
- Dust: three wide low-opacity puffs hugging the floor crest, plus one
  far flat-top mesa on the skyline — "dust and distance" for ~6 calls.

What failed and got fixed:

- A row of five equal dust ellipses looked like lily pads AND leaked
  past the rim on the right: ellipse corners, not centers, decide
  `check_rim`. Assert `on_disc` at `x ± w/2`, not at the centre.
- Two small mesas read as UFOs under the dust layer; one bigger
  flat-top butte at ≤45% opacity reads as distance.
- A throat edge that ends above the chest point leaves a background
  wedge between jaw and shoulder — dive the neck's lower edge to
  mid-chest so it overlaps the body's chest silhouette.

### Proposed change

Add to the milestone-card grammar at the next consolidation, as the
horse-breeds supplement: gallop = two-segment `leg()` + airborne
hooves + dust low on the floor; mane/tail = one mass rooted on the
crest/dock + fly strokes, never stacked ribbons. Destination
`prompts/series/` alongside the dog-breeds note.
