# The NebulaOS manual

**NebulaOS is open firmware for the Creality Ender-3 V3 KE: guided printing on its own touchscreen
app, with full Klipper control underneath.** This manual describes NebulaOS 1.0.1.

## New here? Start printing

Seven short steps, in order. Each one ends with a link to the next.

1. [What is NebulaOS](What-NebulaOS-Is) - what it replaces, safety, and what you need
2. [Install NebulaOS](Installing-NebulaOS) - from stock Creality firmware or from OpenKE
3. [First start](First-Time-Setup) - Wi-Fi, the printer's address, Mainsail
4. [First calibration](First-Calibration) - one guided run, about 7 minutes
5. [Set up your slicer](Slicer-Setup) - two lines of start and end G-code, **do not skip this**
6. [Your first print](Printing) - load filament, print a test, tune the first layer live
7. [Keeping NebulaOS updated](Updating-NebulaOS)

**Install → Connect → Calibrate → Slice → Print.**

## Improve my prints

- [Improve your prints](Improve-Your-Prints) - start from what you see: first layer too high or
  too low, poor adhesion, an uneven bed, a Z offset that drifts
- [Calibration explained](Calibration-Explained) - bed tramming, Z offset and bed mesh, load cell,
  axis twist, PID, input shaper, E-steps, skew, TMC autotune
- [Print setup NebulaOS adds](Adaptive-Print-Setup) - adaptive mesh, purge line, bed soak,
  firmware retraction

## Customize NebulaOS

- [SSH, SFTP and security](SSH-And-SFTP) - logging in, the root password
- [Mainsail and Moonraker](Mainsail-And-Moonraker) - the web interface, slicer upload, apps,
  home automation
- [Custom macros and integrations](Macros-And-Integrations) - your own macros, Spoolman,
  `RUN_SHELL_COMMAND`
- [Files, configuration and backups](Files-And-Configuration) - `printer.cfg`, what an update
  keeps, how to back up
- [How NebulaOS works](Under-the-Hood)

---

**Supported: the Ender-3 V3 KE only** - not the Ender-3 V3, V3 SE or V3 Plus.

- **[Using NebulaScreen](Screen-Reference)** - every tab, button and setting on the printer's
  screen, in the screen's own order.
- **[Help and recovery](Troubleshooting)** - start from the symptom.
  [Going back to stock](Going-Back), [Resetting](Resetting), [Recovery](Recovery).

NebulaOS is not Creality's software and is not supported by Creality. If a page tells you to do
something and you cannot find the button it names, that is a bug in this manual - please report
it: [github.com/NebulaOS-KE/NebulaOS/issues](https://github.com/NebulaOS-KE/NebulaOS/issues).
