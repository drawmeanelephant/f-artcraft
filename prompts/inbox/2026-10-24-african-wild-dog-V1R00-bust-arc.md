## African wild dog V1R00 — portrait busts close on the arc too

- Kind: lesson
- Source: issue #1065, `work/animals/draw_african_wild_dog.py`,
  `art/animals/african-wild-dog/african-wild-dog-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — animal portraits
- Status: pending

### Evidence

First draft ended the chest and shoulder patches on a straight bottom edge at
y868. At that depth the disc is only ~200pt wide, so the shoulders leaked
~150pt past each rim. Fix: treat the whole bust like the floor — one
silhouette whose left/right sides land on the disc edge at a chosen y (here
y800, intercepts x253.4/746.6) and whose bottom closes with the same
`A420,420 0 0 1` arc the floor uses. Interior patches (cream bib, blotches)
then only need to stay inside their own smaller bounds; the bib tip at
(500,874) sits 4pt inside the rim, which the 6pt rim stroke then mows
cleanly. Ears: a painted wolf's round ears read "teddy bear" the moment the
inner ear is a concentric circle — dropping the inner cup low and off-centre
fixed it without changing the outer silhouette.

### Proposed change

Add to the field-plates known traps: *portrait busts reaching the rim must
close on the disc's own arc, same rule as floors — a flat bottom edge below
~y840 is a guaranteed leak.* Destination: `prompts/series/20-field-plates.md`.
