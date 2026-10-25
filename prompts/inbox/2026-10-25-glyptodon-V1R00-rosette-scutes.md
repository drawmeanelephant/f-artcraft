## Glyptodon V1R00 — tessellated dome and glow discipline

- Kind: analysis
- Source: issue #1140, `work/animals/draw_glyptodon.py`,
  `art/animals/glyptodon/glyptodon-V1R00.{vectorcraft,svg}`
- Applies to: field plates (animals), armoured subjects
- Status: pending

### Evidence

Scute tiling by concentric elliptical arcs (polar grid on the dome ellipse,
tile size growing toward the rim) reads convincingly as osteoderm pavement
at plate scale — each tile is a small gradient ellipse + boss dot, ~35
calls, worth it. Two failures caught by proof/checks: a radial-gradient
"dying sun" glow whose bounding ellipse crossed the left rim (soft-glow
ellipses leak past the disc just like hard shapes — keep the whole ellipse
inside, or clip), and a tail tip whose `smooth()` curve overshot its control
points below the disc bottom. Tails closing on smooth curves can overshoot
— pull tips ~20pt inside the rim.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: radial-gradient glows
have rectangular/elliptical bounds that count as geometry for the rim rule
— check them against the disc, not just their visible falloff.
