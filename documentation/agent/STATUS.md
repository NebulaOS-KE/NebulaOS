# Status

**Updated:** 2026-11-01 (morning)
**Phase:** 3 - developer wikis (extensions reference done; five repositories to go)
**Branch:** `docs/agent` in the central `NebulaOS` repository
**Mode:** autonomous, self-paced loop

## Where things stand

The agent's own infrastructure is in place and discovery has run over commands,
configuration, screens, services, the public API, the build pipeline, the developer tooling
and the runtime helpers. There are **510 discovered documentation items** in
`coverage.jsonl`, every one of them recorded against the exact commit it was found at, and
every one of them currently `missing` - which is the honest starting position. No
documentation pages have been written yet.

The dashboard in `COVERAGE.md` is generated from the inventory by script, so it cannot drift
from reality.

## Repositories discovered

All eight repositories in the GitHub organisation, with their default branch tips as fetched
today:

| Repository | Default branch | Tip commit | Wiki enabled | Local checkout |
|---|---|---|---|---|
| `NebulaOS` | `main` | `bef8693` | yes | cloned into the docs worktree |
| `NebulaOS-firmware` | `main` | `82e1320` | yes | yes |
| `NebulaOS-nebulascreen` | `main` | `94869f7` | yes | yes |
| `NebulaOS-klipper-extensions` | `main` | `8e3447a` | **no** | yes |
| `NebulaOS-klipper-mcu` | `main` | `33f5d16` | yes | yes |
| `NebulaOS-kernel` | `openke` | `d86790d` | yes | yes |
| `nebulaos-packages` | `main` | - | yes | no |
| `lv_drivers` | `master` | - | yes | no |

Every local checkout is exactly at its origin tip, so today's discovery reads the newest
code with no reconciliation needed.

## What discovery found

- **49 NebulaScreen panels** - the real user-facing screen list, from `src/*_panel.cpp`.
  This is the backbone of the complete screen reference and of the screenshot plan.
- **35 firmware boot services** - `S00`-`S99` init scripts in the firmware overlay,
  covering boot, Wi-Fi, MCU guarding, update supervision, recovery and housekeeping.
- **51 registered G-code commands** across the Klipper extensions. 43 are registered with
  a literal name; the remaining 8 are assembled from module constants and were resolved by
  reading each module, with the constant recorded next to the name so the mapping can be
  re-checked rather than trusted.
- **172 configuration options** - 152 Klipper extension settings with their declared type,
  and 20 real NebulaScreen settings.
- **30 Klipper extension modules** with **31 test files** beside them - roughly one test
  module per extension, which is unusually good coverage for this kind of code and makes
  `verify_test` genuinely achievable rather than aspirational.
- **34 existing end-user wiki pages** in `NebulaOS-nebulascreen/wiki/`, plus roughly 70
  design and analysis documents in `NebulaOS-firmware/docs/`. Substantial material to reuse
  rather than replace.

## The public API, and the flow behind it

The most valuable find so far. NebulaOS has a real, deliberate public API surface: **56
Moonraker endpoints** under `machine.nebulaos.*`, served by a Moonraker component that ships
inside the firmware overlay at
`scripts/build/overlay/usr/lib/nebulaos/moonraker/nebulaos.py`. Moonraker exposes each HTTP
path `/machine/nebulaos/x/y` as the JSON-RPC method `machine.nebulaos.x.y`, which is how
NebulaScreen addresses them. One notification, `nebulaos:settings_changed`, is published
alongside them.

They cover network and Wi-Fi, the boot display, logs, storage, cleanup, display brightness
and sleep, Spoolman, the camera, system clean-reset and slot swap, system image install,
OTA, MCU flashing, update readiness and the screen's own build report.

The end-to-end flow, which is exactly the kind of cross-repository path the mission asks to
be documented:

```
NebulaScreen panel
  -> Moonraker JSON-RPC  machine.nebulaos.*
  -> nebulaos.py Moonraker component  (in Moonraker's own process - no second daemon)
  -> /usr/libexec/nebulaos/nebulaos-osconfig  (argv only, one JSON object back, validated, atomic)
  -> nebulaos_osconfig/*.py  (17 helper modules: wifi, network, camera, ota, image, mcu, ...)
```

