# Status

**Updated:** 2026-10-31
**Phase:** 1 - repository discovery and coverage inventory (first pass complete)
**Branch:** `docs/agent` in the central `NebulaOS` repository
**Mode:** autonomous, self-paced loop

## Where things stand

The agent's own infrastructure is in place and the first mechanical discovery pass has run.
There are **175 discovered documentation items** in `coverage.jsonl`, every one of them
recorded against the exact commit it was found at, and every one of them currently
`missing` - which is the honest starting position. No documentation pages have been written
yet.

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
- **43 registered G-code commands** across the Klipper extensions, of which 41 have
  literal names and 2 are assembled from module constants and still need resolving by hand.
- **42 Klipper extension modules**, each with a matching test file in most cases - unusually
  good test coverage for this kind of code, which will make `verify_test` genuinely
  achievable.
- **34 existing end-user wiki pages** in `NebulaOS-nebulascreen/wiki/`, plus roughly 70
  design and analysis documents in `NebulaOS-firmware/docs/`. Substantial material to reuse
  rather than replace.

## Shipping pins worth knowing

From `NebulaOS-firmware/manifests/dependencies.conf` at `82e1320`:

- NebulaOS version `0.9.0`, UI API `1`
- NebulaScreen pinned at `94869f7`, which **is** the current `main` tip
- Kernel pinned at `d86790d` on `openke`, which **is** the current tip
- Klipper extensions pinned to branch `production` at `31d6d65`, while `main` is at
  `8e3447a` - **the one place where development is ahead of what ships**, and the reason
  extension pages must label development-only behaviour
- Host Klipper is pristine upstream `Klipper3d/klipper` at `58bd67d`, not a fork

## Next

Finish Phase 1 by deepening the inventory where it is still shallow - configuration keys,
Moonraker and JSON-RPC interfaces, build and developer commands, update and recovery
mechanisms - then start Phase 2, the end-user manual, beginning with the install and
first-setup journey, reusing the existing NebulaScreen wiki pages.

## Open blockers

Two, both recorded in `BLOCKERS.md`: no printer access (by design, mitigated by the
simulator) and two repositories not yet cloned locally (trivial, done when their turn comes).
