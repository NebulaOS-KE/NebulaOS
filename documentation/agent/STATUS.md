# Status

<!-- BEGIN GENERATED STATUS -->
*Figures generated 2026-11-12 from `coverage.jsonl` by `tools/render_dashboard.py`. Do not edit this block by hand.*

| | |
|---|---|
| Discovered items | **560** |
| Documented | **552** (98%) |
| Draft | 8 |
| Missing | 0 |
| Code verified | 560 |
| Test verified | 47 |
| Hardware verified | 0 |
| Screenshots required / captured | 60 / 44 |
| Blocked (cannot proceed) | 3 |
| Completeness gaps (work not done) | 9 |

Per-repository and per-category breakdowns are in `COVERAGE.md`.
<!-- END GENERATED STATUS -->

*Where this stands now, in about a page. Not a changelog: the narrative is this branch's commit
history, the mistakes worth remembering are in `STATUS-LOG.md`, and the per-item truth is
`coverage.jsonl` and `COVERAGE.md`.*

## The release this documentation describes

**NebulaOS 1.0.2, published 2026-11-09, is the first and only end-user release.** 1.0.0 and
1.0.1 and their tags were deleted on purpose, so no page, caption or inventory label refers to
them: there is no version history to write. Pins at tag `v1.0.2`, firmware `3bdf3ff`
(`manifests/dependencies.conf`): kernel `95d0321e` on `openke`, extensions `178a0c2`, screen
`fd47cb6` (NebulaScreen v1.0.1), host Klipper `58bd67db`.

Firmware `main` has moved past the release (`dc4d9d6`, `b95b156`). `REPOSITORY_HEAD` is not
`SHIPPING_PIN`, and the developer pages say which one they describe.

## Open pull requests - all eight refreshed against 1.0.2, and all seven component wikis delivered

Refreshed 2026-11-10 (six) and 2026-11-11 (the two older ones). On **2026-11-12** every
component repository got its developer documentation as a top-level `wiki/` directory on its
docs branch - `Home.md`, `_Sidebar.md`, one page per topic, wiki-style links - the shape the
central manual and the NebulaScreen wiki already use. Nothing is published: no `.wiki.git` was
touched and no publish workflow was run.

