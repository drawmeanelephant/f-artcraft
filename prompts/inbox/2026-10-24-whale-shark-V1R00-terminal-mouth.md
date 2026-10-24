## Whale shark V1R00 — terminal mouths live on the face, not under it

- Kind: analysis
- Source: issue #1049; `work/animals/draw_whale_shark.py`, `art/animals/whale-shark/whale-shark-V1R00.*`
- Applies to: animals field plates; fish anatomy; open-mouth poses
- Status: pending

### Evidence

Proof `work/out/whale-shark-V1R00@2x.png`. First pass drew the gape as a
scoop under the jawline (mouth corner low, chin dropping below the body
line) — it read as a hanging sac, not a filter-feeding head. The fix was
anatomy, not decoration: whale shark mouths are *terminal*. The head front
was rebuilt near-vertical and the mouth drawn as a dark crescent on that
front face, with a pale lip seam, two raker strokes inside, and the
plankton cloud centred dead ahead of the gape. Second pass reads at a
glance.

Working notes: the spot field is ~80 ellipse dots clipped by a body-mask
ellipse (`((x-470)/295)² + ((y-442)/78)² ≤ 1`) — staggered rows, jitter
±4, opacity 45–70. Rows beat random scatter; the grid is the biology.
Spots stay off the head front (they fade there in life). Remoras are a
two-stroke scale tell. A god-ray quad works fine as long as its top edge
seats inside `disc_top(x)`; feed swirls keep `on_disc(x,y,12)` per dot.

### Proposed change

For `prompts/series/20-field-plates.md`: when a mouth opens, check where
the species actually puts it — terminal (whale shark, guppy) lives on the
face silhouette, underslung (white shark, sturgeon) below it. Drawing the
wrong one makes the head sag. Also: dense particle clouds want a spiral
parameter (`t·1.6τ`, radius growing with index) plus a per-dot `on_disc`
assert — uniform scatter reads as noise, a spiral reads as food.
