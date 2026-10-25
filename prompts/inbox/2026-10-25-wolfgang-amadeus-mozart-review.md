## Mozart V1R00 — first human milestone card; face grammar + digit fix

- Kind: analysis
- Source: issue #1530; `work/musicians/draw_wolfgang_amadeus_mozart.py`,
  `art/musicians/wolfgang-amadeus-mozart/wolfgang-amadeus-mozart-V1R00.{vectorcraft,svg}`,
  proof `work/out/wolfgang-amadeus-mozart-V1R00@2x.png`
- Applies to: musicians milestone series; any human-figure plate; all
  milestone lines containing years
- Status: pending

### Evidence

First card of the musicians wave — the chassis carries over verbatim,
the subject type needed new answers:

- **Half-figure bust is the right crop.** Seated at a desk floor chord
  (fy 790), torso widening to the desk, head+wig in the disc's centre.
  Portrait grammar from animals transfers: face slightly off-axis, gaze
  on the work, not the camera.
- **Powdered wig = cap + side-roll stack + queue.** Crown is one closed
  shape over the skull's top half; rolls are 3 stacked horizontal
  ellipses hugging each cheek — NOT across the face. First pass placed
  them at cheek height crossing the eyes and they read as spectacles;
  they must sit outside the head silhouette's eye line.
- **Neck must nearly vanish.** A 60pt visible neck reads as a gooseneck
  on a child; ~35pt mostly hidden by the jabot is right.
- **Hands: one clean mitten.** Finger squiggle strokes (3 × 2.5pt)
  printed as scribbles at card scale — deleted for a single closed hand
  shape plus one knuckle accent line.
- **Virelai Sans digit gotcha is real and now scripted:** milestone
  `REQUIEM · 1791` keeps one centered text object; the year range gets
  `text.setRangeStyle font="Source Sans 3"` (byte offsets via
  `len(line[:idx].encode())` — the `·` is 2 bytes). Renders visibly
  tighter than letting fallback pick.
- **check_rim caught a desk-prop leak** (manuscript corner at r432);
  desk props want `assert on_disc(corner, 6)` per sheet corner, not just
  centre checks — tilted quads leak at corners.

### Proposed change

Musicians series recipe: field-plate chassis + half-figure bust on a
world floor, one signature prop held (instrument/quill), one signature
worn trait (wig/gardenia/suit), world cue on the floor chord. Destination
`prompts/series/` milestone-cards note at next consolidation.
`text.setRangeStyle` for digit runs belongs in the shared caption
boilerplate of every `WORK · YEAR` card.
