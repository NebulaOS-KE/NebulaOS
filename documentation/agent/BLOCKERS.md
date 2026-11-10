# Blockers

Honest list of what cannot be finished, and why. A blocker stays here until it is cleared,
with the work it holds up named. Nothing gets quietly dropped.

## Open

### B-005 - CLOSED (2026-11-04): the screen now names the real reason

**Found 2026-11-04** while checking the main session's report that the OTA retest produced
*"a print was started"* for a `LOW_MEMORY` stop. Firmware `53502bb` fixes the cause it found -
`_stop_check` now uses the `image_switch` profile, which excludes `LOW_MEMORY`. **The wording
bug itself is in NebulaScreen and is not fixed by that commit.**

The firmware carries the real reason. `image.py`'s `stopped()` writes
`phase="stopped_print"` **plus** `error=<reason>` and `message=<the real message>`:

```python
_state(state="failed", phase="stopped_print", error=busy["reason"],
       message=STOPPED_MESSAGE % busy["message"], ...)
```

The screen ignores both and keys only on the phase name
(`src/nebulaos_image.cpp`, the `phase == "stopped_print"` branch):

> "Stopped because a print was started. Nothing changed. Install again after the print."

But `image_switch` still counts **`PRINTING`, `PAUSED`, `ACTIVE`, `CALIBRATING`, `UPDATING`,
`UNKNOWN`, `update_manager`**. Stop an install because a calibration is running and the screen
still says a print was started.

**Narrower than it was, not gone.** `LOW_MEMORY` was the likely trigger in practice and it has
been removed from the profile, so the reported symptom should not recur. The mismatch remains
for the other six.

**Fixed in NebulaScreen `123ef31`**, pinned by firmware `f73b851`, within hours of the report.
The screen now uses the `message` the worker already sent - which names the real reason - and
falls back to *"Stopped because the printer became busy"* when there is none, rather than
naming a print. The source comment records why the phase keeps its misleading name:
*"The phase is named after a print, but any busy reason stops it."* Two tests came with it.

**Reported, not fixed here** - production code is not this agent's to write. What made the
report actionable was that the data was already arriving: the firmware had been sending
`error` and `message` all along, and only the screen's rendering ignored them.

**Held up:** nothing documented, then or now. No page states which reason a stopped install
reports - and now that the screen relays the firmware's own message, no page needs to.

### B-001 - No printer access (by design)

Hardware verification and real-hardware screenshots are out of reach: this session has no
SSH, no hardware launcher and no Moonraker connection to a machine. That is a deliberate
safety boundary, not a fault to work around.

**Holds up:** `verify_hardware` for every runtime behaviour; any screenshot that can only
be produced on a real display.

**Mitigation:** build the NebulaScreen SDL simulator in a local worktree and capture
screens from the real application there. Pages state clearly when behaviour is established
from source rather than observed on hardware. Genuinely hardware-only captures are recorded
as blocked in `SCREENSHOTS.md` rather than faked or skipped silently.

### B-002 - CLOSED (2026-11-03): both repositories are cloned and documented

`nebulaos-packages` and `lv_drivers` had no checkout in this workspace, so their inventories
were empty. Both are now cloned into `_worktrees/docs/`, read, and documented:

