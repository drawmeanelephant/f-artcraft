## bastille-day V1R00 — pleated cockade reads at seal scale

- Kind: lesson
- Source: issue #987, `work/holidays/draw_bastille_day.py`,
  `art/holidays/bastille-day/bastille-day-V1R00.vectorcraft`,
  `work/out/bastille-day-V1R00@2x.png`
- Applies to: holidays / Festival Seals (wider government calendar)
- Status: pending

### Evidence

The tricolor cockade — cobalt / cream / scarlet concentric bands with
alternating dark-light radial pleat strokes (36/26/16 count per band) —
reads clearly as a ribbon rosette at r=118, no flag geometry anywhere.
Swallowtailed tails built from a single `tail(top_x, top_y, lean)` helper
mirror cleanly with lean=±1; cream spine stripe at opacity 42 stays subtle
against cobalt. Two dashed `rocket_trail` ascents flanking the rosette
balanced what was a hollow lower-right field in the first proof — a single
trail left the composition leaning. Vermilion chop takes a drawn mark
(three concentric rings + heart dot) instead of CJK/Hebrew glyphs, matching
the christmas seal's drawn-star approach for script-less holidays.

### Proposed change

For government-calendar seals, prefer a drawn emblem mark in the chop over
translating the name into a script the holiday doesn't own; and when a
composition has a strong low-centre anchor, mirror faint motion cues
(rocket trails, smoke) on both sides before adding more objects.
Destination: a government-seal paragraph under the holidays section of
`prompts/series/` on next consolidation.