| Repository | PR | Branch | Describes |
|---|---|---|---|
| `NebulaOS` | [#3](https://github.com/NebulaOS-KE/NebulaOS/pull/3) | `docs/agent` | The end-user manual: 53 wiki pages (11 moved-page stubs), 202 images, plus this agent's inventory, dashboard and tooling |
| `NebulaOS-firmware` | [#5](https://github.com/NebulaOS-KE/NebulaOS-firmware/pull/5) | `docs/firmware` | **16 wiki pages**: architecture (boot, slots, image install and the trial, recovery, the black box, the printer configuration), 59 API endpoints, 36 boot services, 58 runtime helpers, 190 osconfig functions, 21 build scripts and 62 host tools, plus building from source, build provenance, installing a developer build and the repository map - at `b95b156`, with the 1.0.2 boundary recorded where it bites |
| `NebulaOS-klipper-extensions` | [#3](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions/pull/3) | `docs/extensions` | **8 wiki pages**: architecture, 50 commands with per-command detail, 156 configuration options, 30 modules, testing - at `178a0c2`, the 1.0.2 pin and the tip of `main` and `production` at once |
| `NebulaOS-kernel` | [#2](https://github.com/NebulaOS-KE/NebulaOS-kernel/pull/2) | `docs/kernel` | **8 wiki pages**: which parts of the kernel are NebulaOS, the freeze-diagnosis layer, `CONFIG_PREEMPT` rather than `PREEMPT_RT`, the branch model, what the build verifies - at `95d0321e`, which is the 1.0.2 pin |
| `NebulaOS-nebulascreen` | [#6](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen/pull/6) | `docs/screen` | 35 wiki pages, already published from `wiki/` by its own workflow: contributor guide, the screenshot tour, configuration - describing `fd47cb6`, with the gap to `main` read from the diff. Checked this batch; two moved-page stubs marked and a link-checker false positive fixed |
| `NebulaOS-klipper-mcu` | [#1](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/pull/1) | `docs/mcu` | **7 wiki pages**: the firmware's lifecycle on a printer (both identities, the restore and its bounds, the power-cycle failure, the KE-only boundary), building your own, architecture, reproducibility, toolchain |
| `nebulaos-packages` | [#2](https://github.com/NebulaOS-KE/nebulaos-packages/pull/2) | `docs/packages` | **6 wiki pages**: the ABI fingerprint, the pipeline, four invariants, and the image side of the contract - at `9d0d264` (`gh-pages` `9bef4d4`), with the firmware end read at `3bdf3ff` |
| `lv_drivers` | [#1](https://github.com/NebulaOS-KE/lv_drivers/pull/1) | `docs/lv-drivers` | **6 wiki pages**: which parts of the fork are NebulaOS - two commits on `master` `ea2e4cc`, one live - consumed by NebulaScreen `fd47cb6` (1.0.2) and `84db432`, both pinning `0406ccb` |

**Nothing is merged and nothing is published.** No wiki publish workflow has ever been run from
this session; the owner publishes.

## One user-facing entry added after the wikis (2026-11-12)

`wiki/Troubleshooting.md` now covers the Z-offset calibration failure from issue #9 - the nozzle
not reaching the bed on printers with a softer bed mount - with the two `printer.cfg` lines that
work around it today. The fix itself is extensions `a63964a`, which is on **neither `main` nor
`production`**, so the page promises no version: it says the real fix arrives through
**Settings -> Updates**. Evidence in `VERIFICATION.md`.

## What is still open

1. **Eight drafts**, all the same shape: `machine.nebulaos.*` endpoints whose response keys
   cannot be resolved from source, because the handler composes its answer in the Moonraker
   component or the helper returns something not statically knowable. Each says so on the page
   rather than carrying a plausible example. Closing them needs recorded responses from a
   printer - which is exactly how the ninth closed: `updates.readiness` now shows the response
   recorded on ke-dev on 2026-11-04, with its provenance and the check that the helper has not
   changed since. The other eight are POST actions and the snapshot has none of them.
2. **Three blockers**, and they are one fact: no printer access, so `verify_hardware` is 0 and
   stays 0 - the untested stock-touchscreen install route, and two screens the headless tour
   cannot capture honestly (`storage_panel` needs an extra tour step, `updates_panel`'s busy
   state varies between runs). The fourth closed on 2026-11-11: `NEBULAOS_BED_TRAM` needed a
   file read, not a printer - it is `[gcode_macro NEBULAOS_BED_TRAM]` in the firmware's
   `calibration.cfg`, forwarding `{rawparams}` to the extensions' private command.
3. **Screenshots.** 44 of 60 required items captured, 15 missing, 1 blocked. Separately, eleven
   embedded images show a pre-1.0.2 version *inside the picture* - the retake list, with what
   each one says today, is at the end of `SCREENSHOTS.md`. `r-system.png` is the one to take
   first: it also shows `Kernel 6.6.157-rt79`, and 1.0.2 does not print `-rt79` at all.
4. **One claim this session had to retract**, and it took three passes - the lesson is in
   `STATUS-LOG.md`. The manual said releases are "built twice on separate machines with the two
   results required to be byte-identical". There is no *separate machines* anywhere, and the
   published 1.0.2 was built with the local launcher rather than by the release workflow that
   exists. What **is** now measured, after the main session corrected the firmware's own records
   (`d464b46`): 1.0.2 built twice on one host with the same container digest gives identical
   `xImage` and `rootfs.squashfs`, and those are the hashes the release publishes. The user
   pages say what is checked and nothing about where; the `.img` cannot be byte-identical at all
   (encrypted 7z, random AES IV). Full entry in `BLOCKERS.md`, which also records the two
   discrepancies that closed at the source the same day.
5. **One inventory question.** `wiki/Configuration.md` (NebulaScreen) documents about 25 settings
   while the inventory tracks 20; the difference is GuppyScreen-inherited fields. Decide whether
   they belong in the inventory before the count is quoted anywhere - see `QUEUE.md`.

## Working rules that are easy to get wrong

Read evidence from the worktrees under `_worktrees/docs/`, never from the checkouts at the
workspace root - those belong to the foreground session and move without warning. Push only
`docs/*`; never merge, never force-push, never publish. Never edit production code, tests or
configuration to make a document right: that goes in `BLOCKERS.md`.

## Where the rest lives

`COVERAGE.md` (generated dashboard) · `coverage.jsonl` (the inventory) · `QUEUE.md` (what is
queued) · `BLOCKERS.md` (blockers and code/doc contradictions) · `VERIFICATION.md` (what was
actually run) · `SCREENSHOTS.md` (provenance and the retake list) · `DECISIONS.md` (the owner's
decisions) · `STATUS-LOG.md` (mistakes worth remembering) · `FINAL-REPORT.md` (the mission's
Definition of Done, condition by condition) · `HANDOFF.md` (resume here).
