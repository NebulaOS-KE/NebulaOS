# Improve your prints

Start from what you see on the print. Each row names the most likely fix and where to find it.
Nearly everything here is a guided page under **Tune → Calibration**; the details of each are in
[Calibration explained](Calibration-Explained).

**First check the basics:** the slicer calls `START_PRINT` and `END_PRINT`
([Setting up your slicer](Slicer-Setup)), the bed is clean (no fingerprints, no grease), and the
nozzle has no plastic blob on it.

## First-layer problems

The first layer decides most prints. Watch it go down and compare with the descriptions:

| What you see | What it means | The fix |
|---|---|---|
| Lines stay round, do not fuse, gaps between them; the print lifts or comes loose | The nozzle is **too high** | While it prints: **Tune → Z Offset** (or tap the Z value on the print screen) and **lower** in 0.01 mm steps. It is saved for the next print. [How](Calibration-Explained#fine-tuning-on-the-first-print) |
| Lines flat and see-through, rough or scraped, plastic piling up beside the nozzle | The nozzle is **too low** | The same, but **raise** |
| Too high or too low everywhere, and nudging does not hold from print to print | The Z offset itself is off | **Tune → Calibration → 4 Auto Calibration** (empty bed, about 7 minutes). [Auto Calibration](Calibration-Explained#auto-calibration-z-offset-and-bed-mesh) |
| Good in one area, too thick or too thin in another | The bed is uneven, and the mesh is not keeping up | Check the print used `START_PRINT` (it measures a fresh mesh for each print). Then **1 Bed Tramming**, then **4 Auto Calibration**. [Bed tramming](Calibration-Explained#bed-tramming) |
| One corner always worse than the others | That corner is high or low | **1 Bed Tramming** - it tells you which corner and by how much |
| Squished on one side (left or right), lifting on the other, and a new mesh does not help | The X gantry twists slightly | **3 Axis Twist**, then **4 Auto Calibration**. [Axis Twist](Calibration-Explained#axis-twist) |
| Poor adhesion everywhere although the height looks right | Bed surface or temperature | Clean the bed, check the slicer's bed temperature for the filament. Warping materials (ABS, ASA): a bed soak - [Print setup NebulaOS adds](Adaptive-Print-Setup#bed-soak) |
| The Z offset drifts: right today, wrong after a restart | The adjustment was not saved, or something changed at the front-left corner | Look at **Tune → Z Offset**: it should say *saved*. After work on the front-left corner: **Load Cell Calibration**, then **4 Auto Calibration**. [Load cell](Calibration-Explained#load-cell-calibration) |
| Auto Calibration fails at the load cell or the Z offset | The load cell check does not pass | **Tune → Calibration → Load Cell Calibration** shows why; Manual mode with a water bottle is the fallback |

The **Calibration** menu also says when something needs redoing: an orange *Redo:* line under a
row means a change since then has made it stale.

## After the first layer

| What you see | The fix |
|---|---|
| Faint echoes trailing sharp corners on fast prints (ringing, ghosting) | **5 Input Shaper**. [Input Shaper](Calibration-Explained#input-shaper) |
| Walls uniformly too thick or too thin, everywhere | **6 E-Steps**. [E-Steps](Calibration-Explained#e-steps-rotation-distance) |
| Parts are parallelograms; diagonals differ | **7 Skew Correction**. [Skew Correction](Calibration-Explained#skew-correction) |
| Bed or nozzle temperature swinging around its target | **2 Heaters (PID)**. [Heaters (PID)](Calibration-Explained#heaters-pid) |
| Loud or warm motors | **TMC Autotune** (optional). [TMC Autotune](Calibration-Explained#tmc-autotune) |
| Corner bulges, blobs, stringing, wrong flow | Per filament, in the slicer: see [Flow, pressure advance and temperature](Calibration-Explained#flow-pressure-advance-and-temperature) |

## What NebulaOS adds to every print

The adaptive mesh, purge line, optional bed soak and firmware retraction:
[Print setup NebulaOS adds](Adaptive-Print-Setup).

## Next

- [Calibration explained](Calibration-Explained) - every routine in detail
- Need help? [Troubleshooting](Troubleshooting)
