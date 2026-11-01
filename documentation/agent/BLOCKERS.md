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

## Code problems found while documenting

Discrepancies between code and documentation go here, never into a code change. This agent
does not edit production code, tests or configuration to make documentation look right.

*(none recorded yet)*

## Cleared

*(none yet)*
