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

## Everything is merged and published (2026-11-12)

All eight pull requests were merged at the heads this session reported, and every repository's
`wiki/` is now **published to its GitHub wiki** by a `wiki.yml` workflow on the default branch
(`on: push`, `paths: ['wiki/**']`). The owner decided to publish; the main session merged.

Verified here afterwards, by cloning all eight `.wiki.git` repositories read-only and diffing
each against `wiki/` on its default branch: **0 differences in all eight** - NebulaOS 53 pages,
firmware 16, kernel 8, extensions 8, mcu 7, packages 6, lv_drivers 6, screen 35. The firmware's
and kernel's old August pages are gone.

| Repository | Branch merged | Merge commit | Wiki |
|---|---|---|---|
| `NebulaOS` | `docs/agent` | `a296fe1` | the end-user manual, 53 pages |
| `NebulaOS-firmware` | `docs/firmware` | `0c712b2` | 16 pages |
| `NebulaOS-kernel` | `docs/kernel` | `1dbe846` | 8 pages |
| `NebulaOS-klipper-extensions` | `docs/extensions` | `55a0d11` | 8 pages |
| `NebulaOS-klipper-mcu` | `docs/mcu` | `c9cebf7` | 7 pages |
| `nebulaos-packages` | `docs/packages` | `670a0d4` | 6 pages |
| `lv_drivers` | `docs/lv-drivers` | `fcdda5f` | 6 pages |
| `NebulaOS-nebulascreen` | `docs/screen` | `a61fd51` | 35 pages |

### What this changes for this session

**A merged docs PR now publishes.** There is no separate publish step left to hold the line, so
the line moves to the pull request: a page is published the moment someone merges it, in every
repository, not only NebulaScreen. Three habits follow.

- **Run `tools/check_links.py` before every commit that touches `wiki/`** - it was already the
  rule; now a broken link reaches readers rather than a branch.
- **Never push a half-finished page to a `docs/*` branch "to fix later"**, because the fix and
  the mistake are one merge apart.
- **Still never push to a `.wiki.git` and never run a publish workflow.** Publishing happens
  because a human merged, which is the same consent as before, expressed once instead of twice.

## One user-facing entry added after the wikis (2026-11-12)

`wiki/Troubleshooting.md` covers the Z-offset calibration failure from issue #9 - the nozzle not
reaching the bed on printers with a softer bed mount. The fix shipped the same day as Klipper
extensions **1.0.1** (`6532091`, now on `production`, which is the branch Moonraker's update
manager follows), so the page leads with **Settings -> Updates -> NebulaOS extensions** and keeps
the two `printer.cfg` lines as the fallback for a printer that cannot update. Evidence, and the
three states the page passed through, in `VERIFICATION.md`.

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
4. **One inventory question.** `wiki/Configuration.md` (NebulaScreen) documents about 25 settings
   while the inventory tracks 20; the difference is GuppyScreen-inherited fields. Decide whether
   they belong in the inventory before the count is quoted anywhere - see `QUEUE.md`.

## Working rules that are easy to get wrong

Read evidence from the worktrees under `_worktrees/docs/`, never from the checkouts at the
workspace root - those belong to the foreground session and move without warning. Push only
`docs/*`; never merge, never force-push, never push to a `.wiki.git` and never run a publish
workflow. Never edit production code, tests or configuration to make a document right: that goes
in `BLOCKERS.md`.

**Since 2026-11-12 a merged `docs/*` PR publishes itself** in every repository, through each
default branch's `wiki.yml`. Nothing about what this session may do has changed - it still only
pushes branches and opens pull requests - but the margin for a half-finished page is gone:
whatever is in `wiki/` when someone merges is what readers see. Check links before every commit
that touches `wiki/`.

## Where the rest lives

`COVERAGE.md` (generated dashboard) · `coverage.jsonl` (the inventory) · `QUEUE.md` (what is
queued) · `BLOCKERS.md` (blockers and code/doc contradictions) · `VERIFICATION.md` (what was
actually run) · `SCREENSHOTS.md` (provenance and the retake list) · `DECISIONS.md` (the owner's
decisions) · `STATUS-LOG.md` (mistakes worth remembering) · `FINAL-REPORT.md` (the mission's
Definition of Done, condition by condition) · `HANDOFF.md` (resume here).
