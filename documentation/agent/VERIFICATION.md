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
specific test file and the run date.

**Corrected 2026-11-03.** This file previously listed nine modules as having no test, by the
rule *no `test_<module>.py` exists*. That rule is wrong in both directions and the real answer
is **five**:

- `nebulaos_compat` and `nebulaos_temperature_mcu` **do** have test files. They are excluded
  from the standalone run because they import real Klipper, which is a different thing from
  being untested, and conflating the two understated coverage.
- `nozzle_clear`, `z_compensate` and `nebulaos_z_offset_probe` are covered by tests named after
  what they test rather than after the file - `test_nozzle_clear_native.py`,
  `test_z_compensate_*.py`, `test_z_offset_probe_*.py`.
- `autotune_tmc` is referred to by `test_nebulaos_tmc_autotune.py`.

The five modules no test refers to are `bl24c16f`, `calibrate_shaper_config`,
`gcode_shell_command`, `motor_constants` and `virtual_pins` - **all five vendored**. Every
module NebulaOS wrote is referred to by at least one test. Coverage is now determined by
reading the test files for references to the module, not by matching filenames.

Two cautions, recorded because both nearly produced a wrong result:

- **Do not detect pass/fail with `grep '^OK'`.** `unittest` colours that line when it has a
  TTY, so the match fails and every suite looks broken. The first run here reported 29 of 29
  failing, which was entirely an artifact. Strip ANSI first. The repository's CI script is
  unaffected because CI has no TTY.
- **Do not use `unittest discover` for this suite.** It reports 42 errors, which are
  rootdir and import artifacts rather than real failures - `test_tmcstatus` passes perfectly
  when run as `extras.test_tmcstatus`. Run per-module, the way the project's own CI does.

### The package index's own tests, re-run 2026-11-11

`nebulaos-packages` has an offline suite that needs nothing but Python and a shell (no GitHub, no
Docker, no SDK). Run at `9d0d264` - the current tip of `main`, unchanged since 2026-11-03:

```
sh tests/run-tests.sh   ->   index-tests: 10 passed, 0 failed
```

Same ten tests, same result as the first run, so the four invariants that page describes still
hold as written: helpers outside `simple/`, append-only for helpers and for wheels, one ABI
failing without stopping the rest, and only `sdk-*` releases being used. That is the whole of
`verify_test: verified` for that repository - a **full** index pass is not run here, because it
needs an authenticated `gh`, Docker and the firmware build image pinned by digest.

`lv_drivers` has no tests at all, which is why its `verify_test` is `n/a` rather than `unknown`.

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

## The documented commits are the released ones (re-checked 2026-11-04)

`NebulaOS-firmware` carries the tag **`v1.0.0`**, and it resolves to **`ba98eec`** - verified
here with `git ls-remote --tags`, not taken on report. Its manifest pins:

| Component | Pin at `ba98eec` |
|---|---|
| Extensions | `f498796`, branch `production` |
| NebulaScreen | `36490ed` (`NEBULASCREEN_VERSION=v1.0.0`) |
| Kernel | `d86790d` |
| Host Klipper | `58bd67d` (upstream `Klipper3d/klipper`) |

All four are unchanged from `70ad0b0`, the commit this documentation was written against.

**And the documented behaviour is not merely similar at the release - it is identical.** Three
checks, each one a `git diff --quiet` over the whole subtree:

| Subtree | `70ad0b0` vs `ba98eec` |
|---|---|
| `scripts/build/overlay` - everything that lands on the printer | **byte-identical** |
| `manifests` | identical |
| `scripts/build` - the pipeline | identical |

The release differs from the documented commit only in `scripts/package/build-img.py` and
`validate-img.py`, which compress and check the already-built image, and in two host-only
hardware capture profiles. So every page's citations were re-pointed from `70ad0b0` to
`ba98eec`: a reader following one now lands on the **tagged release** rather than on an
untagged ancestor, and finds exactly the code the page describes.

