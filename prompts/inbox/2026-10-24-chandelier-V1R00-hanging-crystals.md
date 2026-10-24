## Chandelier V1R00 — hanging pieces need hangers, glows need the rim check

- Kind: lesson
- Source: #1175, `work/furniture/draw_chandelier.py`, `art/furniture/chandelier/chandelier-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — furniture and any fixture hanging from above
- Status: pending

### Evidence

First pass put every crystal in place but read flat: the skirt drops
under the arm roots floated as loose diamonds, and three sparkle marks
sat on empty plate reading as stray plus signs. Threads (1.5pt, low
opacity) above each drop and glints moved onto actual crystal bodies
fixed both. Separately, the floor light pool at 460×110 leaked past
the disc rim — the extent check caught it (442 > 394): floor glows
centred on a chord near the rim must be sized so `dist(center)+r` stays
inside, same rule the inbox already records for glows. A ceiling chord
closing on `A420,420 0 0 0` (sweep 0, the upward arc) works as the
mirror of the floor chord for hanging subjects.

### Proposed change

For `prompts/series/20-field-plates.md`: pendant elements must hang
*from* something visible — thread, arm, or knop — and sparkle marks
belong on crystal bodies only. Note the ceiling-chord arc variant
(`0 0 0`) alongside the floor (`0 0 1`).
