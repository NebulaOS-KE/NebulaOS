# NebulaOS documentation coverage dashboard

Generated 2026-11-01 by `documentation/agent/tools/render_dashboard.py` from `documentation/agent/coverage.jsonl`.

**Read this first.** Coverage is relative to the *discovered* inventory, not to some imagined complete list of everything NebulaOS does. Each entry records the exact source commit it was discovered at. A rise in the total item count is normal and healthy: it means discovery found more real functionality, not that documentation regressed.

Verification is reported in four separate columns because they prove different things. *Code verified* means the implementation was read. *Test verified* means a test in the repository covers it. *Hardware verified* means it was observed on a real printer - this agent has no printer access, so that column is expected to stay low and is honest about it. *Screenshot* tracks real captured images only.

## Overall

| Measure | Items | Share |
|---|---|---|
| Discovered documentation items | 544 | 100% |
| Documented (page exists and covers the item) | 15 | 2% |
| Draft | 3 | 0% |
| Missing | 526 | 96% |
| Blocked | 11 | 2% |

## Verification (counted separately, never combined)

| Kind | Verified | Partial | Unknown | Blocked | N/A |
|---|---|---|---|---|---|
| Code verified | 16 | 2 | 526 | 0 | 0 |
| Test verified | 24 | 0 | 520 | 0 | 0 |
| Hardware verified | 0 | 0 | 0 | 2 | 542 |

## Screenshots

| Measure | Items |
|---|---|
| Required | 59 |
| Captured and confirmed current | 37 |
| Verified against the running UI | 0 |
| Candidate image exists, version unconfirmed | 0 |
| Missing outright | 21 |
| Outdated | 0 |
| Blocked (needs real hardware) | 1 |

A *candidate* is not coverage. It means a real image exists but has not been confirmed against the commit this documentation describes, so it cannot yet be trusted to show the reader what they will see.

## By repository

| Repository | Items | Documented | Draft | Missing | Code verified | Documented % |
|---|---|---|---|---|---|---|
| NebulaOS | 11 | 4 | 2 | 5 | 4 | 36% |
| NebulaOS-firmware | 191 | 0 | 1 | 190 | 1 | 0% |
| NebulaOS-kernel | 1 | 0 | 0 | 1 | 0 | 0% |
| NebulaOS-klipper-extensions | 234 | 7 | 0 | 227 | 7 | 2% |
| NebulaOS-klipper-mcu | 1 | 0 | 0 | 1 | 0 | 0% |
| NebulaOS-nebulascreen | 104 | 4 | 0 | 100 | 4 | 3% |
| lv_drivers | 1 | 0 | 0 | 1 | 0 | 0% |
| nebulaos-packages | 1 | 0 | 0 | 1 | 0 | 0% |

## By category

| Category | Items | Documented | Draft | Missing | Documented % |
|---|---|---|---|---|---|
| api | 57 | 0 | 1 | 56 | 0% |
| build-command | 14 | 0 | 0 | 14 | 0% |
| command | 51 | 5 | 0 | 46 | 9% |
| config-option | 172 | 0 | 0 | 172 | 0% |
| developer-tool | 11 | 0 | 0 | 11 | 0% |
| existing-page | 34 | 4 | 0 | 30 | 11% |
| extension | 30 | 2 | 0 | 28 | 6% |
| os-helper | 17 | 0 | 0 | 17 | 0% |
| repo-overview | 8 | 0 | 0 | 8 | 0% |
| runtime-helper | 56 | 0 | 0 | 56 | 0% |
| screen | 49 | 0 | 0 | 49 | 0% |
| service | 35 | 0 | 0 | 35 | 0% |
| user-manual-section | 10 | 4 | 2 | 4 | 40% |

## Source revisions this inventory was discovered at

| Repository | Branch | Commit | Items |
|---|---|---|---|
| NebulaOS | main | not cloned l | 11 |
| NebulaOS-firmware | main | 82e132088fc7 | 191 |
| NebulaOS-kernel | openke | d86790d2e231 | 1 |
| NebulaOS-klipper-extensions | main | a2e763460bb0 | 234 |
| NebulaOS-klipper-mcu | main | 33f5d16daccd | 1 |
| NebulaOS-nebulascreen | main | 94869f756572 | 104 |
| lv_drivers | master | not cloned l | 1 |
| nebulaos-packages | main | not cloned l | 1 |

## Blocked items

| Item | Repository | Reason |
|---|---|---|
| repo:nebulaos-packages | nebulaos-packages | not cloned locally; clone into _worktrees/docs |
| repo:lv_drivers | lv_drivers | not cloned locally; clone into _worktrees/docs |
| manual:01-start-here | NebulaOS | sections on supported hardware and terminology are still stubs |
| manual:02-installation | NebulaOS | verify_hardware outstanding: the stock-touchscreen route has not been observed on a printer (D-009: user pages document it as the normal route; record kept in VERIFICATION.md) |
| manual:07-advanced | NebulaOS | camera, Spoolman, adaptive meshing, macros and console sections still stubs |
| screen:exclude_object_panel | NebulaOS-nebulascreen | not covered by the simulator screenshot tour; needs an extra tour step or a manual capture |
| screen:printer_select_panel | NebulaOS-nebulascreen | not covered by the simulator screenshot tour; needs an extra tour step or a manual capture |
| screen:spoolman_panel | NebulaOS-nebulascreen | not covered by the simulator screenshot tour; needs an extra tour step or a manual capture |
| screen:storage_panel | NebulaOS-nebulascreen | the new Free up space button (screen 3194104) is not in the screenshot tour; needs an extra tour step or a real printer |
| screen:tmc_tune_panel | NebulaOS-nebulascreen | not covered by the simulator screenshot tour; needs an extra tour step or a manual capture |
| screen:updates_panel | NebulaOS-nebulascreen | capture is timing-dependent without a live Moonraker: the busy/idle state varies between runs, so a published image would contradict the page. Needs a real printer. |

