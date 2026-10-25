## Passover/V1R00 — a disc-in-a-disc needs its own grammar

- Kind: lesson
- Source: issue #981, `work/holidays/draw_passover.py`,
  `art/holidays/passover/passover-V1R00.*`, proof `work/out/passover-V1R00@2x.png`
- Applies to: holidays (Festival Seal) series
- Status: pending

### Evidence

The seder plate is a second disc inside the seal disc — porcelain white
with a cobalt rim band makes it read as blue-and-white china rather than
a white blob, and the 28 scallop tick-dots on the band sell the ceramic.
Tiny Hebrew well labels (Arial Hebrew ~12px) survive at 2x and turn six
identical dishes into the actual ka'arah order; a "פסח" title across the
plate's top dead space is borrowed straight from real seder plates.

Caught in proofing: ground shadows count. A drop-shadow ellipse under a
side prop (Elijah's cup at x≈268) reached r>430 and check_rim flagged
2713px — shadows are pixels too. Props near the rim need their shadows
shortened, not just their bodies kept inside. Also: a label below the
lowest well printed dark-on-dark onto the plate's cast shadow — bottom-row
wells label better to the side than below.

### Proposed change

Note for the seal grammar: "when the hero is itself a disc (seder plate,
coin, moon), treat its cast shadow and any side-prop shadows as rim
candidates — run check_rim before art hand-off." Destination:
`prompts/series/40-orient.md`.
