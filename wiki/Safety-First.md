# Safety first

## What this page will help you do

Understand the few things that can actually hurt you or damage your printer, so
that nothing in this manual takes you by surprise. Please read it before you install NebulaOS.

## Switching systems is safe, including with the power switch

**You cannot permanently break the printer by switching between NebulaOS and Creality's
system.** An earlier version of this page said otherwise. It was wrong, and this section
replaces it.

Here is what actually happens. The printer's mainboard has its own small piece of firmware,
separate from the system NebulaOS replaces. Creality's system installs its own version of that
firmware when it starts from cold. **NebulaOS does the same in the other direction:** at every
boot it checks what the mainboard is running, and if it finds a known Creality version it
reinstalls its own automatically.

So each system puts back the mainboard firmware it needs, by itself, and switching back and
forth - power switch included - is recoverable without your intervention.

A detail worth knowing if you ever install mainboard firmware yourself: NebulaOS will **not**
overwrite firmware it does not recognise. It reinstalls only when it finds a known Creality
version. Anything you installed deliberately is left alone.

### The one thing worth waiting for

**Do not switch the printer off while mainboard firmware is being installed.** It is the one
moment in normal use where cutting power leaves you with a job to finish rather than a printer
that just works.

**It is not permanent, and it does not need a computer.** The mainboard holds two separate
things: a small built-in loader that Creality put there, and the firmware on top of it that
actually runs the printer. Installing firmware replaces the second one - the loader itself is
never written, which is what makes this recoverable.

So if power is cut partway, the printer will not print, because the firmware on top is
incomplete. The loader is still there, and NebulaOS can still talk to it. The screen notices
and offers the fix itself: *"The firmware was written, but Klipper does not reach the
mainboard. Reinstall the built-in MCU firmware?"* Accept, and it writes it again.

You can also do it whenever you like from **Settings → Printer → MCU firmware → Reinstall
built-in firmware**.

You will know when an install is happening, because the screen says so - it tells you not to
switch off, and that Klipper is stopped. It takes a short time. Waiting for it saves you the
reinstall; it does not save the printer.

[Mainboard firmware](Mainboard-Firmware) explains this in full, including how to reinstall it.

## Hot and moving parts

- The **nozzle** reaches 300 °C and the **bed** 100 °C. Both stay dangerously hot for several
  minutes after a print ends, and neither looks hot.
- Several calibrations move the printhead and the bed **without warning you first**. Keep
  hands, hair, cables and tools out of the way before you start one, and do not reach in to
  tidy something while a calibration is running.
- A few calibrations do not move or heat anything at all. Each calibration page says which
  kind it is, at the top.

## Electrical

- Unplug the printer at the wall before opening any cover or touching wiring.
- The printer's power supply holds a charge after it is unplugged. If you are not comfortable
  working inside mains equipment, do not.

## Fire

Never leave a print running in a room you are not in, or overnight. A 3D printer is a heater
with moving parts, and a working smoke alarm in the same room is a sensible precaution.

## Before you install anything

- **You can go back.** NebulaOS installs into the printer's second system slot and leaves your
  current system in the first one. [Going back to your old firmware](Going-Back) explains how
  to return.
- **Your print files and settings survive a slot switch.** They live on a separate data area
  that both systems share.
- **A full USB recovery does not.** That procedure rewrites the printer from scratch and
  erases your settings, prints and calibration. It is the last resort, not a routine step.

## What this manual promises you

- No step asks you to do something without saying what it will do.
- Anything that can lose data says so before you do it, not after.
- Every procedure names what you should see at each stage, so you can tell whether a step
  worked rather than guessing.
