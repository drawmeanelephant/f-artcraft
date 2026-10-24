## Stegosaurus V1R00 — kite plates staggered along the spine curve

- Kind: lesson
- Source: issue #1087; `work/animals/draw_stegosaurus.py`, `art/animals/stegosaurus/stegosaurus-V1R00.*`
- Applies to: animals field plates; dorsal-ornament subjects, tail weapons
- Status: pending

### Evidence

Proof `work/out/stegosaurus-V1R00@2x.png`. The dorsal row is the species
code: eight rounded kites with per-plate ridge strokes and alternating
lean, tallest pair over the hips, coral radial against olive hide — reads
instantly. Each kite's base sits half-buried in the torso silhouette, which
is what keeps them on the animal rather than floating above it.

Two traps hit and fixed before shipping: thagomizer spike tips are easy to
push past the rim because the tail already sweeps toward the disc edge —
every spike tip needs the `rim_x` distance check (kept all tips ≤ ~416);
and a grazing head must actually leave the torso silhouette — the first
draft placed the head inside the body's front edge, the fix was a neck
ribbon that underlaps the torso and carries the head forward-down to the
ferns.

Thagomizer in profile: four short triangular spikes fanning off the ribbon
end read fine; don't extend the tail ribbon past the last plate or it
competes with the spike fan.

### Proposed change

For `prompts/series/20-field-plates.md`: dorsal ornament rows (plates,
spines, sail) should sit their bases inside the body silhouette, stagger
lean alternately, and peak over the hips. Tail-tip geometry in corner
poses needs the disc-distance check before commit — the rim forgives
centred subjects, not tails.
