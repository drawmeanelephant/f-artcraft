## Katherine Johnson V1R00 — full-length standing figure on the milestone chassis

- Kind: lesson / analysis
- Source: issue #1555; `work/scientists/draw_katherine_johnson.py`,
  `art/scientists/katherine-johnson/katherine-johnson-V1R00.{vectorcraft,svg}`,
  proof `work/out/katherine-johnson-V1R00@2x.png`
- Applies to: scientists milestone series; standing-figure cards generally
- Status: pending

### Evidence

First full-length figure in the scientist series (the first five cards are
all busts cropped on the arc). What worked and what it took:

- **A standing figure fits the chassis.** Crown ~y235, shoes on a floor
  band at `fy`=800 closed on the disc's arc (`rim_x(800)` leaves ~247pt
  of half-width for the stance). Total figure ~570pt reads naturally;
  the dog-breed "subject owns the lower two-thirds" rule transfers to
  people without change.
- **The chalkboard IS the plate.** Orbit arcs, a dotted transfer ellipse,
  a small stroked Earth and one ghosted SS3 conic formula (`x²/a² +
  y²/b² = 1`, opacity ~15) give the "equations are the backdrop texture"
  brief without a literal board rectangle that would fight the disc.
- **The chalk-in-hand gag pays for itself**: a short bright "Fresh chalk"
  stroke (opacity ~50) continuing the orbit arc's lower leg makes the
  raised arm read as mid-stroke, not waving.
- **Cat-eye glasses want smooth closed paths, not polygons.** First pass
  used straight-segment frames and rendered as hexagonal stop signs;
  `smooth()` pts with the outer corners ~6pt higher than the bridge gives
  the 1960s upsweep.
- **Sheaf-of-papers prop**: two rotated cream quads + three table-line
  strokes reads as hand-computed tables at plate scale; keep the hand
  blob overlapping the top edge so the grip reads.
- **Traps confirmed**: milestone line `ORBITAL MATH · 1962` contains
  digits — whole line in Source Sans 3 (precedent set by einstein/
  darwin/etc., who also set digit-bearing milestone lines in SS3, not
  Virelai). The `·` separator renders in SS3 too.

Open question for later cards: the peter-pan collar still reads slightly
bib-like at 56pt name scale; a true V-notch between two separate collar
wings may read better if another brief calls for it.

### Proposed change

Add "standing full-length variant" to the milestone-card recipe when it
next consolidates (destination `prompts/series/` milestone-cards note):
bust crop for portrait-icon subjects, full figure with floor band at
`fy`≈800 when the brief specifies a stance or action pose. Prop-in-hand
gags (chalk mid-stroke, held specimen) are the cheapest way to carry the
brief's verb.
