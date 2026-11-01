# Status

<!-- BEGIN GENERATED STATUS -->
*Figures generated 2026-11-01 from `coverage.jsonl` by `tools/render_dashboard.py`. Do not edit this block by hand.*

| | |
|---|---|
| Discovered items | **547** |
| Documented | **199** (36%) |
| Draft | 168 |
| Missing | 180 |
| Code verified | 332 |
| Test verified | 28 |
| Hardware verified | 0 |
| Screenshots required / captured | 57 / 41 |
| Blocked (cannot proceed) | 6 |
| Completeness gaps (work not done) | 311 |

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
checked fact that every option needs a Klipper restart, and now a **per-option Purpose column**
for 80 of the 155 - 43 written by reading the module, 37 quoted from the author's own comment
above the option and labelled as such.

Only those 80 are promoted. **72 keep a dash** and stay draft, because a dash is the honest
answer where neither a reading nor a comment exists; the alternative is a sentence invented
from the option's name.

An earlier attempt promoted all 152 on the strength of a section-level purpose, taking coverage
from 21% to 49% in one step. It was reverted the same iteration - see `STATUS-LOG.md`, along
with the separate episode where the purposes file itself sat in the wrong repository and
contributed nothing.

Marking them documented once took the headline from 14% to 49% in a single step. That was
flattering and false, and reverting it is recorded in `STATUS-LOG.md`.

## Open pull requests

| Repository | PR | Contents |
|---|---|---|
| `NebulaOS` | [#3](https://github.com/NebulaOS-KE/NebulaOS/pull/3) | The complete end-user manual: 29 pages, 128 screenshots, plus this agent's dashboard and tooling |
| `NebulaOS-klipper-extensions` | [#3](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions/pull/3) | 49 commands, 155 configuration options, developer README |
| `NebulaOS-firmware` | [#5](https://github.com/NebulaOS-KE/NebulaOS-firmware/pull/5) | 58 Moonraker API endpoints, 35 boot services, developer README |

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
| `NebulaOS-firmware` | `main` | `c377230` |
| `NebulaOS-nebulascreen` | `main` | `3194104` |
| `NebulaOS-klipper-extensions` | `main` | `a2e7634` |
| `NebulaOS-klipper-mcu` | `main` | `33f5d16` |
| `NebulaOS-kernel` | `openke` | `d86790d` |

The firmware manifest currently pins the extensions and the screen at exactly these commits,
so for those two there is no gap between documented and shipped behaviour.

Read evidence from the pinned worktrees under `_worktrees/docs/`, never from the checkouts at
the workspace root - those belong to the foreground session and move without warning.

## Next

1. **Q-036 configuration half** - the 155 extension options still need purpose, runtime
   behaviour, restart requirement and an example. Unlike the commands, these are *not*
   mechanically derivable: a `config.getfloat('duty', 0.5)` call gives the name, type, default
   and range but says nothing about what the setting is for. This needs reading each module,
   not a better parser.
2. **Q-037** - response examples for the firmware API, from `nebulaos_osconfig/` and the
   fixtures in `tests/nebulaos-osconfig-tests.py`.
3. `NebulaOS-nebulascreen` developer pages - LVGL architecture, the panel system, Moonraker
   integration, the simulator, build and testing. **Two real doc bugs to fix while there:** its
   `Building-from-Source` page still says to clone `coreflake1/NebulaOS-guppyscreen`, and its
   documented `LDFLAGS` contain `-static`, which cannot link here.
4. `NebulaOS-klipper-mcu` and `NebulaOS-kernel`.
5. `nebulaos-packages` and `lv_drivers` - still not cloned locally.
6. The firmware's build pipeline, runtime helpers, and A/B / OTA / recovery as an architecture
   rather than a file list.

## Open blockers

Six, all genuine, in `BLOCKERS.md`. The substantive one is **B-001: no printer access**, by
design - so `verify_hardware` is 0 across the whole inventory and will stay there. Everything
documented is established from source and from the repositories' own tests.

Completeness gaps - work not done rather than work unable to proceed - are counted separately
and are not blockers. Conflating the two once made this dashboard report 57% "blocked"; see
`STATUS-LOG.md`.

## History

`STATUS-LOG.md` keeps the mistakes worth remembering. The full narrative is the commit history
of this branch.
