## filetype set V1R00 — what survives a 16 px list row

- Kind: lesson / analysis
- Source: #1257 · `work/virelai/filetypes.py` + `draw_filetype_*.py` ·
  `art/virelai/filetype-*/` · proofs at `work/out/filetype-*-ship-big.png`
- Applies to: virelai asset families that must read at 16 px (filetypes,
  future gutter/sidebar marks)
- Status: pending

### Evidence

Ten gutter icons (folder, folder-open, text, image, audio, document,
archive, binary, contact, calendar) shipped at 32×32, proofed at 16 px
on split navy/light row fields.

What survived at 16 px: one accent hue per family is enough — the
silhouette does the naming (dog-ear page, folder tab, note head, box
tape) and the hue does the grouping. Two-tone construction works where
it's structural (folder back/front, open folder's dark mouth) but dies
as decoration. Slate `#64748B` lines on a white page read fine on both
row colors because the page is the field, not the row.

What needed fixing in-R00: folder-open's first pass hid the dark opening
behind the flap (2 px sliver → reads "closed"). Fix was to give the
mouth real height — a ~4 px ink gap between back panel and swung flap
reads "open" instantly. Also: the navy `binary` chip needed a second
edge — bare INK on NAVY disappears on dark rows; a 1.4 px `#334155`
(shipped dark Border) rim inside the ink stroke keeps the chip
separated on both fields. Lesson: dark-filled assets need a *lighter*
rim token, not house ink, when they sit on dark chrome.

Text vs document stayed legible as siblings by sharing the dog-ear page
but differing structurally — document gets the red ribbon band and two
lines, text gets three bare lines.

### Proposed change

Add to `virelai/notes/style-bible.md`: *16 px family marks earn their
difference through silhouette first, hue second, interior detail never.
Dark fills on dark chrome take a `#334155` inner rim; open/expanded
states read through a visible dark gap, not a rotated part.*
Destination: style bible next consolidation.
