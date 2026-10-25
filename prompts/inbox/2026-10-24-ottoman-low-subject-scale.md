## ottoman-V1R00 — low subjects need design height, not just zoom

- Kind: lesson
- Source: issue #1155, driver `work/furniture/draw_ottoman.py`,
  native + proof `art/furniture/ottoman/`
- Applies to: furniture field plates; low-profile subjects (footstools,
  trays, lowboys)
- Status: pending

### Evidence

First pass modelled a floor-hugging upholstered box on bun feet: honest to
the object but it occupied only the bottom quarter of the disc and read as
a toy chest. Zooming the projection was capped by the rim (the piece is
wider than it is tall, so the far corner hits the arc first). The fix that
survived critique was designing height into the subject: turned walnut
legs (a (y,halfwidth) profile + smooth silhouette, same trick as the
ladderback posts) lift the box, plus a global GS scale factor inside the
projector and a modest raise in body height. A hardcover book on the crown
carries the "doubles as everything" line and gives the top a focal accent
among the button tufts.

Working bits worth keeping: nailhead course as a row of small radial
brass dots parametrised along a 3D edge; page block drawn as two cream
faces + three page-line strokes reads as a real book at plate scale.

### Proposed change

For `prompts/` consolidation: for low-wide furniture, budget a leg or
prop storey — bun-foot cubes leave the top half of the disc empty and the
rim check, not composition, becomes the scaling limit.
