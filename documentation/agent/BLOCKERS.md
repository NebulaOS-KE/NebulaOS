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

## Code problems found while documenting

Discrepancies between code and documentation go here, never into a code change. This agent
does not edit production code, tests or configuration to make documentation look right.

*(none recorded yet)*

## Cleared

*(none yet)*
