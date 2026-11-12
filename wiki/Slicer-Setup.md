# 5. Set up your slicer

## What this guide will help you do

Tell your slicer how to start and end a print on NebulaOS. You do this **once**, before your
first print. Without it, the printer may skip its own preparation - the bed mesh, the purge
line, timelapse - or heat up twice.

## The quick way: our OrcaSlicer profiles

Using OrcaSlicer? Import our ready-made profiles and everything on this page is done for you:
[Quickstart: OrcaSlicer profiles](Quickstart-OrcaSlicer). The rest of this page is for other
slicers and for your own profiles.

## By hand: simple or advanced

You need a slicer that lets you edit its start and end G-code; the examples use **OrcaSlicer**,
which most KE owners use. Start from the printer profile your slicer offers for the Ender-3 V3 KE,
if it has one, and a calibrated printer - [4. First calibration](First-Calibration).

There are two ways to set it up. They differ only in **who retracts** - who pulls the filament back
a little before the nozzle travels, so it does not string or ooze:

| | **Simple** (start here) | **Advanced: firmware retraction** |
|---|---|---|
| Who retracts | The slicer, written into the G-code | The printer (`G10`/`G11`), with your slicer's values |
| **Use firmware retraction** in the slicer | Off | On |
| Start G-code | A short line | A long line that also passes the retraction |
| Change retraction while printing | No: change it in the slicer and slice again | Yes: **Tune → Retraction** on the screen |

Not sure? Take **simple**. The OrcaSlicer profiles come in the same two versions.

## Simple

1. Open the printer settings (the edit icon next to the printer name), tab **Machine G-code**.
2. Replace everything in **Machine start G-code** with:

   ```gcode
   START_PRINT BED_TEMP=[bed_temperature_initial_layer_single] EXTRUDER_TEMP=[nozzle_temperature_initial_layer]
   ```

3. Replace everything in **Machine end G-code** with:

   ```gcode
   END_PRINT
   ```

4. Tab **Extruder**: leave **Use firmware retraction** off. Set the retraction as you would on any
   printer, here or per material in the filament profile.
5. In the print settings, tab **Others**, tick **Label objects**.
6. Save the printer profile.

## Advanced: firmware retraction

1. Open the printer settings, tab **Machine G-code**.
2. Replace everything in **Machine start G-code** with this, all on one line:

   ```gcode
   START_PRINT BED_TEMP=[bed_temperature_initial_layer_single] EXTRUDER_TEMP=[nozzle_temperature_initial_layer] RETRACT_LENGTH={if is_nil(filament_retraction_length[0])}{retraction_length[0]}{else}{filament_retraction_length[0]}{endif} RETRACT_SPEED={if is_nil(filament_retraction_speed[0])}{retraction_speed[0]}{else}{filament_retraction_speed[0]}{endif} UNRETRACT_SPEED={if is_nil(filament_deretraction_speed[0])}{deretraction_speed[0]}{else}{filament_deretraction_speed[0]}{endif} UNRETRACT_EXTRA_LENGTH={if is_nil(filament_retract_restart_extra[0])}{retract_restart_extra[0]}{else}{filament_retract_restart_extra[0]}{endif}
   ```

3. Replace everything in **Machine end G-code** with `END_PRINT`.
4. Tab **Extruder**: tick **Use firmware retraction**. OrcaSlicer then greys out the retraction
   fields there; their values stay as the fallback.
5. Optional: give a material its own retraction in its **filament** profile: **Setting
   Overrides**, tick and set the retraction length, retraction speed, deretraction speed and
   extra length on restart.
6. In the print settings, tab **Others**, tick **Label objects**.
7. Save the printer profile.

**Why the line is so long:** it passes the filament's own retraction values when it has them, and
the printer profile's otherwise. OrcaSlicer's short placeholders do not pick up filament overrides.

The slicer then writes short `G10`/`G11` commands instead of its own retraction moves, and the
printer retracts with the values `START_PRINT` received. Changes you make on the screen during a
print last until the next print, which starts from the slicer's values again. Wipe is not available
with firmware retraction in OrcaSlicer.

**If the start line has no `RETRACT_...` values** (for example the simple line with firmware
retraction ticked), firmware retraction still works, but your slicer's values are ignored. The
printer then uses its current values: after a restart 0.6 mm at 35 mm/s, unretract at 30 mm/s,
otherwise whatever was last set on the screen. Use the long line to avoid this.

## Good to know, for both

- **The words in brackets** are OrcaSlicer's own placeholders. When it slices, it replaces them
  with your filament's first-layer temperatures (and, in the long line, its retraction values).
  Copy a line exactly as it is, all on one line.
