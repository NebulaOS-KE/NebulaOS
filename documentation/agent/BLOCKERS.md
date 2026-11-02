# Blockers

Honest list of what cannot be finished, and why. A blocker stays here until it is cleared,
with the work it holds up named. Nothing gets quietly dropped.

## Open

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

### B-002 - Two repositories are not cloned locally

`nebulaos-packages` and `lv_drivers` have no checkout in this workspace, so their
inventories are empty. Not a real obstacle - they will be cloned into
`_worktrees/docs/` when their turn comes.

**Holds up:** the repo-level items `repo:nebulaos-packages` and `repo:lv_drivers`.

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

*(none recorded yet)*

## Cleared

*(none yet)*
