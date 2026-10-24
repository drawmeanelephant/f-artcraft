## tokens-V1R00 — first figcraft sheet: what the doc register wants

- Kind: lesson
- Source: issue #1264; driver `work/virelai/draw_tokens.py`, native +
  exports `virelai/design/tokens/tokens-V1R00.*`
- Applies to: the virelai figcraft sheets (#1262–#1264) and any future
  design-doc work
- Status: pending

### Evidence

First sheet in the figcraft register and the conventions held up: flat
`<sheet>/` dir under `virelai/design/`, same `Draw` bootstrap as art, same
revision suffix. Sheet-specific lessons:

- **Doc register ≠ art register.** Controls are drawn at *real pixel
  sizes* (toggle 32×18, rail tab h22, scrollbar 12px) on a big sheet
  canvas (1920×1408), not scaled up — the sheet is the contract, so
  honesty beats prettiness. The one sanctioned gradient (seat desktop)
  stays a labeled swatch, not a paint style.
- **`text.setStyle` digit spans work fine** — `PLATE V1R02` renders
  Virelai Sans letters + Source Sans 3 digits inline, which is itself a
  token demo worth repeating on later sheets.
- **Fonts that resolve in-app:** Inter (+SemiBold/Medium), JetBrains
  Mono, **Virelai Mono** (exists! use it for code specimens — labelled
  honestly when the OS ships Fira Code), Source Sans 3/Serif 4, Virelai
  Sans, Virelai Mascots. `Fira Code` silently falls back proportional —
  don't request it.
- **`add_text` y is the first baseline**, not top — budget ~0.8em above.
- Deferred controls are drawn *and labelled* deferred (tooltip, in-window
  tabs) — a design doc that invents shipped UI is worse than one that
  says "no consumer yet".

### Proposed change

None to shared rules — this note just seeds `virelai/notes/` practice:
later sheets (#1262 seat shell, #1263 app screens) should keep the same
page chrome (panel plates `#1D1D29` on the navy page), cite
`docs/ui-primitives.md` rather than restating tokens, and embed this
sheet's vocabulary by reference.
