# Quickstart: OrcaSlicer profiles

The fastest way to print on NebulaOS: import our OrcaSlicer profiles and everything in the slicer
is set up for you - the start and end G-code, retraction, and settings for four materials at four
layer heights.

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

## Simple or advanced?

There are two printer profiles. The filaments and processes are the same for both.

| | **Simple** (start here) | **Advanced: firmware retraction** |
|---|---|---|
| Download | `NebulaOS-Ender3V3KE-OrcaSlicer.orca_printer` | `NebulaOS-Ender3V3KE-OrcaSlicer-firmware-retraction.orca_printer` |
| Printer name in OrcaSlicer | *Creality Ender-3 V3 KE 0.4 nozzle - NebulaOS* | *Creality Ender-3 V3 KE 0.4 nozzle - NebulaOS (firmware retraction)* |
| Who retracts | OrcaSlicer, written into the G-code | The printer (`G10`/`G11`), with each filament's values |
| Wipe | On | Off (OrcaSlicer does not combine wipe with firmware retraction) |
| Change retraction while printing | No: change the filament profile and slice again | Yes: **Tune → Retraction** on the screen |

Not sure? Take **simple**. You can import both and switch printer in OrcaSlicer at any time; what
the two choices mean is explained in
[Set up your slicer](Slicer-Setup#by-hand-simple-or-advanced).

## Steps

1. Download the bundle you chose from the
   [latest release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest).
2. In OrcaSlicer: **File → Import → Import Configs…** and choose that file.
3. Choose the printer (**... - NebulaOS** or **... - NebulaOS (firmware retraction)**), a filament
   ending in **@NebulaOS** (for example *PLA @NebulaOS*) and a process for the same material (for
   example *0.20mm PLA Standard @NebulaOS*).
4. Connect OrcaSlicer to the printer, so you can send prints straight to it: click the connection
   icon next to the printer name, keep the host type **Octo/Klipper** and enter
   `http://` followed by your printer's address, for example `http://192.168.1.42`. The address is
   on the screen under **Settings → Connections**. This is the one thing we cannot set for you.
5. Slice and print. On the first print, watch the first layer and
   [fine-tune it live](Printing).

## What is set up for you

| | |
|---|---|
| Start G-code | One line, `START_PRINT`, with your filament's temperatures (the advanced printer also passes the retraction) - the printer does homing, heating, the bed mesh and the purge line ([details](Slicer-Setup)) |
| End, pause, filament change | `END_PRINT`, `PAUSE`, `M600` |
| Objects | Label objects on, so the printer meshes only where the part goes and you can cancel one object |
| Left to the printer | The machine limits (maximum speed and acceleration), input shaper and square-corner velocity - Klipper keeps its own. Each process still sets its own accelerations per feature, within those limits |
| Not used | Arc fitting (the printer has no arcs) |
| Timelapse | Nothing needed in the slicer |

## The filaments

| | PLA | PETG | PETG-CF | TPU |
|---|---|---|---|---|
| Nozzle, first layer / rest (°C) | 210 / 205 | 240 / 235 | 245 / 240 | 220 / 215 |
| Bed, first layer / rest (°C) | 60 / 55 | 85 / 80 | 85 / 80 | 55 / 50 |
| Max flow (mm³/s) | 15 | 9 | 4.5 | 3 |
| Retraction (mm / retract mm/s / unretract mm/s) | 0.6 / 35 / 35 | 0.8 / 35 / 35 | 1.2 / 40 / 35 | 0.8 / 25 / 25 |
| Retract on layer change | yes | yes | yes | yes |
| Z-hop (mm, slope) | 0.25 | 0.2 | 0 | 0.2 |
| Wipe distance (mm, simple printer) | 0.5 | 0.8 | 0.8 | 0.4 |
| Pressure advance | 0.025 | 0.032 | 0.05 | not set |

A filament without its own retraction values uses the printer profile's: 0.6 mm at 35 mm/s,
unretract at 30 mm/s.

**Wipe (simple printer):** 70 % of each retraction happens before the wipe, the rest while the
nozzle moves off the line, at print speed.

**Pressure advance:** PLA, PETG and PETG-CF set their own value at the start of every print. TPU
sets none, so it prints with whatever value the printer has at that moment: 0.036 after a restart,
otherwise the value the last print set. You can still change it during a print under **Tune**; to
change it for good, change it in the filament profile.

Using another slicer, or your own profiles? [Set up your slicer](Slicer-Setup) shows the lines to
add by hand.

*Profiles in the NebulaOS repository: `slicer/orcaslicer/`.*
