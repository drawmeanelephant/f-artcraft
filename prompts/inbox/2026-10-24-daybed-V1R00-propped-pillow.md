## Daybed V1R00 — a propped pillow must touch what props it

- Kind: lesson
- Source: #1173, `work/furniture/draw_daybed.py`, `art/furniture/daybed/daybed-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates, prism-rig props
- Status: pending

### Evidence

First pass modelled the pillow as a `lean_box` resting at mattress
centre-depth (`x -36..-13`), leaning back onto air. On the proof it read
as a floating wedge — neither the left edge nor the top edge reached the
end frame it was supposed to lean on. Extending it to `x -37.2` (lapping
the frame post's inner face in screen space) plus a seam inset polygon
on the front face made it read as a pillow propped at the head end.
The same proof showed fold lines on a draped throw only read once
redrawn *after* the rail they hang in front of — depth order, not
stroke width, was the fix.

### Proposed change

For `prompts/series/20-field-plates.md` furniture section: a prop that
leans must overlap its support in screen space (draw it after the
support, edges crossing), and drape folds belong on the last draw of
the drape, not the first.
