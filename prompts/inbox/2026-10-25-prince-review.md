## prince V1R00 — a raised arm needs taper and a cuff, not a pole

- Kind: lesson / analysis
- Source: issue #1543; `work/musicians/draw_prince.py`,
  `art/musicians/prince/prince-V1R00.{vectorcraft,svg}`,
  proof `work/out/prince-V1R00@2x.png`
- Applies to: milestone cards / gesture poses
- Status: pending

### Evidence

Two render-and-critique loops:

1. First raised arm was a near-constant-width vertical strip — read as
   a purple baseball bat with a ball on top, not an arm. Fix that
   worked: taper the sleeve (wide at shoulder, narrow at wrist), give
   the outer edge a soft elbow vertex, break the silhouette with a
   white shirt cuff at the wrist, and make the hand an unmistakable
   gesture — index finger extended straight up, two more finger ticks
   fanned. A bare blob hand on a pole reads as a ball; a pointing hand
   reads as a hand.
2. Swallow-tail points zigzagged into the coat's hem edge read
   instantly as a tailcoat at card scale — cheap and effective.
3. Ruffles as shallow scallop strokes (6-bump curves, spaced 34pt) on a
   cream wedge carry the ruffled-shirt read; deeper scallops would moiré.
4. Cloud guitar = lobed blob + one inner curl echo stroke + pale sheen.
   The lobed silhouette alone is ambiguous; the curl line inside is
   what makes it read "cloud" not "lump".

`check_rim` clean; `PURPLE RAIN · 1984` 339pt wide, clears ~65pt.

### Proposed change

For gesture poses: limb = tapered path with an elbow vertex + a
costume break at the wrist (cuff) + an unambiguous hand gesture.
Destination: milestone-cards note at next consolidation.
