# Work queue

Priority order follows `MISSION.md` Part 8.6: critical user instructions first, then safety
and recovery, then installation and setup, then high-impact screenshots, then undocumented
commands and configuration, then developer implementation references, then the rest.

Items are taken from the coverage inventory. A finished item updates `coverage.jsonl` and
the dashboard in the same batch as the page itself.

## P1 - Finish Phase 1 discovery

- [ ] **Q-001** Resolve the 2 G-code command names assembled from module constants
      (`nebulaos_bed_tram.py`, `nebulaos_load_cell_calibration.py`) and add them to the
      inventory as literal command names.
- [ ] **Q-002** Discover configuration keys: every `config.get*` call in the Klipper
      extensions, plus the NebulaScreen configuration schema, with types and real defaults.
      One inventory item per key.
- [ ] **Q-003** Discover the Moonraker / JSON-RPC and WebSocket surface NebulaScreen uses,
      plus NebulaOS-specific methods and Klipper status objects.
- [ ] **Q-004** Discover developer-facing commands: make targets, build scripts, diagnostic
      and recovery scripts, CI workflows, across all five cloned repositories.
- [ ] **Q-005** Inventory the update, rollback, A/B slot and recovery mechanisms in the
      firmware repository as documentation items, not just as files.
- [ ] **Q-006** Audit the 34 existing NebulaScreen wiki pages: for each, decide reuse,
      adapt-and-move, or supersede, and record the decision in the inventory.
- [ ] **Q-007** Clone `nebulaos-packages` and `lv_drivers` into the docs worktree and run
      discovery on them.

## P1 - Phase 2, the end-user manual (starts as soon as discovery is deep enough)

- [ ] **Q-010** Manual skeleton and navigation: `wiki/` in the central repository, home page
      and sidebar covering all ten sections.
- [ ] **Q-011** Section 02, Installation - the highest-risk procedure a user will ever
      follow. Download, choose the right file, prepare USB, install from stock, install from
      OpenKE, first boot, and how to go back. Verified against the firmware's own install
      and recovery scripts.
- [ ] **Q-012** Section 10, Recovery, and the safety material in section 01. Written early
      and deliberately: a user who follows the install guide needs the way out to already
      exist.
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

## From the foreground session

Requests arriving from the foreground development session are added here in priority order.

*(none yet)*

## Done

*(nothing yet - the infrastructure above is Phase 0, recorded in `STATUS.md`)*
