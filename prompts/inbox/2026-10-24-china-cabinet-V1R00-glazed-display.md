## China cabinet V1R00 — glazed display wants a *pale* interior and fat mullions

- Kind: lesson
- Source: #1198, `work/furniture/draw_china_cabinet.py`, `art/furniture/china-cabinet/china-cabinet-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates (glazed case pieces, vitrines, bookcases)
- Status: pending

### Evidence

Porcelain reads through glazing when three things stack in the right order:
a pale fabric-lined display back (`#D9C9A2` ramp, not the carcass wood),
contents drawn at full opacity, and glass as a gradient sheet with
per-stop opacity ~10–22 — not an object-level `opacity` call. Mullions are
drawn *over* the glass; the diagonal sheen lines go over the mullions last,
because the reflection lives on the glass surface, not behind it.

Upright plates are just circles in the x-y plane — the oblique projection
turns them into tilted discs for free, and a second smaller stroked ring in
cobalt sells "china" in one stroke. Dishes rest on a shelf when centre =
shelf_y + r + ~1, not shelf + r + gap.

The astragal grid (1 vertical + 2 horizontal bars per door, ~6 model units
≈ 10pt) holds at @2x and keeps twelve panes legible. A stepped block
pediment on the cornice gives the silhouette its heirloom crown for cheap.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Glazed
cabinets: pale lined back + full-opacity contents + 10–22% glass gradient;
mullions over glass, sheen over mullions. Plates are circles in the front
plane; a cobalt rim ring reads as porcelain." A proposal does not override
current house rules.
