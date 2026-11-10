# Status

<!-- BEGIN GENERATED STATUS -->
*Figures generated 2026-11-10 from `coverage.jsonl` by `tools/render_dashboard.py`. Do not edit this block by hand.*

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
| Blocked (cannot proceed) | 4 |
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

## Open pull requests - all six refreshed against 1.0.2 on 2026-11-10

| Repository | PR | Branch | Describes |
|---|---|---|---|
| `NebulaOS` | [#3](https://github.com/NebulaOS-KE/NebulaOS/pull/3) | `docs/agent` | The end-user manual: 53 wiki pages (11 moved-page stubs), 202 images, plus this agent's inventory, dashboard and tooling |
| `NebulaOS-firmware` | [#5](https://github.com/NebulaOS-KE/NebulaOS-firmware/pull/5) | `docs/firmware` | Architecture (boot, slots, updates, recovery, the black box), 59 API endpoints, 36 boot services, 58 runtime helpers, 190 osconfig functions, 21 build scripts and 62 host tools - at `b95b156`, with the 1.0.2 boundary recorded where it bites |
| `NebulaOS-klipper-extensions` | [#3](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions/pull/3) | `docs/extensions` | Architecture, 50 commands with per-command detail, 156 configuration options, 30 modules - at `178a0c2`, the 1.0.2 pin and the tip of `main` and `production` at once |
| `NebulaOS-kernel` | [#2](https://github.com/NebulaOS-KE/NebulaOS-kernel/pull/2) | `docs/kernel` | Which parts of the kernel are NebulaOS, the freeze-diagnosis layer, and `CONFIG_PREEMPT` rather than `PREEMPT_RT` - at `95d0321e`, which is the 1.0.2 pin |
| `NebulaOS-nebulascreen` | [#6](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen/pull/6) | `docs/screen` | Contributor guide, the screenshot tour, configuration - describing `fd47cb6`, with the gap to `main` read from the diff |
| `NebulaOS-klipper-mcu` | [#1](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/pull/1) | `docs/mcu` | MCU firmware lifecycle on a printer: both identities, the restore and its bounds, the power-cycle failure, and the KE-only boundary |

**Nothing is merged and nothing is published.** No wiki publish workflow has ever been run from
this session; the owner publishes.

## What is still open

1. **Eight drafts**, all the same shape: `machine.nebulaos.*` endpoints whose response keys
   cannot be resolved from source, because the handler composes its answer in the Moonraker
   component or the helper returns something not statically knowable. Each says so on the page
   rather than carrying a plausible example. Closing them needs recorded responses from a
   printer - which is exactly how the ninth closed: `updates.readiness` now shows the response
   recorded on ke-dev on 2026-11-04, with its provenance and the check that the helper has not
   changed since. The other eight are POST actions and the snapshot has none of them.
2. **Four blockers** in `BLOCKERS.md`, three of them one fact: no printer access, so
   `verify_hardware` is 0 and stays 0.
3. **Screenshots.** 44 of 60 required items captured, 15 missing, 1 blocked. Separately, eleven
   embedded images show a pre-1.0.2 version *inside the picture* - the retake list, with what
   each one says today, is at the end of `SCREENSHOTS.md`. `r-system.png` is the one to take
   first: it also shows `Kernel 6.6.157-rt79`, and 1.0.2 does not print `-rt79` at all.
4. **One inventory question.** `wiki/Configuration.md` (NebulaScreen) documents about 25 settings
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
