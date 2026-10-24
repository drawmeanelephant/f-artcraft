## Smilodon V1R00 — big-cat profiles fail without landmarks; sabers are blades, not tusks

- Kind: lesson
- Source: issue #1054; `work/animals/draw_smilodon.py`, `art/animals/smilodon/smilodon-V1R00.*`
- Applies to: animals field plates; quadruped profiles
- Status: pending

### Evidence

Proof `work/out/smilodon-V1R00@2x.png`. Two failed reads and their fixes:

- Torso+head as one smooth outline produced a capybara. A cat profile
  needs explicit landmarks: a vertical nose front, a stop dip between
  forehead and bridge, a poll notch, a withers peak clearly above the
  poll, a brisket dipping below the belly line, and a haunch mass. Even
  then the head-to-chest outline crossing shows; closing it takes an
  unstroked same-fill "neck mass" patch over the seam.
- Sabers drawn as identical-width parallel shapes read as walrus tusks.
  The fix: taper to a point, root them back at the mouth line (under the
  mid-skull, not at the nose), and let the far blade peek only ~28pt
  behind the near one — two equal blades side by side say "tusks," a
  dominant blade plus sliver says "teeth."
- Limbs: the wolverine `limb()` idiom (polyline + per-vertex widths,
  midpoint-quad outline) gives bent, tapering legs in ~20 lines — copied
  verbatim, worth extracting into `vc.py` if a third plate wants it.

### Proposed change

For `prompts/series/20-field-plates.md`: quadruped profiles — build
torso, head and legs as separate shapes sharing one gradient, and patch
the head-chest seam with an unstroked fill; a single fused outline loses
the throatlatch notch and reads rodent. Teeth always taper; tusks never
do — width-constant fangs are the tusk trap.
