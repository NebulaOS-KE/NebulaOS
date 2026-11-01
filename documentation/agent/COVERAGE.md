# NebulaOS documentation coverage dashboard

Generated 2026-11-01 by `documentation/agent/tools/render_dashboard.py` from `documentation/agent/coverage.jsonl`.

**Read this first.** Coverage is relative to the *discovered* inventory, not to some imagined complete list of everything NebulaOS does. Each entry records the exact source commit it was discovered at. A rise in the total item count is normal and healthy: it means discovery found more real functionality, not that documentation regressed.

Verification is reported in four separate columns because they prove different things. *Code verified* means the implementation was read. *Test verified* means a test in the repository covers it. *Hardware verified* means it was observed on a real printer - this agent has no printer access, so that column is expected to stay low and is honest about it. *Screenshot* tracks real captured images only.

## Overall

| Measure | Items | Share |
|---|---|---|
| Discovered documentation items | 546 | 100% |
| Documented (page exists and covers the item) | 78 | 14% |
| Draft | 195 | 35% |
| Missing | 273 | 50% |
| Blocked | 223 | 40% |

## Verification (counted separately, never combined)

| Kind | Verified | Partial | Unknown | Blocked | N/A |
|---|---|---|---|---|---|
| Code verified | 273 | 1 | 272 | 0 | 0 |
| Test verified | 28 | 0 | 518 | 0 | 0 |
| Hardware verified | 0 | 0 | 0 | 2 | 544 |

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
| NebulaOS-firmware | 195 | 1 | 1 | 193 | 2 | 0% |
| NebulaOS-kernel | 1 | 0 | 0 | 1 | 0 | 0% |
| NebulaOS-klipper-extensions | 232 | 17 | 194 | 21 | 211 | 7% |
| NebulaOS-klipper-mcu | 1 | 0 | 0 | 1 | 0 | 0% |
| NebulaOS-nebulascreen | 104 | 50 | 0 | 54 | 50 | 48% |
| lv_drivers | 1 | 0 | 0 | 1 | 0 | 0% |
| nebulaos-packages | 1 | 0 | 0 | 1 | 0 | 0% |

## By category

| Category | Items | Documented | Draft | Missing | Documented % |
|---|---|---|---|---|---|
| api | 59 | 0 | 1 | 58 | 0% |
| build-command | 14 | 0 | 0 | 14 | 0% |
| command | 50 | 8 | 41 | 1 | 16% |
| config-option | 172 | 0 | 152 | 20 | 0% |
| developer-tool | 11 | 0 | 0 | 11 | 0% |
| existing-page | 34 | 16 | 0 | 18 | 47% |
| extension | 30 | 9 | 0 | 21 | 30% |
| os-helper | 17 | 0 | 0 | 17 | 0% |
| repo-overview | 8 | 0 | 1 | 7 | 0% |
| runtime-helper | 57 | 1 | 0 | 56 | 1% |
| screen | 49 | 34 | 0 | 15 | 69% |
| service | 35 | 0 | 0 | 35 | 0% |
| user-manual-section | 10 | 10 | 0 | 0 | 100% |

## Source revisions this inventory was discovered at

| Repository | Branch | Commit | Items |
|---|---|---|---|
| NebulaOS | main | cf74ebd4917f | 11 |
| NebulaOS-firmware | main | a2e763460bb0 | 1 |
| NebulaOS-firmware | main | c3772307ab8e | 194 |
| NebulaOS-kernel | openke | d86790d2e231 | 1 |
| NebulaOS-klipper-extensions | main | a2e763460bb0 | 232 |
| NebulaOS-klipper-mcu | main | 33f5d16daccd | 1 |
| NebulaOS-nebulascreen | main | 319410454519 | 104 |
| lv_drivers | master | not cloned l | 1 |
| nebulaos-packages | main | not cloned l | 1 |

## Blocked items