The component is composed into the Moonraker checkout by the `S05nebulaos-activate` boot
service as an excluded symlink - the same mechanism NebulaOS uses for its Klipper extras -
and is configured by a `[nebulaos]` section in
`/etc/nebulaos/moonraker/nebulaos.conf`. If that file is absent, Moonraker simply runs
without the component. That is worth documenting precisely: it is the difference between a
printer that shows OS settings and one that does not.

### Cross-check result

The registration table was taken as authoritative rather than the UI's call sites, then the
two were compared:

- Every one of the **54** methods NebulaScreen calls is actually served. No phantom calls,
  so no page will describe a method that does not exist.
- **2** endpoints are served but never called by the UI: `machine.nebulaos.ota.discard` and
  `machine.nebulaos.system.notify_refused`. They are still public API and will be documented
  as such, with a note that the shipped UI does not exercise them.

That asymmetry is the reason to inventory from the server side. Had this been discovered from
the UI instead, those two would have been invisible.

## Shipping pins worth knowing

From `NebulaOS-firmware/manifests/dependencies.conf` at `82e1320`:

- NebulaOS version `0.9.0`, UI API `1`
- NebulaScreen pinned at `94869f7`, which **is** the current `main` tip
- Kernel pinned at `d86790d` on `openke`, which **is** the current tip
- Klipper extensions pinned to branch `production` at `31d6d65`, while `main` is at
  `8e3447a`. The gap is **CI and README only** - `.github/workflows/tests.yml`,
  `scripts/ci-tests.sh` and a README edit, verified with
  `git diff --name-status origin/production origin/main`. Nothing under `extras/` differs,
  so the two branches are identical in runtime code and every documented extension
  behaviour is shipped behaviour. Pages carry a footnote with the pin SHA, not a
  development-only warning (see `DECISIONS.md` D-002)
- Host Klipper is pristine upstream `Klipper3d/klipper` at `58bd67d`, not a fork

## A discovery mistake worth recording

The first attempt at NebulaScreen configuration discovery swept the UI source for every
`_json_pointer` literal and produced 104 "settings". Most were not settings at all - they
were pointers into Moonraker response and printer status objects: `/sg_result`,
`/layer_count`, `/commits_behind_count`, `/toff`. Counting those as configuration would have
inflated the inventory with roughly 85 options that do not exist, and the dashboard would
have looked busier while being less true.

Discovery is now scoped to what is actually a setting: keys the config schema itself touches
in `src/config.cpp` and `src/config.h` where defaults are applied, plus keys any panel reads
or writes through the `Config` object. That yields **20** NebulaScreen settings. The
Moonraker and status-object surface is real and still needs documenting, but it is an API
inventory and will be discovered as one.

A second correction: an earlier draft of this file claimed 42 extension modules. The real
count is **30** modules and **31** test files. Both numbers now come from the inventory.

## Build, tooling and runtime (Q-004, Q-005)

- **14 build pipeline scripts** in `scripts/build/`, a clean numbered sequence from
  `00-fetch-vendor-sources.sh` through `06-verify.sh`, plus packaging, SBOM generation and
  baseline gates. Pleasant to document because the order is the architecture.
- **11 tool sets** in `tools/`: attestation, eMMC layout, hardware agent, hardware
  capability probes, qualification, USB recovery, release records, SDK export, workspace
  control.
- **56 runtime helpers** shipped in the overlay outside `init.d` - the update supervisor,
  slot swap, clean reset, OTA markers, network and Wi-Fi apply, camera seeding, display
  sleep/wake, memory guard, health check and more. Together with the 35 boot services and
  the `ota.*` / `image.*` / `updates.*` API groups, these are the real source material for
  the update, rollback and recovery documentation.

### A filter that would have been a mistake

Five of those overlay executables have ordinary system names - `passwd`, `sudo`,
`supervisorctl`, `sftp-server`, `git` - and the obvious move was to drop them as vendor
noise. Reading them first was the right call, because every one is NebulaOS-authored:

