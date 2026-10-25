# Haikus — wave 2 proposal

Status: draft, not posted. Expansion proposal for `art/haikus/`. Each row
below is a **separate leaf-issue candidate**, not one task — the wave splits
into individual `Haiku graphic: <Name>` issues when approved.

## Format reminder (from shipped wave 1)

Per `work/haikus/draw_hai_0436_jiggler_jimmy.py` and siblings:

- Canvas 1000×1000. Dark backdrop gradient, plate ellipse `x=80 y=40
  w=840 h=840` (centre 500,460, r≈420), ~6pt rim stroke, 792×792 inner
  ring at low opacity, plus one soft light pool behind the vignette.
- The plate holds one still moment, not a story: a glowing presence dot,
  a vibrating cursor, a chair pushed back. Mascot presence may be
  implicit — the empty object reads louder than the face.
- Caption stack: the key haiku line **in lowercase**, ~21pt, tracking
  ≈70, around y≈898; `NAME` ~56pt at y≈948. Wave 1 ships no second
  role line — the verse line is the epithet.
- Slug is `hai-NNNN-<mascot-slug>`, NNNN the mascot's archive number,
  zero-padded to four digits.
- Driver `work/haikus/draw_<slug>.py` → `d.finish("<slug>-V1R00")`;
  commit `.vectorcraft`, `.svg`, `@2x.png`. Rim rule: floor bands close
  on the disc's own arc.

## Leaf briefs

Wave 1 covered M-0436–0446 (eleven office haiku, all `hai-`). Wave 2 adds
seasonal spread — one kigo moment per plate — and stretches the form:
`sen-` for senryū (same shape, human foible instead of season) and
`tan-` for tanka (the two-line envoi drawn as a second, fainter caption
line under the key line).

| Slug | Subject | Mood / the drawing's job |
| --- | --- | --- |
| `hai-0425-dawnstamp` | Dawnstamp — spring | Pale gold renewal; the day's first stamp landing on still-wet ink at first light |
| `hai-0421-wrong-door-finch` | Wrong-Door Finch — summer | Startled brightness; a finch mid-turn at the wrong window, paper drifting |
| `hai-0426-old-wire-pilgrim` | Old-Wire Pilgrim — autumn | Weathered pilgrimage; a small figure along a sagging wire, leaves letting go |
| `hai-0408-the-half-held-breath` | The Half-Held Breath — deep winter | Suspended hush; the held breath above a stamp that has not yet fallen |
| `hai-0417-the-unmet-bell` | The Unmet Bell — first snow | Silent expectancy; snow piling on a bell that has never rung |
| `hai-0672-map-72-absentia` | Map-72 Absentia — the grey season | Cartographic longing; a map with the territory politely missing |
| `hai-0938-vantage-hollow` | Vantage Hollow — night | Watchful dark; a hollow that watches back, one low lamp |
| `sen-0503-servicey-unavailabelle` | Servicey Unavailabelle — senryū | Wry apology; the BACK SOON sign as the whole human condition |
| `sen-0937-blinko-chompframe` | Blinko Chompframe — senryū | Flickering wit; attention measured in half-frames |
| `sen-0451-the-quiet-injunction` | The Quiet Injunction — senryū | Hushed mischief; the order nobody heard and everyone obeyed |
| `tan-0412-red-pencil-mercy` | Red-Pencil Mercy — tanka | Five-line absolution; the pencil pausing over a forgivable line |
| `tan-0327-minutes-without-motion` | Minutes Without Motion — tanka | Sedimentary patience; a meeting preserved in strata |

## Guardrails

- Recheck `art/haikus/`, open/closed issues and open PRs before writing
  any leaf issue or claiming; the cast roster in `PROMPTS.md` is
  historical, not a queue.
- `sen-` and `tan-` keep the same plate grammar and caption stack; the
  tanka envoi may add one fainter line under the key line — keep it
  inside the rim.
- A mascot that already ships a haiku stays single-entry: do not re-versify
  M-0436–0446.
- Labels per `.github/LABELS.md`: `type:*` for the deliverable plus an
  explicit `work:*` intent per leaf.
