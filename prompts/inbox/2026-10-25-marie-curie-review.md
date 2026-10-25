## Marie Curie V1R00 — first human card: hide the hands, cut the hood

- Kind: analysis
- Source: issue #1545; `work/scientists/draw_marie_curie.py`,
  `art/scientists/marie-curie/marie-curie-V1R00.{vectorcraft,svg}`,
  proof `work/out/marie-curie-V1R00@2x.png` (`check_rim.py`: clean)
- Applies to: scientist milestone cards; any human portrait bust
- Status: pending

### Evidence

Three render-and-critique loops on the first human subject in the
series. What the loops taught:

- **A bust does not need the wild-dog arc-close if a foreground band
  covers its bottom.** The dark bench is the floor band (`fy`≈795,
  `A420,420` close); the torso silhouette just extends a flat bottom
  edge ~25pt under the crest and the bench hides it. Simpler than
  arc-closing the figure itself — but only because a prop covers the
  seam.
- **Hair pulled up must END at the temples.** First draft ran the hair
  silhouette down both sides of the face to jaw level and under the
  chin — rendered as a nun's wimple, not piled hair. Cutting the side
  masses off at mid-cheek (~y450 for a face ending ~y510) restored the
  updo; the face's own jaw provides the lower outline.
- **Small skin-tone ovals read as eggs, not hands.** Two attempts at a
  resting hand on the bench — upright fist blob, then flat palm blob —
  both read as a tan egg/soap bar at ~40pt scale. The winning move was
  subtraction: the forearm disappears behind the bench edge, no hand
  shown. A hand at this scale only survives when a prop explains it —
  the raised fist works because the vial sticks out of it.
- **An arm drawn as a separate outlined shape on the torso reads as a
  bag.** The hanging arm only read once it became a bulge in the
  dress's own outline plus one seam stroke — no separate silhouette.
- **Disc decor near the face pareidolises.** Two mist lenses drifting
  over the hair rendered as a second pair of eyes. Keep an exclusion
  zone around the face: no symmetric light ellipses within ~120pt of
  the head.
- The glow discipline held: one radial halo + tight halo + the liquid
  column are the only accents above ~50% luminance besides the face;
  bench props stay dead-dark silhouettes so they can't compete.

### Proposed change

For the milestone-card grammar note: *human busts crop under a
foreground floor band, hands hide unless a prop explains them, hair
ends at the temples, and decor keeps an exclusion zone around the
face.* Destination `prompts/series/` scientist/milestone note at the
next consolidation.
