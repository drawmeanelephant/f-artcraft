# Red lionfish V1R00 — separate the needle zones

- Kind: lesson
- Source: issue #1132; `work/animals/draw_red_lionfish.py`,
  `art/animals/red-lionfish/red-lionfish-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: animals field plates; subjects built from radial strokes
  (fin fans, spine ranks, whisks)
- Status: pending

### Evidence

Proof `work/out/red-lionfish-V1R00@2x.png`. First pass fanned the
pectoral rays -78°..+78° from the fin base: the topmost rays collided
with the dorsal spine rank and the whole fish read as a sea-urchin
burst. Trimming the fan to -62°..+77° and dropping a mis-angled "far
fin" echo left two legible systems: bare vertical needles (dorsal) and
a striped fan with a translucent membrane wedge (pectoral).

The membrane wedge matters: rays alone read as loose needles; with a
45–55% translucent membrane joining the inner halves they read as one
fin. Body bands need control-point interpolation onto the silhouette —
a fitted sine left bars poking past the back.

### Proposed change

For `prompts/series/20-field-plates.md`: when a subject carries two
stroke systems (spines vs fin rays), give them disjoint angular ranges
and join one of them with a membrane so the eye can sort needle from
fan. Bars/stripes on an animal's flank should be placed by
interpolating the drawn outline, not an independent curve.
