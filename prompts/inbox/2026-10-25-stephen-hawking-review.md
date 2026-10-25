## Stephen Hawking V1R00 — silhouette card, head-tilt helper, event horizon

- Kind: lesson / analysis
- Source: issue #1557; `work/scientists/draw_stephen_hawking.py`,
  `art/scientists/stephen-hawking/stephen-hawking-V1R00.{vectorcraft,svg}`,
  proof `work/out/stephen-hawking-V1R00@2x.png`
- Applies to: scientists milestone series; profile/silhouette subjects
- Status: pending

### Evidence

First profile-figure card. Two loops. What the critique caught and what
worked:

- **A floating head reads broken; a tilted head reads Hawking.** First
  pass had an upright profile on a thin neck pushed forward of the
  headrest — looked disconnected. Rotating the whole head group −8°
  about a neck pivot produced the signature forward lean *and* closed the
  composition. `rot(p, deg, pivot)` + `rpts(pts, deg)` helpers transform
  every head feature uniformly; straight-segment strokes transform just
  their endpoints. Worth lifting into `vc.py` if more profiles ship.
- **Profile face = one lens.** A single glasses lens + a temple stroke to
  the ear reads instantly; do not draw the far lens.
- **Event-horizon recipe**: dark disc + tilted stroked ellipse
  (`ellipse_pts(cx,cy,rx,ry,deg)` parametric → `smooth()` closed) with a
  fatter low-opacity twin stroke behind it, plus one brighter "lensed
  arc" on the ring's lower-front leg. Cheap and reads as an accretion
  disk at 400pt.
- **Rim light carries "dignified, cosmic"**: 4–5 thin cyan strokes
  (#9FE8E0, 30–50%) on the head's back edge, shoulder, backrest rear,
  shin and wheel rear edge — all on the side facing the ring. Turns a
  flat dark figure into a lit silhouette without repainting fills.
- **Wheelchair anatomy that read at plate scale**: big spoked rear wheel
  (tire fill + rim + smaller handrim ring + 6 spokes + hub), small front
  caster, foot platform on a legrest strut, armrest with a tiny glowing
  control dot.
- Starfield discipline: every star `assert on_disc(x,y,6)`; 2–3 get a
  cross sparkle, the rest plain dots at 40–80%.

Watch: a forward-tilted head opens a gap between jaw and neck-top —
overlap the neck under the head's *back*-bottom edge, not the chin.

### Proposed change

For the consolidated milestone recipe (destination `prompts/series/`):
add a "profile silhouette" branch — when the brief names an iconic
posture, draw the figure profile, keep detail minimal inside the
silhouette, and spend the budget on rim light + one glowing world object.
Two reusable helpers candidate for `vc.py`: `rot/rpts` (point rotation)
and `ellipse_pts` (rotated-ellipse point list).