- **The names matter.** The macros are called `START_PRINT` and `END_PRINT`. NebulaOS has no
  `PRINT_START` or `PRINT_END`, so a profile written for another Klipper printer that uses those
  names will not run NebulaOS's preparation.
- **Leave out** the heating, homing, mesh and purge lines a stock Creality profile may have had,
  and the `M220 S100` / `M221 S100` lines many profiles start with: `START_PRINT` does all of that
  itself, in the right order, and sets speed and flow back to 100 %.
- **Label objects** lets NebulaOS probe only the area the print covers, purge next to it, and
  [cancel one object](Screen-Home#exclude-object-screen) during a print.
- **During a simple print, Tune → Retraction does not open.** The screen says *"This print isn't
  sliced for firmware retraction. These settings won't apply."* It knows from the file: a file
  without `G10`/`G11` was sliced without firmware retraction.

## What START_PRINT does for you

In order: checks that filament is loaded, starts heating, homes, waits for the bed, probes a
fresh bed mesh of the print area, parks next to the print, waits for the nozzle and draws a
purge line. It also starts the [timelapse](Timelapse) watcher, if timelapse is on. The details,
and what each step costs in time, are in [Print setup NebulaOS adds](Adaptive-Print-Setup).

`END_PRINT` turns the heaters off, retracts, and parks the nozzle at the back with the bed
forward, so the print is presented to you.

## Sending files from the slicer

Moonraker, the printer's API, accepts uploads directly from the slicer, so you do not have to copy
files by hand. In your slicer's printer connection settings, choose the host type
**Octo/Klipper** (OrcaSlicer; PrusaSlicer and Cura have an OctoPrint option) and enter the
printer's address, for example `http://192.168.1.42` or `http://nebulaos-4f2a.local`. NebulaOS
answers OctoPrint-style uploads on that plain address. Other ways to connect are in
[Mainsail and Moonraker](Mainsail-And-Moonraker).

You can also drag the file into Mainsail's file list, or use a USB stick - see
[6. Your first print](Printing).

## Optional extras

You can add these to the end of either start line:

| Add | What it does |
|---|---|
| `BED_SOAK=1` | Waits for the bed to settle before measuring it. Useful for ABS and ASA. `BED_SOAK=0` never waits. |
| `BED_MESH_ADAPTIVE=0` | Probes the whole bed instead of just the print area |
| `BED_MESH_PROFILE=<name>` | Loads a saved mesh instead of probing a new one |

To soak the bed only for ABS and ASA, let OrcaSlicer decide - add this, with a space before it,
to the end of either line:

```gcode
{if filament_type[0]=="ABS" or filament_type[0]=="ASA"}BED_SOAK=1{endif}
```

If you leave the temperatures out, `START_PRINT` uses 65 °C for the bed and 230 °C for the
nozzle. Always pass both from the slicer.

## Expected result

When you start a print, the screen shows the start steps - preparing, heating the bed, the mesh,
heating the nozzle, the purge - and then the first layer begins.

## Troubleshooting

| What happens | What to do |
|---|---|
| The print starts without a mesh or a purge line | The start G-code does not call `START_PRINT`. Check the spelling and that nothing replaces it. |
| A full-bed mesh every time, and the purge line at the front-left corner | **Label objects** is off. Turn it on and slice again. |
| The fresh mesh is replaced by an old one | Remove any `BED_MESH_PROFILE LOAD=...` line after `START_PRINT`. |
| No timelapse video, and timelapse is on | The print has to start with `START_PRINT`. See [Timelapse](Timelapse). |
| The screen says the print isn't sliced for firmware retraction | You use the simple setup, so the slicer retracts: change retraction in the slicer. For live tuning, switch to the advanced setup. |
| Firmware retraction is on but ignores the slicer's values | The start line is the short one. Use the long line from the advanced setup. |

*From `START_PRINT`, `_START_PRINT_BED_MESH` and `END_PRINT` in `etc/nebulaos/klipper/print.cfg`,
`[firmware_retraction]` in `machine.cfg` and the upload route from
`etc/nebulaos/moonraker/nebulaos.conf:16-21`, firmware `3bdf3ff`; the screen's retraction check
from NebulaScreen `src/printertune_panel.cpp` and `src/utils.cpp`, `fd47cb6`. The OrcaSlicer field
names and placeholders are OrcaSlicer's, not NebulaOS's.*

## Next step

[6. Your first print](Printing) - load filament, print a small test, and tune the first layer.

Need help? [Troubleshooting](Troubleshooting) · How this works: [Print setup NebulaOS adds](Adaptive-Print-Setup)
