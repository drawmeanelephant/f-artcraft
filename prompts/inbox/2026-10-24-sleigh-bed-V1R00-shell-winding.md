## Sleigh bed V1R00 — extruded cross-sections need a winding check, and no internal strokes

- Kind: lesson
- Source: #1170, `work/furniture/draw_sleigh_bed.py`, `art/furniture/sleigh-bed/sleigh-bed-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates; any curved board made by extruding a cross-section
- Status: pending

### Evidence

The scrolled headboard and footboard are closed x-y polygons extruded along
z: one quad per profile edge plus the near end cap, which carries the true
scroll silhouette to the viewer at ~56° incidence. Two failures on the
proof:

- Mirrored cross-sections (the footboard curls +x, the headboard −x) wind
  opposite directions; outward normals from `(ey,−ex,0)` are only right for
  CCW. A CW polygon culled its own inner face — the first render showed the
  footboard as two bare spikes. Compute the signed area and flip the
  normal when the winding is negative.
- Ink strokes on every profile-edge quad faceted the scroll into visible
  plates. Internal quads should be `stroke=NONE`; the silhouette comes from
  the end cap's outline and the lambert banding.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Curved boards
(scrolls, rockers, bent arms): extrude a closed cross-section, cull faces by
outward normal after checking polygon winding, stroke only the end cap —
internal strokes facet the curve." A proposal does not override current
house rules.
