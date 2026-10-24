## mascot pose set V1R00 — the sexiburger rig generalizes cleanly

- Kind: lesson
- Source: #1250 · `work/virelai/sexiburger.py` (pose rig) ·
  `work/virelai/draw_mascot_{wave,sleep,think,celebrate,oops,locked}.py` ·
  `art/virelai/mascot-{wave,sleep,think,celebrate,oops,locked}/…-V1R00.*`
- Applies to: virelai mascot work, any future pose/expression request
- Status: pending

### Evidence

The brand-plate prediction held: `sexiburger.py` extended into a pose rig
instead of six redraws. `mascot()` keeps its old signature (`arms`, `detail`)
and gains `arm_left`/`arm_right` control triples, `eyes`
(open/closed-∪/happy-∩), `pupils` shift, `mouth`
(smile/grin/flat/wavy/o), `brows` (raise/angle) and a `props` list
(`zzz`, `confetti`, `sweat`, `padlock`, `("wave", gx, gy)` arcs). A `POSES`
table holds the six configs; each driver is ~10 lines calling the same slot
(`mascot(d, 32, 5, 52)` on 64×64 transparent) so the poses swap cleanly.

What survived the 24 px gate: silhouette + arm position carries every pose —
raised glove (wave), drooped arms (sleep), glove at chin (think), both up
(celebrate), shoulder-height shrug (oops), arms-in + gray lock block (locked).
The sweat drop, Z's and padlock read; confetti degenerates to speckle but the
arms-up silhouette does the work. Cream `SEED` and `BUN` props read on both
dark and light surfaces where bare INK would die on navy.

Gotchas: `ARM_PRESETS` needed a `down` entry (drooped tentacle-arms) — a
preset only sets a side's default; an explicit `arm_left`/`arm_right` triple
overrides it, so asymmetric poses mix preset + override. The glove hand is
drawn fingers-up; drooped arms keep it (limp still reads as a mitten).

### Proposed change

Candidate rule for `virelai/notes/style-bible.md`: *mascot poses change
limbs + face + props only — dome, fillings, body mass and the shared slot
stay identical so assets swap in-place. Expressions carry the small-size
read; props are secondary and stay ≥4 u.* Next mascot-adjacent work
(#1255 `spinner-mascot`, spot cameos) should reuse the rig rather than
new bodies.
