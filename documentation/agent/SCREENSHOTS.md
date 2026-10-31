# Screenshot inventory

The end-user manual has to be genuinely visual - a beginner following a procedure needs to
see the screen they are looking at. This file tracks what is needed, what exists, and what
cannot be captured.

## Rules

Real captures only. Screenshots come from one of three places, in this order of preference:

1. Real NebulaOS hardware, when authorised. **Not available to this agent** (see `BLOCKERS.md` B-001).
2. The actual NebulaScreen application running in the SDL simulator, built from a recorded commit.
3. Existing repository images, but only after confirming they match the version being documented.

Never from an image model. Never recreated from memory. Never with edited labels or
invented application states. If a screen cannot be captured, it is recorded as blocked
here - an image that lies is worse than an image that is missing.

Each capture records the commit of the application it came from, so stale images can be
found later instead of quietly misleading readers.

## Required screenshots

The required set is generated from `coverage.jsonl`: every item with
`screenshot_required: true`. As of the current inventory that is **59** items - 49
NebulaScreen panels plus the 10 end-user manual sections, each of which needs several
images across its workflow.

Per-workflow, the mission requires captures of the starting state, the navigation step,
the selection screen, any input dialog, the confirmation dialog, the in-progress state,
successful completion, and the important error states. One image per page is not screenshot
coverage and is not counted as such.

## Status

| Measure | Count |
|---|---|
| Required (inventory items) | 59 |
| Captured | 0 |
| Verified against the running UI | 0 |
| Missing | 59 |
| Blocked (hardware only) | 0 recorded so far |

## Capture method

Not yet established. The next step is to check whether the NebulaScreen SDL simulator can
be built in this workspace and driven to a known screen reproducibly - the repository has
simulator helpers (`sim_*`) and a documented development/simulator workflow. If reproducible
capture works, it becomes a small scripted process that records the commit with each image.
If it turns out to be fragile, direct manual capture from the simulator is preferred over
building elaborate infrastructure.

Building the simulator in this agent's own worktree is permitted. Firmware builds are not.
