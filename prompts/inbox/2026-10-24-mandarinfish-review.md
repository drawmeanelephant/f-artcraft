## mandarinfish-V1R00 — pattern strokes must solve for the silhouette

- Kind: lesson
- Source: issue #1137, `work/animals/draw_mandarinfish.py`,
  `art/animals/mandarinfish/mandarinfish-V1R00.{vectorcraft,svg}`,
  proof `work/out/mandarinfish-V1R00@2x.png`
- Applies to: field plates, fish and any patterned silhouette
- Status: pending

### Evidence

First proof: the flank's swirl bands were single-stroke paths with one
global y-extent — a fish flank is deepest amidships and pinches fore and
aft, so the same band that fit mid-body dangled 40pt into open water at
the tail stock. Pattern strokes need per-band extents solved against
the local silhouette, not one template. Passing each band its own
top/bottom anchors (yt at the back line, yb at the belly line) fixed it
without clipping masks. Same discipline as rim math: a coloured stroke
outside the subject silhouette reads as a decoration leak even inside
the disc.

What worked: translucent pectoral and tail fans (radial gradient with a
~55% tail stop) keep the fins glassy over the dusk water; the male's
erectile first-dorsal filament is the silhouette cue that separates it
from a generic reef fish.

### Proposed change

Add to `prompts/series/20-field-plates.md` animal notes: "Marking bands
on a tapered body (fish, eels, seasnakes) are per-position strokes:
anchor each band's ends on the local dorsal and ventral silhouette,
don't reuse one y-extent across the flank."
