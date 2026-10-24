## Scarlet macaw V1R00 — cling pose and banded single-path wings

- Kind: analysis
- Source: issue #1048; `work/animals/draw_scarlet_macaw.py`, `art/animals/scarlet-macaw/scarlet-macaw-V1R00.*`
- Applies to: animals field plates; birds; parrot/macaw plumage
- Status: pending

### Evidence

Proof `work/out/scarlet-macaw-V1R00@2x.png`. The clay-lick composition works:
the bird clings upright on the bank face, bill planted in a peck pit, long
tail braced down the clay — a pose no perched plate could fake. The wing is
one silhouette with a single linear gradient along its axis carrying hard
stop transitions (red → yellow → blue at offsets 0.48/0.74); that one call
does the whole signature macaw wing and keeps the colour breaks where a
folded wing actually breaks.

Working notes: bare-skin face patch needs the fine red feather tracks
(4 strokes, 2pt, opacity ~70) or the white reads as a wound. Strata lines
on the bank face are the rim-leak trap — below y≈780 the disc half-width
collapses fast (208pt at y=824); every seam endpoint must be re-checked
against `rim_x`, not estimated. Two render passes were needed: first pass
leaked the damp seam past the rim below the disc. Distant macaws only read
as birds with a filled body blob + separate wing arc + tail streak; two
bare strokes read as scratches.

### Proposed change

For `prompts/series/20-field-plates.md`: multi-colour plumage zones
(macaw wing bands, pheasant saddles) can be one path with hard gradient
stops — pair the stops tightly (0.48/0.50) rather than drawing per-zone
shapes. And a behaviour note: for animals with a signature behaviour
(clay-lick clinging, ant-eating, pouch-peeking) the pose IS the plate;
choose it before the palette.
