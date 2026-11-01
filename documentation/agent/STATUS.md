# Status

<!-- BEGIN GENERATED STATUS -->
*Figures generated 2026-11-01 from `coverage.jsonl` by `tools/render_dashboard.py`. Do not edit this block by hand.*

| | |
|---|---|
| Discovered items | **549** |
| Documented | **271** (49%) |
| Draft | 110 |
| Missing | 168 |
| Code verified | 346 |
| Test verified | 46 |
| Hardware verified | 0 |
| Screenshots required / captured | 57 / 41 |
| Blocked (cannot proceed) | 6 |
| Completeness gaps (work not done) | 4 |

Per-repository and per-category breakdowns are in `COVERAGE.md`.
<!-- END GENERATED STATUS -->

**Phase:** 3 - developer wikis. Phase 1 (discovery) and Phase 2 (end-user manual) are complete.

**Branch:** `docs/agent` in the central `NebulaOS` repository.

## Why the documented figure is low, and what it means

The end-user manual is finished and most of the developer references exist, yet "documented"
sits around 14%. That is not pessimism, it is the mission's own bar.

An item counts as **documented** only when a page covers it with what the mission asks for. For
a command (6.5) that includes preconditions, an example invocation, expected output, errors,
side effects and safety warnings. For a configuration option (6.6): purpose, runtime behaviour,
whether a restart is needed, validation rules and an example.

The generated references give name, module, kind, description, type, default and constraints -
real, verified, genuinely useful, and short of that bar. Draft items each carry the specific
gap in their `gaps` field.

The commands have since been raised to that bar and are now documented: parameters with valid
ranges, errors raised, side effects and an example invocation, each naming what remains
unestablished.

Configuration is in progress. `CONFIG.md` carries each section's module-header purpose, the
checked fact that every option needs a Klipper restart, and a **per-option Purpose column**
for **139 of the 155** - 109 written by reading the module, the rest quoted from the author's
own comment above the option and labelled as such.

Only those are promoted. **16 keep a dash** and stay draft, because a dash is the honest answer
where no reading has been done; the alternative is a sentence invented from the option's name.

### Command side effects were misclassified, and are now read rather than detected

