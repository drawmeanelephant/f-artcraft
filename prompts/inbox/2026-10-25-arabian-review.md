## Arabian V1R00 — horses want ONE silhouette, not stacked stroked parts

- Kind: analysis
- Source: issue #1514; `work/horse-breeds/draw_arabian.py`,
  `art/horse-breeds/arabian/arabian-V1R00.{vectorcraft,svg}`,
  proof `work/out/arabian-V1R00@2x.png`
- Applies to: milestone cards, horse breeds, field plates — quadrupeds
  whose anatomy reads through clean lines
- Status: pending

### Evidence

Shipped after four render-and-critique loops. The first three passes
built the horse the way the dog cards build a dog — body, neck and head
as separate stroked shapes overlapping — and every pass read as llama or
antelope: each stroked seam drew a visible interior line that broke the
mass into segments, and the thin upright neck plus tubular body carried
no equine code. The fix was the bactrian camel's construction: ONE
silhouette path from muzzle tip up the dished face, over the poll, down
the arched crest to the withers, along the level croup, around the
hindquarter, forward under the tucked belly to the chest, up the
throatlatch and back along the jaw to the muzzle. Legs drawn BEFORE the
body so their tops hide under the silhouette; the flagged tail drawn
first too, its dock root tucked under the croup edge so it emerges from
the rump, not pasted beside it.

The dish is silhouette work, not detail: forehead (jibbah) bulge, a
deepest point ~14pt inside the forehead-to-muzzle chord, then the tiny
tapered muzzle. A dark throatlatch wedge inside the outline separates
the deep jowl from the neck without a seam. "Fine skin over bone" reads
through a thin cannon tendon line, a faint cheek line and translucent
muscle shades kept at the silhouette edges (the wapiti rule — no
free-floating mid-body strokes).

Survives critique as V1R00 with honest residue: the four legs are still
uniform column-ish blobs (a real knee/hock notch would sharpen them),
the flagged tail is a solid plume that could carry one more wisp at its
trailing edge, and the "three-quarter" cue is only the dimmed offside
legs — no far-side barrel edge is drawn.

### Proposed change

For the milestone-cards note (or a horse-breeds section when the series
consolidates): *quadrupeds with clean silhouette anatomy — horses
especially — should be drawn as a single filled silhouette from muzzle
to dock, with legs drawn under it; stacking separately-stroked
body/neck/head shapes prints seams that read as anatomy errors.* And:
*the arabian dish is a silhouette concavity between the jibbah bulge and
the muzzle tip — verify by chord geometry, not by eye.* Destination:
`prompts/series/` at next consolidation.
