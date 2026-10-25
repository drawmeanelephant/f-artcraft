## Galileo Galilei V1R00 — held props need a parametric axis, not guessed parts

- Kind: analysis
- Source: issue #1549; `work/scientists/draw_galileo_galilei.py`,
  `art/scientists/galileo-galilei/galileo-galilei-V1R00.{vectorcraft,svg}`,
  proof `work/out/galileo-galilei-V1R00@2x.png` (`check_rim.py`: clean)
- Applies to: scientist milestone cards; hand-held instruments
- Status: pending

### Evidence

Two loops.

- **A rotated instrument is one axis, never placed parts.** First pass
  built the telescope from `rot_rect_path` caps and stroked bands with
  hand-picked centres — every fitting drifted off the tube's axis and
  the prop read as floating debris. Fix: define the grip point `GA` and
  sky tip `GB` once, derive unit vectors along/across, and generate the
  tapered quad, band strokes, end caps and grip lines from `t` in
  [0,1]. Everything aligns by construction.
- **The millstone ruff is a cheap, high-yield signature:** one smooth
  ring mass + a dark throat ellipse + ~15 radial pleat strokes
  alternating light/dark reads instantly as the period collar.
- **A fist works when the prop explains it** (same lesson as Curie's
  vial): the grip blob plus two crossing knuckle strokes reads because
  the tube passes through it.
- The cratered moon is the easiest world cue in the series: pale radial
  disc + low-contrast crater rings + a wide faint halo, parked in the
  upper dark where the telescope points — the instrument's axis tells
  the story.
- Milestone `STARRY MESSENGER · 1610` in Source Sans 3, tracking 480 →
  489pt wide, 65pt clear of the rim.

### Proposed change

For the milestone grammar: *hand-held props are parametric — one
axis (grip→tip) and unit vectors, all fittings generated, never placed
by eye; the sky cue the prop points at sits on that same line of
sight.*
