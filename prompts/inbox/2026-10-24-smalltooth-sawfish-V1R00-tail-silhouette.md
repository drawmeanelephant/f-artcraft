## Smalltooth sawfish V1R00 — one continuous fish silhouette

- Kind: analysis
- Source: issue #1128, `work/animals/draw_smalltooth_sawfish.py`,
  `work/out/smalltooth-sawfish-V1R00@2x.png`
- Applies to: field plates / animals
- Status: pending

### Evidence

Pristis pectinata in profile over an estuary mud chord, rostrum leading
with an even rank of ~11 teeth per edge. What failed on pass one: the
tail was a separate short peduncle blob with caudal and two dorsals
stacked on it — three rounded shapes collided into a lumpy potato. The
fix that worked: draw the whole body as one tapering silhouette head to
tail tip, then hang the dorsals and caudal as swept triangles on that
edge — sawfish dorsals sit far aft and the caudal is a small notch, not
a shark fork. The rostrum teeth read best as tiny filled triangles
(3-point paths) planted on both edges, base inset, stopping short of tip
and head. Gill slits and the ventral mouth belong under the head — far
enough back they start reading as body scribbles.

### Proposed change

For `prompts/series/20-field-plates.md` animals notes: elongated fish
bodies want a single silhouette path; separate peduncle + tail shapes
stack into lumps. Diagnostic fins (far-aft dorsals, notched caudal) do
the species ID when the saw has done the headline.
