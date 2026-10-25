## Louis Armstrong V1R00 — raised arms join UNDER the torso; props touch the face

- Kind: analysis
- Source: issue #1532; `work/musicians/draw_louis_armstrong.py`,
  `art/musicians/louis-armstrong/louis-armstrong-V1R00.{vectorcraft,svg}`,
  proof `work/out/louis-armstrong-V1R00@2x.png`
- Applies to: musicians milestone series; figures with raised/prop arms
- Status: pending

### Evidence

Two render loops.

- **Paint sleeves before the torso.** First pass drew arms after the
  suit with their roots ending at the shoulder line — both arms printed
  as detached dark flippers floating beside the body. A sleeve is a
  tapering tube whose root extends ~30pt INSIDE the shoulder edge;
  drawing it first lets the torso silhouette swallow the root.
- **The mouthpiece must overlap the lip shape.** First pass left a ~20pt
  gap between mouth corner and mouthpiece — the horn read as hovering
  NEAR the face, not being played. Anchor the instrument axis on the
  mouth corner point and let it cover the lip edge by 5–8pt.
- **A rotated trumpet bell is a hand-built path.** `draw_shape` takes no
  rotate; `rot_ellipse(cx, cy, a, b, deg)` through `smooth()` gives a
  clean tilted mouth; the flare is a smooth() cone meeting it.
- **A grin is two shapes, not a stroke.** Dark mouth-interior blob +
  cream teeth band tucked under the top edge; closed-eye squints are
  upward arcs ~5pt. That trio reads "joy" at thumbnail size where a
  smile line reads as nothing.
- **1920s suit = shirt wedge + two lapel flaps + thin tie;** a pocket
  square tab on the chest is a cheap era cue.
- Footlight dots along the floor crest sell "stage" for ~10 calls.

### Proposed change

For the musicians note: raised-arm figures paint order is
sleeves→torso→prop→hands; prop axis anchored on its contact feature
(lip, chin, grip); expression beats need FILLED shapes (mouth interior,
teeth) — a stroked smile alone dies at card scale.
