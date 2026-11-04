# Calibrate your KE — start to finish

The full run, in the order that actually matters. Do it **top to bottom** and stop when your prints look
the way you want — you don't need every step.

> **Just want the first layer right?** The [Calibration guide](Calibration-Guide) is the short
> version: the Calibration menu's 1-7 (Bed Tramming, Heaters (PID), Axis Twist, Auto Calibration,
> ...), then fine-tune the Z offset on the first print - and when to redo which step.

> **Golden rule: change one thing, then print a test.** If you tweak five settings and the next print is
> worse, you won't know which one did it.

---

## The order that matters

Calibrate from the **machine outward** — mechanical first, then the first layer, then motion quality,
then slicer. Doing it out of order means redoing work.

| Step | Fixes |
|---|---|
| 0. Touch calibration | Tap targets are off on a fresh install |
| 1. Mechanics | Loose hardware that no software can fix |
| 1b. Bed tramming | One corner of the bed higher or lower than the others |
| 2. Temperature (PID) | Inconsistent extrusion from wobbly heater temps |
| 3. Axis Twist | First layer uneven left-to-right |
| 3b. Load cell | Automatic by default (no bottle); Manual = water bottle, 2 min |
| 4. Z-Offset & Bed Mesh | First layer height everywhere (bed mesh + Z-offset, one guided flow) |
| 5. Input shaper | Ghosting/ringing on fast prints |
| 6. E-Steps Calibration | Prints uniformly over- or under-extruded |
| 7. Pressure advance, flow, temp | Corner bulges, stringing, over/under-extrusion |
| 8. Skew correction | Parts that aren't square |
| 9. TMC Autotune | Loud or hot motors (optional) |

The screen's **Tune → Calibration** menu lists the steps that have their own guided screen, in
this order (Run 19): 1 Bed Tramming, 2 Heaters (PID), 3 Axis Twist, 4 Auto Calibration (formerly
Z-Offset & Bed Mesh), 5 Input Shaper, 6 E-Steps, 7 Skew Correction; under OTHER: Load Cell
Calibration, TMC Autotune, Bed Mesh. Mechanics and pressure advance/flow are done elsewhere, so
they don't get a row. (The step numbers on this page are the walkthrough's own.)

**"Which one fixes my problem?"**

| What you see | Most likely fix |
|---|---|
| Tap targets off / need to press slightly away from what you mean | Step 0 — touch calibration |
| First layer uneven left↔right, bed mesh didn't help | Step 3 — Axis Twist |
| First layer uneven all over / patchy adhesion, or too high/low everywhere | Step 4 — Z-Offset & Bed Mesh |
| Ghosting/echoes after sharp corners | Step 5 — Input shaper |
| Prints look uniformly too thin or over-full, not just at corners | Step 6 — E-Steps |
| Bulging corners, blobs, gaps | Step 7 — Pressure advance + flow |
| Parts not square / parallelogram | Step 8 — Skew correction |
| Loud or hot motors | Step 9 — TMC Autotune |
| Layer shift right after pause/resume | See [Troubleshooting](Troubleshooting) |

---

## Step 0 — Touch calibration (do this first on a fresh install)

A fresh install has no touch calibration data, so taps are uncompensated raw coordinates. Run the
9-tap wizard once and the touchscreen becomes accurate.

**Screen:** Settings → Reset → **Reset touch calibration**

The screen shows three crosshairs in turn — tap the centre of each **three times** (lift your finger
between taps; the screen averages the three for accuracy). Takes about 30 seconds. The calibration is
saved automatically and survives reboots.

> Redo this any time tap targets feel noticeably off, or if you change `display_rotate` — the
> calibration coefficients are rotation-specific.

---

## Step 1 — Mechanics first (no software)

Software can't fix loose hardware — it can only paper over it.

- **Belts:** firm. A plucked belt should "thunk", not flap, and both sides should sound about the same
  pitch — a noticeably lower/duller thunk on one side usually means that belt is looser. Slack belts
  cause layer shift and ringing.
- **Gantry:** square. The X bar should be parallel to the bed, not tilted.
- **Bed corners:** run **Calibration → 1 Bed Tramming**. The printer measures the four corners and
  tells you which one to correct, one at a time (a printed shim on the stock rigid spacers, or a screw
  turn on rubber/spring mounts). See [Bed tramming](Bed-Tramming).
- **Bed:** not rocking. Gently push each corner — no play.
- **V-wheels/rails:** snug but not binding. Should spin with light finger pressure.
- **Nozzle:** clean, no plastic blob.

**Done when:** nothing wobbles when you nudge it. Five minutes here saves hours later.

---

## Step 2 — Stable temperatures (PID)

Wobbling hotend or bed temperature = inconsistent extrusion. If your temp graph swings more than
~±1 °C at target, PID-tune. In the **Klipper console** (Mainsail or the Console tab on screen):

