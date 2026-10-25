## Standard poodle V1R00 — clip contrast carries the likeness

- Kind: analysis
- Source: issue #1509; `work/dog-breeds/draw_standard_poodle.py`,
  `art/dog-breeds/standard-poodle/standard-poodle-V1R00.{vectorcraft,svg}`,
  proof `work/out/standard-poodle-V1R00@2x.png`
- Applies to: dog-breeds milestone cards; any clipped/sculpted-coat subject
- Status: pending

### Evidence

Continental clip in profile, apricot on a slate disc. Three render-and-
critique loops. What worked: the clip contrast — pale `CLIP_GRAD` shaved
muzzle/barrel/legs vs the deeper `COAT_GRAD` fluff — makes the cut read
before any curl tick does. The `puff()` helper (10-point blob, alternating
radii, smoothed) gives passable rosettes for topknot, ear, hip patch,
bracelets and tail pom. Shed comma-curls on the carpet are a cheap
breed-world accent that sits inside the floor grammar.

What didn't: the first pass hid the neck behind the ear leather — the ear
must hang over the *crest*, not the neck front, or the long-neck read
collapses into "hat + blob". Moved it ~15px right; the neck front now runs
chin-to-brisket unbroken. The hind leg still reads slightly sausage;
splitting it into thigh + gaskin pieces helped but the hock bend is subtle
at plate scale. Topknot tilts a touch forward like a cap — next revision
could rotate the puff seed or bias it back over the poll.

Survives its critique as V1R00: recognizable continental clip, elegant
not froufrou, rim clean, milestone clears by 69pt.

### Proposed change

For sculpted-coat breeds: spend the silhouette budget on the *shaved*
shapes and let one fluff color cover all rosettes; and place ear leather
behind the neck line when a long neck is the point. Candidate fold-in to
the milestone-cards grammar note at consolidation.
