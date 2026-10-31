# Work queue

Priority order follows `MISSION.md` Part 8.6: critical user instructions first, then safety
and recovery, then installation and setup, then high-impact screenshots, then undocumented
commands and configuration, then developer implementation references, then the rest.

Items are taken from the coverage inventory. A finished item updates `coverage.jsonl` and
the dashboard in the same batch as the page itself.

## P1 - Finish Phase 1 discovery

- [x] **Q-001** Resolve the G-code command names assembled from module constants. Done:
      8 resolved, each recorded in `tools/seed_inventory.py` next to the constant it comes
      from. Command total is 51, not the 43 the literal-string scan could see.
- [x] **Q-002** Discover configuration keys. Done: 152 Klipper extension options with
      declared types, and 20 real NebulaScreen settings. The first attempt over-collected
      badly - see the discovery mistake recorded in `STATUS.md`. Declared **defaults** are
      still to be extracted per key when each reference page is written, which is the right
      time to read them accurately.
- [x] **Q-003** Discover the Moonraker / JSON-RPC surface. Done: **56** `machine.nebulaos.*`
      endpoints plus the `nebulaos:settings_changed` notification, inventoried from the
      server-side registration table and cross-checked against the UI's call sites, plus 17
      `nebulaos_osconfig` helper modules. Still open as a smaller follow-up: the **Klipper
      status objects** the UI subscribes to via `printer.objects.subscribe` - the ~85
      pointers rejected from configuration discovery belong here, and need their
      subscription sites found before they can be inventoried honestly.
- [x] **Q-004** Discover developer-facing commands. Done for the firmware, which holds
      nearly all of them: 14 build pipeline scripts, 11 tool sets, 56 overlay runtime
      helpers. The other repositories' build entry points are covered by their
      repo-overview items and will be detailed when each developer wiki is written.
- [x] **Q-005** Inventory the update, rollback, A/B slot and recovery mechanisms. Done as
      items rather than as a file list: the update supervisor, slot swap, clean reset, OTA
      markers and image trial/confirm services, together with the `ota.*`, `image.*` and
      `updates.*` API groups.
- [x] **Q-006** Audit the 34 existing NebulaScreen wiki pages. Done: 15 move, 1 adapt,
      16 keep, 2 historical, all recorded in `coverage.jsonl` and written up in
      `REUSE-AUDIT.md`. Two problems found - a confusable page-name pair, and an install
      path that is documented but untested (now `BLOCKERS.md` B-003).
- [ ] **Q-007** Clone `nebulaos-packages` and `lv_drivers` into the docs worktree and run
      discovery on them.

## P1 - Phase 2, the end-user manual (starts as soon as discovery is deep enough)

- [x] **Q-010** Manual skeleton and navigation. Done: `wiki/` with `Home.md` and
      `_Sidebar.md` covering all ten sections, plus `tools/check_links.py` which gates
      broken links, missing images and pages unreachable from the sidebar.
- [x] **Q-011** Section 02, Installation. Done: `wiki/Installing-NebulaOS.md`, both routes,
      with the untested stock-touchscreen caveat given its own section near the top rather
      than buried.
- [x] **Q-012** Section 10, Recovery, plus the safety material. Done:
      `wiki/Recovery.md`, `wiki/Going-Back.md`, `wiki/Safety-First.md`. Trial timings
      verified in source rather than copied from the old wiki.
- [ ] **Q-017** Replace the 17 stub pages with real content, highest-traffic first:
      `First-Time-Setup`, `Connecting-To-WiFi`, `Opening-Mainsail`, then `Resetting` and
      `Updating-NebulaOS`, then `Screen-Reference`.
- [ ] **Q-013** Section 03, First-time setup - startup, Wi-Fi, finding the IP, Mainsail,
      first calibration, first print.
- [ ] **Q-014** Section 04, the complete NebulaScreen guide - 49 panels, task pages plus a
      full screen reference.
- [ ] **Q-015** Section 05, Calibration - every workflow, what it changes, how to read the
      result, verified against the calibration extensions.
- [ ] **Q-016** Sections 06 to 09 - everyday printing, advanced features, updates and
      maintenance, troubleshooting.

## P2 - Screenshots

- [ ] **Q-020** Determine whether the NebulaScreen SDL simulator builds in this workspace
      and can be driven to a known screen reproducibly. Record the method in
      `SCREENSHOTS.md` either way.
- [ ] **Q-021** Capture the install and first-setup screens first - the highest-impact
      images in the manual.
- [ ] **Q-022** Capture the remaining panels, then annotate the ones used in procedures.

## P2 - Phase 3, developer wikis, one repository at a time

- [ ] **Q-030** `NebulaOS-klipper-extensions` - the natural first one: 42 modules, 43
      commands, and a real test suite to verify against. Its wiki is **disabled** on GitHub,
      so the Markdown lands in the repository and the gap is recorded.
- [ ] **Q-031** `NebulaOS-nebulascreen` - LVGL architecture, the panel system, Moonraker
      integration, simulator, build and testing. Reuse the existing developer pages.
- [ ] **Q-032** `NebulaOS-firmware` - architecture, Buildroot, boot, A/B slots, persistent
      storage, the 35 services, OTA, rollback, integrity.
- [ ] **Q-033** `NebulaOS-klipper-mcu` - GD32F303 target, patch series, build, flash layout,
      safety.
- [ ] **Q-034** `NebulaOS-kernel` - Ingenic X2000, PREEMPT_RT, device tree, display and
      touch drivers, Wi-Fi and Bluetooth, kernel configuration. Separate what the kernel
      repository maintains from what the firmware build applies.
- [ ] **Q-035** `nebulaos-packages` and `lv_drivers`.

## P3 - Audit, publishing, maintenance

- [ ] **Q-040** Phase 5 full audit against the complete inventory.
- [ ] **Q-041** Markdown, link, image and navigation validation, run as a script.
- [ ] **Q-042** Publishing preparation: pull requests per batch, validated workflows, final
      dashboard. Publishing itself waits for the project owner.
- [ ] **Q-043** Phase 7 maintenance guide: how a contributor documents a new feature,
      refreshes screenshots and runs validation.

## Verification debt (do not let this accumulate silently)

- [ ] **Q-050** 59 inventory items require a screenshot; **0** exist. Q-020 decides whether
      the simulator can supply them. Until then every procedure page is text-only, which the
      mission explicitly calls insufficient for a beginner audience.
- [ ] **Q-051** `verify_test` is `unknown` for all 544 items. The Klipper extensions ship 31
      test files - running that suite and citing it is the cheapest real verification
      available anywhere in this project.

## From the foreground session

Requests arriving from the foreground development session are added here in priority order.

*(none yet)*

## Done

- **Q-001** G-code command constants resolved (2026-10-31).
- **Q-002** Configuration key discovery (2026-10-31), after correcting an over-collecting
  first attempt.
- **Q-003** Moonraker API discovery (2026-10-31), after fixing an extractor that dropped an
  endpoint whose path contains a digit. Klipper status objects remain as a follow-up.
- **Q-006** Reuse audit of the existing wiki (2026-10-31). The existing wiki is good and is
  being reused rather than replaced; Phase 2 is more relocation than authoring, except for
  sections 01, 03 and 06.
- **Q-004, Q-005** Build pipeline, developer tooling and runtime helpers (2026-10-31).
  Counts verified independently. Five system-named overlay shims were nearly filtered out
  as vendor noise and turned out to be NebulaOS-authored - see `STATUS.md`.
