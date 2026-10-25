## Ada Lovelace V1R00 — ringlets are one mass, not a bead column

- Kind: analysis
- Source: issue #1551; `work/scientists/draw_ada_lovelace.py`,
  `art/scientists/ada-lovelace/ada-lovelace-V1R00.{vectorcraft,svg}`,
  proof `work/out/ada-lovelace-V1R00@2x.png` (`check_rim.py`: clean)
- Applies to: scientist milestone cards; period hair, chained props
- Status: pending

### Evidence

Two loops.

- **Sausage curls want a wavy strip, not stacked circles.** First pass
  placed four separate ellipses beside each cheek — they floated off the
  hair mass and read as beads or buttons. Fix: one smooth lumpy mass per
  side (outer bulge / inner waist alternating), touching both the hair
  cap and the cheek edge, with 3 short C-strokes inside as separations.
- **A chain prop is a curve + sampling, not placed parts** (same lesson
  as Galileo's telescope axis). Punched cards laid along a quadratic
  bezier every ~33px via `rot_rect_path`, tangent-rotated, with 3 punch
  dots offset along the card's own axis — the sag between the hands is
  parametric so the drape stays smooth.
- **Fists grip better when set a step *into* the curve** (`t`≈0.05/0.95),
  not at the exact endpoints — the chain visibly enters the grip.
- **Downcast eyes sell "studying":** closed lid arcs + two short lash
  strokes, no open eye — a cheaper, stronger read than angling pupils.
- Faint gear rings (ring + hub + 12 tick teeth, ~15% opacity) are enough
  to put the engine in the dark behind her.
- Milestone `FIRST ALGORITHM · 1843` in Source Sans 3, tracking 480 →
  457pt wide, 65pt clear of the rim.

### Proposed change

For the milestone grammar: *period hair signatures (ringlets, periwig
masses) are continuous silhouette masses with internal separations —
never stacks of detached circles.* Destination: the scientist/milestone
card note at the next consolidation.
