# The NebulaOS manual

NebulaOS is replacement software for the **Creality Ender-3 V3 KE** 3D printer. It replaces
what Creality installed with a system built around Klipper, Moonraker, Mainsail and its own
touchscreen app, NebulaScreen.

This manual is for the person using the printer. It assumes no Linux, no SSH, no Klipper and
not much 3D printing experience. Where a technical word is unavoidable it is explained the
first time it appears, and [Words you will see](Glossary) collects them all.

## New here? Follow this path, in order

Each page ends with a **Next step** link to the one after it, and the sidebar numbers them the
same way.

1. **[What NebulaOS is](What-NebulaOS-Is)** - what it replaces, and whether it is for you.
2. **[Supported hardware](Supported-Hardware)** - check your printer, and what else you need.
3. **[Safety first](Safety-First)** - the hot and moving parts, and what is and is not
   risky about switching systems. Five minutes, before you install anything.
4. **[Two system slots](Two-System-Slots)** - what installing does to the system you have now.
5. **[Installing NebulaOS](Installing-NebulaOS)** - how to put NebulaOS on the printer, and
   how to get back to what you had before.
6. **[First-time setup](First-Time-Setup)** - the overview of steps 7 to 12.
7. **[Connecting to Wi-Fi](Connecting-To-WiFi)**
8. **[Opening Mainsail](Opening-Mainsail)** - the printer in your web browser.
9. **[Calibration guide](Calibration-Guide)** - the Calibration menu, top to bottom. The
   [Calibration walkthrough](Calibration-Explained) is the long version.
10. **[Setting up your slicer](Slicer-Setup)** - **do not skip this.** Two lines of start and
    end G-code, once, before you print anything. Without them the print skips the mesh and
    purge line that calibration prepared for.
11. **[Filament](Filament)** - loading it.
12. **[Printing](Printing)** - your first print.
13. **[Updating NebulaOS](Updating-NebulaOS)** - staying current.

## Already running NebulaOS?

| What you want | Where to go |
|---|---|
| Learn what a button on the screen does | [Screen reference](Screen-Reference) |
| Get the first layer right | [Calibration guide](Calibration-Guide) |
| Set up the slicer's start and end G-code | [Setting up your slicer](Slicer-Setup) |
| Start, pause or cancel a print | [Printing](Printing) |
| Load or change filament | [Filament](Filament) |
| Watch the print from your phone | [Camera](Camera) |
| Record a video of a print | [Timelapse](Timelapse) |
| Know what an update replaces, and keep Creality | [Two system slots](Two-System-Slots) |
| Install a newer NebulaOS | [Updating NebulaOS](Updating-NebulaOS) |
| See what this printer has printed | [Statistics](Screen-Printer#statistics-panel) |
| Undo a setting, or start fresh | [Resetting](Resetting) |
| Something is broken | [Troubleshooting](Troubleshooting) |
| The printer will not start | [Recovery](Recovery) |

## More than a touchscreen replacement

NebulaOS replaces the KE's original Linux system with a newer real-time kernel,
hardware-specific drivers, official Klipper and its own system management tools. It includes
memory and performance safeguards, independent application updates, and recovery mechanisms
designed around the printer's hardware.

Curious what happens behind the scenes? Read [Under the hood](Under-the-Hood).

## What NebulaOS gives you

- A touchscreen app on the printer's own 480x272 display, with print control, temperatures,
  fans, LED, homing and jogging, a file browser that reads USB sticks, and a 3D bed mesh you
  can rotate and zoom.
- A **Calibration** menu that walks you through each calibration in the order a new printer
  needs them, and remembers which ones you have done.
- Live tuning while a print runs: speed, flow, Z offset and pressure advance.
- **Mainsail** in your web browser, for uploading files and controlling the printer from a
  computer or phone.
- **Statistics** for the printer's whole life - including what it printed before NebulaOS was
  installed, read from the system that was there before.
- Power-loss recovery, so a print can continue after the power goes out.
- Two system slots, so a bad update can be undone by starting the other one -
  [what that means for your old system](Two-System-Slots).
- Camera support, including the settings of Creality's own Nebula Camera, and **timelapse**
  recording that needs no slicer changes.

## What NebulaOS does not do

- It only supports the **Creality Ender-3 V3 KE**. See
  [Supported hardware](Supported-Hardware).
- It is not Creality's software and is not supported by Creality. Installing it is your
  decision and your responsibility.
- This manual describes **NebulaOS 1.0.1**.

## How to read this manual

Every procedure page follows the same shape: what the guide is for, what you need, what to
check before you start, numbered steps, what you should see, what to do if it goes wrong, and
how to undo it. You should never have to guess what a step means or whether it worked.

If a page tells you to do something and you cannot find the button it names, that is a bug in
this manual. Please report it:
[github.com/NebulaOS-KE/NebulaOS/issues](https://github.com/NebulaOS-KE/NebulaOS/issues).
