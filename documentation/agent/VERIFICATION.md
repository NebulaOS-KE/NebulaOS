# Verification policy

Documentation in this project is only as good as the evidence behind it. This file defines
what each state in `coverage.jsonl` means, and what it takes to claim it. Nothing here is
decorative: a status is a promise, and promoting one without the evidence is the single
worst thing this agent could do.

## The states

| State | Meaning | Evidence required |
|---|---|---|
| `verified` | Confirmed against the applicable code, and against tests or runtime evidence | Source read at a recorded commit **and** a passing test or observed runtime behaviour |
| `partial` | Some of the claim is proven, some is not | Recorded per item in `evidence`, with the gap named |
| `unknown` | Not investigated yet | - |
| `blocked` | Cannot be verified with the access available | A named missing dependency in `BLOCKERS.md` |
| `n/a` | The check does not apply to this kind of item | A reason, when it is not obvious |

Documentation status is tracked separately from verification:

| `doc_status` | Meaning |
|---|---|
| `missing` | No page covers this item |
| `draft` | A page exists but has not passed the quality checks in `MISSION.md` Part 10 |
| `documented` | A page exists and covers the item completely |
| `verified` | Documented, and every technical claim on the page is backed by recorded evidence |

The mission also asks for these dispositions where they apply; they are recorded in
`release_applicability` or in the page text itself:

- **Development only** - implemented, but not part of the supported release.
- **Historical** - was true once, or belongs to retired functionality.
- **Planned** - proposed, not implemented.

## What this agent can and cannot prove

**Can prove:** that code exists, what it does, how it is registered, what its defaults
are, which configuration keys it reads, which tests cover it, and which commit each claim
comes from. The repositories' own test suites are available and can be run - and have been.

### Test verification actually performed

Re-run on 2026-11-03 at **`f498796`** - the pin NebulaOS 1.0.0 ships, confirmed equal on
`main`, on `production` and in the firmware manifest at `70ad0b0`:

```
29 of 31 test suites run standalone, the way scripts/ci-tests.sh runs them
912 individual tests, all passing
```

Previously 899 tests at `8e3447a` (2026-10-31). Thirteen more exist now; seven of them are in
the power-loss suite, which went 169 -> 176 as the parked-nozzle resume, the current-object
restart and the timelapse frame handling landed. The other six were not traced to a suite and
that is not claimed here.

The two excluded suites (`test_nebulaos_compat`, `test_nebulaos_temperature_mcu`) import real
Klipper modules and need the pinned Klipper checkout composed in, exactly as the repository's
own CI script documents. They are not failures; they are a different run.

That result promoted `verify_test` to `verified` on **21 extension modules**, each citing the
specific test file and the run date. Nine modules have no test of their own and stay
`unknown`: `autotune_tmc`, `bl24c16f`, `calibrate_shaper_config`, `gcode_shell_command`,
`motor_constants`, `nebulaos_compat`, `nebulaos_temperature_mcu`, `prtouch_test_support`,
`virtual_pins`.

Two cautions, recorded because both nearly produced a wrong result:

- **Do not detect pass/fail with `grep '^OK'`.** `unittest` colours that line when it has a
  TTY, so the match fails and every suite looks broken. The first run here reported 29 of 29
  failing, which was entirely an artifact. Strip ANSI first. The repository's CI script is
  unaffected because CI has no TTY.
- **Do not use `unittest discover` for this suite.** It reports 42 errors, which are
  rootdir and import artifacts rather than real failures - `test_tmcstatus` passes perfectly
  when run as `extras.test_tmcstatus`. Run per-module, the way the project's own CI does.

**Cannot prove:** that any of it works on a real printer. This agent has no printer
access by design - no SSH, no hardware launcher, no Moonraker calls to a machine. So
`verify_hardware` stays `n/a` or `blocked`, and any page describing hardware behaviour
says plainly that the behaviour is established from the implementation and has not been
observed on hardware by the author of the page.

Implementation is evidence of *intended and implemented* behaviour. It is not evidence of
successful hardware operation, and this agent will not blur the two.

## Recording evidence

Every technical claim carries a reference in the item's `evidence` list, in the form
`<repo>@<commit>:<path>#<symbol>`, for example:

```
NebulaOS-klipper-extensions@8e3447a:extras/nebulaos_beeper.py#cmd_NEBULAOS_BEEP
```

Pages cite the same references, pinned to the exact commit, so a reader can check any
sentence against the source it came from.

## Hardware verification still outstanding

Kept here on Tim's instruction (2026-11-01, widened 2026-11-02 — see `DECISIONS.md` D-011),
because the user-facing pages no longer carry it. **No page in the manual states whether
anything has been tested.** This file and `coverage.jsonl` are the whole record.

Not observed on a printer by this agent, and so recorded only here:

| Behaviour | Where it is documented | Established from |
|---|---|---|
| Installing from stock Creality firmware via the touchscreen | `Installing-NebulaOS` | source only (see below) |
| USB recovery, both the slot-marker rewrite and the full `.ingenic` rewrite | `Recovery` | source and the firmware's own recovery tooling |
| The image trial and automatic rollback | `Recovery` | firmware `70ad0b0`, `nebulaos_osconfig/image.py` |
| Power-loss resume ordering, and the cleanup after a failed resume | `Power-Loss-Recovery` | extensions `f498796` and the repository's own tests |
| Statistics, including the one-time import of the pre-NebulaOS figures | `Screen-Reference` | screen `36490ed`, firmware `70ad0b0`; reported working on `ke-dev` by Tim |

**Installing from stock Creality firmware using the printer's touchscreen has not been
observed on a printer by this agent.** The existing wiki recorded on 2026-10-29 that only the
OpenKE/SSH route had been tested. User pages now present the touchscreen route as the normal
route (decision D-009); the route's `verify_hardware` stays unverified in `coverage.jsonl`.

What *is* established from source: the checks run before anything is written, so a failure
stops without changing the running system. What is not established: that the route completes
successfully on real hardware.

## Source revisions

Documentation describes the **newest** code: the tip of each repository's default branch.
The firmware's `manifests/dependencies.conf` says which commit of each component the
firmware build actually ships. Where a default branch is ahead of its shipping pin, the
page documents the newest code and names the pin, so nobody mistakes development work for
released behaviour. `REPOSITORY_HEAD` is not `SHIPPING_PIN`, and the dashboard records
both.
