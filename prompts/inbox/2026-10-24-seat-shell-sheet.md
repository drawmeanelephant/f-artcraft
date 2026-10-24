## seat-shell-V1R00 — framing the seat; an issue/spec drift worth noting

- Kind: lesson
- Source: issue #1262; driver `work/virelai/draw_seat_shell.py`, native +
  exports `virelai/design/seat-shell/seat-shell-V1R00.*`
- Applies to: the virelai figcraft sheets and any seat-chrome drawing
- Status: pending

### Evidence

Six 1280×720 frames on one sheet canvas (4008×1628): desktop at rest,
chrome anatomy, menubar+menu, notifications, lock curtain, welcome tour.
Geometry is copied from `gotabwm` sources (rail 22, ChromeH/W 20/148,
FocusW 216, godMenuW 96, tour 512×384) so the sheet is citable.

Two useful catches:

- **Issue drift:** #1262 asks for a "left tab rail", but the shipped seat
  paints the tab strip across the *top* (`RailHeight = 22`,
  `site/desktop.md`: "the rail — the tab strip across the top"). The
  sheet draws the shipped geometry and notes it — a design doc that draws
  unshipped chrome as fact would be worse than the drift. If a left rail
  is a desired direction, it wants its own issue framed as a proposal.
- **Welcome tour is a real app**, not an overlay: GOWELCOME.ELF
  (`user/go/welcome/`) is a 512×384 tabapp surface exec'd on first boot —
  five gesture chips + four launcher buttons, content pinned by host
  tests. Drawing it as a centered window in a normal viewport is honest.

Reusable bits for later sheets: the `rail()`/`dockband()`/`toast()`/
`fake_shadow()` helpers in the driver are copy-pasteable into #1263's app
frames.

### Proposed change

None to shared rules. If #1263 lands app frames, reuse the seat-chrome
helpers verbatim rather than redrawing the rail.
