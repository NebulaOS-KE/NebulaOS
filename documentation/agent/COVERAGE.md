# NebulaOS documentation coverage dashboard

Generated 2026-11-03 by `documentation/agent/tools/render_dashboard.py` from `documentation/agent/coverage.jsonl`.

**Read this first.** Coverage is relative to the *discovered* inventory, not to some imagined complete list of everything NebulaOS does. Each entry records the exact source commit it was discovered at. A rise in the total item count is normal and healthy: it means discovery found more real functionality, not that documentation regressed.

Verification is reported in four separate columns because they prove different things. *Code verified* means the implementation was read. *Test verified* means a test in the repository covers it. *Hardware verified* means it was observed on a real printer - this agent has no printer access, so that column is expected to stay low and is honest about it. *Screenshot* tracks real captured images only.

## Overall

| Measure | Items | Share |
|---|---|---|
| Discovered documentation items | 552 | 100% |
| Documented (page exists and covers the item) | 472 | 85% |
| Draft | 22 | 3% |
| Missing | 58 | 10% |
| Blocked (cannot proceed without hardware, access or a decision) | 4 | 0% |
| Has a recorded completeness gap (work not done, not stuck) | 15 | 2% |

## Verification (counted separately, never combined)

| Kind | Verified | Partial | Unknown | Blocked | N/A |
|---|---|---|---|---|---|
| Code verified | 485 | 8 | 59 | 0 | 0 |
| Test verified | 47 | 0 | 504 | 0 | 1 |
| Hardware verified | 0 | 0 | 0 | 2 | 547 |

## Screenshots

| Measure | Items |
|---|---|
| Required | 58 |
| Captured and confirmed current | 42 |
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
| NebulaOS-firmware | 196 | 158 | 20 | 18 | 171 | 80% |
| NebulaOS-kernel | 1 | 1 | 0 | 0 | 1 | 100% |
| NebulaOS-klipper-extensions | 236 | 215 | 0 | 21 | 215 | 91% |
| NebulaOS-klipper-mcu | 1 | 1 | 0 | 0 | 1 | 100% |
| NebulaOS-nebulascreen | 105 | 85 | 2 | 18 | 85 | 80% |
| lv_drivers | 1 | 1 | 0 | 0 | 1 | 100% |
| nebulaos-packages | 1 | 1 | 0 | 0 | 1 | 100% |

## By category

| Category | Items | Documented | Draft | Missing | Documented % |
|---|---|---|---|---|---|
| api | 60 | 47 | 13 | 0 | 78% |
| build-command | 14 | 0 | 7 | 7 | 0% |
| command | 52 | 50 | 0 | 2 | 96% |
| config-option | 173 | 173 | 0 | 0 | 100% |
| developer-tool | 11 | 0 | 0 | 11 | 0% |
| existing-page | 34 | 16 | 0 | 18 | 47% |
| extension | 30 | 11 | 0 | 19 | 36% |
| os-helper | 18 | 18 | 0 | 0 | 100% |
| repo-overview | 8 | 7 | 0 | 1 | 87% |
| runtime-helper | 57 | 57 | 0 | 0 | 100% |
| screen | 50 | 48 | 2 | 0 | 96% |
| service | 35 | 35 | 0 | 0 | 100% |
| user-manual-section | 10 | 10 | 0 | 0 | 100% |

## Source revisions this inventory was discovered at

| Repository | Branch | Commit | Items |
|---|---|---|---|
| NebulaOS | main | bef8693fb1f4 | 11 |
| NebulaOS-firmware | main | a53e129bf1b0 | 196 |
| NebulaOS-kernel | openke | d86790d2e231 | 1 |
| NebulaOS-klipper-extensions | main | f498796fcaa2 | 236 |
| NebulaOS-klipper-mcu | main | 33f5d16daccd | 1 |
| NebulaOS-nebulascreen | main | 36490ed0b60d | 105 |
| lv_drivers | master | not cloned l | 1 |
| nebulaos-packages | main | not cloned l | 1 |

## Blocked items

Only genuine blockers: something that cannot proceed without hardware, access or a decision this agent cannot make. Work that is simply not finished is a *completeness gap*, counted separately above - conflating the two made this dashboard report 57% "blocked", which reads as a stuck project rather than one in progress.

| Item | Repository | Reason |
|---|---|---|
| manual:02-installation | NebulaOS | verify_hardware outstanding: the stock-touchscreen route has not been observed on a printer (D-009: user pages document it as the normal route; record kept in VERIFICATION.md) |
| screen:storage_panel | NebulaOS-nebulascreen | the Free up space / Clean up Creality buttons (screen 36490ed) are not in the screenshot tour; needs an extra tour step or a real printer |
| screen:updates_panel | NebulaOS-nebulascreen | capture is timing-dependent without a live Moonraker: the busy/idle state varies between runs, so a published image would contradict the page. Needs a real printer. |
| gcode:NEBULAOS_BED_TRAM | NebulaOS-klipper-extensions | defined as a gcode_macro in the firmware's calibration.cfg, not registered by the extensions; verify the macro file before documenting |

