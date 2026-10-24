## Gila monster V1R00 — bead field reads best as a probability map

- Kind: lesson
- Source: issue #1106, `work/animals/draw_gila_monster.py`,
  `art/animals/gila-monster/gila-monster-V1R00.*`
- Applies to: animals field plates; any scaled/pebbled integument
- Status: pending

### Evidence

The osteoderm bead field is a (u, v) grid lerped between a top quad and a
belly quad, each bead an ~9pt ellipse with its own radial gradient. What
worked: a **band probability function**, not painted bands — inside four
irregular crossband windows the light-bead probability is ~0.95, outside it
~0.10. The result marbles like the live animal instead of striping. First
pass used 0.85 inside bands and the pattern dissolved into uniform speckle;
0.95/0.10 was the first setting where the bands survived at @2x.

Two second-order fixes that mattered: bead dots overlaid on tail bands had
to be jittered ±2pt and size-varied or they read as corn rows; and the head
had to drop below the nape line (top y≈470 vs nape 450) — a head drawn as
tall as the trunk reads as a tadpole balloon, not a dipped blunt snout.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: "Integument texture
(scales, beads, feathers) works as a probability field over the body
parametrization, not as painted shapes — push in-band probability to ~0.95
and out-of-band to ~0.10 or the pattern dissolves to noise at plate scale.
Jitter any dots that ride a painted band or they align into rows."
