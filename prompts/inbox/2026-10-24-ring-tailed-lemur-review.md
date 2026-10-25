## ring-tailed-lemur-V1R00 — banded tail as segmented spline

- Kind: lesson
- Source: issue #1134, `work/animals/draw_ring_tailed_lemur.py`,
  `art/animals/ring-tailed-lemur/ring-tailed-lemur-V1R00.{vectorcraft,svg}`,
  proof `work/out/ring-tailed-lemur-V1R00@2x.png`
- Applies to: field plates, animal subjects with banded/ringed appendages
- Status: pending

### Evidence

The ringed tail is built as a Catmull-Rom centreline sampled into points,
offset along per-point normals into tapered left/right edges, then sliced
into alternating cream/ink closed bands (11 bands, 34→22pt half-taper).
Because consecutive bands share their boundary vertices, the rings butt
seamlessly even through the curl — no gaps, no stroke-join artefacts.
Reads cleanly at @2x. Seated portrait: amber eyes and the dark mask carry
the identity; white face patch at opacity 92 over the grey head keeps the
mask patches from muddying. Forearms drawn as separate gradient shapes
over the body edge read as limbs, not seams.

What nearly failed: with hands and hind feet both planted on the same
rock line, the forearm covered the near hind foot entirely — first proof
showed only three feet. Splayed the hind feet ~30pt wider than the hands
so all four limbs register. Watch limb stacking on frontal seated poses.

### Proposed change

Add to `prompts/series/20-field-plates.md` animal notes: "Banded tails
and striped limbs — draw the appendage as a sampled centreline, offset
into a tapered outline, and slice the outline into closed bands that
share boundary vertices. Stroked rings over a filled tube always show
joint gaps through a curve."
