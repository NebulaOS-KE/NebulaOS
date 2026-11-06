# Final report: the NebulaOS documentation project

**Date:** 2026-11-03
**Branch:** `docs/agent` — [PR #3](https://github.com/NebulaOS-KE/NebulaOS/pull/3)
**Status:** **Documentation prepared with outstanding verification.** Not "fully verified" — the
mission's own term for this situation, and the honest one: this agent has no printer.

## The headline, with its caveat attached

| | |
|---|---|
| Inventory | **551 items**, discovered from source |
| Documented | **542 (98%)** |
| Draft, each with a recorded reason | **9 (1%)** |
| Missing | **0** |
| Code-verified | **551 (100%)** — the implementation was read |
| Test-verified | **47** — a test in the repository covers it |
| Hardware-verified | **0** — no printer access, by design |

**Those are four different claims and the dashboard never merges them.** 98% documented does not
mean 98% proven to work. It means a page covers the item and names the commit it was read at.

## Definition of Done, condition by condition

### End-user documentation — met

The manual is **31 pages** in `wiki/`, published to the GitHub wiki by the owner on 2026-11-03.
Complete navigation (every page reachable from `_Sidebar.md`, checked mechanically), all ten
mission sections at 10/10, installation and first setup end to end, every screen on the
touchscreen, all calibration workflows, troubleshooting and recovery, and the safety pages.

Release compatibility is documented: every page is checked against firmware `70ad0b0`
(`NEBULAOS_VERSION=1.0.0`), screen `36490ed`, extensions `f498796`.

**Screenshots: 42 captured, 15 missing, 1 blocked.** All real captures of the real application
at a recorded commit, from the SDL simulator. The missing ones are named per page rather than
hidden; `07-updates` is excluded on purpose because its capture is timing-dependent without a
live printer and would show a reader greyed-out buttons that are not greyed out on a printer.

### Developer documentation — met

Every repository in the organisation has a technical reference, and every one is an open pull
request:

| Repository | PR | What is there |
|---|---|---|
| `NebulaOS` | [#3](https://github.com/NebulaOS-KE/NebulaOS/pull/3) | The end-user manual, the coverage dashboard, the tooling |
| `NebulaOS-firmware` | [#5](https://github.com/NebulaOS-KE/NebulaOS-firmware/pull/5) | Architecture, 59 API endpoints, 18 osconfig helper modules, 35 boot services, 57 runtime helpers, 21 build scripts, 62 host tools |
| `NebulaOS-klipper-extensions` | [#3](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions/pull/3) | Architecture, 30 modules, 50 commands with per-command detail, 156 configuration options |
| `NebulaOS-nebulascreen` | [#6](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen/pull/6) | Contributor guide, the screenshot tour, the configuration reference |
| `NebulaOS-kernel` | [#2](https://github.com/NebulaOS-KE/NebulaOS-kernel/pull/2) | Which parts of the kernel are NebulaOS |
| `NebulaOS-klipper-mcu` | [#1](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/pull/1) | MCU firmware lifecycle on a printer |
| `nebulaos-packages` | [#2](https://github.com/NebulaOS-KE/nebulaos-packages/pull/2) | The package index, its four invariants |
| `lv_drivers` | [#1](https://github.com/NebulaOS-KE/lv_drivers/pull/1) | Which two commits of this fork are NebulaOS, and which one is dead code |

Cross-repository integration is explained in the firmware architecture guide and in the central
README, which now links the manual and every component reference — it had no link to the
documentation at all before today, which for a project's front door was the single most
user-affecting gap left.

### Quality — met

Claims are checked against a named source revision and the commit is recorded per item.
`check_links.py` passes on every commit touching `wiki/`. Existing documentation was reconciled
rather than replaced: 34 existing NebulaScreen wiki pages audited, 18 of them re-verified against
current source on 2026-11-03. Historical pages are labelled and were checked against the thing
they claim is absent. Unverified claims are labelled, and no page states that anything was tested
(owner decision D-011).

### Coverage and delivery — met

Every discovered item has a disposition; no missing item is silently ignored; documented and
verified coverage are reported separately; all 9 drafts carry an explicit reason. Eight pull
requests are open and current. The dashboard is generated from the inventory, never typed.

**Publishing workflows:** the owner published the manual to the GitHub wiki on 2026-11-03. This
agent has never run a publish workflow, by instruction.

## What is genuinely outstanding

**1. Hardware verification — 0 items, and it will stay 0 here.** No SSH, no launcher, no
Moonraker connection to a machine. That is a deliberate boundary, not a gap to work around. Three
behaviours are recorded as `reported-by-owner` rather than verified: the nozzle-clean routine, the
stock-touchscreen install route, and the Statistics page on `ke-dev`.

**2. Nine API endpoints do not resolve their response keys.** Each records which of two reasons:
the handler builds its answer in the Moonraker component rather than delegating one osconfig
call, or the helper returns a value whose keys are not statically knowable — a JSON document read
at runtime, or a nested call. 50 of 59 resolve. The nine are a limit of static analysis, not a
backlog.

**3. Fifteen screenshots need a printer or a tour step.** Two need a photograph of real hardware
(first boot, the MCU firmware page), one needs a live printer, the rest are reachable in the
simulator but not on the capture tour.

**4. Example response values are 3 endpoints, 5 key/value pairs.** Measured, not estimated: the
4381-line osconfig fixture file exercises the helper functions directly rather than through
endpoints, so it is not a source of per-endpoint examples at scale.

## What this project got wrong, and how it was caught

Recorded because the pattern is more useful than the fixes.

**Four silent tooling bugs, each producing output that looked correct.** The seeder erased every
recorded `gaps` value on each run; it discovered this agent's own unmerged writing as source
material to document; the boot-service verb parser reported 13 of 35 init scripts as implementing
no verbs; and a G-code command literally named `_` sat in the inventory because a regex matched
`register_command('_' + CMD, ...)`.

Nothing failed in any of those. No check went red.

**What caught them was a number that was implausible on its face** — 13 of 35 init scripts with
no verbs is not a fact about an init system — **or a second count derived independently.** That
habit was adopted after two early discovery slices shipped mis-sized inventories, and it has now
paid for itself five times.

**And two false alarms worth as much as the finds.** A word-boundary search for the retired
`NebulaOS-klipper` fork matches `NebulaOS-klipper-extensions`, the live repository, because one
name is the other plus a suffix. And `coreflake1/guppyscreen` is not a retired URL — it is
OpenKE, credited correctly. Both would have produced a confident correction to text that was
already right, which is worse than finding nothing.

## The recurring temptation, named

Several times the fastest way to raise the headline number was to write something plausible: a
response example composed from an endpoint's name, a configuration purpose inferred from an
option, a caption pointed at a near-enough screenshot. Each would have read better than the gap
it replaced and been unfalsifiable by the reader.

The inventory records gaps instead, and the dashboard counts them. A documentation project that
cannot be wrong in public is not finished — it is unfalsifiable, which is a different thing.
