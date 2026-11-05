# First-time setup

## What this guide will help you do

Take a printer that has just had NebulaOS installed and get it to a good first print. This is
the overview that links the pieces together in the right order.

Set aside **about an hour** for the calibrations, most of which is waiting rather than working.

## What you need

- A printer running NebulaOS - see [Installing NebulaOS](Installing-NebulaOS).
- Your Wi-Fi name and password.
- Filament you intend to print with.
- A sheet of paper, and a ruler or caliper. A few calibrations ask for these.
- An empty, clean bed.

## Before you begin

Read [Safety first](Safety-First) if you have not. The relevant part here: **several
calibrations move the printhead and bed without warning you first.** Keep hands and tools
clear once you start one.

Your old calibrations do not carry over. Even if the printer was calibrated under its previous
firmware, NebulaOS starts fresh, and skipping this leaves you chasing first-layer problems
that calibration would have fixed in an hour.

## The order

### 1. Connect to Wi-Fi

**Settings → Connections → Wi-Fi networks.** Full steps:
[Connecting to Wi-Fi](Connecting-To-WiFi).

Do this first, because it makes everything afterwards easier - updates, uploading files, and
watching the printer from another room.

### 2. Open Mainsail and bookmark it

Read the printer's address from **Settings → Connections**, then open it in a browser. Full
steps: [Opening Mainsail](Opening-Mainsail).

### 3. Calibrate, in order

All calibrations live under **Tune → Calibration**, and they are **numbered in the order a new
printer needs them**. Work down from the top.

| # | Menu row | What you need | Roughly how long |
|---|---|---|---|
| 1 | **Bed Tramming** | An empty bed, maybe a printed shim | 5-15 min |
| 2 | **Heaters (PID)** | An empty, cool printer | Hotend a few minutes, bed longer |
| 3 | **Axis Twist** | A sheet of paper | About 5 min |
| 4 | **Auto Calibration** | An empty bed, no tools | About 7 min |
| 5 | **Input Shaper** | Nothing - uses the built-in accelerometer | About 5 min |
| 6 | **E-Steps** | A ruler or caliper, and a marker | About 5 min |
| 7 | **Skew Correction** | A printed test part and a caliper | About 30 min |

Below those, under **OTHER**, are three you do not need on day one: **Load Cell
Calibration**, **TMC Autotune** (optional, makes the motors quieter) and **Bed Mesh** (view or
re-measure).

**You do not have to do all seven before printing.** Numbers 1 to 4 get most printers to a
good first layer. Skew Correction in particular is worth leaving until you have a reason.

Detail for each one: [Calibration guide](Calibration-Guide) for the short version,
[Calibration walkthrough](Calibration-Explained) for the full background.

### 4. Read the status line under each row

This is the part people miss, and it is the most useful thing on the screen. Every calibration
row tells you where you stand:

- **Green**, for example *"Done 24 Oct - Z offset 1.752 mm, mesh range 0.16 mm"* - when it
  last ran, and its result.
- **Grey** - not done yet, with a one-line description and how long it takes.
- **Orange with a bar on the left**, for example *"Redo: Axis Twist changed"* - something you
  did since has invalidated it, so run it again.

That last one matters. The calibrations depend on each other, and the printer tracks the
dependencies for you. Saving **Axis Twist** marks **Auto Calibration** as needing a redo.
Adding a shim at the front-left corner during **Bed Tramming** marks both **Load Cell
Calibration** and **Auto Calibration**. Running the calibration again clears the flag.

If your printer's NebulaOS does not keep a calibration history, the rows show only the
descriptions.

### 5. Your first print

1. Set up your slicer once: its start and end G-code must call NebulaOS's `START_PRINT` and
   `END_PRINT`. Two lines - [Setting up your slicer](Slicer-Setup).
2. Upload a G-code file in Mainsail, or put it on a USB stick and use the printer's file
   browser.
3. Load filament - see [Filament](Filament).
4. Start the print - see [Printing](Printing).
5. Watch the first layer. While it prints, **Tune → Z Offset** or **Fine Tune** adjusts the
   nozzle height live. This is normal and expected: the first layer is tuned by watching it,
   not by calculating it.

Pick something small and simple for the first one. A 20 mm calibration cube tells you more in
20 minutes than a six-hour model tells you in six hours.

![The Calibration menu, numbered in the order a new printer needs them](images/m19-calibration.png)

*The Calibration menu. The rows are numbered in the order to do them.*

![Calibration rows showing their status lines with dates and results](images/m19b-calibration-status.png)

*The status lines in use: what ran, when, and what it measured.*

![The Z Offset screen after saving](images/m16-zoffset-saved.png)

*Live Z offset adjustment - the screen you use while watching the first layer.*

## Expected result

- The printer is on your network and reachable in a browser.
- Calibration rows 1 to 4 show green status lines with results.
- A first print whose first layer is even and stuck down.

## Troubleshooting

| What happens | What to do |
|---|---|
| A calibration refuses to start | Something else is running, or a dependency is unmet. Read the row's status line. |
| A calibration fails partway | Note the message and see [Troubleshooting](Troubleshooting). Nothing is saved from a failed run. |
| The first layer is squished or lifting | Adjust live with **Tune → Z Offset** while it prints. |
| One side is good, the other is not | That is the classic **Axis Twist** symptom - row 3. |
| Parts come out as parallelograms | **Skew Correction** - row 7. |

## If you want to start over

Nothing here is irreversible. **Settings → Reset** can clear the screen's settings or do a
clean NebulaOS reset, and the boot slot swap puts your old firmware back. See
[Resetting](Resetting) and [Going back](Going-Back).

## Next

- **Next step:** [Setting up your slicer](Slicer-Setup), if you have not done it yet - then
  [Printing](Printing)
- [Printing](Printing) - everyday use
- [Screen reference](Screen-Reference) - what every button does
- [Updating NebulaOS](Updating-NebulaOS) - staying current
