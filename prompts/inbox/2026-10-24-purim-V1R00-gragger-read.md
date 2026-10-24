# Purim/V1R00 — the slapper blade is what makes a gragger read

- Kind: lesson
- Source: issue #980, `work/holidays/draw_purim.py`,
  `art/holidays/purim/purim-V1R00.*`, proof `work/out/purim-V1R00@2x.png`
- Applies to: holidays (Festival Seal) series
- Status: pending

### Evidence

First proof read the gragger as a brush or mallet: five small teeth along
the head's top edge looked like bristles. Two changes fixed the read —
four bolder saw teeth, and a thin slapper blade jutting past the head's
lower edge (the part that actually makes the noise). A tilted prop was
built by drawing upright and rotating every point through a small `rot()`
helper about the head centre; `rotation=` on draw_shape composes fine
with pre-rotated positions for symmetric marks like the knob.

The domino mask needed almond eye holes drawn as Q-curve paths (ellipses
read as goggles) and the centre jewel to break the symmetry axis — without
it the band read as a sash. Three objects on a triangle (mask top,
gragger lower-left, platter lower-right) left a dead middle; mid-field
confetti and two extra streamers filled it without crowding.

### Proposed change

In the Festival Seal notes: "a gragger without its slapper blade is a
mallet; a mask without eye-holes is a sash" — props of disguised/
noise-making holidays read through their functional parts, not their
silhouette. Destination: `prompts/series/40-orient.md`.
