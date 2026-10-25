## Easel V1R00 — the canvas leans back onto the mast, not forward

- Kind: lesson
- Source: #1235, `work/furniture/draw_easel.py`, `art/furniture/easel/easel-V1R00.vectorcraft`, proof `work/out/easel-V1R00@2x.png`
- Applies to: furniture series — props resting on other members
- Status: pending

### Evidence

The canvas plane only reads once its top edge sits just *behind* the front
leg plane at that height (CZ_T ~104 vs leg z ~98 at the apex end): set it
forward of the mast and the panel floats. The blocked-in sketch (faint oval,
brow line, neck) at opacity ~35-42 carries the studio-mood story; the tray
lip must overlap the canvas foot by a few units or it reads as levitating.
Paint dabs on the floor band are cheap and earned their keep.

### Proposed change

For `prompts/series/` furniture notes: when a panel/leaner rests on a frame,
compute the frame's z at the contact height and put the panel just inside
it; overlap the supporting lip over the panel's foot.
