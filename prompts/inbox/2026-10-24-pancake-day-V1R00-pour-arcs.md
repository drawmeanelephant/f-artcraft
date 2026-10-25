## Pancake Day V1R00 — poured liquid wants a clean arc, not an S-curve

- Kind: lesson
- Source: #993, `work/holidays/draw_pancake_day.py`,
  `art/holidays/pancake-day/` native and proof
- Applies to: food/drink seals — any pour, stream or drip motif
- Status: pending

### Evidence

First pass drew the syrup pour as a wide (15px) S-curve ribbon from the
jug spout down onto the stack. On the proof it read as a solid orange
noodle wrapping over the butter pat — the double inflection and the
landing point *on* the hero prop killed the pour read. Second pass:
single-bend parabolic arc (spout -> mid -> landing point), narrower
(12px base + 8px core + 3px sheen strokes), landing on the syrup pool
*beside* the butter with a 4-dot splash crown, butter drawn after so it
sits proud. The pour now reads instantly. Also useful: layered stroke
stack (dark edge, body colour, thin highlight) beats one flat stroke for
glossy liquid at this scale.

### Proposed change

Add to the holiday-seal notes in `prompts/`: pouring streams are
single-bend arcs that land *next to* the hero prop, never on it; build
the gloss from stacked strokes (edge / body / sheen), and keep total
stream width under ~12px at seal scale.