| Item | Repository | Reason |
|---|---|---|
| repo:NebulaOS-klipper-extensions | NebulaOS-klipper-extensions | per-module implementation pages not written yet; reference covers commands and configuration |
| repo:nebulaos-packages | nebulaos-packages | not cloned locally; clone into _worktrees/docs |
| repo:lv_drivers | lv_drivers | not cloned locally; clone into _worktrees/docs |
| manual:02-installation | NebulaOS | verify_hardware outstanding: the stock-touchscreen route has not been observed on a printer (D-009: user pages document it as the normal route; record kept in VERIFICATION.md) |
| manual:04-nebulascreen | NebulaOS | 8 screens in the reference have no current capture; 21 panels are indexed but not individually described |
| screen:boot_logo_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:calibration_menu_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:camera_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:connections_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:exclude_object_panel | NebulaOS-nebulascreen | not covered by the simulator screenshot tour; needs an extra tour step or a manual capture |
| screen:filament_runout_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:guided_calibration_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:hostname_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:image_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:init_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:network_detail_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:pid_calibration_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:print_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:printer_select_panel | NebulaOS-nebulascreen | not covered by the simulator screenshot tour; needs an extra tour step or a manual capture |
| screen:prompt_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:report_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:reset_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:spoolman_panel | NebulaOS-nebulascreen | not covered by the simulator screenshot tour; needs an extra tour step or a manual capture |
| screen:spoolman_server_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:static_ip_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| screen:storage_panel | NebulaOS-nebulascreen | the new Free up space button (screen 3194104) is not in the screenshot tour; needs an extra tour step or a real printer |
| screen:tmc_tune_panel | NebulaOS-nebulascreen | not covered by the simulator screenshot tour; needs an extra tour step or a manual capture |
| screen:updates_panel | NebulaOS-nebulascreen | capture is timing-dependent without a live Moonraker: the busy/idle state varies between runs, so a published image would contradict the page. Needs a real printer. |
| screen:wifi_panel | NebulaOS-nebulascreen | indexed in wiki/Screen-Reference.md with a pointer, but no description of its own yet |
| gcode:AUTOTUNE_TMC | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_DEBUG_READ | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_DEBUG_WRITE_BYTE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_DEBUG_WRITE_FLOAT | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_DEBUG_WRITE_INT | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_IS_FIRST_USED | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_POS | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_PRINTER_INFO | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_READ | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_WRITE_BYTE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_WRITE_FLOAT | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:EEPROM_WRITE_INT | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_BED_TRAM | NebulaOS-firmware | defined as a gcode_macro in the firmware's calibration.cfg, not registered by the extensions; verify the macro file before documenting |
| gcode:NEBULAOS_CALIBRATION_RECORD | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_CALIBRATION_STATUS | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_LOAD_CELL_AUTO_CHECK | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_LOAD_CELL_MODE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_LOAD_CELL_READ | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_RAW_CONTACT_COMPARE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_RAW_CONTACT_DIAGNOSTIC | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_RAW_CONTACT_REFERENCE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_TMC_AUTOTUNE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:NEBULAOS_Z_ADJUST | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:RUN_SHELL_COMMAND | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:SAVE_INPUT_SHAPER | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:SET_PIN | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:SET_VIRTUAL_PIN | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:TMCSTATUS | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:Z_OFFSET_APPLY_PROBE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_AUTO_CALIBRATE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_BED_TRAM | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_BED_TRAM_CANCEL | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_CALIBRATION_CANCEL | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_ESTEPS_CALIBRATE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_ESTEPS_CANCEL | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_ESTEPS_CONFIRM | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_INPUT_SHAPER_CALIBRATE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_INPUT_SHAPER_CANCEL | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_LOAD_CELL_CALIBRATE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_LOAD_CELL_CANCEL | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_NOZZLE_CLEAN | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| gcode:_NEBULAOS_Z_OFFSET_CALIBRATE | NebulaOS-klipper-extensions | reference entry exists (name, module, kind, description, test); mission 6.5 also requires per-command preconditions, example invocation, expected output, errors, side effects and safety warnings |
| config:autotune_tmc:motor | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:tuning_goal | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:extra_hysteresis | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:tbl | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:toff | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:tpfd | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:sgt | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:sg4_thrs | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:semin | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:semax | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:seup | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:sedn | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:seimin | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:voltage | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:overvoltage_vth | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:autotune_tmc:pwm_freq_target | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:calibrate_shaper_config:shaper_type | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:calibrate_shaper_config:shaper_type_x | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:calibrate_shaper_config:shaper_freq_x | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:calibrate_shaper_config:shaper_type_y | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:calibrate_shaper_config:shaper_freq_y | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:gcode_shell_command:command | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:gcode_shell_command:timeout | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:gcode_shell_command:verbose | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:motor_constants:resistance | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:motor_constants:inductance | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:motor_constants:holding_torque | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:motor_constants:steps_per_revolution | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:motor_constants:max_current | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:motor_constants:motor | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:motor_constants:deprecated | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_bed_soak:pin | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_bed_soak:filename | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_bed_tram:tolerance | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_bed_tram:shim_step | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_bed_tram:max_shim | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_bed_tram:max_tries | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_bed_tram:min_improvement | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_bed_tram:samples | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_bed_tram:state_path | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:pwmchip | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:channel | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:songs_file | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:default_song | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:duty | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:click_frequency | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:click_duration_ms | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:click_duty | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:max_beep_ms | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:max_tune_seconds | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:max_tune_seconds_printing | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_beeper:max_queue_seconds | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:down_min_z | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:pro_cnt | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:horizontal_move_z | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:travel_speed | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:probe_lift_speed | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:max_offset_correction_mm | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:reference_x | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:reference_y | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:established_contact_margin_mm | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:bootstrap_contact_envelope_mm | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:max_abs_fit_delta | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:min_accepted_samples | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:max_repeatability_range | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:max_repeatability_stddev | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:pid_bed_target | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:pid_hotend_target | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:z_offset_reference_temp | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:thermal_soak_seconds | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:bed_mesh_profile | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:journal_path | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:history_path | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:esteps_temp | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:esteps_commanded_length_mm | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:esteps_extrude_speed_mm_s | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:esteps_max_correction_ratio | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:input_shaper_journal_path | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:shaper_freq_end | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:shaper_accel_per_hz | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:shaper_graph_timeout | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:shaper_graph_dir | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_calibration:shaper_graph_config_dir | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_compat:manifest | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_compat:klipper_path | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_load_cell_calibration:min_grams | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_load_cell_calibration:max_grams | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_load_cell_calibration:default_grams | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_load_cell_calibration:window_seconds | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_load_cell_calibration:stable_drift_counts_per_s | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_load_cell_calibration:replace_tolerance_percent | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_load_cell_calibration:zero_tolerance_grams | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_load_cell_calibration:previous_change_percent | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_load_cell_calibration:empty_shift_grams | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_memory:child_oom_score_adj | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_memory:mlock | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_power_loss_recovery:eeprom_path | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_power_loss_recovery:sidecar_dir | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_power_loss_recovery:checkpoint_interval | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_power_loss_recovery:poll_interval | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_power_loss_recovery:min_z_for_start | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_power_loss_recovery:physical_resume | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_power_loss_recovery:resume_z_lift | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_power_loss_recovery:prime_length | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_version:version_file | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_version:generation_file | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_adjust:filename | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_adjust:max_adjust | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:sensor_type | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:contact_speed | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:retract_dist | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:retract_speed | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:trigger_force | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:force_safety_limit | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:tare_time | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:contact_detection_mode | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:raw_health_time | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:raw_settle_time | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:raw_contact_profile_id | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:raw_reference_counts | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:auto_check_time | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nebulaos_z_offset_probe:load_cell_mode_file | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:clr_noz_start_x | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:clr_noz_start_y | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:clr_noz_len_x | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:clr_noz_len_y | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:pa_clr_dis_mm_x | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:pa_clr_dis_mm_y | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:pa_clr_down_mm | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:clr_xy_spd | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:rdy_xy_spd | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:bed_max_err | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:g29_down_min_z | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:vs_start_z_pos | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:nozzle_clear:pr_clear_probe_cnt | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:tmcstatus:enabled | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:hot_start_temp | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:hot_rub_temp | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:hot_end_temp | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:bed_add_temp | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:z_offset_down_min_z | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:vs_start_z_pos | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:tri_min_hold | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:tri_max_hold | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:speed | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:tri_expand_mm | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:pr_probe_cnt | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:max_offset_correction_mm | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:type_nozz | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:pumpback_mm | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:persist_offset | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |
| config:z_compensate:save_config_command | NebulaOS-klipper-extensions | reference entry exists (name, section, type, default, constraints); mission 6.6 also requires purpose, runtime behaviour, whether a restart is needed, validation rules and an example |

