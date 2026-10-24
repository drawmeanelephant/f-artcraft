# Galápagos tortoise V1R00 — translucent ellipses leak too

- Kind: lesson
- Source: issue #1075, `work/animals/draw_galapagos_tortoise.py`,
  `art/animals/galapagos-tortoise/galapagos-tortoise-V1R00.*`
- Applies to: field plates
- Status: pending

### Evidence

The proof carries the dome carapace (costal seams following the dome's
fall, marginal ticks on the plastron lip, faint growth arcs), four
elephantine columns — far-side legs darker and half-hidden — and the
neck reaching ahead into a low wedge head. A small finch rides the
shell's shoulder; drawn dark enough to be a passenger, not a second
subject. The catch of the round: a ground-mist ellipse laid at low
opacity looked harmless but its left half fell well outside the disc —
low-opacity does not exempt a shape from the rim rule. It was rebuilt
as a stroked arc computed against the disc's own radius.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: the rim-leak rule
applies to strokes and translucent washes, not just filled silhouettes —
any wide soft shape near the disc's edge should be built as an arc
computed from `rim_x`/the disc radius, or pass an `on_disc` assert at
its extreme points.
