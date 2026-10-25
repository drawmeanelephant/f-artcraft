## Dalmatian V1R00 — spots want a helper that still takes a hand-placed centre

- Kind: analysis
- Source: issue #1507; `work/dog-breeds/draw_dalmatian.py`,
  `art/dog-breeds/dalmatian/dalmatian-V1R00.{vectorcraft,svg}`,
  proof `work/out/dalmatian-V1R00@2x.png`
- Applies to: dog-breeds milestone series; spotted/patched coats
- Status: pending

### Evidence

Two render loops. The brief's "individually placed, never a texture
fill" survived as a `spot(cx, cy, w, h)` helper that builds ONE
six-point irregular blob per call — same generator, different centre
and size per spot, so placement is authored but no two spots share a
silhouette. ~24 spots read correctly across body, legs and face; the
face spots matter most for the breed read.

The white-coat-on-plate problem is solved by plate choice, not
outlining: dusk-stone green-grey radial (#AAB0A0 → #3A443C) gives the
cream gradient room to glow; the dog's ink stroke (5–6) plus a bright
topline sheen stroke carries the edge against the light plate centre.
Trot gait reads via the diagonal pair — near fore reaching, far fore
planted near-vertical; drawing BOTH forelegs forward slanted merged
them into a stretch. The stop furrow wants ≤30% opacity — at 50 it
prints as a stray scratch over the skull.

### Proposed change

For spotted breeds: plate mid-tone value should sit at least two value
steps below the lightest coat stop, and spot placement lists belong in
the driver as literal tuples — hand-auditable, which is the point of
the "no texture fill" rule. Milestone-cards note candidate.
