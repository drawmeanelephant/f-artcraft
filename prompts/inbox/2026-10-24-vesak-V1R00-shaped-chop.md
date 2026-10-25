## vesak-V1R00 — shaped-script chops stamp horizontally

- Kind: lesson
- Source: issue #982, `work/holidays/draw_vesak.py`,
  `art/holidays/vesak/vesak-V1R00.vectorcraft`, proof `work/out/vesak-V1R00@2x.png`
- Applies to: holiday seals (festival_kit / orient plate grammar)
- Status: pending

### Evidence

Vesak adopted from a dead worker's uncommitted draft (authorized claim
recovery; the earlier claim log entry on #982 names t3/9c1d54fe). Re-rendered
byte-identical on current main, 284 calls / 0 errors.

The chop carries Devanagari वैशाख. `Plate.chop` stacks glyph-per-line for CJK;
a shaped Indic conjunct cannot be split per codepoint, so the piece calls
`chop(..., horizontal=True)` as a single centred `add_text` — the mark renders
correctly shaped inside a wide vermilion cartouche at the top right.

Critique pass: quiet mid-field between the lantern string and the lotus is
consistent with mid-autumn's emptier night field; lantern hangers land on a
sagging quadratic cord with varied drops, which reads assembled rather than
stamped. `check_rim` flags 209 px — all backdrop stars outside r430, same
deliberate leak as hanukkah-V1R00's 85 px; accepted.

### Proposed change

Add to `prompts/series/40-orient.md` or the seal grammar notes: "chops in
shaped scripts (Devanagari, Arabic, Thai) must be stamped horizontally with a
single text run — never split per codepoint into a vertical stack." Note the
existing `horizontal=True` flag on `Plate.chop` as the mechanism.
