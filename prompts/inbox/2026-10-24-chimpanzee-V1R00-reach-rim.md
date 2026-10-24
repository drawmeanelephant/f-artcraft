## Chimpanzee V1R00 — strokes reach the rim, polygons leak

- Kind: lesson
- Source: issue #1034; `work/animals/draw_chimpanzee.py`, `art/animals/chimpanzee/chimpanzee-V1R00.*`
- Applies to: animals field plates; any plate using canopy/light entering from off-plate
- Status: pending

### Evidence

Proof `work/out/chimpanzee-V1R00@2x.png`. Two structural findings:

1. Filled light-shaft polygons that start above the disc (y<64 at x≈640)
   painted straight over the rim onto the backdrop — the plate rim stroke
   is 6px and cannot hide a big translucent shape. Same for the fig limb:
   a 14px branch crossing the rim left a stub outside the disc. Fix: enter
   canopy decor as stroked paths whose caps START inside r≈400 — a round
   cap at opacity ≤10 reads as haze, not a leak; a hard polygon edge reads
   as a spill.
2. A bent limb (shoulder → elbow → wrist) is much easier as one stroked
   path with `cap: "round"` and a deliberate cusp at the elbow than as a
   filled silhouette — the arm under the chimp needed the elbow LOW and
   the wrist back UP at face height; a single cubic through those three
   points with strokeWidth ~50 gave the whole limb. Hands then attach as
   small closed shapes at the wrist, with the held object drawn last.

What worked first try: lobed fig leaves from a parametric `figleaf(x,y,s)`
— a stem point plus three lobed beziers — and hanging figs on 2.5px stems
directly under the limb give instant "fig-tree mood" for very little code.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: nothing enters the
plate across the rim — canopy, shafts and branches start INSIDE r≈400;
the rim stroke is a finishing edge, not a clip. Multi-segment limbs are
stroked paths (round cap, elbow cusp allowed) — filled limb outlines are
only needed where the limb must taper.
