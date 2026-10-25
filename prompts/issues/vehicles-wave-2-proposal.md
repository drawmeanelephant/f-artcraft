# Vehicles — field plates, wave 2 (proposal)

Status: draft, not posted. Tracking-issue-ready proposal for wave 2 of
the vehicle field-plate series. Each proposed leaf issue is one new
piece, `<slug>-V1R00`, claimed and drawn independently.

## Coverage so far

Wave 1 shipped sixteen plates: rail (steam locomotive, streetcar), road
(double-decker bus, city taxi, fire engine, pickup truck, camper van,
rear-engined coupe, land-speed streamliner, cargo bike, sidecar
motorcycle), air (biplane, flying boat, rigid airship) and two working
vessels (tugboat, paddle steamer). The roster is twentieth-century and
industrial. Wave 2 fills in human-powered and early machines, regional
work vehicles, micro-vehicles and the odd rotorcraft.

Watercraft continue to live under `art/vehicles/` (see the separate
`watercraft-wave-2-proposal.md`); this wave stays on land and air.

## Format (field plates — vehicles)

- 1000×1000 canvas: dark moody backdrop → large gradient plate disc
  (center 500,460, r≈420) → the vehicle → name in caps, Virelai Sans
  ~56–60pt at the bottom (y≈930).
- Profile view, wheels, runners or hull grounded on a chord of the disc,
  facing right unless the design reads better the other way.
- Second line is the spec in caps, Virelai Sans ~22–24pt with wide
  tracking (y≈968), e.g. `1929 · COAL-FIRED 4-6-2`. Keep it ≤760pt
  wide. Human-powered and pre-industrial craft take a construction or
  propulsion spec instead of a year.
- Generic liveries, blank destination blinds — no real operator marks,
  manufacturer badges or racing numbers of actual vehicles.
- Glazing is translucent so the backdrop reads through; chrome is a
  gradient, never a white bar. Spokes, rigging, bracing, lashings and
  grille slats are the thin-geometry trap: ≥3pt, checked at @2x.
- Gradients + translucent shading, never flat fills. Warm dark ink,
  never pure black.
- Deliverables: `art/vehicles/<slug>/<slug>-V1R00.vectorcraft` + `.svg`
  + `@2x.png`; driving script in `work/vehicles/`; the `.pdf` proof
  stays in `work/out/` (local only).
- Known trap: decorative shapes near the plate's lower edge must close on
  the disc's own arc (`A420,420 0 0 1 …`) or they leak past the rim.

## Proposed leaf issues

1. `penny-farthing` — Vehicles — field plate: penny-farthing.
   High-wheel bicycle; one huge front wheel and a tiny rear wheel are
   the whole silhouette. `1870S · DIRECT-DRIVE`
2. `auto-rickshaw` — Vehicles — field plate: auto rickshaw.
   Three-wheeled taxi: scooter nose, canopy top, open sides.
   `1960S · TWO-STROKE`
3. `qamutik` — Vehicles — field plate: qamutik. Inuit freight sled;
   lashed runners and crossbars flex over the ice — no rigid joinery.
   `DOG-DRAWN · LASHED WOOD`
4. `stagecoach` — Vehicles — field plate: stagecoach. Horse-drawn road
   coach slung on thoroughbraces, driver up on the box. `1860S · COACH`
5. `sedan-chair` — Vehicles — field plate: sedan chair. Enclosed
   carried chair on twin poles; window glass and pole-holders read at
   plate scale. `1700S · TWO-BEARER`
6. `traction-engine` — Vehicles — field plate: traction engine. Steam
   road engine: flywheel, canopy and chimney over a front tender.
   `1900S · STEAM`
7. `brass-era-tourer` — Vehicles — field plate: brass-era tourer. Open
   touring car with brass lamps and radiator, fabric top folded.
   `1912 · SIDE-VALVE FOUR`
8. `bubble-car` — Vehicles — field plate: bubble car. Egg-shaped
   microcar with a front-hinged door; three-quarter profile is allowed
   to show the hinge line. `1950S · SINGLE-CYLINDER`
9. `motor-scooter` — Vehicles — field plate: motor scooter.
   Step-through scooter: leg shield, floorboards and small wheels.
   `1950S · 150CC`
10. `milk-float` — Vehicles — field plate: milk float. Battery-electric
    doorstep float with an open cab and crate racks. `1960S · ELECTRIC`
11. `autogyro` — Vehicles — field plate: autogyro. 1930s rotorcraft;
    unpowered overhead rotor plus a pusher prop. `1930S · AUTOROTATING`
12. `caboose` — Vehicles — field plate: caboose. Freight-train tail
    car; cupola, end platforms and marker lamps. `1920S · WOOD CUPOLA`

## Notes

- Recheck `art/vehicles/`, open/closed issues and open PRs before
  posting each leaf; proposal ≠ reservation.
- Vernacular craft (qamutik, sedan chair) follow the regional
  guardrails: specific construction references, no invented ceremonial
  context.
- Held for a later wave: conestoga wagon, streamlined diesel train,
  funicular, wood-framed station wagon, utility jeep, hovercraft.
