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
  Stock Creality lines such as `SET_GCODE_VARIABLE MACRO=PRINTER_PARAM ...`, `SMART_PARK` and
  `LINE_PURGE` do not exist on NebulaOS: Klipper stops the print with *Unknown command*. A fixed
  wait such as `G4 P120000` before the mesh becomes `BED_SOAK=1` on the start line.
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

### What START_PRINT and END_PRINT run

The full text of both macros, as NebulaOS 1.0.3 ships them (`print.cfg`, unchanged since 1.0.2).
You find the same file in Mainsail under `config/nebulaos/print.cfg`.

<details>
<summary><code>START_PRINT</code></summary>

```ini
[gcode_macro START_PRINT]
# G112 (2026-10-31): the step the start sequence is in, for the screen's step
# list ("" = not starting): preparing, heating_bed, soak, mesh,
# heating_nozzle, purge. soak_seconds: the soak's length (_WARP_STABILISE).
variable_step: ""
variable_soak_seconds: 0
variable_max_velocity: 0
variable_max_accel: 0
variable_square_corner_velocity: 0
gcode:
  # cancel any outstanding end-print cooldown
  UPDATE_DELAYED_GCODE ID=wait_for_end_print_cooldown DURATION=0

  # if a cooldown session was still in progress we want to forcefully end it
  {% set started_cooldown = printer["gcode_macro END_PRINT"].started_cooldown|default(false) %}
  {% if started_cooldown %}
    SET_GCODE_VARIABLE MACRO=END_PRINT VARIABLE=started_cooldown VALUE=False
    {% if "xyz" in printer.toolhead.homed_axes %}
      M84
    {% endif %}
    M107
    {% if 'fan_generic auxiliary' in printer.configfile.settings %}
      SET_FAN_SPEED FAN=auxiliary SPEED=0
    {% endif %}
  {% endif %}

  {% set runout_sensor = printer["gcode_macro _CLIENT_VARIABLE"].runout_sensor|default("") %}
  {% if runout_sensor != "" and printer[runout_sensor] != null %}
    {% set runout_sensor_id = (runout_sensor.split(" "))[1] %}
    SET_FILAMENT_SENSOR SENSOR={runout_sensor_id} ENABLE=1
    {% set filament_detected = printer[runout_sensor].filament_detected %}
  {% else %}
    {% set filament_detected = true %}
  {% endif %}

  {% if not filament_detected %}
    RESPOND TYPE=error MSG='Filament not detected, Print aborted! "{runout_sensor_id}" detects no filament, please load filament.'
    RESPOND TYPE=command MSG="action:prompt_begin Print aborted !!!"
    RESPOND TYPE=command MSG='action:prompt_text "{runout_sensor_id}" detects no filament, please load filament.'
    RESPOND TYPE=command MSG="action:prompt_footer_button Ok|RESPOND TYPE=command MSG=action:prompt_end|info"
    RESPOND TYPE=command MSG="action:prompt_show"
    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=step VALUE='""'
    CANCEL_PRINT
  {% else %}
    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=step VALUE='"preparing"'
    # 1.0.2: speed and flow back to 100 % (a tune from the last print would
    # otherwise carry over), so the start G-code needs no M220/M221.
    M220 S100
    M221 S100
    # 1.0.2: firmware retraction values from the slicer, used by G10/G11 when
    # the slicer has "Use firmware retraction" on. The OrcaSlicer start G-code
    # passes its placeholders retraction_length, retraction_speed,
    # deretraction_speed and retract_restart_extra (index 0, see the wiki page
    # Adaptive-Print-Setup; no curly braces here, the template renders them).
    # A value that is not passed keeps the current one ([firmware_retraction]
    # in machine.cfg after a restart, or what the screen set). A speed below
    # 1 mm/s (Klipper's minimum) is not set; an unretract speed of 0 is the
    # slicer's "same as retraction" and takes RETRACT_SPEED.
    {% set fr_args = "" %}
    {% if params.RETRACT_LENGTH is defined %}
      {% set fr_args = fr_args ~ " RETRACT_LENGTH=" ~ ([params.RETRACT_LENGTH|float, 0.0]|max) %}
    {% endif %}
    {% set fr_speed = params.RETRACT_SPEED|default(0)|float %}
    {% if fr_speed >= 1 %}
      {% set fr_args = fr_args ~ " RETRACT_SPEED=" ~ fr_speed %}
    {% endif %}
    {% set fr_unspeed = params.UNRETRACT_SPEED|default(0)|float %}
    {% if fr_unspeed < 1 %}
      {% set fr_unspeed = fr_speed %}
    {% endif %}
    {% if fr_unspeed >= 1 %}
      {% set fr_args = fr_args ~ " UNRETRACT_SPEED=" ~ fr_unspeed %}
    {% endif %}
    {% if params.UNRETRACT_EXTRA_LENGTH is defined %}
      {% set fr_args = fr_args ~ " UNRETRACT_EXTRA_LENGTH=" ~ ([params.UNRETRACT_EXTRA_LENGTH|float, 0.0]|max) %}
    {% endif %}
    {% if fr_args != "" and 'firmware_retraction' in printer %}
      SET_RETRACTION{fr_args}
      RESPOND MSG="Firmware retraction from the slicer:{fr_args}"
    {% endif %}
    # record initial bed temp for warp stabilisation calculation
    {% set current_bed_temp = printer.heater_bed.temperature %}

    {% set BED_TEMP=params.BED_TEMP|default(65)|float %}
    {% set EXTRUDER_TEMP=params.EXTRUDER_TEMP|default(230)|float %}

    {% set max_velocity = printer.toolhead.max_velocity %}
    {% set max_accel = printer.toolhead.max_accel %}
    {% set square_corner_velocity = printer.toolhead.square_corner_velocity %}
    {% set start_max_velocity = [printer["gcode_macro _START_END_PARAMS"].start_max_velocity, max_velocity]|min %}
    {% set start_max_accel = [printer["gcode_macro _START_END_PARAMS"].start_max_accel, max_accel]|min %}
    {% set start_square_corner_velocity = [printer["gcode_macro _START_END_PARAMS"].start_square_corner_velocity, square_corner_velocity]|min %}
    {% set preheat_nozzle_temp = printer["gcode_macro _START_END_PARAMS"].start_preheat_nozzle_temp %}

    # save the current limits so we can restore them in END and CANCEL print
    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=max_velocity VALUE={max_velocity}
    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=max_accel VALUE={max_accel}
    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=square_corner_velocity VALUE={square_corner_velocity}

    M104 S{preheat_nozzle_temp}  # start heating nozzle but only to just before oozing
    M140 S{BED_TEMP}  # start heating bed dont wait

    {% if max_velocity > start_max_velocity or max_accel > start_max_accel or square_corner_velocity > start_square_corner_velocity %}
      RESPOND TYPE=command MSG='Setting VELOCITY={start_max_velocity} (was {max_velocity}) ACCEL={start_max_accel} (was {max_accel}) SQUARE_CORNER_VELOCITY={start_square_corner_velocity} (was {square_corner_velocity})'
      SET_VELOCITY_LIMIT VELOCITY={start_max_velocity} ACCEL={start_max_accel} SQUARE_CORNER_VELOCITY={start_square_corner_velocity}
    {% endif %}

    # if we ran M84 because of cooldown we can't rely on printer.toolhead.homed_axes
    # (klipper does not update that object for M84 when executing during start print)
    {% if started_cooldown or "xyz" not in printer.toolhead.homed_axes %}
      G28
    {% endif %}

    {% set start_print_bed_heating_move_bed_distance = printer["gcode_macro _START_END_PARAMS"].start_print_bed_heating_move_bed_distance %}
    {% if start_print_bed_heating_move_bed_distance > 0 %}
      G0 Z{start_print_bed_heating_move_bed_distance} F1200
    {% endif %}

    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=step VALUE='"heating_bed"'
    M190 S{BED_TEMP}  # wait for bed temperature before next step

    # G112: BED_SOAK=1 soaks, BED_SOAK=0 skips, no BED_SOAK = the switch (off by default)
    {% set bed_soak = params.BED_SOAK|default(-1)|int %}
    {% if bed_soak < 0 %}
      {% set bed_soak = 1 if printer['output_pin Bed_Warp_Stabilisation'].value == 1 else 0 %}
    {% endif %}
    {% if bed_soak == 1 %}
      SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=step VALUE='"soak"'
    {% endif %}
    _WARP_STABILISE TARGET_TEMP={BED_TEMP} CURRENT_TEMP={current_bed_temp} ENABLE={1 if bed_soak == 1 else 0}

    {% if 'bed_mesh' in printer.configfile.settings %}
      BED_MESH_CLEAR
    {% endif %}

    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=step VALUE='"mesh"'
    _START_PRINT_BED_MESH {rawparams}

    _SMART_PARK  # park the printhead near the print area

    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=step VALUE='"heating_nozzle"'
    M109 S{EXTRUDER_TEMP}  # wait for nozzle temperature before next step

    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=step VALUE='"purge"'
    _LINE_PURGE

    {% if max_velocity > start_max_velocity or max_accel > start_max_accel or square_corner_velocity > start_square_corner_velocity %}
      RESPOND TYPE=command MSG='Restoring VELOCITY={max_velocity} ACCEL={max_accel} SQUARE_CORNER_VELOCITY={square_corner_velocity}'
      SET_VELOCITY_LIMIT VELOCITY={max_velocity} ACCEL={max_accel} SQUARE_CORNER_VELOCITY={square_corner_velocity}
    {% endif %}
    SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=step VALUE='""'
    # Timelapse layer watcher (camera.cfg); does nothing while timelapse is off.
    {% if 'gcode_macro _NEBULAOS_TIMELAPSE' in printer %}
      _NEBULAOS_TIMELAPSE ACTION=START
    {% endif %}
  {% endif %}


# C3 (Z-offset chain review, 2026-10-22): the print's mesh is a throwaway.
# It is calibrated under its own name "adaptive" and never saved, so an
# unrelated SAVE_CONFIG later (load cell, PID, shaper...) can never replace
# the calibrated "default" mesh with the last print's mesh. Pinned Klipper's
# bed_mesh (58bd67db3) names it like this:
#   - the adaptive path applies (objects defined, ADAPTIVE=1): the name is
#     dropped (set_adaptive_mesh -> _profile_name None) and the mesh becomes
#     "adaptive-<hex>" - not staged for saving;
#   - ADAPTIVE=0 (bed usage above full_bed_mesh_above_percentage_full), no
#     objects, or no [exclude_object]: a full mesh under PROFILE - before
#     this fix "default" - and probe_finalize stages it (save_profile ->
#     configfile.set [bed_mesh <name>]) for the next SAVE_CONFIG.
# So PROFILE=adaptive here, then _START_PRINT_BED_MESH_UNSTAGE drops a staged
# [bed_mesh adaptive]. BED_MESH_PROFILE REMOVE only deletes the profile from
# storage (configfile.remove_section + the profiles list); it never calls
# set_mesh, so the mesh the print uses stays loaded (bed_mesh.profile_name
# stays "adaptive"). A [bed_mesh adaptive] saved by hand is removed at the
# next SAVE_CONFIG too: the name is reserved for the print mesh.
# F2 (Run 18): REMOVE of a section staged in this session still leaves
# save_config_pending set (pinned configfile records the removal as a
# pending deletion), so Mainsail would offer a SAVE_CONFIG that changes
# nothing. A full mesh is therefore taken through the adaptive path whenever
# the print defines objects: ADAPTIVE=1 with a margin larger than the bed
# clamps the adapted bounds to exactly mesh_min/mesh_max and keeps
# probe_count (ratio 1.0), i.e. the same points as ADAPTIVE=0, but the name
# is dropped and nothing is staged. Only a print WITHOUT exclude_object
# objects still goes through the named fallback + UNSTAGE above; that
# residual stays cosmetic: saving then writes nothing from the print
# (SAVE_CONFIG writes the autosave config, which no longer holds the
# section). Klipper is pristine upstream, so the pending flag itself is not
# patched.
```

