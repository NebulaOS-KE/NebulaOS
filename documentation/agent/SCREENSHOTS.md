# Screenshot inventory

The end-user manual has to be genuinely visual - a beginner following a procedure needs to
see the screen they are looking at. This file tracks what is needed, what exists, what can be
trusted, and what cannot be captured.

## Rules

Real captures only, from one of three sources, in this order of preference:

1. Real NebulaOS hardware, when authorised. **Not available to this agent** - see
   `BLOCKERS.md` B-001.
2. The actual NebulaScreen application running in the SDL simulator, built from a recorded
   commit.
3. Existing repository images - **but only after confirming they match the version being
   documented.** That condition is doing real work here; see below.

Never from an image model. Never recreated from memory. Never with edited labels or invented
application states. An image that lies is worse than an image that is missing.

## What exists today, and what it is worth

Two sets of real screenshots exist in `NebulaOS-nebulascreen`. Neither can be used yet, for
different reasons.

### `wiki/images/` - 26 images, candidates

| | |
|---|---|
| Count | 26 PNGs |
| First committed | **2026-07-01** |
| Last touched | 2026-10-21 (`0929bb3`, a wording pass) |
| Version documented by this manual | NebulaScreen `v0.9.3`, commit `94869f7` |
| Status | **Candidates, unconfirmed** |

These are genuine captures of real panels - home tab, bed mesh and its 3D view, file browser,
fan, LED, filament, homing, Z offset, console, Spoolman, TMC, skew, axis twist and more. They
are referenced by five existing wiki pages.

The problem is the four-month gap between when they were captured and the commit this manual
documents. Four months of active development on a UI is long enough for labels, layouts and
whole panels to have moved. The mission's condition for reusing existing images is confirming
they match the documented version, and **that confirmation has not been done** - it needs the
UI running side by side with the images.

So they are recorded as candidates, not as coverage. Using them now would mean shipping a
beginner's manual whose pictures might not match the screen in front of the reader, which is
precisely the failure a screenshot is supposed to prevent.

### `screenshots/` - 13 images, not usable

| | |
|---|---|
| Count | 13 PNGs |
| Provenance | Committed **2025-08-20**, in `91302a4` ("Drop Android support") |
| Status | **Stale - upstream GuppyScreen era** |

Over a year old and predating the NebulaScreen rename. These show the upstream application,
not this one. They are not candidates for the manual, and using them would misattribute
upstream UI to NebulaOS.

## Status

| Measure | Count |
|---|---|
| Required (inventory items) | 59 |
| Captured and confirmed current | **0** |
| Candidates needing version confirmation | 26 |
| Stale, not usable | 13 |
| Missing outright | 59 |

The "captured" figure stays zero until something is confirmed against the running UI. A
candidate is not coverage.

## Capture method: where this stands

**The simulator is the realistic route, and it is not ruled out.** Findings so far:

- SDL2 development libraries are **available** here (`sdl2-config` present, pkg-config
  reports 2.32.70), and `make`, `g++` and `cmake` are all installed.
- The repository builds as an SDL simulator with a plain `Makefile`, and
  `GUPPY_SMALL_SCREEN=1` gives the KE's real 480x272 layout rather than an 800x480 window.
- **The simulator has purpose-built hooks for exactly this job.** Panels expose `sim_*`
  methods under the `SIMULATOR` define for driving the UI to a specific state without a
  printer - for example `sim_tap_row(i)`, `sim_show_row(i)`, `sim_keypad()`, `sim_type(keys)`,
  `sim_open_graph(i)`, `sim_running(heater)`, `sim_camera_present(bool)`. That is the
  difference between reproducible capture and clicking around by hand.
- **The blocker is submodules.** `lvgl`, `lv_drivers`, `libhv` and `spdlog` are declared in
  `.gitmodules` but are **empty** in the workspace checkout. A simulator build needs them
  fetched first.

Two further things to know before attempting it:

- The program **crashes at startup if the directory in `log_path` does not exist**, so the
  config and its directories must be created before the first run.
- The `machine.nebulaos.*` methods only exist on a real NebulaOS printer. Against any other
  Moonraker - or none - the NebulaOS settings panels show errors or empty values, so those
  particular screens cannot be captured truthfully in the simulator. A virtual Klipper
  printer covers the ordinary printing screens but not the OS settings ones.

### Next step

Fetch the submodules into a dedicated worktree, build with `GUPPY_SMALL_SCREEN=1`, and try to
drive one known panel and capture it. Record the answer here either way: a clear "not possible
in this environment" is worth as much as a yes, because it turns 59 silent gaps into a named
blocker with a reason.

Building the simulator in this agent's own worktree is permitted. Firmware builds are not.
