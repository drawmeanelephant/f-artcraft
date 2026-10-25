## White-nosed coati V1R00 — ringed tail as tapered outline

- Kind: analysis
- Source: issue #1125, `work/animals/draw_white_nosed_coati.py`,
  `work/out/white-nosed-coati-V1R00@2x.png`
- Applies to: field plates / animals
- Status: pending

### Evidence

Nasua narica in profile, nose in the litter, ringed tail held upright in
a loose curl; all four feet grounded on the floor chord. What worked:
building the tail as a tapered outline (polyline + per-point half-widths,
offsets along normals, closed through `smooth()`) and then drawing the
rings as short pale strokes across the local tangent — the bands hug the
curl with no clipping needed. The white muzzle carries the species ID;
the small flipped leaf at the snout tip sells the rooting behaviour only
when it actually touches the muzzle (a floating leaf read as a tongue).
What failed on pass one: a neck shape with a low lobe that read as a
dewlap — fixed by pulling its underside up toward the chest.

### Proposed change

Candidate helper for `work/animals` or the field-plates spec: curved
tapered-appendage idiom (control polyline + half-widths + normal offsets)
with ring/band marks placed by arc-length fraction. Reusable for ringtail,
lemur, genet, snake bodies.
