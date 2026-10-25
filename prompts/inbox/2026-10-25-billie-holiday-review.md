## Billie Holiday V1R00 — light shafts are decor too; eyes-down via lids not pupils

- Kind: analysis
- Source: issue #1533; `work/musicians/draw_billie_holiday.py`,
  `art/musicians/billie-holiday/billie-holiday-V1R00.{vectorcraft,svg}`,
  proof `work/out/billie-holiday-V1R00@2x.png`
- Applies to: musicians milestone series; any backdrop light effect;
  portraiture cues
- Status: pending

### Evidence

Two render loops; check_rim caught the big one.

- **A spotlight beam is decor and must stay inside the disc.** First
  pass ran a light wedge to y880 — 90k px of rim leak. Bound the shaft
  to a chord-bounded quad with `assert on_disc(corner, 8)` per corner,
  same discipline as desk props.
- **Per-stop gradient opacity turns a quad into light:**
  `{"offset","color","opacity"}` stops (opacity is 0–1 float) fade the
  shaft as it falls — flat-opacity beam reads as a solid slab.
- **"Eyes lowered" is lid arcs, not pupils.** Downward-curving lid
  strokes (4.5pt) with three small lash ticks each — no whites, no
  pupils. Reads as lowered gaze at thumbnail size; open eyes with
  down-set pupils read as squinting suspicion.
- **A nape bun must be painted BEHIND the head.** On top it reads as a
  dark growth on the cheek; behind, it peeks as nape hair.
- **Pearls = two catenary strands of small radial-gradient beads**
  (9 beads, `y0 + drop·sin(πt)`) over the collar band — cheap and
  unmistakably 1940s.
- Round grill mic on a slim stand reads "vintage broadcast" instantly;
  keep it at mouth height beside the face, not at the lips — "at the
  mic" is proximity, not contact.

### Proposed change

For the musicians note: mood effects (spot shafts, haze) follow the same
on_disc assertion as solid decor; eyelid arcs + lashes are the house
vocabulary for downcast eyes; hair pieces behind the jaw are painted
before the head.