</details>

<details>
<summary><code>END_PRINT</code></summary>

```ini
[gcode_macro END_PRINT]
variable_started_cooldown: False
gcode:
  {% set bed_warp_stabilisation = printer['output_pin Bed_Warp_Stabilisation'].value == 1 %}
  {% set end_print_cool_down = printer["gcode_macro _START_END_PARAMS"].end_print_cool_down %}
  {% set end_print_cool_down_nozzle_temp = printer["gcode_macro _START_END_PARAMS"].end_print_cool_down_nozzle_temp|float %}
  {% set end_print_cool_down_max_bed_temp = printer["gcode_macro _START_END_PARAMS"].end_print_cool_down_max_bed_temp|float %}
  {% set end_print_keep_bed_heated = printer["gcode_macro _START_END_PARAMS"].end_print_keep_bed_heated %}
  {% set runout_sensor = printer["gcode_macro _CLIENT_VARIABLE"].runout_sensor|default("") %}

  # reset this flag just to make sure
  SET_GCODE_VARIABLE MACRO=END_PRINT VARIABLE=started_cooldown VALUE=False
  {% if 'gcode_macro _NEBULAOS_TIMELAPSE' in printer %}
    _NEBULAOS_TIMELAPSE ACTION=STOP
  {% endif %}
  {% if 'nebulaos_power_loss_recovery' in printer %}
    # after a power-loss resume: the frames from before it, back in front
    _NEBULAOS_PLR_TIMELAPSE_MERGE
  {% endif %}
  SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=step VALUE='""'

  _RESTORE_VELOCITY_ACCEL

  {% if 'bed_mesh' in printer.configfile.settings %}
    BED_MESH_CLEAR
  {% endif %}

  {% set current_bed_temp = printer.heater_bed.temperature %}

  {% if runout_sensor != "" %}
    {% set runout_sensor_id = (runout_sensor.split(" "))[1] %}
    SET_FILAMENT_SENSOR SENSOR={runout_sensor_id} ENABLE=0
  {% endif %}

  {% set cancel_retract = printer['gcode_macro _CLIENT_VARIABLE'].cancel_retract %}
  _CLIENT_RETRACT LENGTH={cancel_retract}

  # park in front of aux fan if cooldown
  {% if end_print_cool_down and current_bed_temp < end_print_cool_down_max_bed_temp %}
    _TOOLHEAD_PARK_CANCEL_END_PRINT COOLDOWN=1
  {% else %}
    _TOOLHEAD_PARK_CANCEL_END_PRINT
  {% endif %}

  {% if bed_warp_stabilisation and end_print_keep_bed_heated %}
    RESPOND TYPE=command MSG='Heat bed waiting for next print'
    M104 S0  # turning off the nozzle
  {% else %}
    TURN_OFF_HEATERS
  {% endif %}

  {% if end_print_cool_down and current_bed_temp < end_print_cool_down_max_bed_temp %}
    RESPOND TYPE=command MSG='Waiting for nozzle temp to be below {end_print_cool_down_nozzle_temp}c'

    {% if 'fan_generic auxiliary' in printer.configfile.settings %}
      SET_FAN_SPEED FAN=auxiliary SPEED=0.5
    {% endif %}

    M106 S180

    # flag that we have started the cooldown procedure
    SET_GCODE_VARIABLE MACRO=END_PRINT VARIABLE=started_cooldown VALUE=True
    UPDATE_DELAYED_GCODE ID=wait_for_end_print_cooldown DURATION=1
  {% else %}
    M84
    M107
    {% if 'fan_generic auxiliary' in printer.configfile.settings %}
      SET_FAN_SPEED FAN=auxiliary SPEED=0
    {% endif %}
  {% endif %}
```

