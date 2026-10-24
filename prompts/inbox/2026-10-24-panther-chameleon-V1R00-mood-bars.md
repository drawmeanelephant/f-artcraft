## Panther chameleon V1R00 — bars as the read, the spiral as the signature

- Kind: analysis
- Source: issue #1043; `work/animals/draw_panther_chameleon.py`, `art/animals/panther-chameleon/panther-chameleon-V1R00.*`
- Applies to: animals field plates; reptiles; saturated subjects
- Status: pending

### Evidence

Proof `work/out/panther-chameleon-V1R00@2x.png`. The species read lands:
tall leaf-compressed body, casque helmet with its own comb teeth, turret
eye (a cone, not a socket — the only lizard whose eye protrudes), clamp
feet on a gnarled branch, and the tail coiled into a flat spiral. The
"mood ring" brief is carried by color: teal flanks, cream lateral stripe,
four coral bars at stepped opacity (62–80) so the bands feel lit rather
than printed.

Working notes: a stroked spiral (strokeWidth 16, cap round) curls the tail
convincingly — no filled taper needed once the tip disappears into the
coil center. Rotated ellipses are not available via `draw_shape`
(`rotate` is not a valid arg); pointed leaf drops are better built as
two-curve paths anyway. The dorsal serration and casque comb are the same
triangle motif at two scales — cheap continuity.

What to watch: zygodactyl feet drawn as mitten-blobs barely read as
gripping; wrapping them *over* the branch with a toe-line split is the
obvious next revision if the pose ever needs re-drawing.

### Proposed change

For `prompts/series/20-field-plates.md`: for color-shift species the
banding IS the species — four or five wide translucent bars beat any
rendering of chromatophore texture. And a note for the API traps list:
`draw_shape` has no `rotate`/`opacity` keyword on some builds — build
rotated primitives as paths, use `object.rotate` only when a returned
id exists.