```
PID_CALIBRATE HEATER=extruder TARGET=230
PID_CALIBRATE HEATER=heater_bed TARGET=60
SAVE_CONFIG
```

NebulaOS also has `PID_HOTEND` (default 230 °C) and `PID_BED` (default 65 °C), each taking an optional
`TARGET=`; run `SAVE_CONFIG` afterwards.

**Done when:** the temperature holds flat at target on the graph (< ±1 °C).

---

## Step 3 — Axis Twist Compensation

Skip this if your first layer is consistently even from left to right. Do it if you see the classic
KE symptom: first layer is fine in the middle but squished on one side and lifting on the other — and
bed mesh hasn't fixed it.

**Full guide with instructions:** [Axis Twist Compensation](Axis-Twist-Compensation)

In short: **Tune → Calibration → Axis Twist** on the screen runs a 5-point guided paper test across the X axis. The
result corrects the probe readings so the bed mesh is accurate. Takes ~15 minutes, done once.

---

## Step 3b — Load cell (Automatic or Manual)

The automatic Z offset feels the bed with the load cell under the front-left bed screw.
**Calibration → 3 Load Cell** offers two modes. **Automatic** (the default) needs no bottle: the
printer checks the sensor by itself on an empty bed (**Run**), and Z-Offset & Bed Mesh runs the same
check first. **Manual** is the calibration with a 1.5 L water bottle and a kitchen scale (about 2
minutes, nothing moves) - see [Load cell calibration](Load-Cell-Calibration); its value is used until
you choose Automatic again. Redo it after changing the front-left bed corner. Short version:
[Calibration guide](Calibration-Guide).

---

## Step 4 — Z-Offset & Bed Mesh (the big one)

This is 80% of whether prints "look good." **Tune → Calibration → 4 Z-Offset & Bed Mesh** on the
screen does both in one guided run (the NebulaOS workflow `NEBULAOS_AUTO_CALIBRATE`): it cleans the
nozzle, measures the Z offset with the load cell, probes a bed mesh, and saves everything with one
Klipper restart. It takes several minutes and the bed must be empty. In Automatic load-cell mode
(Step 3b) it checks the load cell first; in Manual mode do the bottle calibration before it. It sets
the saved Z offset adjustment back to 0.

![Bed Mesh panel](images/m10-bedmesh.png)

If your slicer calls NebulaOS's `START_PRINT`, each print also probes a fresh mesh of just the print
area, on top of the saved full mesh — see [Adaptive meshing](Adaptive-Print-Setup).

Prefer doing it by hand, or don't want the guided flow? Both halves are still available as separate
tools: `BED_MESH_CALIBRATE` from the console or **Tune → Bed Mesh → Calibrate** on the screen, and the
live baby-step readout on the print-status screen or **Tune → Z Offset** (0.01–0.05 mm nudges: lines not
fusing/gaps = too high, lines translucent/flat = too low, squished and fused with no gaps = correct).

**Done when:** the first layer is uniform with no gaps, and it stays that way print after print.

---

## Step 5 — Input shaper (kill ringing/ghosting)

Those faint echoes trailing sharp corners are vibration. Input shaping cancels them.

**The accelerometer is the Creality one for this printer.** NebulaOS configures an ADXL345 on
the KE's own SPI wiring - the same wiring the stock firmware uses - and drives it with
**upstream Klipper's `[adxl345]` and `[resonance_tester]`**, not Creality's patched versions.
So the accelerometer you would use on stock is the accelerometer you use here.

Two values are tuned for this printer rather than left at Klipper's defaults: the test runs to
80 Hz at 50 mm/s² per Hz, because this board's dual-core MIPS SoC produced *"Timer too close"*
shutdowns near 80 Hz at a higher rate. The fitted results sit well below that ceiling
(`machine.cfg`, firmware `ba98eec`).

**On the screen:** Tune → Calibration → **5 Input Shaper** (the NebulaOS workflow
`NEBULAOS_INPUT_SHAPER_CALIBRATE`). Have the accelerometer ready. Everything happens on this page, with
no popups:

1. **Show graphs** (on by default, remembered): draws a graph of each axis. Off saves a little time.
   It can only be changed between runs.
2. Tap **Start**. The printer homes. Mount the accelerometer firmly on the toolhead and tap **Continue**.
3. The page shows what is happening: *Shaking X: 45 Hz (5-135 Hz)*, then *Calculating the best shaper
   for X...*, then *Drawing the X graph...*.
4. The X result (shaper type and frequency, remaining vibrations, smoothing, the highest acceleration
   that shaper allows) with its graph. Tap the graph to see it full screen, tap again to close.
   Move the accelerometer firmly onto the bed and tap **Continue**.
5. The same for Y, then the result is saved with one Klipper restart.
6. The end page shows both results and both graphs.

