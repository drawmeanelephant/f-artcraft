## Coconut crab V1R00 — stroked two-joint legs beat tapered shapes

- Kind: lesson
- Source: issue #1052; `work/animals/draw_coconut_crab.py`, `art/animals/coconut-crab/coconut-crab-V1R00.*`
- Applies to: animals field plates; arthropods; scene mood
- Status: pending

### Evidence

Proof `work/out/coconut-crab-V1R00@2x.png`. First draft built the walking
legs as filled tapered closed paths fanned from under the carapace — on the
proof they read as wings/fins, not legs. Reworked to the spider-crab idiom:
each leg a two-point polyline (base → knee → toe) stroked twice, ink edge
17pt under ember-gradient core 9pt, plus a knee-knob ellipse. The read
flipped immediately: bent joints and toes planted on the sand are the leg
code, silhouette taper is not. Story props carry the plate the way the
ribcage did for komodo: crusher palm resting over a husked coconut with
its three germ pores peeking out, and a stolen fork gripped in the small
pincer — small tells, but they are the issue's own copy made visible.

Working notes: palm fronds drawn as filled pointed paths leaked past the
rim at upper right (caught by a pixel scan for r>445, not by the naked
eye) — keep every control point of a Bézier frond inside r≈415, the curve
stays inside its point hull. A surf line at the sand crest (low-opacity
stroke just above the `A420,420` floor) fills the dead band between sky
and subject without cluttering it.

### Proposed change

For `prompts/series/20-field-plates.md`: arthropod legs want stroked
two-joint polylines with a knee knob, never tapered fills — the joint is
the tell. For night plates, a moon + a single low-opacity surf stroke at
the floor crest gives an island in two shapes.
