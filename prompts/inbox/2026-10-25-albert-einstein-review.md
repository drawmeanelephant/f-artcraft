## Albert Einstein V1R00 — a polar halo of alternating radii, and SS3 tracking isn't Virelai tracking

- Kind: analysis
- Source: issue #1546; `work/scientists/draw_albert_einstein.py`,
  `art/scientists/albert-einstein/albert-einstein-V1R00.{vectorcraft,svg}`,
  proof `work/out/albert-einstein-V1R00@2x.png` (`check_rim.py`: clean)
- Applies to: scientist milestone cards; milestone lines containing digits
- Status: pending

### Evidence

Two loops. The wild-hair signature landed as a polar halo: points at
uneven angles alternating in/out radii (~120 inner / ~170 outer),
x-stretched ×1.16 and y-squashed ×0.94 — evenly spaced tufts at equal
radii read as a *starburst crown*, not hair; the jitter and the stretch
are what make it read as a mane. Elderness comes from three cheap
strokes: heavy lid lines over the eye almonds, under-eye bags, two
forehead arcs. The mustache is one droopy mass with a small mouth
stroke peeking under it.

Deviation forced by the issue text: the milestone line `MIRACLE YEAR ·
1905` contains digits, and Virelai Sans has none, so the whole line is
Source Sans 3 (holiday-card precedent). **SS3 is much narrower than
Virelai at equal tracking** — Virelai 22pt/tracking-280 gave 528pt for
a 26-char line, while SS3 22pt/tracking-300 gave only 315pt for 19
chars and looked thin under the name. Tracking ~520 lands ~407pt, which
hangs with the series. Verify with `inspect_document` bounds every
time; the ≤760pt cap has headroom.

`E = mc²` ghosts into the plate as a real Source Sans 3 text at
opacity 15 (the ² glyph exists); surrounding chalk marks are plain
strokes at 10–14 so nothing literal competes with the face.

### Proposed change

For the milestone grammar: *digit-bearing milestone lines go entirely
to Source Sans 3, and need roughly double the Virelai tracking value
(~500–560) to hold the same visual width — always confirm against
`inspect_document` bounds, never by eye.*
