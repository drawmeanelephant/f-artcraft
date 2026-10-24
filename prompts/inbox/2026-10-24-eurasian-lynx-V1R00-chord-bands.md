## eurasian-lynx V1R00 — a chord is safe, a band on the chord is not

- Kind: lesson
- Source: #1063, work/animals/draw_eurasian_lynx.py, art/animals/eurasian-lynx/eurasian-lynx-V1R00.*
- Applies to: animals field plates; vertical decor (trunks, reeds, masts) drawn as offset chords
- Status: pending

### Evidence

Birch trunks drawn as tapered bands anchored with both ends on the disc arc
still leaked: the ends were on the rim, but the band's perpendicular offset
put each top/bottom *corner* ~27px past r=420 (check_rim: 2544px). A chord
between two rim points is always inside; a band offset from that chord is
only inside if all four corners are. Fix was to compute corners, not
anchors — inset the ends to fixed points and verify each corner's radius
(r417 max after the move). Backdrop stars also flag check_rim (any
non-backdrop pixel outside r430 is a leak), so the night sky lives inside
the disc or not at all.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: decor drawn as a band
(trunks, spars, reeds) needs its four corners inside the disc, not just its
endpoints — the corner, not the anchor, is what crosses the rim.
