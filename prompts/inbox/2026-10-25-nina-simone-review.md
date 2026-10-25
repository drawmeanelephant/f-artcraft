## nina-simone V1R00 — the prop stick is what sells an open grand lid

- Kind: lesson / analysis
- Source: issue #1544; `work/musicians/draw_nina_simone.py`,
  `art/musicians/nina-simone/nina-simone-V1R00.{vectorcraft,svg}`,
  proof `work/out/nina-simone-V1R00@2x.png`
- Applies to: milestone cards / instrument props
- Status: pending

### Evidence

Two render-and-critique loops:

1. The grand lid drawn as a lone curved silhouette floating behind the
   figure read as a shield/surfboard — dark shape next to a dark gown.
   The fix was the prop stick: one slim 5pt stroke from the case edge
   up under the lid, and the whole assembly snaps into reading as an
   open grand piano. Context props need their mechanical connector.
2. A headwrap = one tall shape with fold bands following its rise + a
   separate gathered knot puff. Reads regal and tall; keep the knot off
   the centreline so it does not read as a topknot.
3. Keyboard shorthand that survives card scale: an ivory band + ~9
   short thick black-key ticks staggered in height. Proportional real
   key spacing would moiré at this size.
4. Long milestone lines: `MISSISSIPPI GODDAM · 1964` needed tracking
   240, not 280, to stay inside 760pt — drop tracking before dropping
   point size.

`check_rim` clean; milestone 445pt wide at tracking 240, clears ~65pt.

### Proposed change

For furniture/instrument props behind a figure: draw the connector
(prop stick, hinge, leg) that explains the silhouette. For long
milestone captions: tune `text.setStyle` tracking down to ~240 before
shrinking the 22pt size. Destination: milestone-cards note at next
consolidation.
