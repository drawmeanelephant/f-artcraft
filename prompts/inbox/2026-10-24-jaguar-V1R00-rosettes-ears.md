## Jaguar V1R00 — rosette construction and ear seating

- Kind: analysis
- Source: issue #1030; `work/animals/draw_jaguar.py`, `art/animals/jaguar/jaguar-V1R00.*`
- Applies to: animals field plates; spotted cats and ear-bearing portraits
- Status: pending

### Evidence

Proof `work/out/jaguar-V1R00@2x.png`. The `rosette()` helper — five blob
ellipses on a broken ring (`r*0.8` vertical squash) plus a low-opacity core —
reads as genuine jaguar rosettes at plate scale with ~15 clusters; a seed
offset rotates each ring so they don't pattern-lock. Cenote mood carried by
liana strokes hanging from the rim, limestone hints, and the arc-closed
dark water the chest shoulders out of.

Two fixes this cycle:

1. Ears drawn as a separate pair above the head top floated like round
   mouse ears — the eye measures attachment by overlap, not proximity.
   Dropping the ear ~40pt so the head silhouette swallows its base fixed it;
   same lesson as the bigfoot crest: appendages must be swallowed by the
   silhouette, not parked beside it.
2. A mouth whose outer control points sat level with its ends plus a
   separate pale chin crescent read as a smile over a second smile. A level
   heavy mouth with a small jowl-droop tick at each corner gives the
   jaguar's sulk; a cat mouth wants its downturn drawn explicitly.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: front-facing cat
portraits — draw the mouth as a level line with a downward tick at the
corners (curved-up reads as a plush-toy smile), and seat every ear with at
least a third of its base inside the head silhouette.