The graph shows the measured vibration (blue), what is left after the chosen shaper (orange) and the
shaper itself (dashed). The latest graphs are also in Mainsail: **Machine** → config folder
`input_shaper/` (`shaper_x.png`, `shaper_y.png`). If a graph cannot be drawn, the page says why;
the calibration itself still finishes. **Cancel** stops the run. From Mainsail or the console
the run draws no graphs; `NEBULAOS_INPUT_SHAPER_CALIBRATE GRAPHS=1` draws them.

**Done when:** a fast corner-test print shows no echoes. If it does, try a different shaper type.

---

## Step 6 — E-Steps Calibration

Fixes the *amount* of filament extruded being wrong everywhere — not the corner-specific bulges/gaps
that pressure advance fixes next, but consistent over- or under-extrusion across an entire print (walls
look thicker or thinner than sliced, single-wall prints too fat or too thin).

**On the screen:** Tune → Calibration → **6 E-Steps Calibration** (the NebulaOS workflow
`NEBULAOS_ESTEPS_CALIBRATE`):

1. The hotend heats. Mark the filament at the extruder entry and tap **Start Extrusion**.
2. The printer extrudes a fixed length.
3. Measure how far the mark moved and type it in.
4. The page shows the old and the new `rotation_distance`; **Apply & Save** saves it (Klipper restarts).

Every step's button is on the page itself, no popups.

Repeat once to check. If the result keeps varying between runs rather than converging, that's an
extruder hardware issue (skipping steps, loose grub screw, worn gears), not something calibration can
fix.

**Done when:** the extruded length matches what you commanded within about 0.5 mm.

Do this before dialing in pressure advance and flow (Step 7) — those assume the extruder is already
moving the amount of filament it thinks it is.

---

## Step 7 — Pressure advance, flow & temperature (slicer side)

The last 10%. These fix corner bulges, blobs, gaps, stringing, and over/under-extrusion — but only
after the first layer and motion quality are solid. Tuning these first wastes time.

- **Flow:** start with 0.98 (a modest under-extrusion offset that reduces over-fill) and adjust from
  your first real print. If you did Step 6 (E-Steps), your baseline extrusion accuracy is already
  handled — flow ratio here is just a final, per-filament fudge factor on top of that, not a substitute
  for it.
- **Pressure advance:** print a PA tower or line, find the cleanest corners, dial it in. The on-screen
  **Tune → Fine Tune** lets you adjust PA live while printing.
- **Retraction (stringing):** if you're getting fine hair-like strings between parts, that's usually a
  retraction problem, not pressure advance. Most slicer profiles already retract in the gcode directly,
  which this app doesn't control. If your slicer's retraction *type* is instead set to "Firmware"
  (`G10`/`G11`), you can adjust retraction length/speed live from **Tune → Retraction** — but check
  [Retraction](Screen-Reference#retraction) in the screen reference first, since that panel only does
  anything for gcode sliced that specific way.
- **Temperature:** print a temperature tower from your slicer's test model library and pick the layer
  that looks cleanest.

---

## Step 8 — Skew correction (only if parts aren't square)

If functional parts come out as slight parallelograms, print a calibration square, measure three lengths
with calipers, and enter them on the screen: **Tune → Calibration → Skew Correction**. Full guide: [Skew Correction](Skew-Correction).

**Done when:** a measured test square matches the expected dimensions on both diagonals.

---

## Step 9 — TMC Autotune (optional)

Quieter, cooler stepper motors. **Tune → Calibration → TMC Autotune** — select your motor type, choose a
tuning goal, tap **Save/Restart**. It tunes the stepper drivers and reapplies the settings every boot. Doesn't affect
print quality or dimensions, just reduces noise and heat.

See [TMC Autotune](TMC-Autotune) for the full guide.

---

## After a hardware change

You don't have to redo everything — just the calibrations that the changed part affects.

**The rule:** re-running a calibration overwrites the old value, no "reset first" step. The only time
*reset* matters is if you changed something you can't re-measure right now and the stale value would
be harmful — then set it back to a safe default.

| You changed… | Redo |
|---|---|
| Nozzle / hotend | Z-offset (+ PID if you swapped the heater too) — Z-Offset & Bed Mesh covers this |
| Bed surface, springs, or anything affecting bed height | Z-Offset & Bed Mesh |
| X gantry / anything that could tilt the X axis | **Axis Twist first**, then Z-Offset & Bed Mesh to get a fresh, twist-corrected mesh — doing it the other way round means redoing the mesh anyway, see [Axis Twist Compensation](Axis-Twist-Compensation) |
| Moving mass on an axis (belts, carriage, bed rails) | Input shaper for **that axis only** |
| Extruder gear, hobbed bolt, or hotend melt zone | E-Steps |
| Frame squareness | Skew |
| A heater element | PID |

**Reset commands (rarely needed):** skew → `SET_SKEW CLEAR=1`; active mesh → `BED_MESH_CLEAR`;
disable a shaper axis → set `shaper_freq_x: 0` (or `_y`) in config. For everything else, just
recalibrate — it overwrites.
