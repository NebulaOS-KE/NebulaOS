# Custom macros and integrations

NebulaOS runs standard Klipper, so a macro or an integration written for Klipper works here as it
does anywhere else. This page lists what NebulaOS adds and where your own things go.

## Your own macros

Put them in `config/macros/`, one or more `.cfg` files. `printer.cfg` loads `macros/*.cfg`
automatically, after NebulaOS's own files. Then restart Klipper (**Settings → Printer → Restart
Klipper**). Edit them in Mainsail (**Machine** → `config/macros/`) or over SFTP
([SSH, SFTP and security](SSH-And-SFTP)).

```ini
[gcode_macro PREHEAT_PLA]
description: Preheat for PLA
gcode:
    M140 S60
    M104 S200
```

Your macros appear on the screen's **Macros** tab, where a star makes them favourites
([Macros and Console](Screen-Macros-Console)), and in Mainsail.

**Do not reuse a NebulaOS macro's name** (`START_PRINT`, `END_PRINT`, `PAUSE`, `RESUME`,
`CANCEL_PRINT`, `M600`, `M109`, `M190`, ...): Klipper would merge or replace it, and the print start
would no longer do what the manual describes. To change how one behaves, override its variables -
see [Files, configuration and backups](Files-And-Configuration#changing-a-nebulaos-setting).

## NebulaOS's own macros

All of these are in `config/nebulaos/` (read-only for you) and can be called from Mainsail's
console, the screen's Console tab, or your own macros:

| Macro | What it does |
|---|---|
| `START_PRINT`, `END_PRINT` | Prepare and finish a print - [Print setup NebulaOS adds](Adaptive-Print-Setup) |
| `PAUSE`, `RESUME`, `CANCEL_PRINT`, `M600` | Pause, resume, cancel, filament change |
| `LOAD_FILAMENT`, `UNLOAD_FILAMENT` | The screen's Load and Unload |
| `NEBULAOS_AUTO_CALIBRATE` | Auto Calibration: nozzle clean, Z offset, bed mesh |
| `NEBULAOS_BED_TRAM` | Guided bed tramming |
| `NEBULAOS_LOAD_CELL_CALIBRATE` | Load cell calibration with a 1.5 L water bottle |
| `LOAD_CELL_AUTOMATIC`, `LOAD_CELL_MANUAL` | Choose the load cell mode |
| `NEBULAOS_Z_OFFSET_CALIBRATE` | Load-cell Z offset only |
| `NEBULAOS_INPUT_SHAPER_CALIBRATE` | Guided input shaper (`GRAPHS=1` draws the graphs) |
| `NEBULAOS_ESTEPS_CALIBRATE` | Guided E-steps |
| `NEBULAOS_CALIBRATION_CANCEL` | Cancel a running calibration at the next stage boundary |
| `NEBULAOS_NOZZLE_CLEAN` | The nozzle clean cycle |
| `AXIS_TWIST_X` | Axis twist calibration (upstream `AXIS_TWIST_COMPENSATION_CALIBRATE`) |
| `PID_BED`, `PID_HOTEND` | PID tuning at 65 °C / 230 °C (`TARGET=` to change) |
| `NEBULAOS_RESUME_POWER_LOSS`, `NEBULAOS_CLEAR_POWER_LOSS_RECOVERY` | [Power-loss recovery](Power-Loss-Recovery) |
| `M300`, `BEEP`, `PLAY_TUNE` | The buzzer - [Beeps and songs](Beeps-And-Songs) |
| `SET_CAMERA_QUALITY_LOW` / `_MED` / `_HIGH` | Webcam resolution: 640x480, 1280x720, 1920x1080 at 30 fps |
| `NEBULA_CAMERA_NIGHT_MODE`, `NEBULA_CAMERA_ANTI_FLICKER`, `NEBULA_CAMERA_RESTART`, `NEBULA_CAMERA_DEFAULTS` | The Nebula Camera's settings - [Camera](Camera) |

The descriptions are the macros' own. The full reference of the extension modules and their
commands is in the
[extensions repository](https://github.com/NebulaOS-KE/NebulaOS-klipper-extensions).

## Running shell commands: `RUN_SHELL_COMMAND`

NebulaOS ships Klipper's `gcode_shell_command` module, so a macro can run a program on the printer.
Define the command in `printer.cfg` or a file in `macros/`:

```ini
[gcode_shell_command hello]
command: echo hello from the printer
timeout: 10

[gcode_macro SAY_HELLO]
gcode:
    RUN_SHELL_COMMAND CMD=hello
```

NebulaOS uses the same mechanism for its camera macros (`[gcode_shell_command set_camera_quality]`
and `[gcode_shell_command nebula_camera]` in `camera.cfg`). The command runs as root - only put
commands there that you would type in the shell yourself.

## Spoolman

[Spoolman](https://github.com/Donkie/Spoolman) keeps track of your spools. It runs on another
computer on your network (it is not installed on the printer). On the screen, **Settings →
Connections → Spoolman**: type the server's address and port (Spoolman's default is 7912) and tap
**Use**. NebulaOS writes `[spoolman] server: http://<address>:<port>` into your `moonraker.conf` and
restarts Moonraker; the screen reconnects after a few seconds. Then **Home → Extrude → Spoolman**
shows the spool list, a print or a Load asks *"Use this filament?"* for the active spool, and its
filament use is deducted as you print. Details: [Settings → Connections](Screen-Connections) and
[Home and printing](Screen-Home#spoolman-panel).

## Mainsail, slicers, apps and home automation

Through Moonraker - addresses, ports and who may connect: [Mainsail and Moonraker](Mainsail-And-Moonraker).

*Macro names and descriptions from `etc/nebulaos/klipper/*.cfg` (`camera.cfg:11-57`,
`calibration.cfg`, `print.cfg`, `filament.cfg`, `beeper.cfg`), firmware `dc868e3`; `printer.cfg`'s
includes from `etc/init.d/S04nebulaos-migrate:1227-1238`; `gcode_shell_command.py` in extensions
`f498796`; Spoolman from `usr/lib/nebulaos/python/nebulaos_osconfig/spoolman.py:6-114`.*

## Next

- [Beeps and songs](Beeps-And-Songs)
- [How NebulaOS works](Under-the-Hood)
- Need help? [Troubleshooting](Troubleshooting)