- `usr/bin/sudo` says of itself that it is a "NebulaOS sudo ADAPTER - not sudo".
- `usr/bin/supervisorctl` is a deliberate fake, present only so Moonraker believes a
  supervisor exists and can list services.
- `usr/bin/passwd` redirects to `nebulaos-passwd` because the image's `/etc/shadow` is
  read-only and the real one lives in persistent storage.
- `usr/libexec/sftp-server` exists to open SFTP in `/opt/printer_data` rather than root's
  empty read-only home.
- `usr/libexec/nebulaos/bin/git` is a wrapper placed first on Moonraker's PATH so
  `update_manager`'s git calls go through it.

These are among the most surprising things in the image, and a developer who assumes
standard behaviour will be misled by all five. They are in the inventory, and the
reasoning is in the seeder so nobody "cleans them up" later.

## A second discovery bug, caught the same way

The endpoint extractor first used the character class `[a-z_/]+` for API paths. That silently
dropped `/machine/nebulaos/network/ipv4`, because `ipv4` contains a digit - the inventory
reported 55 endpoints instead of 56, and a missing endpoint is indistinguishable from an
endpoint that does not exist. Found by counting every `/machine/nebulaos/` path literal in
the file and comparing against the table, which now agrees at 56.

Two discovery bugs in two slices, both in the direction of under- or over-collecting
silently. Every extractor from here on gets a second, independent count before its output is
trusted. The build/tooling/runtime slice was checked that way and agreed exactly: 14 build
scripts, 56 overlay executables, 11 tool sets by shell count and by inventory count alike.

Worth noting that the habit cut both ways this time. It caught over-collection in the config
sweep, under-collection in the API regex, and here it prevented a wrong *exclusion* - the
five system-named shims that looked like noise and were not.

## Test verification is real now

Ran the Klipper extensions suite in a dedicated worktree at `8e3447a`: **29 of 31 suites, 899
individual tests, all passing.** The two excluded suites need the pinned Klipper composed in,
as the project's own CI script documents. `verify_test` is now `verified` on 21 extension
modules, each citing its test file.

Two near-misses worth keeping, both of which would have produced a confidently wrong result:

- The first run reported **29 of 29 suites failing**. That was entirely my own detection bug -
  `unittest` colours its `OK` line when attached to a TTY, so `grep '^OK'` never matched.
  Nothing was wrong with the code. Had I trusted that output, the honest-looking conclusion
  would have been "the extensions test suite is broken", filed as a blocker against work that
  is in fact healthy.
- `unittest discover` reports 42 errors on this suite, which are rootdir artifacts.
  `test_tmcstatus` fails under discovery and passes perfectly when run as a module.

The lesson is the same one the discovery bugs taught: a tool's output is a claim too. Both of
these would have been easy to report as findings.

## Screenshots: solved

**129 real screenshots**, captured headless from commit `94869f7` - the exact commit this
manual documents - and committed to `wiki/images/`.

The application turned out to have a built-in screenshot tour: `GUPPY_SIM_SHOTS=<dir>` walks
every page and state, saves each as a PPM from the LVGL framebuffer, and exits. No display
server needed. It captures *states*, not just screens - confirmations, refusals, in-progress,
failed, rolled-back, and step-by-step calibration sequences - which is the per-workflow
coverage the mission asks for rather than one image per page.

36 of 49 panels now have at least one capture. Reproducible via
`tools/capture_screenshots.sh`, which records the commit alongside the images.

Three things blocked the build, all written up in `SCREENSHOTS.md`: the default `LDFLAGS`
contain `-static` and there is no static SDL2 here (and `/usr/lib`'s is 32-bit i386, while a
usable 64-bit one sits in `/lib64`); submodules cannot be fetched into a git worktree because
that needs to write the foreground checkout's `.git/config`, so a separate clone was required;
and two submodule patches must be applied first.

**What this is not:** hardware. The `machine.nebulaos.*` panels need a live printer, so
OS-settings captures must not be presented as a working machine, and the boot/init screens are
outside the tour entirely.

The older images are now superseded and unused: 26 from 2026-07-01 in the screen repository
(four months stale), and 13 from 2025-08-20 that predate the NebulaScreen rename and show the
upstream GuppyScreen app.

