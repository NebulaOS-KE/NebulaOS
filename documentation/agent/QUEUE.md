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
- [~] **Q-017** Replace the stub pages with real content. Done so far:
      `First-Time-Setup`, `Connecting-To-WiFi`, `Opening-Mainsail`, `Power-Loss-Recovery`,
      **all 17 done**, plus 6 calibration sub-pages brought across that were never stubs.
      The manual is 29 pages with no stubs remaining.
- [ ] **Q-018** Describe the 21 panels that `Screen-Reference.md` only indexes with a pointer.
      They are counted `missing`, not credited to the pointer.
- [ ] **Q-013** Section 03, First-time setup - startup, Wi-Fi, finding the IP, Mainsail,
      first calibration, first print.
- [ ] **Q-014** Section 04, the complete NebulaScreen guide - 49 panels, task pages plus a
      full screen reference.
- [ ] **Q-015** Section 05, Calibration - every workflow, what it changes, how to read the
      result, verified against the calibration extensions.
- [ ] **Q-016** Sections 06 to 09 - everyday printing, advanced features, updates and
      maintenance, troubleshooting.

## P2 - Screenshots

- [x] **Q-020** **Solved.** Simulator builds, and the app has a built-in screenshot tour
      (`GUPPY_SIM_SHOTS`). 129 real screenshots at 480x272 from commit `94869f7`, captured
      headless. Reproducible via `tools/capture_screenshots.sh`.
- [x] **Q-023** Moot. The 2026-07-01 images are superseded by captures from the documented
      commit, so they are not used rather than confirmed.
- [ ] **Q-024** Embed the captures. Only **7 of 129** are in pages. Do this as each page is
      written rather than as a sweep at the end.
- [ ] **Q-025** Capture the panels the tour misses. `boot_logo_panel` and `init_panel` need
      real hardware; the rest are reachable with existing `sim_*` hooks. **Priority:
      `storage_panel`** - it has a brand-new user-facing button (**Free up space**) and no
      picture of it.
- [ ] **Q-026** `screen:updates_panel` is now `blocked` for screenshots: the capture is
      timing-dependent without a live Moonraker. Only a real printer can supply a trustworthy
      image of that page.
- [ ] **Q-021** Capture the install and first-setup screens first - the highest-impact
      images in the manual.
- [ ] **Q-022** Capture the remaining panels, then annotate the ones used in procedures.

## P1 - Phase 3 is now the priority

The end-user manual is complete; the developer wikis are untouched and hold most of the
inventory. Start with the extensions, because that is where verification is cheapest and
strongest: the suite already passes and 21 modules are already test-verified.

## P2 - Phase 3, developer wikis, one repository at a time

- [~] **Q-030** `NebulaOS-klipper-extensions` - generated reference done (PR #3 on that
      repo): 49 commands, 155 options, README. All 193 items are **draft**, not documented:
      the tables lack the per-item detail mission 6.5 and 6.6 require.
- [~] **Q-036** Raise the extensions reference to the mission's bar.
      **Commands done:** `COMMANDS-DETAIL.md` gives handler, help text, parameters with types
      / defaults / valid ranges, errors raised, side effects and an example invocation for all
      49. The 41 user-facing ones are now `documented`, each naming the residual gap -
      expected output, preconditions beyond the handler's guards, and safety warnings, none of
      which the source contains.
      **Configuration still draft.** `CONFIG.md` now carries each section's module-header
      purpose and the verified fact that every option needs a Klipper restart (all reads
      happen at load time; none are re-read at runtime). But the **per-option** purpose,
      runtime behaviour, dependencies and example that 6.6 asks for are not written, and those
      *can* be written by reading each of the 18 modules.
      **139 of 155 now carry a per-option purpose** - 109 written by reading the module, the
      rest quoted from the author's comment above the option - and only those are promoted.
      **16 remain draft** with a dash, which is the honest answer where no reading has been
      done. Remaining: scattered options in `autotune_tmc`, `bl24c16f`, `virtual_pins` and
      `nebulaos_probe_pair`.
      Seven options are now marked **accepted but not acted on**; see `CONFIG.md`.
