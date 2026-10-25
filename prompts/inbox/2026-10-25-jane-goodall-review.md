## Jane Goodall V1R00 — two figures, one touchpoint; draw the reach first

- Kind: analysis
- Source: issue #1554; `work/scientists/draw_jane_goodall.py`,
  `art/scientists/jane-goodall/jane-goodall-V1R00.{vectorcraft,svg}`,
  proof `work/out/jane-goodall-V1R00@2x.png` (`check_rim.py`: clean)
- Applies to: scientist milestone cards; two-subject plates, foliage decor
- Status: pending

### Evidence

Two loops (first failed on leaf asserts before rendering).

- **Compose from the touchpoint outward.** The card lives or dies on the
  hand-to-hand moment: fix the offered palm position first (here
  ~(610,692)), run her extended arm back to the shoulder, run the
  chimp's reach from its shoulder forward — then place both bodies so
  those limbs read. Bodies placed first would never meet cleanly.
- **A seated figure is a mound, not a skeleton.** Folded legs = one wide
  smooth mass with two knee-crease strokes and a boot blob at the open
  end; the torso sits on it. Trying to draw lap/ knees/ shins as parts
  is where seated poses fall apart.
- **The young chimp is head-heavy on purpose:** head ~1/3 of body mass,
  pale face mask inside a dark head, ear circles flanking the mask,
  crown stroke — reads infant without fur texture. Reaching arm is one
  15pt round-cap stroke + a skin hand blob; ≥3pt rule applies to the
  detail strokes, the limb itself wants mass.
- **Hanging foliage: leaf = base point + tip + two bulge offsets along
  the normal**, one vein stroke. All leaf extremes need `on_disc`
  asserts *including the width bulge near the base* — the first pass
  passed the tips but leaked the shoulders of the leaves.
- **Binoculars at the neck** are two dark lens circles + strap strokes;
  the cheapest signature prop in the series.
- Milestone `TOOL-MAKING CHIMPS · 1960` in Source Sans 3, tracking 480 →
  530pt wide, 65pt clear of the rim.

### Proposed change

For the milestone grammar: *on two-subject plates, the contact point
(touch, gaze-line, offered object) is the first coordinate committed;
limbs are generated from it back to the shoulders, bodies placed last.*
Destination: the scientist/milestone card note at the next
consolidation.
