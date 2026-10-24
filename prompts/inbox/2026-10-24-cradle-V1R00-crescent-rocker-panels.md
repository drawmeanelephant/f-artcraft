## Cradle V1R00 — end panels as crescent rockers

- Kind: lesson
- Source: #1230, `work/furniture/draw_cradle.py`, `art/furniture/cradle/`
- Applies to: field plates — furniture with rockers / cradles / any slab-end construction
- Status: pending

### Evidence

The cradle's rockers are not separate parts: each end panel is a slab whose
bottom edge is the rocker arc (`R - sqrt(R^2 - x^2)` along x plus a quadratic
tip lift), so one polygon is headboard + rocker at once. That single outline
carries the "cradle" read better than box-plus-runners would. Two grounding
notes: the far rocker contact projects ~40pt above the near one, so the
floor chord should sit at the *near* contact's height — matching the far one
makes the piece float; and a single soft shadow ellipse spanning both
contacts reads weak — small hard contact ellipses at each touch-down point
sell the weight. The bonnet hood is a bezier crown arc in (z,y): shell
between the two x-edges + a solid cheek face proud of the shell edge +
a face-frame rail at the open edge; the cheek face is what gives it a
furniture read instead of a cushion read.

### Proposed change

Note in Furniture traps in `prompts/series/20-field-plates.md`: for cradle/
rocker subjects, end panels can carry the rocker arc as their bottom edge;
set the floor chord at the nearest contact point and add a hard contact
ellipse per touch-down — far contacts sit higher on screen and must not be
pulled down to the chord.
