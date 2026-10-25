## Tu Youyou V1R00 — hero-prop sprig, warm plate, two lapels trap

- Kind: lesson / analysis
- Source: issue #1556; `work/scientists/draw_tu_youyou.py`,
  `art/scientists/tu-youyou/tu-youyou-V1R00.{vectorcraft,svg}`,
  proof `work/out/tu-youyou-V1R00@2x.png`
- Applies to: scientists milestone series; prop-forward portraits
- Status: pending

### Evidence

Second standing/behind-bench card. Two loops to ship. What the critique
caught:

- **Two symmetric rounded lapel shapes read as a bow or petals**, not a
  collar. First pass drew two wide smooth "wings" flanking the garment V
  and the render showed a bow-tie flower at the throat. Fix that survived:
  one slim collar band across the neck + two thin `Lapel edge` strokes
  hugging the V. Wide pale shapes near the face always read as objects,
  not tailoring.
- **Long-sleeve arms must reach their hands.** The bench-resting hand
  shipped orphaned until the sleeve was extended to the wrist — a hand on
  a floor/bench band needs its arm drawn to the cuff, even when the band
  is drawn later.
- **Hero-prop scale trick**: the qinghao sprig is drawn ~1.5× real size
  rising beside the face with a faint warm halo disc behind the tip
  (`rad` stop opacity 20→0). Leaf = pointed-oval `smooth()` lens from a
  `leaf(bx,by,tx,ty,w)` helper; alternate left/right along a stroked
  stem; three tiny bud circles sell "sweet wormwood" over generic leaf.
- **Warm palette swap works**: plate `rad #7E7A54→#4E5034→#202217` +
  `#F2E4BC` light pool + warm dust lenses gives "modest lab, warm light"
  without leaving the moody grammar. Mortar & pestle is the on-theme
  dead-dark prop (the extraction), kept ≤ flask-size so it doesn't rival
  the sprig.
- Confirmed again: digit-bearing milestone (`ARTEMISININ · 1972`) goes
  entirely in Source Sans 3; `TU YOUYOU` at 60pt Virelai suits the short
  name.

### Proposed change

For the consolidated milestone-card recipe (destination
`prompts/series/`): when the brief names a hero prop, scale it up and
give it the card's only bright accent; every other prop stays dead-dark
on the bench/floor band. And a tailoring rule: collar = one band shape +
edge strokes, never two symmetric filled wings.
