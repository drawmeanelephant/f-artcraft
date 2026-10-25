## Nikola Tesla V1R00 — soft glow ellipses are rim-leak vectors too

- Kind: analysis
- Source: issue #1550; `work/scientists/draw_nikola_tesla.py`,
  `art/scientists/nikola-tesla/nikola-tesla-V1R00.{vectorcraft,svg}`,
  proof `work/out/nikola-tesla-V1R00@2x.png` (`check_rim.py`: clean)
- Applies to: scientist milestone cards; any piece with a light-source halo
- Status: pending

### Evidence

Three loops.

- **Glow needs the same on_disc budget as solid decor.** First pass put a
  500x460 "arc wash" and a 300px floor-glow ellipse under the coil — 15,933
  rim-leak pixels, almost all soft halo, plus the plinth's bottom corner.
  Hard shapes get checked with `on_disc` asserts; the translucent washes
  were placed by eye. Fix: shrink every glow until its bbox corners
  satisfy `rim_x`/`hypot`, or centre it deeper inside the plate. A 16%
  wash reads identical inside the disc as outside it — there is no
  visual argument for letting it cross.
- **A contained Tesla coil reads with three parts only:** vertical
  secondary (tapered cylinder + diagonal winding strokes, alternating
  copper/dark every third turn), a toroid terminal (two stacked
  ellipses: gradient donut + dark hole), and 2-3 jagged `zig()` polylines
  drawn twice — 9pt halo stroke at ~22% under a 3.5pt near-white core.
  No crackle field, no storm: the brief asked for contained.
- **The discharge target earns the arcs.** A small ball on a thin stand
  gives the zigzags somewhere to land; arcs with no target read as
  decoration noise.
- **Tesla likeness levers that worked:** high forehead exposed by a
  slicked-back hair band, a *thin* lip-width moustache bar (the first,
  wider version read as a cigar), deep-set eye-shade strokes under the
  brows, and iris placement shifted toward the coil so the gaze tells
  the story. Blue glint dots (#D8F0FF) in the eyes tie face to arc light.
- Milestone `ALTERNATING CURRENT · 1888` in Source Sans 3, tracking 460
  → 541pt wide, 65pt clear of the rim.

### Proposed change

For the milestone grammar: *light-source halos and floor glows are decor
— assert their bbox extremes with `on_disc`/`rim_x` exactly like solid
shapes; a translucent ellipse past the rim fails `check_rim` the same as
an opaque one.* Destination: the scientist/milestone card note at the
next consolidation.
