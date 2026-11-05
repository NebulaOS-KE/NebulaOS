# Handoff - read this to resume

You are `nebulaos-docs`, a long-running background documentation session for NebulaOS. This
file is the resume point. Read it, then continue with "Next actions" at the bottom. Do not
start the project over.

## The mission in one paragraph

Produce the real documentation for the whole NebulaOS project - a complete beginner-friendly
end-user manual in the central `NebulaOS` repository, and developer references for every
component repository - written from the actual source code, with an honest, generated
coverage dashboard, delivered as `docs/*` branches and pull requests. Not a plan, not an
outline: the pages themselves. The full assignment is in `MISSION.md`; `RULES.md` holds the
workspace rules and the owner's decisions and wins wherever the two differ.

## Latest batch (2026-11-05, resumed after a power cut)

Inbox notes processed: FREEZE-OVER, API-SNAPSHOT, CORRECTION-OPENKE-SSH, FLOW-AND-SLICER-MACROS,
PRINTER-SCREENSHOTS, SIM-SCREENSHOTS-AND-STOPPED-INSTALL. Sources: firmware `e523e8c`, screen
`123ef31`, extensions `f498796`; Klipper `58bd67db3` for the `-dirty` marker. Wiki changes only on
`docs/agent`; the main session publishes. Next: Q-074 (API examples, needs the `docs/firmware`
worktree), Q-075 (Tim's page-order decision), Q-076 (final 1.0.0 sha).

**New-owner page order (applied 2026-11-05 after Tim approved it, Q-075):** What NebulaOS is -> Supported hardware -> Safety
first -> Two system slots -> Installing -> First-time setup -> Connecting to Wi-Fi -> Opening
Mainsail -> Calibration guide (walkthrough as the long version) -> Setting up your slicer ->
Filament -> Printing -> Updating. Sidebar today puts Under the hood and Glossary inside "Start
here", Two system slots before Installing (fine), Filament after Printing although Printing needs
filament loaded, and Slicer-Setup is now first under "Everyday printing".

## Batch 4 (2026-11-05): page order applied, install corrections from the ke-dev run

Commit A applied Q-075 (13-step path). Commit B took the main session's corrections measured on
ke-dev on 2026-11-05: the stock touchscreen route needs the file with `ota_img` in its name
(shipped from 1.0.1, e.g. `NebulaOS-Ender3V3KE-F005_ota_img_V9.1.0.1.img`; the normal `.img`
is for SSH and online updates), and after a software restart from Creality's system into
NebulaOS one power cycle (off, 10 s, on) is needed before NebulaOS can install its mainboard
firmware. Installing-NebulaOS examples now use 1.0.1. Follow-up commit: "describes 1.0.0" -> 1.0.1 (Home,
What-NebulaOS-Is, Recovery's .ingenic example), and the interrupted-flash contradiction resolved
from firmware origin/main `4febc2a` / screen `123ef31`: the guard classifies a half-written
application as SUPPORTED_HW_UNKNOWN_APP and never auto-flashes it (mcu_lifecycle.py), so it does
NOT retry at every start; the "Klipper can't reach the board" prompt (mcu_panel.cpp) appears
only at the end of a screen-started install, not after a power cut. Pages now give the safe
advice (switch on, Reinstall built-in firmware, power-cycle if "not answering", then Recovery)
and claim neither "fixes itself" nor "needs a computer".

## Batch 3 (2026-11-05): screenshots for every screen

53 Run 23 images embedded (SCREENSHOTS.md lists source, names, fed states and every skip).
Going-Back has "If your old changes come back with it" (stock overlay mmcblk0p9 survives a
Creality .img). Installing-NebulaOS's "install from the stock touchscreen" was deliberately NOT
touched: the main session is testing the file-name rule and will send the correction.
Open question for the main session: Camera.md says Manual exposure comes back to automatic with
Restart camera "(or Defaults)", while the screen's own Manual-exposure question says only
Restart camera brings it back - check camera_panel.cpp before 1.0.1.

## The project has reached its Definition of Done

**2026-11-03. Read `FINAL-REPORT.md` first** - it answers the mission's Part 15 condition by
condition, with the caveat attached: **documentation prepared with outstanding verification**,
not fully verified, because this agent has no printer.

551 items, 542 documented (98%), 0 missing, 9 draft each with a recorded reason. Eight pull
requests open, one per repository. The dashboard is generated from the inventory.

**Do not start new work without the owner asking.** What remains is genuinely blocked or a limit
of static analysis, and it is listed in the final report:

- hardware verification (0 items, by design - no printer access)
- 9 API endpoints whose response keys are not statically knowable
- 15 screenshots needing a printer or a new tour step
- example response values, measured at 3 endpoints and recorded as such

**If a tip moves,** re-run `seed_inventory.py`, regenerate the affected reference, and re-check
the manifest pins. The generators all resolve the code commit through `_srccommit.py`, never the
worktree's HEAD.

## Current phase

**RELEASE 1.0.0 is in progress — skip to "RELEASE 1.0.0 (read this block first)" below before
acting on anything in this section.** The paragraphs immediately following describe Phase 3 and
are still accurate about the developer references, but they predate the release freeze and the
counts are stale (the manual is 30 pages, 129 screenshots, 550 inventory items).

**Phase 2 is complete. Phase 3 is underway.**

The end-user manual is 29 pages with **no stubs**, covering all ten mission sections (10/10 on
`user-manual-section`). 128 screenshots, 41 of 57 required items captured.

**The extensions reference is done and is PR #3 on that repository** - 49 commands, 155
options, generated with `ast` from `a2e7634`. Branch `docs/extensions`.

**Those 193 items are `draft`, not `documented`, and that is deliberate.** The generated tables
give name, module, kind, description, type, default and constraints. Mission 6.5 and 6.6 also
require per-command preconditions, examples, expected output, errors, side effects and safety
warnings, and per-option purpose, runtime behaviour and restart requirements. Marking them
documented took the headline from 14% to 49% in one step, which was flattering and false. Do
not re-upgrade them without writing that detail.

**The firmware reference is PR #5 on that repository** - 58 API endpoints and 35 boot services,
branch `docs/firmware`, generated from `c377230`.

**Two fields, two meanings, do not merge them again.** `blockers` means something that cannot
proceed without hardware, access or a decision. `gaps` means work not yet done. Both were in
`blockers` at one point and the dashboard reported 57% "blocked", which reads as a stuck
project; the real split is 6 blocked and 311 gaps.

**Next:** Q-036 and Q-037 raise both references to the mission's per-item bar, which is where
most of the 289 draft items sit. Then NebulaScreen developer pages, the MCU, the kernel, and
`nebulaos-packages` / `lv_drivers` (still not cloned).

## Completed

- All eight organisation repositories enumerated with default branches and tip commits.
- Docs worktree created: `_worktrees/docs/NebulaOS`, branch `docs/agent`.
- Tracking system built in `documentation/agent/`: mission, rules, status, queue, blockers,
  verification policy, screenshot inventory, decisions, handoff, and two scripts.
- `coverage.jsonl` holds 544 items: 8 repository references, 10 manual sections, 49
  NebulaScreen panels, 51 G-code commands, 172 configuration options, 30 extension modules,
  35 boot services, 56 Moonraker API endpoints plus 1 notification, 17 OS helper modules, 14 build pipeline scripts, 11 tool sets, 56 overlay runtime
  helpers, 34 audited existing wiki pages.
- **Q-006 done** - the reuse audit, written up in `REUSE-AUDIT.md`.
- **Q-004 and Q-005 done** - the build pipeline, developer tooling, and the update /
  rollback / recovery surface. Counts verified independently and in agreement.
- **Q-001 done** - the 8 G-code commands whose names are built from module constants are
  resolved and recorded with their constants in `tools/seed_inventory.py`.
- **Q-020 done** - screenshot capture solved; 129 images from the documented commit.
- **Q-003 done** - the public Moonraker API surface, inventoried from the server-side
  registration table and cross-checked against UI call sites. Klipper status objects are the
  remaining follow-up.
- **Q-002 done** - configuration discovery, after fixing a first attempt that mistook 85
  Moonraker status-object pointers for settings. Read the note in `STATUS.md` before
  touching that code: the lesson is that a broad literal sweep over UI source looks
  productive and quietly fabricates inventory.
- `COVERAGE.md` generated from the inventory.
- Firmware shipping pins read from the manifest and recorded in `STATUS.md`.

## Active work

Nothing half-finished. 17 stub pages are placeholders by design, each saying so to the reader,
and each still counted `missing` in the inventory.

**Screenshots are solved.** 129 real captures at 480x272 from commit `94869f7`, in
`wiki/images/`, reproducible with `tools/capture_screenshots.sh`. The app has a built-in
headless tour (`GUPPY_SIM_SHOTS=<dir>`). 36 of 49 panels covered. Read `SCREENSHOTS.md` before
re-running it - three non-obvious build blockers are written up there.

**The remaining screenshot work is embedding, not capturing.** 7 of 129 are used in pages. Do
it page by page as you write, not as a sweep at the end.

**Q-060 is closed.** All of it landed and was verified: extensions `a2e7634`, screen
`3194104`, firmware `c377230`. Screenshots re-captured and compared. **The firmware pins now
match the repository tips exactly** for the extensions and the screen, so there is currently no
gap between documented and shipped behaviour there.

**When a tip moves again:** move the matching worktree, re-run the extensions test suite and
`tools/capture_screenshots.sh`, and compare. Run the capture tour twice against the same build
before concluding anything changed - one image (`07-updates.png`) is timing-dependent and will
otherwise look like a code change every time.

**The seeder now reads from the pinned worktrees, not the root checkouts.** The root ones are
the foreground session's and move without warning. Keep it that way: an evidence citation
naming a commit the tree no longer sits at is worse than no citation, because it looks
checked.

## Remaining work

**Phase 3, the developer wikis, has not been started at all.** That is the larger half of the
mission: six component repositories, 234 extension items, 194 firmware items, the API
reference, the command reference, the configuration reference. The end-user manual is well
advanced; do not mistake that for the project being well advanced.

All of it, in `QUEUE.md`, in priority order. Phase 1 needs four more discovery slices
(configuration keys, APIs, developer commands, update/recovery mechanisms) before Phase 2
writing starts in earnest.

## Architectural findings so far

- **NebulaOS is not a Klipper fork.** Host Klipper is pristine upstream `Klipper3d/klipper`
  pinned at `58bd67d` and owned by the firmware build. Custom behaviour lives in
  `NebulaOS-klipper-extensions` as loadable `extras/` modules. Documentation must never
  present upstream Klipper behaviour as NebulaOS behaviour.
- **One install path is documented but untested, and the caveat must survive.** The existing
  install page says the Creality-touchscreen route (from stock firmware) has not been tested
  - and that is the route most first-time users take. Carry that caveat into the manual with
  full prominence. Deleting it while relocating the page would be the most harmful single
  edit available in this migration: a promise of a tested procedure on the one operation that
  can brick a mainboard. Recorded as `BLOCKERS.md` B-003.
- **Five overlay executables have ordinary system names and are not what they look like.**
  `sudo` is an adapter that is not sudo, `supervisorctl` is a deliberate fake so Moonraker
  believes a supervisor exists, `passwd` redirects because the image `/etc/shadow` is
  read-only, `sftp-server` relocates SFTP to `/opt/printer_data`, and `git` is a wrapper
  first on Moonraker's PATH. Any of these would mislead a developer who assumed standard
  behaviour. They were nearly filtered out of discovery as vendor noise.
- **The extensions pin gap is cosmetic.** The firmware manifest pins the extensions to
  branch `production` at `31d6d65`; `main` is at `8e3447a`. The diff is three files - a CI
  workflow, a CI script and a README edit - with nothing under `extras/`. Runtime code is
  identical, so every documented extension behaviour is shipped behaviour and pages get a
  footnote with the pin SHA rather than a development-only label. Do not re-derive this from
  the SHAs alone: a pin gap is a question, and the answer is in the diff.
- **The UI surface is large and well-structured.** 49 panels in `src/*_panel.cpp`, which is
  both the screen reference and the screenshot plan.
- **NebulaOS has a deliberate public API.** 56 Moonraker endpoints under
  `machine.nebulaos.*`, served by `scripts/build/overlay/usr/lib/nebulaos/moonraker/
  nebulaos.py` in Moonraker's own process - no second daemon. The full chain is
  panel -> JSON-RPC -> that component -> the `nebulaos-osconfig` CLI (argv in, one JSON
  object out, validated and atomic) -> 17 `nebulaos_osconfig` modules. The component is
  symlinked into Moonraker by `S05nebulaos-activate` and configured by `[nebulaos]` in
  `/etc/nebulaos/moonraker/nebulaos.conf`; without that file Moonraker runs without it,
  which is precisely the difference between a printer that shows OS settings and one that
  does not.
- **Inventory the API from the server, not from the UI.** Two endpoints
  (`ota.discard`, `system.notify_refused`) are served but never called by the shipped UI.
  Discovering from call sites would have missed both.
- **Boot and lifecycle are script-driven.** 35 ordered init scripts in the firmware overlay,
  covering revert safety, Wi-Fi, MCU guard, update supervision, image trial and
  confirm-good. These are the real source for the update, rollback and recovery pages.
- **The extensions test suite passes, and has been run.** 29 of 31 suites, 899 individual
  tests, at `8e3447a`. 21 modules are now test-verified with per-file citations. Two traps
  when re-running it: strip ANSI before matching `OK` (the coloured line defeats
  `grep '^OK'` and makes every suite look broken), and run per-module rather than via
  `unittest discover` (discovery reports 42 bogus errors). Both are written up in
  `VERIFICATION.md`.
- **Upstream commands are overridden, not just added.** `nebulaos_bed_soak.py` replaces
  upstream Klipper's `SET_PIN`, and `nebulaos_z_adjust.py` deregisters and replaces
  `Z_OFFSET_APPLY_PROBE`. Those two must be documented as modified upstream behaviour, not
  as NebulaOS inventions - getting attribution wrong here would mislead anyone coming from
  stock Klipper.
- **Existing documentation is substantial, not disposable.** 34 end-user wiki pages in
  `NebulaOS-nebulascreen/wiki/` approved on 2026-10-30, and about 70 design and analysis
  documents in `NebulaOS-firmware/docs/`. Reuse before rewriting.

## Source revisions in use

| Repository | Branch | Commit |
|---|---|---|
| `NebulaOS` | `main` | `bef8693fb1f415ee874a250a7e9a0115831c14ef` |
| `NebulaOS-firmware` | `main` | `82e132088fc789edc920e4f9e13173effacac50d` |
| `NebulaOS-nebulascreen` | `main` | `94869f75657270200a306c5a54d694eb6adf7b74` |
| `NebulaOS-klipper-extensions` | `main` | `8e3447ac0da435d42be6d6e699c54385fedf846d` |
| `NebulaOS-klipper-mcu` | `main` | `33f5d16daccd9ff5e5c0be61f3d44406440558f2` |
| `NebulaOS-kernel` | `openke` | `d86790d2e23178e52054c71562f9c40994a5469b` |

Re-check these at the start of each session with `git fetch`; if a tip moved, mark the
affected inventory items for re-verification rather than assuming the pages still hold.

## Blockers

`BLOCKERS.md`: B-001 no printer access (by design; simulator is the mitigation), B-002 two
repositories not yet cloned locally.

## RELEASE 1.0.0 (read this block first)

### Second pass, 2026-11-02 evening: re-verified against the release candidate `70ad0b0`

**This supersedes the first pass below.** Read `RELEASE-1.0.0-READINESS.md` for the full report.

Done in this pass:

- **Statistics** documented in `wiki/Screen-Reference.md` (new `## Statistics panel` section),
  linked from `Home`, `Printing` and `Resetting`, with the real capture `20a-statistics.png`.
- **Screenshots re-captured at `36490ed`**, the screen commit `70ad0b0` pins. 130 captures:
  one new, four changed, `07-updates` still excluded. `screenshots.json` records `36490ed`.
- **Storage/cleanup text corrected:** Clean up Creality files *keeps* the statistics files.
- **`211d804` is gone** from the branch; 44 inventory items relabelled to `70ad0b0`.
- **Timelapse-across-a-power-loss documented** in `Power-Loss-Recovery`.
- **D-011 applied:** no user page says what was tested. `BLOCKERS.md` B-003 closed.

**Three things to carry forward:**

1. **The simulator build still works, without a component worktree.** `_worktrees/docs/screen-sim`
   is a standalone clone, not a `git worktree`, so it does not register in any source
   repository's worktree list and the release identity gate is unaffected. Procedure: fetch,
   `git checkout <pin>`, `make GUPPY_SMALL_SCREEN=1 -j$(nproc) LDFLAGS="-lm -Llibhv/lib
   -Lspdlog/build -l:libhv.a -latomic -lpthread -lstdc++fs -l:libspdlog.a"`, then
   `tools/capture_screenshots.sh`. The script skips its own build when the binary exists, so
   rebuild by hand after moving the checkout or you will capture the old commit.
2. **`render_dashboard.py` takes two arguments** (`coverage.jsonl` then `COVERAGE.md`). With
   none it raises `IndexError` *and still exits 0*, so a chained command carries on as if it
   had worked. Pass the paths; check the output line.
3. **A range is only cosmetic if you checked the range you cited.** The morning's report said
   `a2e7634..f498796` was a pure version bump. It is not — that was true of
   `ed99372..f498796`, and the missing middle commit added a user-visible feature that no page
   described. Diff the range you are actually claiming about.

**Q-064 is done (2026-11-03): `wiki/Timelapse.md`.** The manual is 31 pages. Two findings worth
keeping: NebulaOS takes the layer pictures itself (a watcher in `camera.cfg` started by
`START_PRINT`), so no slicer change is needed; and **cancelling a print does not render a
video** - upstream renders on *"Done printing file"* and nothing else, and the next print
clears the frames. Reading upstream at its pinned commit rather than assuming is what caught
the second one; the clone lives in `$TMPDIR/mt` and is disposable.

**Q-070 done (2026-11-03): `MODULES.md` and the existing-page audit. Coverage 85% -> 92%.**
`docs/extensions` `41653f9`, `docs/agent` `08bd373`.

**A recorded number was wrong for days:** modules with no test. The rule was
`test_<module>.py` exists, which both understated coverage (files excluded from the standalone
run for importing Klipper) and missed tests named after what they test. Real answer: five, all
vendored. Determine coverage by reading tests for references, not by matching filenames.

**Remaining:** 13 API endpoints whose responses do not resolve, 11 firmware developer tools, 14
build commands, 2 extensions commands, 2 internal screen panels, the central repo overview.
About 43 items, and the end is in sight - check the dashboard before choosing.

**Q-069 done (2026-11-03): the NebulaScreen block.** `docs/screen` `fa7cde0` and the manual.
**Coverage 79% -> 85%.**

**Check index pointers, do not trust them.** Two entries in the screen reference's panel index
sent readers to pages that do not mention their subject. Both looked fine in the table.

**Remaining, by size:** 19 extensions modules, 18 existing NebulaScreen wiki pages needing a
disposition, 13 API endpoints whose responses do not resolve, 11 developer tools, 14 build
commands, 2 extensions commands, the central repo overview. Check the dashboard first.

**Q-068 done (2026-11-03): `docs/firmware` `56fdc1e`.** `RUNTIME-HELPERS.md` (57 helpers,
with callers found by searching) and full per-service detail in `BOOT-SERVICES.md`.
**Coverage 65% -> 79%** - the firmware's two largest undocumented blocks.

**Next, by size:** 20 NebulaScreen config-option items, 19 extensions modules, 18 existing
NebulaScreen wiki pages needing a disposition, 15 screen panels, 13 API endpoints whose
responses do not resolve, 11 developer tools, 14 build commands. Check the dashboard rather
than this list - it is accurate only at the moment it was written.

**A habit that keeps paying:** when an extractor reports an implausible count, suspect the
extractor. Thirteen of thirty-five init scripts implementing no verbs is not a fact about an
init system, and it was two separate parser bugs.

**Q-037 is closed, and `OSCONFIG.md` is new (2026-11-03, `docs/firmware` `c58a260`).**
18 helper modules and 189 public functions documented - the largest undocumented block in the
firmware. 46 of 59 endpoints now resolve their response keys. Coverage is 65%.

**Two seeder bugs fixed, both silent (`docs/agent`).** `gaps` was erased on every re-seed
because it was in neither `BLANK` nor the keep list - 22 gaps became 0 with nothing failing.
And the seeder enumerated files from the worktree while citing `origin/<default>`, so a page
this agent wrote was discovered as source to document. **Anything added to the item schema
belongs in both `BLANK` and `main()`'s keep list**, or it will vanish on the next run.

**Do not re-open example response values expecting a larger yield.** Measured: the 4381-line
osconfig fixture file gives 3 endpoints and 5 key/value pairs, because it tests the helper
functions directly rather than through endpoints. The number is in the extractor's docstring.

**Q-036 was done earlier the same day.** `CONFIG.md` is 156 of 156 options
with a purpose (`docs/extensions` `ba436d8`). The firmware API reference resolves responses for
43 of 59 endpoints (`docs/firmware` `87116ad`) via the new
`documentation/agent/tools/gen_firmware_api_responses.py`.

**What is left of Q-037:** example *values*. The keys are established; the contents are not.
`tests/nebulaos-osconfig-tests.py` is 4381 lines of fixtures and is the honest source for them.

**Re-run `seed_inventory.py` after a release.** `machine.nebulaos.stats` was missing from
`coverage.jsonl` entirely - the inventory said 58 endpoints, the component had 59 - because the
seeder last ran before 1.0.0 added it. It surfaced only because the new extractor produced an
independent count that disagreed. Nothing had failed; the number was just a release out of
date.

**Q-007 is done (2026-11-03) and B-002 is closed.** `nebulaos-packages` (PR #2) and
`lv_drivers` (PR #1) are cloned into `_worktrees/docs/`, read and documented. Every repository
in the organisation now has documentation; eight pull requests are open.

The `lv_drivers` finding to carry: the fork is two commits, and only one is live. The fbdev
blank/unblank pair is dead code superseded by NebulaScreen's `nsfb`, and `fbdev_blank()` must
never be called on the KE's panel. Reading the diff alone would have documented both as
shipped behaviour.

**Next:** Q-036 (16 configuration options still carrying a dash in `CONFIG.md`, which need
reading module by module - a parser cannot produce these) and Q-037 (firmware API response
examples, from `nebulaos_osconfig/` and the fixtures in `tests/nebulaos-osconfig-tests.py`).
The firmware worktree needs recreating first, from its existing remote branch with a merge.

**Q-065 is done (2026-11-03): `docs/extensions` `90c646e`.** Extensions reference re-verified
at `f498796`; suite re-run at that commit (29 of 31 standalone, 912 tests); 235 inventory items
and 31 test-evidence lines re-pointed; `ARCHITECTURE.md` gained the physical-resume ordering and
the timelapse frame handling.

**A generator bug worth knowing about, now fixed.** All four `gen_*.py` stamped the worktree's
`HEAD` as the source commit, so the first run today cited `6ef0610` - a documentation merge - as
the source of the command reference. `seed_inventory.py` had been fixed for exactly this the day
before; the generators were not, because the fix went where the bug was noticed rather than where
the pattern lived. They now share `documentation/agent/tools/_srccommit.py`. **If you add another
generator, use it** - a citation that points at prose is worse than none, because it looks
checked.

**Next:** Q-036 (per-option configuration detail, 16 options still with a dash) and Q-037
(firmware API response examples) are the largest remaining blocks, then Q-007 (clone
`nebulaos-packages` and `lv_drivers`, the only two repositories with no documentation at all).
The four other component worktrees still need recreating - only `NebulaOS-klipper-extensions`
was brought back, deliberately, to keep the footprint small while an OTA test was pending.

**The release is published** (v1.0.0, firmware `70ad0b0`, screen `36490ed`) and the main session
pushed the manual to the GitHub wiki as `NebulaOS.wiki b438b9b`. **The freeze is over** - the
component worktrees may be recreated with the procedure in "Resuming afterwards" below, and the
normal Phase 3 queue resumes.

**Superseded: the next batch was Q-064, a Timelapse page.** It ships (manifest pin, `S57nebulaos-timelapse-seed`,
`camera.cfg` / `print.cfg` macros), the mission lists it as a manual section, and the manual
mentions it on two pages in passing. Everything needed is readable with `git show` — no
component worktree required.

### First pass, 2026-11-02 morning (superseded by the block above)

Tim's decision: the end-user manual must be finished before 1.0.0 is published; the developer
wikis are not required for the release. Resumed in this worktree only - no component worktrees
recreated, source read via `git show <sha>:<path>` so no working tree was touched.

**Full report: `RELEASE-1.0.0-READINESS.md` in this directory.** It names what was verified,
what this pass fixed, and the four remaining items with who can close each.

The short version: verified against firmware `211d804`; 30 pages, no stubs, 128 screenshots,
all internal and external links resolving. Four items left, none blocking publication, one a
judgement call for Tim - the stock-touchscreen install route is still unverified on hardware
and the manual now presents it without a caveat.

*The status message to `nebulaos-48` could not be delivered - the session was busy with release
work and the send failed repeatedly. The report is committed instead, which is the channel that
does not depend on timing.*

### PAUSED - acknowledgement to the foreground session

**Status: paused. All six `docs/*` branches are clean and pushed. Safe to remove the five
component worktrees now.** Nothing was in flight - the kernel batch finished and pushed before
the freeze request arrived.

No new work has been started and no further iteration is scheduled. The loop is stopped until
the foreground session says the freeze is over.

*This acknowledgement is recorded here because the cross-session message could not be delivered
- `nebulaos-48` was busy with release work and the send timed out twice. The branch state below
is independently verifiable with `git ls-remote`, so nothing depends on that message arriving.*


**Do not start work in the component worktrees, and do not recreate them, until the foreground
session says the release freeze is over.**

Tim started RELEASE 1.0.0. The release identity gate requires every source repository to have
only its main checkout, so the five component worktrees under `_worktrees/docs/` are being
removed by the foreground session for the freeze - release builds A and B, packaging, hardware
qualification. A few hours.

State at the pause, all clean and pushed:

| Branch | Repository | Commit |
|---|---|---|
| `docs/agent` | `NebulaOS` | `85a850a` |
| `docs/firmware` | `NebulaOS-firmware` | `7c8f108` |
| `docs/extensions` | `NebulaOS-klipper-extensions` | `f8c24ea` |
| `docs/mcu` | `NebulaOS-klipper-mcu` | `f5f489d` |
| `docs/kernel` | `NebulaOS-kernel` | `aa0a0d4f6` |
| `docs/screen` | `NebulaOS-nebulascreen` | `96d6e10` |

**The branches survive; only the worktrees go.** Nothing is lost - every batch was pushed, which
is the habit that made this a non-event rather than a scramble.

**The central `NebulaOS` worktree is not affected** and still holds the inventory, the dashboard
and this file.

### Resuming afterwards

1. Recreate each worktree from its **existing remote branch**, not from `origin/main`:
   ```sh
   git -C <checkout> worktree add /home/tim/workspace/NebulaOS/_worktrees/docs/<repo> docs/<topic>
   ```
   Use an absolute path - a relative one resolves against `-C`, which once created a worktree
   inside a foreground checkout.
2. Merge `origin/<default>` into each branch to pick up release work. **Merge; do not
   `checkout -B`** - that resets the branch and discards the doc commits.
3. Re-run `tools/seed_inventory.py`, the extensions test suite, and
   `tools/capture_screenshots.sh`. A release will have moved tips, so expect screenshots and
   evidence SHAs to need updating.
4. Re-check the manifest pins: a release is exactly when documented-versus-shipped can diverge.

   **Specifically, check the extensions `production` branch.** The manifest pins
   `KLIPPER_EXTENSIONS_BRANCH=production` with `KLIPPER_EXTENSIONS_PIN`, and the 1.0.0 release
   identity gate reported `production != pin` as its one remaining failure, which Tim is
   fixing. The extensions reference on `docs/extensions` currently claims *"Shipped by
   firmware: yes - the manifest advanced to `ed99372`"*, and that claim is only true if
   `production`, the pin and `main` all agree once the release lands. Verify all three before
   leaving that sentence in place; it was already wrong once today in the other direction, when
   the pin lagged `main` by two hours.

   **Observed during the freeze (read-only, 2026-11-01):** `production` is now `ed993726b`,
   which matches the manifest pin this reference describes - so the gate's `production != pin`
   failure looks resolved and the *"Shipped by firmware: yes"* sentence appears correct.
   Meanwhile `main` has moved on to `f498796fc`. That is the normal, expected direction: the
   pin is the shipping authority and `main` running ahead of it is not a problem, it just means
   the reference describes what ships rather than the newest code. Re-confirm all three against
   the real manifest after the freeze rather than trusting this note - it was taken from
   `git ls-remote` without reading `dependencies.conf`.

### What was mid-flight

Nothing. The last batch (kernel documentation) finished and pushed before the pause. The next
queued item is cloning `nebulaos-packages` and `lv_drivers` - the only two repositories with no
documentation - which needs no component worktree and could proceed if the freeze allowed new
work. It does not, so it waits.

## Worktrees and build areas

- `_worktrees/docs/NebulaOS` - the manual and agent state, branch `docs/agent`.
- `_worktrees/docs/NebulaOS-firmware` - pinned at `c377230`, branch `docs/firmware`. **Read
  evidence from here, not from the workspace-root checkout** - the foreground session moves
  that one under you (it was already one commit ahead when checked).
- `_worktrees/docs/NebulaOS-klipper-extensions` - **`a2e7634`**, branch `docs/extensions`,
  used for the test suite.
- `_worktrees/docs/NebulaOS-nebulascreen` - `3194104`, branch `docs/screen`.
- `_worktrees/docs/screen-sim` - a **separate clone** with submodules, for building the
  simulator. Not a worktree, deliberately: submodule init needs to write the parent repo's
  `.git/config`, which lives in the foreground checkout and is write-protected.

One mistake to avoid: `git worktree add` resolves a *relative* path against the `-C`
directory, not the shell's cwd. That briefly created a worktree **inside** the foreground
checkout on 2026-11-01. It was removed and the checkout verified clean, but use absolute
paths.

## Branches and pull requests

- `docs/extensions` in `NebulaOS-klipper-extensions` - worktree at
  `_worktrees/docs/NebulaOS-klipper-extensions`, used for running the test suite. No
  commits, nothing to push. Note that `git worktree add` could not write the parent repo's
  `.git/config` (sandbox), which is harmless - the worktree itself works.
- `docs/agent` in `NebulaOS` - the agent's state and the user manual. Pushed.
- **PR #3** - https://github.com/NebulaOS-KE/NebulaOS/pull/3 - the first batch: manual
  skeleton, install, recovery, safety, and the coverage dashboard. Open, awaiting review.
  Later batches continue on the same branch and update this PR; do not open a second PR for
  the manual unless the owner asks for one.

## Next actions, in order

1. `git fetch` every repository and compare tips against the table above. If a tip moved,
   mark the affected items for re-verification instead of assuming the pages still hold.
2. **Q-017:** replace stubs with real pages, highest-traffic first - `First-Time-Setup`,
   `Connecting-To-WiFi`, `Opening-Mainsail`, then `Resetting` and `Updating-NebulaOS`. The
   existing NebulaScreen wiki already covers the last two well; reconcile rather than rewrite.
3. **Q-020, continued:** fetch the four submodules into
   `_worktrees/docs/NebulaOS-nebulascreen`, build with `GUPPY_SMALL_SCREEN=1`, and try to
   drive one panel and capture one image. Record the answer in `SCREENSHOTS.md` either way.
4. **Q-052:** run the two Klipper-dependent test suites the way `scripts/ci-tests.sh` does,
   by composing `extras/` into a scratch copy of the pinned Klipper at `58bd67d`.
5. Keep running `tools/check_links.py` before every commit that touches `wiki/`.
5. Follow-ups, when their sections come up and not before: Klipper status objects (find the
   `printer.objects.subscribe` call sites; the ~85 rejected pointers are candidates, but tie
   each to a real subscription first), and cloning `nebulaos-packages` and `lv_drivers`.

Each batch ends the same way: update `coverage.jsonl`, regenerate `COVERAGE.md`, update
`STATUS.md` and `QUEUE.md`, commit, push, update this file.

## A habit this work has earned

Two of the first three discovery slices shipped a bug that mis-sized the inventory: a sweep
that over-collected 85 non-existent configuration options, and a regex that silently dropped
an API endpoint whose path contains a digit. Neither announced itself - a wrong inventory
looks exactly like a right one.

So every extractor gets a second, independent count before its output is trusted. Compare
against a different signal: total path literals in the file, a hand count on one module, the
other side of the same interface. It has caught something every time.

## Tim's decisions you must not re-litigate

- **D-009:** the Creality-touchscreen install route is documented as the normal route, with no
  "untested" warning on user pages. The verification record lives in `VERIFICATION.md` and the
  inventory only. This reversed an earlier position of this agent's; it is Tim's call. Do not
  reinstate the warning.
- **D-010:** free rein to rename, merge and restructure the wiki, via PRs.

Note what D-009 did *not* license: no page claims the route is tested, and `verify_hardware`
stays unverified in the inventory. Removing a warning is not the same as asserting a
verification.

## Do not append to STATUS.md

`STATUS.md` answers *where does this stand now*, in about a page. It is not a changelog.

It became one: edited by appending a section per batch until it was 557 lines, with a summary
at the top still reading "510 items, all missing, no pages written" while the dashboard said
otherwise. An append-only status file turns its oldest and most wrong paragraph into the first
thing a reader sees. The foreground session spotted it, which means it had been misleading for
hours.

Now: the factual block between the `GENERATED STATUS` markers is written by
`render_dashboard.py` from the inventory, so it cannot drift. Edit the prose below it, keep it
short, and let the numbers come from the script. Mistakes worth remembering go in
`STATUS-LOG.md`; the narrative is the commit history.

## A process rule, learned the hard way

Never chain `render_dashboard.py && <state updates>` in one shell command. A path mistake in
the render short-circuited the `&&` on 2026-10-31, the state updates silently did not run,
and the commit that followed described a blocker it had not actually written. The dashboard
was left reporting 510 items while the inventory held 544 - the exact stale-dashboard failure
the mission warns about.

Run the updates, then render, then **verify the files say what the commit message claims**
before committing. A commit message is a claim like any other.

## The screen reference, and a rule it established

`wiki/Screen-Reference.md` was adapted from the component wiki, not rewritten, and carries a
generated 49-panel index so no panel can drop off the list.

**The rule: never point a caption at a screenshot of a different screen.** Eight image
references were removed rather than remapped to plausible-looking candidates -
`m10b-bedmesh-saved` is the mesh *after saving* and not the 3D view, `36-spoolman` is the
Spoolman *server settings* and not the spool list, `m13-tmc-metrics` is TMC *status* and not
autotune. Using them would have made the page look finished. A caption naming a screen the
reader is not looking at is worse than no picture at all: the reader trusts it, then cannot
find the control, and stops trusting the rest.

## How to write a page here

Read `REUSE-AUDIT.md` first - 15 of the existing wiki pages move largely as they stand, so
check whether the work is already done before authoring.

Every procedure page follows the mission's shape: what the guide is for, what you need, what
to check first, numbered steps, expected result, troubleshooting, and how to undo it.

Three habits that the first batch proved out:

- **Verify the numbers, do not copy them.** The old wiki's "about 5 minutes" and "three
  times" were correct, but that was established by reading `TRIAL_SECONDS` and
  `TRIAL_ATTEMPTS` in source. Two accurate documents agreeing with each other is not
  evidence.
- **Give caveats their own heading.** The untested install route got a *How much of this is
  tested* section near the top of the page, not a footnote. A reader deciding whether to
  flash their printer needs that before the steps, not after.
- **Cite the commit.** Any claim about timing, defaults or behaviour names the file and the
  commit it came from, so a later reader can re-check it instead of trusting it.

## Working rules that are easy to get wrong

- Commit with `git -c user.name=Tim -c user.email=timdejaeger@gmail.com commit`, message
  ending `Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>`.
- Push only `docs/*`. Never `main`, `openke` or `production`. Never merge, never force-push,
  never run a wiki publish workflow.
- Edit only inside `_worktrees/docs/`. The checkouts at the workspace root belong to the
  foreground session - read them, never write them.
- Never write production code, tests or configuration. A code bug goes to `BLOCKERS.md`.
- No printer, no firmware builds, no `dangerouslyDisableSandbox`, never read the archived
  sibling workspace.
- Never write a bare GitHub handle with an at-sign in a document or pull request - it
  notifies a real person.
- Routine progress goes in these files. Message the foreground session only for a finished
  milestone, a user-affecting code/doc contradiction, or a real blocker.
