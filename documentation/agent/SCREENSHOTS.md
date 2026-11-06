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

## Capture works. 129 real screenshots, headless, at a known commit

**Resolved on 2026-11-01.** The SDL simulator builds here, and the application has a
**built-in screenshot tour**: `GUPPY_SIM_SHOTS=<dir>` walks every page and state, writes a
binary PPM of each, and exits. It captures a copy of the LVGL framebuffer rather than a
window, so no display server is needed - `SDL_VIDEODRIVER=offscreen` is enough. The tour also
suppresses the simulator's demo data, prompts and notifications, so output is clean and
repeatable.

That produced **128 screenshots at 480x272** - the KE's real panel resolution - currently from
commit **`3194104`**, re-captured on 2026-11-01 when the screen tip moved.
`wiki/images/screenshots.json` records the commit, the source, the caveat and the one
exclusion.

### The captures are reproducible, and that was measured

Running the tour twice against the same build gives **128 of 129 byte-identical** images. That
matters: it is what makes comparing two commits' captures a usable way to find stale
screenshots. Without reproducibility the comparison is noise.

### The one exclusion: `07-updates.png`

The Updates page is **timing-dependent and is not published**.

It came to light the right way round. When the screen tip moved from `94869f7` to `3194104`,
re-capturing and comparing showed exactly one image changed - `07-updates.png` - which looked
like a real UI change from the two new commits. Running the tour twice against *the same*
build showed the same image differing again. So it was never a code change; it was
non-determinism.

The cause: the Updates panel disables its buttons while it waits for a reply from Moonraker's
update manager. With no Moonraker there is no reply, so whether the capture lands in the busy
state or the idle state depends on timing. The differing region is exactly where the **Check
now** and **Update all** buttons sit.

Publishing it would have shown a reader greyed-out buttons that are **not** greyed out on a
real printer - a picture that contradicts the page it illustrates. The `Updating-NebulaOS`
page describes that greying-out in words instead.

This is the general caveat below made concrete: panels that depend on a live printer cannot be
captured truthfully here, and a plausible-looking screenshot is the most convincing way to
publish something false.

Coverage is better than a panel count suggests, because the tour captures *states*, not just
screens: confirmation dialogs, refusals, in-progress, failed, rolled-back, and step-by-step
calibration sequences. That is what the mission asks for - starting state, navigation,
selection, input dialog, confirmation, progress, completion, error states - rather than one
image per page.

Reproduce with `documentation/agent/tools/capture_screenshots.sh <screen-checkout> <out>`.

### What this is, and what it is not

**It is** real UI, rendered by the real application, at a recorded commit. Not a mockup, not
an image model, not a memory.

**It is not hardware.** Two limits matter:

- The `machine.nebulaos.*` methods only exist on a real NebulaOS printer. Against no Moonraker
  those panels show errors or empty values, so OS-settings screens captured here must not be
  presented as a working printer.
- The boot and init screens are outside the tour, so a printer's very first start cannot be
  captured this way. That needs a photograph of real hardware, and the install page says so.

### Three things that blocked the build, for whoever does this next

1. **`-static` in the default `LDFLAGS` cannot work here.** There is no static SDL2, and
   `/usr/lib/libSDL2-2.0.so.0` is 32-bit i386 so it cannot satisfy a 64-bit link. A 64-bit
   SDL2 does exist in `/lib64`, and a non-static link finds it.
2. **Submodules cannot be fetched into a git worktree here.** `git submodule update --init`
   registers URLs in the *parent* repository's `.git/config`, which lives in the foreground
   checkout and is correctly write-protected for this agent. Use a separate
   `git clone --recurse-submodules` into the agent's own area.
3. **Apply the two submodule patches first** (`0002-spdlog_fmt_initializer_list`,
   `0003-lvgl-dpi-text-scale`) or the build fails in spdlog.

Also: the app aborts at startup if the directory holding `log_path` does not exist, and the
error (`spdlog_ex: Failed opening file`) does not obviously say so.

## The older images, and why they are not used

### `wiki/images/` in the NebulaScreen repository - 26 images, superseded

Captured **2026-07-01**, four months before the commit documented here. They were candidates
while nothing better existed. Now that 129 images exist from the exact documented commit,
they are superseded and not used.

### `screenshots/` - 13 images, not usable

Committed **2025-08-20** in `91302a4` ("Drop Android support"), predating the NebulaScreen
rename. These show the upstream GuppyScreen application; using them would misattribute
upstream UI to NebulaOS.

## Status

Generated figures are in `COVERAGE.md`. In summary, as of 2026-11-01:

| Measure | Count |
|---|---|
| Screenshots captured from commit `3194104` | **128** |
| Panels with at least one capture | 36 of 49 |
| Panels with no capture yet | 13 |
| Excluded as timing-dependent | 1 (`07-updates.png`) |
| Images embedded in manual pages so far | 11 |

Having 129 images available is not the same as a manual that uses them. Only 7 are embedded so
far, and the gap between those two numbers is the honest measure of how much of the visual
work is left.

The 13 panels without a capture: `boot_logo_panel` and `init_panel` (outside the tour - they
need real hardware), plus `exclude_object_panel`, `filament_runout_panel`, `logs_panel`,
`network_detail_panel`, `printer_select_panel`, `prompt_panel`, `report_panel`,
`spoolman_panel`, `static_ip_panel`, `storage_panel`, `tmc_tune_panel`. Most are reachable
with the existing `sim_*` hooks and need an extra tour step or a manual run.

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