**The honest caveat:** only **7** of the 129 are embedded in pages so far. Having images is
not the same as a manual that uses them, and that gap is the real measure of remaining visual
work.

## Tim's decisions, 2026-11-01

1. **The Creality-touchscreen install route is documented as the normal route.** The "not
   tested" warning is gone from user pages; the record stays in `VERIFICATION.md` and the
   inventory. This reverses the position taken in PR #3 and it is Tim's call. Applied, with
   the trade-off recorded in decision D-009 - including that no page now *claims* the route is
   tested, and that two promises the manual made about caveats were removed too, since a
   manual that promises caveats and then shows none teaches the reader that silence means
   tested.
2. **Free rein to restructure the wiki.** Rename, merge and restructure as it should be, via
   PRs. This unblocks the `Installation.md` / `Installing-NebulaOS.md` name collision, which
   now gets fixed rather than flagged.

## Q-060 progress: the extensions change is in and verified

`origin/main` for the extensions moved to **`a2e7634`** - the power-loss resume fix - so that
part of Q-060 is done rather than pending:

- Pinned worktree moved to `a2e7634`; **full suite re-run, 29/29 suites pass.** The PLR suite
  itself is now 169 tests.
- All 21 test-verified modules had their evidence re-pointed from `8e3447a` to `a2e7634`. An
  evidence citation that names a commit the tree no longer sits at is worse than no citation,
  because it looks checked.
- `wiki/Power-Loss-Recovery.md` written from the new behaviour, replacing a stub.

The behaviour worth documenting, and now documented: a resume that stops partway **cleans up
deliberately** - nozzle heater off, file unloaded, **bed left on** so the part stays stuck
down, and the checkpoint kept so Resume is offered again. Without that explanation a user
would reasonably read a half-finished resume as a malfunction.

### The screen changes landed too, and the re-capture found something

`origin/main` for the screen moved to **`3194104`**, bringing both `4883008` (print status only
for a running print, shorter power-loss popup) and `3194104` (Storage **Free up space**).

Rebuilt and re-captured. **128 of 129 images were byte-identical**, and exactly one differed:
`07-updates.png`. That looked like a real UI change from the new commits.

It was not. Running the tour twice against *the same* build produced the same difference. The
Updates panel disables its buttons while waiting for a reply from Moonraker's update manager,
and with no Moonraker there is no reply - so the capture lands in the busy or the idle state
depending on timing. The differing region is exactly where **Check now** and **Update all**
sit.

So `07-updates.png` is **excluded and not published**. It would have shown a reader greyed-out
buttons that are not greyed out on a real printer - a picture contradicting the page it
illustrates. The text describes the greying-out instead.

Two things worth keeping from this:

- **Measure reproducibility before trusting a comparison.** 128/129 byte-identical is what
  makes commit-to-commit screenshot comparison a real stale-detection method. Without that
  check, a flaky image is indistinguishable from a genuine UI change, and I would have
  "found" a change that never happened.
- **The new Storage button has no screenshot**, because `storage_panel` is one of the panels
  the tour does not visit. Recorded as such rather than quietly left out.

### A drift fix in the tooling

The seeder read source from the workspace-root checkouts, which belong to the foreground
session and move without warning - the firmware one was already a commit ahead of the SHA the
inventory had recorded. It now prefers this agent's own pinned worktrees under
`_worktrees/docs/`, falling back to the root checkout only if no worktree exists. Reading
evidence from a tree that can change underneath you means the recorded commit silently stops
matching the content it describes.

## All of tonight's code is in, and Q-060 is closed

Firmware `origin/main` moved to **`c377230`**, bringing the last of the announced changes:

- **`936c3d6`** - the default root password is now **`NebulaOS`** (was `openke`). A printer
  that already ran NebulaOS keeps the password it seeded, so there is no migration to document.
- **`ed24767`** - a **unique default hostname per printer**: `nebulaos-<last 4 hex of the
  stable Wi-Fi MAC>`, derived once at boot. The reason is worth repeating in the manual, and
  now is: every printer being called `nebulaos` meant two on one network collided in the
  router, in Mainsail and at `nebulaos.local`. A name the user sets always wins; with no
  identifier available it falls back to plain `nebulaos`.
