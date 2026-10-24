## Bunk bed V1R00 — tall frame furniture draws as depth bands, and ladders must touch the floor

- Kind: lesson
- Source: #1171, `work/furniture/draw_bunk_bed.py`, `art/furniture/bunk-bed/bunk-bed-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates; any open frame of posts and rails
- Status: pending

### Evidence

A bunk bed is ~40 small prisms with no enclosing carcass, so draw order is
the whole job — and the club-chair depth-band rule holds verbatim: far
posts → end frames → far side rails → mattresses/blankets/pillows → near
rails → guard rail → ladder → near posts. Written that way, no face of one
member ever lands on a nearer member.

Two small proof catches: a ladder whose stiles ended at y=2 read as hanging
in mid-air (extend to y=0 — furniture props need visible ground contact or
a visible hook), and the head end's slatted frame only read once the slats
were fattened to ~1.2in model width — the thin-geometry rule applies to
verticals as much as spindles.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Open frames
(bunk, étagère, drying rack): draw strict depth bands — far posts, far
rails, contents, near rails, near posts. Ladders and stiles must reach the
floor or a visible hook." A proposal does not override current house rules.
