# Print setup NebulaOS adds

*Setting up a slicer for the first time? The short version is [Setting up your slicer](Slicer-Setup).*

What NebulaOS itself does around every print, and how to switch each part: the adaptive bed mesh,
smart park and purge line, the optional bed soak, firmware retraction, and where the nozzle ends
up. For general tuning - flow, pressure advance, speed, temperature - use the
[Klipper](https://www.klipper3d.org/Pressure_Advance.html) and
[OrcaSlicer](https://github.com/SoftFever/OrcaSlicer/wiki/Calibration) guides; NebulaOS does not
change how those work.

## Adaptive mesh, smart park and purge line

NebulaOS prepares the bed for each print in its `START_PRINT` macro:

- **Adaptive bed mesh** — probes only the area the print covers instead of the whole bed, using
  Klipper's own `BED_MESH_CALIBRATE ADAPTIVE=1`.
- **Smart park** — parks the nozzle next to the print while it heats.
- **Line purge** — draws a purge line just in front of the print area.

All three use the print's object outlines (Klipper `[exclude_object]`), so the slicer must write
object labels. These macros are part of the NebulaOS image (`/etc/nebulaos/klipper/print.cfg`), not
of NebulaScreen; this page describes how to use them.

> **Do [Axis Twist](Calibration-Explained#axis-twist) first** if the first layer is uneven left to
> right. A denser mesh does not help when the probe readings are off.

### Step 1 - Turn on object labels in the slicer

In **OrcaSlicer**: print settings → **Others** → tick **Label Objects**. Other slicers have a similar
option. NebulaOS's `moonraker.conf` has `enable_object_processing: True` (keep it): Moonraker reads the
object outlines from every uploaded file and passes them to Klipper, and it adds the labels itself
when a slicer marks its objects only in comments. The NebulaOS build checks that the shipped
`moonraker.conf` keeps this setting on.

The same setting enables **Exclude Object** on the print status screen: if one part fails, you can drop
it and let the rest keep printing.

### Step 2 - Call `START_PRINT` from the start G-code

In OrcaSlicer: printer profile → **Machine G-code** → **Machine start G-code**:

```gcode
START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]
```

To soak the bed only for filaments that warp (ABS, ASA), let the slicer add `BED_SOAK=1`:

```gcode
START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single] {if filament_type[0]=="ABS" or filament_type[0]=="ASA"}BED_SOAK=1{endif}
```

`START_PRINT` then does, in order:

1. Checks the filament sensor; with no filament it stops with a message.
2. Starts heating the nozzle to 150 °C (below oozing) and the bed to `BED_TEMP`.
3. Homes if needed, moves to Z 50 while the bed heats, and waits for the bed.
4. Bed warp stabilisation (the [bed soak](#bed-soak)), **off by default**.
5. Clears the old mesh and probes a new one — adaptive, unless the print covers more than 75 % of the
   bed, in which case it probes the full bed.
6. Parks next to the print, waits for the nozzle to reach `EXTRUDER_TEMP`, and purges a line in front
   of the print (or along its left side when there is no room in front).

While it runs, speed and acceleration are capped for probing and restored afterwards.

If the parameters are left out, `BED_TEMP` defaults to 65 and `EXTRUDER_TEMP` to 230 — always pass
both from the slicer.

### Options

| Parameter | Effect |
|---|---|
| `BED_MESH_ADAPTIVE=0` | Probe the full bed instead of the print area |
| `BED_MESH_PROFILE=<name>` | Load a saved mesh instead of probing |
| `BED_SOAK=1` | Bed warp stabilisation (soak) before the mesh; `BED_SOAK=0` never soaks |

Remove any `BED_MESH_PROFILE LOAD=...` line from older start G-code: loaded after `START_PRINT`, it
would replace the fresh mesh.

Without object labels there is no print area to adapt to: expect a full-bed mesh, and park and purge
near the bed's front-left corner. Turn labels on.

## Bed soak

Some beds keep moving for a while after they reach temperature, and a mesh measured too early is
already wrong when the print starts. The **bed warp stabilisation** waits before the mesh: 8 s
per °C the bed had to heat (about 11 minutes from room temperature to 85 °C). If the bed was
already above three quarters of its target, only the remaining degrees count. Without it the
console says *"Skipping bed warp stabilisation (off by default - add BED_SOAK=1 to START_PRINT in
the slicer to soak the bed)"*.

| How | Effect |
|---|---|
| `BED_SOAK=1` in the start G-code | Soak this print |
| `BED_SOAK=0` | Never soak this print |
| No `BED_SOAK` | The switch `Bed_Warp_Stabilisation` decides. Mainsail shows it with the other outputs; it is off by default and **remembered** - on stays on, also across Klipper restarts, until you switch it off |

The OrcaSlicer line above with `{if filament_type[0]=="ABS" ...}` soaks only for the filaments
that need it. `END_PRINT` leaves the bed heated only when the switch is on **and** the variable
`end_print_keep_bed_heated` is set (it is off by default).

*From `print.cfg:55-65`, `74-78`, `240-252` and `796-824`, firmware `dc868e3`.*

## Nozzle clean

`START_PRINT` does **not** clean or wipe the nozzle. The nozzle clean is a step of
[Auto Calibration](Calibration-Explained#auto-calibration-z-offset-and-bed-mesh), before the Z
offset is measured. To run it on its own, use the macro `NEBULAOS_NOZZLE_CLEAN` (Mainsail lists it
with the NebulaOS macros).

*`START_PRINT` is `print.cfg:158-278`; `NEBULAOS_NOZZLE_CLEAN` is `calibration.cfg:109-112`,
firmware `dc868e3`.*

## Firmware retraction

NebulaOS configures Klipper's `[firmware_retraction]`: retract 0.6 mm at 35 mm/s, unretract at
30 mm/s with no extra length (`machine.cfg:30-34`, firmware `dc868e3`). It is used **only** by files
sliced with the slicer's retraction set to firmware retraction (`G10`/`G11`). Most slicer profiles
retract in the G-code themselves, and then these values do nothing.

**Tune → Retraction** changes the values live while printing; the changes are not saved and a
Klipper restart goes back to the configured ones. To change them for good, put a
`[firmware_retraction]` section in `printer.cfg`. Details: [Tune → Retraction](Screen-Tune#retraction).

## Settings

The purge and park values are variables of the macro `_KAMP_Settings` (for example
`variable_purge_amount`, `variable_purge_margin`, `variable_flow_rate`, `variable_smart_park_height`),
and the start/end behaviour is in `_START_END_PARAMS` (for example
`variable_full_bed_mesh_above_percentage_full`, `variable_start_preheat_nozzle_temp`). Both are in
`/etc/nebulaos/klipper/print.cfg` (on the printer also as `config/nebulaos/print.cfg`, which an
update replaces - override a variable from `printer.cfg` instead).

At the end of a print (`END_PRINT`), after a cancel (`CANCEL_PRINT`) and at the end of the cooldown,
the nozzle parks at the rear left (X2 Y218) with the bed forward, so the print is presented to you.
A pause or filament change parks as before.

## Credits

The purge and park macros derive from
[pellcorp/creality](https://github.com/pellcorp/creality) ("SimpleAF") and, through it, from
[KAMP](https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging) (GPL-3.0). The adaptive mesh
itself is Klipper's native `ADAPTIVE=1`.
