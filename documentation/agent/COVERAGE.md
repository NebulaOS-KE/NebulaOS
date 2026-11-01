# NebulaOS documentation coverage dashboard

Generated 2026-11-01 by `documentation/agent/tools/render_dashboard.py` from `documentation/agent/coverage.jsonl`.

**Read this first.** Coverage is relative to the *discovered* inventory, not to some imagined complete list of everything NebulaOS does. Each entry records the exact source commit it was discovered at. A rise in the total item count is normal and healthy: it means discovery found more real functionality, not that documentation regressed.

Verification is reported in four separate columns because they prove different things. *Code verified* means the implementation was read. *Test verified* means a test in the repository covers it. *Hardware verified* means it was observed on a real printer - this agent has no printer access, so that column is expected to stay low and is honest about it. *Screenshot* tracks real captured images only.

## Overall

| Measure | Items | Share |
|---|---|---|
| Discovered documentation items | 549 | 100% |
| Documented (page exists and covers the item) | 260 | 47% |
| Draft | 111 | 20% |
| Missing | 178 | 32% |
| Blocked (cannot proceed without hardware, access or a decision) | 6 | 1% |
| Has a recorded completeness gap (work not done, not stuck) | 0 | 0% |

## Verification (counted separately, never combined)

| Kind | Verified | Partial | Unknown | Blocked | N/A |
|---|---|---|---|---|---|
| Code verified | 336 | 36 | 177 | 0 | 0 |
| Test verified | 29 | 0 | 520 | 0 | 0 |
| Hardware verified | 0 | 0 | 0 | 2 | 545 |

## Screenshots

| Measure | Items |
|---|---|
| Required | 57 |
| Captured and confirmed current | 41 |
| Verified against the running UI | 0 |
| Candidate image exists, version unconfirmed | 0 |
| Missing outright | 15 |
| Outdated | 0 |
| Blocked (needs real hardware) | 1 |

A *candidate* is not coverage. It means a real image exists but has not been confirmed against the commit this documentation describes, so it cannot yet be trusted to show the reader what they will see.

## By repository

| Repository | Items | Documented | Draft | Missing | Code verified | Documented % |
|---|---|---|---|---|---|---|
| NebulaOS | 11 | 10 | 0 | 1 | 10 | 90% |
| NebulaOS-firmware | 194 | 1 | 95 | 98 | 61 | 0% |
| NebulaOS-kernel | 1 | 0 | 0 | 1 | 0 | 0% |
| NebulaOS-klipper-extensions | 236 | 199 | 16 | 21 | 215 | 84% |
| NebulaOS-klipper-mcu | 1 | 0 | 0 | 1 | 0 | 0% |
| NebulaOS-nebulascreen | 104 | 50 | 0 | 54 | 50 | 48% |
| lv_drivers | 1 | 0 | 0 | 1 | 0 | 0% |
| nebulaos-packages | 1 | 0 | 0 | 1 | 0 | 0% |

## By category

| Category | Items | Documented | Draft | Missing | Documented % |
|---|---|---|---|---|---|
| api | 59 | 0 | 59 | 0 | 0% |
| build-command | 14 | 0 | 0 | 14 | 0% |
| command | 52 | 50 | 0 | 2 | 96% |
| config-option | 173 | 137 | 16 | 20 | 79% |
| developer-tool | 11 | 0 | 0 | 11 | 0% |
| existing-page | 34 | 16 | 0 | 18 | 47% |
| extension | 30 | 11 | 0 | 19 | 36% |
| os-helper | 17 | 0 | 0 | 17 | 0% |
| repo-overview | 8 | 1 | 1 | 6 | 12% |
| runtime-helper | 57 | 1 | 0 | 56 | 1% |
| screen | 49 | 34 | 0 | 15 | 69% |
| service | 35 | 0 | 35 | 0 | 0% |
| user-manual-section | 10 | 10 | 0 | 0 | 100% |

## Source revisions this inventory was discovered at

| Repository | Branch | Commit | Items |
|---|---|---|---|
| NebulaOS | main | bec4c6571243 | 11 |
| NebulaOS-firmware | main | 7b63c998b9e4 | 194 |
| NebulaOS-kernel | openke | d86790d2e231 | 1 |
| NebulaOS-klipper-extensions | main | 93224bf418d1 | 236 |
| NebulaOS-klipper-mcu | main | 33f5d16daccd | 1 |
| NebulaOS-nebulascreen | main | 59728abcc2ad | 104 |
| lv_drivers | master | not cloned l | 1 |
| nebulaos-packages | main | not cloned l | 1 |

## Blocked items

Only genuine blockers: something that cannot proceed without hardware, access or a decision this agent cannot make. Work that is simply not finished is a *completeness gap*, counted separately above - conflating the two made this dashboard report 57% "blocked", which reads as a stuck project rather than one in progress.

| Item | Repository | Reason |
|---|---|---|
| repo:nebulaos-packages | nebulaos-packages | not cloned locally; clone into _worktrees/docs |
| repo:lv_drivers | lv_drivers | not cloned locally; clone into _worktrees/docs |
| manual:02-installation | NebulaOS | verify_hardware outstanding: the stock-touchscreen route has not been observed on a printer (D-009: user pages document it as the normal route; record kept in VERIFICATION.md) |
| screen:storage_panel | NebulaOS-nebulascreen | the new Free up space button (screen 3194104) is not in the screenshot tour; needs an extra tour step or a real printer |
| screen:updates_panel | NebulaOS-nebulascreen | capture is timing-dependent without a live Moonraker: the busy/idle state varies between runs, so a published image would contradict the page. Needs a real printer. |
| gcode:NEBULAOS_BED_TRAM | NebulaOS-klipper-extensions | defined as a gcode_macro in the firmware's calibration.cfg, not registered by the extensions; verify the macro file before documenting |

