# Quickstart: OrcaSlicer profiles

The fastest way to print on NebulaOS: import our OrcaSlicer profiles and everything in the slicer
is set up for you - the start and end G-code, firmware retraction, and settings for four
materials at four layer heights.

> **A starting point, not a perfect tune.** These are the profiles we print with on our own KE.
> They work well for us, but every printer and every spool is a little different. Use them as a
> good starting point, then calibrate flow and pressure advance for your own filament and adjust
> from there.

## What you need

- **OrcaSlicer 2.5.0 or newer.**
- **Creality's Ender-3 V3 KE preset in OrcaSlicer.** Our profiles build on it. If you have never
  used a KE in OrcaSlicer: open the printer selection, choose **Creality → Ender-3 V3 KE 0.4
  nozzle** once, and close it.
- A printer with NebulaOS, calibrated - [4. First calibration](First-Calibration).

## Steps

1. Download `NebulaOS-Ender3V3KE-OrcaSlicer.orca_printer` from the
   [latest release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest).
2. In OrcaSlicer: **File → Import → Import Configs…** and choose that file.
3. Choose the printer **Creality Ender-3 V3 KE 0.4 nozzle - NebulaOS**, a filament ending in
   **@NebulaOS** (for example *PLA @NebulaOS*) and a process for the same material (for example
   *0.20mm PLA Standard @NebulaOS*).
4. Connect OrcaSlicer to the printer, so you can send prints straight to it: click the connection
   icon next to the printer name, keep the host type **Octo/Klipper** and enter
   `http://` followed by your printer's address, for example `http://192.168.1.42`. The address is
   on the screen under **Settings → Connections**. This is the one thing we cannot set for you.
5. Slice and print. On the first print, watch the first layer and
   [fine-tune it live](Printing).

## What is set up for you

| | |
|---|---|
| Start G-code | One line, `START_PRINT`, with your filament's temperatures and retraction - the printer does homing, heating, the bed mesh and the purge line ([details](Slicer-Setup)) |
| End G-code | `END_PRINT` |
| Retraction | Firmware retraction, with each filament's own values; fine-tune it on the screen under **Tune → Retraction** while printing |
| Objects | Label objects on, so the printer meshes only where the part goes and you can cancel one object |
| Left to the printer | The machine limits (maximum speed and acceleration), input shaper and square-corner velocity - Klipper keeps its own. Each process still sets its own accelerations per feature, within those limits |
| Not used | Arc fitting (the printer has no arcs) and wipe (OrcaSlicer does not combine it with firmware retraction) |

## The filaments

| | PLA | PETG | PETG-CF | TPU |
|---|---|---|---|---|
| Nozzle, first layer / rest (°C) | 210 / 205 | 240 / 235 | 245 / 240 | 220 / 215 |
| Bed, first layer / rest (°C) | 60 / 55 | 85 / 80 | 85 / 80 | 55 / 50 |
| Max flow (mm³/s) | 15 | 9 | 4.5 | 3 |
| Retraction (mm / retract mm/s / unretract mm/s) | 0.6 / 35 / 35 | 0.8 / 35 / 35 | 1.2 / 40 / 35 | 0.8 / 25 / 25 |
| Pressure advance | 0.025 | 0.032 | 0.05 | not set |

**Pressure advance:** PLA, PETG and PETG-CF set their own value at the start of every print. TPU
sets none, so it prints with whatever value the printer has at that moment: 0.036 after a restart,
otherwise the value the last print set. You can still change it during a print under **Tune**; to
change it for good, change it in the filament profile.

Using another slicer, or your own profiles? [Set up your slicer](Slicer-Setup) shows the two lines
to add by hand.

*Profiles in the NebulaOS repository: `slicer/orcaslicer/`.*
