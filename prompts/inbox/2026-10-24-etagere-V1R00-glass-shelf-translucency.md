## Etagere V1R00 — glass shelves need opacity in the gradient stops, not the object

- Kind: lesson
- Source: issue #1221, `work/furniture/draw_etagere.py`,
  `art/furniture/etagere/etagere-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — furniture (glass, tall narrow subjects)
- Status: pending

### Evidence

A glass shelf reads when the sheet carries per-stop translucency
(~0.22–0.34 alpha through the gradient) plus a bright front-edge stroke
at ~60% — the eye keys on the lit edge, and the brass perimeter frame
gives the glass something to sit in. Drawing order for a tower: far
posts, then shelves and their objects bottom-up, then near posts — the
front pair must overpaint the shelf front edges or the frame floats in
front of nothing.

Small props each needed their own cheat: a vase is two stacked
`cylinder()` calls (belly + neck), not one — a straight cylinder reads
as a canister. A globe is a radial-gradient sphere, two low-opacity land
blobs and one swept meridian arc in gold. A bust survives at 23pt tall if
it keeps a plinth + shoulders + head silhouette. Collar rings on the
posts at each shelf line (tiny horizontal ellipses) sell the joinery.

### Proposed change

Furniture note candidate: "Translucent furniture parts: gradient-stop
opacity, bright near edge, and a rigid frame around the pane. For post
furniture, collars at the crossbars read as real joinery and cost four
ellipses." Pending until consolidated.
