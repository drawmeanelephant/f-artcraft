## Hermit crab V1R00 — making the borrowed shell read

- Kind: analysis
- Source: issue #1139, `work/animals/draw_hermit_crab.py`,
  `art/animals/hermit-crab/hermit-crab-V1R00.{vectorcraft,svg}`
- Applies to: field plates (animals), shell/carapace subjects
- Status: pending

### Evidence

First pass drew the whelk as a single smooth teardrop — the proof read as a
leaf or seed pod, not a shell. What fixed the read: a short stepped spire
nub tilted off the dome, suture shadow-strokes under the spire, and five
thin growth bands arcing across the body whorl (fewer fat bands read as
stripes; many thin arcs read as shell growth). Two little barnacles on the
dome sold "borrowed, old". Also: scattered decor near the disc edge needs
an `on_disc` assert — two pebbles sat past r420 on the backdrop and only
`check_rim.py` caught them.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: small decor flecks
(stones, pebbles, motes) need a radial assert against the plate centre —
they are easy to scatter past the rim in the lower corners.