- **`47e07af`** - the **Free up space** endpoints behind the new Storage button.
- **`c377230`** - pins advanced to extensions `a2e7634` and screen `3194104`.

**The pins now match the tips exactly.** Extensions `a2e7634` and screen `3194104` are both
what the firmware ships and what `main` holds, so there is currently no gap at all between
documented and shipped behaviour for those two. Worth noting because D-002 was written when
there was one.

Pages updated for the new facts: `Opening-Mainsail` explains the per-printer naming,
`Installing-NebulaOS` gives the new root password with the advice to change it if the printer
is reachable beyond your own network, and clarifies that the password the SSH install route
asks for is the *current* system's, not NebulaOS's.

## Code changes still expected

The foreground session is landing changes that affect documented behaviour. Final SHAs arrive
in `CONTINUE.md` in the morning. Known so far:

- Power-loss resume fix (extensions `a2e7634`).
- Screen: print view only for a running print; shorter resume popup (screen `4883008`).
- Coming: a Storage **Free up space** button (NebulaOS leftovers only - **Clean up Creality
  files** stays separate); default root password becomes `NebulaOS` (was `openke`); unique
  default hostname `nebulaos-<last 4 MAC hex>`; a clearer SSH prompt.

Queued as **Q-060** with the affected items flagged for re-verification. The screenshots just
captured are from `94869f7` and will need re-running once the screen tip moves - which is
precisely why the capture is now a script.

## Pages written

**Printing** and **Filament** are done, which clears the high-traffic stub list. 8 of the
original 17 stubs are now real pages; 9 remain.

The `Printing` page leads with the **Cancel vs Stop** distinction, because the two sit next to
each other, **Stop** is labelled only "Stop" rather than "Emergency Stop", and pressing it
requires a power-cycle or `FIRMWARE_RESTART` to recover from. A beginner reaching for a gentler
Cancel can easily hit it.

`Filament` records that **Cooldown is the stop control during a Load** - there is no separate
Stop button, and every other button is disabled while loading. Without that, a user watching
filament feed and wanting it to stop has no idea what to press.

## The screen reference exists

`wiki/Screen-Reference.md` - 824 lines, adapted from the NebulaScreen wiki's
`Using-NebulaScreen.md` under decision D-010 rather than rewritten, because that page is good
and re-authoring it would have lost detail for no gain.

What was actually done to it:

- **A generated index of all 49 panels** at the top, built from `coverage.jsonl`, with where
  each one is documented and whether it has a screenshot. Generated rather than typed, so a
  panel cannot quietly go missing from the list.
- **18 image references remapped** to the new captures from `3194104`.
- **8 image references removed**, because no current capture corresponds to them with
  confidence: the bed-mesh 3D view, three console sub-states, exclude object, the printers
  panel, the Spoolman spool list and TMC autotune. Each now says plainly that there is no
  current screenshot of that screen.

That last decision is the one worth defending. There *were* plausible-looking candidates for
several - `m10b-bedmesh-saved` for the 3D view, `36-spoolman` for the spool list,
`m13-tmc-metrics` for autotune - and using them would have made the page look complete. But
`m10b` is the mesh after saving, `36-spoolman` is the Spoolman *server settings*, and
`m13-tmc-metrics` is TMC *status*, not autotune. A caption naming a screen the reader is not
looking at is worse than no picture, because the reader trusts it and then cannot find the
control.

- **7 links remapped**: calibration sub-pages now point at `Calibration-Explained`,
  `Camera-Image-Tuning` at `Camera`, and `Configuration` becomes an explicit external link to
  the component wiki, since the audit's disposition for it was "keep".

Honest state of the reference: **28 of 49 panels are described in detail**; the other 21 are
indexed with a pointer to where they are covered, and are still counted `missing` in the
inventory rather than credited to a pointer.

## Calibration is in: eight pages

