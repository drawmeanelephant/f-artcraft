# Limericks — wave 2 proposal

Status: draft, not posted. Expansion proposal for `art/limericks/`. Each row
below is a **separate leaf-issue candidate**, not one task — the wave splits
into individual `Limerick graphic: <Name>` issues when approved.

## Format reminder (from shipped wave 1)

Per `work/limericks/draw_lim_0436_jiggler_jimmy.py` and siblings:

- Canvas 1000×1000. Dark backdrop gradient, plate ellipse `x=80 y=40 w=840
  h=840` (centre 500,460, r≈420) with ~6pt rim stroke and a 792×792 inner
  ring at low opacity. Plate flecks/patina optional.
- The limerick's scene is the vignette: the mascot (or its signature
  absence — the empty chair reads louder than the dongle) in one
  deadpan office moment. Gradients + translucent shading, warm dark ink.
- Caption stack: the punch line as `Key line` ~23pt, tracking ≈150,
  around y≈862 in a soft tint; `NAME` ~58pt at y≈930; role/epithet
  ~20pt, tracking ≈190, at y≈968 — all Virelai Sans, centred.
- Slug is `lim-NNNN-<mascot-slug>`, NNNN the mascot's own archive number,
  zero-padded to four digits (`lim-0018-404sy-mclostalot`,
  `lim-0446-climate-cliff`).
- Driver `work/limericks/draw_<slug>.py` → `d.finish("<slug>-V1R00")`;
  commit `.vectorcraft`, `.svg`, `@2x.png`. Floor/furniture bands near the
  lower rim must close on the disc's own arc (`A420,420 0 0 1 …`).

## Leaf briefs

Wave 1 covered M-0018 and the whole M-0436–0446 office block. Wave 2 moves
along the unclaimed numbered cast — the 4xx/5xx doorkeepers and the
un-versified tech mascots — plus one form stretch.

| Slug | Subject | Mood / the drawing's job |
| --- | --- | --- |
| `lim-0400-bad-request-bob` | Bad-Request Bob, who returns every form unopened | Cheerfully unhelpful; Bob sliding a pristine envelope back across the counter |
| `lim-0403-htaccessius-the-doorman` | HTAccessius, doorman of the rewritten door | Velvet-rope officiousness; a guest list being edited as guests watch |
| `lim-0405-method-not-allowed-mel` | Method-Not-Allowed Mel, who permits exactly one gesture | Prim refusal; Mel holding up the single allowed hand sign |
| `lim-0418-teapotta-protocol` | Teapotta Protocol, the teapot that is technically a protocol | Steamy propriety; a teapot filing itself under BEVERAGES, LONG |
| `lim-0429-queue-matron` | Queue Matron, keeper of a queue that goes nowhere | Patient authority; numbered tickets curling like laurel |
| `lim-0502-bad-gateway-greg` | Bad-Gateway Greg, upstream of everything | Upstream gloom; Greg relaying a note he never read |
| `lim-0503-servicey-unavailabelle` | Servicey Unavailabelle, unavailable but impeccably polite | Apologetic absence; a desk bell beside a BACK SOON sign gathering dust |
| `lim-0504-unanswered-knock` | The Unanswered Knock | Hollow-door melancholy; the knock itself as a visible shape nobody turns toward |
| `lim-0937-blinko-chompframe` | Blinko Chompframe, the attention mascot | Caffeinated nostalgia; a marquee flicker caught mid-blink |
| `lim-0070-uncacheable-ursula` | Uncacheable Ursula, never stored, always fresh | Perishable glamour; Ursula stepping out of her own expiry date |
| `lim-0029-haikool-breeze` | Haikool Breeze — the haiku mascot gets a limerick | Cross-form mischief; a breeze that keeps overshooting seventeen syllables |
| `lim-0998-chain-of-custody` | Form stretch: a linked limerick chain | Relay-race blame; five small forms passing one error down the line, each verse handing off to the next |

## Guardrails

- Recheck `art/limericks/`, open/closed issues and open PRs before writing
  any leaf issue or claiming: mascot numbers above are proposals, and the
  numbered-cast roster in `PROMPTS.md` is historical.
- If a mascot already has a `mascots/` portrait, its silhouette should
  rhyme with that plate; no redesign inside a limerick.
- The chain piece (`lim-0998`) keeps the same caption stack — the five
  forms share one plate, one name, one epithet.
- Labels per `.github/LABELS.md`: `type:*` for the deliverable plus an
  explicit `work:*` intent per leaf.