Caught in review, not by my tooling. `COMMANDS-DETAIL.md` printed *Runs G-code: yes / no -
reports only*, derived from whether the handler called `run_script`. That labelled
`NEBULAOS_BEEP` (drives the buzzer's PWM), `SAVE_INPUT_SHAPER` (rewrites `printer.cfg`),
`EEPROM_WRITE_INT` (writes the EEPROM) and `Z_OFFSET_APPLY_PROBE` (persists an offset) all as
*reports only* - telling a reader each was safe to try.

Making detection transitive did not fix it: effects are reached through collaborator objects
(`self.pwm.off()`), and resolving those graphs soundly is real static analysis. So the automatic
claim was removed and all 49 commands were **read**, in five classes: runs G-code, writes
hardware, writes files, changes saved configuration, changes state surviving a restart.

The result shows how misleading the old label was: **11 commands touch persistent state, 6
write hardware while running no G-code at all, and only 6 are genuinely reports-only.**

*Running no G-code* and *having no effect* are completely different claims, and the first
version conflated them.

### Seven options are accepted and then ignored

The find that justified reading every module. Three (`tri_min_hold`, `tri_max_hold`, `speed`
in `[z_compensate]`) exist only so Klipper will start: it hard-errors on any option in a
section the module never reads, and a real device sets all three. They belonged to a
sensitivity override removed with PRTouch in Phase 1.8B.

Four more - `type_nozz`, `noz_pos_center`, `noz_pos_offset`, `pumpback_mm` - are read but
unused **because their meaning is unconfirmed**, and the source says so: `noz_pos_center` is
plausibly an XY reference point with nothing confirming it, and misapplying it would send the
toolhead somewhere unintended; `pumpback_mm` is plausibly a pre-wipe retract, and wiring
untested E-axis motion into a probe and heat sequence was judged not worth the risk on a guess.

That second group is an author leaving something visibly unfinished rather than acting on a
plausible guess. Documenting them as ordinary settings would have undone that decision -
it would tell a reader these controls work. And guessing from the names produces exactly that:
"noz_pos_center: the nozzle's centre position" reads perfectly and is worse than useless.

`nozzle_clear`'s thirteen options are the clearest argument for reading modules rather than
parsing them: `clr_noz_len_x`, `pa_clr_dis_mm_x`, `vs_start_z_pos` cannot be described honestly
from their names, but the module header explains the wipe sequence and the options map onto it
once that is known.

An earlier attempt promoted all 152 on the strength of a section-level purpose, taking coverage
from 21% to 49% in one step. It was reverted the same iteration - see `STATUS-LOG.md`, along
with the separate episode where the purposes file itself sat in the wrong repository and
contributed nothing.

Marking them documented once took the headline from 14% to 49% in a single step. That was
flattering and false, and reverting it is recorded in `STATUS-LOG.md`.

## The extensions wiki now has a readable guide, not just references

`docs/reference/ARCHITECTURE.md` on `docs/extensions` - hand-written, because explanation
cannot be extracted. Every factual claim names its source file so any sentence can be
re-checked.

It answers the question the generated references cannot: why the repository is shaped this way.
Not forking Klipper leads, because everything follows from it. Then composition (symlinks into
`klippy/extras/`, excluded from Klipper's git so the update manager sees a clean tree), the
compatibility contract (26 required symbols checked at every Klipper start, plus an empty
forbidden list so retired APIs cannot return), how a calibration actually runs through its four
layers, and why power-loss recovery writes the sidecar before the EEPROM record.

The design point worth repeating: the cost of not forking is that your dependency moves without
telling you, and the answer here is not pinning and hoping - it is declaring the dependency
precisely and refusing to start when it is unmet.

## Everything re-verified at today's tips

All three repositories moved again. Current: firmware `832314d`, extensions `ed99372`, screen
`dee0f6f`. References regenerated, suite re-run, screenshots re-captured.

**The screenshot diff did exactly what it was built for.** Re-capturing at `dee0f6f` changed
**5 of 129** images, and all five were print-status or print-start screens - matching that
commit's own subject, *"Print start: steps centred, the preview back after the start"*. The
other 123 were byte-identical. A capture run is a cheap way to see what a UI change actually
touched, and that is now written into the screen wiki as evidence rather than theory.

### An evidence bug in my own tooling

The seeder recorded each worktree's `HEAD` as the source commit. Those worktrees now sit on this
agent's own `docs/*` branches, which carry documentation commits and merges on top of the code -
so the inventory began citing **documentation** commits as the source of **code** facts.
`ddb14e6` is a page of prose; anyone checking it for the API surface would find nothing.

Fixed: the seeder now records `origin/<default-branch>` - the tip of the code the documentation
describes - and falls back to HEAD only where no such ref exists. The dashboard again shows
`832314d`, `ed99372`, `dee0f6f`.

This one is worth noticing because nothing failed. The SHAs looked perfectly plausible, and
every item carried one. An evidence trail that points at the wrong artefact is indistinguishable
from a correct one until someone follows it.

## Previously: re-verified at extensions `ed99372`

The extensions tip moved twice today. At `ed99372` the full suite was re-run (29 of 31 suites,
all passing) and the references regenerated: **50 commands, 156 options**, up one each -
`_NEBULAOS_PLR_TIMELAPSE_MERGE` and `timelapse_frame_path`.

The change behind them is worth reading rather than just regenerating around. A power-cut test
on the development printer found the resume working, but **heating the nozzle while it still sat
over the part**. The order is now: bed first with the nozzle off, Z lifted and X/Y homed, then
the nozzle heated at the park position. The checkpoint also records the current object so a
part-finished one is restarted rather than skipped, and timelapse frames from before the cut can
be preserved.

That ordering is in the user-facing page **with the reason**, because "the bed heats before the
nozzle" looks arbitrary until you know the alternative melted into the print someone was trying
to save.

The `nozzle_clear` header note was also corrected upstream, so B-004 is fully closed at source.

### A mistake in handling this

Moving the worktree to the new tip, I ran `git checkout -B docs/extensions origin/main`, which
**reset my own branch** and discarded five doc commits from it. Nothing was lost - they were
already pushed, so `origin/docs/extensions` still held them - and the fix was to restore the
branch from the remote and merge `origin/main` into it properly.

The lesson is narrow and worth keeping: to pick up new upstream code on a working branch,
**merge it, do not re-point the branch at it**. `-B` is for creating a branch, not for updating
one. Pushing after each batch is what made this a recoverable annoyance rather than lost work.

## Correction: the MCU-brick warning was wrong

**The most prominent safety warning in the end-user manual was false, and it is now fixed.**

Six user pages said never to power-cycle a printer running Creality's system, because a stock
cold boot reflashes the MCU and would leave it mismatched until a USB recovery. `Safety-First`
led with it under the heading *"The one that can break your printer for good"*.

Current source says otherwise, and it was checkable all along. `S50nebulaos-mcu-guard` delegates
to `mcu_lifecycle.py`, which classifies the running MCU application:

| Classification | What happens |
|---|---|
| `NATIVE_CANDIDATE_001` | Klipper starts; nothing reflashed |
| `KNOWN_STOCK` | `mcu_restore.py` reinstalls the native firmware automatically |
| `UNKNOWN_APPLICATION` | **Never auto-flashed** - a user's own firmware is kept |

`mcu_restore.py` is bounded: one attempt, SHA256 against a pinned value, hardware allow-list
checked before any write and again after bootloader entry.

So **stock reinstalls its MCU firmware at a cold boot and NebulaOS reinstalls its own at boot**.
Switching is self-correcting in both directions, power switch included. Nothing is a hard brick.
The real caution is the ordinary one - do not cut power *while a flash is running* - and the
screen says so while it performs one.

### How I got it wrong

I derived it from `S00revert-safety`'s header comment, which explains that automatic rollback
was removed because a stock boot reflashes the MCU "destroying the qualified native GD32F303 MCU
build". That sentence is true about the reflash. I turned it into *therefore permanent damage*,
and never checked whether anything restored it.

The rule I had written for myself three times over - **derive behaviour from code, not from
prose** - and I took a code *comment* as behaviour. Worse, the comment was correct for its own
subject; I extrapolated a consequence it did not claim. And this was the one claim in the manual
most likely to be read and acted on, because it was the scariest.

The firmware's own `DEVELOPER_RECOVERY.md`, `HOW_TO_SWITCH_STOCK_AND_CUSTOM.md` and
`HARDWARE_AGENT.md` carried the same stale framing - they predate `mcu_restore.py`. All three now
carry corrections, with the historical reasoning preserved because it cites live hardware runs.

### What was written instead

`wiki/Mainboard-Firmware.md` is new: what the mainboard firmware is, why it changes by itself
when you switch systems, that firmware you installed yourself is left alone, the one real
caution, and how to reinstall or replace it from **Settings → Printer → MCU firmware**. That
screen existed and had no documentation at all.

## The firmware has a readable architecture guide too

`docs/reference/ARCHITECTURE.md` on `docs/firmware` - boot, slots, updates and recovery, with
the reasoning rather than just the values.

The find worth repeating: **there is deliberately no automatic rollback to the stock system.**
`S00revert-safety` used to write the stock slot's marker on every boot, so any failure before
the health check landed the next reboot on stock. It was removed in Phase 1.8B and the script is
now an explicit no-op, because **booting the stock Creality slot auto-flashes the MCU with old
Creality firmware**, destroying the qualified native GD32F303 build.

The automatic safety net would have turned a software failure into an MCU firmware change nobody
asked for, which is a good reason to remove it. It is **not** a reason to call stock a one-way
door - see the correction above.

Three more things documented with their reasoning:

- The **OTA marker is a three-way wire format**, not a string in a partition. The exact bytes
  are what Creality's `ota_utils.sh` and `ingenic-usbboot` both write, and usbboot's check is
  `strncmp(ota, "ota:kernel\n", 11)` - so a bare `echo -n` silently fails to match.
- The **image trial is bounded two ways** (`TRIAL_SECONDS 300`, `TRIAL_ATTEMPTS 3`) because
  there are two failure shapes: a hang needs a timeout, a system that crashes and reboots
  cleanly would reset a timeout forever and needs an attempt count.
- **`S99confirm-good` originally accepted any result from `/server/info`** - true the instant
  Moonraker's listener is up, regardless of whether Klipper reached the MCU. Found live, now
  checks `klippy_state`. A health check answering "did it start" while claiming "does it work"
  is worse than none.

## NebulaScreen: a contributor guide, and its tests run

`wiki/Working-on-NebulaScreen.md` on `docs/screen`. It complements the existing `Architecture`
page rather than competing with it - that page says what is where, and the audit was right to
keep it. This one says how to work on the code.

The organising idea is the split that makes the codebase testable: **logic that does not need
LVGL lives in files that do not include it** - twelve of them, each with a matching host test -
while the `*_panel.cpp` files draw and dispatch. `plr_status.cpp` carries 21 tests precisely
because the offer logic was kept out of the panel.

**`make test` at `dee0f6f`: 18 suites, 262 tests, 0 failures, 2 skips.** The skips are the suite
detecting that `AF_UNIX` is not permitted here and saying so - correct behaviour, not a gap. That
promoted `verify_test` on **16 panels**, each citing the specific suite that covers it, so test
verification across the project is now 46 items rather than 28.

One trap documented because I hit it: do not pass a custom `LDFLAGS` to `make test`. It
propagates into libhv's sub-make where the relative paths do not resolve, and the failure looks
exactly like a broken suite. That is the second time this project has produced a
*my-invocation-not-their-code* failure, after the ANSI/`grep OK` trap in the extensions - both
now written down where the next person will look.

The UI API contract gets its own section, because it is the same shape as the extensions'
`required_klipper_symbols` check and for the same reason: a component updatable independently of
what it talks to must declare what it expects and refuse to start when that is unmet. Three
components, three independent update paths, one consistent answer - worth naming as a pattern
rather than describing three times.

## Open pull requests

| Repository | PR | Contents |
|---|---|---|
| `NebulaOS` | [#3](https://github.com/NebulaOS-KE/NebulaOS/pull/3) | The complete end-user manual: 29 pages, 128 screenshots, plus this agent's dashboard and tooling |
| `NebulaOS-klipper-extensions` | [#3](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions/pull/3) | Architecture guide, 49 commands with per-command detail and side effects, 155 configuration options, developer README |
| `NebulaOS-firmware` | [#5](https://github.com/NebulaOS-KE/NebulaOS-firmware/pull/5) | Architecture guide (boot, slots, updates, recovery), 58 Moonraker API endpoints, 35 boot services, developer README |
| `NebulaOS-nebulascreen` | [#6](https://github.com/NebulaOS-KE/NebulaOS-nebulascreen/pull/6) | Contributor guide (testable split, simulator, UI API contract); retired repository URLs fixed; the `GUPPY_SIM_SHOTS` screenshot tour documented |

Nothing is published. No wiki workflow has been run, nothing is merged.

## Done

**Phase 1 - discovery.** Every repository in the organisation enumerated, with the inventory
built from source: 49 NebulaScreen panels, 49 registered commands, 155 extension configuration
options plus 20 screen settings, 58 API endpoints, 35 boot services, 14 build scripts, 56
runtime helpers, 30 extension modules, 34 existing wiki pages audited.

**Phase 2 - the end-user manual.** 29 pages, no stubs, all ten mission sections. 128 real
screenshots captured headless from the application itself at a recorded commit, reproducible
via `tools/capture_screenshots.sh`.

**Phase 3, so far.** Generated references for the extensions (commands, configuration) and the
firmware (API, boot services), both parsed with `ast` rather than regex.

**Verification actually performed.** The extensions test suite run at `a2e7634`: 29 of 31
suites, 899 tests, all passing; 21 modules test-verified with per-file citations.

## Source revisions

| Repository | Branch | Commit |
|---|---|---|
| `NebulaOS-firmware` | `main` | `832314d` |
| `NebulaOS-nebulascreen` | `main` | `dee0f6f` |
| `NebulaOS-klipper-extensions` | `main` | `ed99372` |
| `NebulaOS-klipper-mcu` | `main` | `33f5d16` |
| `NebulaOS-kernel` | `openke` | `d86790d` |

The firmware manifest advanced in `832314d` to extensions `ed99372` and screen `dee0f6f`, so
**the pins match those tips exactly** and there is currently no gap between documented and
shipped behaviour. The caveat recorded earlier today - that the power-loss-recovery changes were
newer than the pin - was correct for about two hours and has been removed rather than left to
mislead in the other direction.

Read evidence from the pinned worktrees under `_worktrees/docs/`, never from the checkouts at
the workspace root - those belong to the foreground session and move without warning.

## Next

1. **Q-036 configuration half** - the 155 extension options still need purpose, runtime
   behaviour, restart requirement and an example. Unlike the commands, these are *not*
   mechanically derivable: a `config.getfloat('duty', 0.5)` call gives the name, type, default
   and range but says nothing about what the setting is for. This needs reading each module,
   not a better parser.
2. **Q-037** - response examples for the firmware API, from `nebulaos_osconfig/` and the
   fixtures in `tests/nebulaos-osconfig-tests.py`. The firmware is at 5% documented and holds
   the largest remaining block: 95 draft and 89 missing items, mostly the 56 runtime helpers
   and per-service detail.
3. `NebulaOS-nebulascreen` developer pages - LVGL architecture, the panel system, Moonraker
   integration, the simulator, build and testing. One real doc bug found and fixed: three wiki
   pages pointed at the old `coreflake1/NebulaOS-guppyscreen` repository.
   **A second "bug" I reported was my own misreading** - see `STATUS-LOG.md`. The page's
   documented `LDFLAGS` are correct and already explain dropping `-static`.
4. `NebulaOS-klipper-mcu` and `NebulaOS-kernel`.
5. `nebulaos-packages` and `lv_drivers` - still not cloned locally.
6. The firmware's build pipeline, runtime helpers, and A/B / OTA / recovery as an architecture
   rather than a file list.

## Open blockers

Seven, all genuine, in `BLOCKERS.md`. The newest is **B-004**: `nozzle_clear`, the nozzle-wipe
routine behind `_NEBULAOS_NOZZLE_CLEAN`, carries a header note saying it had not been exercised
on real hardware when that note was written. It is a motion and contact routine, and the only
module declaring such a gap. The note says "as of this commit" about its own commit, not about
`a2e7634`, so whether it has since been qualified is a question for the owner rather than
something this agent can settle. The substantive one is **B-001: no printer access**, by
design - so `verify_hardware` is 0 across the whole inventory and will stay there. Everything
documented is established from source and from the repositories' own tests.

Completeness gaps - work not done rather than work unable to proceed - are counted separately
and are not blockers. Conflating the two once made this dashboard report 57% "blocked"; see
`STATUS-LOG.md`.

## History

`STATUS-LOG.md` keeps the mistakes worth remembering. The full narrative is the commit history
of this branch.
