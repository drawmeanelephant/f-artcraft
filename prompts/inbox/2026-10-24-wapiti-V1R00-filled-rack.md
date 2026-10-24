# Wapiti V1R00 — a rack is a filled silhouette, not stroked strokes

- Kind: lesson
- Source: issue #1069; `work/animals/draw_wapiti.py`,
  `art/animals/wapiti/wapiti-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: animals field plates; antlered subjects (non-palmate)
- Status: pending

### Evidence

Proof `work/out/wapiti-V1R00@2x.png`. Three passes on the rack:

1. Stroked beam + stroked tines (round caps, 9–13pt) rendered as a
   feather headdress every time — perpendicular tines read as a mohawk,
   forward-leaning tines read as a palm frond. The geometry was right;
   the medium was wrong. Parallel strokes can only ever read as a comb.
2. Filled silhouette (the moose technique) with valleys that stop well
   above the beam rendered as a spiky crown — tine bases of ~40–70pt
   merge into one wedge.
3. Fixed by giving each tine a ~20pt base between deep notches: the top
   outline zigzags beam-edge → tip → beam-edge, and the bottom edge is
   one smooth underside curve back to the poll. That reads as an elk
   rack at @2x. Far antler = same path scaled 0.82 about the poll
   pivot, dimmer gradient.

Second finding: "shade strokes" placed mid-body with even spacing render
as floating bars / rib marks. Only strokes that clearly follow a
silhouette-adjacent flow line (mane, shoulder) survive — anything else
should be an unstroked translucent fill or removed.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: *tined antlers are
one filled silhouette with a zigzag top edge — stroked beam + stroked
tines can only draw a comb. Tine bases stay ≤ ~25pt; the notches between
tines are what make them separate points.* And: interior shading belongs
against the silhouette edge; free-floating mid-body strokes read as
anatomy errors.