`Calibration-Guide`, `Calibration-Explained`, `Bed-Tramming`, `Load-Cell-Calibration`,
`Axis-Twist-Compensation`, `Skew-Correction`, `TMC-Autotune` and `Adaptive-Print-Setup` - all
adapted from the component wiki under D-010, with links and images remapped and real
screenshots added from the capture tour.

The manual is now **29 pages**.

Two things worth noting about how this went:

**All six sub-pages came across, not just the two I set out to write.** The two calibration
pages link to the sub-pages for each individual calibration, and the reuse audit had already
marked all six as "move". Writing only the top two would have left six dangling links or six
more collapsed redirects.

**It let me undo an earlier compromise.** When `Screen-Reference` was built, those sub-pages
did not exist centrally, so eight links to them were collapsed onto `Calibration-Explained` -
correct but lossy, since a reader wanting bed tramming landed on a long walkthrough. Now that
the real pages exist, those links point where they should: `Calibration-Explained` references
dropped from 8 to 1. A workaround taken for a real reason is still worth revisiting once the
reason goes away.

One image reference dropped: TMC Autotune's, because `tmc_tune_panel` has no capture and the
nearest candidate (`m13-tmc-metrics`) is TMC *status*, a different screen.

## The end-user manual is complete: 29 pages, no stubs

Every one of the mission's ten sections is documented, and **all 17 original stub pages are
now real content**. `user-manual-section` coverage is 10/10.

The last batch: `Troubleshooting`, `Camera` and `Beeps-And-Songs` adapted from the component
wiki, and three pages authored from nothing - `What-NebulaOS-Is`, `Supported-Hardware` and
`Glossary`.

Two editorial decisions in that batch worth recording:

**The imported troubleshooting page was reorganised, not just relinked.** It arrived organised
by component, ended with a "Simulator and development" section, and had no entry for the
things a stuck user actually experiences. It now opens with *the printer is not working at
all* - black screen, no touch, Mainsail unreachable, worked-before-the-update - because
someone reaching that page is not thinking in components. The developer and simulator section
was removed and linked to in the component wiki where it belongs.

**The glossary defines the words the manual actually uses**, checked against the pages rather
than guessed: the Klipper/Moonraker/Mainsail/NebulaScreen distinction, boot slots, trial start,
baby-stepping, load cell, E-steps, pressure advance, DHCP. A beginner's manual that uses
"MCU" and "pressure advance" without defining them is not a beginner's manual.

### A self-check caught a miscount

Marking two sections as needing no screenshot by setting `screenshot_status: n/a` - while
leaving `screenshot_required: true` - made them vanish from the screenshot table, 57 counted
against 59 required. `render_dashboard.py`'s sum check fired and named the unreported status.

The fix was to the data, not the renderer: the honest way to say an item needs no screenshot
is to clear the requirement, not to invent a status the renderer does not count. Without that
check the dashboard would have quietly under-reported by two, which is precisely the failure
the check was added for after the same thing happened with screenshot candidates.

## Phase 3 started: the extensions reference

`NebulaOS-klipper-extensions` now has a generated developer reference in `docs/reference/`,
on branch `docs/extensions`, as **PR #3** on that repository. Its GitHub wiki is disabled, so
the reference lives in the repository - which the mission prefers anyway.

- `COMMANDS.md` - 49 registered commands with module, kind, test coverage and description,
  plus the G-code parameters each module reads.
- `CONFIG.md` - 155 configuration options with literal defaults and constraints.
- `README.md` - what the repository is, command attribution, verification state, how to run
  the tests.

### Parsing instead of pattern-matching caught three more bugs

Written with Python's `ast` deliberately, after the two regex extraction bugs earlier in this
project. It found three more immediately:

- **About 140 invented settings.** A naive walk over every `.getX()` call finds **299** "config
  options"; only **155** are called on a config object. The rest are dictionary and JSON
  lookups and G-code parameter reads on `gcmd`.
- **`getfloatlist` missing** from the getter list, dropping 3 real options in `z_compensate`.
- **Fifteen options wrongly marked required.** Defaults passed as `default=CONSTANT` keyword
  arguments were not seen. That is worse than a wrong default - it tells a reader to set
  fifteen TMC registers they never needed to touch.

