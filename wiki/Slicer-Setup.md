# 5. Set up your slicer

## What this guide will help you do

Tell your slicer how to start and end a print on NebulaOS. You do this **once**, before your
first print. Without it, the printer may skip its own preparation - the bed mesh, the purge
line, timelapse - or heat up twice.

## What you need

- A slicer. Any slicer that lets you edit its start and end G-code works; the examples use
  **OrcaSlicer**, which most KE owners use. **NebulaOS ships no slicer profile.** Start from the
  printer profile your slicer offers for the Ender-3 V3 KE, if it has one, and change the two
  fields below.
- A calibrated printer - [4. First calibration](First-Calibration).

## The two lines

NebulaOS has one macro that prepares a print and one that ends it:

| Slicer field | Put exactly this in it |
|---|---|
| Start G-code | `START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single] RETRACT_LENGTH={retraction_length[0]} RETRACT_SPEED={retraction_speed[0]} UNRETRACT_SPEED={deretraction_speed[0]} UNRETRACT_EXTRA_LENGTH={retract_restart_extra[0]}` |
| End G-code | `END_PRINT` |

The words in brackets are OrcaSlicer's own placeholders. When it slices, it replaces them with
the nozzle and bed temperatures of your filament's first layer and with the retraction values of
your profile. Copy the line as it is, all on one line.

`START_PRINT` also sets the speed and flow back to 100 %, so you don't need the
`M220 S100` / `M221 S100` lines that many profiles start with.

**The names matter.** The macros are called `START_PRINT` and `END_PRINT`. NebulaOS has no
`PRINT_START` or `PRINT_END`, so a profile written for another Klipper printer that uses those
names will not run NebulaOS's preparation.

## Step-by-step in OrcaSlicer

1. Open the printer settings (the edit icon next to the printer name), tab **Machine G-code**.
2. Replace everything in **Machine start G-code** with:

   ```gcode
   START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single] RETRACT_LENGTH={retraction_length[0]} RETRACT_SPEED={retraction_speed[0]} UNRETRACT_SPEED={deretraction_speed[0]} UNRETRACT_EXTRA_LENGTH={retract_restart_extra[0]}
   ```

3. Replace everything in **Machine end G-code** with:

   ```gcode
   END_PRINT
   ```

4. In the print settings, tab **Others**, tick **Label objects**. NebulaOS uses the object
   outlines to probe only the area the print covers, to purge next to it, and to let you
   [cancel one object](Screen-Home#exclude-object-screen) during a print.
5. Save the printer profile.

Leave out the heating, homing, mesh and purge lines a stock Creality profile may have had:
`START_PRINT` does all of that itself, in the right order.

## What START_PRINT does for you

In order: checks that filament is loaded, starts heating, homes, waits for the bed, probes a
fresh bed mesh of the print area, parks next to the print, waits for the nozzle and draws a
purge line. It also starts the [timelapse](Timelapse) watcher, if timelapse is on. The details,
and what each step costs in time, are in [Print setup NebulaOS adds](Adaptive-Print-Setup).

`END_PRINT` turns the heaters off, retracts, and parks the nozzle at the back with the bed
forward, so the print is presented to you.

## Firmware retraction (optional)

With the line above, every print starts with the retraction values from your slicer. They are
only used when the slicer leaves the retraction to the printer:

1. In the printer settings, tab **Extruder**, set the retraction length and speeds you want.
2. Tick **Use firmware retraction** (in the same section).
3. Slice and print.

The slicer then writes short `G10`/`G11` commands instead of its own retraction moves, and the
printer retracts with the values `START_PRINT` received. During the print you can fine-tune them
on the screen under **Tune → Retraction**; the next print starts from the slicer's values again.

Without **Use firmware retraction** the slicer retracts by itself, as before, and the values passed
to `START_PRINT` change nothing. If the start G-code passes no retraction values, the printer keeps
its own: 0.6 mm at 35 mm/s, unretract at 30 mm/s.

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

You can add these to the `START_PRINT` line:

| Add | What it does |
|---|---|
| `BED_SOAK=1` | Waits for the bed to settle before measuring it. Useful for ABS and ASA. `BED_SOAK=0` never waits. |
| `BED_MESH_ADAPTIVE=0` | Probes the whole bed instead of just the print area |
| `BED_MESH_PROFILE=<name>` | Loads a saved mesh instead of probing a new one |

To soak the bed only for ABS and ASA, let OrcaSlicer decide:

```gcode
START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single] RETRACT_LENGTH={retraction_length[0]} RETRACT_SPEED={retraction_speed[0]} UNRETRACT_SPEED={deretraction_speed[0]} UNRETRACT_EXTRA_LENGTH={retract_restart_extra[0]} {if filament_type[0]=="ABS" or filament_type[0]=="ASA"}BED_SOAK=1{endif}
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
| The screen says the print isn't sliced for firmware retraction | **Use firmware retraction** is off in the slicer. Turn it on and slice again, or leave it off and let the slicer retract. |

*From `START_PRINT`, `_START_PRINT_BED_MESH` and `END_PRINT` in `etc/nebulaos/klipper/print.cfg`,
and the upload route from `etc/nebulaos/moonraker/nebulaos.conf:16-21`, firmware `bf8fb53`. The OrcaSlicer field names and placeholders are OrcaSlicer's, not
NebulaOS's.*

## Next step

[6. Your first print](Printing) - load filament, print a small test, and tune the first layer.

Need help? [Troubleshooting](Troubleshooting) · How this works: [Print setup NebulaOS adds](Adaptive-Print-Setup)
