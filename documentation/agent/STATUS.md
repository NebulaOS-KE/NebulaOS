# Status

**Updated:** 2026-10-31
**Phase:** 1 - repository discovery and coverage inventory (substantially complete)
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

## Next

Phase 1 has produced enough evidence to write against, and the mission is explicit that the
deliverable is pages rather than an audit. So: **Q-006**, the reuse audit of the 34 existing
wiki pages, and then straight into Phase 2 - the manual skeleton and the installation and
recovery sections, which is the first pull request.

Two discovery follow-ups stay open and are deliberately not blocking: the Klipper status
objects the UI subscribes to, and the two repositories not yet cloned
(`nebulaos-packages`, `lv_drivers`). Both are additive and will be folded in when their
sections come up.

## Open blockers

Two, both recorded in `BLOCKERS.md`: no printer access (by design, mitigated by the
simulator) and two repositories not yet cloned locally (trivial, done when their turn comes).
