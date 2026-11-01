# Status

**Updated:** 2026-11-01 (overnight, third pass)
**Phase:** 2 - writing the end-user manual (first batch complete)
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

## Next

The **49-panel screen reference** (images exist for 36), then the calibration pages, then
`Troubleshooting`, `What-NebulaOS-Is`, `Supported-Hardware` and `Glossary`.

Also worth doing: tour steps for the panels the capture misses, starting with `storage_panel`,
which now has a new user-facing button and no picture of it.

Two discovery follow-ups stay open and deliberately non-blocking: the Klipper status objects
the UI subscribes to, and cloning `nebulaos-packages` and `lv_drivers`.

## Open blockers

Two, both recorded in `BLOCKERS.md`: no printer access (by design, mitigated by the
simulator) and two repositories not yet cloned locally (trivial, done when their turn comes).
