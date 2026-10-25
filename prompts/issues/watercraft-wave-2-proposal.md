# Watercraft — field plates, wave 2 (proposal)

Status: draft, not posted. Tracking-issue-ready proposal for a second
wave of watercraft field plates. Each proposed leaf issue is one new
piece, `<slug>-V1R00`, claimed and drawn independently.

## Coverage so far

The watercraft sub-series lives inside `art/vehicles/` and
`work/vehicles/`. Shipped so far — effectively wave 1: three
working/powered vessels in vehicles wave 1 (tugboat, paddle steamer,
flying boat) and three regional paddle craft from the
americas-and-islands batch (caballito de totora, Chono dalca, Samoan
paopao). Wave 2 deepens the vernacular-craft thread: skin, reed, plank
and dugout construction plus a few working and historical types.

## Format (field plates — watercraft)

- 1000×1000 canvas: dark moody backdrop → large gradient plate disc
  (center 500,460, r≈420) → the vessel → name in caps, Virelai Sans
  ~56–60pt at the bottom (y≈930).
- Profile or slight elevated near-profile so hull shape, waterline and
  any outrigger/float read; hull grounded on a chord of the disc,
  moving right unless the design reads better the other way. Water or
  reflection must end on the disc's actual arc.
- Second line is the construction/propulsion spec in caps, Virelai Sans
  ~22–24pt with wide tracking (y≈968), e.g. `DUGOUT · OUTRIGGER`,
  `PLANK-BUILT · PADDLE`. Keep it ≤760pt wide. No invented dates or
  engine specifications.
- Generic craft only: no real fleet names, flags, registry marks or
  ceremonial regalia.
- Oars, paddles, rigging, lashings and mast fittings are the
  thin-geometry trap: ≥3pt, checked at @2x.
- Gradients + translucent shading, never flat fills. Warm dark ink,
  never pure black.
- Deliverables: `art/vehicles/<slug>/<slug>-V1R00.vectorcraft` + `.svg`
  + `@2x.png`; driving script in `work/vehicles/`; the `.pdf` proof
  stays in `work/out/` (local only).
- Known trap: decorative shapes near the plate's lower edge must close on
  the disc's own arc (`A420,420 0 0 1 …`) or they leak past the rim.

## Proposed leaf issues

1. `coracle` — Watercraft — field plate: coracle. Round lath-and-hide
   river boat, one paddle worked over the bow. `HIDE · WILLOW LATH`
2. `kayak` — Watercraft — field plate: kayak. Low decked Inuit hunting
   kayak; cockpit, deck lashings and a double paddle. `SKIN · DRIFTWOOD`
3. `umiak` — Watercraft — field plate: umiak. Open Inuit skin boat,
   broad-beamed for crew and cargo — the kayak's open twin.
   `SKIN · LASHED FRAME`
4. `dugout-canoe` — Watercraft — field plate: Northwest Coast dugout
   canoe. Cedar dugout with a high flared prow; no outrigger — distinct
   from the paopao. `CEDAR · PADDLE`
5. `jangada` — Watercraft — field plate: jangada. Brazilian log
   fishing raft with a single lateen sail and a raised steering bench.
   `LOG RAFT · LATEEN`
6. `sampan` — Watercraft — field plate: sampan. Flat-bottomed Chinese
   river boat; stern scull (yuloh) and a bent mat canopy.
   `WOOD · STERN SCULL`
7. `junk` — Watercraft — field plate: junk. Chinese ocean junk: high
   stern, battened lug sails and a hung rudder. `TEAK · BATTENED LUG`
8. `felucca` — Watercraft — field plate: felucca. Nile lateen-rigged
   open sailboat, slim hull and long dipping yard. `PLANK · LATEEN SAIL`
9. `gondola` — Watercraft — field plate: gondola. Asymmetric Venetian
   rowing boat; ferro prow and the rower's aft station.
   `OAK · IRON FERRO`
10. `viking-longship` — Watercraft — field plate: longship.
    Clinker-built oared ship, square sail furled or set, shields along
    the rail. `OAK · SQUARE SAIL`
11. `dory` — Watercraft — field plate: banks dory. Stackable
    flat-bottomed fishing dory with flared sides and thwarts.
    `PINE · OARS`
12. `lightship` — Watercraft — field plate: lightship. Anchored light
    vessel: red hull, lantern mast and a daymark, moored not under way.
    `STEEL · MOORED`

## Notes

- Recheck `art/vehicles/`, open/closed issues and open PRs before
  posting each leaf; proposal ≠ reservation.
- Regional craft follow the americas-and-islands guardrails: keep place
  and community names specific, do not merge traditions (a PNW dugout is
  not a paopao; a tankwa is not a caballito), no invented ceremonial
  context or regalia.
- Held for a later wave: currach, whaleboat, narrowboat, racing shell,
  Micronesian proa, Ethiopian tankwa, ice yacht, hydrofoil.
