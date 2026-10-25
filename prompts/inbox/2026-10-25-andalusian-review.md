## Andalusian V1R00 — collected gait on the single-silhouette recipe

- Kind: analysis
- Source: issue #1524; `work/horse-breeds/draw_andalusian.py`,
  `art/horse-breeds/andalusian/andalusian-V1R00.{vectorcraft,svg}`,
  proof `work/out/andalusian-V1R00@2x.png`
- Applies to: horse-breeds milestone cards; baroque/gaited quadrupeds
- Status: pending

### Evidence

Shipped after two render-and-critique loops. Built on the appaloosa
single-silhouette chassis plus the friesian `leg()` helper.

What worked:

- The collected canter reads on three decisions: near fore drawn with
  the friesian fold (top inside the chest, joint tucked back to
  ~(510,546), hoof hanging at ~y615), far hind lifted under the belly
  with bent hock, and the face carried near-vertical with the muzzle
  tucked so the chin underside shows. Croup stays high; the gait reads
  "up", not "forward".
- First pass let the thick wavy mane hang to ~y522 and it consumed the
  whole neck — head grew straight out of a dark column. Pulling the
  hem up to ~y470 with a scalloped edge (alternate tip/notch points)
  left ~40pt of neck face showing and the mass still reads heavy.
- Grey-on-amber is a good pairing: light warm-silver coat ramp over an
  ochre plate pops without any rim light, and the dark charcoal mane
  gives the contrast the pale coat loses.
- Baroque build = crest peaking ~10pt above the poll + deep barrel +
  compact back, not bigger size.

Survives critique as V1R00 with residue: the two forelegs still make a
stiff K at the chest (one more bend at the raised leg's pastern would
soften it); the muzzle tip is a touch squared; the sierra skyline is
nearly invisible — either commit to it or drop it next revision.

### Proposed change

For the horse-breeds card note at consolidation: *a heavy mane must
keep ~40pt of neck face below its scalloped hem — let it reach the
chest and the head reads hooded;* and *collected gaits = raised fore
with tucked-back fold + diagonal hind lifted under the belly + the
chin underside showing.* No structural divergence.