### Next steps

1. Embed captures into pages as each is drafted. 7 of 129 are in use.
2. Cover the 13 panels the tour misses. Most need only an extra tour step.
3. Re-run the capture whenever the screen repository's tip moves, and compare. **Done once
   already**, for `94869f7` -> `3194104`: 128 identical, 1 difference that turned out to be
   non-determinism rather than a code change. When comparing, run the tour twice against the
   same build first - otherwise a flaky image is indistinguishable from a real UI change, and
   you will "discover" changes that did not happen.

Building the simulator in this agent's own worktree is permitted. Firmware builds are not.

## Run 23 captures embedded (2026-11-05)

Source: `_scratch/run23/wiki-shots/` (main session). 17 files copied into `wiki/images/`:

- `p-*.png` - exact framebuffer grabs from ke-dev's own display (1.0.0 `ba98eec`, screen
  `36490ed`, hardware profile `screen-grab`): `p-updates.png` (from `printer/updates.png`),
  `p-mcu-firmware.png` (from `printer/mcu-firmware.png`). Captioned "the printer's own display".
- `r-*.png` - the real NebulaScreen `123ef31` as the simulator, fed only from ke-dev's redacted
  API snapshot (MANIFEST.md there). Captioned "the real screen app, showing data from a printer".
  `r-exclude-object`, `r-prompt-m600`, `r-filament-runout` are synthetic states and say so.

Deliberately not used: `L61-image.png` (0.9.9 test build in slot A), `not-for-wiki/L34-logs.png`
(false "No log files found"), `L42-statistics.png` (shows the 16-vs-20 count bug tracked for
1.0.1), `L01-home` / `L02-print-files` (real+ gaps; the existing `m01`/`m09` are better),
`L41-mcu` and `L60-updates` (the real-display `p-` grabs replace them), `L51-camera` (`41-camera`
already in use). Still missing: first-boot screen (Tim deferred), boot logo panel,
TMC tune.

## 1.0.1 real-display grabs (2026-11-05)

Source: `_scratch/run23/printer-101/` (main session; ke-dev on 1.0.1, firmware `2074c34`, screen
`fd47cb6`; checked by the main session for private data). Copied as `p-logs.png` (Screen-Reference
System, closes the Logs "Not yet"), `p-statistics.png` (replaces the example-data `20a-statistics`
in the Statistics panel; 20 prints = 7 done + 9 cancelled + 4 failed), `p-bed-tram-start.png`
(replaces the simulator `m40-tram-idle` on Bed-Tramming) and `p-bed-tram-start-confirm.png`.
Captioned "the real screen on a printer running NebulaOS 1.0.1". `20a-statistics.png` and
`m40-tram-idle.png` stay in `images/` but are no longer embedded. Later the same day: `p-spoolman-spools.png` (from `grab-5.png`, the Spoolman spool list;
Filament and the Screen-Reference Spoolman panel, closes that "Not yet").

## Run 23 rounds 1-3 embedded (2026-11-05, second batch)

Source: `_scratch/run23/wiki-shots/` (MANIFEST.md there; screen `123ef31` + unpushed sim-only
tour commits, mock Moonraker on the redacted ke-dev snapshot). 53 files copied into
`wiki/images/` under descriptive names: the MANIFEST name without its `Lxx-` prefix
(`L52-boot-logo.png` -> `boot-logo.png`). `boot-logo-delete-confirm.png` is L57a cropped with
PIL to the dialog border (29,70)-(451,202), which removes the mock's refusal text behind it.
Every image was looked at for a real SSID, 192.168.0.x, MAC or serial: none (names are the
snapshot's HomeWiFi stand-ins, addresses 192.168.1.x / 127.0.0.1).

Fed states are captioned "An example state ... fed in for the picture": print-cancel-confirm,
exclude-object-confirm, unavailable-while-printing, plr-resume-offer, static-ip-invalid,
wifi-password, 03-wifi (fed scan), spoolman-save-confirm, download-progress/-stopped/-done,
after-clean-reset-notice. online-up-to-date is derived (captioned as the same check answered
by 1.0.0).

Skipped: L1F (not clean), L61 (0.9.9 build in slot A), L13/L14/L15 (background says
"calibration not available"; L13 shows a stray background letter between its buttons even when
cropped, L14/L15 hide their last warning line behind the buttons), L42 (16-vs-20 count bug,
see earlier), L60 / L41 (the real-display p- grabs cover them), L01 / L02 / L1G (real+ gaps;
m01 / m09 / m07 stay), L51 (41-camera stays), not-for-wiki/L34. Identical to images already
in wiki/ (md5): L04 L05 L06 L17 L1H L20 L21 L22 L23 L27 L30 L31 L32 L33 L35 L40 L50 L70 L73.

## Restructure (2026-11-06)

No new images. Images moved with their sections: the Screen-Reference sections into
`Screen-*.md` (one page per tab / Settings tile), the calibration pages' images into
`Calibration-Explained.md`, Connecting-To-WiFi's into `First-Time-Setup.md`, Filament's load
images into `Printing.md`. `m40-tram-idle.png`, `20a-statistics.png`, `m01`-era duplicates stay
in `images/` unused. The older `m*` simulator images (screen `36490ed`) were kept where they
were; they were not re-checked against 1.0.1 one by one.

