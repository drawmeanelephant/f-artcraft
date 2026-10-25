## Pembroke welsh corgi V1R00 — erect ear pairs are ordered triangles, not mirrored ones

- Kind: analysis
- Source: issue #1508; `work/dog-breeds/draw_pembroke_welsh_corgi.py`,
  `art/dog-breeds/pembroke-welsh-corgi/pembroke-welsh-corgi-V1R00.{vectorcraft,svg}`,
  proof `work/out/pembroke-welsh-corgi-V1R00@2x.png`
- Applies to: dog-breeds milestone series; erect-eared profiles
- Status: pending

### Evidence

Two render loops. Profile ear pairs fail a specific way: two mirrored
triangles sharing the skull top cross at the base and read as a bowtie.
Fix is ordering, not geometry — draw the FAR ear first (smaller, dimmer,
offset right and slightly behind), then the NEAR ear taller and
forward-cupped overlapping its base. The overlap at the skull reads as
ear placement, the spread tips read as the breed's bat ears.

The heel-nip brief survives as: near fore stepping out low + head
stretched forward level with the back, not dipped — a dipped head reads
beagle-scenting, level-forward reads herding-lunge. Smile is a 3-stroke
build: level mouth, one upturned corner tick, a tongue wedge tucked
under the corner at ≤30pt. Docked tail is a tiny nub only — anything
longer argues with the brief. White underside as one overlay shape
(blaze + chest + belly skirt) unifies the red-and-white pattern.
check_rim clean; milestone cleared by 69pt.

### Proposed change

Add to the milestone-cards note at consolidation: "profile ear pairs —
far ear first, smaller and behind; near ear overlaps its base; tips
spread, bases never cross."