Note the tag is **not** the tip of `main`. `d73dbe3` ("packaging check: compare the .img data
streams, not the archive sizes") came after it. `REPOSITORY_HEAD != SHIPPING_PIN`, as ever.

### Why it was rebuilt, kept as the record

The first published 1.0.0 `.img` was compressed with a 192 MB LZMA dictionary, chosen by 7-Zip
26 for `-mx=9`. Unpacking needs more memory than the printer's 248 MB, so an **online update**
ran out of memory. `ba98eec` pins `-md=16m` - about 25 MB to unpack - and `validate-img.py`
refuses a dictionary above 16 MB. Tim kept the version name and the tag was moved.

**The stock-touchscreen route was not observed failing.** It plausibly would have - same file,
same RAM, and Creality's updater also has to unpack it - but that is an inference. `BLOCKERS.md`
B-003 stays unverified rather than becoming *observed failing*; see `STATUS-LOG.md` for the
correction this agent needed on exactly that point.

## The published wiki matches the branch (checked 2026-11-04)

End-to-end, by cloning `NebulaOS-KE/NebulaOS.wiki` read-only and comparing it with `wiki/` at
`docs/agent` `e38a3c3`:

| | |
|---|---|
| Pages | **31, all byte-identical** |
| Screenshots | **129 PNGs, all byte-identical** |
| Pages on one side only | none, in either direction |

Worth doing rather than assuming, because the branch and the published wiki are two artefacts
and only one of them is what a reader sees. A screenshot that is stale **on the wiki** would be
invisible from here - the inventory would say *captured* and the reader would see something
else.

The check also answered a smaller worry the right way round. The main session's summary of the
last wiki push listed four pages, and two more had changed on the branch since the push before
it. The clone shows an intermediate wiki commit (`1f7addd`) carrying exactly those two, so
nothing was dropped - the summary described one commit, not the range.

This is read-only verification. This agent does not push to the wiki and has never run a
publish workflow.

## The Z-offset troubleshooting entry, and what was read for it (2026-11-12)

The entry in `wiki/Troubleshooting.md` describes a failure two users reported (issue #9) and a
fix that reached printers the same day. The page was written three times as the fix moved, and
each move was checked here rather than taken on report:

| When | State | Checked |
|---|---|---|
| First | `a63964a`, on no branch | the commit itself; the page named no version |
| Then | **1.0.1** = `6532091` on `main`, `production` still `178a0c2` | `extensions_version` in `nebulaos-extensions.json`; the page named the version and said *once it is on the branch printers follow* |
| Now | `production` **is** `6532091` | `git ls-remote`: `main` and `production` are the same commit, and `production` is what `[update_manager nebulaos_klipper_extensions]` follows (`primary_branch: production`) |

So the page leads with **Settings → Updates → NebulaOS extensions** and keeps the two
`printer.cfg` lines as the fallback for a printer that cannot update. The screen labels come
from `wiki/Screen-Updates.md`, which was written from the panel itself.

What was read, rather than taken from the report:

| Claim | Evidence |
|---|---|
| Both knobs the workaround uses exist on 1.0.2 | `extras/nebulaos_calibration.py` at `178a0c2`: `bootstrap_contact_envelope_mm` default **8.0**, `max_abs_fit_delta` default **0.3**, both `[nebulaos_calibration]` options |
| What the fix changes | `a63964a`: envelope default 8.0 → **5.0** *and* measured from the fresh CR-Touch reading instead of the nozzle's hover height; `max_abs_fit_delta` 0.3 → **0.5**; the bare upstream `No trigger on probe after full movement` wrapped in `_no_contact_message()` |
| Why a hand-set `z_offset` helps | `extras/nebulaos_probe_pair.py` at `178a0c2`: a credible saved offset takes the *established* path, whose floor is `raw_probe_trigger_z - probe_z_offset - established_contact_margin_mm` with that margin defaulting to **1.0 mm** - deeper than the bootstrap floor the affected units could not reach. `0.000` is explicitly a "not yet calibrated" marker (`_CREDIBLE_Z_OFFSET_EPSILON_MM`) |
| Why a second `[nebulaos_calibration]` section in `printer.cfg` overrides the firmware's | Klipper at the pinned `58bd67db`: `klippy/configfile.py` builds `configparser.RawConfigParser(strict=False, ...)`, so a later duplicate section's options win - which is why the page says the block must sit below the `[include ...]` lines |

Not verified here: that the workaround succeeds on an affected printer. No printer access, and
the two reports are the main session's, not this session's observation. The page does not say
*tested*.

## The reproducibility claim, third version (2026-11-12)

The sentence "releases are built twice on separate machines with the two results required to be
byte-identical" was wrong, and the two corrections that followed were wrong in the same way -
each took a statement about *process* from a person rather than from an artifact
(`STATUS-LOG.md` has the lesson). This is what the third version rests on, all read here:

| Claim on the pages | Evidence |
|---|---|
| 1.0.2 built twice, identical kernel and root filesystem | `docs/REPRODUCIBILITY.md` at firmware `d464b46`: Build A and Build B of `3bdf3ff` on 2026-11-09, one host, container digest `sha256:a6ba57c6…`, `xImage` `14a47aa8…`, `rootfs.squashfs` `df65c724…` |
| Those are the files in the release | the published `release-manifest.txt` for v1.0.2 carries the same `XIMAGE_SHA256` and `ROOTFS_SQUASHFS_SHA256` (downloaded from the release, not quoted from the record) |
| The download cannot be compared byte for byte | `docs/RELEASE_ARTIFACTS.md`: encrypted 7z with a fresh random AES IV; the check records `IMG_BYTE_IDENTICAL=NO` with `IMG_CONTENT_IDENTICAL=YES` |
| No location is claimed | 1.0.2's `release-manifest.txt` names `BUILD_MODE=candidate` and one local `BUILD_RUN`; the release workflow (`.github/workflows/release.yml`, 2026-10-29) exists and has run once, but not for this release |
| The kernel's part of it | `NebulaOS-kernel` `b31be02d9`, one line (`gzip -v9f` to `gzip -nv9f`), an ancestor of the 1.0.2 pin, checked by `scripts/build/01-apply-kernel-patches.sh` |

Not established, and said so wherever the claim appears: the same bytes from a **different
host** or a different container digest. Nobody has measured that.

## Source revisions

Documentation describes the **newest** code: the tip of each repository's default branch.
The firmware's `manifests/dependencies.conf` says which commit of each component the
firmware build actually ships. Where a default branch is ahead of its shipping pin, the
page documents the newest code and names the pin, so nobody mistakes development work for
released behaviour. `REPOSITORY_HEAD` is not `SHIPPING_PIN`, and the dashboard records
both.
