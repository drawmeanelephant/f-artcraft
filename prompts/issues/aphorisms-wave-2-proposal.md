# Aphorisms — wave 2 proposal

Status: draft, not posted. Expansion proposal for `art/aphorisms/`. Each
row below is a **separate leaf-issue candidate**, not one task — the wave
splits into individual `Aphorism graphic: <Name> — motivational poster`
issues when approved.

## Format reminder (from shipped wave 1)

Per `work/aphorisms/draw_aph_003_blamey_mctypoface.py` and siblings:

- Canvas 1000×1000. Dark backdrop gradient, plate ellipse `x=80 y=40
  w=840 h=840` (centre 500,460, r≈420), ~6pt rim stroke, 792×792 inner
  ring, optional patina/flecks.
- The vignette is a bureaucratic scene in progress — a routing slip
  stamped mid-impression, papers flying between cabinets, a scapegoat
  badge. Warm bureau palette is precedent, not required; gradients and
  translucent document layers throughout.
- Caption stack: the aphorism as two `Key line`s ~22pt, tracking ≈110,
  around y≈738/772 in a light tint; `NAME` ~56pt at y≈905;
  role/epithet ~18pt, tracking ≈160, at y≈950 — Virelai Sans, centred.
- Slug is `aph-NNN-<mascot-slug>`, NNN the mascot's archive number
  (`aph-008-cssandra-cascade`, `aph-067-vexsys-antagon`).
- Driver `work/aphorisms/draw_<slug>.py` → `d.finish("<slug>-V1R00")`;
  commit `.vectorcraft`, `.svg`, `@2x.png`. Stamp impressions may tilt
  via `transform` rotate, as shipped.

## Leaf briefs

Twenty-seven plates shipped (M-003 through M-067). Wave 2 stays in the
numbered cast and picks the un-aphorised mascots whose job already sounds
like a proverb.

| Slug | Subject | Mood / the drawing's job |
| --- | --- | --- |
| `aph-007-crashy-mcthinkslow` | Crashy McThinkslow, the timeout guru | On slowness as caution; a progress bar meditating beside an expired stopwatch |
| `aph-009-draft-file-derrick` | Draft-File Derrick, who ships only drafts | On the permanence of provisional things; a final-final-v2 stack leaning like a tower |
| `aph-010-forbiddy-noentry` | Forbiddy Noentry, the boundary keeper | On gates guarding empty rooms; a velvet rope across an open field of paper |
| `aph-011-formee-formeson` | Formee Formeson, born of a form | On paperwork as lineage; a form whose parent field is itself a form |
| `aph-014-htmlie-structura` | HTMLie Structura | On bones before paint; a skeleton of nested frames holding up one small ornament |
| `aph-018-kafkey-errorhandler` | Kafkey Errorhandler | On grace under stack trace; a net calmly catching falling exception slips |
| `aph-020-maila-delayden` | Maila Delayden | On lateness as timing; a letter arriving at exactly the wrong, therefore right, moment |
| `aph-042-robots-dot-txt` | Robots Dot Txt, the polite exclusion | On rules everyone reads and few obey; a small PLEASE KEEP OFF sign on fresh paper grass |
| `aph-044-spooler-gremlin` | Spooler Gremlin, hoarder of the print queue | On jobs saved for a better tomorrow; a queue of pages queuing for the queue |
| `aph-048-twiggy-snipsnark` | Twiggy Snipsnark | On marginalia as mercy; scissors paused above a comment that deserved it |
| `aph-053-tabby-fields` | Tabby Fields, the field-tabbing familiar | On order imposed by the tab key; pawprints landing on successive field boxes |
| `aph-070-uncacheable-ursula` | Uncacheable Ursula | On freshness versus memory; a mirror that declines to keep yesterday |

## Guardrails

- Recheck `art/aphorisms/`, open/closed issues and open PRs before
  writing any leaf issue or claiming; aphorisms already shipped for
  M-003–008, 012, 016–019, 026–028, 030–037, 039–041, 046, 050, 057
  and 067 are off the list.
- The aphorism earns the scene: write the two-line saying first, then
  find the bureaucratic tableau that makes it literal. No mascot needs
  a face if the prop carries the joke.
- Numbers above are proposals — if a leaf brief finds its mascot
  renumbered or already taken, pick the next free `aph-NNN`.
- Labels per `.github/LABELS.md`: `type:*` for the deliverable plus an
  explicit `work:*` intent per leaf.