Also corrected in the inventory: `gcode:_` was an artifact of the very first regex pass and
does not exist, and `NEBULAOS_BED_TRAM` was misattributed - the source says plainly that this
repository registers `_NEBULAOS_BED_TRAM` and the public name is a `gcode_macro` in the
firmware's `calibration.cfg`. It is now recorded against the firmware.

### I over-credited the inventory, then corrected it

Marking the command and configuration items `documented` took coverage from 14% to **49%** in
one step. That was wrong, and worth recording rather than quietly fixing.

Mission 6.5 requires per command: preconditions, example invocation, expected output, errors,
side effects and safety warnings. 6.6 requires per option: purpose, runtime behaviour, whether
a restart is needed, validation rules and an example. The generated tables give name, module,
kind, description, type, default and constraints - real and verified, but not that.

All 193 items are now **draft**, each carrying the specific gap. Coverage is back to **14%
documented, 35% draft**. A generated table is a genuine deliverable; it is not the same as a
documented item, and a dashboard that cannot tell those apart is worthless.

## The firmware reference: API and boot services

`NebulaOS-firmware` now has a generated reference in `docs/reference/`, on branch
`docs/firmware`, as **PR #5** on that repository.

- `MOONRAKER-API.md` - **58** endpoints with HTTP method, JSON-RPC name, handler, and the
  request parameters each handler actually reads, with literal defaults. For example
  `machine.nebulaos.wifi.connect` takes `ssid` (required), `password` (default `""`) and
  `hidden` (default `false`) - read out of `_wifi_connect`, not inferred from the name.
- `BOOT-SERVICES.md` - **35** services in boot order, each with its own script's stated
  purpose.

58, not the 56 recorded earlier: `47e07af` added the two `machine.nebulaos.cleanup.nebulaos*`
endpoints behind the Storage **Free up space** button. The generated list and the inventory
agreed exactly at 58 on an independent diff.

**Response shapes are deliberately absent.** They come from the `nebulaos-osconfig` helper at
runtime, so taking them from the component source would mean inventing them. The README says
so, and names the helper modules and test fixtures where the real shapes live.

## A misleading number I introduced, and removed

Recording "what still needs writing" in the inventory's `blockers` field made the dashboard
report **57% blocked**. That reads as a stuck project. It was nothing of the kind: almost all
of those were completeness gaps - work not yet done - rather than anything unable to proceed.

Now separated. `blockers` means only what it says: something that cannot proceed without
hardware, access, or a decision this agent cannot make. Everything else is a `gaps` entry,
counted on its own line. The real split is **6 blocked (1%)** and **311 completeness gaps
(56%)**.

Two numbers, two meanings. One field holding both made the honest-looking figure the wrong one.

## Next

- **Q-036 / Q-037:** raise both references to the mission's per-item bar. That is the gap
  between a generated table and a documented item, and it is where most of the 289 draft items
  sit.
- `NebulaOS-nebulascreen` developer pages, then the MCU and kernel, then `nebulaos-packages`
  and `lv_drivers` (still not cloned).
- The firmware's build pipeline, runtime helpers, and A/B/OTA/recovery as an architecture.

**None of it is started.** Six component repositories, and the bulk of the inventory sits
there: 234 extension items, 194 firmware items, 57 API endpoints, 172 configuration options.

Sensible order, cheapest-verification-first: **`NebulaOS-klipper-extensions`** has 30 modules,
51 commands, a 899-test suite already passing and 21 modules already test-verified - so its
command and configuration reference can be written with real evidence behind every claim.
Then `NebulaOS-firmware` (the API, boot services, build pipeline), then NebulaScreen's
developer pages, then the MCU and kernel.

Also worth doing: tour steps for the panels the capture misses, starting with `storage_panel`,
which now has a new user-facing button and no picture of it.

Two discovery follow-ups stay open and deliberately non-blocking: the Klipper status objects
the UI subscribes to, and cloning `nebulaos-packages` and `lv_drivers`.

## Open blockers

Two, both recorded in `BLOCKERS.md`: no printer access (by design, mitigated by the
simulator) and two repositories not yet cloned locally (trivial, done when their turn comes).
