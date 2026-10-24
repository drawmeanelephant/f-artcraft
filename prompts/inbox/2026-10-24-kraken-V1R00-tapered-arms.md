## Kraken V1R00 — tapered-ribbon tentacles and sucker rows

- Kind: analysis
- Source: issue #1027; `work/animals/draw_kraken.py`, `art/animals/kraken/kraken-V1R00.*`
- Applies to: animals field plates; any tentacled/limbed subject
- Status: pending

### Evidence

Proof `work/out/kraken-V1R00@2x.png`. The quadratic `ribbon()` taper (w0→w1
along the spine, edges offset along the curve normal) produces convincing
arms with no manual polygon work; a short second ribbon chained off the tip
reads as a natural curl-hook. `sucker_row()` samples the same quadratic so
the pale cups track the arm's inner edge automatically — six cups per
climber arm reads at @2x. The gold-on-oxblood eye set wide on the mantle,
plus the 8pt brow fold, keeps the plate in field-guide idiom rather than
monster-poster. Storm mood survived: rain streaks at opacity 16 are
visible-but-quiet at @2x, and the two snapped-rigging props (broken yard
upper-left, drowned mast lower-right with a tentacle already on it) give the
"rigging-snap" note without crowding the subject. Sea and front swell both
close on `A420,420`; no rim leaks, name at y=962 clears the arc.

What didn't fully work: the front swell at y=790 nearly merges with the sea
band — the two wave lines need a wider value gap or one should go. The beak
shadow under the mantle reads as an anonymous dark blob unless you know to
look for it.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps list: tentacles and other
tapered limbs want the ribbon-along-quadratic construction, not stroked
paths — strokes can't taper, and a fixed-width stroke reads as a wire at
plate scale. Keep sucker cups ≥7pt across or they vanish at @2x.
