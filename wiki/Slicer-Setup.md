# Setting up your slicer

## What this guide will help you do

Tell your slicer how to start and end a print on NebulaOS. You do this **once**, before your
first print. Without it, the printer may skip its own preparation - the bed mesh, the purge
line, timelapse - or heat up twice.

## What you need

- A slicer. The examples use **OrcaSlicer**, which most KE owners use. Its **Creality Ender-3
  V3 KE** printer profile is a good starting point.
- A calibrated printer - [Calibration guide](Calibration-Guide).

## The two lines

NebulaOS has one macro that prepares a print and one that ends it:

| Slicer field | Put exactly this in it |
|---|---|
| Start G-code | `START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]` |
| End G-code | `END_PRINT` |

The words in square brackets are OrcaSlicer's own placeholders. When it slices, it replaces them
with the nozzle and bed temperatures of your filament's first layer.

**The names matter.** The macros are called `START_PRINT` and `END_PRINT`. NebulaOS has no
`PRINT_START` or `PRINT_END`, so a profile written for another Klipper printer that uses those
names will not run NebulaOS's preparation.

## Step-by-step in OrcaSlicer

1. Open the printer settings (the edit icon next to the printer name), tab **Machine G-code**.
2. Replace everything in **Machine start G-code** with:

   ```gcode
   START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]
   ```

3. Replace everything in **Machine end G-code** with:

   ```gcode
   END_PRINT
   ```

4. In the print settings, tab **Others**, tick **Label objects**. NebulaOS uses the object
   outlines to probe only the area the print covers, to purge next to it, and to let you
   [cancel one object](Printing#cancelling-one-object-out-of-several) during a print.
5. Save the printer profile.

Leave out the heating, homing, mesh and purge lines a stock Creality profile may have had:
`START_PRINT` does all of that itself, in the right order.

## What START_PRINT does for you

In order: checks that filament is loaded, starts heating, homes, waits for the bed, probes a
fresh bed mesh of the print area, parks next to the print, waits for the nozzle and draws a
purge line. It also starts the [timelapse](Timelapse) watcher, if timelapse is on. The details,
and what each step costs in time, are in [Adaptive meshing and purge](Adaptive-Print-Setup).

`END_PRINT` turns the heaters off, retracts, and parks the nozzle at the back with the bed
forward, so the print is presented to you.

## Optional extras

You can add these to the `START_PRINT` line:

| Add | What it does |
|---|---|
| `BED_SOAK=1` | Waits for the bed to settle before measuring it. Useful for ABS and ASA. `BED_SOAK=0` never waits. |
| `BED_MESH_ADAPTIVE=0` | Probes the whole bed instead of just the print area |
| `BED_MESH_PROFILE=<name>` | Loads a saved mesh instead of probing a new one |

To soak the bed only for ABS and ASA, let OrcaSlicer decide:

```gcode
START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single] {if filament_type[0]=="ABS" or filament_type[0]=="ASA"}BED_SOAK=1{endif}
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

*From `START_PRINT`, `_START_PRINT_BED_MESH` and `END_PRINT` in `etc/nebulaos/klipper/print.cfg`,
firmware `e523e8c`. The OrcaSlicer field names and placeholders are OrcaSlicer's, not
NebulaOS's.*

## Next

[Printing](Printing) - start your first print and watch it.