| Repository | Branch | Pull request |
|---|---|---|
| `nebulaos-packages` | `docs/packages` | [#2](https://github.com/NebulaOS-KE/nebulaos-packages/pull/2) |
| `lv_drivers` | `docs/lv-drivers` | [#1](https://github.com/NebulaOS-KE/lv_drivers/pull/1) |

**Every repository in the organisation now has documentation.** This was never a real
obstacle - only an unvisited corner - and it is recorded as closed rather than deleted so the
inventory's history stays readable.

### B-003 - CLOSED as a documentation blocker (2026-11-01), still an open verification gap

`Installing-NebulaOS.md` says plainly: *"Tested from OpenKE on 2026-10-29. The path through
Creality's touchscreen is not tested yet."* That untested path - installing from stock
Creality firmware using the printer's own touchscreen - is the one most first-time users will
take, because most arrive from stock firmware rather than from OpenKE.

The caveat is preserved verbatim in the central manual, with the same prominence. It cannot
be cleared here: verifying it needs a printer running stock firmware, and this agent has no
hardware access.

**Holds up:** `verify_hardware` for the installation section, and any claim that the stock
touchscreen route works.

**Resolution as a documentation question:** Tim decided on 2026-11-01 that the wiki should
assume the route works and document it as the normal route, with the record kept in
`VERIFICATION.md` only. Applied - see decision D-009. No user-facing page carries the warning
any more, and no page claims the route is tested either.

**Still open as verification:** `verify_hardware` for the installation item remains unverified
and only a printer run can change that. This is no longer blocking documentation work.

**Closed outright on 2026-11-02** (Tim, relayed by the main session): the route stays the normal
route and the manual says nothing about what was tested — see `DECISIONS.md` D-011. The
verification record stays in `VERIFICATION.md` and `coverage.jsonl`.

### B-004 - CLOSED (2026-11-01): the note was stale, not a gap

`extras/nozzle_clear.py`, the native nozzle-wipe routine behind
`_NEBULAOS_NOZZLE_CLEAN`, carries a note in its own header stating that the module **had not
been exercised on real hardware** when that note was written, and that it was enabled for a
Phase 1.8B integration candidate by source-level activation.

The flag name inverts, which is worth stating plainly: `HARDWARE_BEHAVIOR_BLOCKED = False`
means the routine is **not** blocked and does run. The guard raises only when it is `True`.

It matters because this is a motion and contact routine - it heats, probes two randomised
points on the wipe pad, and drags the nozzle between them under load. It is the only module in
the extensions carrying such a note.

**Resolution.** The owner reports that `_NEBULAOS_NOZZLE_CLEAN` has run on the development
printer more than once, and the code corroborates that it would: auto calibration invokes it
at `nebulaos_calibration.py:1762`, so anyone running auto calibration exercises this routine.
The header comment is stale and is to be corrected in the extensions repository.

Recording this one carefully was worthwhile, and so is recording how it closed. The inventory
now says `verify_hardware: reported-by-owner` rather than `verified` - because the call site is
something this agent checked, while the hardware runs are the owner's report. Those are
different kinds of evidence and collapsing them into "verified" would overstate what this
documentation knows.

Raising it as a question rather than a finding turned out to be the right call: the answer was
that the source comment was wrong, which is not something this agent could have established
alone.

## Code problems found while documenting

Discrepancies between code and documentation go here, never into a code change. This agent
does not edit production code, tests or configuration to make documentation look right.

**2026-11-06, found during the wiki restructure (firmware `dc868e3`, screen `fd47cb6`,
extensions `f498796`). Reported to the main session; none changed.**

- **Release notes 1.0.1, "Adaptive print start: an automatic nozzle wipe".** `START_PRINT`
  (`print.cfg:158-278`) has no nozzle wipe or clean. The nozzle clean is a step of Auto
  Calibration (`nebulaos_calibration.py:1753-1762`) and a separate macro
  `NEBULAOS_NOZZLE_CLEAN` (`calibration.cfg:109-112`). The manual says so.
- **Release notes 1.0.1, "For tinkerers: SSH and SFTP access, `sudo`".** `/usr/bin/sudo` is an
  adapter that only runs `reboot`/`poweroff`/`halt` for a caller that is already root (its own
  header). There is no general sudo. The manual says root needs none.
- **Firmware `docs/INSTALL_FROM_STOCK.md`** (stock touchscreen section) still says to copy
  `NebulaOS-Ender3V3KE-<version>.img` and "Not tested on hardware yet"; the 1.0.1 notes and the
  ke-dev run say the touchscreen needs the `ota_img` file. Developer doc, firmware repository.
- **Not settled from source:** which mainboard firmware OpenKE leaves and whether it matches
  the single `KNOWN_STOCK` identity (`mcu_known_identities.py:45-47`); so whether NebulaOS
  re-flashes after an OpenKE install. The manual gives the screen's notices as the trigger.

**2026-11-10, found while refreshing the MCU documentation at the 1.0.2 pins. Not changed -
documented instead.**

- **Two copies of `creality_flash.py`, and the shipped one is not the repository's.**
  `NebulaOS-klipper-mcu/tools/creality_flash.py` still hashes to the value its provenance sidecar
  in `NebulaOS-firmware` records (`57a9bf4...`, copied at mcu commit `c793e77`), while the copy
  the image deploys to `/opt/nebulaos/tools/` is `3727622...`. The difference is two fixes that
  only real hardware surfaced: opening the serial port with DTR and RTS low in the form pyserial
  3.5 supports (the keyword form raises `ValueError`; the guard could not open the port at all on
  ke-dev on 2026-10-03), and closing the transport before the post-flash identify (without it
  every successful restore was reported `FLASH_FAILED`, ke-dev 2026-11-05). A developer using the
  mcu repository's copy against a printer gets the old behaviour. The mcu README on `docs/mcu`
  now says so; back-porting the fixes, or making the deployed copy a checked copy rather than a
  manual one, is a code decision for the owner.
- **`NebulaOS-klipper-mcu`'s README said no firmware built there had ever been flashed to a real
  printer.** The firmware repository's own records contradict it (the 2026-08-28 live
  qualification of candidate-001, built from this patch queue; the restore path exercised again
  on 2026-11-05). This is documentation, so it was corrected on `docs/mcu` rather than reported:
  the status line still claims no hardware qualification - that is the owner's call and
  `compatibility.json` is untouched - but it now reads as *no claim* instead of *never run*.

## Cleared

*(none yet)*
