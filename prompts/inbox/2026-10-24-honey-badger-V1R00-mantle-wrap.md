## Honey badger V1R00 — the mantle is a drape, not a decal

- Kind: analysis
- Source: issue #1041; `work/animals/draw_honey_badger.py`, `art/animals/honey-badger/honey-badger-V1R00.*`
- Applies to: animals field plates; two-tone coats (saddle/mantle species)
- Status: pending

### Evidence

Proof `work/out/honey-badger-V1R00@2x.png`. Low-slung profile walking right,
pale saddle over black everything-else, pale digging claws on the near
forepaw, flat-top acacia with a hanging log hive (and bees) behind it —
the hive joke lands small, which is right.

What failed first: the mantle drawn as a closed capsule floating above the
body read as a white tube strapped to a black submarine. The fix was to
share the body's own topline as the mantle's top edge — the saddle is the
same silhouette, only its lower edge is new, and a few ragged fray strokes
soften the parting line. Second failure: the ear drawn as a pale nub
breaking the crown line rendered as a ball on a stalk — the ear-seating
rule again, and the honest fix was near-deletion (a crease inside the
line); honey badger ears are famously vestigial anyway. Third: a blunt
tiny head reads "slug with a nub" — ratels need the broad forehead and
heavy jaw merged into the body silhouette, head ~15% of length.

### Proposed change

For `prompts/series/20-field-plates.md`: on saddle-marked species, build
the pale coat as a drape sharing the subject's topline — never an
independent shape hovering over it. Ears that are vestigial in life earn
a crease, not a bump.