- [ ] **Q-031** `NebulaOS-nebulascreen` - LVGL architecture, the panel system, Moonraker
      integration, simulator, build and testing. Reuse the existing developer pages.
- [~] **Q-032** `NebulaOS-firmware` - API, boot services and now an **architecture guide**
      (PR #5): slots and the marker, boot order, why there is no automatic rollback to stock,
      the two-way bounded image trial, recovery by severity, the build pipeline in order.
      Still to write: the 56 runtime helpers individually, per-service failure behaviour,
      Buildroot internals, the filesystem layout, and what each build script does inside.
- [ ] **Q-037** Raise the firmware API reference to mission 6.7: response examples, verified
      against `nebulaos_osconfig/` and the fixtures in `tests/nebulaos-osconfig-tests.py`.
      Do not take them from the component source - it does not contain them.
- [~] **Q-033** `NebulaOS-klipper-mcu` - the on-printer lifecycle written (PR #1 on that repo):
      identity classification, automatic restore with its bounds, the `UNKNOWN_APPLICATION`
      branch, user install from the screen, board parameters, and the repository's own
      qualification status quoted rather than paraphrased. Its existing docs already covered
      building, the Creality header, the patch queue, reproducibility and the toolchain and
      were left alone. Still to write: the patch series file by file, flash layout detail,
      validation tooling.
- [~] **Q-034** `NebulaOS-kernel` - written (PR #2 on that repo): branch layout with `main` as
      the pristine vendor baseline, the three layers on `openke`, the five vendor board-file
      fixes, the eight NebulaOS changes with their subsystems, how three of them serve
      components above the kernel, and the build-applies-nothing answer. Still to write:
      device-tree detail, PREEMPT_RT behaviour, the vendor SDK, U-Boot.
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
- [x] **Q-051** Done 2026-10-31. 29 of 31 suites, **899 tests, all passing**, at `8e3447a`.
      `verify_test` now `verified` on 21 extension modules with per-file citations. The two
      remaining suites need the pinned Klipper composed in; 9 modules have no test at all and
      honestly stay `unknown`.
- [ ] **Q-052** Run the two Klipper-dependent suites the way `scripts/ci-tests.sh` does, by
      composing `extras/` into a scratch copy of the pinned Klipper (`58bd67d`). That would
      finish test verification for `nebulaos_compat` and `nebulaos_temperature_mcu`.

## From the foreground session

- [x] **Q-059** Tim's two decisions of 2026-11-01 - install-route framing, and free rein to
      restructure. Applied; see `DECISIONS.md` D-009 and D-010.
- [~] **Q-060** **Re-verify against tonight's code changes.** Extensions part **done**;
      the rest waits for pushed SHAs.
      - [x] Power-loss resume fix, extensions `a2e7634` - **pushed and verified.** Worktree
        moved to it, full suite re-run (29/29 suites pass; the PLR suite is now 169 tests),
        all 21 test-verified modules re-pointed from `8e3447a` to `a2e7634`, and
        `wiki/Power-Loss-Recovery.md` written from the new behaviour.
      - [x] Screen `4883008` + `3194104` - **pushed and verified.** Rebuilt and re-captured
        at `3194104`; 128/129 images byte-identical, the one difference proved to be
        non-determinism rather than a code change (see `SCREENSHOTS.md`). All screenshot
        citations re-pointed to `3194104`.
      - [x] Storage **Free up space** documented in `wiki/Resetting.md` and
        `wiki/Updating-NebulaOS.md`, kept **separate** from **Clean up Creality files** as
        instructed - they do different jobs and the separation is what keeps going back to
        stock working.
      - [x] Firmware `c377230` - **pushed and documented.** Root password now `NebulaOS`
        (`936c3d6`), unique per-printer hostname `nebulaos-<last 4 hex of stable Wi-Fi MAC>`
        (`ed24767`), Free up space endpoints (`47e07af`), pins advanced to extensions
        `a2e7634` + screen `3194104`. `Opening-Mainsail` and `Installing-NebulaOS` updated.
      **Q-060 is closed.** The pins now match the tips exactly - no gap between documented and
      shipped behaviour for the extensions or the screen.
      - Storage **Free up space** button, NebulaOS leftovers only. **Clean up Creality files**
        stays separate - do not merge the two in the docs; they do different things.
      - Default root password `NebulaOS` (was `openke`), unique default hostname
        `nebulaos-<last 4 MAC hex>`, clearer SSH prompt - affects any page mentioning SSH or
        the printer's name, and `Opening-Mainsail` in particular.
      Re-run `tools/capture_screenshots.sh` once the screen tip moves.
- [ ] **Q-061** Restructure under D-010: retitle the component `Installation.md` to say what
      it is, and reconcile the screen wiki's navigation with the central manual.
- [x] **Q-062** **Statistics for 1.0.0** (Tim via the main session, 2026-11-02). Done:
      `wiki/Screen-Reference.md` gained a full **Statistics panel** section with the real
      capture `20a-statistics.png`, and the page is linked from `Home`, `Printing` and
      `Resetting`. Storage text now says the Creality cleanup keeps the statistics files.
      Evidence: screen `36490ed` (`statistics_panel.cpp`, `stats_text`), firmware `70ad0b0`
      (`nebulaos_osconfig/stats.py`, `combine_stats`, `cleanup.STATISTICS_KEEP`).
- [x] **Q-063** Re-point the release references from firmware `211d804` to the 1.0.0
      release candidate `70ad0b0`: 44 inventory items, the `Recovery` trial-bounds citation
      (constants re-read at `70ad0b0` and unchanged) and the readiness report.
- [x] **Q-064** **Timelapse page written** (2026-11-03). `wiki/Timelapse.md`: switching it on in
      Mainsail, the park-head trade-off, the NebulaOS layer watcher that removes the slicer
      change, what a power loss does, storage, and the cancel-does-not-render trap. Linked from
      the sidebar, `Home`, `Camera`, `Printing` and `Power-Loss-Recovery`. Evidence: firmware
      `70ad0b0` (`camera.cfg`, `print.cfg`, `nebulaos-seed-timelapse`, `nebulaos.conf`,
      `machine.cfg`) and upstream `moonraker-timelapse` at the pinned `c7fff11`. **No screenshot
      yet** - the page is Mainsail's, which this agent cannot capture. Original entry:
      **Timelapse was not in the user manual at all** - found while checking the
      1.0.0 extensions pin. It ships (manifest pins `moonraker-timelapse`, seeded by
      `S57nebulaos-timelapse-seed`, macros in `camera.cfg`/`print.cfg`), the mission lists it
      as a manual section, and 1.0.0 adds frame-keeping across a power loss. The power-loss
      side is now documented in `Power-Loss-Recovery`; a proper `Timelapse` page is the next
      manual batch.
- [ ] **Q-065** Re-verify the extensions developer reference against the 1.0.0 pin.
      189 inventory items are still labelled *0.9.0 (manifest pins a2e7634)*, but 1.0.0 ships
      `f498796`, and `a2e7634..f498796` is **not** cosmetic: `nebulaos_power_loss_recovery.py`
      (+155 lines) and `nozzle_clear.py` changed. Developer docs only - not release-blocking,
      and not startable until the component worktrees come back.

## Done

- **Q-001** G-code command constants resolved (2026-10-31).
- **Q-002** Configuration key discovery (2026-10-31), after correcting an over-collecting
  first attempt.
- **Q-003** Moonraker API discovery (2026-10-31), after fixing an extractor that dropped an
  endpoint whose path contains a digit. Klipper status objects remain as a follow-up.
- **Q-020** Screenshot capture solved (2026-11-01): 129 images from the documented commit,
  via the app's own headless tour.
- **Q-051** Extensions test suite run and cited (2026-10-31): 899 tests passing, 21 modules
  promoted to test-verified. Two detection bugs of my own caught on the way - see
  `VERIFICATION.md`.
- **Q-006** Reuse audit of the existing wiki (2026-10-31). The existing wiki is good and is
  being reused rather than replaced; Phase 2 is more relocation than authoring, except for
  sections 01, 03 and 06.
- **Q-004, Q-005** Build pipeline, developer tooling and runtime helpers (2026-10-31).
  Counts verified independently. Five system-named overlay shims were nearly filtered out
  as vendor noise and turned out to be NebulaOS-authored - see `STATUS.md`.
