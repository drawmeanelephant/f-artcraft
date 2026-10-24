## Dhole V1R00 — gallop legs need a joint, echo figures need a neck

- Kind: lesson
- Source: issue #1095; `work/animals/draw_dhole.py`,
  `art/animals/dhole/dhole-V1R00.*`
- Applies to: animals field plates; quadruped locomotion and background
  echo figures
- Status: pending

### Evidence

Proof `work/out/dhole-V1R00@2x.png`. First pass drew the four legs as
smooth tapered blobs hanging off a capsule body — at plate scale they read
as sausages, not a gallop. Re-drawn as `smooth()` polygons that kink once
at wrist/hock with a dark foot cap trailing at the tip, they read as
running legs. The eye wants exactly one bend per leg; two reads noodly,
zero reads sausage.

The "chorus line" echo is a dim packmate on the floor line, drawn as body
blob + raised neck-and-head wedge + ear nub + tail + three leg strokes,
all one flat dusk colour at 60% opacity. A first version merged the head
into the body and read as a small hippo — a background silhouette still
needs its neck drawn, even at 100pt total height.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: quadruped legs at
gallop — draw each leg as a closed polygon with a single hard bend
(wrist/hock) and let the foot be a separate dark cap; straight tapered
blobs never read as legs. Echo/chorus figures in silhouette still need
the neck joint articulated or they read as other species.
