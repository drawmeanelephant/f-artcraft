## Moose V1R00 — palmate antlers and profile wattles

- Kind: lesson
- Source: issue #1033; `work/animals/draw_moose.py`, `art/animals/moose/moose-V1R00.*`
- Applies to: animals field plates; antlered/horned subjects
- Status: pending

### Evidence

Proof `work/out/moose-V1R00@2x.png`. Two findings:

1. A palmate antler reads wrong if the palm is round. First pass gave a
   near-circular blade with tines only along the top — it rendered as a
   foam finger / crown floating over the poll. Fix: palm wider than tall
   (≈180×120), tines around the WHOLE outer rim (front brow tines, top
   tines, back-and-bottom trailing tines), and a beam at least ~40px thick
   leaving the poll. A second darker blade behind, shifted up-right ~50px,
   is enough to imply the pair without drawing the full spread.
2. The moose bell (dewlap) must be ONE flap. First pass grew wattle bumps
   out of the silhouette throat AND drew a separate bell path — the render
   showed two dangling strips fighting each other. Fix: keep the silhouette
   throat smooth and add a single narrow flap shape under it.

Also: lily pads / floating props near the bottom arc leak fast — at x≈240
the disc floor is already at y≈800, so on_disc asserts with pad≥20 are
mandatory for anything placed on the water/drift near the edges.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: palmate antlers are a
blade, not a circle — elongate the palm past the beam axis and ring the
outer edge with tines. Hanging appendages (bells, dewlaps, wattles) go in
ONE layer: either the silhouette grows them or a separate flap supplies
them, never both.
