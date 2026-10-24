## Sarchi folding rocker V1R00 — a sling reads by zones, not one screen-y gradient

- Kind: lesson / analysis
- Source: issue #1109, `work/furniture/sarchi-folding-rocker-V1R00.py`,
  `art/furniture/sarchi-folding-rocker/sarchi-folding-rocker-V1R00.*`
- Applies to: furniture field plates; any draped/slung surface
- Status: pending

### Evidence

The leather is one parametric sling (front lip bar → seat dip → back top),
but it only became legible when drawn as **two surfaces with separate
gradients**: a lighter amber back panel and a mid-amber seat, overlapped
~6% at the bend. A single screen-y gradient over the whole sling put the
seat pan in the gradient's dark tail — the seat vanished against the
backdrop and the piece read as a frame missing its fabric. Also: pale
"light" lambert strips over a dark-seat region read as translucent gauze,
not lit leather — cut them rather than brighten.

Form notes that sold "folding rocker, not generic rocker": the two long
members per side actually cross at a visible bolted pivot (draw the bolt
big, ≥9pt radius, with a glint); feet land on an upturned runner; both
runners share one model ground plane — their projected contacts differ by
perspective, which is correct and worth asserting in the script rather
than eyeballing.

### Proposed change

For `prompts/series/20-field-plates.md` furniture notes: "Slung surfaces
(slings, hammock seats, leather panels): give seat and back zones their own
gradients drawn as overlapping surfaces — one screen-space gradient across
a folded surface strands the fold's dark side in the tail stop."
