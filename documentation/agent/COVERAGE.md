# NebulaOS documentation coverage dashboard

Generated 2026-10-31 by `documentation/agent/tools/render_dashboard.py` from `documentation/agent/coverage.jsonl`.

**Read this first.** Coverage is relative to the *discovered* inventory, not to some imagined complete list of everything NebulaOS does. Each entry records the exact source commit it was discovered at. A rise in the total item count is normal and healthy: it means discovery found more real functionality, not that documentation regressed.

Verification is reported in four separate columns because they prove different things. *Code verified* means the implementation was read. *Test verified* means a test in the repository covers it. *Hardware verified* means it was observed on a real printer - this agent has no printer access, so that column is expected to stay low and is honest about it. *Screenshot* tracks real captured images only.

## Overall

| Measure | Items | Share |
|---|---|---|
| Discovered documentation items | 429 | 100% |
| Documented (page exists and covers the item) | 0 | 0% |
| Draft | 0 | 0% |
| Missing | 429 | 100% |
| Blocked | 2 | 0% |

## Verification (counted separately, never combined)

| Kind | Verified | Partial | Unknown | Blocked | N/A |
|---|---|---|---|---|---|
| Code verified | 0 | 0 | 429 | 0 | 0 |
| Test verified | 0 | 0 | 429 | 0 | 0 |
| Hardware verified | 0 | 0 | 0 | 0 | 429 |

## Screenshots

| Measure | Items |
|---|---|
| Required | 59 |
| Captured | 0 |
| Verified against the running UI | 0 |
| Missing | 59 |
| Outdated | 0 |
| Blocked (needs real hardware) | 0 |

## By repository

| Repository | Items | Documented | Draft | Missing | Code verified | Documented % |
|---|---|---|---|---|---|---|
| NebulaOS | 11 | 0 | 0 | 11 | 0 | 0% |
| NebulaOS-firmware | 110 | 0 | 0 | 110 | 0 | 0% |
| NebulaOS-kernel | 1 | 0 | 0 | 1 | 0 | 0% |
| NebulaOS-klipper-extensions | 234 | 0 | 0 | 234 | 0 | 0% |
| NebulaOS-klipper-mcu | 1 | 0 | 0 | 1 | 0 | 0% |
| NebulaOS-nebulascreen | 70 | 0 | 0 | 70 | 0 | 0% |
| lv_drivers | 1 | 0 | 0 | 1 | 0 | 0% |
| nebulaos-packages | 1 | 0 | 0 | 1 | 0 | 0% |

## By category

| Category | Items | Documented | Draft | Missing | Documented % |
|---|---|---|---|---|---|
| api | 57 | 0 | 0 | 57 | 0% |
| command | 51 | 0 | 0 | 51 | 0% |
| config-option | 172 | 0 | 0 | 172 | 0% |
| extension | 30 | 0 | 0 | 30 | 0% |
| os-helper | 17 | 0 | 0 | 17 | 0% |
| repo-overview | 8 | 0 | 0 | 8 | 0% |
| screen | 49 | 0 | 0 | 49 | 0% |
| service | 35 | 0 | 0 | 35 | 0% |
| user-manual-section | 10 | 0 | 0 | 10 | 0% |

## Source revisions this inventory was discovered at

| Repository | Branch | Commit | Items |
|---|---|---|---|
| NebulaOS | main | not cloned l | 11 |
| NebulaOS-firmware | main | 82e132088fc7 | 110 |
| NebulaOS-kernel | openke | d86790d2e231 | 1 |
| NebulaOS-klipper-extensions | main | 8e3447ac0da4 | 234 |
| NebulaOS-klipper-mcu | main | 33f5d16daccd | 1 |
| NebulaOS-nebulascreen | main | 94869f756572 | 70 |
| lv_drivers | master | not cloned l | 1 |
| nebulaos-packages | main | not cloned l | 1 |

## Blocked items

| Item | Repository | Reason |
|---|---|---|
| repo:nebulaos-packages | nebulaos-packages | not cloned locally; clone into _worktrees/docs |
| repo:lv_drivers | lv_drivers | not cloned locally; clone into _worktrees/docs |

