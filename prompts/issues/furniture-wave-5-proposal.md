# Furniture — field plates, wave 5 (proposal)

Status: draft, not posted. Tracking-issue-ready proposal for wave 5 of the
furniture field-plate series. Each proposed leaf issue is one new piece,
`<slug>-V1R00`, claimed and drawn independently.

## Coverage so far

Waves 1–4 plus the regional batch have shipped ~100 plates: heavy on
Euro-American seating, storage, tables and lamps, with a recent regional
addition (silla matera, Sarchí rocker, Masaya hammock, Jardín taburete,
Orkney chair, kali headrest). Open: wave 4 tracker #1208 and leaf #1237
(library globe). Wave 5 widens the vocabulary further — Asian joinery
types, African and Levantine forms, and vernacular storage — still as
generic type specimens, never attributed to makers or museums.

## Format (field plates — furniture)

- 1000×1000 canvas: dark moody backdrop → large gradient plate disc
  (center 500,460, r≈420) → the piece → name in caps, Virelai Sans
  ~56–60pt at the bottom (y≈930).
- Near-side view with a slight three-quarter so depth reads, seated on a
  soft shadow ellipse that hugs the disc. Nothing touches the rim.
- Second line is the material list in caps, Virelai Sans ~22–24pt with
  wide tracking (y≈968), e.g. `OAK · CANE · BRASS`. Keep it ≤760pt wide.
- Generic type names only — no manufacturer names, badges or designer
  attributions.
- Spindles, stretchers, cane webbing, lashings and thin metal frames are
  the thin-geometry trap: ≥3pt of stroke, checked at @2x.
- Gradients + translucent shading, never flat fills. Warm dark ink, never
  pure black.
- Deliverables: `art/furniture/<slug>/<slug>-V1R00.vectorcraft` + `.svg`
  + `@2x.png`; driving script in `work/furniture/`; the `.pdf` proof
  stays in `work/out/` (local only).
- Known trap: decorative shapes near the plate's lower edge must close on
  the disc's own arc (`A420,420 0 0 1 …`) or they leak past the rim.

## Proposed leaf issues

1. `horseshoe-armchair` — Furniture — field plate: horseshoe-back
   armchair. Chinese chair with a continuous bent crestrail flowing into
   the arms over an S-curved splat. `ELM · CANE`
2. `kaidan-tansu` — Furniture — field plate: kaidan tansu. Japanese
   staircase chest: stepped carcass of mixed-size drawers with iron
   corner hardware. `PAULOWNIA · IRON`
3. `bandaji` — Furniture — field plate: bandaji. Korean blanket chest
   with a fall-front flap and bat-wing brass hinges. `PINE · BRASS`
4. `charpai` — Furniture — field plate: charpai. Indian rope bed: a
   woven jute grid tensioned over turned legs, read as a springy surface
   not a flat net. `WOOD · JUTE`
5. `ashanti-stool` — Furniture — field plate: Ashanti stool. Ghanaian
   stool carved from one block: concave seat over a pierced central
   support. `CARVED WOOD`
6. `butaka` — Furniture — field plate: butaka. Philippine planter's
   chair whose long armrests double as leg rests over a cane seat.
   `HARDWOOD · CANE`
7. `vargueno` — Furniture — field plate: vargueño. Spanish fall-front
   cabinet on an open trestle stand, iron lock and corner fittings.
   `WALNUT · IRON`
8. `kubbestol` — Furniture — field plate: kubbestol. Norwegian chair
   hollowed from a single log with a plank back; mass is the drawing.
   `PINE`
9. `welsh-dresser` — Furniture — field plate: Welsh dresser. Open
   plate-rack upper stage over a cupboard-and-drawer base. `OAK`
10. `pie-safe` — Furniture — field plate: pie safe. Punched-tin panel
    food safe; the tin's punched pattern carries the drawing.
    `PINE · TIN`
11. `kotatsu` — Furniture — field plate: kotatsu. Low table frame
    quilted under a thick blanket, brazier hinted beneath. `WOOD · TEXTILE`
12. `syrian-inlaid-table` — Furniture — field plate: inlaid octagonal
    table. Levantine side table with mother-of-pearl and bone marquetry.
    `WALNUT · MOTHER-OF-PEARL`

## Notes

- Recheck `art/furniture/`, open/closed issues and open PRs before
  posting each leaf; proposal ≠ reservation.
- Regional types need a specific structural reference (see the guardrails
  in `prompts/themes/americas-and-islands.md`): study construction, do
  not trace a living artisan's design or invent ceremonial context.
- Held for a later wave: lit clos, prie-dieu, washstand, icebox,
  caquetoire, sōban tray table, gyeongsang desk.
