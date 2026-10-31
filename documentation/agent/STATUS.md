# Status

**Updated:** 2026-10-31
**Phase:** 1 - repository discovery and coverage inventory (commands, configuration and APIs done)
**Branch:** `docs/agent` in the central `NebulaOS` repository
**Mode:** autonomous, self-paced loop

## Where things stand

The agent's own infrastructure is in place and discovery has run over commands,
configuration, screens, services and the public API. There are **429 discovered
documentation items** in
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

## A second discovery bug, caught the same way

The endpoint extractor first used the character class `[a-z_/]+` for API paths. That silently
dropped `/machine/nebulaos/network/ipv4`, because `ipv4` contains a digit - the inventory
reported 55 endpoints instead of 56, and a missing endpoint is indistinguishable from an
endpoint that does not exist. Found by counting every `/machine/nebulaos/` path literal in
the file and comparing against the table, which now agrees at 56.

Two discovery bugs in two slices, both in the direction of under- or over-collecting
silently. Every extractor from here on gets a second, independent count before its output is
trusted.

## Next

Finish Phase 1 with developer-facing commands and build targets (Q-004), the update and
recovery mechanisms (Q-005), and the audit of the 34 existing wiki pages (Q-006). Then start
Phase 2, the end-user manual, beginning with the install and first-setup journey.

## Open blockers

Two, both recorded in `BLOCKERS.md`: no printer access (by design, mitigated by the
simulator) and two repositories not yet cloned locally (trivial, done when their turn comes).