</details>

**To add a step** (a nozzle wipe, a light, ...), put your own macro in `config/macros/` and call it
on the line after `START_PRINT` - see [Custom macros and integrations](Macros-And-Integrations#your-own-macros).
You can also copy `START_PRINT` into a macro of your own with a new name, but it then no longer
gets NebulaOS's fixes.

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
| The print stops at the start with *Unknown command* | The start G-code still has stock Creality lines (`PRINTER_PARAM`, `SMART_PARK`, `LINE_PURGE` ...). Replace it with the start line above. |

*From `START_PRINT`, `_START_PRINT_BED_MESH` and `END_PRINT` in `etc/nebulaos/klipper/print.cfg`,
`[firmware_retraction]` in `machine.cfg` and the upload route from
`etc/nebulaos/moonraker/nebulaos.conf:16-21`, firmware `3bdf3ff`; the screen's retraction check
from NebulaScreen `src/printertune_panel.cpp` and `src/utils.cpp`, `fd47cb6`. The OrcaSlicer field
names and placeholders are OrcaSlicer's, not NebulaOS's.*

## Next step

[6. Your first print](Printing) - load filament, print a small test, and tune the first layer.

Need help? [Troubleshooting](Troubleshooting) · How this works: [Print setup NebulaOS adds](Adaptive-Print-Setup)
