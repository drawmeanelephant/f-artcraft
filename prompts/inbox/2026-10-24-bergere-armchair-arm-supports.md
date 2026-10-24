## bergere-armchair-V1R00 — far-side arm support is a silhouette problem

- Kind: lesson
- Source: issue #1152, driver `work/furniture/draw_bergere_armchair.py`,
  native + proof `art/furniture/bergere-armchair/`
- Applies to: furniture field plates; any piece with protruding arm pads or rails
- Status: pending

### Evidence

First proofs had the manchette (arm pad) as a flat slab: at 26deg yaw it read
as a diving board, and the far pad's front end floated with nothing under it.
Three fixes were tried in order: (1) an S-scroll console at the pad's outer
x-plane rendered as a detached gold hook past the chair's silhouette;
(2) a rounded front cap face on the pad rendered as a protruding pink pill —
the z-facing cap projects as a wide slab at three-quarter yaw; (3) winner —
draw the console *inboard* (x aligned near the side-panel plane) so only a
dark curl peeks under the pad front, and give the pad a crowned top edge plus
a separate top-strip face. Supported mass, no floating parts.

What survives critique: clipped hex weave (Cyrus-Beck on a convex polygon)
works for non-elliptical cane panels — the arched back panel took weave with
no special casing. The serpentine apron + shell cartouche + cabriole legs read
immediately as Louis XV. Wobble left: far pad still borders on a flag read;
a real front cap probably wants a smaller, tilted face rather than a full
rounded-rect slab.

### Proposed change

For `prompts/` consolidation: on three-quarter plates, every protruding
element needs a visible support path to the body — a thin scroll drawn
inboard reads better than an accurate one drawn at the true outer plane,
because the outer-plane version detaches at the silhouette edge.
