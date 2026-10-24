## christmas-V1R00 — snow floors must hug the rim arc

- Kind: lesson
- Source: issue #975, work/holidays/draw_christmas.py, art/holidays/christmas/christmas-V1R00.*
- Applies to: holidays / festival seals
- Status: pending

### Evidence

First proof used a plain ellipse for the snow drift at the foot of the disc;
it crossed the rim and failed check_rim (6687 px outside, e.g. 218,785) and
read as a grey UFO platform rather than snow. Replacing it with a chord-plus-
rim-arc path (`M242,788 Q500,742 758,788 A420,420 0 0 0 242,788 Z`) keeps
every pixel inside r420 and reads as a snow bank because the lower edge IS
the rim curve. Drooping fir tiers built as arched-top/scalloped-bottom boughs
read clearly as a lit tree once ornaments and candle dots sit on the scallop
line.

### Proposed change

In the Festival Seal grammar, ground elements at the foot of the disc should
be drawn as a chord across the disc closed by the rim arc, never as free
ellipses that can drift outside r420. Worth one line in prompts/core or the
holidays section of the Orient series.
